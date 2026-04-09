"""Ch. 17.5: Sentence implementations — iterator class vs generator vs generator expression."""

from __future__ import annotations

import re
import reprlib
from collections.abc import Iterator


RE_WORD = re.compile(r"\w+")


class SentenceClassic:
    """Version 1: classic iterator pattern (explicit iterator class)."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f"SentenceClassic({reprlib.repr(self.text)})"

    def __iter__(self) -> "SentenceIterator":
        return SentenceIterator(self.words)


class SentenceIterator(Iterator[str]):
    def __init__(self, words: list[str]) -> None:
        self._words = words
        self._i = 0

    def __iter__(self) -> "SentenceIterator":
        return self

    def __next__(self) -> str:
        try:
            word = self._words[self._i]
        except IndexError as e:
            raise StopIteration from e
        self._i += 1
        return word


class SentenceGenFunc:
    """Version 2: generator function inside __iter__ (pythonic)."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f"SentenceGenFunc({reprlib.repr(self.text)})"

    def __iter__(self):
        for w in self.words:
            yield w


class SentenceGenExpr:
    """Version 3: generator expression returned by __iter__."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f"SentenceGenExpr({reprlib.repr(self.text)})"

    def __iter__(self):
        return (w for w in self.words)


class SentenceBadIterator:
    """Anti-pattern: iterable object is its own iterator (one-shot)."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)
        self._i = 0

    def __repr__(self) -> str:
        return f"SentenceBadIterator({reprlib.repr(self.text)})"

    def __iter__(self) -> "SentenceBadIterator":
        return self

    def __next__(self) -> str:
        try:
            word = self.words[self._i]
        except IndexError as e:
            raise StopIteration from e
        self._i += 1
        return word


def show_twice(label: str, s) -> None:
    print(label, "->", s)
    print("list #1 ->", list(s))
    print("list #2 ->", list(s))
    print()


def main() -> None:
    text = '"The time has come," the Walrus said,'
    show_twice("classic iterator", SentenceClassic(text))
    show_twice("generator func", SentenceGenFunc(text))
    show_twice("generator expr", SentenceGenExpr(text))
    show_twice("BAD one-shot", SentenceBadIterator(text))


if __name__ == "__main__":
    main()

