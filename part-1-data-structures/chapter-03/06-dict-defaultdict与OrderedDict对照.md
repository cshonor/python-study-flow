# `dict` / `defaultdict` / `OrderedDict`：它们到底差在哪？别背表，先把“行为”搞懂

很多人学到这 3 个类型时，会陷入“背 API 表”的痛苦：这一行 ✅/❌，那一行又 ✅/❌，背了也不会用。

更好的学习方式是先抓住它们的**核心行为差异**：

- **`dict`**：普通字典，最常用，默认就选它。
- **`defaultdict`**：重点不在“多了几个方法”，而在“**缺键时 `d[k]` 会自动补一个默认值**”。
- **`OrderedDict`**：重点不在“也能保持顺序”（3.7+ 的 `dict` 也能），而在“**提供显式的顺序操作 API**（例如 `move_to_end`）”。

这篇笔记会做两件事：

1. 把最容易混淆的行为（`get` vs `[]`、`setdefault`、`fromkeys`、`popitem` 顺序）讲成能直接用的规则。
2. 给你一张“查表用”的方法对照（需要时再回来看，而不是死背）。

---

## 零、极简人话版（先抓触发逻辑，再查表）

抛开死记表格，只记三件事：**谁会在缺键时自动造值**、**`get` 和 `[]` 差在哪**、**谁有「手动挪键顺序」的独门 API**。下文 **§二～§七** 是展开与避坑。

### 零.1 核心本质（各一句话）

1. **`dict`（Python 3.7+）**  
   语言层保证**插入顺序**；**没有**缺键自动补值——`d[k]` 缺键就 **`KeyError`**；日常 **首选**。

2. **`defaultdict`**  
   只改了 **`d[k]`（`__getitem__`）** 一条路：**键不存在时**调用 **`default_factory`**，造出默认值并**写进字典**。  
   **重点**：**`get(k)` 完全不走这套**，缺键时该 `None` 还 `None`，**不会**触发工厂。

3. **`OrderedDict`**  
   3.7+ 在「遍历插入顺序」上和 `dict` 很像；**独门价值**是 **`move_to_end()`**、**`popitem(last=...)`**——要 **FIFO/LIFO 可控**、**LRU**、把某个键挪到队尾/队首时用它。

### 零.2 最容易混的三组行为

**① 缺键：`d[k]` vs `d.get(k)`**

|  | `dict` | `defaultdict` | `OrderedDict` |
| :--- | :--- | :--- | :--- |
| `d[k]` 缺键 | `KeyError` | **自动造默认并写入** | `KeyError` |
| `d.get(k)` 缺键 | `None` / 你给的默认，**不写回** | 同上，**绝不触发工厂** | 同 `dict` |

**② `popitem()`**

- **`dict`（3.7+）**：**LIFO**（弹「最后插入」的那一项）。  
- **`OrderedDict`**：**`popitem(last=False)`** 可 **FIFO**（从最老键弹），也可 LIFO。  
- **`defaultdict`**：没有额外顺序 API，跟 `dict` 一样走 **LIFO**。

**③ 独有「招牌」**

- **`defaultdict`**：`default_factory`、`__missing__` 那条缺键自动补链路。  
- **`OrderedDict`**：`move_to_end`、`popitem(last=...)`。  
- **`dict`**：无上述扩展，就是基准实现。

### 零.3 `setdefault` 和 `defaultdict` 怎么选？

| 对比点 | `setdefault` | `defaultdict` |
| :--- | :--- | :--- |
| 触发 | **只有你调用** `setdefault` 且缺键时才写入 | **每次** `d[k]` 缺键就自动补 |
| 典型场景 | 偶尔补一个键、写法显式 | 高频分组、计数、`d[k].append(...)` 极简 |
| 代码量 | 容易重复 `if k not in d` | 工厂一次配置，后面直接下标 |

### 零.4 选型照抄

1. **绝大多数** → **`dict`**（含「只要插入顺序」）。  
2. **`d[k]` 缺键就要默认容器/默认数** → **`defaultdict`**。  
3. **要挪键顺序、FIFO 弹、`move_to_end`** → **`OrderedDict`**。

