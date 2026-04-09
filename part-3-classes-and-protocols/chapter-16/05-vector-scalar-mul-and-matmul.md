# 16.5–16.6 标量乘法 `*` 与矩阵乘法 `@`（点积）

## 16.5 标量乘法 `*`（element-wise × 标量）

语义：**每个分量乘以同一标量**，得到新 `Vector`，不修改原对象。

- 实现：`__mul__(self, scalar)` 内将标量转为 `float`（或接受 `float(...)` 成功的类型，如 `int`、`bool`、`fractions.Fraction`）。
- 转换失败（如传入另一个向量、字符串）→ **`return NotImplemented`**，便于解释器尝试反向方法或最终报错。注意 `float("x")` 抛出 **`ValueError`**，通常与 `TypeError` 一并捕获。
- 交换律：`x * v` 走 **`__rmul__`**；对可交换的标量乘可写 **`__rmul__ = __mul__`**。

---

## 16.6 矩阵乘法 `@`（两向量点积）

Python 3.5+ 中缀 `@` 对应 **`__matmul__` / `__rmatmul__`**。对两个**长度相同**的一维数值序列，语义为点积：

\[
\sum_i a_i b_i
\]

- 长度不一致：应 **`raise ValueError`**（书中风格）或借助 **`zip(..., strict=True)`**（3.10+）在遍历时发现长度不同再转为明确错误。
- 左操作数非可迭代、或与标量做 `@`：返回 **`NotImplemented`**，最终 `TypeError`。
- **`__rmatmul__`**：在 `[1,2,3] @ v` 这类表达式中，列表无合适的 `__matmul__` 时，会落到 **`v.__rmatmul__(列表)`**；实现上常 **`return self @ other`**（点积可交换）。

---

## `*` 与 `@` 的分工

| 运算符 | 方法 | 典型语义 |
|--------|------|----------|
| `*` | `__mul__` / `__rmul__` | 向量 × **标量**（逐分量缩放） |
| `@` | `__matmul__` / `__rmatmul__` | 向量 · 向量（**点积**，结果为标量） |

避免用 `*` 表示点积，以免与 NumPy 等生态中“逐元素乘”的习惯混淆；`@` 与 PEP 465 及线性代数记号一致。

---

## 实现提示（3.10+）

- **`zip(self, other, strict=True)`**：在遍历时强制等长，捕获 `ValueError` 后改抛更贴切的 `ValueError("@ requires ...")`。
- 与 **`collections.abc.Sized` / `Iterable`**：用于分支判断（生成器无长度时需依赖 `strict` 或完全消费才能发现不等长）。

配套 runnable：`vector_add_operator_demo.py`（在 16.4 的 `Vector` 上扩展了 `*` 与 `@`）。其中 `@` 使用了 **`zip(..., strict=True)`**，需要 **Python 3.10+**。
