from __future__ import annotations

import http.client
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn


# --- Case 1: standard library mixin (ThreadingMixIn) ---


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # Show which thread handled this request.
        msg = f"handled by {threading.current_thread().name}\n"
        body = msg.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        # Silence default logging to keep output focused.
        return


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


def demo_threading_mixin() -> None:
    print("ThreadingMixIn demo (stdlib)")
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    host, port = server.server_address

    t = threading.Thread(target=server.serve_forever, name="server-main", daemon=True)
    t.start()

    def fetch(label: str) -> None:
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/")
        resp = conn.getresponse()
        data = resp.read().decode("utf-8").strip()
        print(label, "->", data)
        conn.close()

    t1 = threading.Thread(target=fetch, args=("request-1",), name="client-1")
    t2 = threading.Thread(target=fetch, args=("request-2",), name="client-2")
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    server.shutdown()
    server.server_close()
    time.sleep(0.05)


# --- Case 2: "Django-style" cooperative mixins (toy CBV) ---


class View:
    def dispatch(self, request: dict) -> dict:
        return {"status": 200, "body": "ok"}


class LoggingMixin:
    def dispatch(self, request: dict) -> dict:
        request.setdefault("log", []).append("LoggingMixin.before")
        response = super().dispatch(request)
        request["log"].append("LoggingMixin.after")
        return response


class AuthMixin:
    def dispatch(self, request: dict) -> dict:
        request.setdefault("log", []).append("AuthMixin.before")
        if not request.get("user"):
            return {"status": 401, "body": "unauthorized"}
        response = super().dispatch(request)
        request["log"].append("AuthMixin.after")
        return response


class HelloView(AuthMixin, LoggingMixin, View):
    def dispatch(self, request: dict) -> dict:
        request.setdefault("log", []).append("HelloView")
        response = super().dispatch(request)
        if response.get("status") == 200:
            response["body"] = f"hello {request['user']}"
        return response


def demo_cbv_mixins() -> None:
    print("\nCBV-style mixins demo (toy)")
    print("MRO:", " -> ".join(cls.__name__ for cls in HelloView.__mro__))

    req1: dict = {"user": "alice"}
    resp1 = HelloView().dispatch(req1)
    print("authorized resp ->", resp1, "| log ->", req1["log"])

    req2: dict = {}
    resp2 = HelloView().dispatch(req2)
    print("unauthorized resp ->", resp2, "| log ->", req2["log"])


# --- Case 3: Tkinter deep MRO (optional) ---


def demo_tkinter_mro() -> None:
    print("\nTkinter MRO demo (optional)")
    try:
        import tkinter  # noqa: F401
        from tkinter import Text
    except Exception as e:
        print("tkinter not available ->", e)
        return

    print("Text.__mro__ ->")
    print(" -> ".join(cls.__name__ for cls in Text.__mro__))


def main() -> None:
    demo_threading_mixin()
    demo_cbv_mixins()
    demo_tkinter_mro()


if __name__ == "__main__":
    main()

