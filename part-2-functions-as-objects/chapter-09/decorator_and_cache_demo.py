"""
Decorator + functools.wraps + caching demo for Chapter 9.

Run from repo root:
  python part-2-functions-as-objects/chapter-09/decorator_and_cache_demo.py
"""

from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache, wraps
from time import perf_counter


def timed(func: Callable[..., object]) -> Callable[..., object]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        t0 = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            dt_ms = (perf_counter() - t0) * 1000
            print(f"{func.__name__} took {dt_ms:.2f} ms")

    return wrapper


@timed
def slow_add(a: int, b: int) -> int:
    # intentionally tiny slowdown
    s = 0
    for _ in range(200_000):
        s += 1
    return a + b


@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


def fib_plain(n: int) -> int:
    if n < 2:
        return n
    return fib_plain(n - 1) + fib_plain(n - 2)


def main() -> None:
    print("=== wraps keeps metadata ===")
    print("slow_add.__name__ ->", slow_add.__name__)
    print("slow_add(1, 2) ->", slow_add(1, 2))

    print("\n=== caching avoids recomputation ===")
    n = 30
    t0 = perf_counter()
    v1 = fib_plain(n)
    t1 = perf_counter()
    v2 = fib_cached(n)
    t2 = perf_counter()
    # second cached call should be near-zero
    v3 = fib_cached(n)
    t3 = perf_counter()

    print("fib_plain ->", v1, f"({(t1 - t0) * 1000:.1f} ms)")
    print("fib_cached first ->", v2, f"({(t2 - t1) * 1000:.1f} ms)")
    print("fib_cached second ->", v3, f"({(t3 - t2) * 1000:.3f} ms)")


if __name__ == "__main__":
    main()

