# 8.5 注解中可用的类型：从 `Any` 到泛型容器与抽象基类

本节是日常类型提示的**速查骨架**：每种写法解决什么问题、语法在 3.9+/3.10+ 怎么写、参数与返回值各用什么类型更稳。

配套脚本：`types_in_annotations_demo.py`。

**进阶续篇**（类型别名、`Iterable`/`Sequence`、`TypeVar`、`Protocol`、`Callable`、`NoReturn`）：见 `06-types-in-annotations-advanced.md` 与 `types_advanced_demo.py`。

---

## 8.5.1 `Any`：渐进式类型的“通配符”

- 未注解的参数/返回值，静态检查器往往按 **`Any`** 处理（等价于“暂不约束”）。
- **`Any` 的特殊规则**：与任意类型**双向**相容——既可接收一切，也可当作一切传给别的注解（因此会**关闭**很多检查，滥用等于关掉类型系统）。

### `Any` vs `object`

| 注解 | 静态检查眼中的 `x * 2` |
|------|-------------------------|
| `x: Any` | 允许（`Any` 上几乎所有操作都被放行） |
| `x: object` | 通常**拒绝**（`object` 不保证支持 `__mul__`） |

直觉：**越宽泛、越“顶”的类型，保证的操作越少**；`Any` 是例外，它是工具给渐进式迁移开的“后门”。

```python
def double_object(x: object) -> object:
    return x * 2  # mypy/pyright：object 不支持 *
```

---

## 8.5.2 简单类型与类

- 内置：`int`、`float`、`str`、`bytes`、`bool` 等可直接写进注解。
- 自定义类、标准库具体类同理。
- **数值可赋值相容**（PEP 484 的实用折中）：例如需要 `float` 的位置常可传入 `int`（与继承无关，属于类型系统的特殊规则）。

---

## 8.5.3 `Optional` 与 `Union`

- **`Optional[T]`** 等价 **`Union[T, None]`**，也等价（3.10+）**`T | None`**：表示“要么是 `T`，要么是 `None`”。
- **`Union[A, B]`**（3.10+ 多写成 **`A | B`**）：表示多种可能类型。
- **返回值尽量别滥用大 `Union`**：调用方往往要再分支或 `isinstance`，API 会变难用；简单解析函数（如 `str | float`）是常见例外。

嵌套会被展平：`A | B | (C | D)` 与 `A | B | C | D` 一类。

---

## 8.5.4 泛化容器（内置泛型）

- **3.9+**：直接写 `list[str]`、`dict[str, int]`、`set[int]` 等。
- **3.7 / 3.8**：同样写法常配合 `from __future__ import annotations`（推迟求值注解，避免运行期对 `list[str]` 求值失败）。
- 老代码里的 **`typing.List` / `typing.Dict`** 等：新代码优先用内置泛型；长期方向是少依赖大写别名。

**无界列表**：`list` 与 `list[Any]` 类同，表示“元素未约束”；迁移期可用，库 API 建议逐步收紧。

---

## 8.5.5 元组：三种角色、三种写法

1. **定长、异构（当记录用）**  
   `tuple[str, float, str]` —— 位置 0/1/2 类型各不相同。

2. **具名字段**  
   优先 **`typing.NamedTuple`**，可读性、重构性更好。

3. **变长、同构（当不可变序列用）**  
   `tuple[str, ...]` —— 任意长度，元素均为 `str`。

---

## 8.5.6 泛化映射

- 具体字典：`dict[K, V]`。
- **只读/宽入参**：更常用 **`collections.abc.Mapping[K, V]`**，兼容 `dict`、`defaultdict`、`ChainMap` 等**只读使用**场景。

---

## 8.5.7 抽象基类与 API 形状（伯斯塔尔定律）

- **参数（接收）**：宜**宽**——`Sequence[T]`、`Iterable[T]`、`Mapping[K, V]` 等，只要函数内部只依赖其协议。
- **返回值（给出）**：宜**具体**——`list[...]`、`dict[...]`，让调用方明确拿到什么结构。

这与 Python 的鸭子类型一致：ABC 在静态侧帮你表达“我只需要这些操作”。

---

## 速查表（3.10+ 为主）

| 需求 | 推荐写法 | 旧写法 / 备注 |
|------|-----------|----------------|
| 暂不约束 | `Any` | 少用，避免“注解了等于没注解” |
| 可为 `None` | `T \| None` | `Optional[T]` |
| 多选一 | `A \| B` | `Union[A, B]` |
| 列表元素 | `list[T]` | `typing.List[T]` |
| 字典键值 | `dict[K, V]` | `typing.Dict[K, V]` |
| 定长元组 | `tuple[A, B]` | `Tuple[A, B]` |
| 同构元组 | `tuple[T, ...]` | `Tuple[T, ...]` |
| 只读序列入参 | `Sequence[T]` | 比 `list` 更宽 |
| 只读映射入参 | `Mapping[K, V]` | 比 `dict` 更宽 |

---

## 运行

```bash
python part-2-functions-as-objects/chapter-08/types_in_annotations_demo.py
python -m mypy part-2-functions-as-objects/chapter-08/types_in_annotations_demo.py
```

---

## 附录：书本式综合示例（可粘贴到独立模块中试验）

下列片段把本节多个点子串在一起；与 `types_in_annotations_demo.py` 中的函数可对照阅读（demo 为便于阅读做了拆分）。

```python
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import NamedTuple


def parse_token(token: str) -> str | float:
    try:
        return float(token)
    except ValueError:
        return token


def tokenize(text: str) -> list[str]:
    return text.upper().split()


GeoCoord = tuple[float, float]


def geohash(lat_lon: GeoCoord) -> str:
    lat, lon = lat_lon
    return f"{lat:.6f},{lon:.6f}"


class Coordinate(NamedTuple):
    lat: float
    lon: float

    def geohash(self) -> str:
        return f"{self.lat:.6f},{self.lon:.6f}"


def columnize(sequence: Sequence[str], num_columns: int = 0) -> list[tuple[str, ...]]:
    if num_columns == 0:
        num_columns = round(len(sequence) ** 0.5)
    num_rows, reminder = divmod(len(sequence), num_columns)
    num_rows += bool(reminder)
    return [tuple(sequence[i::num_rows]) for i in range(num_rows)]


def name2hex(name: str, color_map: Mapping[str, int]) -> str:
    return f"#{color_map[name]:06x}"
```
