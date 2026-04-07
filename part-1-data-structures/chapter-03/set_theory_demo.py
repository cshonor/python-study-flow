"""
Demo for 13-sets-and-frozenset.md (Fluent Python §3.10–§3.11).

Run:
  python part-1-data-structures/chapter-03/set_theory_demo.py
"""

from __future__ import annotations

from unicodedata import name


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_empty_literal() -> None:
    section("1) Empty {} is dict, not set")
    empty_braces = {}
    empty_set = set()
    print("type({}):", type(empty_braces))
    print("type(set()):", type(empty_set))


def demo_dedupe_ordered() -> None:
    section("2) Dedupe: unordered set vs ordered dict.fromkeys (3.7+)")
    l = ["spam", "spam", "eggs", "spam", "bacon", "eggs"]
    print("list -> set -> list (order not guaranteed):", list(set(l)))
    print("preserve first-seen order:", list(dict.fromkeys(l)))


def demo_membership_and_intersection() -> None:
    section("3) needles & haystack; intersection with list")
    needles = {1, 2, 3}
    haystack = {2, 3, 4, 5}
    print("len(needles & haystack):", len(needles & haystack))

    a = {1, 2, 3}
    b_list = [3, 4, 5]
    print("a.intersection(b_list):", a.intersection(b_list))
    try:
        print(a & b_list)
    except TypeError as e:
        print("a & list -> TypeError:", e)


def demo_set_comp_unichar() -> None:
    section("4) Set comprehension: chars whose Unicode name contains SIGN")
    chars = {chr(i) for i in range(32, 256) if "SIGN" in name(chr(i), "")}
    codes = sorted(ord(c) for c in chars)[:8]
    print("count:", len(chars), "sample codepoints (hex):", [hex(c) for c in codes])


def demo_frozenset_nested() -> None:
    section("5) Nested frozenset inside set")
    outer: set[frozenset[int]] = {frozenset({1, 2}), frozenset({3})}
    print(outer)


def main() -> None:
    demo_empty_literal()
    demo_dedupe_ordered()
    demo_membership_and_intersection()
    demo_set_comp_unichar()
    demo_frozenset_nested()


if __name__ == "__main__":
    main()
