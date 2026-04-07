"""
Demo for 03-mapping-unpack-and-merge.md (PEP 448, PEP 584)

Run:
  python part-1-data-structures/chapter-03/dict_unpack_merge_demo.py
"""

from __future__ import annotations

import sys
from collections import ChainMap


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_pep448_call() -> None:
    section("1) PEP 448: ** in function call")

    def dump(**kwargs: object) -> dict[str, object]:
        return kwargs

    out = dump(**{"x": 1}, y=2, **{"z": 3})
    print(out)
    assert out == {"x": 1, "y": 2, "z": 3}


def demo_pep448_literal() -> None:
    section("2) PEP 448: ** inside dict literal (later wins)")
    d = {"a": 0, **{"x": 1}, "y": 2, **{"z": 3, "x": 4}}
    print(d)
    assert d == {"a": 0, "x": 4, "y": 2, "z": 3}


def demo_merge_star_star() -> None:
    section("3) {**d1, **d2} shallow merge (3.5+)")
    d1 = {"a": 1, "b": 3}
    d2 = {"a": 2, "b": 4, "c": 6}
    merged = {**d1, **d2}
    print("merged:", merged)
    assert merged == {"a": 2, "b": 4, "c": 6}


def demo_pep584_pipe() -> None:
    section("4) PEP 584: | and |= (Python 3.9+)")
    if sys.version_info < (3, 9):
        print("skip: need Python 3.9+ for | and |=")
        return
    d1 = {"a": 1, "b": 3}
    d2 = {"a": 2, "b": 4, "c": 6}
    print("d1 | d2:", d1 | d2)
    left = {"a": 1, "b": 3}
    right = {"a": 2, "b": 4, "c": 6}
    left |= right
    print("after d1 |= d2:", left)
    assert left == {"a": 2, "b": 4, "c": 6}


def demo_update_and_chainmap() -> None:
    section("5) dict.update vs ChainMap")
    d1 = {"a": 1}
    d2 = {"a": 2, "b": 3}
    base = dict(d1)
    base.update(d2)
    print("after update:", base)

    cm = ChainMap(d1, d2)
    print("ChainMap['a'] (first mapping wins):", cm["a"])
    print("ChainMap['b']:", cm["b"])


def main() -> None:
    demo_pep448_call()
    demo_pep448_literal()
    demo_merge_star_star()
    demo_pep584_pipe()
    demo_update_and_chainmap()


if __name__ == "__main__":
    main()
