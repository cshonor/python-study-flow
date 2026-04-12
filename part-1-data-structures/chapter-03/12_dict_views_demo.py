"""
Demo for 12-字典视图.md (Fluent Python §3.8).

Run:
  python part-1-data-structures/chapter-03/12_dict_views_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

from collections.abc import ItemsView, KeysView, ValuesView


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_basic() -> None:
    section("1) Basic: len, iter, list, reversed(values)")
    d = dict(a=10, b=20, c=30)
    values = d.values()
    print("values repr:", values)
    print("len(values):", len(values))
    print("list(values):", list(values))
    print("reversed(values):", list(reversed(values)))

    try:
        _ = values[0]
    except TypeError as e:
        print("values[0] -> TypeError:", e)


def demo_live_sync() -> None:
    section("2) View tracks live dict mutations")
    d = dict(a=10, b=20, c=30)
    values = d.values()
    print("before:", list(values))
    d["z"] = 99
    print("after d['z']=99, same values view:", list(values))


def demo_set_ops() -> None:
    section("3) Set-like ops: dict_keys & ; dict_items | (hashable pairs)")
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2, "c": 3}
    print("d1.keys() & d2.keys():", d1.keys() & d2.keys())

    i1 = {("x", 1), ("y", 2)}
    d3 = dict(i1)
    d4 = dict([("y", 2), ("z", 3)])
    print("d3.items() | d4.items():", d3.items() | d4.items())


def demo_abc_and_construct() -> None:
    section("4) ABC registration + cannot instantiate dict_values()")
    d = {"k": 1}
    print("isinstance(keys, KeysView):", isinstance(d.keys(), KeysView))
    print("isinstance(values, ValuesView):", isinstance(d.values(), ValuesView))
    print("isinstance(items, ItemsView):", isinstance(d.items(), ItemsView))

    vc = type({}.values())
    print("type({}.values()):", vc)
    try:
        vc()
    except TypeError as e:
        print("dict_values() ->", e)


def main() -> None:
    demo_basic()
    demo_live_sync()
    demo_set_ops()
    demo_abc_and_construct()


if __name__ == "__main__":
    main()
