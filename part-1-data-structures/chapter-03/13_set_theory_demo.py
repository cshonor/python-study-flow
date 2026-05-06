"""
Demo for 13-集合与frozenset.md (Fluent Python §3.10–§3.11).

Run:
  python part-1-data-structures/chapter-03/13_set_theory_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
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


def demo_one_liners() -> None:
    """与 13-集合与frozenset.md §零 口诀一一对应的一行一例。"""
    section("6) One-liners for §零 mnemonics")

    # 1) 哈希 + 可哈希元素 + O(1) 成员测试
    s = frozenset((1, 2, 3))
    print("1 hashable + membership:", 2 in s, "| type:", type(s))

    # 2) set 不可作 dict 键；frozenset 可作 dict 键且可嵌套进 set
    d = {frozenset({1, 2}): "ok"}
    nested = {frozenset({1})}
    print("2 frozenset as dict key:", d[frozenset({1, 2})], "| set of frozenset:", nested)

    # 3) 去重：set 不保序 vs dict.fromkeys 保首次序（3.7+）
    seq = ["b", "a", "b", "c", "a"]
    print("3 set dedupe (order not guaranteed):", list(set(seq)))
    print("3 ordered dedupe:", list(dict.fromkeys(seq)))

    # 4) 运算符要集合型；方法吃可迭代
    a, lst = {1, 2}, [2, 3]
    print("4 method + list:", a.intersection(lst))
    print("4 set & frozenset OK:", a & frozenset(lst))


def main() -> None:
    demo_empty_literal()
    demo_dedupe_ordered()
    demo_membership_and_intersection()
    demo_set_comp_unichar()
    demo_frozenset_nested()
    demo_one_liners()


if __name__ == "__main__":
    main()
