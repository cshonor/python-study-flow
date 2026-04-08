# 8.5（续）类型提示进阶：别名、`TypeVar`、`Protocol`、`Callable`、`NoReturn`

承接 `05-types-in-annotations.md` 中的基础注解；本节补齐**类型别名**、**迭代/序列选型**、**参数化泛型与 `TypeVar`**、**静态协议 `Protocol`**、**可调用类型 `Callable`**、**永不返回 `NoReturn`**。

配套脚本：`types_advanced_demo.py`。

---

## 一、类型别名（Type Alias）

- **作用**：给冗长类型起短名字，**只影响注解可读性**，不引入新运行时类型。
- **3.10+** 推荐显式标注，避免与普通赋值混淆：

```python
from typing import TypeAlias

FromTo: TypeAlias = tuple[str, str]
# 例如：Iterable[FromTo] 比 Iterable[tuple[str, str]] 更清晰
```

---

## 二、`Iterable` vs `Sequence`：入参怎么选

| 类型 | 能力 | 典型入参 |
|------|------|----------|
| `Iterable[T]` | 可迭代（`for`） | 列表、元组、生成器、自定义迭代器 |
| `Sequence[T]` | 有限、`len`、按索引访问 | 列表、元组、字符串等**序列** |

- **只需要遍历**：优先 `Iterable`（最宽）。
- **需要长度或索引**（例如按列排版、分块）：用 `Sequence`。
- **返回值**：尽量写具体类型（如 `list[T]`），少用裸 `Iterable`/`Sequence` 表示“我返回什么”，以免调用方不好用。

---

## 三、`TypeVar`：把“输入类型”和“输出类型”绑在一起

```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")

def sample(population: Sequence[T], size: int) -> list[T]:
    ...
```

- 传入 `Sequence[int]`，检查器会期望返回 `list[int]`；同理 `str` 等。

### 受限 `TypeVar`（固定几种）

```python
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar

NumberT = TypeVar("NumberT", float, Decimal, Fraction)
```

### 有界 `TypeVar`（`bound=`）

```python
from collections.abc import Hashable
from typing import TypeVar

HashableT = TypeVar("HashableT", bound=Hashable)
```

### 标准库：`AnyStr`

```python
from typing import AnyStr  # TypeVar('AnyStr', str, bytes)

def join_lines(lines: list[AnyStr], sep: AnyStr) -> AnyStr: ...
```

常用于 **同一套 API 在 `str` 与 `bytes` 上保持类型一致**。

---

## 四、静态协议 `typing.Protocol`

- **含义**：只描述“需要哪些方法/属性”，**不要求**目标类显式继承该协议（结构子类型）。
- 与 ABC：**名义继承** vs **结构匹配**——二者可并存；协议特别适合“只依赖一两个操作”的函数。

示例（可比较）：

```python
from collections.abc import Iterable
from typing import Any, Protocol, TypeVar

class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...

LT = TypeVar("LT", bound=SupportsLessThan)

def top(series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]
```

---

## 五、`Callable`：注解“可调用对象”

- **形式**：`Callable[[Arg1, Arg2, ...], Return]`。
- **任意参数**：`Callable[..., R]`（参数列表用 `...`）。

```python
from collections.abc import Callable

def repl(prompt: str, input_fn: Callable[[str], str] = input) -> str:
    return input_fn(prompt)
```

适用于回调、高阶函数、装饰器（更复杂的型变在第 15 章等深入）。

---

## 六、`NoReturn`：永不正常返回

用于：**总是抛错**、**无限循环不返回**、`os._exit` 一类路径。只用于**返回值**位置。

```python
from typing import NoReturn

def fatal_error(msg: str) -> NoReturn:
    raise RuntimeError(msg)
```

检查器会假定调用点之后的代码在“能返回”的前提下不可达（配合控制流分析）。

---

## 七、速览表

| 工具 | 作用 |
|------|------|
| `TypeAlias` | 缩短复杂注解 |
| `TypeVar` / `bound` / 受限 | 泛型函数、输入输出类型关联 |
| `Protocol` | 静态鸭子类型、结构约束 |
| `Callable[[...], R]` | 回调与高阶函数 |
| `NoReturn` | 不返回的函数 |
| `Iterable` / `Sequence` | 宽入参：只迭代 vs 要长度/索引 |

---

## 八、实践原则（精简）

1. **别名**：只为真实存在的冗长签名服务，避免无意义缩写。
2. **`TypeVar`**：能用 **`bound=` 描述公共超类型或协议**时，往往比硬编码“几种类型”更稳、更易扩展。
3. **`Protocol`**：在“只依赖少量操作”时减少继承耦合；需要共享实现或生态约定时仍会用 ABC。
4. **`Callable[..., R]`**：回调参数常很杂时用 `...`，返回值尽量具体。
5. **`NoReturn`**：只标**确实不会正常返回**的函数，避免削弱控制流推断。

---

## 运行

```bash
python part-2-functions-as-objects/chapter-08/types_advanced_demo.py
python -m mypy part-2-functions-as-objects/chapter-08/types_advanced_demo.py
```
