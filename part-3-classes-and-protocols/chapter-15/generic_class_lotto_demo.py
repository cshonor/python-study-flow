from __future__ import annotations

import random
from collections.abc import Iterable
from typing import Generic, Protocol, TypeVar


T = TypeVar("T")


class Tombola(Protocol[T]):
    def load(self, items: Iterable[T]) -> None: ...
    def pick(self) -> T: ...
    def loaded(self) -> bool: ...
    def inspect(self) -> tuple[T, ...]: ...


class LottoBlower(Generic[T]):
    """Generic bingo/lottery machine.

    - load: accepts Iterable[T]
    - pick: returns T
    - inspect: returns tuple[T, ...]
    """

    def __init__(self, items: Iterable[T]) -> None:
        self._balls: list[T] = list(items)

    def load(self, items: Iterable[T]) -> None:
        self._balls.extend(items)

    def pick(self) -> T:
        if not self._balls:
            raise LookupError("pick from empty LottoBlower")
        pos = random.randrange(len(self._balls))
        return self._balls.pop(pos)

    def loaded(self) -> bool:
        return bool(self._balls)

    def inspect(self) -> tuple[T, ...]:
        return tuple(self._balls)


def draw_two(machine: Tombola[T]) -> tuple[T, T]:
    return (machine.pick(), machine.pick())


def main() -> None:
    ints = LottoBlower[int](range(1, 6))
    print("ints.inspect() ->", ints.inspect())
    a = ints.pick()
    print("ints.pick() ->", a, "| type:", type(a).__name__)
    ints.load([99, 100])
    print("ints.inspect() after load ->", ints.inspect())
    print("draw_two(ints) ->", draw_two(ints))

    strs = LottoBlower[str](["A", "B", "C"])
    print("\nstrs.inspect() ->", strs.inspect())
    print("draw_two(strs) ->", draw_two(strs))


if __name__ == "__main__":
    main()

