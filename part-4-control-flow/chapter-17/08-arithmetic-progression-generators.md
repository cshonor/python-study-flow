# 等差数列生成器：三种实现与核心原理（17.8）

## 本节要点

用“等差数列”这个最小问题，串起三件事：

- 生成器函数如何实现惰性序列
- `itertools` 如何用组合子快速搭出迭代器管道
- 类型提示如何写得“既实用又不过度承诺”

---

## 三种实现（同一语义，不同风格）

### 版本 1：类 + `__iter__`（教学用最直观）

- 类保存 `begin/step/end`
- `__iter__` 用 `yield` 产出项（所以它本质是个生成器函数）

### 版本 2：独立生成器函数（更轻量）

- 不需要类，直接 `def aritprog_gen(...): yield ...`
- 通常是生产中最常见的写法

### 版本 3：`itertools.count` + `takewhile`（最“管道化”）

- `count(start, step)` 生成无穷等差数列
- `takewhile(pred, it)` 在满足条件时截断（做有限序列）

---

## 为什么用 `begin + step * index`（避免累积误差）

如果每次用“上一次结果 + step”推进，在浮点场景下容易累积误差。

更稳的做法是：

- 每一项都用同一个公式重新计算：`begin + step * index`

这也是书里示例的关键细节之一。

---

## 类型提示建议

- 返回“可迭代/迭代器”优先用 `collections.abc.Iterator[T]`
- 如果你需要表达 `yield/send/return` 的三元组语义，再用 `Generator[Y, S, R]`

本节 demo 用 `Iterator[Number]`（并用 `type(begin + step)` 推导数值类型）。

---

## 配套代码

`arithmetic_progression_demo.py`：

- `ArithmeticProgression`（类）
- `aritprog_gen`（生成器函数）
- `aritprog_itertools`（itertools 版本）
- 覆盖 `int/float/Fraction/Decimal` 场景

