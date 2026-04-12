# `iter()` 与 Python 迭代的底层规则（17.3）

## `for x in obj` 的第一步：`iter(obj)`

所有迭代最终都绕不开一件事：

- `for` 会先调用 `iter(obj)` 拿到一个 **迭代器**，再不断取“下一个元素”。

---

## `iter(x)` 的三段回退规则

当你执行 `iter(x)`，解释器会按优先级尝试：

1. **`x.__iter__`**：存在就调用它，得到迭代器（现代标准）
2. **`x.__getitem__`**：若无 `__iter__` 但有 `__getitem__`，则按索引 `0,1,2...` 调用直到 `IndexError`（历史兼容）
3. 否则抛 **`TypeError`**：对象不可迭代

---

## 鸭子类型：可迭代不等于 `isinstance(x, Iterable)`

Python 在“能不能迭代”上更信奉鸭子类型：

- 只要 `iter(x)` 能工作 → 就能迭代

一个常见陷阱：

- **只实现 `__getitem__` 的对象**通常能被 `for`/`list()` 消费
- 但它可能 **不被** `isinstance(x, collections.abc.Iterable)` 认出来（因为 `Iterable` 主要看 `__iter__`）

因此判断“是否可迭代”最可靠的方法往往是：**直接 `iter(x)` 试一下**（必要时捕获 `TypeError`）。

---

## `iter()` 的第二种形态：`iter(callable, sentinel)`

双参数形式返回一个 “callable_iterator”：

- 反复调用 `callable()` 获取值
- 当返回值 **等于** `sentinel` 时停止迭代（抛 `StopIteration`）

常见用途：

- 按块读文件（直到 `b''`）
- 轮询/采样（直到某个哨符）
- 掷骰子/随机试验（直到某个结果）

如果 callable 需要参数，通常用 `functools.partial` 变成“无参 callable”。

---

## 配套代码

`03_iter_builtin_demo.py`：

- `__iter__` 优先于 `__getitem__` 的演示
- 只实现 `__getitem__` 仍可迭代，但可能不属于 `abc.Iterable`
- `iter(callable, sentinel)`：掷骰子直到 1；按块读文件直到空字节

