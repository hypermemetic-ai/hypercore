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
        super().do_GET()

    def send_graph(self) -> None:
        try:
            with Store(self.db_path, read_only=True) as store:
                payload = store.graph()
            self.send_json(200, payload)
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
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"serving http://{host}:{port} from {WEB_ROOT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
