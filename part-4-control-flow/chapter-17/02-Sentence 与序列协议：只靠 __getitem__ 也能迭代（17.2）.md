# `Sentence` 与序列协议：只靠 `__getitem__` 也能迭代（17.2）

## `Sentence` 的定位

用一个极小的类，说明 Python 的一个“协议式”规则：

- **实现 `__getitem__` 就足以让对象可迭代**（当对象没有 `__iter__` 时）

---

## 序列协议的迭代回退规则

当解释器看到：

```python
for x in obj:
    ...
```

它会做：

1. 先尝试 `iter(obj)` → 查找 `obj.__iter__`
2. 若没有 `__iter__`，但有 `__getitem__`：解释器会用 **0,1,2...** 的索引不断调用 `__getitem__`
3. 直到 `__getitem__` 抛出 **`IndexError`**，迭代结束

这就是为什么很多“只实现下标访问”的对象也能被 `for`、`list()` 消费。

---

## `Sentence`（最小实现）

核心方法：

| 方法 | 作用 |
|------|------|
| `__getitem__` | 下标访问；也触发“可迭代回退” |
| `__len__` | 长度（非必需，但完整序列体验更好） |
| `__repr__` | 友好打印（用 `reprlib.repr` 防刷屏） |

正则提词：

- `RE_WORD = re.compile(r'\w+')`
- `RE_WORD.findall(text)` 一次性得到词列表 `words`

---

## 序列协议 vs 迭代器协议

| 对比点 | 序列协议（`__getitem__`） | 迭代器协议（`__iter__` + `__next__`） |
|--------|---------------------------|----------------------------------------|
| 实现复杂度 | 最小 | 更明确、更可控 |
| 适用 | 需要下标/切片、或“简单可迭代” | 懒加载、复杂遍历、一次性流式迭代 |
| 迭代停止 | `IndexError` | `StopIteration` |

---

## 配套代码

`02_sentence_sequence_protocol_demo.py`：

- `Sentence`（仅 `__getitem__`）→ 证明 `for` / `list()` 可用
- `SentenceIter`（显式 `__iter__`）→ 对比“更标准的可迭代实现”

