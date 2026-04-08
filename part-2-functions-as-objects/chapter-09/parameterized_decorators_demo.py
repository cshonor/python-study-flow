"""
Demo for 10-parameterized-and-class-decorators.md (Fluent Python 9.10–9.10.3).

Includes:
- parameterized registration decorator (factory) with active flag and set registry
- parameterized clock decorator (factory) with fmt and wraps + kwargs support
- class-based clock decorator using __call__
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import wraps
from time import perf_counter, sleep

# --- 9.10 parameterized registration decorator -------------------------------

registry: set[object] = set()


def register(active: bool = True):
    def decorate(func):
        print(f"running register(active={active})->decorate({func.__name__})")
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func

    return decorate


@register(active=True)
def f1() -> None:
    print("running f1()")


@register()  # must call even when using default args
def f2() -> None:
    print("running f2()")


@register(active=False)
def f3() -> None:
    print("running f3()")


# --- 9.10.2 parameterized clock decorator (factory) --------------------------

DEFAULT_FMT = "[{elapsed:0.8f}s] {name}({args}) -> {result}"


def clock(fmt: str = DEFAULT_FMT):
    def decorate(func):
        @wraps(func)
        def clocked(*args, **kwargs):
            t0 = perf_counter()
            _result = func(*args, **kwargs)
            elapsed = perf_counter() - t0
            name = func.__name__
            arg_list = [repr(a) for a in args]
            arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
            args_str = ", ".join(arg_list)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result

        return clocked

    return decorate


@clock()  # default fmt
def snooze(seconds: float) -> None:
    sleep(seconds)


@clock("[elapsed={elapsed:.4f}s] {name} -> {result}")
def add(a: int, b: int, *, scale: int = 1) -> int:
    return (a + b) * scale


# --- 9.10.3 class-based decorator -------------------------------------------


@dataclass(frozen=True)
class Clock:
    fmt: str = DEFAULT_FMT

    def __call__(self, func):
        @wraps(func)
        def clocked(*args, **kwargs):
            t0 = perf_counter()
            _result = func(*args, **kwargs)
            elapsed = perf_counter() - t0
            name = func.__name__
            arg_list = [repr(a) for a in args]
            arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
            args_str = ", ".join(arg_list)
            result = repr(_result)
            print(self.fmt.format(**locals()))
            return _result

        return clocked


@Clock(fmt="[class-clock {elapsed:.6f}s] {name}({args})")
def factorial(n: int) -> int:
    return 1 if n < 2 else n * factorial(n - 1)


def main() -> None:
    print("=== registration decorator ===")
    print("registry ->", sorted(fn.__name__ for fn in registry))
    f1()
    f2()
    f3()

    print("\n=== parameterized clock (factory) ===")
    print("snooze.__name__ ->", snooze.__name__)
    snooze(0.05)
    print("add.__name__ ->", add.__name__)
    add(2, 3, scale=10)

    print("\n=== class-based clock ===")
    print("factorial.__name__ ->", factorial.__name__)
    print("6! =", factorial(6))


if __name__ == "__main__":
    main()