### 零.5 必记避坑 + 一句话

1. **`defaultdict`**：只有 **`[]`** 会触发工厂，**`get` 不会**——别混用语义。  
2. **`dict.fromkeys(keys, [])`**：所有键**共享同一个 list**；用 **`{k: [] for k in keys}`**。  
3. **3.7+** 没有顺序操控需求就**别上 `OrderedDict`**，原生 **`dict`** 更简单。

**一句话**：`dict` 管通用存储；`defaultdict` 管 **`[]` 缺键自动兜底**；`OrderedDict` 管 **顺序 API**；各干各的，按「缺键要不要自动造」「要不要手挪顺序」选。

---

## 一、自定义类可哈希（复习）

- 默认实例常**可哈希**（基于 `id`）；若重写 **`__eq__`** 按值比较，须同步定义 **`__hash__`**（或置 `__hash__ = None` 表示不可哈希）。  
- **`__hash__`** 应只依赖**不可变**参与相等性判断的属性。  
- 完整讨论与示例见 **`05-Mapping抽象与可哈希.md`**（及其中 `frozen` dataclass 示例）。

---

## 二、三种类型一句话

| 类型 | 要点 |
| :--- | :--- |
| **`dict`** | 内置映射；**Python 3.7+** 语言规范保证**插入顺序**。 |
| **`defaultdict`** | 在 **`__getitem__`**（`d[k]`）时若缺键，用 **`default_factory`** 生成默认值；**不**改变 `get()` 行为。 |
| **`OrderedDict`** | **`move_to_end`**、**`popitem(last=...)`** 的显式顺序控制；仅「按插入顺序遍历」时 **3.7+ 往往用 `dict` 即可**。 |

---

## 三、完整方法总表（书表 3-1 合并版）

下列为**能力对照**（✅ / ❌）。**`|*` 运算符**需 **Python 3.9+**（见 `03-映射拆包与字典合并.md`）。

> **`__copy__` 一行**：不同 CPython 版本对是否在类型上**暴露** `__copy__` 方法不一致；**实用上**以 **`copy.copy(d)`** 能否得到浅拷贝为准（三者均可；**`defaultdict` 会保留 `default_factory`**）。不必死记某版书上对 `__copy__` 的勾叉。

| 方法 / 属性 | `dict` | `defaultdict` | `OrderedDict` | 说明 |
| :--- | :---: | :---: | :---: | :--- |
| `clear` | ✅ | ✅ | ✅ | 清空 |
| `copy` / `copy.copy` | ✅ | ✅ | ✅ | 浅拷贝 |
| `__contains__` / `k in d` | ✅ | ✅ | ✅ | 成员检测 |
| `default_factory` | ❌ | ✅ | ❌ | 缺键时构造默认值 |
| `__delitem__` / `del d[k]` | ✅ | ✅ | ✅ | 删除 |
| `fromkeys` | ✅ | ✅ | ✅ | 可变默认值陷阱见 §七 |
| `get` | ✅ | ✅ | ✅ | **不**触发 `default_factory` / `__missing__` |
| `__getitem__` / `d[k]` | ✅ | ✅ | ✅ | `defaultdict` 缺键走工厂 |
| `items` / `keys` / `values` | ✅ | ✅ | ✅ | 动态视图 |
| `__iter__` | ✅ | ✅ | ✅ | 迭代键 |
| `__len__` / `len(d)` | ✅ | ✅ | ✅ | 项数 |
| `__missing__(k)` | ❌ | ✅ | ❌ | `defaultdict` 缺键逻辑（由 `default_factory` 驱动） |
| `move_to_end(k, last=...)` | ❌ | ❌ | ✅ | 调整顺序 |
| `__or__`、`__ior__`、`__ror__`（并集运算符，见 `03`） | ✅ | ✅ | ✅ | **3.9+** |
| `pop` / `popitem` | ✅ | ✅ | ✅ | `OrderedDict.popitem(last=...)` **FIFO/LIFO** |
| `__reversed__` / `reversed(d)` | ✅ | ✅ | ✅ | 逆序迭代键 |
| `setdefault` | ✅ | ✅ | ✅ | 见 §五、§七 |
| `__setitem__` / `d[k]=v` | ✅ | ✅ | ✅ | 赋值 |
| `update` | ✅ | ✅ | ✅ | 原地合并 |

