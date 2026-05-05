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

抛开死记表格，只记三件事：**谁会在缺键时自动造值**、**`get` 和 `[]` 差在哪**、**谁有「手动挪键顺序」的独门 API**。下文 **§二～§七** 是展开与避坑；一章内串联背诵见 [`00-字典与映射-背诵速查.md`](00-字典与映射-背诵速查.md)。

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

**② `popitem()`**（细则、可复制示例与**速查表**见 **§四** 从 **`popitem()` 行为对比** 到 **速查表** 一段。）

- **`dict`（3.7+）**：**LIFO**（弹「最后插入」的那一项）。  
- **`OrderedDict`**：**`popitem(last=False)`** 可 **FIFO**（从最老键弹），也可 LIFO。  
- **`defaultdict`**：没有额外顺序 API，跟 `dict` 一样走 **LIFO**。

**③ 独有「招牌」**

- **`defaultdict`**：`default_factory`、`__missing__` 那条缺键自动补链路。  
- **`OrderedDict`**：`move_to_end`、`popitem(last=...)`。  
- **`dict`**：无上述扩展，就是基准实现。

### 零.3 `setdefault` 和 `defaultdict` 怎么选？

#### 核心一句话

- **偶尔用、想显式控制 → 用 `dict.setdefault`**  
- **高频分组 / 计数 / `append` → 用 `defaultdict`**

（与 **`get`** 的边界、可变默认值坑见 **§五**、**§七**。）

---

#### 详细对比表

| 对比点 | `dict.setdefault` | `collections.defaultdict` |
| :--- | :--- | :--- |
| **触发时机** | 只有**主动调用** `setdefault` 且键不存在时，才写入默认值 | 每次用 **`d[key]`** 访问**不存在的键**，就**自动补默认值**（走 **`default_factory`**） |
| **`d.get(k)`** | 不涉及；缺键不写回 | **同样不触发工厂**、不插入键；只有 **`d[k]`** 才自动造值 |
| **典型场景** | 偶尔补一个键，代码要**显式、清晰** | 高频分组、计数、`d[k].append(...)`，追求极简 |
| **代码量** | 容易重复写 `if k not in d` 逻辑 | 工厂函数**一次配置**，后面直接 **`[]` 下标**访问 |
| **是否改变原字典** | 是，不存在就插入 | 是，自动插入 |
| **默认值类型** | **每次调用**可传**不同**的 `default` 参数 | 构造时**固定一种** `default_factory`（如 `list` / `int` / `set`） |
| **可读性** | 新手也能一眼看懂「在缺键时干了啥」 | 读者需知道「缺键会自动造值」这条约定 |
| **依赖** | 仅内置 **`dict`** | 需 **`from collections import defaultdict`** |

---

#### 代码示例对比

**1. `setdefault`（显式、偶尔用）**

```python
d: dict[str, list[int]] = {}
d.setdefault("key", []).append(1)  # 缺 "key" → 插入 [] → 再 append
```

**2. `defaultdict`（自动、高频用）**

```python
from collections import defaultdict

d = defaultdict(list)  # 一次定义：缺失键 → 空列表
d["key"].append(1)  # 缺 "key" → list() → 写入 → append
```

---

#### 怎么选（最实用口诀）

1. **只处理一两个键** → `setdefault`  
2. **循环里大量分组 / 统计** → `defaultdict`  
3. **不想引入 `collections`** → `setdefault`（或普通 `dict` + `get` / 显式分支）  
4. **代码要极简、少写判断** → `defaultdict`

---

#### 小结

- **`setdefault`**：**手动触发**、**灵活**（每次可给不同默认）、偏**显式**，适合**偶尔**补键。  
- **`defaultdict`**：**自动触发**、**统一**默认类型，适合**大量**分组 / 计数。

**实战**：「按词分组到列表」的 **`setdefault` vs `defaultdict` 对照**见 **`06_mapping_types_three_way_demo.py`** 第 **9)** 节。

### 零.4 选型照抄（可直接背）

1. **绝大多数场景**、只需要保留**插入顺序** → 直接用**普通 `dict`**（**Python 3.7+** 语言规范保证插入顺序）。  
2. 下标 **`d[k]`** 访问缺键，要自动给**列表 / 集合 / 计数**等初始值 → 用 **`defaultdict`**。  
3. 需要**手动挪动键位置**、**FIFO 弹出**、**`move_to_end`**、**LRU 缓存**等「顺序当 API 用」→ 用 **`OrderedDict`**。

### 零.5 必记避坑 + 核心一句话

