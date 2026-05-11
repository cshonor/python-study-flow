"""
Minimal runnable example for 01-11.x 特殊方法速查表（Fluent Python ch.11 cheat sheet).

Run from repo root:
  python part-3-classes-and-protocols/chapter-11/01_special_methods_minimal_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


class MiniVector:
    """Tiny type mapping rows in 01-11.x tables (not full book Vector2d)."""

    __slots__ = ("_x", "_y")

    def __init__(self, x: float, y: float) -> None:
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __iter__(self):
        yield self.x
        yield self.y

    def __repr__(self) -> str:
        return f"MiniVector({self.x!r}, {self.y!r})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __bytes__(self) -> bytes:
        return f"{self.x},{self.y}".encode("utf-8")

    def __format__(self, fmt: str) -> str:
        return f"({format(self.x, fmt)}, {format(self.y, fmt)})"

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def __bool__(self) -> bool:
        return bool(self.x or self.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MiniVector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


def main() -> None:
    section("01 cheat sheet: repr / str / bytes (sec I)")
    v = MiniVector(3, 4)
    print("repr(v) :", repr(v))
    print("str(v)  :", str(v))
    print("bytes(v):", bytes(v))

    section("iter + abs + bool (sec II-III)")
    print("tuple(v):", tuple(v))
    print("abs(v)  :", abs(v))
    print("bool(v) :", bool(v), "| bool(zero):", bool(MiniVector(0, 0)))

    section("eq + hash (sec IV)")
    w = MiniVector(3, 4)
    print("v == w  :", v == w)
    s = {MiniVector(1, 2), MiniVector(1, 2), v}
    print("set size (dedup):", len(s), s)

    section("__format__ (sec V)")
    print("format(v, '.3g'):", format(v, ".3g"))
    print("f-string        :", f"{v:.2f}")

    section("__slots__ (sec VII)")
    print("__slots__       :", MiniVector.__slots__)


if __name__ == "__main__":
    main()
