# `Mapping`/`MutableMapping`、hashable、以及 `match` 里的 `**rest`（把“概念”讲成“能用”）

这一篇要解决 3 个新手最常卡住的问题：

1. **为什么有时不该写 `type(x) is dict`，而要写 `isinstance(x, Mapping)`？**  
2. **hashable 到底是什么意思？为什么 list 不能当 dict 的 key？**  
3. `match/case` 的映射模式里，`**rest` 是干嘛的？为什么 `**_` 还会报错？

读完你应该能做到：看到别人代码里写 `Mapping`、`MutableMapping`、`hashable`、`**rest`，你不是“背过”，而是能解释清楚“为什么要这么写”。

---

## 零、总纲（新手先读这段：不堆术语）

这一页就讲 **3 件事**（工作、面试、写类型注解都用得上）：

1. **`Mapping`**：所有「长得像字典、能用 `key` 取 `value`」的东西——**用 `isinstance(x, Mapping)` 判断**，比 `type(x) is dict` **更宽、更稳**。  
2. **可哈希（hashable）**：能稳定参与 **`dict` 的 key / `set` 的元素`** 的那类对象；**可变容器**以及「**tuple 里塞了可变对象**」通常 **不行**。  
3. **`match` 映射模式里的 `**rest`**：把**已经点名的键**匹配掉之后，**剩下没写到的键值对**一次性抓进 `rest` 这个「小 dict」里。

---

### 零.1 `Mapping` / `MutableMapping` 是啥？

- **`Mapping`**：抽象上的**只读映射接口**（能读、能迭代、能 `len`）；**不要求**实现方真的不能改，但类型注解里写它表示「我这段代码**只读**」。  
- **`MutableMapping`**：在 `Mapping` 之上还要求 **`__setitem__` / `__delitem__`** 等——表示「我要**改键值**」。

**为啥用 `isinstance(x, Mapping)`？**  
`type(x) is dict` **只认**内置 `dict`；而 **`UserDict`、`ChainMap`、你自己实现的映射`** 常常也是 `Mapping` 实例，用 `Mapping` 才**不漏判**。

**练习口径**：函数**只读** `m` → 参数标 **`Mapping`**；必须**原地改**映射 → **`MutableMapping`**。

---

### 零.2 可哈希：人话版

**工程直觉**：放进 `dict` / `set` 的东西，哈希表要靠 **`hash(…)`** 找格子；**内容一变 hash 就变** → 定位全乱，所以 **`list` / `dict` / `set` 不能当 key`**。

**好记版**（有例外补丁，见 **§三** 与 `tuple` 含 `list`）：

- **一般**：不可变标量 / `str` / `bytes` / 元素都可哈希的 `tuple` / `frozenset` → **可哈希**。  
- **一般不行**：`list`、`dict`、`set`，以及 **`(1, 2, [3])` 这种 tuple**。

```python
try:
    a = [1, 2]
    {a: 123}
except TypeError as e:
    assert "unhashable" in str(e).lower()  # 成立 → list 不能当 key
```

---

### 零.3 `match` 里的 `**rest`

```python
row = {"type": "user", "id": "1", "note": ""}
match row:
    case {"type": "user", **rest}:
        assert rest == {"id": "1", "note": ""}  # 成立 → 其余键进 rest
