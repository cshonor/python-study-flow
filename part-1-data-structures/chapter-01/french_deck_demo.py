import collections
from random import choice

# 1. 用namedtuple定义单张纸牌的数据结构
Card = collections.namedtuple('Card', ['rank', 'suit'])

# 2. 用普通类定义一摞纸牌的逻辑容器
class FrenchDeck:
    # 定义纸牌的rank和suit
    # rank: 2-10, J, Q, K, A
    # suit: spades, diamonds, clubs, hearts
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        # 生成52张纸牌，存储为Card实例的列表
        self._cards = [Card(rank, suit) for suit in self.suits
                      for rank in self.ranks]

    def __len__(self):
        # 让len()函数可以直接作用于FrenchDeck实例
        return len(self._cards)

    def __getitem__(self, position):
        # 让实例支持索引、切片操作
        return self._cards[position]

# 3. 示例用法
if __name__ == "__main__":
    # 创建一张7方块纸牌
    beer_card = Card('7', 'diamonds')
    print("单张纸牌示例：", beer_card)
    
    # 创建一摞纸牌
    deck = FrenchDeck()
    print("\n一摞纸牌的数量：", len(deck))
    
    # 访问指定位置的纸牌
    print("第一张牌：", deck[0])
    print("最后一张牌：", deck[-1])
    
    # 随机抽一张牌
    print("随机抽牌：", choice(deck))