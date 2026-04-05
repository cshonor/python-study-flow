"""
FrenchDeck：组合 + __len__ / __getitem__ / __setitem__，支持 random.shuffle 与自定义排序 key。

对应笔记：10-french-deck-composition-setitem-shuffle.md
"""

from __future__ import annotations

import collections
import random

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()
    # 花色权重：数值越大，在相同 rank 下越“大”（可按书或习惯调整）
    suit_values = {"spades": 3, "hearts": 2, "diamonds": 1, "clubs": 0}

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, value) -> None:
        """委托给内部 list，使 random.shuffle(deck) 能原地交换元素。"""
        self._cards[position] = value


def spades_high(card: Card) -> int:
    """按点数再按花色计算排序键（与书中常见写法同型）。"""
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(FrenchDeck.suit_values) + FrenchDeck.suit_values[card.suit]


def explain_spades_high(card: Card) -> tuple[int, int, int, int]:
    """返回 (rank_value, 点数项, 花色项, 总权重)，便于对照笔记公式。"""
    rank_value = FrenchDeck.ranks.index(card.rank)
    n_suits = len(FrenchDeck.suit_values)
    suit_part = FrenchDeck.suit_values[card.suit]
    rank_part = rank_value * n_suits
    total = rank_part + suit_part
    return rank_value, rank_part, suit_part, total


def demo_spades_high_weights() -> None:
    """打印几张牌的权重分解：2♣ / 2♠ / A♣ / A♠。"""
    samples = [
        Card("2", "clubs"),
        Card("2", "spades"),
        Card("A", "clubs"),
        Card("A", "spades"),
    ]
    print("\n--- spades_high 权重分解（对照 10-...md §5）---")
    for c in samples:
        rv, rpart, spart, total = explain_spades_high(c)
        print(
            f"{c!s}: rank_index={rv}, "
            f"rank*{len(FrenchDeck.suit_values)}={rpart}, "
            f"suit={spart} → key={total}"
        )


def main() -> None:
    demo_spades_high_weights()

    deck = FrenchDeck()
    print("洗牌前前 5 张:", deck[:5])

    random.shuffle(deck)
    print("洗牌后前 5 张:", deck[:5])

    ordered = sorted(deck, key=spades_high)
    print("按 spades_high 排序后前 5 张:", ordered[:5])
    print("按 spades_high 排序后最后 5 张:", ordered[-5:])


if __name__ == "__main__":
    main()