```

**规则**：`**…` 必须写在映射模式的**最后**；`**_` 单独作名字在语法里**不合法**，用 **`**rest`** 或 **`**_rest`**；它**只捕获**，不会给缺了的键**补默认值**（与 `defaultdict` 不同）。更细的约定见 **§一**。

---

### 零.4 六句背诵（够应付大部分场景）

1. **`Mapping` = 类 dict 总接口**，`isinstance(..., Mapping)` 最稳。  
2. **`MutableMapping` = 要改键值时再收窄**。  
3. **hashable ≈ 能当 `dict` key / 能进 `set`**（严格定义见 **§三**）。  
4. **`list` / `dict` / `set` 不当 key**；**`tuple` 里别塞可变货**。  
5. **`**rest` = 映射模式里抓「剩下字段」**。  
6. **别写 `**_`**，写成 `**rest` / `**_rest`。

---

## 一、映射模式补充：`**rest` 捕获其余键

（**§零.3** 已用人话带过；这里是 PEP 634 规则与稍复杂例子。）

在 **`match` / `case`** 的**映射模式**中，可写 `**details`（名字自定），表示「已列出的键值都匹配后，**其余**键值对绑定到 `details`」。

规则要点：

- **`**` 段必须出现在映射模式的最后**（PEP 634）。  
- **`**_` 不是合法语法**（解析器报 `SyntaxError`）；应使用 **`**rest`** 等名字；若不需要使用其余键，仍须绑定名（如 `**_rest`）或不在模式里写 `**`。  
- **不会**因为缺键而向对象里「补键」：匹配失败则换下一 `case`；这与 **`defaultdict`** 在访问时自动建默认值**完全不同**。

```python
food = {"category": "ice cream", "flavor": "vanilla", "cost": 199}
match food:
    case {"category": "ice cream", **details}:
        print(details)  # {'flavor': 'vanilla', 'cost': 199}
```

适用：JSON/API 返回的**部分字段固定、其余字段动态**时的分支与收集。

你可以把它当成“解构”：

- 你先把你关心的键（例如 `category`）匹配掉。
- 剩下你不想一个个列出来的键，统一塞到 `details` 里。

这比你手动写 `details = dict(food); details.pop('category')` 更直接，也更不容易漏字段。

---

## 二、3.4 映射类型的标准 API（`collections.abc`）

### 1. `Mapping` 与 `MutableMapping`

- 定义在 **`collections.abc`**（教学中常 `import collections.abc as abc`）。  
- 作用：描述 **只读映射** 与 **可变映射** 的接口；配合 **`isinstance(x, abc.Mapping)`** 可接受 **`dict`、`UserDict`** 等实现，而不仅是 `type(x) is dict`。

#### 2.1 为什么不用 `type(x) is dict`？

因为 Python 里“像 dict 的东西”不只有 `dict`。例如：

- `collections.UserDict`（书里后面会讲，自定义映射时更推荐继承它）
- `collections.ChainMap`（多个映射的查找视图）
- 你自己实现的映射类型（实现了 `__getitem__`/`__iter__`/`__len__` 等协议）

如果你只写 `type(x) is dict`，这些都会被排除掉，代码会变得不通用。

更稳的写法是：

```python
from collections.abc import Mapping

def accepts_mapping(m: Mapping) -> None:
    ...
