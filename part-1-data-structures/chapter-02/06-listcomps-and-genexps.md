# 列表推导式 vs 生成器表达式（Listcomps vs Genexps）

> **本篇定位**：把《流畅的 Python》第 2 章开篇的核心（list comprehension / generator expression）整理成可直接抄进笔记的“模板 + 规则 + 面试问答”。  
> **相关**：序列整体框架与对象模型合并版见 `02-container-vs-flat-sequences.md`；学习路线见 `01-rich-sequences-chapter2-overview.md`。

---

## 一、先把一句话讲清楚

- **列表推导式（listcomp）**：用 `[]` **一次性**生成一个 `list`（eager / 立即构造）。
- **生成器表达式（genexp）**：用 `()` 生成一个**惰性迭代器**（lazy / 按需产出），常用来喂给 `tuple(...)`、`sum(...)`、`any(...)`、`dict(...)` 等消费方。

---

## 二、基础模板（最常用）

### 1. map（转换）

```python
codes = [ord(ch) for ch in symbols]
```

### 2. filter（过滤）

```python
evens = [x for x in data if x % 2 == 0]
```

### 3. map + filter（先过滤再转换）

```python
codes = [ord(ch) for ch in symbols if ch.isascii()]
```

### 4. “双循环”笛卡尔积（最多两层，别再深）

```python
pairs = [(a, b) for a in A for b in B]
```

---

## 三、生成器表达式怎么用最顺

### 1. 直接喂给消费者（推荐）

```python
total = sum(x * x for x in data)
```

### 2. 构造其他容器（需要时才 materialize）

```python
codes_tuple = tuple(ord(ch) for ch in symbols)
codes_set = {ord(ch) for ch in symbols}  # 这是集合推导式，不是 genexp
```

### 3. 什么时候不用 genexp？

- 你接下来要**重复遍历**多次，且数据量不大 → 直接 list 更省心。
- 你需要随机访问 / 切片 / `len` → 生成器不适合。

---

## 四、可读性准则（写得像 Python，而不是谜语）

- **一条推导式只做一件事**：转换或过滤或“两层组合”。  
- **嵌套超过 2 层**：大概率该改成普通 `for` 或拆成函数。  
- **复杂条件**：把条件提取成具名函数（或先 `if` 再推导）。  
- **别在推导式里做副作用**：例如打印、写文件、改外部列表等。

---

## 五、作者的工程边界（非常重要）

### 1. listcomp 的真实定位：**构建并返回一个新列表**

作者强调的是“意图表达”：

- `for` + `append` 描述的是**过程**（先建空列表，再逐个 append）。
- listcomp 描述的是**意图**（把一个可迭代对象映射成新列表）。

```python
codes = [ord(symbol) for symbol in symbols]
```

当你的目标就是“我要一个新列表”，这句话读起来通常更直接。

### 2. 禁止为了副作用而写 listcomp

如果你只是为了执行副作用（打印、写数据库、发请求、修改外部状态），**不要**用 listcomp：

```python
# ❌ 不要：为了副作用强行 listcomp，还会构造一个无意义的列表
_ = [print(x) for x in items]

# ✅ 就写 for
for x in items:
    print(x)
```

一句话：**listcomp 是表达式，副作用循环是语句；别把表达式当语句用。**

---

## 五、作用域与变量名（面试高频坑）

在 Python 3 中，listcomp / genexp 的循环变量有自己的作用域：

```python
x = "outer"
_ = [x for x in range(3)]
assert x == "outer"
```

（Python 2 不同；现代项目一般只讨论 Python 3 行为。）

---

## 六、句法提示：括号内自动换行 + 尾随逗号

### 1. 括号内忽略换行（不需要反斜杠）

在 `[]` / `{}` / `()` 内部，Python 允许自然换行，因此你可以把较长的推导式拆行写：

```python
codes = [
    ord(symbol)
    for symbol in symbols
    if symbol != "$"
]
```

### 2. 尾随逗号（trailing comma）

在列表/字典等字面量里，最后一项后面加逗号是合法的；好处是**后续新增一行时 diff 更干净**：

```python
items = [
    "a",
    "b",
]
```

---

## 六、性能与内存：别背百分比，背结论

- **listcomp 通常比 `for` + `append` 更短、更少 Python 层开销**（但性能差距取决于操作与版本）。  
- **genexp 的优势**在于**省内存**：不一次性构造整张列表，适合大数据流。  
- **真正的瓶颈**往往在：I/O、函数调用、对象分配、算法复杂度；推导式只是“写法更 Pythonic”的一环。

---

## 七、面试题（带标准答案）

### Q1：`[f(x) for x in it]` 和 `(f(x) for x in it)` 的区别？

- 前者返回 **list**（立即计算）。
- 后者返回 **generator**（惰性计算，迭代一次消耗一次）。

### Q2：为什么 `sum([x*x for x in it])` 不如 `sum(x*x for x in it)`？

后者**不构建中间 list**，内存更省；对大输入更稳。

### Q3：集合推导式和生成器表达式是什么关系？

- `{...}` 是**集合推导式**，直接返回 `set`。  
- `(...)` 是**生成器表达式**，返回 generator；它本身不生成 set，除非你 `set(genexp)`。

### Q4：推导式里能不能写 `try/except`？

不能直接写语句块。通常做法：

- 把异常处理封装成函数，再在推导式里调用；或
- 改回普通 `for` 循环（可读性更重要）。

### Q5：推导式适合所有场景吗？

不适合。读不懂、嵌套深、逻辑复杂、有副作用时，用普通循环/函数更清晰。

