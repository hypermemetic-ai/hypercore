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
        if self.path == "/api/endorse":
            self.endorse()
            return
        self.send_json(404, {"error": "unknown endpoint"})

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
            length = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(length) or b"{}")
            ids = payload.get("ids")
            if not isinstance(ids, list) or not ids:
                raise ValueError("ids: a non-empty list of statement ids")
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
                        endorsed.append(sid)
                write_views(store)
            self.send_json(
                200, {"endorsed": endorsed, "already_operator_owned": already}
            )
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
