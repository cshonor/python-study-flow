"""Ch. 17.8: Arithmetic progression generators — class, generator function, itertools."""

from __future__ import annotations

import itertools
from collections.abc import Iterator
from decimal import Decimal
from fractions import Fraction
from typing import TypeAlias, TypeVar

Number: TypeAlias = int | float | Fraction | Decimal
TNum = TypeVar("TNum", int, float, Fraction, Decimal)


class ArithmeticProgression:
    def __init__(self, begin: TNum, step: TNum, end: TNum | None = None) -> None:
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self) -> Iterator[TNum]:
        result_type = type(self.begin + self.step)
        result = result_type(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:  # type: ignore[operator]
            yield result
            index += 1
            result = self.begin + self.step * index  # type: ignore[operator]


def aritprog_gen(begin: TNum, step: TNum, end: TNum | None = None) -> Iterator[TNum]:
    result_type = type(begin + step)
    result = result_type(begin)
    forever = end is None
    index = 0
    while forever or result < end:  # type: ignore[operator]
        yield result
        index += 1
        result = begin + step * index  # type: ignore[operator]


def aritprog_itertools(begin: TNum, step: TNum, end: TNum | None = None) -> Iterator[TNum]:
    first = type(begin + step)(begin)
    ap = itertools.count(first, step)  # type: ignore[arg-type]
    if end is None:
        return ap  # type: ignore[return-value]
    return itertools.takewhile(lambda n: n < end, ap)  # type: ignore[return-value,operator]


def take(it: Iterator[Number], n: int) -> list[Number]:
    return list(itertools.islice(it, n))


def main() -> None:
    print("== class-based ==")
    print(take(iter(ArithmeticProgression(0, 1, 5)), 10))
    print(take(iter(ArithmeticProgression(0.0, 0.1, 0.5)), 10))
    print(take(iter(ArithmeticProgression(Fraction(1, 3), Fraction(1, 3), Fraction(2, 1))), 10))
    print(take(iter(ArithmeticProgression(Decimal("0.0"), Decimal("0.1"), Decimal("0.5"))), 10))
    print()

    print("== generator function ==")
    print(take(aritprog_gen(0, 1, 5), 10))
    print(take(aritprog_gen(0.0, 0.1, 0.5), 10))
    print()

    print("== itertools ==")
    print(take(aritprog_itertools(0, 1, 5), 10))
    print(take(aritprog_itertools(0.0, 0.1, 0.5), 10))
    print("infinite preview ->", take(aritprog_itertools(1, 2, None), 6))


if __name__ == "__main__":
    main()

