"""Small stdlib HTTP server for the hypercore browser view."""

from __future__ import annotations

from functools import partial
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .store import Store


WEB_ROOT = Path(__file__).resolve().parent.parent / "web"


class HypercoreHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, db_path: str, **kwargs):
        self.db_path = db_path
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == "/api/graph":
            self.send_graph()
            return
        if self.path == "/api/version":
            self.send_version()
            return
        if self.path.startswith("/api/material/"):
            self.send_material(self.path.removeprefix("/api/material/"))
            return
        super().do_GET()

    def do_POST(self):
        # Every POST is the operator acting in the viewer (s_a6ea7c7a); the
        # machine drives the CLI verbs instead and never calls these. Each
        # endpoint maps one-to-one onto a verb and spends the same checks.
        routes = {
            "/api/endorse": self.endorse,
            "/api/verdict": self.verdict,
            "/api/amend": self.amend,
            "/api/strike": self.strike,
            "/api/fold": self.fold,
        }
        handler = routes.get(self.path)
        if handler is None:
            self.send_json(404, {"error": "unknown endpoint"})
            return
        handler()

    def read_payload(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        payload = json.loads(self.rfile.read(length) or b"{}")
        if not isinstance(payload, dict):
            raise ValueError("the request body must be a JSON object")
        return payload

    def send_graph(self) -> None:
        try:
            with Store(self.db_path, read_only=True) as store:
                # Statements are not nodes (s_d4bd1b45): the store rides
                # beside the graph so the viewer can still show intent state.
                payload = {**store.graph(), "statements": store.statements()}
            self.send_json(200, payload)
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def send_version(self) -> None:
        """A fingerprint of the store, cheap enough to poll.

        Every verb and the endorse endpoint write the database file, so its
        mtime and size move with the graph; the viewer polls this and
        re-derives itself when it changes — the view stays live without the
        operator refreshing."""
        try:
            parts = []
            db = Path(self.db_path)
            for path in (db, db.with_name(db.name + ".wal")):
                if path.exists():
                    stat = path.stat()
                    parts.append(f"{stat.st_mtime_ns}:{stat.st_size}")
            self.send_json(200, {"version": "|".join(parts) or "missing"})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def send_material(self, material_id: str) -> None:
        try:
            with Store(self.db_path, read_only=True) as store:
                body = store.material_body(material_id)
            self.send_json(200, {"id": material_id, "body": body})
        except ValueError as exc:
            self.send_json(404, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def endorse(self) -> None:
        """Take machine-owned statements on as the operator.

        The browser button is the operator acting — endorsement names who
        stands behind a statement, and the click is the taking-on. The
        machine never calls this endpoint (endorsement.md)."""
        # Imported here: cli imports this module for `serve`, so a top-level
        # import back would be circular. The views logic stays in one place.
        from .cli import write_views

        try:
            payload = self.read_payload()
            ids = payload.get("ids")
            if not isinstance(ids, list) or not ids:
                raise ValueError("ids: a non-empty list of statement ids")
            grounds = (payload.get("grounds") or "").strip() or None
            endorsed, already = [], []
            with Store(self.db_path) as store:
                for sid in ids:
                    statement = store.statement(sid)
                    if statement is None:
                        raise ValueError(f"statement '{sid}' does not exist")
                    if statement["owner"] == "operator":
                        already.append(sid)
                    else:
                        store.update_statement(sid, owner="operator")
                        store.record_decision(
                            "endorse",
                            sid,
                            text=statement["text"],
                            grounds=grounds,
                            actor="operator, via the viewer",
                        )
                        endorsed.append(sid)
                write_views(store)
            self.send_json(
                200, {"endorsed": endorsed, "already_operator_owned": already}
            )
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def verdict(self) -> None:
        """Record the operator's verdict on a test operation.

        The click is the judgment being spent (s_81c38173): the grounds are
        recorded with the operator named as their warrant."""
        from .cli import fetch_node, write_views

        try:
            payload = self.read_payload()
            test_id = payload.get("id")
            verdict = payload.get("verdict")
            if not test_id or verdict not in ("pass", "fail"):
                raise ValueError("id and a verdict of pass|fail are required")
            grounds = (payload.get("grounds") or "").strip()
            grounds = (
                f"operator, via the viewer: {grounds}"
                if grounds
                else "operator, via the viewer"
            )
            with Store(self.db_path) as store:
                fetch_node(store, test_id, kind="test")
                store.update_node(
                    test_id, props_patch={"verdict": verdict, "grounds": grounds}
                )
                write_views(store)
            self.send_json(200, {"id": test_id, "verdict": verdict})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def amend(self) -> None:
        """Rewrite a statement in the operator's words — one of the
        operator's three answers to a statement (endorsement.md)."""
        from .cli import fetch_statement, write_views

        try:
            payload = self.read_payload()
            sid = payload.get("id")
            text = (payload.get("text") or "").strip()
            if not sid or not text:
                raise ValueError("id and text are required")
            grounds = (payload.get("grounds") or "").strip() or None
            with Store(self.db_path) as store:
                statement = fetch_statement(store, sid)
                store.update_statement(sid, text=text, owner="operator")
                store.record_decision(
                    "amend",
                    sid,
                    text=statement["text"],
                    grounds=grounds,
                    actor="operator, via the viewer",
                )
                write_views(store)
            self.send_json(200, {"id": sid, "owner": "operator"})
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def strike(self) -> None:
        """Remove a statement — the operator's third answer. The machine
        never strikes operator-owned intent; the operator may strike any."""
        from .cli import fetch_statement, renumber_segment, write_views

        try:
            payload = self.read_payload()
            sid = payload.get("id")
            if not sid:
                raise ValueError("id is required")
            grounds = (payload.get("grounds") or "").strip() or None
            with Store(self.db_path) as store:
                statement = fetch_statement(store, sid)
                # Blast radius before the strike lands (s_070617cf); the
                # card showed it, the response restates it for the record.
                consequences = store.statement_consequences(sid)
                store.delete_statement(sid)
                renumber_segment(store, statement["segment"])
                store.record_decision(
                    "strike",
                    sid,
                    text=statement["text"],
                    grounds=grounds,
                    actor="operator, via the viewer",
                )
                write_views(store)
            self.send_json(
                200,
                {
                    "struck": sid,
                    "text": statement["text"],
                    "breaks": {
                        "anchors_open": [
                            n["id"] for n in consequences["anchors_open"]
                        ],
                        "anchors_folded": [
                            n["id"] for n in consequences["anchors_folded"]
                        ],
                        "produced": [
                            n["id"] for n in consequences["produced"]
                        ],
                        "linked_by": [
                            s["id"] for s in consequences["linked_by"]
                        ],
                    },
                },
            )
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def fold(self) -> None:
        """Fold an open work: the click is the operator confirming the
        settlement, so the operator-judgment gate is satisfied by it."""
        from .cli import fold_work, write_views

        try:
            payload = self.read_payload()
            work_id = payload.get("id")
            if not work_id:
                raise ValueError("id is required")
            with Store(self.db_path) as store:
                result = fold_work(store, work_id, operator_confirms=True)
                write_views(store)
            self.send_json(200, result)
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(db_path: str = "hypercore.duckdb", host: str = "127.0.0.1", port: int = 8000):
    handler = partial(HypercoreHandler, db_path=db_path, directory=str(WEB_ROOT))
    try:
        httpd = ThreadingHTTPServer((host, port), handler)
    except OSError as exc:
        if exc.errno == 98:  # EADDRINUSE
            raise ValueError(
                f"port {port} is already serving — likely an earlier "
                f"`hypercore serve`. The running one reads the database and "
                f"files per request, so it is already current: open "
                f"http://{host}:{port}/. To run a second viewer, pass --port."
            ) from exc
        raise
    print(f"serving http://{host}:{port} from {WEB_ROOT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
