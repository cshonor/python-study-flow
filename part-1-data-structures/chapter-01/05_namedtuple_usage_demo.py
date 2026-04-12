"""
与 05-namedtuple用法指南与rename参数.md 配套的演示脚本。

运行：python part-1-data-structures/chapter-01/05_namedtuple_usage_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

from collections import namedtuple


def demo_field_names_forms() -> None:
    """2.1.2：field_names 可用 list / 空格字符串 / tuple，三种写法等价。"""
    Card_a = namedtuple("Card", ["rank", "suit"])
    Card_b = namedtuple("Card", "rank suit")
    Card_c = namedtuple("Card", ("rank", "suit"))
    c = Card_a("A", "spades")
    assert c == Card_b("A", "spades") == Card_c("A", "spades")
    print("[field_names] list / str / tuple 三种定义得到等价 Card:", c)


def demo_rename() -> None:
    """2.1.3：rename=True 时，非法/重复字段名会被改成 _1、_2…"""
    Person = namedtuple("Person", ["name", "class", "name"], rename=True)
    print("[rename] Person._fields =", Person._fields)
    p = Person("Tom", "3A", "dup")
    print("[rename] 实例:", p)


def demo_card_full() -> None:
    """第 3、4 节：扑克牌 + 访问、遍历、解包、_make / _asdict / _replace。"""
    Card = namedtuple("Card", ["rank", "suit"])

    card1 = Card("A", "spade")
    card2 = Card("K", "heart")

    print("[访问] .rank / .suit:", card1.rank, card1.suit)
    print("[访问] 下标 [0] [1]:", card1[0], card1[1])

    print("[遍历]", list(card1))
    rank, suit = card1
    print("[解包] rank, suit =", rank, suit)

    card3 = Card._make(["Q", "club"])
    print("[_make]", card3)

    print("[_asdict]", card1._asdict())

    new_card = card1._replace(rank="2")
    print("[_replace] 原 card1 不变:", card1, "新实例:", new_card)

    # 不可变：下面一行若取消注释会报 AttributeError
    # card1.rank = "B"


def demo_tuple_subclass() -> None:
    """5.1：是 tuple 子类，可用 isinstance 与元组操作。"""
    Card = namedtuple("Card", ["rank", "suit"])
    c = Card("7", "diamonds")
    print("[tuple 子类] isinstance(c, tuple):", isinstance(c, tuple))
    print("[repr]", repr(c))


def main() -> None:
    print("=== namedtuple 用法演示（对应 05-namedtuple用法指南与rename参数.md）===\n")
    demo_field_names_forms()
    print()
    demo_rename()
    print()
    demo_card_full()
    print()
    demo_tuple_subclass()
    print("\n说明：field_names 是「字段名字符串」的可迭代；与 array.array 存数值无关。")


if __name__ == "__main__":
    main()
