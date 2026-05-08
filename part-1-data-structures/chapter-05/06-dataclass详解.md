# 5.6 `@dataclass` 详解：参数、字段、`__post_init__`、`ClassVar`、`InitVar` 与实战建模

`@dataclass` 解决的核心问题只有一个：**把“数据对象”的样板代码交给标准库自动生成**。

你写：

- 字段（以及类型）
- 默认值/默认工厂
- 哪些字段参与比较/打印/哈希
- 需要的初始化后校验与派生字段

标准库帮你生成（或部分生成）：

- `__init__`
- `__repr__`
- `__eq__`（以及可选的排序方法）
- `__hash__`（在“安全”的条件下自动生成）

配套脚本：`06_dataclass_deep_dive_demo.py`（把本节所有关键点都跑出来）。

---

## 零、装饰器参数终极速查（考试 / 面试背诵版）

下面这一行就是「默认值长什么样」；后面六个参数**一字一句对应**这张心智表即可。

```python
@dataclass(
    init=True,
    repr=True,
    eq=True,
    order=False,
    frozen=False,
    unsafe_hash=False,
)
```

### `init`

- **控制什么**：是否**自动生成**构造方法 **`__init__`**
- **什么时候改**：你要**自己写 `__init__`**，或构造逻辑不由字段直出时，设 **`init=False`**

### `repr`

- **控制什么**：是否自动生成 **`__repr__`**（控制台里「一眼能看字段」的那种）
- **什么时候改**：默认太长、含**敏感信息**、或你要**完全自定义**展示格式时，设 **`repr=False`** 或配合 **`field(repr=False)`**

### `eq`

- **控制什么**：是否自动生成 **`==`**（**按字段**比较是否相等）
- **什么时候改**：你不想按字段比，而要**按对象身份**（类似默认对象语义）时，设 **`eq=False`**

### `order`

- **控制什么**：是否生成 **`<` `<=` `>` `>=`**，让实例**可按字段序比较、排序**
- **什么时候改**：你要对实例**排序**（按分数、时间戳等）时，设 **`order=True`**（且须 **`eq=True`**，见 **§一·1.2**）

### `frozen`

- **控制什么**：**冻结**实例 → 赋值给字段会失败，得到**逻辑上的不可变对象**
- **什么时候改**：想要**防误改**、当值对象用时，设 **`frozen=True`**（语义细节见 **§一·1.3**）

### `unsafe_hash`

- **控制什么**：在 dataclass 认为**不安全**的情况下，仍**强行生成 `__hash__`**，以便进 **`set` / `dict` 键**
- **什么时候改**：**绝大多数情况保持默认 `False`**；只有你非常清楚**可变字段与哈希不变式**的风险时才考虑打开

### 最精简口诀（约 10 秒）

- **`init`**：要不要自动 **`__init__`**
- **`repr`**：要不要自动 **`__repr__`**
- **`eq`**：要不要自动 **`==`（按字段）**
- **`order`**：要不要 **`<`… 与排序**
- **`frozen`**：要不要**冻结不可改**
- **`unsafe_hash`**：**没事别碰**

**版本提示**：Python 3.10 起另有 **`slots`** 等参数；先把上表六个背熟，再按需查 [`dataclasses.dataclass`](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass) 或下文 **§一** 表格。

---

## 一、`@dataclass` 装饰器参数：你到底让它“自动生成什么”

### 1.1 常见参数（你必须掌握）

> 注意：不同 Python 版本 `dataclass` 参数会略有增减；下面先抓住**最常用、最影响语义**的几个。（与 **§零** 背诵版同一张「参数—语义」表，可对照记忆。）

