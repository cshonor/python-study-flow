# Python 容器 API：`collections.abc` 与抽象基类（ABC）

> 《流畅的 Python》核心脉络：用 **`collections.abc`** 理解 **容器协议（接口）**、**鸭子类型**、**特殊方法** 三者关系；与 UML 里「Iterable / Sized / Container → Collection → Sequence|Mapping|Set」的常见画法一一对应。

---

## 一、三大基础能力（容器的最小接口）

所有「像容器」的对象，都可以从三个维度问：**能不能迭代、有没有长度、能不能做 `in`**。

1. **`Iterable`**
   - **能力**：可迭代（`for`、`*` 解包、`iter(obj)` 等路径之一成立即可）。
   - **对应方法**：优先 **`__iter__`**；历史上若只有 **`__getitem__`**（整数下标 0,1,2…），解释器仍可能通过「序列式迭代」驱动 `for`（与 `Iterable` 的 `isinstance` 检测**不是**同一条规则，见第七节）。

2. **`Sized`**
   - **能力**：`len(obj)`。
   - **对应方法**：`__len__`。

3. **`Container`**
   - **能力**：`x in obj`。
   - **对应方法**：显式 **`__contains__`** 最理想；未实现时可能退化为 **`__iter__` 遍历**，再退化为 **`__getitem__` 按索引遍历**（见第四节）。

**广义容器（`Collection`，以当前 `collections.abc` 为准）**

- 可理解为 **`Collection` ≈ `Iterable` + `Sized` + `Container`**：能 `len()`、能 `for`、能 `in` 的对象，在抽象层面都可归入「广义容器」讨论。

---

## 二、三大容器分支（Sequence / Mapping / Set）

### 2.1 接口体系（概念）

| ABC 接口 | 代表类型 | 核心特点 | 必须方法（抽象侧，以标准库为准） | 常用 mixin（继承后可「白嫖」） |
| :--- | :--- | :--- | :--- | :--- |
| **Sequence** | `list`、`tuple`、`str` | 有序、整数索引、切片 | `__getitem__`、`__len__` | `index`、`count`、`__contains__`、`__reversed__` 等 |
| **Mapping** | `dict`、`defaultdict` | 键 → 值 | `__getitem__`、`__iter__`、`__len__` | `keys`、`values`、`items`、`get` 等 |
| **Set** | `set`、`frozenset` | 无序、去重、集合代数 | `__contains__`、`__iter__`、`__len__` | `&`、`|`、`-`、`^`、`<=`、`<` 等 |

### 2.2 重要补充

- **`dict` 有序**：CPython 3.7+ 起语言规范保证 **`dict` 插入有序**；抽象上仍是 **Mapping**，**不是** Sequence（没有「整数位置」的 `deck[i]` 语义，也没有序列式切片）。
- **`reversed()`**：与 **`Reversible`** / `__reversed__` 天然合拍的是 **Sequence** 这一路；Mapping / Set 的「反序」没有统一标准语义，不要硬套。

---

## 三、鸭子类型 vs ABC：「像」≠「是」

### 3.1 核心思想（《流畅的 Python》重点）

> Python **不强制**继承 ABC：只要实现了**对应特殊方法**，对象往往就能参与 `len` / `for` / `in`。  
> **`isinstance` / `issubclass`** 是**类型层级上的判断**（含 `__subclasshook__`、`register` 等），**不是**「这段代码运行时会不会报错」的完整替代。

### 3.2 以 `FrenchDeck` 为例（经典）

```python
import collections

Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(r, s) for s in self.suits for r in self.ranks]

    def __len__(self) -> int:  # → Sized
        return len(self._cards)

    def __getitem__(self, i):  # → 索引、切片；并常驱动「序列式」for
        return self._cards[i]
```

#### 用法（「像」序列）

```python
deck = FrenchDeck()
len(deck)  # 52
deck[0]  # Card(rank='2', suit='spades')
deck[::2]  # 切片
for card in deck:
    ...
# 成员检测：元素是 Card，应与 Card 比较（不要误以为 'J' in deck 一定为 True）
Card("J", "spades") in deck  # True
```

#### 类型检查（关键区别）

```python
from collections.abc import Sequence, Iterable, Sized

# 以下结果以「你本机 CPython 大版本」为准：ABC 的 __subclasshook__ 可能随版本调整
isinstance(deck, Sized)  # 通常 True（有 __len__）
isinstance(deck, Iterable)  # 现代版本常 True（仅 __getitem__ 也可能被识别）
isinstance(deck, Sequence)  # 未继承、未 register 时：可能 True，也可能 False——不要死记
```

### 3.3 为什么会扯上 `__subclasshook__`？

- 许多 ABC 带 **`__subclasshook__`**：在**未显式继承**时，也能按「类上是否挂有某组方法」把第三方类判成虚拟子类。
- 例如 **`Sized`** 常只盯 **`__len__`**；**`Sequence`** 会盯 **`__getitem__` + `__len__`** 等组合。
- 规则可能微调 → **不要用 `isinstance(x, Iterable)` 代替「能不能迭代」的工程判定**；更稳的是 **`iter(x)`** 或 **`try` / `except TypeError`**（见第七节）。

### 3.4 显式声明 ABC（工程规范）

需要 **IDE / 类型检查器 / 文档契约** 更明确时：

```python
from collections.abc import Sequence

# 方式 1：继承 ABC（必须实现抽象方法，由 ABC 保证形状）
class FrenchDeck(Sequence):
    def __len__(self): ...
    def __getitem__(self, i): ...

# 方式 2：register 虚拟子类（不改变继承链，只影响 issubclass / isinstance）
Sequence.register(FrenchDeck)  # 若类已存在且不便改基类
```

