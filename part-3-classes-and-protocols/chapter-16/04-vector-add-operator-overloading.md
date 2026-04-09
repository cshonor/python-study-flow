# 16.4 重载向量加法运算符 `+`

## 一、语义

对**向量型**自定义类，`+` 常表示**按分量相加**（欧几里得向量加法）：

- 两个操作数按**并行迭代**对齐；较短一侧用 `0.0` 补齐缺失分量（书中示例策略：不抛长度错误）。
- **`__add__` 应返回新实例**，不原地修改 `self` 或右操作数，与内置不可变运算习惯一致。

---

## 二、实现要点：`zip_longest` 与生成器

```python
pairs = itertools.zip_longest(self, other, fillvalue=0.0)
return Vector(a + b for a, b in pairs)
```

前提是 **`Vector` 自身是可迭代的**（实现 `__iter__`，逐分量产出），右操作数 `other` 为任意**可迭代的数值序列**（元组、列表、另一个 `Vector` 等）。

---

## 三、分派与交换律：`__radd__`

表达式 `a + b` 的求值顺序：

1. 调用 `type(a).__add__(a, b)`；若得到**非** `NotImplemented`，即为结果。
2. 否则调用 `type(b).__radd__(b, a)`；同上。
3. 若仍无法处理，抛出 `TypeError`。

因此仅实现 `Vector.__add__` 时，`Vector + (10, 20, 30)` 可行（左操作数是 `Vector`），但 **`(10, 20, 30) + Vector`** 会先走 `tuple.__add__`，tuple 不支持与 `Vector` 相加时会返回 `NotImplemented`，再尝试 **`Vector.__radd__`**。

对**交换律**成立的 `+`，常见写法：

```python
__radd__ = __add__
```

注意：**减法、除法**等不满足交换律，**不能**简单 `__rsub__ = __sub__`，需单独实现反向语义。

---

## 四、类型不兼容：返回 `NotImplemented`

在 `__add__` 内若无法把 `other` 当作数值序列参与运算（例如触发 `TypeError`），应 **`return NotImplemented`**，而不是自己 `raise TypeError`（除非你想自定义错误信息）。这样解释器还能尝试反向方法，并最终给出统一的 `unsupported operand type(s) for +` 风格错误。

鸭子类型思路：**先尝试运算**，失败再交回解释器，而不是事先硬编码 `isinstance` 罗列所有合法类型（书中倾向后者配合异常）。

---

## 五、小结表

| 项目 | 说明 |
|------|------|
| `__add__` | 左操作数为 `Vector` 时的 `+` |
| `__radd__` | 右操作数为 `Vector` 时的 `+`（可与 `__add__` 等同） |
| `NotImplemented` | 本类型无法处理该组合时返回，交给对方类型或最终报错 |
| `zip_longest(..., fillvalue=0.0)` | 变长向量按 0 补齐再相加 |

配套代码：`vector_add_operator_demo.py`（该脚本在后续 16.5–16.6 中还实现了 `*` 与 `@`）。
