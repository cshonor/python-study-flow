# 切片（Slicing）：约定、`slice` 对象与就地修改（Fluent Python 2.7）

> **本篇定位**：系统掌握 Python 切片的设计约定（左闭右开）、步距与反转、`slice` 对象的命名复用、多维切片与 `Ellipsis` 的语义，以及切片赋值/删除对可变序列的就地修改规则。  
> **相关**：序列整体框架见 `01-rich-sequences-chapter2-overview.md`；容器/扁平、可变性与 hashable 见 `02-container-vs-flat-sequences.md`。

---

## 一、为什么切片排除最后一项？（左闭右开）

Python 切片遵循 **左闭右开**：`seq[start:stop)`，核心收益：

- **长度计算直观**：长度就是 `stop - start`（当两者都给出时）。
- **无重叠拆分**：在索引 `x` 处拆成两段：`seq[:x]` 与 `seq[x:]`，不重不漏。

```python
l = [10, 20, 30, 40, 50, 60]
assert l[:2] == [10, 20]
assert l[2:] == [30, 40, 50, 60]
```

这套约定也与 `range(n)` 这类“长度等于 `n`”的直觉一致。

---

## 二、切片语法与步距：`s[a:b:c]`

`a` 起始（默认 0），`b` 结束（默认到尾），`c` 步距（默认 1，可为负）。

```python
s = "bicycle"
assert s[::3] == "bye"
assert s[::-1] == "elcycib"
assert s[::-2] == "eccb"
```

实践建议：当你写出 `s[a:b:c]` 且逻辑稍复杂时，优先考虑把它做成命名 `slice`（下一节）。

---

## 三、`slice` 对象：给切片“命名”，提升可读性

切片表达式 `a:b:c` 本质上会创建一个 `slice(a, b, c)`，并传给 `__getitem__`：

- `seq[a:b]` ≈ `seq.__getitem__(slice(a, b, None))`

命名切片的价值在于：把“魔法数字”变成“字段含义”。

```python
SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)

line = "123456" + "BANANA".ljust(34) + f"{12.50:>12.2f}"
assert line[SKU] == "123456"
assert line[DESCRIPTION].rstrip() == "BANANA"
assert float(line[UNIT_PRICE]) == 12.50
```

---

## 四、多维切片与省略号：`,` 与 `...`

### 1. 多维切片（本质：把索引打包成 tuple）

`obj[a, b]` 会把 `a, b` 作为一个 tuple 传给 `obj.__getitem__`/`__setitem__`。  
内置的一维序列（`list/tuple/str/...`）不支持多维；`numpy.ndarray` 等类型支持。

### 2. 省略号 `...`（Ellipsis）

- 写法是三个 ASCII 点：`...`（不是 Unicode 省略号）
- 它是 `Ellipsis` 单例，常用于多维数组切片的占位，例如 `x[i, ...]`

标准库里很少直接用到它，主要在 NumPy 等扩展库中出现。

---

## 五、切片赋值与删除：就地修改可变序列

切片可以出现在赋值左侧或 `del` 目标中，对 `list` 这类可变序列会**就地修改**：

### 1. 右侧必须是可迭代对象

```python
l = list(range(10))
l[2:5] = [20, 30]  # ✅
# l[2:5] = 100     # ❌ TypeError: 右侧不是可迭代对象
l[2:5] = [100]     # ✅
```

### 2. 替换/插入/删除都能做

```python
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
l[2:5] = [20, 30]
assert l == [0, 1, 20, 30, 5, 6, 7, 8, 9]

del l[5:7]
assert l == [0, 1, 20, 30, 5, 8, 9]
```

### 3. 带步距的切片赋值：长度必须匹配

带 `step` 的切片赋值是“对指定槽位逐个写入”，因此右侧长度必须与目标槽位数一致：

```python
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
l[3::2] = [11, 22, 33, 44]  # 目标槽位数为 4
assert l == [0, 1, 2, 11, 4, 22, 6, 33, 8, 44]
```

---

## 六、补充要点（面向实践）

- 自定义类型要支持切片：实现 `__getitem__`（必要时还要 `__setitem__`），第 12 章会更系统。
- `+`/`*` 往往创建新序列；切片赋值/删除是就地操作（语义与性能不同）。
- 内置类型里，`memoryview` 是少数在标准库层面支持多维切片的对象（更多多维切片在 NumPy 等库中）。

---

## 七、配套 demo

脚本：`part-1-data-structures/chapter-02/slicing_demo.py`

```bash
python part-1-data-structures/chapter-02/slicing_demo.py
```

