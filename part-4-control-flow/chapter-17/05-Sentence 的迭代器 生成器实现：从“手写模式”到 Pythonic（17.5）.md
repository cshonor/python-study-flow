# `Sentence` 的迭代器/生成器实现：从“手写模式”到 Pythonic（17.5）

## 新手大白话：`Sentence` 三种写法 + 一个大坑

### 1）本节要干嘛？

同一个目标：**让 `Sentence` 能被 `for` 按单词遍历。**

给你 **3 种写法**，从「笨但清楚」→「最常用」→「最短」：

1. **手写迭代器类**（显式 `__next__`，最长）  
2. **在 `__iter__` 里用 `yield` 的生成器函数**（⭐ 多数时候最 Pythonic）  
3. **`__iter__` 里 `return (… for …)` 生成器表达式**（一行包一层）

---

### 2）最重要结论（先背）

**不要让「可迭代的 `Sentence` 自己」当迭代器！**  
也就是：**别写 `def __iter__(self): return self` 再配 `__next__`**——否则对象往往变成**一次性**：走一遍就把自己耗尽了，第二次 `for` 啥也没有。

**正确姿势：**  
**每次**进入 `__iter__`，都返回一个**新的**迭代器对象，或一个**新的**生成器（生成器函数 / 生成器表达式每次调用都会新建）。

---

### 3）版本 1：手写迭代器（最机械、最直观）

自己维护索引，自己在末尾抛 **`StopIteration`**（或 `IndexError` 转 **`StopIteration`**）。

```python
class Sentence:
    def __init__(self, text: str) -> None:
        self.words = text.split()

    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words: list[str]) -> None:
        self.words = words
        self.index = 0

    def __next__(self) -> str:
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return word
```

下面为阅读简单用 **`split()`**；书里/仓库配套脚本常用 **`re.findall` 提词**（见 **`05_sentence_iterator_generator_demo.py`**）。

---

### 4）版本 2：生成器函数（⭐ 最推荐）

只要 **`yield`**，解释器帮你管「状态机 + `__next__`」：

```python
class Sentence:
    def __init__(self, text: str) -> None:
        self.words = text.split()

    def __iter__(self):
        for word in self.words:
            yield word
```

**直觉**：`__iter__` 变成「小生成器工厂」——每次 `for s in Sentence(...)` 都会拿到**新的生成器迭代器**。

---

### 5）版本 3：生成器表达式（极简）

```python
class Sentence:
    def __init__(self, text: str) -> None:
        self.words = text.split()

    def __iter__(self):
        return (word for word in self.words)
```

逻辑复杂时，可读性可能不如版本 2 的显式 `for … yield`。

---

### 6）超级大坑（千万别犯）

```python
# ❌ 反例：可迭代对象自己当自己的迭代器
class SentenceBad:
    def __init__(self, text: str) -> None:
        self.words = text.split()
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        try:
            w = self.words[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return w
```

后果：**第一次 `list(s)` 走完后，索引已经到头**；同一个 `s` 再 `list(s)` 往往是 **`[]`**。

---

### 7）新手三句终极总结

1. **`yield` ≈ 让 Python 帮你写迭代器**（版本 2 最省心）。  
2. **`__iter__` 每次返回「新东西」**，`Sentence` 本体才能被反复遍历。  
3. **`return self` + `__next__` 在 `Sentence` 上** ≈ 把句子变成**一次性筷子**。

---

### 8）一段复制就能跑（含 3 种好写法 + 1 个坏示范）

下面整段保存为 `demo_175_min.py` 或在 REPL 粘贴即可（**按空格分词**）：

```python
text = "hello world python"


class V1:
    def __init__(self, t: str) -> None:
        self.words = t.split()

    def __iter__(self):
        return V1It(self.words)


class V1It:
    def __init__(self, words: list[str]) -> None:
        self.words = words
        self.i = 0

    def __next__(self) -> str:
        if self.i >= len(self.words):
            raise StopIteration
        w = self.words[self.i]
        self.i += 1
        return w


class V2:
    def __init__(self, t: str) -> None:
        self.words = t.split()

    def __iter__(self):
        for w in self.words:
            yield w


class V3:
    def __init__(self, t: str) -> None:
        self.words = t.split()

    def __iter__(self):
        return (w for w in self.words)


class Bad:
    def __init__(self, t: str) -> None:
        self.words = t.split()
        self.i = 0

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.i >= len(self.words):
            raise StopIteration
        w = self.words[self.i]
        self.i += 1
        return w


def twice(name: str, s) -> None:
    print(name, list(s), "| again:", list(s))


twice("V1", V1(text))
twice("V2", V2(text))
twice("V3", V3(text))
twice("Bad", Bad(text))
```

仓库里的「书风格」完整对照（`SentenceClassic` / `SentenceGenFunc` / `SentenceGenExpr` / `SentenceBadIterator` + **`RE_WORD`**）：

```bash
python part-4-control-flow/chapter-17/05_sentence_iterator_generator_demo.py
```

---

## 本节要解决什么

同一个需求：让 `Sentence` 能被 `for`/`list()` 遍历单词。

我们用 3 种版本对比：

1. **经典迭代器模式**：`Sentence.__iter__` 返回自定义 `SentenceIterator`
2. **生成器函数**：`Sentence.__iter__` 里 `yield`
3. **生成器表达式**：`Sentence.__iter__` 返回一个生成器对象

---

## 版本 1：经典迭代器模式（显式 `__next__`）

特点：

- 最“机械”，但最直观：你清楚知道状态（索引）怎么推进
- 代码量最大，需要维护索引并抛 `StopIteration`

---

## 版本 2：生成器函数（推荐的 Python 风格）

`yield` 帮你做了两件事：

- 自动保存/恢复迭代状态（无需手动索引）
- 自动实现迭代器协议（生成器对象自带 `__iter__`/`__next__`）

当迭代逻辑只是“按顺序产出元素”时，这通常是最优解。

---

## 版本 3：生成器表达式（更短，但别过度）

当 `__iter__` 只是“把一个现成 iterable 包一下”时，可以直接返回生成器表达式：

- 写法很短
- 但复杂逻辑时可读性可能不如显式 `for ...: yield ...`

---

## 常见误区：让可迭代对象本身当迭代器

反例（不要这么做）：

- `Sentence` 同时实现 `__iter__` 和 `__next__`，并让 `__iter__` 返回 `self`

问题：

- `Sentence` 会变成**一次性**对象：第一次遍历耗尽后，再遍历拿不到数据

正确做法：

- `__iter__` 每次都返回**新的迭代器对象**（迭代器类或新的生成器）

---

## 配套代码

`05_sentence_iterator_generator_demo.py`：

- 三种版本的 `Sentence` 实现
- 一个“坏例子”展示“一次性耗尽”的坑
- 输出对比：`list(s)` 两次的结果是否一致

