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

## 三、书内示例：`fruits`（逐行对照）

下面与书中示例一致，用来同时看到 **`sorted` 不修改原列表**、**`reverse` / `key=len`**、以及 **稳定排序**（见 §六）。

```python
fruits = ["grape", "raspberry", "apple", "banana"]

sorted(fruits)                      # ['apple', 'banana', 'grape', 'raspberry']  新列表；默认按字典序（见 §六）
fruits                              # 原列表未变

sorted(fruits, reverse=True)        # ['raspberry', 'grape', 'banana', 'apple']  整段序列反转

sorted(fruits, key=len)             # ['grape', 'apple', 'banana', 'raspberry']   按长度升序
# 长度都是 5 的 'grape' 与 'apple'：保持原列表中的先后 → 稳定性

sorted(fruits, key=len, reverse=True)
# ['raspberry', 'banana', 'grape', 'apple']  按长度降序；长度相同时仍保持原相对顺序
# 注意：这一结果一般不是「上一行结果的简单反转」，因为稳定性固定了并列时的次序

fruits.sort()                       # 原地升序；返回 None；此后 fruits 已变
```

多优先级（先长度、再字母序）可用**元组键**：

```python
sorted(fruits, key=lambda x: (len(x), x))
```

---

## 四、为什么原地方法返回 `None`？

Python 约定：**会修改接收者自身**的列表方法（如 `append`、`extend`、`sort`、`clear`）返回 **`None`**，避免让人误以为「拿到了一个新列表」。因此不要写：

```python
a = data.sort()  # 错误：a 是 None，原排序结果在 data 里
```

同类：**`random.shuffle(seq)`** 也是原地打乱，返回 `None`。

`sorted(x)` 则**不依赖**可变序列，适合管道式写法：`sorted(..., key=...)` 再继续链式处理。

---

## 五、`key` 进阶（实战向）

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

### 3. 多字段商品（价格 / 销量 / 名称）

典型需求：**价格升序**，同价则**销量降序**，再**名称升序**。数值「降序」可对那一维取负（仅适用于全为数字且不会溢出的场景）：

```python
products = [
    {"name": "A", "price": 10, "sales": 100},
    {"name": "B", "price": 10, "sales": 200},
    {"name": "C", "price": 9, "sales": 50},
]
sorted(products, key=lambda p: (p["price"], -p["sales"], p["name"]))
```

### 4. 稳定排序（stable sort）

Python 的排序（Timsort）是**稳定**的：键相等时，**保持原有相对顺序**。可利用这一点做「主键 / 次键」：**先按次键排，再按主键排**。

### 5. 与生态中其它 `key`

`min` / `max`、`heapq.nlargest` / `nsmallest`、`itertools.groupby`（要求**已按分组键排序**）等也接受类似的 `key=` 思路，可一并掌握。

---

## 六、Timsort、默认字典序与多语言文本

- **实现**：CPython 使用 **Timsort**（归并与插入的混合、针对真实数据自适应），最坏 **O(n log n)**，对已部分有序的数据往往更快；Java 等生态也广泛采用。
- **稳定**：键相等时保留原顺序（§三、`key=len` 并列即一例）。
- **默认规则**：`sorted` / `list.sort` 在无 `key` 时，对字符串按**码位**比较（Python 3 里即 Unicode 码点）；**ASCII 子集**下即传统「字典序」，大写与小写混排时未必符合人类阅读习惯，可用 `key=str.lower`。
- **中文等本地化**：不要指望默认排序符合语言习惯；需要时用 **`locale`**、**ICU** 或专门库做**自然语言排序**（collation）。

**有序后的利用**：对已排序序列可用 **`bisect`** 做二分查找 / 维持有序插入（`bisect_left`、`insort`）。

---

## 七、可运行对照

见 `list_sort_vs_sorted_demo.py`（第 1–5 段：基础与 `itemgetter` / 稳定两趟；第 6–8 段：`fruits` 全书示例、多字段商品、`shuffle` 返回 `None`）。
