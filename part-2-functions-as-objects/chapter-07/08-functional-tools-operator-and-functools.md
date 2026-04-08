# 7.8 支持函数式编程的包：`operator` 与 `functools.partial`

这一节的核心目标很明确：**用标准库把“常见的小 lambda”换成更清晰、可复用的工具函数**，并掌握 `partial` 这种“冻结部分参数”的高阶工具。

本节分两块：

- **7.8.1 `operator`**：把运算符/取字段/取属性/调方法变成函数对象（经常替代简单 `lambda`）。
- **7.8.2 `functools.partial`**：基于现有函数创建“参数更少的新可调用对象”（偏函数/冻结参数）。

配套脚本：`functional_tools_demo.py`（把示例 7-11～7-18 跑出来）。

---

## 一、`operator`：把“运算/取值/调方法”变成可传递的函数

### 1.1 用 `operator.mul` / `operator.add` 替代简单算术 lambda（示例 7-11、7-12）

当你写：

```python
lambda a, b: a * b
```

如果它只是“乘法”，那就直接用标准库：

```python
from operator import mul
```

这样做的好处：

- **更短、更直白**：看到 `mul` 就知道是乘法
- **可复用**：不用每次都写匿名函数
- **和 `reduce`/`map` 等高阶函数搭配自然**

用它写阶乘（典型示例）：

```python
from functools import reduce
from operator import mul

def factorial(n: int) -> int:
    return reduce(mul, range(1, n + 1), 1)
```

> 这里还顺手加了初始值 `1`，使得 `factorial(0)` 也正确为 1。

---

### 1.2 `itemgetter`：按索引取字段（示例 7-13）

当你写 `lambda x: x[1]` 做排序键/提取字段时，`itemgetter(1)` 通常更清晰：

```python
from operator import itemgetter

get_cc = itemgetter(1)
sorted(metro_data, key=get_cc)
```

`itemgetter(0, 1)` 还能一次取多个位置，返回一个元组：

```python
cc_name = itemgetter(0, 1)
cc_name(("Tokyo", "JP", 123))  # ("Tokyo", "JP")
```

---

### 1.3 `attrgetter`：按属性取字段（示例 7-14）

当你处理对象（例如 `namedtuple`、`dataclass`）时，经常写：

```python
lambda obj: obj.attr
```

可以换成：

```python
from operator import attrgetter
```

亮点是它支持**嵌套属性**：

```python
attrgetter("coord.lat")
```

也支持一次取多个属性，返回元组：

```python
name_lat = attrgetter("name", "coord.lat")
```

---

### 1.4 `methodcaller`：在对象上调用方法（示例 7-15）

当你写：

```python
lambda s: s.upper()
```

可写成：

```python
from operator import methodcaller
upcase = methodcaller("upper")
```

它还能绑定方法参数：

```python
hyphenate = methodcaller("replace", " ", "-")
hyphenate("The time has come")  # "The-time-has-come"
```

---

## 二、`functools.partial`：冻结部分参数，创建“更专用的新 callable”

### 2.1 `partial(func, *args, **keywords)` 做了什么（示例 7-16）

`partial` 会返回一个新的可调用对象 `p`，它会在你调用时：

- 先把你冻结的 `args/keywords` 放进去
- 再把这次调用传入的新参数接在后面
- 最终调用原函数 `func`

例如：

```python
from operator import mul
from functools import partial

triple = partial(mul, 3)
triple(7)  # 21，相当于 mul(3, 7)
```

### 2.2 用在文本归一化（示例 7-17）

把 `unicodedata.normalize` 的第一个参数固定为 `"NFC"`：

```python
import unicodedata
from functools import partial

nfc = partial(unicodedata.normalize, "NFC")
nfc("cafe\u0301")
```

### 2.3 用在 `tag`：固定标签名与 class（示例 7-18）

如果你有 7.7 的 `tag` 函数：

```python
from functools import partial
picture = partial(tag, "img", class_="pic-frame")
picture(src="x.png")
```

这会得到一个“专门生成 img 标签”的 callable，调用者不必每次都重复写 `"img"` 与 `class_`。

### 2.4 `partial` 的自省：`.func / .args / .keywords`

`partial` 对象会暴露：

- `p.func`：原函数
- `p.args`：冻结的位置参数
- `p.keywords`：冻结的关键字参数字典

这在调试/打印说明时很好用。

---

## 三、运行

```bash
python part-2-functions-as-objects/chapter-07/functional_tools_demo.py
```

脚本会展示：

- `reduce(lambda...)` vs `reduce(operator.mul, ...)`
- `itemgetter/attrgetter/methodcaller` 的典型用法
- `partial` 冻结参数 + `.func/.args/.keywords`
- `partial` 结合 7.7 的 `tag` 生成 `picture(...)`

