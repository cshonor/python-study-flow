"""Ch. 16.4–16.6: Vector + (add), * (scalar), @ (dot) with reverse methods."""

from __future__ import annotations

import itertools
from collections import abc
from collections.abc import Iterable, Iterator
from fractions import Fraction


class Vector:
    """N-dimensional vector: + with padding, * scalar, @ dot product."""

    def __init__(self, components: Iterable[float]) -> None:
        self._components = [float(x) for x in components]

    def __iter__(self) -> Iterator[float]:
        return iter(self._components)

    def __len__(self) -> int:
        return len(self._components)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self._components == other._components

    def __repr__(self) -> str:
        return f"Vector({self._components!r})"

    def __add__(self, other: Iterable[float]) -> Vector:
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    __radd__ = __add__

    def __mul__(self, scalar: object) -> Vector:
        try:
            factor = float(scalar)  # int, bool, Fraction, etc.
        except (TypeError, ValueError):
            return NotImplemented
        return Vector(n * factor for n in self)

    __rmul__ = __mul__

    def __matmul__(self, other: object) -> float:
        if isinstance(other, (str, bytes)) or not isinstance(other, abc.Iterable):
            return NotImplemented
        if isinstance(other, abc.Sized) and len(self) != len(other):
            raise ValueError("@ requires vectors of equal length.")
        try:
            return sum(a * float(b) for a, b in zip(self, other, strict=True))
        except TypeError:
            return NotImplemented
        except ValueError:
            raise ValueError("@ requires vectors of equal length.") from None

    def __rmatmul__(self, other: object) -> float:
        return self @ other


def main() -> None:
    v1 = Vector([3, 4, 5])
    v2 = Vector([6, 7, 8])
    print("v1 + v2 ->", v1 + v2)
    print("v1 + v2 == Vector([9, 11, 13]) ->", v1 + v2 == Vector([9, 11, 13]))

    print("v1 + (10, 20, 30) ->", v1 + (10, 20, 30))
    print("(10, 20, 30) + v1 ->", (10, 20, 30) + v1)

    print("Vector([1, 2]) + Vector([1]) ->", Vector([1, 2]) + Vector([1]))

    try:
        _ = v1 + "ABC"  # noqa: F841
    except TypeError as e:
        print("v1 + 'ABC' -> TypeError:", e)

    print("--- 16.5 scalar *")
    v0 = Vector([1, 2, 3])
    print("v0 * 10 ->", v0 * 10)
    print("11 * v0 ->", 11 * v0)
    print("v0 * True ->", v0 * True)
    print("v0 * Fraction(1, 3) ->", v0 * Fraction(1, 3))

    print("--- 16.6 @ dot")
    va = Vector([1, 2, 3])
    vz = Vector([5, 6, 7])
    print("va @ vz ->", va @ vz)
    print("va @ vz == 38 ->", va @ vz == 38.0)
    print("[10, 20, 30] @ vz ->", [10, 20, 30] @ vz)

    try:
        _ = va @ 3  # noqa: F841
    except TypeError as e:
        print("va @ 3 -> TypeError:", e)


if __name__ == "__main__":
    main()
