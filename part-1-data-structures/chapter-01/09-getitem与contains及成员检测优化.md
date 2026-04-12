# `__getitem__` 与 `__contains__` 核心总结

## 一、`__getitem__` 与 `__contains__` 速览

### 1. `__getitem__`

- **对应操作**：`obj[key]`（方括号取值），支持索引、切片、迭代（包括正向/反向迭代）。
- **例子**：`deck[0]`、`deck[:3]`、`for card in deck` 都会触发它。
- **注意**：和属性访问（`obj.attr`）无关；属性访问由 `__getattr__` / `__getattribute__` 负责。

### 2. `__contains__`

- **对应操作**：`item in obj`。
- **如果没实现**：Python 会自动用**顺序扫描**（遍历整个对象）来判断成员是否存在。
- **如果实现**：你可以自定义判断逻辑，比如用哈希表、二分查找等，**不一定需要顺序扫描**，可以优化效率。

### 一句话

- `__getitem__` 让你的类能用 `[]` 取值/迭代。
- `__contains__` 让你自定义 `in` 的判断逻辑，可优化性能。

---

## 二、先明确 `__contains__` 的作用

`__contains__` 是专门处理 **`in` 运算符** 的魔术方法。

- **没实现**：Python 自动**顺序扫描**（遍历整个对象）判断是否存在。
- **实现**：可自定义逻辑——既可以继续全表扫描，也可以用更高效的结构。

---

## 三、如何优化 `__contains__`？

核心思路：**降低查找的时间复杂度**，避免无谓的全表扫描。

### 例子 1：用哈希表（`set`）优化

维护与牌堆一致的集合，`in` 时查集合：

```python
class FrenchDeck:
    def __init__(self):
        self._cards = [...]
        self._card_set = set(self._cards)

    def __contains__(self, item):
        return item in self._card_set
```

通常可把「最坏 O(n) 顺序扫描」变成 **均摊 O(1)** 的哈希查找（以额外空间为代价）。

### 例子 2：有序结构 + 二分查找

数据**按同一规则有序**时，可用 `bisect`：

```python
import bisect

class SortedDeck:
    def __init__(self):
        self._sorted_cards = sorted(...)

    def __contains__(self, item):
        index = bisect.bisect_left(self._sorted_cards, item)
        return index < len(self._sorted_cards) and self._sorted_cards[index] == item
```

时间复杂度 **O(log n)**。注意：`Card` 等类型必须支持一致的全序比较，且列表排序规则与 `item` 一致。

### 若实现了 `__contains__` 仍是全表扫描？

自定义里手写 `for x in self._cards: if x == item`，与默认行为等价，**没有性能收益**，一般不推荐（除非你要顺带做副作用或特殊相等语义）。

---

## 四、总结

| 情况 | `in` 的行为 | 典型复杂度 |
|------|-------------|------------|
| 未实现 `__contains__` | 自动顺序扫描 | O(n) |
| `__contains__` + `set` | 哈希查找 | 均摊 O(1) |
| `__contains__` + 有序 + `bisect` | 二分 | O(log n) |
| `__contains__` 仍手写 for 循环 | 与默认类似 | O(n) |

---

## 五、可运行示例（扑克牌）

同目录 `getitem_contains_demo.py` 对比：

1. **仅** `__len__` + `__getitem__`：默认 `in` 顺序扫描。  
2. **`__contains__` + `set`**：近似 O(1)。  
3. **`__contains__` + 有序列表 + `bisect`**：O(log n)。  
4. **`__contains__` 手写 for**：与默认同类，作对照。

运行：

```bash
python part-1-data-structures/chapter-01/getitem_contains_demo.py
```
