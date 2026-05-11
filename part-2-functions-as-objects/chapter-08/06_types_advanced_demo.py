"""
Demo for 06-8.5（续）类型提示进阶：别名、TypeVar、Protocol、Callable、NoReturn.md (Fluent Python 8.5 advanced)

Run from repo root:
  python part-2-functions-as-objects/chapter-08/06_types_advanced_demo.py
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Callable, NoReturn, Protocol, TypeAlias, TypeVar

# --- Type alias ---------------------------------------------------------------
FromTo: TypeAlias = tuple[str, str]


# --- Protocol + bounded TypeVar ----------------------------------------------
class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...


LT = TypeVar("LT", bound=SupportsLessThan)
T = TypeVar("T")


def top(series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]


def apply_func(data: Iterable[T], func: Callable[[T], str]) -> list[str]:
    return [func(item) for item in data]


def fatal_error(msg: str) -> NoReturn:
    raise RuntimeError(msg)


# --- § zero: one-screen cheat sheet (see 06 md "零·八") -----------------------
Point: TypeAlias = tuple[int, int]


def first_item(items: list[T]) -> T:
    return items[0]


class Drawable(Protocol):
    def draw(self) -> None: ...


class MiniCanvas:
    def draw(self) -> None:
        print("  MiniCanvas.draw()")


def paint(obj: Drawable) -> None:
    obj.draw()


def run_noarg(fn: Callable[[], None]) -> None:
    fn()


def cheat_sheet_snippets() -> None:
    print("\n--- cheat_sheet_snippets (md section zero) ---")
    pt: Point = (3, 4)
    print("Point:", pt)
    print("first_item([7, 8, 9]):", first_item([7, 8, 9]))
    paint(MiniCanvas())
    run_noarg(lambda: print("  lambda body"))
    try:
        raise SystemExit("demo exit")
    except SystemExit as e:
        print("SystemExit (not calling real stop()):", e)


def main() -> None:
    # FromTo: type-only; runtime uses plain tuples
    route: FromTo = ("NYC", "LON")
    print("FromTo route:", route)

    print("top([3, 1, 4, 1, 5], 3) ->", top([3, 1, 4, 1, 5], 3))
    print("top('cba', 2) ->", top("cba", 2))

    print("apply_func ->", apply_func([1, 2, 3], lambda n: f"v={n}"))

    try:
        fatal_error("demo")
    except RuntimeError as e:
        print("fatal_error -> RuntimeError:", e)

    cheat_sheet_snippets()


if __name__ == "__main__":
    main()
