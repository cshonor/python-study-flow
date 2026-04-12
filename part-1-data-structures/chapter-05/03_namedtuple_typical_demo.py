"""
Demo for 03-典型具名元组namedtuple.md

Run:
  python part-1-data-structures/chapter-05/03_namedtuple_typical_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

from collections import namedtuple
from typing import NamedTuple, get_type_hints


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_city_basic_and_core_api() -> None:
    section("1) City namedtuple: basic usage + _fields/_make/_asdict/_replace")
    City = namedtuple("City", "name country population coordinates")

    tokyo = City("Tokyo", "JP", 36.933, (35.689722, 139.691667))
    print("tokyo:", tokyo)
    print("tokyo.name:", tokyo.name)
    print("tokyo[0]:", tokyo[0])

    print("City._fields:", City._fields)

    delhi_data = ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889))
    delhi = City._make(delhi_data)
    print("City._make(...):", delhi)

    print("delhi._asdict():", delhi._asdict())

    tokyo2 = tokyo._replace(population=37.0)
    print("tokyo._replace(...):", tokyo2)


def demo_defaults() -> None:
    section("2) defaults=... (rightmost fields get defaults)")
    Coordinate = namedtuple("Coordinate", "lat lon reference", defaults=[None])
    print("Coordinate(0,0):", Coordinate(0, 0))
    print("Coordinate(0,0,'GPS'):", Coordinate(0, 0, "GPS"))


def demo_dynamic_injection_card_rank() -> None:
    section("3) Dynamic injection: add class attributes/methods to a namedtuple class")
    Card = namedtuple("Card", ["rank", "suit"])

    rank_value = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    Card.suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)  # type: ignore[attr-defined]

    def overall_rank(self: Card) -> int:
        return rank_value[self.rank] * 4 + Card.suit_values[self.suit]  # type: ignore[attr-defined]

    Card.overall_rank = overall_rank  # type: ignore[attr-defined]

    deck = [Card(rank, suit) for suit in ["spades", "hearts"] for rank in ["2", "A"]]
    deck.sort(key=Card.overall_rank)  # type: ignore[attr-defined]
    print("sorted deck:", deck)
    print("best card overall_rank():", deck[-1].overall_rank())  # type: ignore[attr-defined]


def demo_typing_namedtuple_contrast() -> None:
    section("4) Contrast: typing.NamedTuple with annotations + methods")

    class CoordinateT(NamedTuple):
        lat: float
        lon: float

        def __str__(self) -> str:
            return f"({self.lat:.3f}, {self.lon:.3f})"

    c = CoordinateT(55.756, 37.617)
    print("CoordinateT:", c)
    print("str(CoordinateT):", str(c))
    print("type hints:", get_type_hints(CoordinateT))
    print("issubclass(CoordinateT, tuple):", issubclass(CoordinateT, tuple))


def main() -> None:
    demo_city_basic_and_core_api()
    demo_defaults()
    demo_dynamic_injection_card_rank()
    demo_typing_namedtuple_contrast()


if __name__ == "__main__":
    main()

