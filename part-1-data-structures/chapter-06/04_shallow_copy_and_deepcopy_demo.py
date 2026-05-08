"""
对应笔记：04-浅拷贝为默认.md

Run:
  python part-1-data-structures/chapter-06/04_shallow_copy_and_deepcopy_demo.py

脚本说明：
- 教学演示：浅拷贝方式速查（copy.copy / [:] / list / .copy / dict）、赋值 vs 浅 vs 深、嵌套可变项、Bus、循环 deepcopy；请与笔记对照。
"""

from __future__ import annotations

import copy
from collections.abc import Callable
from typing import Any

from ch06_demo_support import section


def demo_shallow_copy_catalog_and_assignment_contrast() -> None:
    section("7) Shallow copy catalog + assignment vs shallow vs deep")

    a = [1, 2, [3, 4]]
    b_alias = a
    print("assignment (b = a): a is b_alias ->", a is b_alias)

    def check(name: str, fn: Callable[[Any], Any]) -> None:
        x = [1, 2, [3, 4]]
        y = fn(x)
        print(
            f"{name:12} outer new={x is not y!s:5} inner list shared (x[2] is y[2]) -> {x[2] is y[2]}"
        )

    check("copy.copy", copy.copy)
    check("slice [:]", lambda x: x[:])
    check("list(...)", list)
    check("list.copy", lambda x: x.copy())

    d1 = {"x": [1, 2]}
    d2 = dict(d1)
    print("dict(dict): d1['x'] is d2['x'] ->", d1["x"] is d2["x"])

    src = [1, 2, [3, 4]]
    shallow = copy.copy(src)
    shallow[0] = 99
    shallow[2][0] = 999
    print("after shallow[0]=99 and shallow[2][0]=999")
    print("  src    :", src)
    print("  shallow:", shallow)

    base = [1, 2, [3, 4]]
    deep = copy.deepcopy(base)
    base[2][0] = 111
    print("after deepcopy: mutating base[2][0]=111")
    print("  base:", base)
    print("  deep:", deep, "| inner independent ->", base[2] is not deep[2])


def demo_shallow_copy_three_ways_and_trap() -> None:
    section("8) Shallow copy: three syntaxes and the nested-mutable trap")

    l1 = [3, [66, 55, 44], (7, 8, 9)]
    l2a = list(l1)
    l2b = l1[:]
    l2c = l1.copy()

    print("l1 == l2a:", l1 == l2a, "| l1 is l2a:", l1 is l2a)
    print("inner list shared (l1[1] is l2a[1]):", l1[1] is l2a[1])
    print("inner tuple shared (l1[2] is l2a[2]):", l1[2] is l2a[2])

    l1.append(100)
    print("after l1.append(100)")
    print("l1 :", l1)
    print("l2a:", l2a)

    l1[1].remove(55)
    print("after l1[1].remove(55) (mutates shared inner list)")
    print("l1 :", l1)
    print("l2a:", l2a)

    l1[1] += [33, 22]
    print("after l1[1] += [33, 22] (in-place list extend)")
    print("l1 :", l1)
    print("l2a:", l2a)

    l1[2] += (10, 11)
    print("after l1[2] += (10, 11) (new tuple + rebinding)")
    print("l1 :", l1)
    print("l2a:", l2a)

    print("l2b inner list shared:", l1[1] is l2b[1])
    print("l2c inner list shared:", l1[1] is l2c[1])


class Bus:
    def __init__(self, passengers: list[str] | None = None) -> None:
        self.passengers = [] if passengers is None else list(passengers)

    def pick(self, name: str) -> None:
        self.passengers.append(name)

    def drop(self, name: str) -> None:
        self.passengers.remove(name)

    def __repr__(self) -> str:
        return f"Bus(passengers={self.passengers!r})"


def demo_copy_vs_deepcopy_bus_and_cycles() -> None:
    section("9) copy.copy vs copy.deepcopy with Bus (and cycle-safe deepcopy)")

    bus1 = Bus(["Alice", "Bill", "Claire", "David"])
    bus2 = copy.copy(bus1)
    bus3 = copy.deepcopy(bus1)

    print("bus1 is bus2:", bus1 is bus2)
    print("bus1.passengers is bus2.passengers:", bus1.passengers is bus2.passengers)
    print("bus1.passengers is bus3.passengers:", bus1.passengers is bus3.passengers)
    print("id(passengers):", id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))

    bus1.drop("Bill")
    print("after bus1.drop('Bill')")
    print("bus1:", bus1)
    print("bus2 (shallow copy shares list):", bus2)
    print("bus3 (deepcopy independent):", bus3)

    a = [10, 20]
    b = [a, a]
    a.append(b)
    c = copy.deepcopy(a)
    print("cycle deepcopy ok:", c[0:2], "| len(c):", len(c))
    print("c[2][0] is c:", c[2][0] is c)


def demo_shallow_vs_deep_copy() -> None:
    section("10) Shallow copy vs deep copy")
    original = [1, [2, 3], 4]
    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    print("id(original) != id(shallow):", id(original) != id(shallow))
    print("shared inner list (original[1] is shallow[1]):", original[1] is shallow[1])
    print("deep inner list independent (original[1] is deep[1]):", original[1] is deep[1])

    original[1].append(99)
    print("after original[1].append(99)")
    print("original:", original)
    print("shallow :", shallow)
    print("deep    :", deep)


def main() -> None:
    demo_shallow_copy_catalog_and_assignment_contrast()
    demo_shallow_copy_three_ways_and_trap()
    demo_copy_vs_deepcopy_bus_and_cycles()
    demo_shallow_vs_deep_copy()


if __name__ == "__main__":
    main()
