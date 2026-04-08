"""
Demo for 08-timing-decorator-clock.md (Fluent Python 9.8).

Shows:
- basic clock decorator (no kwargs, no wraps): works but loses metadata
- improved clock decorator (wraps + kwargs)
- recursion example (factorial)
"""

from __future__ import annotations

from functools import wraps
from time import perf_counter, sleep


def clock0(func):
    def clocked(*args):
        t0 = perf_counter()
        result = func(*args)
        elapsed = perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(a) for a in args)
        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result

    return clocked


def clock(func):
    @wraps(func)
    def clocked(*args, **kwargs):
        t0 = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - t0
        name = func.__name__
        arg_list = [repr(a) for a in args]
        arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_list)
        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result

    return clocked


@clock0
def snooze0(seconds: float) -> None:
    sleep(seconds)


@clock
def snooze(seconds: float) -> None:
    sleep(seconds)


@clock0
def factorial0(n: int) -> int:
    return 1 if n < 2 else n * factorial0(n - 1)


@clock
def factorial(n: int) -> int:
    return 1 if n < 2 else n * factorial(n - 1)


@clock
def power(base: int, *, exp: int) -> int:
    return base**exp


def main() -> None:
    print("*" * 40, "clock0 metadata")
    print("factorial0.__name__ ->", factorial0.__name__)

    print("*" * 40, "clock metadata (wraps)")
    print("factorial.__name__ ->", factorial.__name__)

    print("*" * 40, "Calling snooze0(.05)")
    snooze0(0.05)

    print("*" * 40, "Calling snooze(.05)")
    snooze(0.05)

    print("*" * 40, "Calling factorial0(6)")
    print("6! =", factorial0(6))

    print("*" * 40, "Calling factorial(6)")
    print("6! =", factorial(6))

    print("*" * 40, "kwargs supported in improved version")
    print("power(2, exp=10) ->", power(2, exp=10))


if __name__ == "__main__":
    main()

