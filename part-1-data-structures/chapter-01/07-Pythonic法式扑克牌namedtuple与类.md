# Python风格纸牌：`namedtuple`与`class`的协作实现

---

## 一、完整代码实现
```python
import collections
from random import choice

# 1. 使用namedtuple定义单张纸牌的数据结构
Card = collections.namedtuple('Card', ['rank', 'suit'])

# 2. 使用class定义一摞纸牌的逻辑容器
class FrenchDeck:
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
```

---

## 二、`namedtuple`与`class`的配合逻辑
### 1. 角色分工
- **`Card`（namedtuple）**：
  - 作为**轻量级数据载体**，仅存储单张纸牌的`rank`（牌面）和`suit`（花色）两个属性。
  - 不可变、无自定义方法，适合表示简单数据结构，避免冗余代码。
  
- **`FrenchDeck`（class）**：
  - 作为**业务逻辑容器**，负责生成、管理整摞纸牌。
  - 通过`__init__`生成52个`Card`实例，通过`__len__`和`__getitem__`提供访问接口。

### 2. 协作流程
1. `FrenchDeck`在初始化时，遍历所有花色和牌面，调用`Card(rank, suit)`创建单张纸牌实例。
2. 所有`Card`实例被存入`self._cards`列表，形成整摞牌。
3. 用户通过`len(deck)`或`deck[position]`等操作，间接访问`Card`实例的数据。

---

## 三、命令行使用示例
### 1. 启动Python交互环境
在终端输入：
```bash
python3
```

### 2. 导入代码并使用
```python
# 导入模块（假设文件名为french_deck.py）
from french_deck import Card, FrenchDeck

# 1. 创建单张纸牌
beer_card = Card('7', 'diamonds')
print("单张纸牌:", beer_card)
# 输出: Card(rank='7', suit='diamonds')

# 2. 创建一摞纸牌
deck = FrenchDeck()

# 3. 获取纸牌数量
print("纸牌总数:", len(deck))
# 输出: 52

# 4. 访问指定位置的纸牌
print("第一张牌:", deck[0])
# 输出: Card(rank='2', suit='spades')
print("最后一张牌:", deck[-1])
# 输出: Card(rank='A', suit='hearts')

# 5. 随机抽牌
from random import choice
print("随机抽牌:", choice(deck))
# 示例输出: Card(rank='Q', suit='clubs')
```

---

## 四、设计亮点
- **`namedtuple`的优势**：用极简代码实现不可变数据类，无需手动编写`__init__`和`__repr__`。
- **`class`的优势**：通过实现`__len__`和`__getitem__`，让自定义类拥有Python内置序列的特性，符合Pythonic风格。
- **协作价值**：数据与逻辑分离，代码结构清晰，易于维护和扩展。

---

✅ **最终总结**：`namedtuple`负责定义单张纸牌的数据结构，`class`负责实现整摞纸牌的业务逻辑，二者配合实现了一个功能完整、符合Python风格的纸牌程序。

---

要不要我帮你补充**扩展功能示例**，比如添加按花色排序或筛选的方法？

