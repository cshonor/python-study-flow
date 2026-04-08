"""
Demo for 09-functools-standard-decorators.md (Fluent Python 9.9).

Includes:
- cache / lru_cache Fibonacci
- decorator stacking order: @cache above @clock
- singledispatch htmlize example
"""

from __future__ import annotations

import decimal
import fractions
import html
import numbers
import time
from collections import abc
from functools import cache, lru_cache, singledispatch, wraps


def clock(func):
    @wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_list = [repr(a) for a in args]
        arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_list)
        print(f"[{elapsed:0.6f}s] {name}({arg_str}) -> {result!r}")
        return result

    return clocked


# --- Fibonacci: plain recursion (slow) ----------------------------------------
@clock
def fib_plain(n: int) -> int:
    if n < 2:
        return n
    return fib_plain(n - 2) + fib_plain(n - 1)


# --- Fibonacci: cache + clock (stacking order matters) ------------------------
@cache
@clock
def fib_cache(n: int) -> int:
    if n < 2:
        return n
    return fib_cache(n - 2) + fib_cache(n - 1)


# --- Fibonacci: lru_cache variant --------------------------------------------
@lru_cache(maxsize=128, typed=False)
@clock
def fib_lru(n: int) -> int:
    if n < 2:
        return n
    return fib_lru(n - 2) + fib_lru(n - 1)


# --- singledispatch htmlize ---------------------------------------------------
@singledispatch
def htmlize(obj: object) -> str:
    content = html.escape(repr(obj))
    return f"<pre>{content}</pre>"


@htmlize.register
def _(text: str) -> str:
    content = html.escape(text).replace("\n", "<br/>\n")
    return f"<p>{content}</p>"


@htmlize.register
def _(seq: abc.Sequence) -> str:  # type: ignore[misc]
    inner = "</li>\n<li>".join(htmlize(item) for item in seq)
    return "<ul>\n<li>" + inner + "</li>\n</ul>"


@htmlize.register
def _(n: numbers.Integral) -> str:  # covers int, but not bool once bool is registered
    return f"<pre>{n} (0x{n:x})</pre>"


@htmlize.register
def _(b: bool) -> str:
    return f"<pre>{b}</pre>"


@htmlize.register(fractions.Fraction)
def _(x) -> str:
    frac = fractions.Fraction(x)
    return f"<pre>{frac.numerator}/{frac.denominator}</pre>"


@htmlize.register(decimal.Decimal)
@htmlize.register(float)
def _(x) -> str:
    frac = fractions.Fraction(x).limit_denominator()
    return f"<pre>{x} ({frac.numerator}/{frac.denominator})</pre>"


def main() -> None:
    print("=== cache / lru_cache / stacking order ===")
    n_small = 6
    print("\n-- fib_cache(6) (should time each n once) --")
    print("fib_cache ->", fib_cache(n_small))

    print("\n-- fib_lru(6) (also cached, with maxsize) --")
    print("fib_lru ->", fib_lru(n_small))

    # Avoid running fib_plain(30) because it spams logs and is slow without caching.
    print("\n-- fib_plain(6) (no caching, repeated calls) --")
    print("fib_plain ->", fib_plain(n_small))

    print("\n=== singledispatch htmlize ===")
    samples = [
        "hello\nworld",
        42,
        True,  # bool should match bool handler, not Integral
        [1, "x", False],
        fractions.Fraction(2, 3),
        0.125,
        decimal.Decimal("0.2"),
    ]
    for s in samples:
        out = htmlize(s)
        print(type(s).__name__, "->", out)


if __name__ == "__main__":
    main()

