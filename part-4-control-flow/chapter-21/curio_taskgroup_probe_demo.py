"""Ch. 21.11-21.13: Curio TaskGroup vs asyncio as_completed (domain probe).

This script is runnable even without Curio installed:
- If `curio` is available, it uses Curio + TaskGroup.
- Otherwise it falls back to asyncio.
"""

from __future__ import annotations

import argparse
import asyncio
import socket
import sys
import time
from keyword import kwlist
from typing import Iterable


def domains_from_keywords(*, suffix: str, max_len: int, limit: int) -> list[str]:
    names = [kw for kw in kwlist if len(kw) <= max_len]
    names.sort()
    if limit > 0:
        names = names[:limit]
    return [f"{name}{suffix}".lower() for name in names]


async def asyncio_probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


async def run_asyncio(domains: Iterable[str]) -> None:
    coros = [asyncio_probe(d) for d in domains]
    for coro in asyncio.as_completed(coros):
        domain, found = await coro
        mark = "+" if found else " "
        print(f"{mark} {domain}", flush=True)


def main() -> None:
    p = argparse.ArgumentParser(description="Curio TaskGroup domain probe demo (Ch. 21.11-21.13)")
    p.add_argument("--suffix", default=".dev")
    p.add_argument("--max-len", type=int, default=4)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--mode", choices=("auto", "curio", "asyncio"), default="auto")
    args = p.parse_args()

    domains = domains_from_keywords(
        suffix=args.suffix,
        max_len=max(1, args.max_len),
        limit=max(0, args.limit),
    )

    t0 = time.perf_counter()

    if args.mode in ("auto", "curio"):
        try:
            import curio  # type: ignore
            import curio.socket as csocket  # type: ignore
        except Exception:
            if args.mode == "curio":
                print("[need curio] Install with: pip install curio", file=sys.stderr)
                raise SystemExit(2)
        else:

            async def curio_probe(domain: str) -> tuple[str, bool]:
                try:
                    await csocket.getaddrinfo(domain, None)
                except csocket.gaierror:
                    return (domain, False)
                return (domain, True)

            async def curio_main() -> None:
                async with curio.TaskGroup() as g:
                    for d in domains:
                        await g.spawn(curio_probe, d)
                    async for task in g:
                        domain, found = task.result
                        mark = "+" if found else " "
                        print(f"{mark} {domain}", flush=True)

            curio.run(curio_main)
            print(f"[curio] elapsed: {time.perf_counter() - t0:.2f}s")
            return

    asyncio.run(run_asyncio(domains))
    print(f"[asyncio] elapsed: {time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    main()

