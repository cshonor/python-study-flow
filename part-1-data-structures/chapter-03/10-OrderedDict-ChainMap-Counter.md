# `dict` 的变体：`OrderedDict`、`ChainMap`、`Counter`（§3.6）

`dict` 够用了，但标准库还提供了几种“带特殊能力”的映射类型。你可以把它们理解成：

- **`OrderedDict`**：当你需要“显式控制顺序”（例如把某个 key 移到末尾）时用。\n- **`ChainMap`**：当你需要“多层查找（覆盖）”而不是“真合并”时用。\n- **`Counter`**：当你在做“计数/词频/多重集运算”时用（比自己写 `d.get(k, 0) + 1` 更直接）。

配套脚本：`dict_variants_demo.py`。

---

## 一、`collections.OrderedDict`（§3.6.1）

### 1. 与原生 `dict`（Python **3.7+** 语言保证插入顺序）

- **3.7+** 的 `dict` 已保证**插入顺序**；仅当需要 **`move_to_end`**、**`popitem(last=...)` 的 FIFO/LIFO 控制**、或与旧代码协同时，再选 **`OrderedDict`**。  
- **相等性**：两个 **`OrderedDict`** 若**键顺序不同**，可能 **`==` 为假**；**`OrderedDict` 与普通 `dict`** 在键值集合相同时，**通常仍按映射相等**（顺序不阻等）。以当前 CPython 行为为准，见 `dict_variants_demo.py`。

### 2. 顺序 API（与 `06` 呼应）

- **`move_to_end(key, last=True)`**  
- **`popitem(last=True)`**：`last=False` 时从**先插入端**弹出（FIFO）。

---

## 二、`collections.ChainMap`（§3.6.2）

### 1. 原理

- **不复制**子映射，只保存**引用**；查找时从**前到后**第一个含该键的映射取值。  
- **写入**（含新键）：默认落在**第一个**映射上；后续映射多为**只读**（除非拿到引用直接改原 `dict`）。

### 2. 与「合并成新 dict」对比

| 方式 | 新对象 | 与原 dict 同步 |
| :--- | :--- | :--- |
| `ChainMap(d1, d2)` | 否（视图） | 改原 dict 会反映到查找 |
| `{**d1, **d2}` / `d1 \| d2`（3.9+） | 是 | 否 |

### 3. 典型用途

- **配置覆盖**（默认 → 环境 → 本地）。  
- 教学上可类比**名字查找链**（如 `locals` → `globals` → `builtins`），真实解释器不限于此实现。

---

## 三、`collections.Counter`（§3.6.3）

- 为**可哈希对象**计数；是 **`dict` 子类**，值为整型计数。  
- 常用：**`update`** 累加、**`most_common(n)`**、集合式 **`+`/`-`**（见文档）。  
- 适合词频、频次表、与 **`defaultdict(int)`** 选型相近时，**API 更省事**。  
- **续**：**`abracadabra`** 式构造、**`&` / `|`**、与 **`shelve` / `UserDict`** 小结见 **`11-Counter与shelve及UserDict子类化.md`**。

---

## 四、选型简表

| 类型 | 何时用 |
| :--- | :--- |
| **`OrderedDict`** | 必须 **`move_to_end` / `popitem(last=False)`** 等顺序语义 |
| **`ChainMap`** | 多层默认值、零拷贝叠放、配置链 |
| **`Counter`** | 计数、`most_common`、与集合运算结合的统计 |

---

## 五、可运行对照

见 `dict_variants_demo.py`（`OrderedDict` 相等性与顺序、`ChainMap` 查找与写首表、`Counter`）。
