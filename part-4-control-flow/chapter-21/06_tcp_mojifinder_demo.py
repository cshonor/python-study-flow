"""Ch. 21.9: minimal asyncio TCP server (mojifinder-like text search)."""

from __future__ import annotations

import argparse
import asyncio
import unicodedata
from dataclasses import dataclass


@dataclass(frozen=True)
class Hit:
    char: str
    name: str


def search_unicode(q: str, limit: int = 10) -> list[Hit]:
    q = q.strip().upper()
    if not q:
        return []
    hits: list[Hit] = []
    # Scan a small-ish range for demo purposes.
    for codepoint in range(0x0000, 0x2FFF):
        ch = chr(codepoint)
        try:
            name = unicodedata.name(ch)
        except ValueError:
            continue
        if q in name:
            hits.append(Hit(char=ch, name=name))
            if len(hits) >= limit:
                break
    return hits


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    writer.write(b"mojifinder> type a query, or 'quit'\n")
    await writer.drain()

    while True:
        writer.write(b"query> ")
        await writer.drain()
        line = await reader.readline()
        if not line:
            break
        q = line.decode("utf-8", errors="replace").strip()
        if q.lower() in {"quit", "exit"}:
            break

        hits = search_unicode(q, limit=10)
        if not hits:
            writer.write(b"(no hits)\n")
        else:
            for h in hits:
                writer.write(f"{h.char}  {h.name}\n".encode("utf-8"))
        await writer.drain()

    writer.close()
    await writer.wait_closed()
    _ = addr


async def main(host: str, port: int) -> None:
    server = await asyncio.start_server(handle_client, host, port)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
    print("listening on", addrs)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="asyncio TCP mojifinder demo (Ch. 21.9)")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=25000)
    args = p.parse_args()
    asyncio.run(main(args.host, args.port))

