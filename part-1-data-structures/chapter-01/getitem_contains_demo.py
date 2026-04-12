"""
演示 __getitem__ 与 __contains__：
- 未实现 __contains__：in 顺序扫描
- __contains__ + set：哈希查找
- __contains__ + bisect：有序 + 二分（O(log n)）
- __contains__ 手写 for：与默认同类，无优化

对应笔记：09-getitem与contains及成员检测优化.md
运行：python part-1-data-structures/chapter-01/getitem_contains_demo.py
"""

from __future__ import annotations

import bisect
import time
from collections import namedtuple

Card = namedtuple("Card", ["rank", "suit"])


class FrenchDeckNoContains:
    """只有 __len__ + __getitem__：in 走默认顺序扫描。"""

    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self) -> None:
        self._cards = [Card(r, s) for s in self.suits for r in self.ranks]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, index):
        return self._cards[index]


class FrenchDeckSetContains(FrenchDeckNoContains):
    """__contains__ 用 set（均摊 O(1)）。"""

    def __init__(self) -> None:
        super().__init__()
        self._card_set = set(self._cards)

    def __contains__(self, item: object) -> bool:
        return item in self._card_set


class FrenchDeckBisectContains(FrenchDeckNoContains):
    """__contains__ 用有序列表 + bisect（O(log n)）。Card 按 (rank, suit) 字典序可比较。"""

    def __init__(self) -> None:
        super().__init__()
        self._sorted_cards = sorted(self._cards)

    def __contains__(self, item: object) -> bool:
        if not isinstance(item, Card):
            return False
        i = bisect.bisect_left(self._sorted_cards, item)
        return i < len(self._sorted_cards) and self._sorted_cards[i] == item


class FrenchDeckManualLinearContains(FrenchDeckNoContains):
    """__contains__ 手写 for：逻辑等价于默认扫描，无性能优化（仅作对照）。"""

    def __contains__(self, item: object) -> bool:
        for card in self._cards:
            if card == item:
                return True
        return False


def _time_in(deck, needle: Card, repeats: int) -> float:
    t0 = time.perf_counter()
    for _ in range(repeats):
        _ = needle in deck
    return time.perf_counter() - t0


def main() -> None:
    slow = FrenchDeckNoContains()
    with_set = FrenchDeckSetContains()
    with_bisect = FrenchDeckBisectContains()
    with_linear = FrenchDeckManualLinearContains()

    needle = slow[-1]
    for name, d in [
        ("无 __contains__", slow),
        ("set", with_set),
        ("bisect", with_bisect),
        ("手写 for", with_linear),
    ]:
        assert needle in d, name

    n = 5000
    print(f"len(deck) = {len(slow)}，查找目标 = {needle}，重复 {n} 次 `in`\n")

    t_slow = _time_in(slow, needle, n)
    t_set = _time_in(with_set, needle, n)
    t_bisect = _time_in(with_bisect, needle, n)
    t_linear = _time_in(with_linear, needle, n)

    print(f"无 __contains__（默认扫描）: {t_slow:.4f} s")
    print(f"__contains__ + set:            {t_set:.4f} s")
    print(f"__contains__ + bisect:         {t_bisect:.4f} s")
    print(f"__contains__ 手写 for:         {t_linear:.4f} s")
    print("\n说明：n=52 时 set 通常仍最快；bisect 优势在 n 很大时更明显。手写 for 与默认扫描同类。")


if __name__ == "__main__":
    main()
