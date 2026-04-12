"""
Demo for 01-第3章字典与集合总览.md

Run:
  python part-1-data-structures/chapter-03/dict_and_set_quickstart_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

from collections import Counter


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_get_and_setdefault() -> None:
    section("1) get vs [] and setdefault")
    d: dict[str, int] = {"a": 1}
    print("d.get('missing', 0):", d.get("missing", 0))
    d.setdefault("a", 99)
    d.setdefault("b", 2)
    print("after setdefault:", d)


def demo_counter() -> None:
    section("2) Counter: word frequency")
    words = "to be or not to be".split()
    c = Counter(words)
    print("Counter:", dict(c))
    print("most common 2:", c.most_common(2))


def demo_set_ops() -> None:
    section("3) set operations")
    a = {1, 2, 3}
    b = {2, 3, 4}
    print("a | b", a | b)
    print("a & b", a & b)
    print("a - b", a - b)


def demo_frozenset_as_key() -> None:
    section("4) frozenset as dict key (set is not hashable)")
    fs = frozenset({1, 2})
    d = {fs: "ok"}
    print("dict with frozenset key:", d)
    mutable_set = {1, 2}
    try:
        {mutable_set: "bad"}
    except TypeError as e:
        print("set as key -> TypeError:", e)


def main() -> None:
    demo_get_and_setdefault()
    demo_counter()
    demo_set_ops()
    demo_frozenset_as_key()


if __name__ == "__main__":
    main()
