from __future__ import annotations

from array import array
from collections.abc import Iterable
import math
import reprlib
from typing import overload


class Vector:
    """Vector v3: v2 + dynamic attributes + stricter immutability."""

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


def main() -> None:
    v2 = Vector([10, 20])
    v4 = Vector([1, 2, 3, 4])

    print("dynamic attribute access")
    print("v2 ->", v2)
    print("v2.x, v2.y ->", v2.x, v2.y)
    try:
        print("v2.z ->", v2.z)
    except AttributeError as e:
        print("v2.z ->", e)

    print("\n__match_args__ mapping")
    print("Vector.__match_args__ ->", Vector.__match_args__)
    print("v4.x, v4.y, v4.z, v4.t ->", v4.x, v4.y, v4.z, v4.t)

    print("\nassignment is blocked (immutability)")
    try:
        v4.x = 999  # type: ignore[misc]
    except AttributeError as e:
        print("v4.x = 999 ->", e)

    try:
        v4.a = 1  # type: ignore[misc]
    except AttributeError as e:
        print("v4.a = 1 ->", e)

    try:
        v4.new_attr = 123  # type: ignore[misc]
    except AttributeError as e:
        print("v4.new_attr = 123 ->", e)

    try:
        v4._components = array("d", [0, 0, 0, 0])
    except AttributeError as e:
        print("rebind _components ->", e)


if __name__ == "__main__":
    main()

