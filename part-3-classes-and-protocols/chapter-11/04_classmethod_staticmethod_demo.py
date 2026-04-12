"""
Demo for 04-11.5 classmethod vs staticmethod：到底差在哪（以及什么时候该用）.md (Fluent Python 11.5).

Includes:
- Demo.klassmeth/statmeth argument behavior
- Vector2d.from_polar as classmethod (returns subclass)
- Vector2d.from_polar_static as staticmethod (shows common pitfall)
"""

from __future__ import annotations

import math


class Demo:
    @classmethod
    def klassmeth(*args):
        return args

    @staticmethod
    def statmeth(*args):
        return args


class Vector2d:
    def __init__(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.x!r}, {self.y!r})"

    @classmethod
    def from_polar(cls, r: float, theta: float) -> "Vector2d":
        return cls(r * math.cos(theta), r * math.sin(theta))

    @staticmethod
    def from_polar_static(r: float, theta: float) -> "Vector2d":
        # Common pitfall: hard-codes base class, so subclasses don't get instances.
        return Vector2d(r * math.cos(theta), r * math.sin(theta))


class SubVector2d(Vector2d):
    pass


def main() -> None:
    print("=== Demo ===")
    print("Demo.klassmeth() ->", Demo.klassmeth())
    print("Demo.klassmeth('spam') ->", Demo.klassmeth("spam"))
    print("Demo.statmeth() ->", Demo.statmeth())
    print("Demo.statmeth('spam') ->", Demo.statmeth("spam"))

    print("\n=== classmethod returns subclass ===")
    v = SubVector2d.from_polar(2, math.pi / 2)
    print("SubVector2d.from_polar(...) ->", v, "type:", type(v).__name__)

    print("\n=== staticmethod pitfall ===")
    v2 = SubVector2d.from_polar_static(2, math.pi / 2)
    print("SubVector2d.from_polar_static(...) ->", v2, "type:", type(v2).__name__)


if __name__ == "__main__":
    main()

