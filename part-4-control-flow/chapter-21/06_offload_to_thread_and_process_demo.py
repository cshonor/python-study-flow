"""Ch. 21.8: offload blocking/CPU work to thread/process executors."""

from __future__ import annotations

import asyncio
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor


def blocking_io(seconds: float) -> str:
    time.sleep(seconds)
    return "io-done"


def cpu_heavy(n: int) -> float:
    # Pure Python-ish CPU work
    acc = 0.0
    for k in range(1, n + 1):
        acc += math.sqrt(k)
    return acc


async def ticker(label: str, interval: float, ticks: int) -> None:
    for i in range(ticks):
        print(f"{label} tick {i}", flush=True)
        await asyncio.sleep(interval)


async def bad_blocking() -> None:
    print("\n== BAD: blocking I/O in event loop ==")
    t = asyncio.create_task(ticker("ticker", 0.2, 10))
    blocking_io(1.5)  # freezes loop
    await t


async def good_to_thread() -> None:
    print("\n== GOOD: asyncio.to_thread for blocking I/O ==")
    t = asyncio.create_task(ticker("ticker", 0.2, 10))
    await asyncio.to_thread(blocking_io, 1.5)
    await t


async def cpu_with_process_pool() -> None:
    print("\n== CPU: offload to ProcessPoolExecutor ==")
    print("cpu_count ->", os.cpu_count())
    t = asyncio.create_task(ticker("ticker", 0.2, 10))

    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=min(os.cpu_count() or 1, 4)) as pool:
        # Run a couple CPU jobs without blocking the loop
        futs = [
            loop.run_in_executor(pool, cpu_heavy, 500_000),
            loop.run_in_executor(pool, cpu_heavy, 500_000),
        ]
        results = await asyncio.gather(*futs)
        print("cpu results ->", [f"{r:.3f}" for r in results])

    await t


async def main() -> None:
    await bad_blocking()
    await good_to_thread()
    await cpu_with_process_pool()


if __name__ == "__main__":
    asyncio.run(main())

