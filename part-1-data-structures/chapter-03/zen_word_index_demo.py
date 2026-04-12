"""
Demo for 07-可变值与词索引.md (Fluent Python §3.4.3).

Uses an in-memory excerpt of "The Zen of Python" — no external zen.txt required.
Line numbers in locations use enumerate(..., 1) like Fluent Python example 3-5.

Run:
  python part-1-data-structures/chapter-03/zen_word_index_demo.py
"""

from __future__ import annotations

import re
from collections import defaultdict
from io import StringIO

WORD_RE = re.compile(r"\w+")

# Short excerpt; enough tokens to exercise the index
ZEN_EXCERPT = """Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
"""


def build_index_get(text: str) -> dict[str, list[tuple[int, int]]]:
    index: dict[str, list[tuple[int, int]]] = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in WORD_RE.finditer(line):
            word = m.group()
            col = m.start() + 1
            loc = (line_no, col)
            occ = index.get(word, [])
            occ.append(loc)
            index[word] = occ
    return index


def build_index_setdefault(text: str) -> dict[str, list[tuple[int, int]]]:
    index: dict[str, list[tuple[int, int]]] = {}
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in WORD_RE.finditer(line):
            word = m.group()
            col = m.start() + 1
            index.setdefault(word, []).append((line_no, col))
    return index


def build_index_defaultdict(text: str) -> defaultdict[str, list[tuple[int, int]]]:
    index: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in WORD_RE.finditer(line):
            word = m.group()
            col = m.start() + 1
            index[word].append((line_no, col))
    return index


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_three_builders() -> None:
    section("1) same result: get vs setdefault vs defaultdict")
    g = build_index_get(ZEN_EXCERPT)
    s = build_index_setdefault(ZEN_EXCERPT)
    d = build_index_defaultdict(ZEN_EXCERPT)
    assert g == dict(s) == dict(d)
    print("word count:", len(g))
    w = sorted(g, key=str.upper)[0]
    print("first word (casefold sort):", w, "->", g[w][:3], "...")


def demo_default_arg_evaluated() -> None:
    section("2) get/setdefault: default expression runs every call")
    calls = 0

    def fresh_list() -> list[int]:
        nonlocal calls
        calls += 1
        return []

    idx: dict[str, list[int]] = {"w": [1]}
    _ = idx.get("w", fresh_list())
    _ = idx.get("w", fresh_list())
    print("get existing key: fresh_list() called", calls, "times")

    calls = 0
    idx2: dict[str, list[int]] = {}
    idx2.setdefault("w", fresh_list())
    idx2.setdefault("w", fresh_list())
    print("setdefault existing key: fresh_list() called", calls, "times")


def demo_defaultdict_factory_only_on_miss() -> None:
    section("3) defaultdict: factory only when key missing")
    factory_calls = 0

    def track() -> list[int]:
        nonlocal factory_calls
        factory_calls += 1
        return []

    dd: defaultdict[str, list[int]] = defaultdict(track)
    dd["a"].append(1)
    dd["a"].append(2)
    dd["b"].append(3)
    print("factory_calls (expect 2 for keys a,b):", factory_calls)


def main() -> None:
    demo_three_builders()
    demo_default_arg_evaluated()
    demo_defaultdict_factory_only_on_miss()


if __name__ == "__main__":
    main()
