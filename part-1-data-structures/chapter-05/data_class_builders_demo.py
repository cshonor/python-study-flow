"""
Demo for Chapter 5: data class builders (Fluent Python 2e, ch.5).

Run:
  python part-1-data-structures/chapter-05/data_class_builders_demo.py
"""

from __future__ import annotations

from collections import namedtuple
from dataclasses import dataclass, field
from typing import NamedTuple, TypedDict


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_namedtuple() -> None:
    section("1) collections.namedtuple (tuple subclass, immutable record)")
    Point = namedtuple("Point", "x y")
    p = Point(10, 20)
    print("p:", p)
    print("p.x, p.y:", p.x, p.y)
    print("p[0], p[1]:", p[0], p[1])
    try:
        p.x = 99  # type: ignore[misc]
    except AttributeError as e:
        print("immutable -> AttributeError:", e)


def demo_typing_namedtuple() -> None:
    section("2) typing.NamedTuple (namedtuple + type annotations)")

    class UserNT(NamedTuple):
        id: int
        name: str
        active: bool = True

    u = UserNT(1, "Ada")
    print("u:", u)
    print("u.name:", u.name)
    print("UserNT.__annotations__:", UserNT.__annotations__)


def demo_dataclass() -> None:
    section("3) @dataclass (modern default; methods/defaults/customization)")

    @dataclass
    class User:
        id: int
        name: str
        tags: list[str] = field(default_factory=list)

    @dataclass(frozen=True)
    class FrozenPoint:
        x: int
        y: int

    u = User(1, "Ada")
    u.tags.append("vip")
    print("User:", u)

    fp = FrozenPoint(10, 20)
    print("FrozenPoint:", fp)
    try:
        fp.x = 99  # type: ignore[misc]
    except Exception as e:
        print("frozen ->", type(e).__name__ + ":", e)


def demo_typeddict() -> None:
    section("4) TypedDict (type shape for dict; not a class builder)")

    class UserTD(TypedDict):
        id: int
        name: str
        active: bool

    # Runtime object is still a dict.
    payload: UserTD = {"id": 1, "name": "Ada", "active": True}
    print("payload type:", type(payload))
    print("payload:", payload)
    print("payload['name']:", payload["name"])
    # TypedDict is mainly for static type checkers, not runtime behavior.


def main() -> None:
    demo_namedtuple()
    demo_typing_namedtuple()
    demo_dataclass()
    demo_typeddict()


if __name__ == "__main__":
    main()