#### 1. `defaultdict` 避坑

只有**方括号下标 `d[k]`** 在缺键时才触发 **`default_factory`**（经 **`__missing__`** 那条链）；**`.get(k)`**、**`.setdefault(...)`** **都不会触发工厂**，别混用语义。（细则见 **§五**、**§七**；与 `setdefault` 选型对照见 **§零.3**。）

#### 2. `dict.fromkeys` 经典大坑

**`dict.fromkeys(keys, [])`**：所有键**共享同一个列表对象**；改一个键下的列表，别的键**跟着变**。  
✅ **正确写法**：字典推导式 **`{k: [] for k in keys}`**，每个键各自**一个新** `list`。

#### 3. `OrderedDict` 选型避坑

**Python 3.7+** 原生 **`dict` 已保留插入顺序**；**没有**手动调序、**`move_to_end`**、**FIFO 弹出**等需求时，**坚决不用 `OrderedDict`**——原生 **`dict` 更轻、更简单**。

**核心一句话**：`dict` 管通用存储；`defaultdict` 管 **`d[k]` 缺键自动兜底**；`OrderedDict` 管**顺序 API**；各干各的，按「缺键要不要自动造」「要不要手挪顺序」选。

一章内**串联背诵**（可哈希、`ChainMap`、`setdefault`、三大字典、避坑）：[`00-字典与映射-背诵速查.md`](00-字典与映射-背诵速查.md)。

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
| `setdefault` | ✅ | ✅ | ✅ | 选型见 **§零.3**；坑见 **§五**、**§七** |
| `__setitem__` / `d[k]=v` | ✅ | ✅ | ✅ | 赋值 |
| `update` | ✅ | ✅ | ✅ | 原地合并 |

---

## 四、核心方法解析

### 0. 背题用速记（四句）

