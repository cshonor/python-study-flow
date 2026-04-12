"""
Demo for 07-08-数据类异味与match-case.md

Requires Python 3.10+ for match/case.

Run from repo root:
  python part-1-data-structures/chapter-05/dataclass_code_smell_and_match_demo.py
"""

from __future__ import annotations

from dataclasses import dataclass


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def safe(obj: object) -> object:
    # Windows consoles may use GBK; ascii() avoids UnicodeEncodeError for demos.
    return ascii(obj) if isinstance(obj, str) else obj


@dataclass
class City:
    continent: str
    name: str
    country: str
    population_m: float


def demo_keyword_pattern(cities: list[City]) -> None:
    section("1) Keyword pattern: match by field names (recommended)")

    for c in cities:
        match c:
            case City(continent="Asia", name=name, population_m=pop) if pop >= 20:
                print("Asia mega-city:", safe(name), "| pop_m:", pop)
            case City(continent="Asia", name=name):
                print("Asia city:", safe(name))
            case City(continent="North America", country="US", name=name):
                print("US city:", safe(name))
            case _:
                print("Other:", safe(c.name), "|", safe(c.continent))


def demo_positional_pattern(cities: list[City]) -> None:
    section("2) Positional class pattern: depends on __match_args__ order")

    print("City.__match_args__:", City.__match_args__)
    for c in cities:
        match c:
            case City("Asia", name, country, pop):
                print("POS Asia ->", safe(name), safe(country), pop)
            case City(continent, name, _, _):
                print("POS other continent ->", safe(continent), ":", safe(name))


def demo_sequence_pattern_with_type_constraints() -> None:
    section("3) Sequence pattern + type checks (for list/tuple-like records)")

    records: list[object] = [
        ["Tokyo", 35.6895, 139.6917],
        ["BadLat", "35.0", 139.0],
        ("Delhi", 28.61, 77.23),
        ["TooLong", 1.0, 2.0, 3.0],
    ]

    for rec in records:
        match rec:
            case [str() as name, float() as lat, float() as lon]:
                print("LIST ok:", safe(name), lat, lon)
            case (str() as name, float() as lat, float() as lon):
                print("TUPLE ok:", safe(name), lat, lon)
            case _:
                print("no match:", repr(rec))


def main() -> None:
    cities = [
        City("Asia", "Tokyo", "JP", 36.933),
        City("Asia", "Delhi NCR", "IN", 21.935),
        City("North America", "New York", "US", 8.406),
        City("South America", "São Paulo", "BR", 21.650),
    ]

    demo_keyword_pattern(cities)
    demo_positional_pattern(cities)
    demo_sequence_pattern_with_type_constraints()


if __name__ == "__main__":
    main()

