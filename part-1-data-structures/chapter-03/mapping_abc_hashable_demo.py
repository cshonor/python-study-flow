"""
Demo for 05-mapping-abc-and-hashable.md

Run:
  python part-1-data-structures/chapter-03/mapping_abc_hashable_demo.py
"""

from __future__ import annotations

import collections.abc as abc
import sys
from collections import UserDict
from dataclasses import dataclass


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_mapping_star_capture() -> None:
    section("1) match mapping pattern: **rest (must be last)")
    food = {"category": "ice cream", "flavor": "vanilla", "cost": 199}
    if sys.version_info < (3, 10):
        print("Need 3.10+ for match/case (PEP 634).")
        return
    match food:
        case {"category": "ice cream", **details}:
            print("details:", details)
    assert details == {"flavor": "vanilla", "cost": 199}


def demo_isinstance_mapping() -> None:
    section("2) isinstance Mapping vs type is dict")
    d: dict[str, int] = {}
    ud = UserDict(a=1)
    print("dict -> Mapping:", isinstance(d, abc.Mapping))
    print("dict -> MutableMapping:", isinstance(d, abc.MutableMapping))
    print("UserDict -> Mapping:", isinstance(ud, abc.Mapping))


def demo_hash_tuple_and_error() -> None:
    section("3) hash: tuple of hashables, fail on list inside tuple")
    tt = (1, 2, (30, 40))
    print("hash(tt):", hash(tt))
    tf = (1, 2, frozenset([30, 40]))
    print("hash(tf):", hash(tf))
    ti = (1, 2, [30, 40])
    try:
        hash(ti)
    except TypeError as e:
        print("hash(ti) -> TypeError:", e)


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def demo_frozen_dataclass_hashable() -> None:
    section("4) hashable dataclass (frozen=True)")
    p = Point(1, 2)
    q = Point(1, 2)
    print("hash(p), p == q:", hash(p), p == q)
    d: dict[Point, str] = {p: "origin"}
    print("dict keyed by Point:", d[q])


def main() -> None:
    demo_mapping_star_capture()
    demo_isinstance_mapping()
    demo_hash_tuple_and_error()
    demo_frozen_dataclass_hashable()


if __name__ == "__main__":
    main()