---

## 四、核心方法解析

### 1. `__missing__(k)`（实质在 `defaultdict`）

- 仅在用 **`d[k]`** 访问且键不存在时，由 `defaultdict` 内部与 **`default_factory`** 配合处理。  
- **`get(k)`** 不会调用 `__missing__`。

### 2. `move_to_end(k, last=True)`（`OrderedDict`）

- 调整键在**插入顺序**中的位置；典型用途：**LRU**（访问后移到末尾，淘汰时从头部 `popitem(last=False)`）。

### 3. `|` / `|=`（`__or__` / `__ior__` / `__ror__`）

- **Python 3.9+**：`d1 | d2` 得**新**映射；`d1 |= d2` **原地**更新；`other | d` 走 **`__ror__`**。  
- **3.8 及以下**：用 **`{**d1, **d2}`** 等，见 `03-映射拆包与字典合并.md`。

### 4. `popitem()`

- **Python 3.7+** 起，内置 **`dict`** 的 `popitem()` 为 **LIFO**（后进先出），与插入顺序一致。  
- **3.7 之前** `dict.popitem()` 顺序未保证；**`OrderedDict`** 仍可用 **`last`** 控制 FIFO/LIFO。

---

## 五、`setdefault` vs `defaultdict`

| 维度 | `setdefault(k, default)` | `defaultdict(factory)` |
| :--- | :--- | :--- |
| 何时写入 | 调用 `setdefault` 且键缺失时 | 每次 **`d[k]`** 缺键时 |
| `get` | 不涉及 | 不触发工厂 |
| 典型用法 | 偶尔补一项 | 高频计数、分组、嵌套累加 |

---

## 六、选型指南

| 类型 | 优势 | 适合 | 不太适合 |
| :--- | :--- | :--- | :--- |
| `dict` | 默认、快、3.7+ 有插入顺序 | 绝大多数场景 | 需要自动默认值、显式顺序 API |
| `defaultdict` | 缺键自动建默认值 | 计数、分组、多层嵌套累加 | 完全不需要默认值的场景 |
| `OrderedDict` | `move_to_end`、`popitem(last=...)` | LRU、顺序敏感 API、与旧代码互操作 | 仅遍历插入顺序且无其它需求（多用 `dict`） |

---

## 七、避坑

（与 **§零.5** 同脉络，这里再列全一点。）

1. **`get` 与 `__missing__`**：`defaultdict` 的 **`get`** 对缺键不调用工厂。  
2. **`fromkeys` / 可变默认值**：`dict.fromkeys(keys, [])` 使**所有键共享同一列表**；应 **`{k: [] for k in keys}`**。  
3. **`setdefault` 与可变默认值**：若传入**同一个**可变对象作为 `default` 并在多处复用，可能产生意外共享；缺键时每次传入**新**对象更安全。  
4. **`OrderedDict` vs `dict`**：3.7+ 二者**都有**插入顺序；需要 **`move_to_end`** 等再用 `OrderedDict`。

---

## 八、可运行对照

见 `06_mapping_types_three_way_demo.py`（计数、`get` vs `[]`、`fromkeys`、`move_to_end` / `popitem`、`|` 合并、简易 LRU、可哈希 `User`）。

**下一篇**：词索引与可变值更新见 `07-可变值与词索引.md`。**§3.6** `OrderedDict` / `ChainMap` / `Counter` 专题见 `10-OrderedDict-ChainMap-Counter.md`；**`Counter` 深化、`shelve`、`UserDict` 子类化**见 `11-Counter与shelve及UserDict子类化.md`。**§3.8** `keys()` / `values()` / `items()` **字典视图**见 `12-字典视图.md`。
