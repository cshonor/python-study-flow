# 映射 ABC、可哈希性与模式中的 `**rest`

> **本篇定位**：《流畅的 Python》**§3.4 / 3.4.1**：`collections.abc` 中的 **`Mapping` / `MutableMapping`**；**可哈希（hashable）** 的精确定义与常见类型；映射模式匹配中用 **`**变量名`** 收集未在模式中列出的键值对。  
> **相关**：容器 ABC 总览见 `../chapter-01/12-collections-abc-container-api.md`；第 2 章可哈希与 `dict` 键见 `../chapter-02/02-container-vs-flat-sequences.md`。  
> **配套脚本**：`mapping_abc_hashable_demo.py`。

---

## 一、映射模式补充：`**rest` 捕获其余键

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

---

## 二、3.4 映射类型的标准 API（`collections.abc`）

### 1. `Mapping` 与 `MutableMapping`

- 定义在 **`collections.abc`**（教学中常 `import collections.abc as abc`）。  
- 作用：描述 **只读映射** 与 **可变映射** 的接口；配合 **`isinstance(x, abc.Mapping)`** 可接受 **`dict`、`UserDict`** 等实现，而不仅是 `type(x) is dict`。

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

### 3. 模式匹配与数据校验

- `**rest` 适合「固定字段 + 扩展字段」；  
- 严格校验可配合 **guard**（`case ... if ...`）或 `TypedDict` / 校验库。

---

## 五、可运行对照

见 `mapping_abc_hashable_demo.py`（`**rest` 示例、`isinstance` Mapping、`hash`/`TypeError`、简易可哈希数据类）。

**下一篇**：`dict` / `defaultdict` / `OrderedDict` API 对照见 `06-dict-defaultdict-ordereddict-api.md`。
