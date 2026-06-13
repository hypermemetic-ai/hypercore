"""trak — a thin, stdlib-only client for plexus-trak's facet store.

Hand-written per the operator's decision (2026-06-13, "the trak client —
synapse-cc or hand-write": option 2): a small direct JSON-RPC client over
trak's facet surface, talking to trak's streaming WebSocket on :44107,
living entirely in hyper's repo.  No codegen, no third-party dependency —
so hyper stays one file, stdlib only, even once this becomes its document
backend.

The wire, from the standup (trak-backend graph) and the write-probe:

  * trak speaks Plexus streaming JSON-RPC 2.0 over a WebSocket.  Every
    call is a `trak.call` subscription — request
    {jsonrpc, id, method:"trak.call", params:{method:"facet.create", params:{…}}}
    answered first by an ack {id, result:<sub>}, then by a stream of
    notifications whose params.result is an envelope:
        {type:"data",  content:<event>}   one per yielded event
        {type:"error", message, code}     a transport/dispatch failure
        {type:"done"}                     end of stream
  * each `content` is a trak event, a dict tagged by snake_case "type":
    facet_created / facet_detail / facet_updated carry "facet"; list and
    tree stream "facet_summary" rows; login carries "login_success".
  * auth binds at the WebSocket upgrade — an `Authorization: Bearer <jwt>`
    header — so a token change means a fresh socket.  This client opens
    one socket per call and reads `self.token` each time, which makes
    `login()` followed by writes Just Work.

This module implements just enough of RFC 6455 (the client handshake and
masked text frames) to carry that, then maps trak's ~13-method facet
surface to plain Python methods.

Limits, named honestly: plaintext ws:// only (localhost) — wss/TLS waits
for the deferred network phase; auth is the single-user HS256 path the
standup landed on.  The backend URL is `ws://127.0.0.1:44107` unless
$TRAK_URL overrides it — the seed of the root's "network by configuration
alone", not yet its whole story.

Run it directly — `python3 trak.py` — for a live round-trip against a
running trak: it logs in, then create → get → update → list → delete,
printing each step and PASS/FAIL.  That is this slice's acceptance probe.
"""

import base64
import hashlib
import json
import os
import socket
import struct
from urllib.parse import urlparse

_WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
DEFAULT_URL = os.environ.get("TRAK_URL", "ws://127.0.0.1:44107")


class TrakError(Exception):
    """A trak call failed — carries the server's message and error code."""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


# ── the minimum WebSocket a client needs (RFC 6455) ──────────────────────

