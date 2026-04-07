"""
Demo for 08-list-sort-vs-sorted.md

Run:
  python part-1-data-structures/chapter-02/list_sort_vs_sorted_demo.py
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from operator import attrgetter, itemgetter


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_sort_returns_none() -> None:
    section("1) list.sort() is in-place; return value is None")
    data = [3, 1, 2]
    ret = data.sort()
    print("return value of .sort():", ret)
    print("data after sort:", data)
    # a = data.sort()  # bug: a would be None


def demo_sorted_any_iterable() -> None:
    section("2) sorted() builds a new list; leaves tuple/str unchanged")
    t = (3, 1, 2)
    new_t = sorted(t)
    print("tuple t unchanged?", t)
    print("sorted(t) -> new list:", new_t)

    s = "cba"
    print("sorted(s) chars:", sorted(s))


def demo_reverse_and_key() -> None:
    section("3) reverse= and key= (both APIs)")
    words = ["apple", "Banana", "cherry"]
    w = words.copy()
    w.sort(key=str.lower)
    print("words.sort(key=str.lower):", w)

    nums = [3, 1, 4, 1]
    print("sorted(nums, reverse=True):", sorted(nums, reverse=True))


def demo_itemgetter_attrgetter() -> None:
    section("4) key=itemgetter / attrgetter (dicts + dataclass)")

    rows = [
        {"name": "bob", "score": 90},
        {"name": "Ada", "score": 90},
        {"name": "ada", "score": 80},
    ]
    by_score_then_name = sorted(rows, key=itemgetter("score", "name"))
    print("by (score, name):", by_score_then_name)

    @dataclass
    class User:
        dept: str
        name: str

    users = [
        User("sales", "Zoe"),
        User("eng", "Ann"),
        User("eng", "Bob"),
    ]
    by_dept_name = sorted(users, key=attrgetter("dept", "name"))
    print("users by dept, name:", [(u.dept, u.name) for u in by_dept_name])


def demo_stable_sort_two_pass() -> None:
    section("5) stable sort: two passes for primary / secondary key")
    pairs = [(1, "b"), (2, "a"), (1, "a"), (2, "b")]
    # Want: sort by first ascending, then by second ascending within ties.
    # Stable sort: sort by secondary first, then by primary.
    step1 = sorted(pairs, key=lambda p: p[1])
    step2 = sorted(step1, key=lambda p: p[0])
    print("pairs:", pairs)
    print("after stable two-pass:", step2)


def demo_shuffle_returns_none() -> None:
    section("6) random.shuffle is also in-place, returns None")
    deck = list(range(5))
    r = random.shuffle(deck)
    print("shuffle return:", r)
    print("deck mutated:", deck)


def main() -> None:
    random.seed(0)
    demo_sort_returns_none()
    demo_sorted_any_iterable()
    demo_reverse_and_key()
    demo_itemgetter_attrgetter()
    demo_stable_sort_two_pass()
    demo_shuffle_returns_none()


if __name__ == "__main__":
    main()
