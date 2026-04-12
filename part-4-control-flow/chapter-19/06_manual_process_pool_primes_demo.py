"""Ch. 19.6: manual process pool (SimpleQueue + sentinel) for CPU-bound is_prime batch.

Usage:
  python 06_manual_03_process_pool_primes_demo.py sequential
  python 06_manual_03_process_pool_primes_demo.py threads 6
  python 06_manual_03_process_pool_primes_demo.py procs 6

  python 06_manual_03_process_pool_primes_demo.py sequential --quick
"""

from __future__ import annotations

import argparse
import math
import queue
import sys
import threading
import time
from multiprocessing import Process, SimpleQueue, cpu_count
from typing import NamedTuple


SENTINEL = 0


class PrimeResult(NamedTuple):
    n: int
    prime: bool
    elapsed: float


# Default: a handful of large-ish odd integers (CPU-heavy is_prime); tune for your machine.
NUMBERS_HEAVY: list[int] = [
    50_000_111_000_021,
    50_000_111_000_039,
    50_000_111_000_051,
    50_000_111_000_057,
    50_000_111_000_063,
    50_000_111_000_069,
]

NUMBERS_QUICK: list[int] = [
    1_000_003,
    1_000_033,
    1_000_037,
    1_000_039,
    1_000_063,
    1_000_073,
]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True


def check(n: int) -> PrimeResult:
    t0 = time.perf_counter()
    ok = is_prime(n)
    return PrimeResult(n, ok, time.perf_counter() - t0)


def run_sequential(numbers: list[int]) -> None:
    print(f"Checking {len(numbers)} numbers sequentially:")
    t0 = time.perf_counter()
    for n in numbers:
        r = check(n)
        print(f"  {r.n:>18}  {'P' if r.prime else ' '}  {r.elapsed:7.4f}s")
    print(f"Total time: {time.perf_counter() - t0:.2f}s")


def thread_worker(jobs: queue.Queue[int], results: queue.Queue[PrimeResult]) -> None:
    while True:
        n = jobs.get()
        if n == SENTINEL:
            results.put(PrimeResult(SENTINEL, False, 0.0))
            return
        results.put(check(n))


def run_threads(numbers: list[int], workers: int) -> None:
    print(f"Checking {len(numbers)} numbers with {workers} threads:")
    jobs: queue.Queue[int] = queue.Queue()
    results: queue.Queue[PrimeResult] = queue.Queue()
    for n in numbers:
        jobs.put(n)
    for _ in range(workers):
        jobs.put(SENTINEL)
        threading.Thread(target=thread_worker, args=(jobs, results), daemon=True).start()

    t0 = time.perf_counter()
    done = 0
    checked = 0
    while done < workers:
        r = results.get()
        if r.n == SENTINEL:
            done += 1
        else:
            checked += 1
            print(f"  {r.n:>18}  {'P' if r.prime else ' '}  {r.elapsed:7.4f}s")
    print(f"{checked} checks in {time.perf_counter() - t0:.2f}s")


def proc_worker(jobs: SimpleQueue, results: SimpleQueue) -> None:
    while True:
        n = jobs.get()
        if n == SENTINEL:
            results.put(PrimeResult(SENTINEL, False, 0.0))
            return
        results.put(check(n))


def run_processes(numbers: list[int], workers: int) -> None:
    print(f"Checking {len(numbers)} numbers with {workers} processes:")
    jobs = SimpleQueue()
    results = SimpleQueue()
    for n in numbers:
        jobs.put(n)
    for _ in range(workers):
        jobs.put(SENTINEL)
        Process(target=proc_worker, args=(jobs, results)).start()

    t0 = time.perf_counter()
    done = 0
    checked = 0
    while done < workers:
        r = results.get()
        if r.n == SENTINEL:
            done += 1
        else:
            checked += 1
            print(f"  {r.n:>18}  {'P' if r.prime else ' '}  {r.elapsed:7.4f}s")
    print(f"{checked} checks in {time.perf_counter() - t0:.2f}s")


def main(argv: list[str]) -> None:
    p = argparse.ArgumentParser(description="Manual pool demo: sequential / threads / procs")
    p.add_argument(
        "mode",
        choices=("sequential", "threads", "procs"),
        help="run mode",
    )
    p.add_argument(
        "workers",
        nargs="?",
        type=int,
        default=None,
        help="worker count for threads/procs (default: cpu_count())",
    )
    p.add_argument(
        "--quick",
        action="store_true",
        help="use smaller numbers for a fast smoke test",
    )
    args = p.parse_args(argv[1:])

    numbers = NUMBERS_QUICK if args.quick else NUMBERS_HEAVY
    workers = args.workers if args.workers is not None else (cpu_count() or 1)

    if args.mode == "sequential":
        run_sequential(numbers)
    elif args.mode == "threads":
        run_threads(numbers, max(1, workers))
    else:
        run_processes(numbers, max(1, workers))


if __name__ == "__main__":
    main(sys.argv)
