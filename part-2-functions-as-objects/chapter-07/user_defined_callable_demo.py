"""
Demo for 06-user-defined-callable-types.md (Fluent Python 7.6)

Run from repo root:
  python part-2-functions-as-objects/chapter-07/user_defined_callable_demo.py
"""

from __future__ import annotations

import random


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


class BingoCage:
    def __init__(self, items) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError as e:
            raise LookupError("pick from empty BingoCage") from e

    def __call__(self):
        return self.pick()


def main() -> None:
    section("BingoCage: pick() and __call__()")
    cage = BingoCage(range(5))
    print("callable(cage):", callable(cage))
    print("pick via method:", cage.pick())
    print("pick via call  :", cage())

    section("Drain the cage")
    picked = []
    while True:
        try:
            picked.append(cage())
        except LookupError as e:
            print("LookupError:", e)
            break
    print("picked:", picked)


if __name__ == "__main__":
    main()

