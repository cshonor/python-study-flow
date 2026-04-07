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

- **三步**：取列表 → 改列表 → 写回（键已存在时写回仍执行）。  
- **默认实参求值**：`get(word, [])` 在**每次调用**时都会先对第二个实参求值，**新建一个 `[]`**；若键已存在，`get` 返回已有列表，**刚建的那个空列表会被丢弃**（徒增分配与 GC 压力）。  
  - 同理：`setdefault(word, [])` 里的 **`[]` 也会在每次调用时被求值**（见脚本验证）。  
- 真正在「缺键才建列表」上更省的是 **`defaultdict(list)`**：只有 **`__getitem__`** 路径上缺键才会调用 **`default_factory`**，已存在键**不会**多造空列表。

---

## 三、`setdefault` 一行式

```python
index.setdefault(word, []).append(location)
```

- 去掉显式写回，逻辑更紧凑。  
- 仍注意：若写成 **`setdefault(word, [])`**，**`[]` 每次调用都会求值**；书中常用写法在工程上仍优于三行 `get`，但若极端在意分配，可对 `defaultdict` 或**自定义工厂**再优化。

---

## 四、`defaultdict` 版本

```python
from collections import defaultdict

index: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
# ...
index[word].append(location)
```

- **缺键**时由 `defaultdict` 插入 `list()`；**键已存在**时不再调用工厂。  
- 需 `from collections import defaultdict`。

---

## 五、对比小结

| 写法 | 典型代码 | 备注 |
| :--- | :--- | :--- |
| `get` + 写回 | 三行 | 冗长；`[]` 每次求值 |
| `setdefault` | 一行 `setdefault(..., []).append(...)` | 简洁；`[]` 每次仍求值 |
| `defaultdict(list)` | `idx[word].append(...)` | 缺键才 `list()` |

---

## 六、实现细节提示

- **`enumerate(fp)`**：默认行号从 **0** 起；若要「人类行号从 1」，用 **`enumerate(fp, 1)`** 并相应理解「位置」语义。  
- **排序**：`sorted(index, key=str.upper)` 为**大小写不敏感**按键排序；区分大小写则用 `sorted(index)`。  
- **快速失败**：`d[k]` 对缺键抛 **`KeyError`**，促使显式处理默认值；`get`/`setdefault`/`defaultdict` 是不同层面的默认策略。

---

## 七、可运行对照

见 `zen_word_index_demo.py`（三种建索引方式、`get`/`setdefault` 默认实参求值次数示意、`defaultdict` 工厂调用次数示意）。
