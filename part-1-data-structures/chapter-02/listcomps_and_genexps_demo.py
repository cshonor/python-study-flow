"""
Demo for 03-列表推导式与生成器表达式.md

Run:
  python part-1-data-structures/chapter-02/listcomps_and_genexps_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

from collections.abc import Iterator
from itertools import product


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def safe_text(s: str) -> str:
    """Render Unicode safely in non-UTF8 consoles (e.g. GBK)."""
    return s.encode("unicode_escape").decode("ascii")


def demo_listcomp_vs_for_append() -> None:
    section("1) listcomp vs for+append (same result)")
    symbols = "$¢£¥€¤"

    codes_a: list[int] = []
    for ch in symbols:
        codes_a.append(ord(ch))

    codes_b = [ord(ch) for ch in symbols]

    # Use escaped form so output works in non-UTF8 consoles.
    print("symbols (escaped):", safe_text(symbols))
    print("for+append:", codes_a)
    print("listcomp  :", codes_b)
    assert codes_a == codes_b


def demo_listcomp_vs_map_filter() -> None:
    section("2) listcomp vs map/filter (unicode codepoints > 127)")
    symbols = "$¢£¥€¤"

    beyond_ascii_a = [ord(s) for s in symbols if ord(s) > 127]
    beyond_ascii_b = list(filter(lambda c: c > 127, map(ord, symbols)))

    print("symbols (escaped):", safe_text(symbols))
    print("listcomp     :", beyond_ascii_a)
    print("map+filter   :", beyond_ascii_b)
    assert beyond_ascii_a == beyond_ascii_b


def demo_genexp_is_lazy() -> None:
    section("3) genexp is lazy; listcomp is eager")
    data = [1, 2, 3, 4]

    gen = (x * x for x in data)
    print("gen type:", type(gen))
    assert isinstance(gen, Iterator)

    print("consume 2 items:", next(gen), next(gen))
    print("consume rest   :", list(gen))

    eager = [x * x for x in data]
    print("listcomp result:", eager)


def demo_no_side_effect_listcomp() -> None:
    section("4) don't use listcomp for side effects (demo only)")
    items = [10, 20, 30]
    print("preferred: for-loop printing")
    for x in items:
        print(" ", x)

    print("anti-pattern: listcomp for printing (creates useless list of Nones)")
    noles = [print(" ", x) for x in items]
    print("result list:", noles)
    assert noles == [None, None, None]


def demo_comprehension_scope() -> None:
    section("5) comprehension loop variable doesn't leak (Python 3)")
    x = "ABC"
    codes = [ord(x) for x in x]
    print("outer x:", x)
    print("codes  :", codes)
    assert x == "ABC"
    assert codes == [65, 66, 67]


def demo_walrus_exception() -> None:
    section("6) walrus (:=) target remains in outer scope")
    x = "ABC"
    codes = [last := ord(c) for c in x]
    print("codes:", codes)
    print("last :", last)
    assert last == 67

    try:
        c  # noqa: F821
        raise AssertionError("c should not be defined outside comprehension")
    except NameError:
        print("c is not defined outside comprehension (expected)")


def demo_cartesian_product() -> None:
    section("7) Cartesian product: listcomp vs itertools.product")
    ranks = ["A", "K", "Q"]
    suits = ["♠", "♡", "♢", "♣"]

    cards_lc = [(r, s) for r in ranks for s in suits]
    cards_prod = list(product(ranks, suits))
    assert cards_lc == cards_prod
    print("ranks:", ranks)
    print("suits (escaped):", safe_text("".join(suits)))
    print("count:", len(cards_lc), "(3 x 4 = 12)")
    first4 = [(safe_text(r), safe_text(s)) for r, s in cards_lc[:4]]
    print("first 4 (listcomp, escaped):", first4)

    colors = ["黑色", "白色"]
    sizes = ["S", "M", "L"]
    tees = [(c, z) for c in colors for z in sizes]
    assert len(tees) == 6
    print("T-shirts sample (escaped):", str(tees[:3]).encode("unicode_escape").decode("ascii"), "...")

    # Lazy: generator expression does not build full list until consumed
    gen = ((r, s) for r in ranks for s in suits)
    first = next(gen)
    print(
        "genexp is lazy:",
        gen,
        "-> first:",
        (safe_text(first[0]), safe_text(first[1])),
    )


def demo_bracketed_line_breaks() -> None:
    section("8) line breaks inside [] work (no backslashes)")
    symbols = "$¢£¥€¤"
    codes = [
        ord(symbol)
        for symbol in symbols
        if ord(symbol) > 127
    ]
    print("symbols (escaped):", safe_text(symbols))
    print("codes:", codes)
    assert codes == [162, 163, 165, 8364, 164]


def main() -> None:
    demo_listcomp_vs_for_append()
    demo_listcomp_vs_map_filter()
    demo_genexp_is_lazy()
    demo_no_side_effect_listcomp()
    demo_comprehension_scope()
    demo_walrus_exception()
    demo_cartesian_product()
    demo_bracketed_line_breaks()


if __name__ == "__main__":
    main()

