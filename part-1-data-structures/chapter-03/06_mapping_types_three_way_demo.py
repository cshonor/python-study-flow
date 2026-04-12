"""
Demo for 06-dict-defaultdict与OrderedDict对照.md

Run:
  python part-1-data-structures/chapter-03/06_mapping_types_three_way_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import sys
from collections import OrderedDict, defaultdict


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_defaultdict_count() -> None:
    section("1) defaultdict(int): count without key check")
    words = "to be or not to be".split()
    wc: defaultdict[str, int] = defaultdict(int)
    for w in words:
        wc[w] += 1
    print(dict(wc))


def demo_get_vs_getitem() -> None:
    section("2) get() does NOT call default_factory")
    dd: defaultdict[str, list[str]] = defaultdict(list)
    _ = dd["missing"]  # triggers factory, inserts key
    print("after d['missing']:", dict(dd))
    dd2: defaultdict[str, list[str]] = defaultdict(list)
    g = dd2.get("nope")
    print("dd2.get('nope'):", g)
    print("dd2 keys after get:", list(dd2.keys()))


def demo_fromkeys_trap() -> None:
    section("3) dict.fromkeys mutable default: shared reference")
    bad = dict.fromkeys(["a", "b"], [])
    bad["a"].append(1)
    print("bad (shared list):", bad)
    good = {k: [] for k in ["a", "b"]}
    good["a"].append(1)
    print("good (independent lists):", good)


def demo_ordered_move_to_end() -> None:
    section("4) OrderedDict.move_to_end")
    od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
    od.move_to_end("a", last=False)
    print(list(od.keys()))
    last, val = od.popitem(last=True)
    print("popitem last:", last, val)


class User:
    __slots__ = ("user_id", "name")

    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.user_id == other.user_id and self.name == other.name

    def __hash__(self) -> int:
        return hash((self.user_id, self.name))


def demo_hashable_user() -> None:
    section("5) custom __eq__ + __hash__ for dict key")
    u1 = User(1, "Ann")
    u2 = User(1, "Ann")
    registry: dict[User, str] = {u1: "ok"}
    print("u1 == u2:", u1 == u2)
    print("registry[u2]:", registry[u2])


def demo_merge_or() -> None:
    section("6) dict | and |= (PEP 584, 3.9+)")
    if sys.version_info < (3, 9):
        print("skip: need Python 3.9+")
        return
    d1 = {"a": 1, "b": 3}
    d2 = {"a": 2, "c": 6}
    print("d1 | d2:", d1 | d2)
    left = {"a": 1, "b": 3}
    left |= d2
    print("after left |= d2:", left)


def demo_lru_ordered() -> None:
    section("7) OrderedDict: access moves to end, evict oldest (capacity 2)")
    cap = 2
    od: OrderedDict[str, int] = OrderedDict()
    for key in ("a", "b", "c"):
        if key in od:
            od.move_to_end(key)
        od[key] = 1
        while len(od) > cap:
            od.popitem(last=False)
    print("final keys (FIFO evict):", list(od.keys()))


def main() -> None:
    demo_defaultdict_count()
    demo_get_vs_getitem()
    demo_fromkeys_trap()
    demo_ordered_move_to_end()
    demo_hashable_user()
    demo_merge_or()
    demo_lru_ordered()


if __name__ == "__main__":
    main()
