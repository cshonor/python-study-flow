"""
Demo for 02-dict-comprehension.md

Run:
  python part-1-data-structures/chapter-03/dict_comprehension_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_dial_codes() -> None:
    section("1) dial_codes -> country_dial (swap key/value)")
    dial_codes = [
        (880, "Bangladesh"),
        (55, "Brazil"),
        (86, "China"),
        (91, "India"),
        (62, "Indonesia"),
        (81, "Japan"),
        (234, "Nigeria"),
        (92, "Pakistan"),
        (7, "Russia"),
        (1, "United States"),
    ]
    country_dial = {country: code for code, country in dial_codes}
    print("country_dial:", country_dial)


def demo_sorted_filtered() -> None:
    section("2) sorted items + filter + upper (code < 70)")
    country_dial = {
        "Bangladesh": 880,
        "Brazil": 55,
        "China": 86,
        "India": 91,
        "Indonesia": 62,
        "Japan": 81,
        "Nigeria": 234,
        "Pakistan": 92,
        "Russia": 7,
        "United States": 1,
    }
    out = {
        code: country.upper()
        for country, code in sorted(country_dial.items())
        if code < 70
    }
    print(out)


def demo_duplicate_key() -> None:
    section("3) duplicate keys: last wins")
    d = {k: v for k, v in [(1, "a"), (1, "b")]}
    print(d)


def demo_set_comprehension() -> None:
    section("4) set comprehension")
    evens = {x for x in range(1, 11) if x % 2 == 0}
    print(evens)


def demo_exercises() -> None:
    section("5) exercise answers (grades + drop None)")
    grades = [("Ann", 88), ("Bob", 55), ("Cara", 72)]
    passing = {name: score for name, score in grades if score >= 60}
    print("passing >= 60:", passing)

    raw = {"a": 1, "b": None, "c": 2}
    cleaned = {k: v for k, v in raw.items() if v is not None}
    print("drop None:", cleaned)


def main() -> None:
    demo_dial_codes()
    demo_sorted_filtered()
    demo_duplicate_key()
    demo_set_comprehension()
    demo_exercises()


if __name__ == "__main__":
    main()
