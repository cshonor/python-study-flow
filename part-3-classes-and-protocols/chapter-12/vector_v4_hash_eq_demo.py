from __future__ import annotations

from array import array
from collections.abc import Iterable
import functools
import math
import operator
import reprlib
from itertools import zip_longest
from typing import overload


class Vector:
    """Vector v4: v3 + hashability + faster equality for large dimensions."""

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

        # Fast path when other is sized: length mismatch => False immediately.
        try:
            if len(self) != len(other):  # type: ignore[arg-type]
                return False
        except TypeError:
            # other has no len(); fall back to element-wise compare.
            pass

        sentinel = object()
        return all(a == b for a, b in zip_longest(self, other, fillvalue=sentinel))

    def __hash__(self) -> int:
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)


def main() -> None:
    print("hashability")
    a = Vector([1, 2, 3])
    b = Vector([1, 2, 3])
    c = Vector([1, 2, 4])
    s = {a, b, c}
    print("a == b ->", a == b)
    print("hash(a) == hash(b) ->", hash(a) == hash(b))
    print("set size ({a,b,c}) ->", len(s))

    print("\nfast equality behavior")
    big1 = Vector(range(10_000))
    big2 = Vector(list(range(10_000)))
    big3 = Vector([999] + list(range(1, 10_000)))
    print("big1 == big2 ->", big1 == big2)
    print("big1 == big3 ->", big1 == big3)
    print("big1 == list(range(10000)) ->", big1 == list(range(10_000)))
    print("big1 == tuple(range(9999)) ->", big1 == tuple(range(9_999)))


if __name__ == "__main__":
    main()

