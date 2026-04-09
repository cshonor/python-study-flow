"""Chapter 16 intro: operator overloading with Decimal and a tiny domain type."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


def compound_interest_decimal(
    principal: Decimal, rate: Decimal, periods: int
) -> Decimal:
    """Same shape as the book's formula: principal * ((1 + rate) ** periods - 1)."""
    one = Decimal("1")
    return principal * ((one + rate) ** periods - one)


@dataclass(frozen=True)
class Position:
    """Minimal 'quant' style: notional = shares * price (demonstrates __mul__)."""

    symbol: str
    shares: Decimal
    price: Decimal

    def __mul__(self, other: Decimal) -> Decimal:
        if not isinstance(other, Decimal):
            return NotImplemented
        return self.shares * self.price * other

    def __rmul__(self, other: Decimal) -> Decimal:
        return self.__mul__(other)

    def notional(self) -> Decimal:
        return self.shares * self.price


def main() -> None:
    p = Decimal("10000")
    r = Decimal("0.05")
    n = 3
    print("compound interest (Decimal, infix formula) ->", compound_interest_decimal(p, r, n))

    pos = Position("AAA", Decimal("100"), Decimal("12.5"))
    print("position ->", pos)
    print("notional() ->", pos.notional())
    print("pos * Decimal('2') ->", pos * Decimal("2"))
    print("Decimal('2') * pos ->", Decimal("2") * pos)


if __name__ == "__main__":
    main()
