"""
Demo for 05-type-hints-primer.md

Run:
  python part-1-data-structures/chapter-05/type_hints_primer_demo.py
"""

from __future__ import annotations

from dataclasses import dataclass
from inspect import get_annotations
from typing import NamedTuple, Optional, get_type_hints


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_plain_class_annotations() -> None:
    section("1) Plain class: annotation is not necessarily an attribute")

    class DemoPlainClass:
        a: int
        b: float = 1.1
        c = "spam"

    print("DemoPlainClass.__annotations__:", DemoPlainClass.__annotations__)
    print("hasattr(DemoPlainClass, 'a'):", hasattr(DemoPlainClass, "a"))
    print("DemoPlainClass.b:", DemoPlainClass.b)
    print("DemoPlainClass.c:", DemoPlainClass.c)
    try:
        print(DemoPlainClass.a)  # type: ignore[attr-defined]
    except AttributeError as e:
        print("DemoPlainClass.a -> AttributeError:", e)


def demo_namedtuple_annotations_runtime() -> None:
    section("2) typing.NamedTuple: annotations become instance fields (but no runtime checks)")

    class Coordinate(NamedTuple):
        lat: float
        lon: float

    ok = Coordinate(1.0, 2.0)
    trash = Coordinate("Ni!", None)  # type: ignore[arg-type]
    print("ok:", ok)
    print("trash (repr):", repr(trash))
    print("Coordinate._fields:", Coordinate._fields)
    print("Coordinate.__annotations__:", Coordinate.__annotations__)
    print("get_type_hints(Coordinate):", get_type_hints(Coordinate))
    print("inspect.get_annotations(Coordinate):", get_annotations(Coordinate))
    # Show that it's immutable
    try:
        ok.lat = 0.0  # type: ignore[misc]
    except Exception as e:
        print("immutable ->", type(e).__name__ + ":", e)


def demo_dataclass_annotations_and_mutability() -> None:
    section("3) @dataclass: annotations become instance fields (mutable by default)")

    @dataclass
    class DemoDataClass:
        a: int
        b: float = 1.1
        c = "spam"

    dc = DemoDataClass(1)
    print("dc:", dc)
    print("DemoDataClass.__annotations__:", DemoDataClass.__annotations__)
    print("get_type_hints(DemoDataClass):", get_type_hints(DemoDataClass))
    print("inspect.get_annotations(DemoDataClass):", get_annotations(DemoDataClass))

    dc.a = 99
    dc.z = "secret stash"  # dynamic attribute is allowed by default
    print("after mutation:", dc, "| dc.z:", getattr(dc, "z"))


def demo_dataclass_slots() -> None:
    section("4) dataclass(slots=True): forbid dynamic attributes")

    @dataclass(slots=True)
    class Slotted:
        a: int
        b: Optional[str] = None

    s = Slotted(1)
    print("s:", s)
    try:
        s.z = "nope"  # type: ignore[attr-defined]
    except Exception as e:
        print("adding new attribute ->", type(e).__name__ + ":", e)


def main() -> None:
    demo_plain_class_annotations()
    demo_namedtuple_annotations_runtime()
    demo_dataclass_annotations_and_mutability()
    demo_dataclass_slots()


if __name__ == "__main__":
    main()

