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

    # += behaves differently on list vs tuple
    l1[1] += [33, 22]
    print("after l1[1] += [33, 22] (in-place list extend)")
    print("l1 :", l1)
    print("l2a:", l2a)

    l1[2] += (10, 11)
    print("after l1[2] += (10, 11) (new tuple + rebinding)")
    print("l1 :", l1)
    print("l2a:", l2a)

    # show the three shallow copies behave the same w.r.t. shared inner objects
    print("l2b inner list shared:", l1[1] is l2b[1])
    print("l2c inner list shared:", l1[1] is l2c[1])


class Bus:
    def __init__(self, passengers: list[str] | None = None) -> None:
        # Important: we always build a NEW list, even if an iterable is passed in.
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

    # Cycle example: a list that contains itself (via another list)
    a = [10, 20]
    b = [a, a]
    a.append(b)  # cycle-ish structure: a -> b -> a
    c = copy.deepcopy(a)
    print("cycle deepcopy ok:", c[0:2], "| len(c):", len(c))
    print("c[2][0] is c:", c[2][0] is c)  # structure preserved in copy


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


def f_iadd(a: object, b: object) -> object:
    # same structure as the book's `f(a, b): a += b`
    a += b  # type: ignore[operator]
    return a


def demo_call_by_sharing_iadd() -> None:
    section("16) Call by sharing: `+=` differs for int/list/tuple")

    x = 1
    y = 2
    r1 = f_iadd(x, y)
    print("int -> f_iadd(x,y):", r1, "| x,y:", x, y)

    a = [1, 2]
    b = [3, 4]
    r2 = f_iadd(a, b)
    print("list -> f_iadd(a,b):", r2, "| a,b:", a, b)

    t = (10, 20)
    u = (30, 40)
    r3 = f_iadd(t, u)
    print("tuple -> f_iadd(t,u):", r3, "| t,u:", t, u)


class HauntedBus:
    def __init__(self, passengers: list[str] = []) -> None:
        self.passengers = passengers

    def pick(self, name: str) -> None:
        self.passengers.append(name)

    def drop(self, name: str) -> None:
        self.passengers.remove(name)

    def __repr__(self) -> str:
        return f"HauntedBus(passengers={self.passengers!r})"


class TwilightBus:
    def __init__(self, passengers: list[str] | None = None) -> None:
        if passengers is None:
            self.passengers = []
        else:
            # defensive copy: bus mutates its own list, not the caller's
            self.passengers = list(passengers)

    def pick(self, name: str) -> None:
        self.passengers.append(name)

    def drop(self, name: str) -> None:
        self.passengers.remove(name)

    def __repr__(self) -> str:
        return f"TwilightBus(passengers={self.passengers!r})"


def demo_hauntedbus_mutable_default_and_defaults_evidence() -> None:
    section("17) Mutable default argument pitfall: HauntedBus")

    bus1 = HauntedBus(["Alice", "Bill"])
    bus1.pick("Charlie")
    bus1.drop("Alice")
    print("bus1:", bus1)

    bus2 = HauntedBus()
    bus2.pick("Carrie")
    print("bus2:", bus2)

    bus3 = HauntedBus()
    bus3.pick("Dave")
    print("bus3:", bus3)

    print("bus2.passengers is bus3.passengers:", bus2.passengers is bus3.passengers)
    print("HauntedBus.__init__.__defaults__:", HauntedBus.__init__.__defaults__)
    if HauntedBus.__init__.__defaults__:
        shared_default = HauntedBus.__init__.__defaults__[0]
        print("__defaults__[0] is bus2.passengers:", shared_default is bus2.passengers)


def demo_twilightbus_defensive_copy() -> None:
    section("18) Defensive copy: TwilightBus does not mutate the caller")

    basketball_team = ["Sue", "Tina", "Maya", "Diana", "Pat"]
    bus = TwilightBus(basketball_team)
    bus.drop("Tina")
    bus.drop("Pat")
    print("bus.passengers:", [safe(x) for x in bus.passengers])
    print("basketball_team (unchanged):", [safe(x) for x in basketball_team])


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


def f_bad(a: list[int] = []) -> list[int]:
    a.append(1)
    return a


def f_good(a: list[int] | None = None) -> list[int]:
    if a is None:
        a = []
    a.append(1)
    return a


def demo_mutable_default_argument() -> None:
    section("11) Mutable default argument pitfall")
    print("f_bad() #1:", f_bad())
    print("f_bad() #2:", f_bad())
    print("f_bad() #3:", f_bad())
    print("f_good() #1:", f_good())
    print("f_good() #2:", f_good())


def demo_del_and_gc_basics() -> None:
    section("12) del removes a name; GC frees objects when unreachable")

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
    section("13) Weak references: cache entries vanish after GC")

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


def demo_dataclass_default_factory_echo() -> None:
    section("15) Dataclass: mutable defaults must use default_factory")

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
    demo_assignment_right_to_left_gizmo()
    demo_aliasing_identity_vs_equality()
    demo_none_comparison_is_safer()
    demo_tuple_relative_immutability_and_hash()
    demo_is_vs_eq()
    demo_shallow_copy_three_ways_and_trap()
    demo_copy_vs_deepcopy_bus_and_cycles()
    demo_tuple_relative_immutability()
    demo_shallow_vs_deep_copy()
    demo_mutable_default_argument()
    demo_del_and_gc_basics()
    demo_weakref_cache_like()
    demo_small_int_and_string_interning_warning()
    demo_dataclass_default_factory_echo()
    demo_call_by_sharing_iadd()
    demo_hauntedbus_mutable_default_and_defaults_evidence()
    demo_twilightbus_defensive_copy()


if __name__ == "__main__":
    main()