| 参数 | 它控制什么 | 你什么时候会改它 |
|---|---|---|
| `init` | 是否自动生成 `__init__` | 你想自己写 `__init__`，或用别的方式构造对象 |
| `repr` | 是否自动生成 `__repr__` | `repr` 太长、包含敏感字段、或你要自定义格式 |
| `eq` | 是否按字段生成 `__eq__` | 你不希望用字段相等（例如对象按 id 比较） |
| `order` | 是否生成排序方法（`< <= > >=`） | 你想让对象可排序（常见于“按分数/时间排序”） |
| `frozen` | 实例是否“冻结”（禁止给字段赋新值） | 你想要“逻辑不可变”的数据对象 |
| `unsafe_hash` | 强制生成 `__hash__` | 你知道自己在做什么；否则多数情况下不要开 |

### 1.2 关于 `order=True` 的硬规则

- `order=True` 需要你有“可比较”的字段顺序（按字段定义顺序生成比较）
- 另外，`order=True` 要求 `eq=True`；否则会直接抛 `ValueError`

### 1.3 关于 `frozen=True` 的真实含义（新手最容易误解）

`frozen=True` 的意思是：

- dataclass 会生成一个禁止写入字段的 `__setattr__`
- 你对 `obj.x = ...` 会抛 `FrozenInstanceError`

但它 **不是安全机制**（不是“防黑客”），因为：

- 你仍可能通过 `object.__setattr__(obj, "x", ...)` 绕过
- 如果字段本身是可变对象（例如 `list`），冻结只禁止“把字段指向另一个 list”，并不禁止“改 list 里面的内容”

所以更准确的理解是：

> `frozen=True` 主要用来**防误操作**，把“这个对象当成不可变值”写进代码结构里。

---

## 二、字段配置：`field()` 解决“默认值、显示、比较、初始化参与”等细粒度需求

### 2.1 最经典的大坑：可变默认值

在普通类里你可能写过：

```python
class C:
    def __init__(self, guests=[]):
        self.guests = guests
```

这会导致所有实例共享同一个 `guests` 列表，属于“隐蔽且致命”的 bug。

dataclass 直接把这类坑拦住了：**你在 dataclass 里写可变默认值会被拒绝**。

```python
from dataclasses import dataclass

@dataclass
class ClubMember:
    name: str
    guests: list[str] = []  # 会触发 ValueError（可变默认值）
```

### 2.2 正确写法：`default_factory`

```python
from dataclasses import dataclass, field

@dataclass
class ClubMember:
    name: str
    guests: list[str] = field(default_factory=list)
```

关键点：

- `default_factory` 接收 **无参可调用对象**
- 每次构造实例，dataclass 都会调用它来创建一个新对象
- 因此每个实例都有自己的 `guests`

### 2.3 `field()` 常用参数你该怎么理解

你可以把 `field()` 当成“对单个字段的开关面板”：

| 参数 | 直觉解释 | 常见用途 |
|---|---|---|
| `default` | 固定默认值 | `title="<untitled>"` |
| `default_factory` | 每次构造都调用，生成新默认值 | `list/dict/set` 等可变默认 |
| `init` | 这个字段是否出现在 `__init__` 参数里 | 派生字段、缓存字段 |
| `repr` | 是否出现在 `__repr__` 里 | 隐藏密码/token/大对象 |
| `compare` | 是否参与 `__eq__`/排序比较 | 忽略缓存、忽略不影响逻辑相等的字段 |
| `hash` | 是否参与 `__hash__` | 需要定制哈希时才碰 |
| `metadata` | 附加元数据（供框架/工具读取） | ORM、序列化、表单校验 |

### 2.4 实用例子：隐藏敏感字段

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    password: str = field(repr=False)
    is_admin: bool = field(default=False, repr=False)
