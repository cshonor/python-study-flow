"""
对应笔记：07-不可变类型技巧.md

Run:
  python part-1-data-structures/chapter-06/07_immutable_type_tricks_demo.py

脚本说明：
- 教学演示：元组/frozenset 复用、字符串驻留、`sys.intern`、小整数缓存提示；请与笔记对照。
"""

from __future__ import annotations

import sys

from ch06_demo_support import section


def demo_immutable_type_tricks() -> None:
    section("22) Immutable tricks: tuple/frozenset reuse, string interning, small ints")

    t1 = (1, 2, 3)
    t2 = tuple(t1)
    t3 = t1[:]
    print("tuple(t1) is t1:", t2 is t1)
    print("t1[:] is t1:", t3 is t1)

    fs1 = frozenset({1, 2, 3})
    fs2 = fs1.copy()
    print("fs1.copy() is fs1:", fs2 is fs1)

    s1 = "ABC"
    s2 = "ABC"
    s3 = "".join(["A", "B", "C"])
    print("s1 is s2 (literal):", s1 is s2)
    print("s1 == s3:", s1 == s3, "| s1 is s3 (runtime build):", s1 is s3)
    si1 = sys.intern(s3)
    si2 = sys.intern("ABC")
    print("sys.intern(s3) is sys.intern('ABC'):", si1 is si2)

    a = 10
    b = 10
    c = int("10")
    print("10: a is b:", a is b, "| a is int('10'):", a is c)


def demo_small_int_and_string_interning_warning() -> None:
    section("14) CPython caching (don't rely on it): small ints / some strings")
    a = 256
    b = 256
    print("256: a is b ->", a is b, "(implementation detail)")
    a2 = 257
    b2 = 257
    print("257: a2 is b2 ->", a2 is b2, "(implementation detail)")

    s1 = "hello_world"
    s2 = "hello_" + "world"
    print("strings: s1 == s2 ->", s1 == s2)
    print("strings: s1 is s2 ->", s1 is s2, "(may be True/False depending on interning)")


def main() -> None:
    demo_immutable_type_tricks()
    demo_small_int_and_string_interning_warning()


if __name__ == "__main__":
    main()
