"""Ch. 21.9: tiny client for tcp_mojifinder_demo.py."""

from __future__ import annotations

import argparse
import socket


def main(host: str, port: int, query: str) -> None:
    with socket.create_connection((host, port), timeout=5) as sock:
        f = sock.makefile("rwb", buffering=0)
        # read greeting + prompt
        for _ in range(2):
            line = f.readline()
            if not line:
                break
            print(line.decode("utf-8", errors="replace"), end="")

        f.write((query + "\n").encode("utf-8"))
        # read until next prompt
        while True:
            line = f.readline()
            if not line:
                break
            text = line.decode("utf-8", errors="replace")
            if text.startswith("query> "):
                break
            print(text, end="")

        f.write(b"quit\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="client for tcp mojifinder demo")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=25000)
    p.add_argument("query", nargs="?", default="GREEK")
    args = p.parse_args()
    main(args.host, args.port, args.query)

