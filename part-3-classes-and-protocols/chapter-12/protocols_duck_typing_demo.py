from __future__ import annotations

from collections import namedtuple
from typing import Protocol, runtime_checkable


# --- Dynamic protocol demo: "sequence protocol" via __len__ + __getitem__ ---

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


# --- Static protocol demo (PEP 544): structural subtyping for type checkers ---


class Speaker(Protocol):
    def speak(self) -> str: ...


@runtime_checkable
class RuntimeSpeaker(Protocol):
    def speak(self) -> str: ...


class Duck:
    def speak(self) -> str:
        return "quack"


class Person:
    def speak(self) -> str:
        return "hello"


class Silent:
    pass


def call_speak(x: Speaker) -> str:
    # At runtime, this just calls the method.
    # Type checkers use Speaker to validate "has .speak() -> str".
    return x.speak()


def main() -> None:
    print("sequence protocol (duck typing)")
    deck = FrenchDeck()
    print("len(deck) ->", len(deck))
    print("deck[0] ->", deck[0])
    print("deck[1:4] ->", deck[1:4])
    print("iter works ->", list(deck[:3]))

    print("\nstatic Protocol (structural typing)")
    print("call_speak(Duck()) ->", call_speak(Duck()))
    print("call_speak(Person()) ->", call_speak(Person()))

    print("\nruntime_checkable Protocol (optional runtime isinstance)")
    print("isinstance(Duck(), RuntimeSpeaker) ->", isinstance(Duck(), RuntimeSpeaker))
    print("isinstance(Silent(), RuntimeSpeaker) ->", isinstance(Silent(), RuntimeSpeaker))

    print("\nwhat happens without the method (runtime)?")
    try:
        call_speak(Silent())  # type: ignore[arg-type]
    except AttributeError as e:
        print("call_speak(Silent()) ->", e)


if __name__ == "__main__":
    main()

