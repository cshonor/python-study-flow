# 《流畅的 Python》第 8 章：全套类型提示 — 深度展开与学习路线

本文件是 **`chapter-08/`** 目录的**总览索引**：把书中「函数中的类型提示」拆成 **01～07** 与可运行 **`.py` demo**，便于按工业习惯做 **mypy** 落地与渐进改造。各节**正文仍以对应 `NN-…md` 为准**；此处侧重**路线、命令、可复制片段与避坑**。

**对应关系**（建议顺序）：

| 总览 § | 笔记 | 配套脚本 |
|--------|------|----------|
| §01 | [01 开篇](<./01-第 8 章开篇：函数中的类型提示（Type Hints）到底是什么.md>) | `01_type_hints_mypy_demo.py` |
| §02 | [02 渐进式类型](<./02-8.2 渐进式类型系统（Gradual Typing）：Python 类型提示的设计哲学与落地方式.md>) | `02_gradual_typing_demo.py` |
| §03 | [03 show_count 实战](<./03-8.3 渐进式类型实践：从 0 注解到可检查的函数签名（show_count 实战）.md>) | `03_show_count_demo.py`、`mypy_strict_pyproject_snippet.toml` |
| §04 | [04 鸭子 vs 名义](<./04-8.4 类型由受支持的操作定义：鸭子类型 vs 名义类型（静态检查在看什么）.md>) | `04_duck_nominal_typing_demo.py` |
| §05 | [05 注解可用类型](<./05-8.5 注解中可用的类型：从 Any 到泛型容器与抽象基类.md>) | `05_types_in_annotations_demo.py` |
| §06 | [06 进阶别名与泛型](<./06-8.5（续）类型提示进阶：别名、TypeVar、Protocol、Callable、NoReturn.md>) | `06_types_advanced_demo.py` |
| §07 | [07 位置/变长与局限](<./07-8.6 仅限位置参数与变长参数的类型注解 · 8.7 类型系统的局限性.md>) | `07_tag_type_hints_demo.py` |

目录级说明与一键运行命令：[`README.md`](README.md)。

---

## §01 入门：基础类型提示 + mypy 静态检查

### 核心概念

- **Type hints（类型提示）**：自 **PEP 484**（Python 3.5+ 起逐步落地语法）起，注解主要给 **IDE / 静态检查器**用；**默认运行时不按注解强制校验**（除非你显式用 `typing` 运行时设施或第三方校验）。
- **mypy**：常用的静态类型检查器；**不执行业务逻辑**，在开发/CI 阶段抓大量「形状错误」。

### 基础语法示例

```python
# 无注解：渐进式下 mypy 常把形参当 Any，检查很松（见 §03）
def add(a, b):
    return a + b

# 标准写法（Python 3.9+ 内置泛型）
def add(a: int, b: int) -> int:
    return a + b
```

### mypy 实操（在仓库根目录）

```bash
pip install mypy
mypy --version
mypy part-2-functions-as-objects/chapter-08/01_type_hints_mypy_demo.py
```

### 错误拦截直觉

```python
def add(a: int, b: int) -> int:
    return a + b

add(1, "2")  # mypy：第二实参应为 int，实际为 str（示例意义；若该行在 .py 里会报错）
```

### 工程/量化侧价值（直觉）

- 公共 API（行情、指标、订单、风控参数）**入参/返回值**一眼可读，减少「传错单位/传成 str 的数值」类低级错误。
- CI 里跑 mypy，与测试互补：**类型挡形状，测试挡行为**。

---

## §02 渐进式类型系统（Gradual Typing）

### 核心原理

Python 是**渐进式类型**语言（与「全程序必须注解」的语言不同）：

1. 老代码可以长期不加注解，**仍能运行**。
2. 可以只给部分模块/函数加注解。
3. 动态与静态信息可长期共存。
4. 适合**从小到大**增量改造，不必一次性重写仓库。

### 代码直觉

```python
def old_calculate_volatility(price_list):  # 未注解：mypy 默认往往很松
    return max(price_list) - min(price_list)


def new_calculate_volatility(price_list: list[float]) -> float:
    return max(price_list) - min(price_list)
```

### 配置灵活度