```

这保证：

- `repr(user)` 不会把 `password` 打到日志里
- 但字段仍然存在、仍可用

---

## 三、初始化后处理：`__post_init__`（生成的 `__init__` 之后自动调用）

你可以把 dataclass 的生命周期想成两步：

1. 自动生成的 `__init__`：把参数赋给字段
2. 自动调用 `__post_init__`：你在这里做校验、派生字段、查库填充等

### 3.1 为什么需要它

因为 `__init__` 是自动生成的。你不想为了“多一步校验”就放弃自动生成。

### 3.2 示例：自动生成 handle + 唯一性校验

关键点：

- `all_handles` 是**类级别集合**（不属于每个实例）
- `handle` 是实例字段
- `__post_init__` 负责：
  - 缺省 handle 的生成
  - 唯一性检查
  - 更新全局集合

配套脚本会把重复 handle 的异常跑出来，帮助你理解执行顺序。

---

## 四、类属性 vs 实例字段：用 `ClassVar` 明确“这不是字段”

### 4.1 为什么必须用 `ClassVar`

dataclass 的规则很简单：**凡是带注解的名字，默认都当作字段处理**。

但你有时确实想写“带类型的类属性”，例如：全局计数器、类级缓存、全局集合。

这时必须写：

```python
from typing import ClassVar

all_handles: ClassVar[set[str]] = set()
```

效果：

- 类型检查工具知道它是类属性
- dataclass 也会跳过它：不会进 `__init__`，不会出现在 `fields()` 里

---

## 五、只用于初始化、但不保存为属性：`InitVar`

### 5.1 它解决什么问题

有些参数你只想“构造时用一下”，例如：

- 传一个数据库连接/配置对象
- 传一个原始字典/原始字符串

用完之后不希望它留在实例上（不希望 `obj.database` 存在），那就用 `InitVar`。

### 5.2 运行机制（理解这一句就够了）

> `InitVar` 会出现在 `__init__` 参数里，但不会成为字段；它会作为参数传给 `__post_init__`。

配套脚本会演示：

- `InitVar` 不会出现在 `vars(obj)` / `obj.__dict__` 里（也就不算“实例属性”）
- 但 `__post_init__(database=...)` 可以使用它来计算别的字段

补充一个容易误会的细节：

- Python 的属性查找顺序是“先找实例，再找类”。所以即便 `InitVar` 不在实例里，**你用 `hasattr(obj, "database")` 也可能得到 `True`**（因为类上可能有同名属性）。判断“是不是实例真正保存了这个值”，请用 `vars(obj)` 或检查 `"name" in obj.__dict__`。

---

## 六、综合实战：Dublin Core 风格的 `Resource`（把所有要点串起来）

下面这个例子故意包含典型需求：

- 必填字段（identifier）
- 有默认值的可选字段（title/type/description…）
- 两个“列表字段”，必须 `default_factory=list`
- `Enum` 字段表示资源类型
- 可选日期字段（`date | None` 的语义）

此外，我们还会演示两种 `repr`：

- dataclass 自动生成的单行 `repr`
- 自定义多行 `repr`（更适合“配置对象/元数据对象”的可读性）

这些内容都在配套脚本里可直接运行观察。

---

## 七、`@dataclass` vs `typing.NamedTuple`：你该怎么选

| 维度 | `@dataclass` | `typing.NamedTuple` |
|---|---|---|
| 默认可变性 | ✅ 可变（可 `frozen=True`） | ❌ 不可变 |
| `__post_init__` | ✅ 有 | ❌ 无 |
| `ClassVar` / `InitVar` | ✅ 支持 | ❌ 不支持（语义不同） |
| 可变默认值 | ✅ `default_factory` 规范支持 | 通常要手动处理 |
| 继承扩展 | ✅ 友好 | 元组子类继承通常不推荐 |

一句话建议：

- **只读简单 DTO**：`NamedTuple`
- **需要校验/派生字段/继承/复杂建模**：`@dataclass`

---

## 八、运行

```bash
python part-1-data-structures/chapter-05/06_dataclass_deep_dive_demo.py
```

你将看到每一节关键点的“可证据输出”：异常类型、字段列表、是否进 `__init__`、是否可变、`ClassVar/InitVar` 是否成为字段等。

