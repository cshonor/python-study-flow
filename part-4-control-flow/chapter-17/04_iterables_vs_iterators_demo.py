"""Ch. 17.4: iterables vs iterators + explicit SentenceIterator."""

from __future__ import annotations

import re
import reprlib
from collections.abc import Iterator


RE_WORD = re.compile(r"\w+")


class Sentence:
    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __iter__(self) -> "SentenceIterator":
        return SentenceIterator(self.words)

    def __repr__(self) -> str:
        return f"Sentence({reprlib.repr(self.text)})"


class SentenceIterator(Iterator[str]):
    def __init__(self, words: list[str]) -> None:
        self._words = words
        self._index = 0

    def __iter__(self) -> "SentenceIterator":
        return self

    def __next__(self) -> str:
        try:
            word = self._words[self._index]
        except IndexError as e:
            raise StopIteration from e
        self._index += 1
        return word


def main() -> None:
    print("== iterable vs iterator ==")
    data = [1, 2, 3]
    it = iter(data)
    print("iter(data) is data ->", iter(data) is data)
    print("iter(it) is it     ->", iter(it) is it)
    print("list(it)           ->", list(it))
    print("list(it) again     ->", list(it), "(iterator exhausted)")
    print()

    print("== Sentence with explicit iterator ==")
    s = Sentence('"The time has come," the Walrus said,')
    print("repr(s) ->", s)

    it2 = iter(s)
    print("iter(s) is s  ->", it2 is s)
    print("iter(it2) is it2 ->", iter(it2) is it2)

    print("list(s) ->", list(s), "(new iterator each time)")
    print("list(it2) ->", list(it2))
    print("list(it2) again ->", list(it2), "(exhausted)")


if __name__ == "__main__":
    main()

