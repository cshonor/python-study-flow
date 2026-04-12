# Python 容器 API：`collections.abc` 与抽象基类（ABC）

> 《流畅的 Python》相关脉络：用 **`collections.abc`** 理解「容器在协议层面长什么样」，以及它与**鸭子类型 / 特殊方法**的关系。

---

## 一、核心抽象（与 UML 常见画法对应）

容器相关抽象里，常出现三个「能力维度」：

1. **`Iterable`**：可迭代（`for`、解包、`iter()` 等路径之一成立即可）。
2. **`Sized`**：有长度（`len()` → `__len__`）。
3. **`Container`**：可做成员检测（`in` → 通常与 `__contains__` 相关；未实现时可能退化为遍历比较，见下文补充）。

在标准库中，**`Collection`** 可以理解为把 **Iterable + Sized + Container** 合在一起描述的「广义容器」接口（具体以当前 Python 版本的 `collections.abc` 为准）。

---

## 二、三大类容器分支（概念上）

`Collection` 之下，常见三大分支对应不同数据结构形态：

| 接口（概念） | 代表类型 | 核心特点 | 常涉及的能力 / 方法 |
| :--- | :--- | :--- | :--- |
| **Sequence** | `list`、`str`、`tuple` | 有序、可按整数索引/切片 | `__getitem__`、`__len__`；`index`/`count` 等 |
| **Mapping** | `dict`、`defaultdict` | 键到值的映射 | `__getitem__`、`keys`/`values`/`items` 等 |
| **Set** | `set`、`frozenset` | 无序、元素不重复 | `__contains__`；集合运算相关特殊方法等 |

**补充**：

- **字典顺序**：CPython 3.7+ 保证 `dict` **插入顺序**；教学上仍可把「映射」与「序列」在抽象上分开理解。
- **`reversed()`**：在标准库的 ABC 体系里，**序列**一侧常强调可反序迭代；映射/集合的「反序」不是同一套故事，因此教材/UML 里常说**只有序列这一路**与 `Reversible` 天然合拍。

---

## 三、鸭子类型：不必继承，但要「长得像」

要点：

> Python **不强制**你继承这些 ABC；很多时候只要实现了**对应特殊方法**，对象就能参与 `len`、`for`、`in` 等用法。

例如 `FrenchDeck`：

- 实现 `__len__`、`__getitem__` 后，在**用法上**往往像**类序列**（索引、切片、`for` 等）。
- **`isinstance(x, collections.abc.Sequence)`** 在**未继承、未 `register`** 时，不同 CPython 版本可能为 `True` 或 `False`（取决于该版本的 `__subclasshook__` 规则）；这与「`for` / `in` 能不能跑」**不是同一件事**——后者看的是运行时协议。
- 需要类型检查或静态工具友好时，可**显式** `Sequence.register(YourClass)` 或**继承**对应 ABC（按项目规范选择）。
- 这就是书中强调的**数据模型 + 协议**思路，和「非要继承某个接口」的静态语言习惯不同。

**和 `in` 的关系（精读）**：

- 运行时 `item in deck` 可能走 `__contains__`，也可能在**未实现**时退化为**遍历**（依赖迭代路径）。
- 若你要写类型注解或强调「容器契约」，可显式实现 `__contains__`，或参考标准库文档对 `Container` 的说明。

---

## 四、与前面 `FrenchDeck` 笔记的关联

`FrenchDeck` 是典型的「**隐式满足协议**」：

- `__len__` → **Sized** 能力（`len`）。
- `__getitem__` → 序列式访问；并常与 **`for` / 迭代**路径配合（书中讲的「序列式迭代」场景）。
- `in`：可能用 `__contains__`（若实现），或走**遍历**回退。

因此它**不必**继承 `list`，也能在用法上「像列表一样工作」。

---

## 五、为什么要了解 `collections.abc`？

- **更 Pythonic 的设计**：优先想「要实现哪些特殊方法」，而不是「要继承谁」。
- **类型注解**：例如 `def f(seq: Sequence[int]) -> None:` 比写死 `list` **更通用**（任何实现序列协议的对象都可能适用）。
- **读第三方库**：许多数组/表格类也围绕这些协议做 API，读源码时更好对齐心智模型。

---

## 六、可运行示例

同目录：`12_collections_abc_minimal_demo.py`：一个只实现 `__len__` + `__getitem__` 的小类，打印若干 `isinstance(..., abc.XXX)` 的结果，便于和本节对照。

```bash
python part-1-data-structures/chapter-01/12_collections_abc_minimal_demo.py
```
