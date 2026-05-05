"""
Demo for 07-可变值与词索引.md (Fluent Python §3.4.3).

Uses an in-memory excerpt of "The Zen of Python" — no external zen.txt required.
Line numbers in locations use enumerate(..., 1) like Fluent Python example 3-5.

Run:
  python part-1-data-structures/chapter-03/07_zen_word_index_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
- 第 **2b)** 节：键已存在时，打印「造空列表」次数（`get` / `setdefault` vs `defaultdict`）。  
- 第 **4)** 节：键已存在时，`get`/`setdefault` 每次仍对 `[]` 求值 vs `defaultdict` 热循环粗计时（见笔记 **§四**）。
"""

from __future__ import annotations

import re
import time
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


def demo_list_ctor_counts_when_key_exists() -> None:
    section("2b) key exists: count empty-list constructions (get vs setdefault vs defaultdict)")
    loops = 5
    key = "x"

    built = 0

    def tracked_empty() -> list[int]:
        nonlocal built
        built += 1
        return []

    d1: dict[str, list[int]] = {key: [41]}
    built = 0
    for _ in range(loops):
        lst = d1.get(key, tracked_empty())
        lst.append(0)
        d1[key] = lst
    print(f"get + writeback: tracked_empty() -> {built} (expect {loops} dead lists)")

    d2: dict[str, list[int]] = {key: [41]}
    built = 0
    for _ in range(loops):
        d2.setdefault(key, tracked_empty()).append(0)
    print(f"setdefault:        tracked_empty() -> {built} (expect {loops})")

    factory_calls = 0

    def track_factory() -> list[int]:
        nonlocal factory_calls
        factory_calls += 1
        return []

    dd: defaultdict[str, list[int]] = defaultdict(track_factory)
    dd[key].append(41)  # miss -> one list
    before = factory_calls
    for _ in range(loops):
        dd[key].append(0)
    during_loop = factory_calls - before
    print(
        f"defaultdict:       factory calls total={factory_calls}; "
        f"during {loops} appends on existing key = {during_loop} (expect 0)"
    )


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


def demo_hot_loop_empty_list_overhead() -> None:
    section("4) hot loop: key exists, N appends (rough perf; see 07 md section 4)")
    n = 250_000
    key = "k"

    d_get: dict[str, list[int]] = {key: []}
    t0 = time.perf_counter()
    for _ in range(n):
        lst = d_get.get(key, [])
        lst.append(0)
        d_get[key] = lst
    t_get = time.perf_counter() - t0

    d_sd: dict[str, list[int]] = {key: []}
    t0 = time.perf_counter()
    for _ in range(n):
        d_sd.setdefault(key, []).append(0)
    t_sd = time.perf_counter() - t0

    d_dd: defaultdict[str, list[int]] = defaultdict(list)
    _ = d_dd[key]  # one miss -> factory once
    t0 = time.perf_counter()
    for _ in range(n):
        d_dd[key].append(0)
    t_dd = time.perf_counter() - t0

    print(f"N={n} appends (key already in dict before loop)")
    print(f"  get + writeback:  {t_get:.3f}s")
    print(f"  setdefault:       {t_sd:.3f}s")
    print(f"  defaultdict[k]:   {t_dd:.3f}s  (no [] literal per iteration)")


def main() -> None:
    demo_three_builders()
    demo_default_arg_evaluated()
    demo_list_ctor_counts_when_key_exists()
    demo_defaultdict_factory_only_on_miss()
    demo_hot_loop_empty_list_overhead()


if __name__ == "__main__":
    main()
