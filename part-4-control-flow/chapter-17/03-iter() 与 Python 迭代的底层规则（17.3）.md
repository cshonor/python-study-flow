# `iter()` 与 Python 迭代的底层规则（17.3）

## 新手大白话：`iter()` 到底在干嘛？

### 1）先记住一句

几乎所有 **`for x in obj`** 的开场，等价于要先拿到迭代器：

```python
it = iter(obj)
# 然后再反复 next(it) ……直到结束
```

所以：**`iter(obj)` 就是「问 Python：这东西怎么一个一个往外吐？」**

### 2）`iter(obj)` 的三步底层规则（按顺序试）

Python 会**按顺序试**，不是随机猜：

1. **有 `__iter__` 吗？**  
   有 → 走**现代标准路径**：调用它，拿到真正的迭代器。

2. **没有 `__iter__`，但有 `__getitem__` 吗？**  
   有 → 走**序列回退路径**：用 **`0, 1, 2, …`** 当下标一直取，直到 **`IndexError`** 停（这就是你在 **[17.2](<./02-Sentence 与序列协议：只靠 __getitem__ 也能迭代（17.2）.md>)** 看到的那条「旧式序列」兼容逻辑）。

3. **两个都没有** → **`TypeError`**：**不是可迭代对象**。

### 3）超级重要的坑（新手必看）

**只写 `__getitem__`、不写 `__iter__` 的对象：**

- **`for` / `list()` 往往照样能用**（走回退路径）。  
- 但 **`isinstance(x, collections.abc.Iterable)` 可能是 `False`**，因为 **`Iterable` 抽象基类主要认 `__iter__`**，不认「我有 `__getitem__`」这种老协议。

所以更「鸭子类型」的做法是：**别光靠 `isinstance` 猜**，需要时**直接试 `iter(x)`**（再按需捕获 **`TypeError`**）。

### 4）`iter()` 还有第二种用法：`iter(函数, 停止值)`

```python
import random


def dice() -> int:
    return random.randint(1, 6)


# 一直掷骰子，直到掷出 1 就停（1 本身不会出现在迭代结果里）
for num in iter(dice, 1):
    print(num)
```

直觉：**反复调用无参函数**，返回值**一旦等于哨兵 `sentinel`**，迭代结束。

工程里常见兄弟用法：**按块读文件直到空字节**、**轮询直到某个状态**；若 callable 需要参数，常用 **`functools.partial`** 先绑成「无参函数」（见 **`03_iter_builtin_demo.py`**）。

### 5）新手三句终极总结

1. **`for` 的第一步语义上就是 `iter(obj)`**（再 `next`）。  
2. **`iter` 先试 `__iter__`，不行再试 `__getitem__` 回退**。  
3. **只写 `__getitem__` 也可能能迭代，但别用错 `isinstance` 判断**。

### 6）一页复习：`17.2` + `17.3` 怎么一起看？

- **17.2**：讲清「**为什么只写 `__getitem__` 也能 `for`**」。  
- **17.3**：讲清「**`iter()` 在两种协议之间怎么选**，以及 **`iter(callable, sentinel)`**」。

### 7）完整可运行对照

仓库脚本 **`03_iter_builtin_demo.py`**（`__iter__` 优先、`__getitem__` 回退、`isinstance` 陷阱、`iter(d6, 1)`、按块读文件）：

```bash
python part-4-control-flow/chapter-17/03_iter_builtin_demo.py
```

---

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