```

### 2. `Mapping` 和 `MutableMapping` 大概差在哪？

把它们想成“只读版”和“可写版”：

- **`Mapping`**：你能 `m[key]` 取值、能迭代、能 `len`，但不保证你能改。
- **`MutableMapping`**：在 `Mapping` 基础上，额外要求你能 `m[key] = value`、能删除键等。

在类型注解/接口设计里，这个区分非常常见：如果函数只需要读取，就用 `Mapping`（更宽）；如果必须修改，就用 `MutableMapping`（更窄）。

### 2. 继承关系（简图）

`Collection` → `__contains__` / `__iter__` / `__len__`  

在其上：`Mapping` 增加 `__getitem__`、`get`、`items`、`keys`、`values` 等只读语义；  

`MutableMapping` 再增加 `__setitem__`、`__delitem__`、`pop`、`update`、`setdefault` 等。

### 3. 自定义映射的推荐做法

- **优先** **`collections.UserDict`** 子类，或 **组合** 内置 `dict`（委托 `__getitem__` 等）。  
- **一般不**从零实现 `Mapping` / `MutableMapping` 抽象基类的全部方法，除非有特殊需求。  
- **键必须可哈希**（`dict` / `set` 底层为哈希表）；**值**任意。

---

## 三、3.4.1 可哈希（hashable）

### 1. 定义（工程口径）

对象 **可哈希** 当且仅当：

1. 生命周期内 **`hash(obj)` 稳定**（或该类型不可哈希，`hash` 抛 `TypeError`）。  
2. 可与同类对象比较 **`==`**。  
3. 若 **`a == b`**，则 **`hash(a) == hash(b)`**（否则破坏哈希表约定）。

把它翻译成“好记版”就是：

- 你把它当作 key 后，它的“定位信息（hash）”不能变。
- 否则 dict/set 就会找不到它，或者找错位置。

这也是为什么“可变对象通常不可哈希”：你一改内容，hash 就可能变。

### 2. 常见类型

| 类型 | 可哈希 |
| :--- | :--- |
| `None`、数字、`str`、`bytes`、`frozenset` | 是 |
| `tuple` | 当且仅当**每个元素**都可哈希 |
| `list`、`dict`、`set` | 否（可变） |
| 自定义类实例 | 默认常基于 `id`；若定义 **`__eq__` 且未妥善定义 `__hash__`**，可能变为不可哈希 |

### 3. 实现细节与 CPython

- **哈希随机化**（`PYTHONHASHSEED`）：**进程之间**或不同运行间，字符串等对象的 `hash` 可能不同；**同一进程内**稳定。  
- 重写 **`__eq__`** 时：应同步 **`__hash__`**（或显式 `__hash__ = None` 表示不可哈希），否则 `dict`/`set` 行为不可靠。

---

## 四、实战与避坑

### 1. 类型判断

- 偏窄：`type(x) is dict`（漏掉 `UserDict` 等）。  
- 更宽：`isinstance(x, collections.abc.Mapping)`。

### 2. 键的选择

- 列表、集合、字典**不能**作 `dict` 键或 `set` 元素。  
- 需要复合键时，用**元素均可哈希**的 `tuple` 或 `frozenset`。

这里建议你记一个“最简单的自检办法”：

```python
def is_hashable(x: object) -> bool:
    try:
        hash(x)
    except TypeError:
        return False
    else:
        return True
```

当你不确定某个对象能不能当 key，就 `is_hashable(x)` 试一下；这比背类型表更稳。

### 3. 模式匹配与数据校验

- `**rest` 适合「固定字段 + 扩展字段」；  
- 严格校验可配合 **guard**（`case ... if ...`）或 `TypedDict` / 校验库。

---

## 五、可运行对照

见 `05_mapping_abc_hashable_demo.py`（`**rest` 示例、`isinstance` Mapping、`hash`/`TypeError`、简易可哈希数据类）。

运行：

```bash
python part-1-data-structures/chapter-03/05_mapping_abc_hashable_demo.py
```

下一篇会把 `dict/defaultdict/OrderedDict` 常用方法差异做成一张更易查的表，并补上“哪些点最容易写错”，见 `06-dict-defaultdict与OrderedDict对照.md`。

---

## 六、小练习（用 `Mapping` 与 hashable 角度回答）

1. 写一个函数 `f(m)`：只读取 `m` 的内容，不修改它。你会给参数标注 `Mapping` 还是 `MutableMapping`？为什么？  
2. 构造一个“外壳不可变但不可哈希”的对象（提示：`tuple` 里塞 `list`）。解释它为什么不能当 dict key。  
3. 用 `match/case` 的映射模式写一个分支：匹配 `{"type": "user", **rest}`，并把 `rest` 打印出来。  

---

## 七、小练习参考答案（可复制）

### 题 1

**只读** → 参数用 **`Mapping`**（见 **§零.1**）。

### 题 2

```python
t = (1, 2, [3, 4])
try:
    hash(t)
except TypeError as e:
    assert "unhashable" in str(e).lower()  # 成立 → tuple 内有 list，整体不可哈希
```

### 题 3

```python
row = {"type": "user", "id": "42", "note": "alice"}
match row:
    case {"type": "user", **rest}:
        assert rest == {"id": "42", "note": "alice"}  # 成立
        print(rest)
```

