from __future__ import annotations

import abc
from collections.abc import Sized
from random import randrange
from typing import Iterable, TypeVar


# --- Part 1: virtual subclass via register() ---

T = TypeVar("T")


class Tombola(abc.ABC):
    @abc.abstractmethod
    def load(self, iterable: Iterable[T]) -> None: ...

    @abc.abstractmethod
    def pick(self) -> T:
        """Remove and return one item; raise LookupError if empty."""

    def loaded(self) -> bool:
        # Concrete method that relies only on the abstract interface.
        try:
            self.inspect()
        except LookupError:
            return False
        return True

    def inspect(self) -> tuple[T, ...]:
        items: list[T] = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(items)


@Tombola.register
class TomboList(list[T]):
    """Virtual subclass of Tombola: registered, not inherited."""

    def pick(self) -> T:
        if not self:
            raise LookupError("pop from empty TomboList")
        pos = randrange(len(self))
        return self.pop(pos)

    def load(self, iterable: Iterable[T]) -> None:
        self.extend(iterable)


@Tombola.register
class BadTombola:
    """Registered but does NOT implement the interface (register does not validate)."""

    pass


# --- Part 2: __subclasshook__ (runtime structural typing) ---


class Struggle:
    def __len__(self) -> int:
        return 23


class NoLen:
    pass


def main() -> None:
    print("virtual subclass: register() affects isinstance/issubclass only")
    tl = TomboList([10, 20, 30])
    print("TomboList.__mro__ ->", TomboList.__mro__)
    print("issubclass(TomboList, Tombola) ->", issubclass(TomboList, Tombola))
    print("isinstance(tl, Tombola) ->", isinstance(tl, Tombola))

    print("\nvirtual subclass does NOT inherit ABC methods")
    print("hasattr(tl, 'loaded') ->", hasattr(tl, "loaded"))
    print("hasattr(tl, 'inspect') ->", hasattr(tl, "inspect"))
    print("tl.pick() ->", tl.pick())
    try:
        tl.loaded()  # type: ignore[attr-defined]
    except AttributeError as e:
        print("tl.loaded() ->", e)

    print("\nregister() does NOT validate interface conformance")
    bt = BadTombola()
    print("isinstance(bt, Tombola) ->", isinstance(bt, Tombola))
    try:
        # This fails at runtime because the behavior isn't actually there.
        bt.pick()  # type: ignore[attr-defined]
    except AttributeError as e:
        print("bt.pick() ->", e)

    print("\n__subclasshook__ example: collections.abc.Sized")
    print("isinstance(Struggle(), Sized) ->", isinstance(Struggle(), Sized))
    print("isinstance(NoLen(), Sized) ->", isinstance(NoLen(), Sized))


if __name__ == "__main__":
    main()

