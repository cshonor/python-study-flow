# 字典推导式（Dict Comprehension）

> **本篇定位**：《流畅的 Python》**3.2.1**：用 `{k: v for ...}` 从可迭代对象**一次性**构造字典；与列表/集合推导式同一套语法家族。  
> **相关**：列表推导式见 `../chapter-02/03-listcomps-and-genexps.md`；本章开篇见 `01-dicts-and-sets-chapter3-overview.md`。  
> **配套脚本**：`dict_comprehension_demo.py`。

---

## 一、语法

Python 2.7+ 起支持字典推导式，形式为：

```python
{key_expr: value_expr for item in iterable [if condition]}
```

- **`key_expr` / `value_expr`**：对每个 `item` 求值，得到一对键值。  
- **`for item in iterable`**：遍历数据源。  
- **`if condition`**：可选；仅当条件为真时保留该项（等价于在循环里 `if` 过滤）。

---

## 二、书内示例：电话区号

### 1. 数据源

```python
dial_codes = [
    (880, "Bangladesh"),
    (55, "Brazil"),
    (86, "China"),
    (91, "India"),
    (62, "Indonesia"),
    (81, "Japan"),
    (234, "Nigeria"),
    (92, "Pakistan"),
    (7, "Russia"),
    (1, "United States"),
]
```

### 2. 键值对调：国家 → 区号

```python
country_dial = {country: code for code, country in dial_codes}
```

等价于显式循环：

```python
country_dial = {}
for code, country in dial_codes:
    country_dial[country] = code
```

### 3. 排序、过滤、再转换

```python
{
    code: country.upper()
    for country, code in sorted(country_dial.items())
    if code < 70
}
```

含义拆解：

1. **`sorted(country_dial.items())`**：得到 `(country, code)` 的列表，按**国家名**（元组首元素）排序。  
2. **`code: country.upper()`**：以区号为键、国家名为大写字符串为值（与 `country_dial` 中「国名→区号」再次对调并格式化）。  
3. **`if code < 70`**：只保留区号小于 70 的项。

---

## 三、与 `dict()` 构造的对比

| 维度 | 字典推导式 | `dict()` |
| :--- | :--- | :--- |
| **适用** | 需映射、过滤、对 `item` 做任意表达式时 | 已有「键值对序列」、直接构造即可 |
| **可读性** | 逻辑集中在一处；过复杂时宜拆行或写循环 | 简单场景很直观 |

性能上通常不必纠结二者；**清晰度优先**。

---

## 四、常见用途

- 键值对调、从 `(k, v)` 列表生成 `dict`。  
- 清洗：过滤 `None`、非法值等。  
- 对已有 `dict` 做 `for k, v in d.items()` 的二次转换。

---

## 五、避坑

1. **重复键**：同一键出现多次时，**后者覆盖前者**（与顺序赋值一致）。  
   ```python
   {k: v for k, v in [(1, "a"), (1, "b")]}  # {1: 'b'}
   ```
2. **键须可哈希**：`str` / `int` / 元素可哈希的 `tuple` 等；`list` / `dict` / `set` 不能作键。  
3. **可读性**：条件与表达式过多时，改用多行推导式或普通循环，避免「一行炫技」。

---

## 六、拓展：集合推导式

与字典推导式同形，但**无冒号**，生成 `set`：

```python
{x for x in range(1, 11) if x % 2 == 0}  # {2, 4, 6, 8, 10}
```

注意：**`{}` 在只有「单表达式」时是集合推导式**；若写成 `{a: b for ...}` 则是字典推导式。

**延伸**：**`set` / `frozenset`** 全貌（构造陷阱、运算、实现直觉）见 **`13-sets-and-frozenset.md`**。

---

## 七、自测练习（参考答案见 `dict_comprehension_demo.py` 第 5 段）

1. **成绩表**：给定 `grades = [("Ann", 88), ("Bob", 55), ("Cara", 72)]`，用字典推导式生成「姓名 → 分数」字典，且**只保留分数 ≥ 60** 的学生。  
2. **规范化**：给定 `raw = {"a": 1, "b": None, "c": 2}`，生成新字典，**去掉值为 `None` 的项**。

---

## 八、可运行对照

见 `dict_comprehension_demo.py`（区号示例、进阶过滤、重复键、`set` 推导式、自测答案）。

**下一篇**：`**` 拆包与 `|` / `|=` 合并见 `03-mapping-unpack-and-merge.md`。
