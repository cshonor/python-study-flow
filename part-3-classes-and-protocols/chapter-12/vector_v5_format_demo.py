from __future__ import annotations

from array import array
from collections.abc import Iterable
import functools
import itertools
import math
import operator
import reprlib
from itertools import zip_longest
from typing import overload


class Vector:
    """Vector v5: v4 + __format__ with hyperspherical ('h') coordinates."""

    typecode = "d"
    __match_args__ = ("x", "y", "z", "t")
    __slots__ = ("_components",)

    def __init__(self, components: Iterable[float]) -> None:
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self) -> str:
        components = reprlib.repr(self._components)
        components = components[components.find("[") : -1]
        return f"Vector({components})"

    def __str__(self) -> str:
        return str(tuple(self))

    def __bytes__(self) -> bytes:
        return bytes([ord(self.typecode)]) + bytes(self._components)

    @classmethod
    def frombytes(cls, octets: bytes) -> "Vector":
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __abs__(self) -> float:
        return math.hypot(*self)

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __len__(self) -> int:
        return len(self._components)

    @overload
    def __getitem__(self, index: int) -> float: ...

    @overload
    def __getitem__(self, index: slice) -> "Vector": ...

    def __getitem__(self, index: int | slice) -> float | "Vector":
        if isinstance(index, slice):
            return Vector(self._components[index])
        return float(self._components[index])

    def __getattr__(self, name: str) -> float:
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1

        if 0 <= pos < len(self._components):
            return float(self._components[pos])

        msg = f"{cls.__name__!r} object has no attribute {name!r}"
        raise AttributeError(msg)

    def __setattr__(self, name: str, value: object) -> None:
        cls = type(self)

        if name == "_components":
            if hasattr(self, "_components"):
                raise AttributeError(f"can't set attribute {name!r}")
            super().__setattr__(name, value)
            return

        if name in cls.__match_args__:
            raise AttributeError(f"readonly attribute {name!r}")

        if name.islower() and len(name) == 1:
            raise AttributeError(
                f"can't set attributes 'a' to 'z' in {cls.__name__!r}"
            )

        raise AttributeError(f"can't set attribute {name!r}")

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if isinstance(other, Vector):
            return self._components == other._components
        if not isinstance(other, Iterable):
            return NotImplemented

        try:
            if len(self) != len(other):  # type: ignore[arg-type]
                return False
        except TypeError:
            pass

        sentinel = object()
        return all(a == b for a, b in zip_longest(self, other, fillvalue=sentinel))

    def __hash__(self) -> int:
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    # --- v5: formatting and hyperspherical coordinates ---
    def angle(self, n: int) -> float:
        r = math.hypot(*self[n:])
        return math.atan2(r, self[n - 1])

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec: str = "") -> str:
        if fmt_spec.endswith("h"):
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = "<{}>"
        else:
            coords = self
            outer_fmt = "({})"

        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(", ".join(components))


def main() -> None:
    print("cartesian (default)")
    v = Vector([3, 4, 5])
    print("format(v) ->", format(v))
    print("format(v, '.2f') ->", format(v, ".2f"))
    print("format(v, '.3e') ->", format(v, ".3e"))

    print("\nhyperspherical ('h' suffix)")
    print("format(Vector([1, 1]), 'h') ->", format(Vector([1, 1]), "h"))
    print("format(Vector([0, 0, 1]), 'h') ->", format(Vector([0, 0, 1]), "h"))
    print(
        "format(Vector([1, 1, 1, 1]), '.3eh') ->",
        format(Vector([1, 1, 1, 1]), ".3eh"),
    )


if __name__ == "__main__":
    main()

