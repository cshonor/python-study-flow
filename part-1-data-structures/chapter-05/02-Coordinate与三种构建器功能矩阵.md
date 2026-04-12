# 5.2 数据类构建器概述：用 `Coordinate` 把差异一次看懂（手写类 vs 三种构建器）

这一节的目标只有一个：**让你能“选对工具”**。  
你会用同一个坐标类 `Coordinate(lat, lon)`，对比 4 种写法：

- 手写类（baseline：你会发现它缺什么）
- `collections.namedtuple`（极简不可变记录）
- `typing.NamedTuple`（不可变 + 类型提示 + 可写方法）
- `@dataclasses.dataclass`（现代默认：可变/不可变都行，可扩展）

配套脚本：`coordinate_builders_demo.py`（把每个差异都跑出来）。

---

## 一、手写 `Coordinate` 的核心痛点（为什么会想要“构建器”）

从最简单的写法开始：

```python
class Coordinate:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
```

这个类“能用”，但你很快会遇到这些问题：

### 1.1 样板代码会随着字段数爆炸

字段越多，你就越痛苦：

- `__init__` 形参要写一遍
- `self.xxx = xxx` 再写一遍
- 想要好用的打印/比较/拷贝/默认值，还得再写更多

### 1.2 `repr/eq/hash` 等“好用能力”缺失

默认情况下：

- `repr(obj)` 打印的是内存地址（你看不出 lat/lon）
- `obj1 == obj2` 比的是身份（不是值）
- 不能直接拿去当 dict key / 放进 set（除非你手写 `__hash__` 且遵守契约）

### 1.3 没有类型提示（可读性与静态检查都差）

你想表达“lat/lon 应该是 float”，手写类要额外写注解、校验、甚至引入工具库。

---

## 二、三种构建器：从“极简记录”到“现代数据对象”

下面用同一个 `Coordinate` 形状解释三种构建器的本质区别。

---

### 2.1 `collections.namedtuple`：最轻量的不可变记录

```python
from collections import namedtuple

Coordinate = namedtuple("Coordinate", "lat lon")
moscow = Coordinate(55.756, 37.617)
```

你得到的是什么？

- 它是 **tuple 子类**（不可变）
- 自动生成 `__repr__` / `__eq__` / `_asdict()` / `_replace()` 等

适合：

- 轻量只读记录（坐标/尺寸/点/返回值打包）

不适合：

- 需要可变字段、复杂默认值、继承扩展较多的对象

---

### 2.2 `typing.NamedTuple`：给不可变记录加上类型提示

推荐的 class 语法：

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
```

你得到的是什么？

- 仍然是 **tuple 子类**（不可变）
- 但字段有类型，IDE/类型检查器更友好
- 还能写方法（例如把坐标格式化成 `55.8°N, 37.6°E`）

常见误解：

- `NamedTuple` **不是**你的“父类类型”（你最终继承的仍是 `tuple`）

---

### 2.3 `@dataclasses.dataclass`：现代默认（可变/不可变都能表达）

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float
```

你得到的是什么？

- 一个真正的“普通类”（不是 tuple）
- 自动生成 `__init__` / `__repr__` / `__eq__`（按你配置还可生成 order 等）
- `frozen=True` 时不可变（更像值对象），不写则默认可变
- 更容易扩展：默认值、`__post_init__`、继承、组合都更自然

---

## 三、功能对比表（把差异讲成“能不能做”）

| 功能 | `namedtuple` | `typing.NamedTuple` | `@dataclass` |
|---|---:|---:|---:|
| **可变实例** | ❌ | ❌ | ✅（默认）/ ✅（`frozen=True` 切换为不可变） |
| **class 语法** | ❌（常见用法是函数式） | ✅ | ✅ |
| **转 dict** | `_asdict()` | `_asdict()` | `dataclasses.asdict()` |
| **字段名列表** | `_fields` | `_fields` | `dataclasses.fields()` |
| **默认值** | `_field_defaults` | `_field_defaults` | `dataclasses.fields()`（Field 上有 default/default_factory） |
| **字段类型** | ❌ | ✅（`__annotations__`） | ✅（`__annotations__`） |
| **“修改后生成新实例”** | `_replace(**kw)` | `_replace(**kw)` | `dataclasses.replace(obj, **kw)` |
| **运行时动态创建类** | ✅（`namedtuple(...)`） | ✅（函数式 NamedTuple(...)） | ✅（`make_dataclass(...)`） |
| **自定义方法** | ⚠️ 能写但不常见 | ✅ | ✅（最自然） |
| **继承** | ⚠️ 不推荐 | ⚠️ 不推荐 | ✅（最自然） |

怎么读这张表？

- 你需要“像 tuple 一样轻量、不可变”的记录 → `NamedTuple`
- 你需要“像正常类一样的对象”，但不想手写样板 → `@dataclass`

---

## 四、7 个常用能力点（把表里的结论讲透）

### 4.1 可变 vs 不可变（影响 `hash`、dict key、并发安全直觉）

- tuple 系列（`namedtuple`/`NamedTuple`）天然不可变：更像“值”
- dataclass 默认可变，但可以 `frozen=True` 变成不可变值对象

### 4.2 class 语法的重要性（方法/文档/可读性）

当你需要给数据对象加一个 “`__str__` / `to_tuple()` / `from_row()`” 之类的方法时：

- `NamedTuple`/`dataclass` 的 class 语法更自然

### 4.3 转 dict / 取字段信息（反射与工具化）

做序列化、日志、调试工具时常用：

- `_asdict()`（namedtuple 系）
- `asdict()`（dataclass，递归转换）

### 4.4 字段类型获取：别直接读 `__annotations__`（推荐工具函数）

你当然可以读 `__annotations__`，但更推荐：

- `typing.get_type_hints()`：解析前向引用、处理字符串注解
- `inspect.get_annotations()`（3.10+）：标准化获取注解

### 4.5 “修改后生成新实例”

不可变对象的“修改”往往是“基于旧对象创建新对象”：

- namedtuple：`_replace`
- dataclass：`replace`

### 4.6 运行时动态建类（框架/工具会用到）

- `namedtuple(...)`
- `make_dataclass(...)`

你写业务不一定用，但理解它能帮你读懂很多框架代码。

### 4.7 继承与扩展

如果你确实要做层级结构、领域对象扩展：

> dataclass 更适合把“数据 + 少量行为”放在同一个结构里。

---

## 五、可运行对照

运行：

```bash
python part-1-data-structures/chapter-05/coordinate_builders_demo.py
```

你会看到：

- 4 种实现的 `repr/eq` 行为差异
- 不可变性（能不能赋值）
- `_asdict/_replace` vs `asdict/replace`
- `get_type_hints` / `get_annotations` 的输出对比

