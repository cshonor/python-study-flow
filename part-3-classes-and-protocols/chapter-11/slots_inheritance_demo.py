"""
Demo for 08-slots-memory-optimization.md.

Shows:
- instances with __slots__ usually have no __dict__
- subclasses without __slots__ regain __dict__
- how to extend slots in subclasses
- weakref support via __weakref__
"""

from __future__ import annotations

import weakref


class Pixel:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class OpenPixel(Pixel):
    # no __slots__: instances usually have __dict__
    pass


class ColorPixel(Pixel):
    __slots__ = ("color",)

    def __init__(self, x: int, y: int, color: str) -> None:
        super().__init__(x, y)
        self.color = color


class WeakPixel:
    __slots__ = ("x", "__weakref__")

    def __init__(self, x: int) -> None:
        self.x = x


def has_dict(obj: object) -> bool:
    return hasattr(obj, "__dict__")


def main() -> None:
    p = Pixel(1, 2)
    op = OpenPixel(1, 2)
    cp = ColorPixel(1, 2, "red")

    print("Pixel has __dict__ ->", has_dict(p))
    print("OpenPixel has __dict__ ->", has_dict(op))
    print("ColorPixel has __dict__ ->", has_dict(cp))

    print("\n-- dynamic attribute test --")
    try:
        p.z = 3  # type: ignore[attr-defined]
    except Exception as e:
        print("Pixel p.z ->", type(e).__name__ + ":", e)
    op.z = 3
    print("OpenPixel op.z -> ok, op.__dict__ ->", op.__dict__)
    try:
        cp.flavor = "vanilla"  # type: ignore[attr-defined]
    except Exception as e:
        print("ColorPixel cp.flavor ->", type(e).__name__ + ":", e)

    print("\n-- weakref test --")
    try:
        weakref.ref(p)
        print("weakref(Pixel) -> ok")
    except Exception as e:
        print("weakref(Pixel) ->", type(e).__name__ + ":", e)
    wp = WeakPixel(10)
    print("weakref(WeakPixel) ->", weakref.ref(wp))


if __name__ == "__main__":
    main()

