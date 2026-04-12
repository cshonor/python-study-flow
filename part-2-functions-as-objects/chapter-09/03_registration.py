"""
03_registration.py

Classic import-time decorator demo from Fluent Python (Chapter 9).

Run as a script:
  python part-2-functions-as-objects/chapter-09/03_registration.py

Or import it from the repo root:
  python -c "import part-2-functions-as-objects.chapter-09.registration"
  (Tip: for interactive use, add repo root to PYTHONPATH.)
"""

from __future__ import annotations

from collections.abc import Callable

registry: list[Callable[[], None]] = []


def register(func: Callable[[], None]) -> Callable[[], None]:
    print(f"running register {func}")
    registry.append(func)
    return func


@register
def f1() -> None:
    print("running f1")


@register
def f2() -> None:
    print("running f2")


def f3() -> None:
    print("running f3")


def main() -> None:
    print("running main()")
    print("registry ->", registry)
    f1()
    f2()
    f3()


if __name__ == "__main__":
    main()

