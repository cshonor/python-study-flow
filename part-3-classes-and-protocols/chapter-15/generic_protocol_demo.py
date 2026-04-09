from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, TypeVar


T = TypeVar("T")


class HasPrice(Protocol):
    def price(self) -> float: ...


TPrice = TypeVar("TPrice", bound=HasPrice)


def max_by_price(items: Iterable[TPrice]) -> TPrice:
    return max(items, key=lambda x: x.price())


class Stock:
    def __init__(self, symbol: str, px: float) -> None:
        self.symbol = symbol
        self._px = px

    def price(self) -> float:
        return self._px

    def __repr__(self) -> str:
        return f"Stock({self.symbol!r}, {self._px})"


class Future:
    def __init__(self, code: str, mark: float) -> None:
        self.code = code
        self.mark = mark

    def price(self) -> float:
        return self.mark

    def __repr__(self) -> str:
        return f"Future({self.code!r}, {self.mark})"


def main() -> None:
    s = [Stock("AAPL", 190.5), Stock("TSLA", 170.25)]
    f = [Future("ES", 5200.0), Future("NQ", 18000.0)]
    print("max stock ->", max_by_price(s))
    print("max future ->", max_by_price(f))


if __name__ == "__main__":
    main()

