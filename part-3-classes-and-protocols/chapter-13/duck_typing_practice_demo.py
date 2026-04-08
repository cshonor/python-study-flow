from __future__ import annotations

from collections import namedtuple
from random import shuffle
from typing import Iterable


class Vowels:
    """Minimal dynamic-protocol example: __getitem__ only."""

    def __getitem__(self, i):
        return "AEIOU"[i]


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


def normalize_field_names(field_names: str | Iterable[str]) -> tuple[str, ...]:
    """Fail-fast normalization similar in spirit to namedtuple.

    Accepts:
    - "x y z" or "x,y,z"
    - iterable of strings
    """

    if isinstance(field_names, str):
        raw = field_names.replace(",", " ").split()
    else:
        raw = tuple(field_names)

    if not raw:
        raise ValueError("field_names must not be empty")

    normalized: list[str] = []
    for name in raw:
        if not isinstance(name, str):
            raise TypeError("field names must be strings")
        if not name.isidentifier():
            raise ValueError(f"invalid field name: {name!r}")
        normalized.append(name)

    # Copy to an immutable container to prevent external mutation.
    return tuple(normalized)


def main() -> None:
    print("dynamic protocol: __getitem__ fallback for iteration and membership")
    v = Vowels()
    print("v[0], v[-1] ->", v[0], v[-1])
    print("list(v) ->", list(v))
    print("'E' in v ->", "E" in v)
    print("'Z' in v ->", "Z" in v)

    print("\nsequence protocol: FrenchDeck behaves like a sequence")
    deck = FrenchDeck()
    print("len(deck) ->", len(deck))
    print("deck[0] ->", deck[0])
    print("deck[1:4] ->", deck[1:4])

    print("\nmonkey patching: make shuffle(deck) work by adding __setitem__")
    try:
        shuffle(deck)
    except TypeError as e:
        print("shuffle(deck) before patch ->", e)

    def set_card(self: FrenchDeck, position: int, card: Card) -> None:
        self._cards[position] = card

    FrenchDeck.__setitem__ = set_card  # type: ignore[attr-defined]
    shuffle(deck)
    print("shuffle(deck) after patch -> ok")
    print("deck[:3] ->", deck[:3])

    print("\nfail fast: normalize_field_names")
    print("normalize_field_names('x, y z') ->", normalize_field_names("x, y z"))
    print("normalize_field_names(['a', 'b']) ->", normalize_field_names(["a", "b"]))
    try:
        normalize_field_names(["ok", "not-valid!"])
    except Exception as e:
        print("normalize_field_names([...]) error ->", e)


if __name__ == "__main__":
    main()

