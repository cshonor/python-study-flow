"""Ch. 17.6: lazy iteration with re.finditer and generator expressions."""

from __future__ import annotations

import re
import reprlib
from itertools import islice


RE_WORD = re.compile(r"\w+")


class SentenceEager:
    """Eager: precompute and store all words."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f"SentenceEager({reprlib.repr(self.text)})"

    def __iter__(self):
        return iter(self.words)


class SentenceLazyYield:
    """Lazy: finditer + generator function (yield)."""

    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self) -> str:
        return f"SentenceLazyYield({reprlib.repr(self.text)})"

    def __iter__(self):
        for m in RE_WORD.finditer(self.text):
            yield m.group()


class SentenceLazyGenExpr:
    """Lazy: finditer + generator expression."""

    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self) -> str:
        return f"SentenceLazyGenExpr({reprlib.repr(self.text)})"

    def __iter__(self):
        return (m.group() for m in RE_WORD.finditer(self.text))


def preview(iterable, n: int = 7) -> list[str]:
    return list(islice(iterable, n))


def main() -> None:
    text = ('"The time has come," the Walrus said, ' * 10_000).strip()

    print("== re.findall vs re.finditer ==")
    words = RE_WORD.findall(text)
    it = RE_WORD.finditer(text)
    print("type(findall) ->", type(words).__name__, "len ->", len(words))
    print("type(finditer) ->", type(it).__name__)
    print("preview(finditer) ->", [m.group() for m in islice(RE_WORD.finditer(text), 7)])
    print()

    print("== Sentence eager vs lazy ==")
    s1 = SentenceEager(text)
    s2 = SentenceLazyYield(text)
    s3 = SentenceLazyGenExpr(text)
    print("repr ->", s1)
    print("eager preview ->", preview(iter(s1)))
    print("lazy(yield) preview ->", preview(iter(s2)))
    print("lazy(genexpr) preview ->", preview(iter(s3)))
    print()

    print("== laziness: iterator is one-shot ==")
    it2 = iter(s3)
    print("first 5 ->", list(islice(it2, 5)))
    print("then 5 ->", list(islice(it2, 5)))
    print("rest?  ->", list(islice(it2, 5)), "(still advancing)")
    remaining = sum(1 for _ in it2)
    print("remaining items after slices ->", remaining)
    print()


if __name__ == "__main__":
    main()

