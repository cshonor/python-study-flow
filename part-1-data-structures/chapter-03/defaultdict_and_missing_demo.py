"""
Demo for 08-defaultdict与missing.md (Fluent Python §3.5).

Run:
  python part-1-data-structures/chapter-03/defaultdict_and_missing_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import re
from collections import defaultdict

WORD_RE = re.compile(r"\w+")
TEXT = """Beautiful is better than ugly.
Explicit is better than implicit.
"""


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def build_defaultdict_index(text: str) -> defaultdict[str, list[tuple[int, int]]]:
    index: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in WORD_RE.finditer(line):
            word = m.group()
            index[word].append((line_no, m.start() + 1))
    return index


def demo_defaultdict_index() -> None:
    section("1) defaultdict(list) word index (example 3-6 style)")
    idx = build_defaultdict_index(TEXT)
    print("keys sample:", sorted(idx, key=str.upper)[:3])
    print("Beautiful ->", idx.get("Beautiful"))


def demo_get_does_not_insert() -> None:
    section("2) get() does not trigger default_factory")
    dd: defaultdict[str, list[int]] = defaultdict(list)
    print("dd.get('x'):", dd.get("x"), "| 'x' in dd:", "x" in dd)
    _ = dd["x"]
    print("after dd['x'], 'x' in dd:", "x" in dd, "| value:", dd["x"])


def demo_int_count() -> None:
    section("3) defaultdict(int) counting")
    wc: defaultdict[str, int] = defaultdict(int)
    for w in "a b a c b b".split():
        wc[w] += 1
    print(dict(wc))


def demo_nested_defaultdict_dict() -> None:
    section("4) defaultdict(dict) one level nesting")
    nested: defaultdict[str, dict[str, str]] = defaultdict(dict)
    nested["user"]["name"] = "Alice"
    print(dict(nested))


class ListOnMiss(dict[str, list[tuple[int, int]]]):
    """Minimal __missing__: create empty list for unknown keys."""

    def __missing__(self, key: str) -> list[tuple[int, int]]:
        self[key] = []
        return self[key]


def demo_dunder_missing() -> None:
    section("5) custom dict subclass with __missing__")
    m = ListOnMiss()
    m["hi"].append((1, 1))
    print(m["hi"])


def main() -> None:
    demo_defaultdict_index()
    demo_get_does_not_insert()
    demo_int_count()
    demo_nested_defaultdict_dict()
    demo_dunder_missing()


if __name__ == "__main__":
    main()
