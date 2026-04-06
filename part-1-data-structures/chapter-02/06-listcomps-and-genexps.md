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

### 4. 笛卡尔积（Cartesian Product）：多个 `for` 子句

**含义**：对每个 `a ∈ A`、每个 `b ∈ B` 各取一个，组成 `(a, b)`。结果长度约为 **`|A| × |B|`**（再乘以后续集合若有多层）。

**扑克牌（点数 × 花色）**

```python
ranks = ["A", "K", "Q"]
suits = ["♠", "♡", "♢", "♣"]

cards = [(rank, suit) for rank in ranks for suit in suits]
# 等价嵌套 for：外层 rank，内层 suit；顺序与嵌套循环一致
```

**T 恤（颜色 × 尺寸）**

```python
colors = ["黑色", "白色"]
sizes = ["S", "M", "L"]

t_shirts = [(color, size) for color in colors for size in sizes]
# 长度 2 × 3 = 6
```

**三个集合**：继续追加 `for` 子句即可：

```python
colors = ["黑", "白"]
sizes = ["S", "M"]
styles = ["圆领", "翻领"]

products = [(c, s, st) for c in colors for s in sizes for st in styles]
# 长度 2 × 2 × 2 = 8
```

**与 `itertools.product` 的关系**：语义相同；`product(A, B)` 常更可读、也便于惰性迭代：

```python
from itertools import product

list(product(ranks, suits))  # 与上面 listcomp 结果顺序一致（默认）
```

**避坑**

- **循环顺序**决定展开顺序；写反了组合顺序就反了。  
- **集合很大**时，`|A|×|B|` 可能爆内存 → 用 **生成器表达式** `(… for … for …)` 或 **`product(...)` 直接迭代**，不要先 `list(...)` 全家桶。  
- **超过 2～3 层**仍要可读：优先拆函数或显式 `product`，别硬堆一行。

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

#### 2.1 一个括号细节：什么时候必须写 `(...)`？

- **genexp 是“唯一参数”时**：外层括号可省略（推荐写法更干净）

```python
codes_tuple = tuple(ord(ch) for ch in symbols)
```

- **当函数调用还有别的参数时**：为了避免语法歧义，genexp **必须**保留外层括号

```python
import array

# array(...) 需要多个参数，因此 genexp 必须写成 ( ... )
codes_array = array.array("I", (ord(ch) for ch in symbols))
```

### 3. 一个常见小坑：生成器只能消费一次

```python
gen = (x for x in range(3))
list(gen)  # [0, 1, 2]
list(gen)  # []  已耗尽
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

## 六、作用域与变量名（面试高频坑）

在 Python 3 中，listcomp / genexp 的循环变量有自己的作用域：

```python
x = "outer"
_ = [x for x in range(3)]
assert x == "outer"
```

（Python 2 不同；现代项目一般只讨论 Python 3 行为。）

---

## 七、海象运算符 `:=` 在推导式里的“例外规则”

### 1. 核心结论

- **推导式的 `for` 循环变量**：不会泄漏到外部作用域（Python 3）。
- **推导式里的 `:=` 赋值目标**：会绑定在**外部作用域**（因此推导式结束后你还能访问到它）。

### 2. 最小可运行示例（和《流畅的 Python》一致）

```python
x = "ABC"
codes = [ord(x) for x in x]
assert x == "ABC"
assert codes == [65, 66, 67]
```

上面这句看着别扭但非常经典：**可迭代表达式 `in x` 用的是外层 `x`**（先求值），而 `for x in ...` 的 `x` 是推导式内部的循环变量（不污染外层）。

再看海象运算符：

```python
x = "ABC"
codes = [last := ord(c) for c in x]
assert last == 67
try:
    c  # noqa: F821
    raise AssertionError("c should not be defined")
except NameError:
    pass
