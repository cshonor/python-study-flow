"""演示 `random.choice` 如何依赖 `__len__` 与 `__getitem__` 从自定义“序列”中取样。

运行（仓库根目录）：
  python part-1-data-structures/chapter-01/random_choice_special_methods_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

from collections import namedtuple
from random import choice
from typing import Union

Card = namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    """一个最小的“类序列”示例，用来演示 random.choice 的工作方式。

    核心结论：
    - 只要对象支持 len(x) 和 x[i]，random.choice(x) 就能随机取元素
    - 对自定义类来说，通常就是实现 __len__ 和 __getitem__
    """

    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self) -> None:
        # 用真实 list 存储数据；对外通过特殊方法暴露“序列行为”。
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self) -> int:
        # len(deck) 会触发；random.choice(deck) 内部也会间接触发它来拿长度。
        print("[__len__] called")
        return len(self._cards)

    def __getitem__(self, index: Union[int, slice]) -> Union[Card, list[Card]]:
        # deck[0] / deck[:3] 会触发；random.choice(deck) 选出随机下标 i 后也靠它取 deck[i]。
        print(f"[__getitem__] called with index={index!r}")
        return self._cards[index]


def main() -> None:
    deck = FrenchDeck()

    # 这些调用用来“看见”哪些特殊方法在什么时候被触发。
    print("len(deck):", len(deck))
    print("deck[0]:", deck[0])
    print("deck[-1]:", deck[-1])
    print("deck[:3]:", deck[:3])

    # random.choice(deck) -> 内部等价于：先 len(deck)，再取 deck[i]。
    print("choice(deck):", choice(deck))


if __name__ == "__main__":
    main()

