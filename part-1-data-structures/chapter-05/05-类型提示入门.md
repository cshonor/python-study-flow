# 5.5 类型提示入门：它是“静态文档”，不是运行时校验（普通类 vs NamedTuple vs dataclass）

这一节要把类型提示讲成“不会再混淆”的程度。你要牢牢记住一句话：

> **Python 的类型提示主要给人和工具看（IDE / mypy / pyright），解释器运行时默认不会强制校验。**

所以你会看到一种现象：代码跑得好好的，但静态检查会报错；反过来，静态检查通过也不代表运行时一定没 bug（比如你写的方法假设某字段是 `float`，却被传了 `str`）。

本节用三个对比对象讲清楚“注解写在哪里、它会不会变成属性、它对运行时有什么影响”：

- 普通类（Plain class）
- `typing.NamedTuple`
- `@dataclass`

配套脚本：`type_hints_primer_demo.py`。

---

## 一、核心本质：类型提示不等于类型检查

### 1.1 解释器不会因为注解而拒绝错误类型

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float

trash = Coordinate("Ni!", None)   # 运行时通常不会在这里报错
```

但如果你用 mypy / pyright 做静态检查，它会指出：

- `lat` 期望 `float`，你传了 `str`
- `lon` 期望 `float`，你传了 `None`

这就是类型提示的价值：**尽量在运行前把错误找出来**。

---

## 二、变量注解语法（先记住这两种形态）

```python
var_name: some_type            # 只有注解
var_name: some_type = value    # 注解 + 赋值（同时会创建真实变量/属性）
```

这一点会直接影响“它是不是类属性/实例属性”，下面会用普通类做演示。

---

## 三、三类“类结构”对比：普通类 vs NamedTuple vs dataclass

### 3.1 普通类：注解不等于属性

```python
class DemoPlainClass:
    a: int          # 只有注解，不会创建类属性
    b: float = 1.1  # 注解 + 赋值 -> 类属性
    c = "spam"      # 普通类属性（无注解）
```

结论：

- `DemoPlainClass.__annotations__` 会有 `a` 和 `b`
- 但 `DemoPlainClass.a` **不存在**（会 `AttributeError`）
- `DemoPlainClass.b` 存在（类属性），`DemoPlainClass.c` 也存在

这就是新手最容易混淆的点：**注解只是记录，不会自动创建属性**。

### 3.2 `typing.NamedTuple`：注解字段会变成“实例字段”（并生成 `__init__` 参数）

```python
from typing import NamedTuple

class DemoNTClass(NamedTuple):
    a: int
    b: float = 1.1
    c = "spam"      # 没注解 -> 只是类属性，不进入实例字段
```

结论：

- `a`、`b` 会成为实例字段（出现在 `_fields`，出现在 `__init__` 参数里）
- `c` 只是类属性，不会出现在实例字段里
- 实例不可变（tuple 子类语义）

### 3.3 `@dataclass`：注解字段会变成“实例字段”（并生成 `__init__` 参数）

```python
from dataclasses import dataclass

@dataclass
class DemoDataClass:
    a: int
    b: float = 1.1
    c = "spam"      # 没注解 -> 类属性
```

结论：

- `a`、`b` 进入实例字段与 `__init__` 参数
- `c` 是类属性
- 实例默认可变（除非 `frozen=True`）
- 默认允许动态加属性（除非 `slots=True`）

---

## 四、核心差异表（复习用）

| 维度 | 普通类 | `typing.NamedTuple` | `@dataclass` |
|---|---|---|---|
| 注解字段会变实例字段 | ❌ | ✅ | ✅ |
| 默认可变 | ✅ | ❌ | ✅ |
| 自动生成 `__init__/__repr__/__eq__` | ❌ | ✅ | ✅ |
| 动态新增实例属性 | ✅ | ❌ | ✅（可用 `slots=True` 限制） |
| 主要用途 | 业务类/手写控制 | 只读 DTO/VO/配置 | 通用数据对象 |

---

## 五、注解读取：别迷信 `__annotations__`，优先用工具函数

你当然可以读 `__annotations__`，但更推荐：

- `typing.get_type_hints(cls)`：会解析前向引用
- `inspect.get_annotations(cls)`：标准化接口（3.10+）

配套脚本会把它们的输出打印出来对比。

---

## 六、可运行对照

运行：

```bash
python part-1-data-structures/chapter-05/type_hints_primer_demo.py
```

你会看到：

- 普通类的“只有注解不等于属性”
- NamedTuple/dataclass 的“注解字段自动变实例字段”
- 运行时对“错误类型”不自动报错（但你的方法/逻辑可能会炸）
- dataclass 的动态属性与 `slots=True` 的效果（对照）

