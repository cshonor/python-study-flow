"""
Demo for 01-object-references-mutability-and-gc-overview.md

Run from repo root:
  python part-1-data-structures/chapter-06/object_refs_mutability_gc_demo.py
"""

from __future__ import annotations

import copy
import gc
import sys
import weakref
from dataclasses import dataclass, field


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def safe(obj: object) -> object:
    # Windows consoles may use GBK; ascii() prevents UnicodeEncodeError in demos.
    return ascii(obj) if isinstance(obj, str) else obj


def demo_names_are_labels() -> None:
    section("1) Names are labels: aliasing vs rebinding")
    a = [1, 2, 3]
    b = a
    print("id(a) == id(b):", id(a) == id(b))
    a.append(4)
    print("after a.append(4) -> a:", a, "b:", b)
    a = []  # rebinding a; b still points to old list
    print("after rebinding a = [] -> a:", a, "b:", b)


def demo_is_vs_eq() -> None:
    section("2) is vs == (identity vs equality)")
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
    section("3) Tuple is 'relatively immutable'")
    t = (1, [2, 3])
    print("t before:", t)
    t[1].append(4)
    print("t after t[1].append(4):", t)
    try:
        t[1] = [9]  # type: ignore[misc]
    except Exception as e:
        print("t[1] = ... ->", type(e).__name__ + ":", e)


def demo_shallow_vs_deep_copy() -> None:
    section("4) Shallow copy vs deep copy")
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


def f_bad(a: list[int] = []) -> list[int]:
    a.append(1)
    return a


def f_good(a: list[int] | None = None) -> list[int]:
    if a is None:
        a = []
    a.append(1)
    return a


def demo_mutable_default_argument() -> None:
    section("5) Mutable default argument pitfall")
    print("f_bad() #1:", f_bad())
    print("f_bad() #2:", f_bad())
    print("f_bad() #3:", f_bad())
    print("f_good() #1:", f_good())
    print("f_good() #2:", f_good())


def demo_del_and_gc_basics() -> None:
    section("6) del removes a name; GC frees objects when unreachable")

    class Tracker:
        def __init__(self, label: str) -> None:
            self.label = label

        def __repr__(self) -> str:
            return f"Tracker({safe(self.label)})"

    obj = Tracker("alive")
    w = weakref.ref(obj)
    print("weakref before del:", w())

    # delete the name; if no other strong refs exist, object becomes unreachable
    del obj
    gc.collect()
    print("weakref after del + gc.collect():", w())


def demo_weakref_cache_like() -> None:
    section("7) Weak references: cache entries vanish after GC")

    @dataclass(eq=True, frozen=True)
    class Key:
        name: str

    cache: weakref.WeakKeyDictionary[Key, str] = weakref.WeakKeyDictionary()
    k = Key("k1")
    cache[k] = "payload"
    print("cache has k:", k in cache, "| size:", len(cache))

    w = weakref.ref(k)
    del k
    gc.collect()
    print("key weakref after del+gc:", w())
    print("cache size after key collected:", len(cache))


def demo_small_int_and_string_interning_warning() -> None:
    section("8) CPython caching (don't rely on it): small ints / some strings")
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


def demo_dataclass_default_factory_echo() -> None:
    section("9) Dataclass: mutable defaults must use default_factory")

    @dataclass
    class Member:
        name: str
        guests: list[str] = field(default_factory=list)

    m1 = Member("A")
    m2 = Member("B")
    m1.guests.append("Eve")
    print("m1.guests:", [safe(x) for x in m1.guests])
    print("m2.guests:", [safe(x) for x in m2.guests])


def main() -> None:
    print("Python:", sys.version.split()[0])
    demo_names_are_labels()
    demo_is_vs_eq()
    demo_tuple_relative_immutability()
    demo_shallow_vs_deep_copy()
    demo_mutable_default_argument()
    demo_del_and_gc_basics()
    demo_weakref_cache_like()
    demo_small_int_and_string_interning_warning()
    demo_dataclass_default_factory_echo()


if __name__ == "__main__":
    main()

