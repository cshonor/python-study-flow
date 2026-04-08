from __future__ import annotations

from array import array
from collections.abc import Iterable
import math
import reprlib
from typing import overload


class Vector:
    """Vector v2: v1 + sequence protocol + slicing.

    Features:
    - composition: store components in array('d')
    - readable repr (reprlib truncation)
    - __bytes__/frombytes round-trip
    - eq/abs/bool semantics (generalized from Vector2d)
    - __len__/__getitem__ for sequence behavior
      - index -> float
      - slice -> Vector (same type)
    """

    typecode = "d"

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Iterable):
            return NotImplemented
        try:
            return tuple(self) == tuple(other)
        except TypeError:
            return NotImplemented

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


def main() -> None:
    v = Vector([3, 4, 5, 6])

    print("sequence protocol")
    print("v ->", v)
    print("len(v) ->", len(v))
    print("v[0], v[-1] ->", v[0], v[-1])
    print("v[1:3] ->", v[1:3], "| type ->", type(v[1:3]).__name__)
    print("v[::-1] ->", v[::-1])

    print("\nslice.indices best-practice demo")
    s = slice(-3, None)
    print("slice(-3, None).indices(len(v)) ->", s.indices(len(v)))

    print("\nbytes/frombytes still works on slices")
    vs = v[1:3]
    print("vs ->", vs)
    print("Vector.frombytes(bytes(vs)) == vs ->", Vector.frombytes(bytes(vs)) == vs)

    print("\nflat sequence: no multi-dimensional indexing")
    try:
        _ = v[1, 2]  # type: ignore[index]
    except TypeError as e:
        print("v[1, 2] ->", e)


if __name__ == "__main__":
    main()

