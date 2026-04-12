"""
Demo for 05-8.5 注解中可用的类型：从 Any 到泛型容器与抽象基类.md (Fluent Python 8.5)

Run from repo root:
  python part-2-functions-as-objects/chapter-08/05_types_in_annotations_demo.py
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, NamedTuple


# --- 8.5.1 Any: static checkers allow * on Any --------------------------------
def double_any(x: Any) -> Any:
    return x * 2


# --- 8.5.3 Union-style return (str | float) -----------------------------------
def parse_token(token: str) -> str | float:
    try:
        return float(token)
    except ValueError:
        return token


# --- 8.5.4 list[str] ----------------------------------------------------------
def tokenize(text: str) -> list[str]:
    return text.upper().split()


# --- 8.5.5 fixed-length tuple as record ---------------------------------------
GeoCoord = tuple[float, float]


def geohash(lat_lon: GeoCoord) -> str:
    lat, lon = lat_lon
    return f"{lat:.6f},{lon:.6f}"


class Coordinate(NamedTuple):
    lat: float
    lon: float

    def geohash(self) -> str:
        return f"{self.lat:.6f},{self.lon:.6f}"


# --- 8.5.5 homogeneous tuple (variable length) -------------------------------
def first_chunk(items: Sequence[str], size: int) -> tuple[str, ...]:
    return tuple(items[:size])


# --- 8.5.6 / 8.5.7 Mapping as wide parameter type ----------------------------
def name2hex(name: str, color_map: Mapping[str, int]) -> str:
    return f"#{color_map[name]:06x}"


def main() -> None:
    print("double_any(21) ->", double_any(21))
    print("parse_token('3.5') ->", parse_token("3.5"))
    print("parse_token('pi') ->", parse_token("pi"))
    print("tokenize('a b c') ->", tokenize("a b c"))
    print("geohash((48.858, 2.294)) ->", geohash((48.858, 2.294)))
    c = Coordinate(48.858, 2.294)
    print("Coordinate.geohash ->", c.geohash())
    print("first_chunk ->", first_chunk(["a", "b", "c", "d"], 2))
    colors: dict[str, int] = {"red": 0xFF0000, "green": 0x00FF00}
    print("name2hex('red', ...) ->", name2hex("red", colors))


if __name__ == "__main__":
    main()
