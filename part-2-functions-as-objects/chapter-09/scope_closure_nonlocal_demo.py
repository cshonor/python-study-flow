"""
LEGB / closure / nonlocal demo for Chapter 9.

Run from repo root:
  python part-2-functions-as-objects/chapter-09/scope_closure_nonlocal_demo.py
"""

from __future__ import annotations


def legb_demo() -> None:
    x = "enclosing x"

    def inner() -> None:
        # Reads from enclosing scope (E in LEGB).
        print("inner reads x ->", x)

    inner()


def unboundlocal_demo() -> None:
    # Classic pitfall: assignment makes the name local.
    y = "global y"

    def broken() -> None:
        try:
            print("broken reads y ->", y)  # UnboundLocalError
            y = "local y"
        except Exception as e:
            print(type(e).__name__ + ":", e)

    def fixed_nonlocal() -> None:
        nonlocal y
        print("fixed_nonlocal y(before) ->", y)
        y = "mutated via nonlocal"
        print("fixed_nonlocal y(after) ->", y)

    broken()
    fixed_nonlocal()
    print("outer y ->", y)


def make_counter():
    count = 0

    def inc() -> int:
        nonlocal count
        count += 1
        return count

    return inc


def main() -> None:
    print("=== LEGB / enclosing variable ===")
    legb_demo()

    print("\n=== UnboundLocalError and nonlocal ===")
    unboundlocal_demo()

    print("\n=== Closure with state (counter) ===")
    c = make_counter()
    print("counter ->", c(), c(), c())


if __name__ == "__main__":
    main()

