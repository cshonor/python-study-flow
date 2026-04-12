"""
Demo for 14-字典视图集合运算.md (Fluent Python §3.12).

Run:
  python part-1-data-structures/chapter-03/dict_view_setops_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_keys_items_ops() -> None:
    section("1) dict_keys / dict_items: & | -")
    d1 = {"a": 1, "b": 2, "c": 3}
    d2 = {"b": 2, "c": 3, "d": 4}
    print("keys intersection:", d1.keys() & d2.keys())
    print("items intersection:", d1.items() & d2.items())
    print("keys difference d1 - d2:", d1.keys() - d2.keys())
    print("keys union:", d1.keys() | d2.keys())


def demo_values_rejected() -> None:
    section("2) dict_values: no &")
    d1 = {"a": 1, "b": 2}
    d2 = {"a": 1, "c": 3}
    try:
        d1.values() & d2.values()
    except TypeError as e:
        print("d1.values() & d2.values() ->", e)


def demo_isdisjoint() -> None:
    section("3) isdisjoint on dict_keys")
    d = {"a": 1, "b": 2}
    print("keys.isdisjoint({'x'}):", d.keys().isdisjoint({"x"}))
    print("keys.isdisjoint({'a'}):", d.keys().isdisjoint({"a"}))


def demo_no_named_intersection() -> None:
    section("4) dict_keys has no .intersection() (CPython); frozenset does")
    d = {"a": 1, "b": 2}
    k = d.keys()
    print("hasattr(keys, 'intersection'):", hasattr(k, "intersection"))
    fs = frozenset(k)
    print("frozenset(keys).intersection(['a', 'z']):", fs.intersection(["a", "z"]))


def demo_reversed_keys_vs_frozenset() -> None:
    section("5) reversed(keys) vs reversed(frozenset)")
    d = {"a": 1, "b": 2, "c": 3}
    print("list(reversed(d.keys())):", list(reversed(d.keys())))
    fs = frozenset(d.keys())
    try:
        reversed(fs)
    except TypeError as e:
        print("reversed(frozenset(keys)) ->", e)


def main() -> None:
    demo_keys_items_ops()
    demo_values_rejected()
    demo_isdisjoint()
    demo_no_named_intersection()
    demo_reversed_keys_vs_frozenset()


if __name__ == "__main__":
    main()
