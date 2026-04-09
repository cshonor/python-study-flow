# 可迭代对象 vs 迭代器：协议、底层驱动与陷阱（17.4）

## 两个概念先对齐

| 概念 | 一句话 | 关键方法 |
|------|--------|----------|
| **可迭代对象（iterable）** | 能被 `iter(x)` 取出迭代器的对象 | `__iter__`（或兼容的 `__getitem__`） |
| **迭代器（iterator）** | 能被 `next(it)` 反复取值直到耗尽的对象 | `__next__` + `__iter__` |

迭代器的一个硬规则：

- **`it.__iter__()` 必须返回 `it` 自身**（保证“迭代器也是可迭代的”）

---

## `for` 循环的底层等价形式

```python
it = iter(obj)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    ...
```

要点：

- `for` 不关心 `obj` 是什么类型，只要 `iter(obj)` 能拿到迭代器即可（鸭子类型）
- 结束信号不是返回 `None`，而是抛 `StopIteration`

---

## 迭代器的核心特性（最容易踩坑的点）

- **一次性**：迭代器走完就耗尽，不能“重置”
- **可重复遍历的是 iterable**：容器/序列每次 `iter(x)` 会给你一个新的迭代器
- 判断一个对象是否是迭代器的典型方式：
  - `iter(x) is x` 往往为真（对迭代器）

---

## `Sentence`：显式迭代器版本（对比 17.2）

17.2 用的是“仅 `__getitem__` 的回退迭代”。在 17.4 里我们补一个更标准的写法：

- `Sentence.__iter__` 返回一个 **独立的迭代器对象**
- 迭代器对象实现 `__next__`（无元素时抛 `StopIteration`）与 `__iter__`

---

## 配套代码

`iterables_vs_iterators_demo.py`：

- 演示 iterable vs iterator 的差异（`iter(x) is x`、耗尽行为）
- `Sentence` + `SentenceIterator` 的显式实现
- 展示“同一个 iterator 不能二次遍历”

