"""
Demo for 04-typing-NamedTuple详解.md

Run:
  python part-1-data-structures/chapter-05/typed_namedtuple_demo.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import NamedTuple, get_type_hints


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_namedtuple_typed() -> None:
    section("1) typing.NamedTuple: annotations + defaults + tuple behavior")

    class Coordinate(NamedTuple):
        lat: float
        lon: float
        reference: str = "WGS84"

        def __str__(self) -> str:
            # ASCII-safe output for Windows consoles.
            ns = "N" if self.lat >= 0 else "S"
            we = "E" if self.lon >= 0 else "W"
            return f"{abs(self.lat):.2f} deg {ns}, {abs(self.lon):.2f} deg {we} ({self.reference})"

    c1 = Coordinate(55.75, 37.62)
    c2 = Coordinate(55.75, 37.62, "GCJ-02")

    print("c1 repr:", c1)
    print("c1 str :", str(c1))
    print("c1[0], c1[1]:", c1[0], c1[1])
    print("issubclass(Coordinate, tuple):", issubclass(Coordinate, tuple))

    print("Coordinate.__annotations__:", Coordinate.__annotations__)
    print("get_type_hints(Coordinate):", get_type_hints(Coordinate))

    print("_fields:", Coordinate._fields)
    print("_asdict:", c1._asdict())
    print("_replace:", c1._replace(reference="BD-09"))

    try:
        c1.lat = 0.0  # type: ignore[misc]
    except Exception as e:
        print("immutable ->", type(e).__name__ + ":", e)

    # runtime does not enforce annotations
    weird = Coordinate("not-float", 0)  # type: ignore[arg-type]
    print("runtime accepts wrong types (repr):", repr(weird))
    try:
        print("runtime accepts wrong types (str):", str(weird))
    except Exception as e:
        print("but your methods may break at runtime:", type(e).__name__ + ":", e)

    # silence unused variable warning
    _ = c2


def demo_dataclass_contrast() -> None:
    section("2) Contrast: @dataclass mutable vs frozen + replace/asdict")

    @dataclass
    class CoordinateDC:
        lat: float
        lon: float
        reference: str = "WGS84"

    @dataclass(frozen=True)
    class CoordinateFrozen:
        lat: float
        lon: float
        reference: str = "WGS84"

    a = CoordinateDC(55.75, 37.62)
    a.lat = 0.0  # mutable by default
    print("mutable dataclass:", a)

    b = CoordinateFrozen(55.75, 37.62)
    print("frozen dataclass :", b)
    try:
        b.lat = 0.0  # type: ignore[misc]
    except Exception as e:
        print("frozen ->", type(e).__name__ + ":", e)

    print("asdict(b):", asdict(b))
    print("replace(b, reference='BD-09'):", replace(b, reference="BD-09"))


def main() -> None:
    demo_namedtuple_typed()
    demo_dataclass_contrast()


if __name__ == "__main__":
    main()

