# `Sentence` 与序列协议：只靠 `__getitem__` 也能迭代（17.2）

## 新手大白话：只写 `__getitem__` 就能 `for`

### 1）背一句就够

在 Python 里：**只要实现了 `__getitem__`，且没有自己的 `__iter__` 来“抢活”**，你的对象就常常能**直接被 `for` 遍历**——不必先写一整套 `__iter__` / `__next__`。

（更严谨：**迭代器协议**仍是底层真相；这里说的是解释器为「旧式序列」留的**回退路径**。）

### 2）`for 词 in 句子` 时，解释器在干什么（超通俗三步）

当你写：

```python
for x in obj:
    ...
```

Python 会大致按这个顺序想办法：

1. **先找 `__iter__`**：有就走标准「可迭代对象 → 迭代器」流程。  
2. **没有 `__iter__`，但有 `__getitem__`**：就用 **`0, 1, 2, …`** 当索引，一直调用 **`__getitem__(i)`**。  
3. **直到 `__getitem__` 抛出 `IndexError`**：认为迭代结束。

这就叫：**序列协议的迭代回退**（书里常叫「序列协议 / 旧式迭代」那条线）。

### 3）最小可复制示例（与配套脚本一致）

下面与 **`02_sentence_sequence_protocol_demo.py`** 里的 **`Sentence`** 同一思路（`__repr__` 里用原文 `text`，方便对照书与调试）：

```python
import re
import reprlib

RE_WORD = re.compile(r"\w+")


class Sentence:
    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    # 只写这一个“魔法方法”，就能驱动 for 回退迭代
    def __getitem__(self, index: int):
        return self.words[index]

    def __len__(self) -> int:
        return len(self.words)

    def __repr__(self) -> str:
        return f"Sentence({reprlib.repr(self.text)})"
```

### 4）拿来就用

```python
s = Sentence("hello world python")

for word in s:
    print(word)

print(list(s))
print(s[0])
```

**上面全部能跑**：你没有手写 `__iter__` / `__next__`，但 **`for` / `list()` / `[]`** 都成立。

### 5）两个协议怎么选（新手版）

| | **序列回退（`__getitem__`）** | **标准迭代器（`__iter__` + `__next__`）** |
|---|-------------------------------|------------------------------------------|
| 代码量 | 往往很少 | 多一些，但更“显式” |
| 停止信号 | **`IndexError`** | **`StopIteration`**（在迭代器协议里） |
| 典型用途 | 像列表一样支持下标、教学演示 | 惰性流、复杂状态、要完全掌控迭代过程 |

配套里还有一个 **`SentenceIter`**：走显式 **`__iter__`**，可以和 **`Sentence`** 对照跑（见脚本）。

### 6）新手必记三句话

1. **`__getitem__` 是很多人接触到的第一把「可迭代钥匙」**（在**没有** `__iter__` 的前提下）。  
2. **`for` 不是魔法**：底层还是 **`iter` / `next`** 与异常收束；回退路径只是帮你少写样板代码。  
3. **工程里**：需要惰性、复杂遍历或明确迭代器语义时，再升级到 **`__iter__`/`__next__` 或生成器**（见后文 **05** 起）。

### 7）完整可运行工程版

仓库已准备好一份可直接运行的脚本（含 **`Sentence` + `SentenceIter` 对照**）：

- **`02_sentence_sequence_protocol_demo.py`**

在仓库根目录：

```bash
python part-4-control-flow/chapter-17/02_sentence_sequence_protocol_demo.py
```

---

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

