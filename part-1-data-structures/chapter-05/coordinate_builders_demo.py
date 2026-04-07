"""
Demo for 02-coordinate-overview-and-feature-matrix.md

Run:
  python part-1-data-structures/chapter-05/coordinate_builders_demo.py
"""

from __future__ import annotations

from collections import namedtuple
from dataclasses import asdict, dataclass, fields, make_dataclass, replace
from inspect import get_annotations
from typing import NamedTuple, get_type_hints


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_handwritten() -> None:
    section("1) Handwritten class (baseline)")

    class Coordinate:
        def __init__(self, lat, lon):
            self.lat = lat
            self.lon = lon

    a = Coordinate(55.756, 37.617)
    b = Coordinate(55.756, 37.617)
    print("repr(a):", repr(a))
    print("a == b:", a == b)
    print("a.lat, a.lon:", a.lat, a.lon)


def demo_namedtuple() -> None:
    section("2) collections.namedtuple")
    CoordinateNT = namedtuple("Coordinate", "lat lon")
    moscow = CoordinateNT(55.756, 37.617)
    print("moscow:", moscow)
    print("issubclass(Coordinate, tuple):", issubclass(CoordinateNT, tuple))
    print("eq:", moscow == CoordinateNT(55.756, 37.617))
    print("_fields:", CoordinateNT._fields)
    print("_asdict:", moscow._asdict())
    print("_replace:", moscow._replace(lat=0.0))
    try:
        moscow.lat = 0.0  # type: ignore[misc]
    except AttributeError as e:
        print("immutable -> AttributeError:", e)


def demo_typing_namedtuple() -> None:
    section("3) typing.NamedTuple (with annotations + custom method)")

    class CoordinateT(NamedTuple):
        lat: float
        lon: float

        def __str__(self) -> str:
            ns = "N" if self.lat >= 0 else "S"
            we = "E" if self.lon >= 0 else "W"
            # Keep ASCII-only output for Windows console safety.
            return f"{abs(self.lat):.1f} deg {ns}, {abs(self.lon):.1f} deg {we}"

    moscow = CoordinateT(55.756, 37.617)
    print("moscow repr:", ascii(repr(moscow)))
    print("moscow str :", ascii(str(moscow)))
    print("issubclass(CoordinateT, tuple):", issubclass(CoordinateT, tuple))
    print("type hints:", get_type_hints(CoordinateT))
    print("_asdict:", moscow._asdict())
    print("_replace:", ascii(str(moscow._replace(lon=0.0))))


def demo_dataclass() -> None:
    section("4) @dataclass (frozen=True)")

    @dataclass(frozen=True)
    class CoordinateDC:
        lat: float
        lon: float

        def __str__(self) -> str:
            ns = "N" if self.lat >= 0 else "S"
            we = "E" if self.lon >= 0 else "W"
            # Keep ASCII-only output for Windows console safety.
            return f"{abs(self.lat):.1f} deg {ns}, {abs(self.lon):.1f} deg {we}"

    moscow = CoordinateDC(55.756, 37.617)
    print("moscow repr:", ascii(repr(moscow)))
    print("moscow str :", ascii(str(moscow)))
    print("annotations (raw):", CoordinateDC.__annotations__)
    print("type hints:", get_type_hints(CoordinateDC))
    print("inspect.get_annotations:", get_annotations(CoordinateDC))
    print("fields:", [(f.name, f.type, f.default) for f in fields(CoordinateDC)])
    print("asdict:", asdict(moscow))
    print("replace:", ascii(str(replace(moscow, lat=0.0))))
    try:
        moscow.lat = 0.0  # type: ignore[misc]
    except Exception as e:
        print("frozen ->", type(e).__name__ + ":", e)


def demo_make_dataclass() -> None:
    section("5) make_dataclass (runtime class creation)")
    Dynamic = make_dataclass("DynamicCoord", [("lat", float), ("lon", float)])
    d = Dynamic(1.0, 2.0)
    print("Dynamic instance:", d)
    print("type hints:", get_type_hints(Dynamic))


def main() -> None:
    demo_handwritten()
    demo_namedtuple()
    demo_typing_namedtuple()
    demo_dataclass()
    demo_make_dataclass()


if __name__ == "__main__":
    main()

