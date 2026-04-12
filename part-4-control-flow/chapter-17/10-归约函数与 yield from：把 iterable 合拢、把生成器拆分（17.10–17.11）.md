# 归约函数与 `yield from`：把 iterable 合拢、把生成器拆分（17.10–17.11）

## 17.10 归约函数（reduction）：把很多值变成一个值

归约函数的共同点：

- 输入：一个 iterable
- 输出：一个结果（单个值）

### 常用归约函数速查

| 函数 | 模块 | 作用 | 关键点 |
|------|------|------|--------|
| `all(it)` | builtins | 全真才真；空迭代为 `True` | **短路**：遇到假立刻停 |
| `any(it)` | builtins | 有真就真；空迭代为 `False` | **短路**：遇到真立刻停 |
| `max(it, key=...)` | builtins | 最大值 | 可自定义 `key` |
| `min(it, key=...)` | builtins | 最小值 | 可自定义 `key` |
| `sum(it, start=0)` | builtins | 求和 | 浮点精度可用 `math.fsum` |
| `functools.reduce(fn, it, initial=...)` | functools | 自定义折叠 | 能表达很多归约，但**不自带短路** |

### `all/any` 为什么不是 `reduce` 的简单语法糖

关键差异在于：**短路**。

- `all(it)` 一旦发现一个假值，就不用再看后面
- `any(it)` 一旦发现一个真值，就不用再看后面

如果 `it` 很大、或 `it` 的每次产出都很贵（I/O/计算），短路就是实打实的性能差异。

> 归约通常只适用于有限 iterable；对无限迭代器要先 `islice/takewhile` 截断。

---

## 17.11 `yield from`：把“产出”委托给子生成器

`yield from` 可以把一个生成器的工作委托给另一个 iterable/生成器：

```python
for x in sub:
    yield x
```

等价于：

```python
yield from sub
```

但 `yield from` 不只是省几行：

- 它会自动转发 `next/send/throw`（在需要 `.send()` 的协程式生成器里尤其重要）
- 它会捕获子生成器的 `return value`（也就是 `StopIteration.value`）

---

## 典型用法

### 1) 重写 `chain`

```python
def chain(*iterables):
    for it in iterables:
        yield from it
```

### 2) 递归遍历树状结构

```python
def tree(cls, level=0):
    yield cls.__name__, level
    for sub in cls.__subclasses__():
        yield from tree(sub, level+1)
```

---

## 配套代码

`10_reduction_and_yield_from_demo.py`：

- `all/any` 的短路演示（用“带副作用的生成器”可视化）
- `reduce` 做自定义归约
- `yield from` 实现 `chain`
- `yield from` 捕获子生成器 `return` 值
- `yield from` 递归遍历 `BaseException` 的继承树（截断输出）

