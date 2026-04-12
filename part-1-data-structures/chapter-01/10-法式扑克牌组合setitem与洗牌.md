# 第 1 章后续：特殊方法、组合模式与洗牌（`__setitem__`）

> 《流畅的 Python》第 1 章后续思路：**特殊方法** + **组合**（委托给 `self._cards`），以及用 **`__setitem__`** 让序列可原地修改，从而支持 `random.shuffle`。

---

## 1. 核心知识点回顾（速览）

### `spades_high`（自定义排序键，非内置）

给每张牌算一个**整数权重**，交给 `sorted(deck, key=spades_high)` 做**升序**比较。名称可理解为「**黑桃在同点数里最大**」一类规则；**公式与拆解见 §5**。

### 组合模式（Composition）

- `FrenchDeck` **不继承** `list`，用 `self._cards`（内部 `list`）存数据。
- 通过 `__len__`、`__getitem__`、`__setitem__` 把操作**委托**给 `_cards`，让外层**表现得像序列**。

### 「洗牌」与写回

- `random.shuffle` 需要能按索引**赋值**（交换位置）。
- 没有 `__setitem__` 时，`deck[i] = ...` 不成立 → `shuffle` 通常会失败。
- 实现 `__setitem__` 并委托给 `self._cards` → `shuffle(deck)` 可正常工作。

---

## 2. `__setitem__` 和 `random.shuffle`：原理拆清楚

### 2.1 `shuffle` 在做什么？

`random.shuffle(seq)` 是**原地**随机打乱序列。核心思路是（Fisher–Yates 型）：

- 从后往前遍历下标；
- 每一步随机选一个 `j`，把 `seq[i]` 与 `seq[j]` **交换**；
- 最终得到均匀随机排列。

### 2.2 为什么需要 `__setitem__`？

交换元素本质是**按索引赋值**，例如：

```python
# shuffle 内部逻辑与下面类似（示意）
for i in range(len(seq) - 1, 0, -1):
    j = random.randint(0, i)
    seq[i], seq[j] = seq[j], seq[i]
```

`seq[i] = 新值` 会触发：

```text
seq.__setitem__(i, 新值)
```

因此：

- **没实现 `__setitem__`** → 不支持 `[]` 赋值 → `shuffle` 报错。
- **实现了 `__setitem__`**，并把赋值委托给 `self._cards[i] = value` → `shuffle` 能改内部列表，洗牌成功。

### 2.3 最小改动：加上 `__setitem__`

```python
class FrenchDeck:
    # ... 已有 __init__ / __len__ / __getitem__

    def __setitem__(self, position, value):
        self._cards[position] = value
```

```python
import random

deck = FrenchDeck()
random.shuffle(deck)
```

---

## 3. Python 的 `list` 和 `FrenchDeck` 是什么关系？

### 3.1 `list` 是什么？

`list` 是 Python 内置的**可变、有序序列**，底层可理解为**动态数组**（连续存储、按索引 O(1) 访问的常见实现）。

常见能力包括：

- 索引读：`lst[i]`
- 索引写：`lst[i] = x`
- 增删、切片、迭代等

### 3.2 `FrenchDeck` 和 `list` 的关系

`FrenchDeck` **不是** `list` 的子类，而是**组合**：

```python
self._cards = [Card(...) for ...]  # 内层就是一个 list
```

对外通过魔术方法**委托**：

| 操作 | 特殊方法 | 委托到 |
|------|----------|--------|
| `len(deck)` | `__len__` | `len(self._cards)` |
| `deck[i]` | `__getitem__` | `self._cards[i]` |
| `deck[i] = x` | `__setitem__` | `self._cards[i] = x` |

所以：`FrenchDeck` **用起来像序列**，但类型上仍是「包了一层 list + 自定义逻辑」的类。

---

## 4. 一句话总结

1. `random.shuffle` 依赖**按索引写回**，因此依赖 **`__setitem__`**。
2. 你的 `__setitem__` 通常只是把赋值交给内部的 **`list`（`self._cards`）**。
3. **`list`** 是可变动态数组；**组合 + 魔术方法** = 「像 list、又可自定义」的容器。

---

## 5. 排序键函数 `spades_high` 拆透（《流畅的 Python》思路）

这是你在代码里**自定义**的函数，**不是** Python 内置；它只负责：对每张 `Card` 返回一个数，`sorted(..., key=...)` 再按这个数从小到大排。

### 5.1 名称含义与核心逻辑

- **名称**：`spades_high` 可理解为「**同点数下黑桃最大**」（具体取决于 `suit_values` 里谁最大）。
- **目的**：规定扑克牌**全序**：先比点数，再比花色。
- **核心公式**：

```python
return rank_value * len(suit_values) + suit_values[card.suit]
```

给每张牌一个**唯一整数权重**；`sorted()` 只比较这些整数。

### 5.2 公式拆解（示例）

设 `suit_values = {'spades': 3, 'hearts': 2, 'diamonds': 1, 'clubs': 0}`，`len(suit_values) == 4`。

**第一步：`rank_value`**

`FrenchDeck.ranks.index(card.rank)`

- 在 `ranks`（`2…10, J, Q, K, A`）里找点数下标：`2 → 0`，…，`A → 12`。
- 把符号点数变成**可比的整数**。

**第二步：`rank_value * len(suit_values)`**

- 相当于**按点数“进位”**：每个点数占一段长度为 `4` 的区间。
- 保证：**任意 2 的权重都小于任意 3**，不会出现「某张 2 比某张 3 大」的交叉。

**第三步：`+ suit_values[card.suit]`**

- **同点数**下用花色微调：黑桃 3 > 红心 3 > … > 梅花 3（与表中数值一致时）。

### 5.3 升序下的直观顺序

在**升序** `sorted(deck, key=spades_high)` 中，大致是：

1. 所有 **2**：梅花 → 方块 → 红心 → 黑桃  
2. 所有 **3**：同上  
3. …  
4. 所有 **A**：同上  

（花色相对顺序由 `suit_values` 决定；上面假设梅花最小、黑桃最大。）

### 5.4 在代码中的用法

```python
# 按 spades_high(card) 的返回值升序排列
for card in sorted(deck, key=spades_high):
    print(card)
```

### 5.5 具体权重数值 demo

同目录 `10_french_deck_shuffle_demo.py` 运行时会打印例如 **2♣**、**2♠**、**A♣**、**A♠** 的 `rank_value`、花色项与最终权重，便于对照公式。

---

## 6. 完整可运行示例（逐行对照）

同目录：`10_french_deck_shuffle_demo.py`（含 `FrenchDeck`、`__setitem__`、`spades_high`、权重打印、`random.shuffle` 与 `sorted`）。

```bash
python part-1-data-structures/chapter-01/10_french_deck_shuffle_demo.py
```
