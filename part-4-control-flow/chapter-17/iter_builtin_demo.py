"""Ch. 17.3: iter() rules, duck typing, and iter(callable, sentinel)."""

from __future__ import annotations

import os
from collections.abc import Iterable as AbcIterable
from functools import partial
from random import randint
from tempfile import NamedTemporaryFile


class WithIter:
    def __init__(self) -> None:
        self._data = [10, 20, 30]

    def __iter__(self):
        # iter() should prefer this over __getitem__
        return iter(self._data)

    def __getitem__(self, index: int):
        raise AssertionError("__getitem__ should not be used when __iter__ exists")


class GetItemOnly:
    def __init__(self) -> None:
        self._data = ["A", "B", "C"]

    def __getitem__(self, index: int):
        return self._data[index]


def d6() -> int:
    return randint(1, 6)


def main() -> None:
    print("== iter(x): prefer __iter__ ==")
    x = WithIter()
    print("list(x) ->", list(x))
    print()

    print("== iter(x): fallback to __getitem__ ==")
    y = GetItemOnly()
    print("list(y) ->", list(y))
    print("isinstance(y, abc.Iterable) ->", isinstance(y, AbcIterable))
    try:
        it = iter(y)
    except TypeError as e:
        print("iter(y) -> TypeError:", e)
    else:
        print("iter(y) works ->", it)
    print()

    print("== iter(callable, sentinel): roll d6 until 1 ==")
    rolls = list(iter(d6, 1))
    print("rolls (stops before 1) ->", rolls)
    print()

    print("== iter(callable, sentinel): read file in blocks ==")
    payload = b"0123456789ABCDEF" * 4  # 64 bytes
    with NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
        tmp.write(payload + b"TAIL")

    try:
        with open(path, "rb") as f:
            read16 = partial(f.read, 16)
            blocks = list(iter(read16, b""))
        print("blocks read ->", len(blocks), "of size", {len(b) for b in blocks})
        print("first block ->", blocks[0])
        print("last block  ->", blocks[-1])
    finally:
        os.unlink(path)


if __name__ == "__main__":
    main()

