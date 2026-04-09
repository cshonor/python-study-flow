from __future__ import annotations

from typing import NotRequired, TypedDict


class StockData(TypedDict):
    symbol: str
    price: float
    ts: int  # epoch seconds for demo
    currency: NotRequired[str]


def mid_price(tick: StockData) -> float:
    return tick["price"]


def main() -> None:
    tick1: StockData = {"symbol": "AAPL", "price": 190.5, "ts": 1712570000}
    tick2: StockData = {
        "symbol": "TSLA",
        "price": 170.25,
        "ts": 1712570001,
        "currency": "USD",
    }
    print("tick1:", tick1)
    print("tick2:", tick2)
    print("mid_price:", mid_price(tick2))


if __name__ == "__main__":
    main()

