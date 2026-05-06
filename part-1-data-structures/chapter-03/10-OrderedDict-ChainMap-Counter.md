# `dict` 的变体：`OrderedDict`、`ChainMap`、`Counter`（§3.6）

`dict` 够用了，但标准库还提供了几种“带特殊能力”的映射类型。你可以把它们理解成：

- **`OrderedDict`**：当你需要“显式控制顺序”（例如把某个 key 移到末尾）时用。  
- **`ChainMap`**：当你需要“多层查找（覆盖）”而不是“真合并”时用。  
- **`Counter`**：当你在做“计数/词频/多重集运算”时用（比自己写 `d.get(k, 0) + 1` 更直接）。

配套脚本：`10_dict_variants_demo.py`。

---

## 零、三样变体，各管一件文雅事（总览）

### 一）`OrderedDict`：管**顺序**

**一句话**：**能精确摆弄键顺序的字典**——适合顺序敏感、要像队列那样从一端弹出的场景。

- **Python 3.7+** 起，普通 **`dict` 已保证插入顺序**；**`OrderedDict` 仍值得用**的时候，多半是你要**额外 API**：**`move_to_end(key)`** 把键挪到队尾/队首，或 **`popitem(last=False)`** 做 **FIFO**（先插入的先出）。  
- 另：**两个 `OrderedDict` 若键顺序不同，可能 `==` 为假**（与普通 `dict` 的相等习惯不同，见 **§一**）。

### 二）`ChainMap`：管**多层查找**

**一句话**：**把多只字典叠成一条查找链**——从前到后找到第一个有该键的就返回；**不复制、不合并成一只新 dict**，底层映射改了，链上的视图也跟着变。

- 典型：**默认配置 → 环境 → 本地** 一层层盖住；不想拷贝大块数据，只想**覆盖语义**的读。

### 三）`Counter`：管**计数**

**一句话**：**为「出现次数」而生的字典子类**——喂 iterable，它帮你聚成 **`{元素: 次数}`**；**`most_common(n)`** 直接拿前几名；**`+` / `-` / `&` / `|`** 做计数层面的集合式运算。

- 词频、打分、统计表：**API 往往比手写 `defaultdict(int)` 更省事**（选型对照见 **`06-dict-defaultdict与OrderedDict对照.md`**）。

### 三句口诀（好记）

1. **`OrderedDict`**：**顺序**我作主——**能移、能 FIFO 弹、顺序还能参与相等判断**。  
2. **`ChainMap`**：**多层**叠着查——**像配置覆盖，零拷贝链式找**。  
3. **`Counter`**：**数数**最省事——**词频排行、计数运算一把梭**。

---

## 一、`collections.OrderedDict`（§3.6.1）

### 1. 与原生 `dict`（Python **3.7+** 语言保证插入顺序）

- **3.7+** 的 `dict` 已保证**插入顺序**；仅当需要 **`move_to_end`**、**`popitem(last=...)` 的 FIFO/LIFO 控制**、或与旧代码协同时，再选 **`OrderedDict`**。  
- **相等性**：两个 **`OrderedDict`** 若**键顺序不同**，可能 **`==` 为假**；**`OrderedDict` 与普通 `dict`** 在键值集合相同时，**通常仍按映射相等**（顺序不阻等）。以当前 CPython 行为为准，见 `10_dict_variants_demo.py`。

```python
from collections import OrderedDict

od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])

od1 == od2                 # False：顺序不同可判不等
od1 == {"a": 1, "b": 2}    # True：与普通 dict 常仍「映射相等」（以 CPython 为准）
```

### 2. 顺序 API（与 `06` 呼应）

- **`move_to_end(key, last=True)`**  
- **`popitem(last=True)`**：`last=False` 时从**先插入端**弹出（FIFO）。

```python
from collections import OrderedDict

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("a")  # 把 a 挪到「最后插入」端 → 键序 …, a
od.move_to_end("c", last=False)  # c 挪到「最先插入」端
k, v = od.popitem(last=False)    # FIFO：弹出当前最「老」的一项
```

