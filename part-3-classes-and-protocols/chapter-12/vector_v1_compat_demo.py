from __future__ import annotations

from array import array
import math
import reprlib
from collections.abc import Iterable


class Vector:
    """Vector v1: N-dimensional, Vector2d-compatible core behavior.

    Focus (Fluent Python 2e, ch12.3):
    - composition: store components in array('d')
    - reprlib-based truncation for readable repr
    - bytes/frombytes round-trip
    - eq/abs/bool semantics compatible with Vector2d (generalized to N dims)
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

    @classmethod
    def frombytes(cls, octets: bytes) -> "Vector":
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)


def main() -> None:
    print("basic construction")
    v2 = Vector([3, 4])
    v4 = Vector(range(4))
    print("v2 repr ->", repr(v2))
    print("v2 str  ->", str(v2))
    print("v4 repr ->", repr(v4))
    print("tuple(v4) ->", tuple(v4))

    print("\nrepr truncation (reprlib)")
    v_big = Vector(range(100))
    print("v_big repr ->", repr(v_big))

    print("\nbytes/frombytes round-trip")
    octets = bytes(v4)
    v4b = Vector.frombytes(octets)
    print("bytes(v4) first byte(typecode) ->", chr(octets[0]))
    print("Vector.frombytes(bytes(v4)) == v4 ->", v4b == v4)

    print("\neq / abs / bool semantics")
    print("Vector([3,4]) == [3,4] ->", Vector([3, 4]) == [3, 4])
    print("abs(Vector([3,4])) ->", abs(Vector([3, 4])))
    print("bool(Vector([0,0])) ->", bool(Vector([0, 0])))
    print("bool(Vector([0,1])) ->", bool(Vector([0, 1])))


if __name__ == "__main__":
    main()