- **`__missing__`**：写在 **`defaultdict`** 这条链路上；**只有 `d[k]` 缺键**才触发；**`get` / `setdefault` 都不走**它（也不走 **`default_factory`**）。  
- **`move_to_end`**：**`OrderedDict` 独有**；**LRU** 常用「访问 → 挪到末尾；淘汰 → `popitem(last=False)` 从头部弹」。  
- **`|` / `|=`**：**Python 3.9+**（[PEP 584](https://peps.python.org/pep-0584/)）；**右侧覆盖左侧同名键**；老版本用 **`{**d1, **d2}`**。  
- **`popitem`**：**`dict` / `defaultdict`** 在 **3.7+** 均为 **LIFO**；**`OrderedDict`** 可用 **`last=False` 做 FIFO**。

（细则、官方链接与可复制示例见 **§四** 下 **`### 1`～`### 4`**；**打印用一页表**见 **`### 7`**。）

---

### 1. `__missing__(k)`（**真正归属：`defaultdict` 核心机制**）

- **触发条件**：**仅当**用 **`d[k]`** 访问**不存在**的键时（经映射的 **`__getitem__`**）。  
- **工作方式**：`defaultdict` 调用 **`default_factory()`**（无参），把返回值**写入**该键并返回。  
- **重要边界**（背题常考）：  
  - **`d.get(k)`** **不会**触发 **`__missing__`**，也**不会**插入键。  
  - **`d.setdefault(k, …)`** **也不会**触发 **`__missing__`** / **`default_factory`**；缺键时插入的是你传入的 **`default`**（`defaultdict` 若只写一个参数则与普通 `dict` 一样，缺省值为 `None`）。想要「按工厂自动补」，请用 **`d[k]`** 或 **§零.3** 的选型。  
- **本质**：映射子类可用的**缺键钩子**；`defaultdict` 用它把 **`default_factory`** 接到 **`d[k]`** 上。普通 **`dict`** 类型本身**不带**这条自动补逻辑。

### 2. `move_to_end(k, last=True)`（**归属：`OrderedDict` 独有**）

- **功能**：把**已存在**的键 `k` 挪到当前**插入顺序**的**队尾**或**队首**。  
- **参数**：  
  - **`last=True`（默认）** → 移到**末尾**（常表示「最新」）。  
  - **`last=False`** → 移到**开头**（常表示「最老」）。  
- **经典用途：LRU**  
  - **访问命中**：`move_to_end(key)`，把该键标成「最近用过」。  
  - **容量满要淘汰**：`popitem(last=False)` 从**头部**删掉最久未更新顺序的一端（配合你的「哪端算 LRU」约定）。

### 3. `|` / `|=`（字典合并运算符，**Python 3.9+**）

- **`d1 | d2`**：生成**新** `dict`；**`d2` 里与 `d1` 重复的键**以 **`d2` 的值为准**（右操作数覆盖左操作数）。  
- **`d1 |= d2`**：**原地**更新 **`d1`**，合并规则同上。  
- **`other | d`**：当左侧不是 `dict`、右侧是 `dict` 时，可能走映射的 **`__ror__`**，使「非 dict 在左」也能合并。  
- **向下兼容（≤3.8）**：用 **`{**d1, **d2}`**（或 `update` / 循环），见 **`03-映射拆包与字典合并.md`**。  
- 规范：[PEP 584 — Add Union Operators To dict](https://peps.python.org/pep-0584/)。

### 4. `popitem()` 行为对比（**`dict` / `OrderedDict` / `defaultdict`，最重要**）

**速读（①②③）**

1. **普通 `dict`（Python 3.7+）**：**LIFO**，弹**最后插入**；空字典 **`KeyError`**。  
2. **`OrderedDict`**：**`popitem()` 默认 LIFO**；**`popitem(last=False)` → FIFO**（弹**最先插入**）。  
3. **`defaultdict`**：继承 **`dict`**，**无**额外顺序 API；与 **`dict`** 一样 **3.7+ LIFO**。

**权威口径（记版本边界）**

- **`dict`**：自 **Python 3.7** 起，语言规范保证映射的**插入顺序**；`dict.popitem()` **移出并返回**一对 `(key, value)`，且为 **LIFO**（**最后插入**的先被弹出）。**3.6 及更早**：`dict` 不保证顺序，`popitem()` 的顺序也不应依赖。官方说明：[Built-in Types — `dict.popitem`](https://docs.python.org/3/library/stdtypes.html#dict.popitem)。  
- **`OrderedDict`**：`popitem(last=True)` 与 **`dict`** 同为 **LIFO**；`last=False` 时为 **FIFO**（弹出**最早插入**的项）。官方说明：[collections — `OrderedDict.popitem`](https://docs.python.org/3/library/collections.html#collections.OrderedDict.popitem)。  
- **`defaultdict`**：继承自 **`dict`**，**没有**自己的 `popitem` 实现；顺序语义与 **`dict`** 相同（**3.7+ LIFO**）。类说明见 [collections — `defaultdict` 对象](https://docs.python.org/3/library/collections.html#collections.defaultdict)。

**共同边界**：映射为空时调用 **`popitem()`** 均抛出 **`KeyError`**（三者一致）。

#### 4.1 `dict`（Python 3.7+）

- **无参数**：`d.popitem()` → **LIFO**。  
- **空字典**：`KeyError`。

```python
d = {"a": 1, "b": 2, "c": 3}
assert d.popitem() == ("c", 3)

try:
    {}.popitem()
except KeyError:
    pass
```

#### 4.2 `OrderedDict`

- **签名**：`od.popitem(last=True)`。  
  - **`last=True`（默认）**：**LIFO**（与 `dict.popitem()` 同向）。  
  - **`last=False`**：**FIFO**（最老键先出）。

```python
from collections import OrderedDict

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
assert od.popitem() == ("c", 3)  # LIFO
assert od.popitem(last=False) == ("a", 1)  # FIFO：剩下 {"b": 2}，最老的是 "a"
assert dict(od) == {"b": 2}
```

#### 4.3 `defaultdict`

- **无额外顺序 API**；`popitem()` 与 **`dict`** 一致（**3.7+ LIFO**）。  
- **`KeyError`**：空映射时同上。

```python
from collections import defaultdict

dd: defaultdict[str, int] = defaultdict(int, [("a", 1), ("b", 2), ("c", 3)])
assert dd.popitem() == ("c", 3)
```

---

### 5. 三者「独有招牌」方法（对照记忆）

| 类型 | 独有 / 特色 | 要点 |
| :--- | :--- | :--- |
| **`defaultdict`** | **`default_factory`**、`__missing__(key)` | 仅 **`d[k]`**（`__getitem__`）在**缺键**时走工厂并**写回**；**`get(k)` 不触发**。 |
| **`OrderedDict`** | **`move_to_end(key, last=True)`**、`popitem(last=...)` | 在「已有插入顺序」上提供**显式重排**与 **FIFO/LIFO** 弹出。 |
| **`dict`** | 无上述扩展 | 基准映射；**3.7+** 已有插入顺序，但**不能** `move_to_end` / `popitem(last=False)`。 |

**`defaultdict` 示例（缺键自动建容器）**

```python
from collections import defaultdict

dd = defaultdict(list)
dd["a"].append(1)  # 缺 "a" → 调 list() → [] 写入 → 再 append
assert dd == {"a": [1]}
```

**`OrderedDict` 示例（挪键 + 双端弹出）**

```python
from collections import OrderedDict

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("b")  # 把已有键 "b" 移到队尾
od.move_to_end("c", last=False)  # 把 "c" 移到队首
assert list(od.keys()) == ["c", "a", "b"]
```

---

### 6. 一句话 + 速查表（`popitem` / 独有 API）

**一句话**

- **`dict`（3.7+）**：`popitem()` 固定 **LIFO**；无 `move_to_end` / `popitem(last=False)`。  
- **`OrderedDict`**：`popitem(last=...)` 支持 **FIFO / LIFO**；独有 **`move_to_end`**。  
- **`defaultdict`**：顺序行为同 **`dict`**；独有 **`default_factory` + `__missing__`** 缺键自动补链路。

**速查表（`popitem` + 谁独有啥）**

| 项目 | `dict`（3.7+） | `OrderedDict` | `defaultdict` |
| :--- | :--- | :--- | :--- |
| `popitem()` 默认 | **LIFO** | **LIFO**（`last=True`） | **LIFO**（同左） |
| **FIFO** 弹出 | ❌ | ✅ `popitem(last=False)` | ❌ |
| 空映射 `popitem` | `KeyError` | `KeyError` | `KeyError` |
| **`move_to_end`** | ❌ | ✅ | ❌ |
| **`default_factory` / 缺键 `d[k]` 自动造值** | ❌ | ❌ | ✅ |

可运行对照见 **`06_mapping_types_three_way_demo.py`** 第 **4)** 节（`popitem` 三者对比）、第 **8)** 节（简易 LRU）。

---

### 7. 一页纸速查表（`__missing__`、`move_to_end`、字典 `|` / `|=`、`popitem`）

打印或截图时，可与 **§四.0** 四句对照；本表收「**谁 / 何时 / 不触发谁**」。

| 考点 | 归属 / 版本 | 何时 / 行为 | **不**走这条链路的常见写法 |
| :--- | :--- | :--- | :--- |
| **`__missing__(k)`** | **`defaultdict`**（及可自定义的 `dict` 子类） | 仅 **`d[k]`** 且键尚不存在 | **`get`**、**`setdefault`** |
| **`move_to_end(k, last=…)`** | **`OrderedDict`** | 已有键挪到**尾**（`True`）或**首**（`False`） | — |
| **`|` / `|=`** | 内置 **`dict`** 等，**3.9+**（[PEP 584](https://peps.python.org/pep-0584/)） | **`|`** 新 dict；**`|=`** 原地并；**右操作数覆盖左**同名键 | **≤3.8**：`{**d1, **d2}` 等 |
| **`popitem()`** | **`dict` / `defaultdict`**：**3.7+ LIFO**；**`OrderedDict`**：可 **FIFO** | 空映射一律 **`KeyError`** | — |

---

## 五、`setdefault` / `defaultdict` 补充（边界与坑）

（**对比表、口诀、示例**见 **§零.3**；这里只收「容易写错」的边界。）

1. **`get(k)` 与 `defaultdict`**：`get` **不会**调用 **`__missing__` / `default_factory`**，也**不会**插入键；需要「缺键就造并写入」只能用 **`d[k]`** 或自己分支。  
2. **`setdefault` 与可变默认值**：若事先 `shared = []`，再对多个键反复 `setdefault(k, shared)`，会出现**多键共享同一列表**；`dict.fromkeys(keys, [])` 同理。高频分组优先 **`defaultdict(list)`** 或显式分支里 **`d[k] = []`**。详见 **§七**。

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

见 `06_mapping_types_three_way_demo.py`（计数、`get` vs `[]`、`fromkeys`、**`popitem` 三者对比**、`move_to_end` / `popitem`、`|` 合并、简易 LRU、可哈希 `User`、**`setdefault` vs `defaultdict` 分组**）。

**下一篇**：词索引与可变值更新见 `07-可变值与词索引.md`。**§3.6** `OrderedDict` / `ChainMap` / `Counter` 专题见 `10-OrderedDict-ChainMap-Counter.md`；**`Counter` 深化、`shelve`、`UserDict` 子类化**见 `11-Counter与shelve及UserDict子类化.md`。**§3.8** `keys()` / `values()` / `items()` **字典视图**见 `12-字典视图.md`。
