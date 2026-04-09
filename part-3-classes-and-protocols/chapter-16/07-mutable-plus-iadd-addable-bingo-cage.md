# 可变对象的 `+` 与 `+=`：`AddableBingoCage`（示例 16-19）

## 不可变 vs 可变（本章两条线）

| 行为 | 值对象（如 `Vector`） | 可变容器（如 `AddableBingoCage`） |
|------|----------------------|-----------------------------------|
| **`a + b`（`__add__`）** | 返回**新**实例，不改 `a`、`b` | 同样返回**新**实例，不修改左右操作数 |
| **`a += b`（`__iadd__`）** | 通常**无** `__iadd__` → 退化为 `a = a + b`，**重新绑定** | 实现 **`__iadd__`**：**原地**修改 `a`，并 **`return self`** |

要点：**中缀 `+` 不应对左操作数做原地修改**；是否在 `+=` 里原地改，由是否提供 `__iadd__` 决定。

---

## `AddableBingoCage` 设计（书中思路）

- **`__add__(self, other)`**  
  - 仅当 `isinstance(other, Tombola)`：用 `self.inspect() + other.inspect()` 得到合并后的有序元组（`inspect` 会暂时抽空再装回，具体顺序/洗牌细节见 `BingoCage.load`）。  
  - 构造 **`AddableBingoCage(...)`** 返回。  
  - 否则 **`return NotImplemented`**（例如 `cage + [1,2]` → 最终 `TypeError`）。

- **`__iadd__(self, other)`**  
  - 若 `other` 是 **`Tombola`**：`other_iterable = other.inspect()`。  
  - 否则尝试 **`iter(other)`**（列表、元组、字符串等）；失败则 **`TypeError`**，提示需为 `Tombola` 或可迭代对象。  
  - **`self.load(other_iterable)`** 就地装入，**`return self`**。

`+` 的类型约束可以**更严**（只接另一种 `Tombola`）；`+=` 常**更宽**（类似 `list.extend` 接受任意可迭代对象），便于“往里倒一批元素”。

---

## 何时需要 `__radd__`

若 `__add__` **只**处理“本类 + `Tombola`”，且不希望 `list + cage` 等成立，可以不实现 `__radd__`。需要与内置类型对称时，再按分派规则补反向方法。

---

## 配套代码

`addable_bingo_cage_demo.py`：内嵌精简版 `Tombola` / `BingoCage`（与 `chapter-13/goose_typing_abcs_demo.py` 同源 API），可直接运行。
