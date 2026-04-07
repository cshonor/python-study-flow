# `list.sort()` 与 `sorted()`：原地排序 vs 新列表

> **本篇定位**：《流畅的 Python》第 2 章中关于**两种排序入口**的对比：`list` 专用、原地、返回 `None`；以及适用于任意可迭代对象、返回新 `list` 的内置函数。  
> **相关**：序列协议与对象模型见 `02-container-vs-flat-sequences.md`；第 1 章里按自定义 `key` 排序扑克见 `../chapter-01/10-french-deck-composition-setitem-shuffle.md`。  
> **配套脚本**：`list_sort_vs_sorted_demo.py`。

---

## 一、核心对照

| 特性 | `list.sort()` | 内置函数 `sorted()` |
| :--- | :--- | :--- |
| **操作类型** | **原地**排序（in-place） | **新建**一个 `list` |
| **返回值** | **`None`** | 排序后的**新列表** |
| **适用对象** | 仅 **`list`** | **任意可迭代对象**（`list`、`tuple`、`str`、`dict` 的键/值视图等） |
| **对原数据** | **修改**原列表 | 一般**不修改**输入（不可变输入自然不变） |

---

## 二、共同参数：`reverse` 与 `key`

两者都支持：

- **`reverse=False`**：默认升序；`True` 时降序（在「按 `key` 投影后的结果」上取反序，而不是对 `key` 本身取反）。
- **`key=None`**：单参数函数，对每个元素先求**排序键**，再按键比较（**不修改**原元素）。

常见写法：`key=len`、`key=str.lower`、按属性/字段：`key=lambda x: x.name` 或 `operator.attrgetter("name")`。

---

## 三、为什么原地方法返回 `None`？

Python 约定：**会修改接收者自身**的列表方法（如 `append`、`extend`、`sort`、`clear`）返回 **`None`**，避免让人误以为「拿到了一个新列表」。因此不要写：

```python
a = data.sort()  # 错误：a 是 None，原排序结果在 data 里
```

同类：**`random.shuffle(seq)`** 也是原地打乱，返回 `None`。

`sorted(x)` 则**不依赖**可变序列，适合管道式写法：`sorted(..., key=...)` 再继续链式处理。

---

## 四、`key` 进阶（实战向）

### 1. `operator.itemgetter` / `attrgetter`

- 字典列表：按字段排 — `sorted(rows, key=itemgetter("name"))`；多字段 — `itemgetter("last", "first")`（等价于先按 `last` 再按 `first` 的元组键）。
- 对象列表：按属性排 — `sorted(users, key=attrgetter("score"))`；多属性 — `attrgetter("dept", "name")`。

比手写 `lambda` 往往更快、更可读（名字即文档）。

### 2. 多关键字：返回**元组**作为键

排序键支持**序列比较**（逐元素、短路）：先比第一维，相同再比第二维……

```python
sorted(items, key=lambda x: (x.priority, x.name.lower()))
```

需要「某一维降序、其余升序」时，常对该维取反或用 `functools.cmp_to_key`（少用）；更简单的是**排两次**（稳定排序，见下）或拆成两步。

### 3. 稳定排序（stable sort）

Python 的排序（Timsort）是**稳定**的：键相等时，**保持原有相对顺序**。可利用这一点做「主键 / 次键」：**先按次键排，再按主键排**。

### 4. 与生态中其它 `key`

`min` / `max`、`heapq.nlargest` / `nsmallest`、`itertools.groupby`（要求**已按分组键排序**）等也接受类似的 `key=` 思路，可一并掌握。

---

## 五、可运行对照

见 `list_sort_vs_sorted_demo.py`（含 `None` 陷阱、`tuple`/`str` 输入、`itemgetter`/`attrgetter`、稳定排序小实验）。
