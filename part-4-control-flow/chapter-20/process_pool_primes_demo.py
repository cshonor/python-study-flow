"""Ch. 20.3: CPU-bound work with ProcessPoolExecutor (prime checking demo)."""

from __future__ import annotations

import argparse
import math
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from time import perf_counter
from typing import Iterable, Literal


NUMBERS: list[int] = [
    2,
    3,
    4,
    5,
    10_000_019,  # prime-ish
    10_000_079,  # prime-ish
    10_000_003,  # prime-ish
    9_999_999_967,  # large prime-ish
    9_999_999_996,  # composite
    9_999_999_989,  # prime-ish
]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    limit = int(math.isqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


@dataclass(frozen=True)
class PrimeResult:
    n: int
    prime: bool
    elapsed: float


def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n=n, prime=res, elapsed=perf_counter() - t0)


PoolKind = Literal["thread", "process"]
OrderKind = Literal["map", "completed"]


def iter_results_map(ex, numbers: Iterable[int]) -> Iterable[PrimeResult]:
    # map yields results in *input order*
    yield from ex.map(check, numbers)


def iter_results_as_completed(ex, numbers: Iterable[int]) -> Iterable[PrimeResult]:
    futures = [ex.submit(check, n) for n in numbers]
    for fut in as_completed(futures):
        yield fut.result()


def run(pool: PoolKind, order: OrderKind, workers: int | None, numbers: list[int]) -> None:
    ex_cls = ThreadPoolExecutor if pool == "thread" else ProcessPoolExecutor
    label = f"{ex_cls.__name__} / {order}"

    t0 = perf_counter()
    with ex_cls(max_workers=workers) as ex:
        it = iter_results_map(ex, numbers) if order == "map" else iter_results_as_completed(ex, numbers)
        for r in it:
            tag = "P" if r.prime else "."
            print(f"{r.n:>12} {tag} {r.elapsed:7.3f}s")

    print(f"[{label}] total: {perf_counter() - t0:.2f}s")


def main() -> None:
    parser = argparse.ArgumentParser(description="ProcessPoolExecutor primes demo (Ch. 20.3)")
    parser.add_argument("--pool", choices=("thread", "process"), default="process")
    parser.add_argument("--order", choices=("map", "completed"), default="map")
    parser.add_argument("-w", "--workers", type=int, default=0, help="0 -> default")
    parser.add_argument("--desc", action="store_true", help="sort numbers descending (to amplify map blocking)")
    args = parser.parse_args()

    workers = None if args.workers == 0 else args.workers
    nums = sorted(NUMBERS, reverse=args.desc)

    print("cpu_count ->", os.cpu_count())
    print("numbers ->", nums)
    print()
    run(args.pool, args.order, workers, nums)


if __name__ == "__main__":
    main()

