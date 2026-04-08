from __future__ import annotations

import abc
from collections import namedtuple
from collections.abc import MutableSequence, Sequence
from random import randrange, shuffle
from typing import Generic, Iterable, TypeVar


# --- Part 1: FrenchDeck (duck typing) vs FrenchDeck2 (goose typing via ABC) ---

Card = namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


class FrenchDeck2(MutableSequence[Card]):
    """Explicitly a mutable sequence (ABC subclass)."""

    ranks = FrenchDeck.ranks
    suits = FrenchDeck.suits

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value: Card) -> None:
        self._cards[position] = value

    def __delitem__(self, position) -> None:
        del self._cards[position]

    def insert(self, index: int, value: Card) -> None:
        self._cards.insert(index, value)


# --- Part 2: Custom ABC (Tombola) + concrete methods + virtual subclass ---

T = TypeVar("T")


class Tombola(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def load(self, iterable: Iterable[T]) -> None: ...

    @abc.abstractmethod
    def pick(self) -> T:
        """Remove and return one item; raise LookupError if empty."""

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


class LotteryBlower(Tombola[T]):
    def __init__(self, items: Iterable[T]) -> None:
        self._balls: list[T] = list(items)

    def load(self, iterable: Iterable[T]) -> None:
        self._balls.extend(iterable)

    def pick(self) -> T:
        if not self._balls:
            raise LookupError("pick from empty Tombola")
        pos = randrange(len(self._balls))
        return self._balls.pop(pos)


class TomboList(list[T]):
    def pick(self) -> T:
        if not self:
            raise LookupError("pop from empty TomboList")
        pos = randrange(len(self))
        return self.pop(pos)

    def load(self, iterable: Iterable[T]) -> None:
        self.extend(iterable)

    def loaded(self) -> bool:
        return bool(self)

    def inspect(self) -> tuple[T, ...]:
        return tuple(sorted(self, key=repr))


Tombola.register(TomboList)


def main() -> None:
    print("FrenchDeck (duck typing sequence behavior)")
    deck = FrenchDeck()
    print("isinstance(deck, Sequence) ->", isinstance(deck, Sequence))
    try:
        shuffle(deck)
    except TypeError as e:
        print("shuffle(deck) ->", e)

    print("\nFrenchDeck2 (goose typing via MutableSequence)")
    deck2 = FrenchDeck2()
    print("isinstance(deck2, Sequence) ->", isinstance(deck2, Sequence))
    print("isinstance(deck2, MutableSequence) ->", isinstance(deck2, MutableSequence))
    shuffle(deck2)
    print("shuffle(deck2) -> ok")
    deck2.append(Card("A", "spades"))
    print("append(...) -> ok; last ->", deck2[-1])

    print("\nTombola ABC: abstract + concrete methods")
    cage = BingoCage([1, 2, 3, 4])
    blower = LotteryBlower(["a", "b", "c"])
    print("cage.inspect() ->", cage.inspect())
    print("blower.loaded() ->", blower.loaded())

    print("\nvirtual subclass via register()")
    tl: TomboList[int] = TomboList([10, 20, 30])
    print("isinstance(tl, Tombola) ->", isinstance(tl, Tombola))
    print("tl.inspect() ->", tl.inspect())

    print("\nfail fast: abstract methods enforced")
    try:
        class Fake(Tombola[int]):
            def load(self, iterable: Iterable[int]) -> None:
                pass

        Fake()  # type: ignore[abstract]
    except TypeError as e:
        print("instantiating Fake ->", e)


if __name__ == "__main__":
    main()

