"""
Demo for 02-repr-str-bytes-format-vector2d.md.

Implements a minimal Vector2d that supports:
- repr() / str() (must return str in Python 3)
- bytes() (must return bytes)
- format() (custom format spec, including polar mode via trailing 'p')
"""

from __future__ import annotations

import math
from array import array


class Vector2d:
    typecode = "d"
    __match_args__ = ("x", "y")
    __slots__ = ("__x", "__y")

    def __init__(self, x: float, y: float) -> None:
        object.__setattr__(self, "_Vector2d__x", float(x))
        object.__setattr__(self, "_Vector2d__y", float(y))

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def __setattr__(self, name: str, value: object) -> None:
        # Make instances effectively immutable after initialization.
        if name in ("_Vector2d__x", "_Vector2d__y", "__x", "__y"):
            raise AttributeError(f"{type(self).__name__} is immutable")
        raise AttributeError(f"cannot set attribute {name!r}")

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({self.x!r}, {self.y!r})"

    def __str__(self) -> str:
        return str(tuple(self))

    def __bytes__(self) -> bytes:
        # One-byte typecode + binary array payload of two floats.
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    @classmethod
    def frombytes(cls, octets: bytes) -> "Vector2d":
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

    @classmethod
    def from_polar(cls, r: float, theta: float) -> "Vector2d":
        return cls(r * math.cos(theta), r * math.sin(theta))

    def __format__(self, fmt_spec: str) -> str:
        # If fmt_spec ends with 'p', format in polar coordinates.
        polar = False
        if fmt_spec.endswith("p"):
            polar = True
            fmt_spec = fmt_spec[:-1]
        if polar:
            r = abs(self)
            theta = math.atan2(self.y, self.x)
            coords = (r, theta)
            outer = "<{}, {}>"
        else:
            coords = tuple(self)
            outer = "({}, {})"
        components = (format(c, fmt_spec) for c in coords)
        return outer.format(*components)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector2d):
            return (self.x, self.y) == (other.x, other.y)
        try:
            ox, oy = other  # type: ignore[misc]
        except Exception:
            return NotImplemented
        return (self.x, self.y) == (float(ox), float(oy))

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __complex__(self) -> complex:
        return complex(self.x, self.y)


def main() -> None:
    v = Vector2d(3, 4)
    print("repr(v) ->", repr(v))
    print("str(v) ->", str(v))
    print("bytes(v) ->", bytes(v))
    print("format(v) ->", format(v))
    print("format(v, '.2f') ->", format(v, ".2f"))
    print("format(v, '.2fp') ->", format(v, ".2fp"))
    v2 = Vector2d.frombytes(bytes(v))
    print("Vector2d.frombytes(bytes(v)) ->", v2, "equal:", v2 == v)
    vp = Vector2d.from_polar(2, math.pi / 2)
    print("Vector2d.from_polar(2, pi/2) ->", vp)
    print("hash(v) ->", hash(v))
    print("complex(v) ->", complex(v))


if __name__ == "__main__":
    main()

