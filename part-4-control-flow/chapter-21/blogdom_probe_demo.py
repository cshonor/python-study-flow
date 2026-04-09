"""Ch. 21.3: asyncio domain probe demo (DNS getaddrinfo + as_completed)."""

from __future__ import annotations

import argparse
import asyncio
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from keyword import kwlist
from typing import Iterable


def domains_from_keywords(*, suffix: str, max_len: int, limit: int) -> list[str]:
    names = [kw for kw in kwlist if len(kw) <= max_len]
    names.sort()
    if limit > 0:
        names = names[:limit]
    return [f"{name}{suffix}".lower() for name in names]


async def probe(domain: str) -> tuple[str, bool]:
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


async def run_asyncio(domains: Iterable[str]) -> None:
    coros = [probe(d) for d in domains]
    for coro in asyncio.as_completed(coros):
        domain, found = await coro
        mark = "+" if found else " "
        print(f"{mark} {domain}", flush=True)


def probe_sync(domain: str) -> tuple[str, bool]:
    try:
        socket.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


def run_threadpool(domains: Iterable[str], workers: int) -> None:
    domains = list(domains)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(probe_sync, d) for d in domains]
        for fut in as_completed(futures):
            domain, found = fut.result()
            mark = "+" if found else " "
            print(f"{mark} {domain}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Async domain probe demo (Ch. 21.3)")
    parser.add_argument("--suffix", default=".dev", help="domain suffix (default: .dev)")
    parser.add_argument("--max-len", type=int, default=4, help="max keyword length")
    parser.add_argument("--limit", type=int, default=0, help="limit number of keywords (0 -> no limit)")
    parser.add_argument("--mode", choices=("asyncio", "threadpool"), default="asyncio")
    parser.add_argument("-w", "--workers", type=int, default=32, help="threadpool workers")
    args = parser.parse_args()

    domains = domains_from_keywords(
        suffix=args.suffix,
        max_len=max(1, args.max_len),
        limit=max(0, args.limit),
    )

    t0 = time.perf_counter()
    if args.mode == "asyncio":
        asyncio.run(run_asyncio(domains))
    else:
        run_threadpool(domains, workers=max(1, args.workers))
    print(f"[{args.mode}] elapsed: {time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    main()

