# `dict`、`defaultdict`、`OrderedDict`：常用 API 对照（§3.4.2）

> **本篇定位**：《流畅的 Python》**3.4.2**：三种最常用**映射实现**的**完整方法表**、能力差异与选型；并重申**自定义类可哈希**与 `__eq__`/`__hash__` 契约。  
> **相关**：抽象接口与可哈希定义见 `05-mapping-abc-and-hashable.md`；**`|` / `|=`** 语义见 `03-mapping-unpack-and-merge.md`。  
> **配套脚本**：`mapping_types_three_way_demo.py`。

---

## 一、自定义类可哈希（复习）

- 默认实例常**可哈希**（基于 `id`）；若重写 **`__eq__`** 按值比较，须同步定义 **`__hash__`**（或置 `__hash__ = None` 表示不可哈希）。  
- **`__hash__`** 应只依赖**不可变**参与相等性判断的属性。  
- 完整讨论与示例见 **`05-mapping-abc-and-hashable.md`**（及其中 `frozen` dataclass 示例）。

---

## 二、三种类型一句话

| 类型 | 要点 |
| :--- | :--- |
| **`dict`** | 内置映射；**Python 3.7+** 语言规范保证**插入顺序**。 |
| **`defaultdict`** | 在 **`__getitem__`**（`d[k]`）时若缺键，用 **`default_factory`** 生成默认值；**不**改变 `get()` 行为。 |
| **`OrderedDict`** | **`move_to_end`**、**`popitem(last=...)`** 的显式顺序控制；仅「按插入顺序遍历」时 **3.7+ 往往用 `dict` 即可**。 |

---

## 三、完整方法总表（书表 3-1 合并版）

下列为**能力对照**（✅ / ❌）。**`|*` 运算符**需 **Python 3.9+**（见 `03-mapping-unpack-and-merge.md`）。

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
- **3.8 及以下**：用 **`{**d1, **d2}`** 等，见 `03-mapping-unpack-and-merge.md`。

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

1. **`get` 与 `__missing__`**：`defaultdict` 的 **`get`** 对缺键不调用工厂。  
2. **`fromkeys` / 可变默认值**：`dict.fromkeys(keys, [])` 使**所有键共享同一列表**；应 **`{k: [] for k in keys}`**。  
3. **`setdefault` 与可变默认值**：若传入**同一个**可变对象作为 `default` 并在多处复用，可能产生意外共享；缺键时每次传入**新**对象更安全。  
4. **`OrderedDict` vs `dict`**：3.7+ 二者**都有**插入顺序；需要 **`move_to_end`** 等再用 `OrderedDict`。

---

## 八、可运行对照

见 `mapping_types_three_way_demo.py`（计数、`get` vs `[]`、`fromkeys`、`move_to_end` / `popitem`、`|` 合并、简易 LRU、可哈希 `User`）。

**下一篇**：词索引与可变值更新见 `07-dict-mutable-values-indexing.md`。**§3.6** `OrderedDict` / `ChainMap` / `Counter` 专题见 `10-dict-variants-ordered-chain-counter.md`；**`Counter` 深化、`shelve`、`UserDict` 子类化**见 `11-counter-shelve-and-userdict-subclassing.md`。
