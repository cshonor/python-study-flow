from __future__ import annotations

from array import array
from collections.abc import Iterable
import math
from typing import overload


class Vector:
    """N-dimensional immutable vector with basic sequence protocol.

    This is intentionally minimal for Chapter 12.2:
    - __len__
    - __getitem__ (index + slicing -> Vector)
    """

    typecode = "d"

    def __init__(self, components: Iterable[float]) -> None:
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self) -> str:
        comps = repr(list(self._components))
        comps = comps[1:-1]  # strip [ ]
        return f"Vector({comps})"

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

    def __setattr__(self, name: str, value: object) -> None:
        if hasattr(self, "_components"):
            raise AttributeError(f"{type(self).__name__} instances are immutable")
        super().__setattr__(name, value)


def main() -> None:
    v = Vector([3, 4, 5, 6])

    print("v ->", v)
    print("len(v) ->", len(v))

    print("\nindexing")
    print("v[0] ->", v[0])
    print("v[-1] ->", v[-1])

    print("\nslicing")
    print("v[1:3] ->", v[1:3])
    print("type(v[1:3]) ->", type(v[1:3]).__name__)
    print("v[::-1] ->", v[::-1])

    print("\niteration/unpacking (sequence behavior)")
    a, b, c, d = v
    print("a, b, c, d ->", a, b, c, d)
    print("list(v) ->", list(v))

    print("\nimmutability check")
    try:
        v._components = array("d", [1, 2, 3, 4])
    except AttributeError as e:
        print("rebind attribute ->", e)

    print("\ncosine similarity (works thanks to sequence protocol)")
    a = Vector([1, 0, 1])
    b = Vector([1, 1, 0])

    def cosine_similarity(u: Vector, w: Vector) -> float:
        dot = sum(x * y for x, y in zip(u, w, strict=True))
        nu = math.sqrt(sum(x * x for x in u))
        nw = math.sqrt(sum(y * y for y in w))
        return dot / (nu * nw)

    print("a ->", a)
    print("b ->", b)
    print("cos(a, b) ->", f"{cosine_similarity(a, b):.6f}")


if __name__ == "__main__":
    main()

