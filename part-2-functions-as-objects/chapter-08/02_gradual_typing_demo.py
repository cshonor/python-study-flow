"""
Demo for 02-8.2 渐进式类型系统（Gradual Typing）：Python 类型提示的设计哲学与落地方式.md (Fluent Python 8.2)

Run from repo root:
  python part-2-functions-as-objects/chapter-08/02_gradual_typing_demo.py

Optional (if mypy installed):
  mypy part-2-functions-as-objects/chapter-08/02_gradual_typing_demo.py
"""

from __future__ import annotations

from typing import Any, Callable


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# Example: untyped function. Static checkers often treat the parameters/return
# as Any unless configured more strictly.
def untyped_add(a, b):
    return a + b


def typed_add(a: int, b: int) -> int:
    return a + b


def takes_callable(f: Callable[[int], int], x: int) -> int:
    return f(x)


def main() -> None:
    section("Optional + runtime behavior (type hints are not enforced)")
    print("untyped_add(1, 2):", untyped_add(1, 2))
    print("typed_add(1, 2):", typed_add(1, 2))

    # Runtime may accept mismatched types until an operation fails.
    try:
        print("typed_add('1', 2) at runtime:", typed_add("1", 2))  # type: ignore[arg-type]
    except TypeError as e:
        print("typed_add('1', 2) raised:", type(e).__name__, "-", str(e))

    section("Any as an escape hatch (static), still dynamic at runtime")
    x: Any = "not an int"
    # Static checker: Any lets this pass (may hide mistakes).
    # Runtime: this will fail because + expects compatible operands.
    try:
        print("typed_add(x, 1) where x: Any is str:", typed_add(x, 1))  # type: ignore[arg-type]
    except TypeError as e:
        print("typed_add(x, 1) raised:", type(e).__name__, "-", str(e))

    section("Gradual: tighten boundaries first")
    print("takes_callable(typed_add, 10):", takes_callable(lambda n: typed_add(n, 1), 10))
    # Static checker should reject passing greet-like callables here.
    # (Runtime may fail or behave oddly depending on operations inside.)
    print("takes_callable(lambda n: n + 1, 10):", takes_callable(lambda n: n + 1, 10))


if __name__ == "__main__":
    main()

