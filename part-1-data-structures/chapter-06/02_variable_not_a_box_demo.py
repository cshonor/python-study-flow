"""
对应笔记：02-变量不是盒子.md

Run:
  python part-1-data-structures/chapter-06/02_variable_not_a_box_demo.py

脚本说明：
- 教学演示：名称即标签、赋值从右到左与 Gizmo 反例；请与笔记对照。
"""

from __future__ import annotations

from ch06_demo_support import section


def demo_names_are_labels() -> None:
    section("1) Names are labels: aliasing vs rebinding")
    a = [1, 2, 3]
    b = a
    print("id(a) == id(b):", id(a) == id(b))
    a.append(4)
    print("after a.append(4) -> a:", a, "b:", b)
    a = []  # rebinding a; b still points to old list
    print("after rebinding a = [] -> a:", a, "b:", b)


def demo_assignment_right_to_left_gizmo() -> None:
    section("2) Assignment is right-to-left: object created before error (Gizmo)")

    class Gizmo:
        def __init__(self) -> None:
            print("Gizmo created, id:", id(self))

    x = Gizmo()
    print("x bound:", x is not None)
    try:
        y = Gizmo() * 10  # type: ignore[operator]
        print("y bound:", y)  # pragma: no cover
    except TypeError as e:
        print("TypeError:", e)
        print("'y' in locals():", "y" in locals())


def main() -> None:
    demo_names_are_labels()
    demo_assignment_right_to_left_gizmo()


if __name__ == "__main__":
    main()