---

## 二、`collections.ChainMap`（§3.6.2）

### 1. 原理

- **不复制**子映射，只保存**引用**；查找时从**前到后**第一个含该键的映射取值。  
- **写入**（含新键）：默认落在**第一个**映射上；后续映射多为**只读**（除非拿到引用直接改原 `dict`）。

```python
from collections import ChainMap

d1 = {"a": 1, "b": 3}
d2 = {"a": 2, "b": 4, "c": 6}
chain = ChainMap(d1, d2)

chain["a"], chain["c"]  # (1, 6)：a 命中 d1，c 只在 d2

chain["c"] = -1         # 写入落在「第一个」映射 → 改的是 d1
# d1 新增 'c': -1；d2['c'] 仍为 6（除非你再通过 d2 引用去改）
```

### 2. 与「合并成新 dict」对比

| 方式 | 新对象 | 与原 dict 同步 |
| :--- | :--- | :--- |
| `ChainMap(d1, d2)` | 否（视图） | 改原 dict 会反映到查找 |
| `{**d1, **d2}` / `d1 \| d2`（3.9+） | 是 | 否 |

```python
d1, d2 = {"a": 1}, {"a": 2, "b": 3}
cm = ChainMap(d1, d2)
snap = {**d1, **d2}  # 或 Python 3.9+：d1 | d2

d1["a"] = 99
cm["a"], snap["a"]   # ChainMap 读到 99；snap 仍是合并当时的快照
```

### 3. 典型用途

- **配置覆盖**（默认 → 环境 → 本地）。  
- 教学上可类比**名字查找链**（如 `locals` → `globals` → `builtins`），真实解释器不限于此实现。

```python
from collections import ChainMap

defaults = {"host": "127.0.0.1", "port": 8000}
overrides = {"port": 9000}
cfg = ChainMap(overrides, defaults)

cfg["host"], cfg["port"]  # 127.0.0.1, 9000 —— 高优先级表盖住默认
```

---

## 三、`collections.Counter`（§3.6.3）

- 为**可哈希对象**计数；是 **`dict` 子类**，值为整型计数。  
- 常用：**`update`** 累加、**`most_common(n)`**、集合式 **`+` / `-` / `&` / `|`**（各键取和、差、min、max；细节见文档与 **`11`**）。  
- 适合词频、频次表、与 **`defaultdict(int)`** 选型相近时，**API 更省事**。  
- **续**：**`abracadabra`** 式构造、**`&` / `|`**、与 **`shelve` / `UserDict`** 小结见 **`11-Counter与shelve及UserDict子类化.md`**。

```python
from collections import Counter

c = Counter("abracadabra")
c.update("aaa")           # 同键累加
c.most_common(3)          # [('a', 8), ('b', 2), ('r', 2)]（以实际计数为准）

c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
c1 + c2, c1 & c2          # 并计数 / 取各键 min
```

---

## 四、选型简表

（与 **§零** 三句口诀同一脉络，这里是「查表版」。）

| 类型 | 何时用 |
| :--- | :--- |
| **`OrderedDict`** | 必须 **`move_to_end` / `popitem(last=False)`** 等顺序语义 |
| **`ChainMap`** | 多层默认值、零拷贝叠放、配置链 |
| **`Counter`** | 计数、`most_common`、与集合运算结合的统计 |

---

## 五、可运行对照

见 **`10_dict_variants_demo.py`**（与 **§一–§三** 代码块同一脉络）：

1. **`OrderedDict`**：**`move_to_end`**、**`popitem(last=False)`**、**`==`** 与顺序 / 普通 **`dict`**（**§一**）  
2. **`ChainMap`**：查找链、**写首表**、与 **`locals`/`globals`/`builtins`** 的教学类比（**§二**）  
3. **`Counter`**：**`most_common`**、**`update`**、**`+` / `&`**（**§三**；**`abracadabra`** 全量演示见 **`11`**）
