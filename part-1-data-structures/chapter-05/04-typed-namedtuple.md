# 5.4 带类型的具名元组：`typing.NamedTuple`（只读数据模型的现代写法）

这一节的重点是：**在保留 namedtuple 的轻量与不可变语义的同时，加上类型注解**。  
你会看到 `typing.NamedTuple` 和 `collections.namedtuple` 的关系是“同一个家族”，但它更适合现代代码库（IDE 友好、类型检查友好、可读性更强）。

配套脚本：`typed_namedtuple_demo.py`（含与 `@dataclass` 的对比）。

---

## 一、最核心的写法（示例：Coordinate）

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    reference: str = "WGS84"
```

你马上能得到这些能力：

- 自动生成 `__init__ / __repr__ / __eq__ / __hash__`
- 仍然是 **tuple 子类** → 不可变、可解包、可索引
- 自带元操作：`_fields`、`_asdict()`、`_replace()`
- 多了类型注解：`__annotations__`（以及 `typing.get_type_hints` 读取后的类型）

---

## 二、`typing.NamedTuple` 的关键特性（把你最容易误会的点说清楚）

### 2.1 它仍然是 tuple（不可变是“硬语义”）

```python
isinstance(Coordinate(1.0, 2.0), tuple)  # True
issubclass(Coordinate, tuple)            # True
```

不可变意味着：

- 你不能 `c.lat = ...`（会报错）
- “修改”只能用 `_replace` 生成新实例（copy-with 模式）

### 2.2 它有默认值，但规则和函数参数一样

带默认值的字段必须放后面：

```python
class Bad(NamedTuple):
    a: int = 1
    b: int          # ❌ 语法/定义层面就不允许
```

### 2.3 `__annotations__` 是“注解信息”，不是运行时校验

非常重要的一点：**Python 运行时不会因为你标注了 `float` 就拒绝 `str`**。  
类型注解主要服务于：

- IDE 提示
- 静态类型检查（mypy/pyright）
- 文档生成/工具反射

如果你要运行时校验，需要你自己写校验逻辑（或用 pydantic 等库）。

---

## 三、`typing.NamedTuple` vs `collections.namedtuple`：现代写法主要赢在“可读性 + 类型”

| 维度 | `collections.namedtuple` | `typing.NamedTuple` |
|---|---|---|
| 类型提示 | ❌ | ✅ |
| 写法 | 常见函数式 | ✅ class 语法（更自然） |
| 默认值 | `defaults=`（3.7+，右对齐） | ✅ 直接字段赋值（更直观） |
| 扩展方法 | 能动态注入，但不推荐 | ✅ 直接在 class 中写方法 |
| 适用 | 极简只读记录、快速脚本 | 现代代码库：DTO/VO/配置等只读模型 |

一句话：

- 想要“现代化 namedtuple” → `typing.NamedTuple`

---

## 四、与 `@dataclass` 的核心区别（选型最常卡在这里）

| 维度 | `typing.NamedTuple` | `@dataclass` |
|---|---|---|
| 可变性 | ❌ 不可变 | ✅ 默认可变；`frozen=True` 可变成不可变 |
| 继承扩展 | ⚠️ 不推荐复杂继承 | ✅ 更自然（更像普通类） |
| 默认值/工厂 | 支持（但不像 dataclass 那么丰富） | ✅ 很强（default/default_factory/post_init 等） |
| 性能/内存 | 更轻（tuple 语义） | 更灵活（普通类语义） |

工程经验（新手够用版）：

- **只读数据**（DTO、返回值、坐标、配置快照）→ `NamedTuple`
- **业务对象**（需要可变字段/继承/方法更复杂）→ `dataclass`

---

## 五、可运行对照

运行：

```bash
python part-1-data-structures/chapter-05/typed_namedtuple_demo.py
```

你会看到：

- 默认值如何生效
- `_fields/_asdict/_replace` 的效果
- 类型注解如何被 `get_type_hints` 读取
- 与 `dataclass(frozen=True)` / `dataclass()`（可变）的差异

