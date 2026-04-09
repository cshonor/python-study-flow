"""Ch. 17.2: Sentence and the sequence protocol (__getitem__ fallback iteration)."""

from __future__ import annotations

import re
import reprlib
from collections.abc import Iterator


RE_WORD = re.compile(r"\w+")


class Sentence:
    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index: int):
        return self.words[index]

    def __len__(self) -> int:
        return len(self.words)

    def __repr__(self) -> str:
        return f"Sentence({reprlib.repr(self.text)})"


class SentenceIter:
    """Same interface, but with an explicit iterator."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __iter__(self) -> Iterator[str]:
        return iter(self.words)

    def __len__(self) -> int:
        return len(self.words)

    def __repr__(self) -> str:
        return f"SentenceIter({reprlib.repr(self.text)})"


def main() -> None:
    text = '"The time has come," the Walrus said,'
    s = Sentence(text)
    s2 = SentenceIter(text)

    print("repr(s)  ->", s)
    print("len(s)   ->", len(s))
    print("s[0]     ->", s[0])
    print("s[-1]    ->", s[-1])
    print("list(s)  ->", list(s))
    print()

    print("repr(s2) ->", s2)
    print("list(s2) ->", list(s2))


if __name__ == "__main__":
    main()