---

## 四、`in` 操作的底层逻辑（精读）

对 **`item in obj`**，CPython 大致顺序为：

1. 若有 **`__contains__`** → 调用它（复杂度取决于实现：可能是 O(1)、O(log n)…）。
2. 若无 **`__contains__`**，但有 **`__iter__`** → 在迭代上比较（常见 O(n)）。
3. 若再退回 **`__getitem__`** → 按 `0, 1, 2, …` 取下标直到 `IndexError`（常见 O(n)）。

**工程建议**：自定义容器若频繁做 **`in`**，应**显式实现 `__contains__`**，避免无意中的全表扫描。

---

## 五、为什么要学 `collections.abc`？

1. **更 Pythonic 的设计**：先想「要暴露哪些**特殊方法** / 协议」，而不是先想「继承哪棵树」。
2. **类型注解更通用**：

   ```python
   from collections.abc import Sequence

   # 好：接受 list / tuple / str / 自研序列等
   def process(seq: Sequence[int]) -> None: ...

   # 坏（过窄）：只接受 list
   def process(seq: list[int]) -> None: ...
   ```

3. **读源码 / 第三方库**：NumPy、pandas 等大量 API 与「序列 / 映射 / 集合」协议对齐，认识 ABC 更容易读类型签名与 mixin 行为。
4. **自定义容器**：继承 **`Sequence` / `MutableSequence`** 等可**免费获得**大量 mixin 方法（`index`、`count`、部分 `__contains__` 逻辑等），减少样板代码。

---

## 六、可运行示例（与本节对照）

### 6.1 仓库自带：`12_collections_abc_minimal_demo.py`

同目录脚本：实现 **`__len__` + `__getitem__` + `__contains__`** 的 `MiniSeq`，分步打印 **`isinstance(..., abc.XXX)`** 以及 **`Sequence.register` 前后**的差异——专门用来钉死「**运行时能用**」和「**ABC 认不认**」不是一回事。

```bash
python part-1-data-structures/chapter-01/12_collections_abc_minimal_demo.py
```

### 6.2 最小 REPL 片段（仅 `__len__` + `__getitem__`）

```python
from collections.abc import Iterable, Sized, Container, Sequence, Mapping, Set


class MySeq:
    def __len__(self) -> int:
        return 10

    def __getitem__(self, i):
        return i


s = MySeq()
print("Sized      ->", isinstance(s, Sized))
print("Iterable   ->", isinstance(s, Iterable))
print("Container  ->", isinstance(s, Container))
print("Sequence   ->", isinstance(s, Sequence))  # 以本机为准
print("Mapping    ->", isinstance(s, Mapping))
print("Set        ->", isinstance(s, Set))
```

> **`Container`**：在无 `__contains__` 时，现代 CPython 的 `Container.__subclasshook__` 仍可能因存在 **`__iter__` / `__getitem__`** 而返回 True；与第四节「`in` 的实际查找顺序」合在一起记，避免背公式背拧。

---

## 七、面试高频陷阱

1. **`isinstance` ≠ 功能测试**
   - 能写 `for x in obj` 也不等于 **`isinstance(obj, Iterable)`** 一定为 True（历史上 `Iterable` 更强调 `__iter__`；与「序列式迭代」路径别混）。
   - 更稳的「可迭代吗」：**`iter(obj)`** 或 **`collections.abc` + 你项目约定的类型**。

2. **`Sequence` ≠「有序」的全部故事**
   - `dict` 3.7+ **插入有序**，但仍 **不是** Sequence（无整数位置索引 / 切片语义）。

3. **`__getitem__` 很强，但不是魔法**
   - 配合 **`__len__`** 常能驱动索引、切片、**序列式** `for`；**`in`** 仍可能走 **`__contains__` 或遍历**（第四节）。
   - 元素类型要与 **`in`** 的左操作数匹配：例如 **`Card('J', 'spades') in deck`**，不要想当然 **`'J' in deck`**。

4. **ABC 是接口契约，不是「默认实现大礼包」**
   - 继承 ABC 主要保证**方法集合**；真正省代码的是 **mixin**；未继承时**不会**自动获得 `index`/`count` 等。

---

## 八、与前面 `FrenchDeck` 笔记的关联（小结）

| 特殊方法 | 常见能力维度 | 与 `FrenchDeck` |
| :--- | :--- | :--- |
| `__len__` | **Sized** | `len(deck)` |
| `__getitem__` | 序列式访问；常驱动 **for** | `deck[i]`、切片、迭代 |
| `in` | **Container** 语义 / 或遍历回退 | 应对 **`Card`** 做成员检测，必要时自写 **`__contains__`** |

**不必继承 `list`**，也能在用法上「像序列」——这就是 **Python 数据模型 + 协议** 的精髓；**`collections.abc`** 则是把这套协议**说清、画全、写进类型系统**的工具箱。

---

## 附录：一页背诵用（可自行打印）

- **三能力**：Iterable / Sized / Container → **Collection**。  
- **三分支**：Sequence / Mapping / Set。  
- **`in`**：`__contains__` → `__iter__` → `__getitem__` 下标扫。  
- **鸭子类型**：能跑 ≠ `isinstance`；契约用 **继承 ABC** 或 **`register`**。  
- **命令**：`python part-1-data-structures/chapter-01/12_collections_abc_minimal_demo.py`