```

- `c` 是推导式循环变量 → **外部访问报 `NameError`**
- `last` 是 `:=` 赋值目标 → **外部可用，值为最后一次赋值**

### 3. 何时该用、何时别用

- **可以用**：你确实需要在表达式里缓存中间结果（例如避免重复计算），且写法仍清晰。
- **别滥用**：把推导式写成“带状态机”的一行，很容易降低可读性；必要时直接回退到 `for` 循环更好维护。

---

## 八、句法提示：括号内自动换行 + 尾随逗号

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

## 九、列表推导式 vs `map`/`filter`（更 Pythonic 的原因）

### 1. 同一需求，两种写法

需求：从 `symbols = '$¢£¥€¤'` 中筛出 Unicode 码点 > 127 的字符，并得到码点列表。

**列表推导式（推荐）**

```python
symbols = "$¢£¥€¤"
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
```

读法接近自然语言：遍历 → 转换 → 过滤 → 得到列表。

**`map` + `filter`（传统函数式风格）**

```python
symbols = "$¢£¥€¤"
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
```

这段的成本在于：嵌套调用 + `lambda` + 最外层 `list(...)`，阅读顺序也更“从内到外”。

### 2. 作者的偏好点（别背口号，背原则）

- **当你要“构建一个列表”**：优先 listcomp（意图更直接）。
- **当你只是要“惰性流水线”**：优先 genexp / `map` / `filter`（不落地中间列表）。
- **当不用 `lambda` 且函数名本身很清楚**：`map(func, it)` / `filter(pred, it)` 有时也很干净。

### 3. 性能与内存的正确理解

- `map` / `filter` 在 Python 3 返回的是**惰性迭代器**；若最终还要 `list(...)` 落地，优势就主要剩下“写法偏好”。  
- listcomp 由解释器优化得很好；在很多“落地成 list”的场景里，**listcomp 不逊色**，且可读性往往更强。  
- 不要执着于“某个一定快 10%”：选择依据应优先是**可读性**与**是否需要惰性**。

---

## 十、性能与内存：别背百分比，背结论

- **listcomp 通常比 `for` + `append` 更短、更少 Python 层开销**（但性能差距取决于操作与版本）。  
- **genexp 的优势**在于**省内存**：不一次性构造整张列表，适合大数据流。  
- **真正的瓶颈**往往在：I/O、函数调用、对象分配、算法复杂度；推导式只是“写法更 Pythonic”的一环。

---

## 十一、面试题（带标准答案）

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

### Q6：为什么 `:=` 的目标在推导式外还能访问？

因为 `:=` 的目标是对**外层作用域**的绑定（这也是它在表达式中“赋值并复用”的设计初衷）；而推导式的循环变量本身在 Python 3 是隔离的。

### Q7：推导式里 `in <expr>` 的 `<expr>` 在哪个作用域求值？

记住结论即可：**可迭代表达式在外层求值**，循环变量绑定在推导式内部作用域。这也是 `x = "ABC"; [ord(x) for x in x]` 能成立且外层 `x` 不变的原因。

### Q8：`map` / `filter` 和推导式怎么选？

- **要落地 list** 且逻辑不复杂：优先 listcomp（意图清晰、好调试）。  
- **要惰性处理大输入**：优先 genexp / `map` / `filter`（配合 `sum`/`any`/`all`/`itertools`）。  
- **避免 `lambda` 套娃**：一旦出现多层嵌套 + `lambda`，通常可读性就输给推导式了。

### Q9：笛卡尔积用 listcomp 还是 `itertools.product`？

- **两者等价**（顺序一致时）：`[(a,b) for a in A for b in B]` ≈ `list(product(A, B))`。  
- **更推荐 `product` 的场景**：层数多、要惰性、或参数来自「可迭代对象列表」需要 `product(*iterables)`。  
- **大组合**：不要先 `list(product(...))` 除非真的需要整张表。

---

## 十二、配套 demo（建议直接跑一遍）

脚本：`part-1-data-structures/chapter-02/listcomps_and_genexps_demo.py`（含笛卡尔积与 `itertools.product` 对照）

```bash
python part-1-data-structures/chapter-02/listcomps_and_genexps_demo.py
```

