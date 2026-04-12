from __future__ import annotations

from typing import overload


@overload
def calculate_return(price: float, *, base: float = 1.0) -> float: ...


@overload
def calculate_return(prices: list[float], *, base: float = 1.0) -> list[float]: ...


def calculate_return(price_or_prices: float | list[float], *, base: float = 1.0):
    """Demo: overload gives type checkers precise signatures.

    Runtime: we still implement a single function.
    """

    def one(x: float) -> float:
        return (x - base) / base

    if isinstance(price_or_prices, list):
        return [one(x) for x in price_or_prices]
    return one(price_or_prices)


def main() -> None:
    print("single:", calculate_return(1.25, base=1.0))
    print("batch:", calculate_return([1.0, 1.1, 0.9], base=1.0))


if __name__ == "__main__":
    main()

