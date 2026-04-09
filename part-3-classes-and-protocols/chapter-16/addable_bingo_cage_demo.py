"""Ch. 16: AddableBingoCage — mutable __iadd__ vs non-mutating __add__ (Fluent Python 16-19)."""

from __future__ import annotations

import abc
from random import shuffle
from typing import Generic, Iterable, TypeVar


T = TypeVar("T")


class Tombola(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def load(self, iterable: Iterable[T]) -> None: ...

    @abc.abstractmethod
    def pick(self) -> T: ...

    def loaded(self) -> bool:
        return bool(self.inspect())

    def inspect(self) -> tuple[T, ...]:
        items: list[T] = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items, key=repr))


class BingoCage(Tombola[T]):
    def __init__(self, items: Iterable[T]) -> None:
        self._items: list[T] = []
        self.load(items)

    def load(self, iterable: Iterable[T]) -> None:
        self._items.extend(iterable)
        shuffle(self._items)

    def pick(self) -> T:
        try:
            return self._items.pop()
        except IndexError as e:
            raise LookupError("pick from empty Tombola") from e


class AddableBingoCage(BingoCage[T]):
    def __add__(self, other: object):
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        return NotImplemented

    def __iadd__(self, other: object) -> AddableBingoCage[T]:
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError as e:
                raise TypeError(
                    "right operand in += must be 'Tombola' or an iterable"
                ) from e
        self.load(other_iterable)
        return self


def main() -> None:
    vowels = "AEIOU"
    globe = AddableBingoCage(vowels)
    globe2 = AddableBingoCage("XY")  # 5 + 2 == 7 items in globe + globe2

    globe3 = globe + globe2
    print("len(globe3.inspect()) ->", len(globe3.inspect()))
    print("globe is globe3 ->", globe is globe3)

    try:
        _ = globe + [10, 20]  # noqa: F841
    except TypeError as e:
        print("globe + [10, 20] -> TypeError:", e)

    globe_orig = globe
    n0 = len(globe.inspect())
    print("len(globe) after inspect ->", n0)

    globe += globe2
    print("after += cage: len(inspect) ->", len(globe.inspect()))
    print("globe is globe_orig ->", globe is globe_orig)

    globe += ["M", "N"]
    print("after += list: len(inspect) ->", len(globe.inspect()))

    try:
        globe += 1  # type: ignore[operator]
    except TypeError as e:
        print("globe += 1 -> TypeError:", e)


if __name__ == "__main__":
    main()
