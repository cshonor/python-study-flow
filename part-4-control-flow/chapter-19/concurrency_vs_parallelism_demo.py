"""Ch. 19 intro: show concurrency vs parallelism with threading/asyncio/multiprocessing."""

from __future__ import annotations

import asyncio
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from typing import Callable


def now() -> float:
    return time.perf_counter()


def io_bound_task(i: int, seconds: float) -> str:
    time.sleep(seconds)
    return f"io#{i}"


def cpu_bound_task(i: int, n: int) -> str:
    # Pure-Python-ish CPU work: sum sqrt for determinism.
    acc = 0.0
    for k in range(1, n + 1):
        acc += math.sqrt(k)
    return f"cpu#{i}:{acc:.3f}"


async def aio_io_bound_task(i: int, seconds: float) -> str:
    await asyncio.sleep(seconds)
    return f"aio-io#{i}"


@dataclass(frozen=True)
class BenchResult:
    label: str
    elapsed_s: float


def bench(label: str, fn: Callable[[], None]) -> BenchResult:
    t0 = now()
    fn()
    return BenchResult(label=label, elapsed_s=now() - t0)


def run_threading_io(count: int, seconds: float) -> None:
    with ThreadPoolExecutor(max_workers=min(32, count)) as ex:
        list(ex.map(lambda i: io_bound_task(i, seconds), range(count)))


def run_asyncio_io(count: int, seconds: float) -> None:
    async def runner() -> None:
        await asyncio.gather(*(aio_io_bound_task(i, seconds) for i in range(count)))

    asyncio.run(runner())


def run_process_cpu(count: int, n: int) -> None:
    # Use processes to actually run CPU work in parallel on multi-core.
    with ProcessPoolExecutor(max_workers=min(os.cpu_count() or 1, count)) as ex:
        list(ex.map(partial(cpu_bound_task, n=n), range(count)))


def run_threading_cpu(count: int, n: int) -> None:
    # Threads: typically no CPU speedup under CPython for pure Python loops.
    with ThreadPoolExecutor(max_workers=min(32, count)) as ex:
        list(ex.map(partial(cpu_bound_task, n=n), range(count)))


def main() -> None:
    print("cpu_count ->", os.cpu_count())
    print()

    io_count = 20
    io_seconds = 0.05

    cpu_count = 4
    cpu_n = 350_000

    results: list[BenchResult] = []
    results.append(bench("threading (I/O: sleep)", lambda: run_threading_io(io_count, io_seconds)))
    results.append(bench("asyncio   (I/O: sleep)", lambda: run_asyncio_io(io_count, io_seconds)))
    results.append(bench("threading (CPU: sqrt loop)", lambda: run_threading_cpu(cpu_count, cpu_n)))
    results.append(bench("processes (CPU: sqrt loop)", lambda: run_process_cpu(cpu_count, cpu_n)))

    for r in results:
        print(f"{r.label:<26} -> {r.elapsed_s:.3f}s")


if __name__ == "__main__":
    main()