class _WebSocket:
    """A blocking client WebSocket: text frames only, masks what it sends,
    auto-pongs pings, raises on close.  Enough to carry trak's stream."""

    def __init__(self, host, port, path="/", headers=None, timeout=15.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self._buf = b""
        self._handshake(host, port, path, headers or {})

    def _handshake(self, host, port, path, headers):
        key = base64.b64encode(os.urandom(16)).decode()
        lines = [
            f"GET {path} HTTP/1.1",
            f"Host: {host}:{port}",
            "Upgrade: websocket",
            "Connection: Upgrade",
            f"Sec-WebSocket-Key: {key}",
            "Sec-WebSocket-Version: 13",
        ]
        lines += [f"{k}: {v}" for k, v in headers.items()]
        self.sock.sendall(("\r\n".join(lines) + "\r\n\r\n").encode())

        head = self._read_until(b"\r\n\r\n")
        status = head.split(b"\r\n", 1)[0].decode("latin1")
        if "101" not in status:
            raise TrakError(f"websocket upgrade refused: {status}")
        accept = base64.b64encode(
            hashlib.sha1((key + _WS_GUID).encode()).digest()
        ).decode()
        if accept.encode() not in head:
            raise TrakError("websocket upgrade: bad Sec-WebSocket-Accept")

    def _read_until(self, sep):
        while sep not in self._buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise TrakError("connection closed during handshake")
            self._buf += chunk
        head, self._buf = self._buf.split(sep, 1)
        return head + sep

    def _read_exact(self, n):
        while len(self._buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise TrakError("connection closed mid-frame")
            self._buf += chunk
        out, self._buf = self._buf[:n], self._buf[n:]
        return out

    @staticmethod
    def _mask(data, key):
        return bytes(b ^ key[i & 3] for i, b in enumerate(data))

    def _send_frame(self, opcode, payload=b""):
        n = len(payload)
        header = bytearray([0x80 | opcode])  # FIN set — no fragmentation out
        if n < 126:
            header.append(0x80 | n)
        elif n < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        key = os.urandom(4)
        header += key
        self.sock.sendall(bytes(header) + self._mask(payload, key))

    def send(self, text):
        self._send_frame(0x1, text.encode("utf-8"))

    def recv(self):
        """One full text message — reassembles fragments, swallows pings/pongs."""
        chunks = []
        while True:
            b0, b1 = self._read_exact(2)
            fin = b0 & 0x80
            opcode = b0 & 0x0F
            masked = b1 & 0x80
            length = b1 & 0x7F
            if length == 126:
                length = struct.unpack(">H", self._read_exact(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self._read_exact(8))[0]
            key = self._read_exact(4) if masked else b""
            data = self._read_exact(length)
            if masked:
                data = self._mask(data, key)
            if opcode == 0x8:            # close
                raise TrakError("websocket closed by server")
            if opcode == 0x9:            # ping → pong
                self._send_frame(0xA, data)
                continue
            if opcode == 0xA:            # pong
                continue
            chunks.append(data)          # text (0x1) or continuation (0x0)
            if fin:
                return b"".join(chunks).decode("utf-8")

    def close(self):
        try:
            self._send_frame(0x8)
        except OSError:
            pass
        try:
            self.sock.close()
        except OSError:
            pass


# ── the facet client ─────────────────────────────────────────────────────

class Trak:
    """A thin client over trak's facet surface.

    Construct without a token and `login()` to get one (it is stored, so
    subsequent calls authenticate); or pass a token you already hold.  A
    fresh WebSocket is opened per call — trak binds auth at the upgrade,
    so this is the simplest correct shape, and the calls are short.
    """

    def __init__(self, url=DEFAULT_URL, token=None, origin="http://localhost"):
        u = urlparse(url)
        if u.scheme not in ("ws", ""):
            raise TrakError(f"only plaintext ws:// is supported, not {u.scheme!r}")
        self.host = u.hostname or "127.0.0.1"
        self.port = u.port or 44107
        self.path = u.path or "/"
        self.token = token
        self.origin = origin
        self._id = 0

    # — transport —

    def _open(self):
        headers = {"Origin": self.origin}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return _WebSocket(self.host, self.port, self.path, headers)

    def call(self, method, params=None):
        """Run one RPC; return the list of event payloads (each `content`)
        up to `done`.  Raises TrakError on any error layer."""
        ws = self._open()
        try:
            self._id += 1
            rid = self._id
            ws.send(json.dumps({
                "jsonrpc": "2.0", "id": rid, "method": "trak.call",
                "params": {"method": method, "params": params or {}},
            }))
            datas = []
            while True:
                obj = json.loads(ws.recv())
                if obj.get("id") == rid and "error" in obj:   # jsonrpc-level
                    e = obj["error"] or {}
                    raise TrakError(e.get("message", "rpc error"), e.get("code"))
                if obj.get("id") == rid and "result" in obj:  # subscription ack
                    continue
                if obj.get("method") != "trak.call":
                    continue
                res = obj.get("params", {}).get("result", {})
                kind = res.get("type")
                if kind == "data":
                    content = res.get("content")
                    if isinstance(content, dict) and content.get("type") == "error":
                        raise TrakError(content.get("message", "error"),
                                        content.get("code"))
                    datas.append(content)
                elif kind == "error":                          # transport-level
                    raise TrakError(res.get("message", "stream error"),
                                    res.get("code"))
                elif kind == "done":
                    break
                # progress / anything else: ignore
            return datas
        finally:
            ws.close()

    @staticmethod
    def _params(**kw):
        """Drop None — trak reads an omitted optional as 'unchanged'.  An
        explicit empty list (e.g. tags=[] to clear) is kept."""
        return {k: v for k, v in kw.items() if v is not None}

    def _facet(self, datas):
        for c in datas:
            if isinstance(c, dict) and "facet" in c:
                return c["facet"]
        raise TrakError(f"no facet in response: {datas}")

    # — identity —

    def register(self, username, password, tenant="local"):
        """Register a user.  Returns the event payload; raises if it fails
        (a duplicate is an error — catch TrakError if you want idempotence)."""
        return self.call("identity.register", self._params(
            username=username, password=password, tenant=tenant))[0]

    def login(self, username, password):
        """Log in, store and return the access token."""
        datas = self.call("identity.login",
                          {"username": username, "password": password})
        token = datas[0]["access_token"]
        self.token = token
        return token

    # — facet CRUD —

    def create(self, title, body=None, parent_id=None, status=None,
               tags=None, priority=None, meta_extra=None):
        return self._facet(self.call("facet.create", self._params(
            title=title, body=body, parent_id=parent_id, status=status,
            tags=tags, priority=priority, meta_extra=meta_extra)))

    def get(self, id):
        return self._facet(self.call("facet.get", {"id": id}))

    def update(self, id, title=None, body=None, status=None,
               tags=None, priority=None, meta_extra=None):
        return self._facet(self.call("facet.update", self._params(
            id=id, title=title, body=body, status=status,
            tags=tags, priority=priority, meta_extra=meta_extra)))

    def delete(self, id):
        """Delete a facet; returns the deleted id."""
        datas = self.call("facet.delete", {"id": id})
        return datas[0].get("id") if datas else id

    def move_to(self, id, new_parent_id=None):
        """Move a facet under a new parent (or to root).  Returns the
        {id, old_parent, new_parent} event payload."""
        return self.call("facet.move_to",
                         self._params(id=id, new_parent_id=new_parent_id))[0]

    # — tree / list —

    def list(self, parent_id=None, tags=None, tags_all=None, priority=None):
        """Children of a parent (or roots).  Returns facet_summary rows."""
        datas = self.call("facet.list", self._params(
            parent_id=parent_id, tags=tags, tags_all=tags_all, priority=priority))
        return [c for c in datas if c.get("type") == "facet_summary"]

    def tree(self, id):
        """The subtree rooted at a facet, as facet_summary rows (with depth)."""
        datas = self.call("facet.tree", {"id": id})
        return [c for c in datas if c.get("type") == "facet_summary"]

    # — links / queries —

    def link(self, from_id, to_id, kind):
        """Create a typed edge (depends_on / blocks / relates_to / duplicates)."""
        return self.call("facet.link",
                         {"from_id": from_id, "to_id": to_id, "kind": kind})[0]

    def unlink(self, from_id, to_id, kind):
        return self.call("facet.unlink",
                         {"from_id": from_id, "to_id": to_id, "kind": kind})[0]

    def links(self, id, direction=None, kind=None):
        """Edges touching a facet.  Returns the edge dicts."""
        datas = self.call("facet.links",
                         self._params(id=id, direction=direction, kind=kind))
        return [c["edge"] for c in datas
                if isinstance(c, dict) and "edge" in c]

    def blocked(self, parent_id=None):
        """Facets blocked by non-done dependencies."""
        datas = self.call("facet.blocked", self._params(parent_id=parent_id))
        return [c for c in datas if c.get("type") == "blocked"]

    def search(self, query, tags=None, tags_all=None, priority=None):
        """Full-text search; returns search_result rows (facet + score)."""
        datas = self.call("facet.search", self._params(
            query=query, tags=tags, tags_all=tags_all, priority=priority))
        return [c for c in datas if c.get("type") == "search_result"]

    def grep(self, pattern, status=None, parent_id=None,
             tags=None, tags_all=None, priority=None):
        """Regex search over titles and bodies; returns matching facets."""
        datas = self.call("facet.grep", self._params(
            pattern=pattern, status=status, parent_id=parent_id,
            tags=tags, tags_all=tags_all, priority=priority))
        return [c["facet"] for c in datas
                if isinstance(c, dict) and "facet" in c]


# ── acceptance probe ─────────────────────────────────────────────────────

def _selftest():
    """Live round-trip against a running trak — this slice's evidence."""
    import sys
    import time

    url = DEFAULT_URL
    user, password = "hyper-local", "hyper-local-dev"
    print(f"trak self-test → {url}")
    t = Trak(url)

    try:
        t.register(user, password)
        print("register: ok")
    except TrakError as e:
        print(f"register: already present ({e})")

    t.login(user, password)
    print(f"login:    ok (token {t.token[:12]}…)")

    marker = f"selftest-{int(time.time())}"
    title = "hyper trak-client self-test"
    body = f"thin-client round-trip · {marker}"

    created = t.create(title=title, body=body, status="open")
    fid = created["id"]
    print(f"create:   id={fid}")

    got = t.get(fid)
    ok_get = got["id"] == fid and got["title"] == title and got.get("body") == body
    print(f"get:      title={got['title']!r}  ({'match' if ok_get else 'MISMATCH'})")

    upd = t.update(fid, status="done", body=body + " · updated")
    ok_upd = upd["status"] == "done" and upd.get("body", "").endswith("updated")
    print(f"update:   status={upd['status']!r}  ({'ok' if ok_upd else 'FAILED'})")

    rows = t.list()
    seen = any(r.get("id") == fid for r in rows)
    print(f"list:     {len(rows)} root(s)  (probe {'present' if seen else 'ABSENT'})")

    t.delete(fid)
    gone = False
    try:
        t.get(fid)
    except TrakError:
        gone = True
    print(f"delete:   {'gone' if gone else 'STILL THERE'}")

    ok = ok_get and ok_upd and seen and gone
    print(f"\nROUND-TRIP: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    _selftest()
