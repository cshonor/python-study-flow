"""
Demo for 01-type-hints-in-functions-overview.md

Run from repo root:
  python part-2-functions-as-objects/chapter-08/type_hints_mypy_demo.py

Optional (if mypy installed):
  mypy part-2-functions-as-objects/chapter-08/type_hints_mypy_demo.py
"""

from __future__ import annotations

from typing import Callable


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def greet(name: str) -> str:
    return "Hello, " + name


def apply_twice(f: Callable[[int], int], x: int) -> int:
    return f(f(x))


def plus_one(x: int) -> int:
    return x + 1


def main() -> None:
    section("Runtime: type hints do not enforce types")
    print("greet('Bob'):", greet("Bob"))

    # Runtime accepts wrong types unless code breaks.
    # A static checker would flag these:
    #   greet(123)  # error: Argument 1 has incompatible type "int"; expected "str"
    try:
        print("greet(123) at runtime:", greet(123))  # type: ignore[arg-type]
    except TypeError as e:
        print("greet(123) raised:", type(e).__name__, "-", str(e))

    section("Callable typing: apply_twice expects (int)->int")
    print("apply_twice(plus_one, 10):", apply_twice(plus_one, 10))

    # Static checkers should reject this: (str)->str is not compatible with (int)->int
    try:
        print(
            "apply_twice(greet, 10) at runtime:",
            apply_twice(greet, 10),  # type: ignore[arg-type]
        )
    except Exception as e:
        print("apply_twice(greet, 10) raised:", type(e).__name__, "-", str(e))


if __name__ == "__main__":
    main()

