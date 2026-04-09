"""Chapter 16.4: Vector.__add__ / __radd__ with zip_longest and NotImplemented."""

from __future__ import annotations

import itertools
from collections.abc import Iterable, Iterator


class Vector:
    """N-dimensional vector: component-wise + with 0.0 padding for shorter side."""

    def __init__(self, components: Iterable[float]) -> None:
        self._components = [float(x) for x in components]

    def __iter__(self) -> Iterator[float]:
        return iter(self._components)

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


if __name__ == "__main__":
    main()
