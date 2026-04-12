"""
Demo for 06-dataclass详解.md

Run from repo root:
  python part-1-data-structures/chapter-05/dataclass_deep_dive_demo.py
"""

from __future__ import annotations

from dataclasses import InitVar, dataclass, field, fields
from datetime import date
from enum import Enum, auto
from typing import ClassVar, Optional


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def show_field_names(cls: type) -> None:
    print(cls.__name__ + ".fields:", [f.name for f in fields(cls)])


def demo_mutable_default_rejected() -> None:
    section("1) Mutable default is rejected (dataclass protects you)")
    try:
        # Defining inside the function so we can catch the error at runtime.
        @dataclass
        class BadMember:
            name: str
            guests: list[str] = []  # mutable default -> ValueError

        _ = BadMember("nobody")  # pragma: no cover
    except Exception as e:
        print("defining BadMember ->", type(e).__name__ + ":", e)


def demo_default_factory_and_repr_hiding() -> None:
    section("2) field(default_factory=...) and repr=False")

    @dataclass
    class ClubMember:
        name: str
        guests: list[str] = field(default_factory=list)

    @dataclass
    class User:
        name: str
        password: str = field(repr=False)
        is_admin: bool = field(default=False, repr=False)

    a = ClubMember("Alice")
    b = ClubMember("Bob")
    a.guests.append("Eve")
    print("a.guests:", a.guests)
    print("b.guests (independent):", b.guests)

    u = User("tom", password="secret", is_admin=True)
    print("repr(User):", repr(u))


def demo_frozen_and_hash_behavior() -> None:
    section("3) frozen=True: blocks field assignment (not deep immutability)")

    @dataclass(frozen=True)
    class FrozenPoint:
        x: int
        y: int

    p = FrozenPoint(1, 2)
    print("p:", p)
    print("hash(p):", hash(p))
    try:
        p.x = 9  # type: ignore[misc]
    except Exception as e:
        print("p.x = 9 ->", type(e).__name__ + ":", e)


def demo_ordering() -> None:
    section("4) order=True: dataclass generates rich comparisons")

    @dataclass(order=True)
    class Score:
        points: int
        name: str = field(compare=False)  # ignore name for ordering/equality if you want

    s1 = Score(10, "Alice")
    s2 = Score(7, "Bob")
    s3 = Score(10, "Carol")
    print("s1:", s1)
    print("s2:", s2)
    print("s3:", s3)
    print("s2 < s1:", s2 < s1)
    print("s1 == s3 (name ignored):", s1 == s3)
    print("sorted:", sorted([s1, s2, s3]))


def demo_post_init_and_classvar() -> None:
    section("5) __post_init__ + ClassVar for class-level registry")

    @dataclass
    class ClubMember:
        name: str
        guests: list[str] = field(default_factory=list)
        handle: str = ""

    @dataclass
    class HackerClubMember(ClubMember):
        all_handles: ClassVar[set[str]] = set()

        def __post_init__(self) -> None:
            if self.handle == "":
                self.handle = self.name.split()[0]
            cls = self.__class__
            if self.handle in cls.all_handles:
                raise ValueError(f"handle {self.handle!r} already exists")
            cls.all_handles.add(self.handle)

    show_field_names(HackerClubMember)
    a = HackerClubMember("Alice Cooper")
    b = HackerClubMember("Bob", handle="bob42")
    print("a.handle:", a.handle)
    print("b.handle:", b.handle)
    print("HackerClubMember.all_handles:", sorted(HackerClubMember.all_handles))
    try:
        _ = HackerClubMember("Alice Smith")  # would get handle "Alice" again
    except Exception as e:
        print("duplicate handle ->", type(e).__name__ + ":", e)


class Database:
    def lookup(self, key: str) -> str:
        return "value_" + key


def demo_initvar() -> None:
    section("6) InitVar: init-only parameter passed to __post_init__")

    @dataclass
    class C:
        i: int
        j: Optional[str] = None
        database: InitVar[Optional[Database]] = None

        def __post_init__(self, database: Optional[Database]) -> None:
            if self.j is None and database is not None:
                self.j = database.lookup(str(self.i))

    db = Database()
    c1 = C(10, database=db)
    c2 = C(11, j="manual", database=db)
    print("c1:", c1)
    print("c2:", c2)
    # Important subtlety:
    # - `InitVar` is NOT stored on the instance as a field.
    # - But `hasattr(c1, "database")` may still be True because the class
    #   has an attribute named "database" (instance attribute lookup falls back
    #   to class attributes). So we check instance storage instead.
    print("'database' in vars(c1):", "database" in vars(c1))
    print("vars(c1):", vars(c1))
    print("type(C.database):", type(C.database).__name__)


class ResourceType(Enum):
    BOOK = auto()
    EBOOK = auto()
    VIDEO = auto()


def demo_resource_dublin_core() -> None:
    section("7) Resource case study (Dublin Core-like) + custom multi-line repr")

    @dataclass
    class Resource:
        identifier: str
        title: str = "<untitled>"
        creators: list[str] = field(default_factory=list)
        date: Optional[date] = None
        type: ResourceType = ResourceType.BOOK
        description: str = ""
        language: str = ""
        subjects: list[str] = field(default_factory=list)

        def __repr__(self) -> str:
            indent = " " * 4
            parts: list[str] = [f"{self.__class__.__name__}("]
            for f in fields(self.__class__):
                parts.append(f"{indent}{f.name} = {getattr(self, f.name)!r},")
            parts.append(")")
            return "\n".join(parts)

    r = Resource(
        identifier="isbn:978-1491946008",
        title="Fluent Python",
        creators=["Luciano Ramalho"],
        type=ResourceType.BOOK,
        language="en",
        subjects=["python", "programming"],
    )
    print(r)


def main() -> None:
    demo_mutable_default_rejected()
    demo_default_factory_and_repr_hiding()
    demo_frozen_and_hash_behavior()
    demo_ordering()
    demo_post_init_and_classvar()
    demo_initvar()
    demo_resource_dublin_core()


if __name__ == "__main__":
    main()

