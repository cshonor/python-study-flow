"""Ch. 20 intro: concurrent.futures executors + Future essentials."""

from __future__ import annotations

import os
import time
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Iterable


def now() -> float:
    return time.perf_counter()


def io_task(i: int, delay_s: float) -> str:
    time.sleep(delay_s)
    return f"io#{i}"


def cpu_task(i: int, n: int) -> str:
    # Pure python loop to burn CPU deterministically.
    acc = 0
    for k in range(1, n + 1):
        acc = (acc + k) % 1_000_003
    return f"cpu#{i}:{acc}"


def boom(i: int) -> str:
    if i == 3:
        raise RuntimeError("demo error at i=3")
    return f"ok#{i}"


@dataclass(frozen=True)
class RunResult:
    label: str
    elapsed_s: float
    ok: int
    failed: int


def run_pool(
    label: str,
    make_executor: Callable[[], Any],
    fn: Callable[[int], Any],
    items: Iterable[int],
) -> RunResult:
    t0 = now()
    ok = 0
    failed = 0

    with make_executor() as ex:
        futures: list[Future[Any]] = []

        def on_done(fut: Future[Any]) -> None:
            # Callback runs in the main interpreter thread (implementation detail),
            # but it's enough to show the hook point.
            _ = fut.done()

        for i in items:
            fut = ex.submit(fn, i)
            fut.add_done_callback(on_done)
            futures.append(fut)

        for fut in as_completed(futures):
            try:
                _ = fut.result()
            except Exception:
                failed += 1
            else:
                ok += 1

    return RunResult(label=label, elapsed_s=now() - t0, ok=ok, failed=failed)


def main() -> None:
    print("cpu_count ->", os.cpu_count())
    print()

    # I/O-bound: threads shine, processes usually waste overhead.
    io_items = range(20)
    io_delay = 0.05
    r1 = run_pool(
        "ThreadPoolExecutor (I/O sleep)",
        lambda: ThreadPoolExecutor(max_workers=32),
        partial(io_task, delay_s=io_delay),
        io_items,
    )
    r2 = run_pool(
        "ProcessPoolExecutor (I/O sleep)",
        lambda: ProcessPoolExecutor(max_workers=min(os.cpu_count() or 1, 8)),
        partial(io_task, delay_s=io_delay),
        io_items,
    )

    # CPU-bound: processes can run in parallel; threads typically won't speed up in CPython.
    cpu_items = range(6)
    cpu_n = 600_000
    r3 = run_pool(
        "ThreadPoolExecutor (CPU loop)",
        lambda: ThreadPoolExecutor(max_workers=32),
        partial(cpu_task, n=cpu_n),
        cpu_items,
    )
    r4 = run_pool(
        "ProcessPoolExecutor (CPU loop)",
        lambda: ProcessPoolExecutor(max_workers=min(os.cpu_count() or 1, 6)),
        partial(cpu_task, n=cpu_n),
        cpu_items,
    )

    # Exception propagation through Future.result().
    r5 = run_pool(
        "ThreadPoolExecutor (exceptions)",
        lambda: ThreadPoolExecutor(max_workers=8),
        boom,
        range(6),
    )

    for r in (r1, r2, r3, r4, r5):
        print(f"{r.label:<32} -> {r.elapsed_s:.3f}s  ok={r.ok} failed={r.failed}")


if __name__ == "__main__":
    main()

