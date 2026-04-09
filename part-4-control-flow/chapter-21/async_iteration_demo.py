"""Ch. 21.10: async iteration, async generators, async comprehensions."""

from __future__ import annotations

import asyncio
import socket
from collections.abc import AsyncGenerator, AsyncIterator, Iterable
from dataclasses import dataclass
from keyword import kwlist


@dataclass(frozen=True)
class ProbeResult:
    domain: str
    found: bool


class AsyncCursor(AsyncIterator[str]):
    """A tiny async iterator that yields rows with an async delay."""

    def __init__(self, rows: list[str], delay_s: float = 0.05) -> None:
        self._rows = rows
        self._i = 0
        self._delay_s = delay_s

    def __aiter__(self) -> "AsyncCursor":
        return self

    async def __anext__(self) -> str:
        if self._i >= len(self._rows):
            raise StopAsyncIteration
        await asyncio.sleep(self._delay_s)
        row = self._rows[self._i]
        self._i += 1
        return row


async def probe(domain: str) -> ProbeResult:
    loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return ProbeResult(domain=domain, found=False)
    return ProbeResult(domain=domain, found=True)


async def multi_probe(domains: Iterable[str]) -> AsyncGenerator[ProbeResult, None]:
    coros = [probe(d) for d in domains]
    for coro in asyncio.as_completed(coros):
        yield await coro


def domains_from_keywords(*, suffix: str = ".dev", max_len: int = 4, limit: int = 10) -> list[str]:
    names = [kw for kw in kwlist if len(kw) <= max_len]
    names.sort()
    if limit > 0:
        names = names[:limit]
    return [f"{name}{suffix}".lower() for name in names]


async def demo_async_for_custom_iterator() -> None:
    print("== async for over custom async iterator ==")
    cursor = AsyncCursor(["row-1", "row-2", "row-3"], delay_s=0.02)
    async for row in cursor:
        print("row ->", row)
    print()


async def demo_async_generator_and_comprehensions() -> None:
    print("== async generator: multi_probe ==")
    domains = domains_from_keywords(limit=12)

    async for r in multi_probe(domains):
        mark = "+" if r.found else " "
        print(f"{mark} {r.domain}")
    print()

    print("== async generator expression: only found ==")
    found_gen = (r.domain async for r in multi_probe(domains) if r.found)
    found_list = [d async for d in found_gen]  # async list comprehension
    print("found ->", found_list)
    print()


async def main() -> None:
    await demo_async_for_custom_iterator()
    await demo_async_generator_and_comprehensions()


if __name__ == "__main__":
    asyncio.run(main())

