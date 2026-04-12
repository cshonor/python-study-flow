"""
对应笔记：03-同一性相等与别名.md

Run:
  python part-1-data-structures/chapter-06/03_identity_equality_aliasing_demo.py

脚本说明：
- 教学演示：`is`/`==`、别名、None 判断、元组相对不可变与 hash；请与笔记对照。
"""

from __future__ import annotations

from ch06_demo_support import section


def demo_aliasing_identity_vs_equality() -> None:
    section("3) Aliasing with dict: identity vs equality")
    charles = {"name": "Charles L. Dodgson", "born": 1832}
    lewis = charles
    print("lewis is charles:", lewis is charles)
    print("id(charles) == id(lewis):", id(charles) == id(lewis))
    lewis["balance"] = 950
    print("after lewis['balance']=950 -> charles:", charles)

    alex = {"name": "Charles L. Dodgson", "born": 1832, "balance": 950}
    print("alex == charles:", alex == charles)
    print("alex is charles:", alex is charles)


def demo_none_comparison_is_safer() -> None:
    section("4) None comparison: why `is None` is safer than `== None`")

    class WeirdEq:
        def __eq__(self, other: object) -> bool:  # can lie
            return other is None

    w = WeirdEq()
    print("w == None:", w == None)  # noqa: E711 (intentional demo)
    print("w is None:", w is None)


def demo_tuple_relative_immutability_and_hash() -> None:
    section("5) Tuple relative immutability and hashing")

    t1 = (1, 2, [30, 40])
    t2 = (1, 2, [30, 40])
    print("t1 == t2:", t1 == t2)
    print("id(t1[-1]) == id(t2[-1]):", id(t1[-1]) == id(t2[-1]))

    t1[-1].append(99)
    print("after t1[-1].append(99) -> t1:", t1)
    print("t1 == t2:", t1 == t2)

    try:
        print("hash(t1):", hash(t1))
    except Exception as e:
        print("hash(t1) ->", type(e).__name__ + ":", e)


def demo_is_vs_eq() -> None:
    section("6) is vs == (identity vs equality)")
    x = [1, 2]
    y = [1, 2]
    print("x == y:", x == y)
    print("x is y:", x is y)
    z = x
    print("x is z:", x is z)
    print("x == z:", x == z)
    n = None
    print("n is None:", n is None)


def demo_tuple_relative_immutability() -> None:
    section("7) Tuple is 'relatively immutable'")
    t = (1, [2, 3])
    print("t before:", t)
    t[1].append(4)
    print("t after t[1].append(4):", t)
    try:
        t[1] = [9]  # type: ignore[misc]
    except Exception as e:
        print("t[1] = ... ->", type(e).__name__ + ":", e)


def main() -> None:
    demo_aliasing_identity_vs_equality()
    demo_none_comparison_is_safer()
    demo_tuple_relative_immutability_and_hash()
    demo_is_vs_eq()
    demo_tuple_relative_immutability()


if __name__ == "__main__":
    main()
