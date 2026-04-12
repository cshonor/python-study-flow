"""Chapter 16.2–16.3: unary operator overloading (Vector) + Decimal/Counter edge cases."""

from __future__ import annotations

import math
from collections import Counter
from decimal import Decimal, getcontext


class Vector:
    """Example 16-1 style: 2D vector with unary -, unary +, abs."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __pos__(self) -> Vector:
        return Vector(self.x, self.y)

    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r})"


def demo_vector() -> None:
    v = Vector(3.0, 4.0)
    print("v ->", v)
    print("abs(v) ->", abs(v))
    print("-v ->", -v)
    print("+v ->", +v)


def demo_decimal_pos_inequality() -> None:
    ctx = getcontext()
    saved = ctx.prec
    try:
        ctx.prec = 40
        one_third = Decimal("1") / Decimal("3")
        print("Decimal prec=40: one_third == +one_third ->", one_third == +one_third)

        ctx.prec = 28
        print("after prec=28: one_third == +one_third ->", one_third == +one_third)
    finally:
        ctx.prec = saved


def demo_counter_pos() -> None:
    ct = Counter("abracadabra")
    ct["r"] = -3
    ct["d"] = 0
    print("ct ->", ct)
    print("+ct ->", +ct)
    print("ct == +ct ->", ct == +ct)


def main() -> None:
    demo_vector()
    print("---")
    demo_decimal_pos_inequality()
    print("---")
    demo_counter_pos()


if __name__ == "__main__":
    main()