- 宽松：`strict = false`（默认），适合存量项目起步。
- 收紧：`disallow_untyped_defs` / `disallow_incomplete_defs` 等，见 **§03** 与官方 [mypy 配置](https://mypy.readthedocs.io/en/stable/config_file.html)。
- 新项目可考虑逐步趋近 `strict = true`；老项目**不要一步到位**。

### 量化意义

多年策略与脚本可继续跑；新模块先加「热路径」注解，再扩大覆盖面。

---

## §03 渐进式类型落地：从零注解改造

### 改造顺序（实用）

1. 先补**返回值**（收益大、冲突少）。
2. 再补关键**入参**。
3. 再细化容器、`None`、`Literal` 等。
4. 最后按模块打开 **mypy 严格项**（见 `03-8.3` **§二** 与 `mypy_strict_pyproject_snippet.toml`）。

### 贯穿案例：`show_count`

正文与断言版见 **`03_show_count_demo.py`** 与 **`03-8.3 …md`**。下面是与总览对齐的最小片段：

```python
def show_count(count, word):
    if count == 1:
        return f"1 {word}"
    return f"{count} {word}s"


def show_count(count: int, word: str) -> str:
    if count == 1:
        return f"1 {word}"
    return f"{count} {word}s"
```

可选参数完整版（书中风格；现代写法可用 `str | None` 代替 `Optional[str]`）：

```python
from typing import Optional


def show_count(
    count: int,
    word: str,
    plural: Optional[str] = None,
) -> str:
    if count == 1:
        return f"1 {word}"
    if plural is None:
        plural = word + "s"
    return f"{count} {plural}"
```

---

## §04 鸭子类型 vs 名义类型

### 鸭子类型（运行时 Python）

只关心对象**是否支持**所需操作，不关心类名是否出现在某棵继承树上。

### 名义类型（静态检查常见视角）

声明了 `x: T` 后，检查器主要按 **`T` 上是否具备**被访问的属性/方法来推断合法性（再叠加继承）。

### 现代折中：`Protocol`（静态结构化子类型）

见 **`04-8.4 …md`** 与 **`04_duck_nominal_typing_demo.py`**（含 `Protocol` + 可运行对照）。

```python
from typing import Protocol


class VolatilityCalculator(Protocol):
    def calc(self, prices: list[float]) -> float: ...


class SimpleVol:
    def calc(self, prices: list[float]) -> float:
        return max(prices) - min(prices)


def exec_calc(cal: VolatilityCalculator, prices: list[float]) -> float:
    return cal.calc(prices)
```

---

## §05 注解可用类型：从 `Any` 到容器

### 基础

`int`、`str`、`float`、`bool`、`None`（或 `type(None)` 在部分上下文）。

### 常用复合类型

| 写法 | 作用 |
|------|------|
| `T \| None`（3.10+）或 `Optional[T]` | 可能是 `T` 或 `None` |
| `T1 \| T2`（3.10+）或 `Union[T1, T2]` | 多选一类型 |
| `Any` | 与任意类型相容；**少用**，否则等于关掉检查 |

示例：

```python
def get_latest_price() -> float | None:
    return None


def get_raw_value() -> int | str:
    return 100
```

### 容器（Python 3.9+）

`list[T]`、`dict[K, V]`、`tuple[T1, T2, ...]`、`set[T]`。更早版本从 **`typing`** 导入 `List`、`Dict` 等大写别名。

---

## §06 进阶：类型别名、`TypeVar`、协议与可调用类型

### 类型别名

```python
from typing import TypeAlias

PriceSeries: TypeAlias = list[float]
StockPool: TypeAlias = dict[str, float]


def calc_sharpe(prices: PriceSeries) -> float:
    ...
```

### `TypeVar` 泛型

```python
from typing import TypeVar

T = TypeVar("T")


def get_first(items: list[T]) -> T:
    return items[0]
```

限定取值范围：

```python
Number = TypeVar("Number", int, float)


def square(x: Number) -> Number:
    return x * x
```

更多（`Protocol`、`Callable`、`NoReturn` 等）见 **§06** 正文与 **`06_types_advanced_demo.py`**。

---

## §07 仅限位置参数、变长参数与结构化字典

### `/` 仅限位置

```python
def demo(a: int, b: int, /, c: int) -> int:
    return a + b + c


demo(1, 2, 3)      # OK
demo(1, 2, c=3)   # OK
# demo(a=1, b=2, c=3)  # 错误：/ 左侧不可用关键字
```

### `*args` / `**kwargs` 注解形状

```python
def total_sum(*args: int) -> int:
    return sum(args)


def init_config(**kwargs: float) -> None:
    pass
```

### `TypedDict`（固定键、值类型按键变化）

与 **`07_tag_type_hints_demo.py`** 中 **`KLineBar`** / **`fetch_bar`** 示例一致（可 `mypy`）：

```python
from typing import TypedDict


class KLineBar(TypedDict):
    open: float
    high: float
    low: float
    close: float


def fetch_bar() -> KLineBar:
    return {"open": 100.2, "high": 106.5, "low": 99.1, "close": 104.8}
```

---

## 专属落地学习路线（可复制流程）

1. **环境**

   ```bash
   pip install mypy
   mypy --version
   ```

2. **每一节**

   1. 读对应 **`NN-…md`**。
   2. 运行对应 **`NN_*_demo.py`**（命令见 [`README.md`](README.md)）。
   3. **故意写错类型**，再跑 `mypy` 对照报错码与位置。
   4. 改到本文件约定范围内 **mypy 干净**（严格度可按 `03-8.3` 逐步加）。

3. **量化/大型项目迁移（分阶段）**

   - 一阶段：指标、纯计算、数据清洗等**纯函数**先完整注解。
   - 二阶段：策略核心对象、回测入口、配置边界。
   - 三阶段：IO、存储、外部 API（配合 **`TypedDict`** / **`Protocol`** 收窄外部数据形状）。
   - 最后：按目录/包打开 **`strict`** 或等价选项集（仍可对 `tests.*` 做 overrides）。

---

## 高频避坑

1. **`Any` 泛滥** ≈ 没写类型；优先 **`object`**、 **`Protocol`**、 **`TypeVar`**、 **`TypedDict`** 等收窄。
2. **Python 3.8 及更早**：容器注解用 **`from typing import List, Dict, ...`**（3.9+ 可用内置 `list[...]` / `dict[...]`）。
3. **注解 ≠ 运行时校验**：边界数据仍要校验与测试。
4. **严格模式**：先 **`disallow_untyped_defs` / `disallow_incomplete_defs`**，再考虑 `strict`；详见 **`03-8.3`** 与 **`mypy_strict_pyproject_snippet.toml`**。

---

## 官方参考（查阅用）

- [PEP 484 – Type Hints](https://peps.python.org/pep-0484/)
- [mypy 命令行](https://mypy.readthedocs.io/en/stable/command_line.html)
- [mypy 配置文件](https://mypy.readthedocs.io/en/stable/config_file.html)

以上与 **`chapter-08/`** 内各篇互为补充：**想系统跟书走，按 `01`→`07` 读；想快速建立工程化心智模型，以本文件为地图即可。**
