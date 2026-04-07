"""
Demo for 10-dict-variants-ordered-chain-counter.md (Fluent Python §3.6).

Run:
  python part-1-data-structures/chapter-03/dict_variants_demo.py
"""

from __future__ import annotations

import builtins
from collections import ChainMap, Counter, OrderedDict


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_ordered_dict() -> None:
    section("1) OrderedDict: move_to_end, popitem, equality nuance")
    od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
    od.move_to_end("a")
    print("after move_to_end(a):", list(od.keys()))
    od.move_to_end("c", last=False)
    print("after move_to_end(c, last=False):", list(od.keys()))
    k, v = od.popitem(last=False)
    print("popitem last=False:", k, v)

    od_a = OrderedDict([("a", 1), ("b", 2)])
    od_b = OrderedDict([("b", 2), ("a", 1)])
    print("OD(a,b) == OD(b,a):", od_a == od_b)
    print("OD == plain dict (same items):", od_a == {"a": 1, "b": 2})


def demo_chainmap() -> None:
    section("2) ChainMap: lookup chain, writes go to first mapping")
    d1 = {"a": 1, "b": 3}
    d2 = {"a": 2, "b": 4, "c": 6}
    chain = ChainMap(d1, d2)
    print("chain['a'], chain['c']:", chain["a"], chain["c"])
    chain["c"] = -1
    print("after chain['c'] = -1, d1:", d1)
    print("d2 unchanged:", d2)

    py_lookup = ChainMap(locals(), globals(), vars(builtins))
    print("len via ChainMap:", py_lookup["len"]([1, 2, 3]))


def demo_counter() -> None:
    section("3) Counter: count and most_common")
    words = ["a", "b", "a", "c", "b", "a"]
    cnt = Counter(words)
    print(cnt)
    print("most_common(2):", cnt.most_common(2))
    cnt.update(["a", "d"])
    print("after update:", dict(cnt))


def main() -> None:
    demo_ordered_dict()
    demo_chainmap()
    demo_counter()


if __name__ == "__main__":
    main()
