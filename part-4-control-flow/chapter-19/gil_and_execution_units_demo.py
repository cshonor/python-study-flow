"""Ch. 19.2-19.3: demo threads/coroutines/processes for IO vs CPU work."""

from __future__ import annotations

import asyncio
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial


def now() -> float:
    return time.perf_counter()


def io_sleep(i: int, seconds: float) -> str:
    time.sleep(seconds)
    return f"io#{i}"


async def aio_sleep(i: int, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return f"aio#{i}"


def cpu_work(i: int, n: int) -> str:
    acc = 0.0
    for k in range(1, n + 1):
        acc += math.sqrt(k)
    return f"cpu#{i}:{acc:.1f}"


@dataclass(frozen=True)
class Result:
    label: str
    elapsed_s: float


def bench(label: str, fn) -> Result:
    t0 = now()
    fn()
    return Result(label, now() - t0)


def run_threads_io(count: int, seconds: float) -> None:
    with ThreadPoolExecutor(max_workers=min(32, count)) as ex:
        list(ex.map(partial(io_sleep, seconds=seconds), range(count)))


def run_threads_cpu(count: int, n: int) -> None:
    with ThreadPoolExecutor(max_workers=min(32, count)) as ex:
        list(ex.map(partial(cpu_work, n=n), range(count)))


def run_processes_cpu(count: int, n: int) -> None:
    with ProcessPoolExecutor(max_workers=min(os.cpu_count() or 1, count)) as ex:
        list(ex.map(partial(cpu_work, n=n), range(count)))


def run_asyncio_io(count: int, seconds: float) -> None:
    async def runner() -> None:
        await asyncio.gather(*(aio_sleep(i, seconds) for i in range(count)))

    asyncio.run(runner())


def main() -> None:
    print("cpu_count ->", os.cpu_count())
    print()

    io_count = 30
    io_seconds = 0.03

    cpu_count = 4
    cpu_n = 400_000

    results: list[Result] = []
    results.append(bench("threads   IO (sleep)", lambda: run_threads_io(io_count, io_seconds)))
    results.append(bench("asyncio   IO (sleep)", lambda: run_asyncio_io(io_count, io_seconds)))
    results.append(bench("threads   CPU (sqrt)", lambda: run_threads_cpu(cpu_count, cpu_n)))
    results.append(bench("processes CPU (sqrt)", lambda: run_processes_cpu(cpu_count, cpu_n)))

    for r in results:
        print(f"{r.label:<20} -> {r.elapsed_s:.3f}s")


if __name__ == "__main__":
    main()

