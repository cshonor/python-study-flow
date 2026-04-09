from __future__ import annotations

import math
import random
from collections.abc import Iterable
from typing import Generic, Protocol, TypeVar, runtime_checkable


# --- Generic Protocol #1: SupportsAbs[R_co] (output covariant) ---

R_co = TypeVar("R_co", covariant=True)


@runtime_checkable
class SupportsAbs(Protocol[R_co]):
    def __abs__(self) -> R_co: ...


def is_unit(v: SupportsAbs[float]) -> bool:
    return math.isclose(abs(v), 1.0)


class Vector2d:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __repr__(self) -> str:
        return f"Vector2d({self.x}, {self.y})"


# --- Generic Protocol #2: RandomPicker[T_co] (output covariant) ---

T_co = TypeVar("T_co", covariant=True)


@runtime_checkable
class RandomPicker(Protocol[T_co]):
    def pick(self) -> T_co: ...


T = TypeVar("T")


class LottoBlower(Generic[T]):
    def __init__(self, items: Iterable[T]) -> None:
        self._balls = list(items)

    def load(self, items: Iterable[T]) -> None:
        self._balls.extend(items)

    def pick(self) -> T:
        if not self._balls:
            raise LookupError("pick from empty LottoBlower")
        pos = random.randrange(len(self._balls))
        return self._balls.pop(pos)


def pick_two(picker: RandomPicker[T]) -> tuple[T, T]:
    return (picker.pick(), picker.pick())


def main() -> None:
    print("SupportsAbs[R_co] demo")
    v = Vector2d(0.0, 1.0)
    print("v ->", v, "| abs ->", abs(v), "| is_unit ->", is_unit(v))
    print("is_unit(1) ->", is_unit(1))
    print("isinstance(v, SupportsAbs) ->", isinstance(v, SupportsAbs))

    print("\nRandomPicker[T_co] demo")
    machine = LottoBlower[int](range(1, 6))
    print("pick_two(machine) ->", pick_two(machine))
    print("isinstance(machine, RandomPicker) ->", isinstance(machine, RandomPicker))


if __name__ == "__main__":
    main()

