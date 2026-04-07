# 插入或更新可变值：词索引与 `get` / `setdefault` / `defaultdict`（§3.4.3）

> **本篇定位**：《流畅的 Python》**3.4.3**：用 `dict` 存**可变值**（如 `list`）时，在「缺键要初始化」场景下对比 **`dict.get`**、**`setdefault`**、**`defaultdict`**；示例为**单词 → 出现位置列表**。  
> **相关**：三种映射总表见 `06-dict-defaultdict-ordereddict-api.md`。  
> **配套脚本**：`zen_word_index_demo.py`（内存中的《Python 之禅》节选，无需单独 `zen.txt`）。

---

## 一、场景

- **输入**：多行文本。  
- **输出**：`dict[str, list[tuple[int, int]]]`，键为词，值为 **`(行号, 列号)`** 列表（列号从 1 起与书中一致时，对 `match.start()` **+1**）。  
- **难点**：词**首次**出现要挂**新列表**；之后在同一列表上 **`append`**。

---

## 二、示例 3-4 风格：`get` + 写回

```python
occurrences = index.get(word, [])
occurrences.append(location)
index[word] = occurrences
```

### 优点

- 易读；不会 `KeyError`。

### 缺点

- **三步**：取列表 → 改列表 → **写回**（键已存在时写回仍执行）。  
- **默认实参求值**：`get(word, [])` 在**每次调用**时都会先对第二个实参求值，**新建一个 `[]`**；若键已存在，`get` 返回已有列表，**刚建的那个空列表会被丢弃**。  
- 同理：**`setdefault(word, [])` 里的 `[]` 也会在每次调用时被求值**（见 §四与脚本）。  
- 若希望「**仅缺键才分配**」：`defaultdict(list)`（§五）。

---

## 三、示例 3-5 风格：`setdefault` 一行（书中最常推荐的写法）

```python
WORD_RE = re.compile(r"\w+")
index: dict[str, list[tuple[int, int]]] = {}

with open(sys.argv[1], encoding="utf-8") as fp:
    for line_no, line in enumerate(fp, 1):  # 行号从 1 起，便于人类阅读
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index.setdefault(word, []).append(location)

for word in sorted(index, key=str.upper):
    print(word, index[word])
```

### 与「显式分支」等价（语义上）

```python
if word not in index:
    index[word] = []
index[word].append(location)
```

`setdefault` 把「缺则建、再取引用、再改」收进**一次方法调用**，省去显式 **`index[word] = …` 写回**，也比 §二 少一步。

### 相对 §二 的优势

- **无单独写回**：`get` 三行里第三步在键已存在时仍是多余赋值。  
- **代码一行**：适合词索引、分组累加等高频路径。

---

## 四、性能与「查找次数」（教学向）

下表是**阅读代码时的直觉步数**，不是 CPython 字节码级微基准；解释器可能对 `in`、下标等做优化。

| 方案 | 典型代码形态 | 直觉 |
| :--- | :--- | :--- |
| `if key not in d` + 赋值 + `append` | 显式分支 | 多次名字查找 / 方法调用 |
| `get` + `append` + 写回 | §二 | `get` 一次 + **写回**一次 |
| `setdefault(k, []).append(…)` | §三 | **一次** `setdefault`（内部完成缺键插入或返回值） |
| `defaultdict(…); d[k].append` | §五 | **`d[k]`** 一次；缺键时才跑工厂 |

**重要**：`setdefault(k, [])` 与 `get(k, [])` 一样，**每次调用都会对第二个实参 `[]` 先求值**；键已存在时仍会多分配一个随即丢弃的空列表。若极端在意分配次数，优先 **`defaultdict(list)`**（工厂仅在缺键时调用，见 `zen_word_index_demo.py` §3）。

---

## 五、`defaultdict` 版本

```python
from collections import defaultdict

index: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
# ...
index[word].append(location)
```

- **缺键**时由 `defaultdict` 插入 `list()`；**键已存在**时不再调用工厂。  
- 后续章节（书中 **3.5** 等）会对 `collections` 做系统展开；此处作为 §3.4.3 的**自然延伸**。

---

## 六、避坑与选型

### 1. 不要共用同一个可变默认值

```python
# 错：所有键共享同一列表对象
shared: list[int] = []
d.setdefault(k, shared).append(v)

# 对：每次用新列表（`[]` 字面量）或 `defaultdict(list)`
d.setdefault(k, []).append(v)
```

### 2. `get` vs `setdefault`

- **只读**、不想插入键：用 **`get`**。  
- **要改可变值**（追加、原地更新）：用 **`setdefault`** 或 **`defaultdict`**。

### 3. `setdefault` vs `defaultdict`

- 已有普通 **`dict`**、偶尔需要默认值：**`setdefault`**。  
- **大量**缺键、固定用 `list`/`int` 等工厂：**`defaultdict`** 往往更清晰，且可避免 §四所述的 **`[]` 反复求值**（在键已存在时）。

---

## 七、实现细节

- **`enumerate(fp, 1)`**：行号从 **1** 起；若与 §二 其它示例用 `enumerate(fp)`（从 0 起）混用，注意**同一项目内统一**。  
- **`sorted(index, key=str.upper)`**：传入 **`str.upper` 方法对象**，排序键为单词的大写形式，实现**大小写不敏感**的字典序；函数作一等值传递详见原书后续章节。  
- **快速失败**：`d[k]` 缺键抛 **`KeyError`**；`get`/`setdefault`/`defaultdict` 是不同默认策略。

---

## 八、对比总表

| 写法 | 典型代码 | 备注 |
| :--- | :--- | :--- |
| `get` + 写回 | 三行 | 冗长；写回冗余；`[]` 每次求值 |
| `setdefault` | `d.setdefault(k, []).append(v)` | 一行；`[]` 每次仍求值 |
| `if` + 赋值 + `append` | 显式分支 | 清晰；步数多 |
| `defaultdict(list)` | `d[k].append(v)` | 缺键才 `list()` |

---

## 九、可运行对照

见 `zen_word_index_demo.py`（三种建索引、`get`/`setdefault` 默认实参求值、`defaultdict` 工厂调用次数）。

**下一篇**：§3.5 **`defaultdict` 与 `__missing__`** 见 `08-defaultdict-and-missing.md`。
