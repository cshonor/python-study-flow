# 序列的两套分类：《流畅的 Python》视角（扁平/容器 × 可变/不可变 + `collections.abc`）

> 与 `02-container-vs-flat-sequences.md` 配套：**那一篇**侧重内存、`PyObject*` 与多语言对照；**本篇**按书里思路，把「扁平 vs 容器」「可变 vs 不可变」和 **ABC 继承**、**交叉表**收拢成一块。  
> **与书对齐的一页纸骨架**（对象头 + 两套分类 + ABC）：`01-rich-sequences-chapter2-overview.md` **§二**。

---

## 一、核心概念：扁平序列 vs 容器序列

| 维度 | **扁平序列（Flat Sequence）** | **容器序列（Container Sequence）** |
| :--- | :--- | :--- |
| **存储内容** | 载荷区直接放**原始机器级编码**（字节、定宽整数/浮点等） | 槽位里是**对象引用**，指向堆上的独立对象 |
| **内存布局** | 连续、紧凑；元素一般**不再各自占一个完整 `PyObject` 壳**（相对「一堆小标量 float」而言） | 多层间接；元素常为完整 Python 对象，开销更大 |
| **典型代表** | `str`、`bytes`、`bytearray`、`array.array` | `list`、`tuple`、`collections.deque` |
| **限制** | **同构**、不能当通用「装任意对象」的篮子 | **可异构**、可嵌套 |

---

## 二、以浮点数为例：`PyFloatObject` 与 `array('d')` 的对比

Python 里一个「单独的 `float`」也是**堆上的对象**，带通用头；CPython 里可理解为类似：

```c
typedef struct {
    PyObject_HEAD;   /* 含引用计数、类型指针等 */
    double ob_fval;  /* IEEE double 载荷 */
} PyFloatObject;
```

- **`PyObject_HEAD`**：实现里展开为引用计数、`ob_type`（指向类型对象）等，用于管理与动态分派。
- **`ob_fval`**：真正的双精度值。

**对比记忆**（数量级直觉，非精确 benchmark）：

- **`array.array('d', [1.1, 2.2, ...])`**：缓冲里**紧排 `double`**，没有「每个数一个 `PyFloatObject`」那种普遍情况。
- **`(1.1, 2.2, ...)`**（或等价地由浮点构成的 `tuple`）：每个元素往往是**独立的 `PyFloatObject`**（头 + 值），总开销通常明显高于同长度的 `array('d')`。

（写笔记时避免写成 `tuple(1.1, 2.2)`：`tuple()` 只接受**一个**可迭代对象；字面量用 `(1.1, 2.2)`。）

---

## 三、另一套轴：可变序列 vs 不可变序列

### 1. 分类

| 可变 / 不可变 | 含义（笔记级） | 典型内置序列 |
| :--- | :--- | :--- |
| **可变** | 可原地改元素、增删（视类型而定） | `list`、`bytearray`、`array.array`、`collections.deque` |
| **不可变** | 创建后不能改元素、不能增删槽位 | `tuple`、`str`、`bytes` |

### 2. `collections.abc` 中的接口层次（概念）

内置序列**并不**在 Python 里多重继承出一棵显式类图，但 **`collections.abc`** 用抽象基类描述了**统一协议**：

| ABC | 角色（笔记级） |
| :--- | :--- |
| **`Collection`** | 可迭代、有长度、支持 `in`：`__iter__`、`__len__`、`__contains__` |
| **`Reversible`** | 支持 `__reversed__` |
| **`Sequence`** | 在 `Collection` 等之上强调**按整数下标取值**等序列语义（如 `__getitem__`）；还提供 `index`、`count` 等混入式默认实现 |
| **`MutableSequence`** | 在 `Sequence` 上增加**原地修改**：如 `append`、`pop`、`extend`、`insert` 等（具体方法以文档为准） |

**MRO 细节**随版本可能微调，考试/面试记**「Sequence ⊃ 有序按索引；MutableSequence ⊃ 可原地改」**即可。

### 3. 虚拟子类（`register` / 内置注册）

很多内置类型**并没有**在源码里写 `class list(MutableSequence)`，但通过 **ABC 的注册机制**成为**虚拟子类**，于是：

```python
from collections import abc

issubclass(tuple, abc.Sequence)           # True
issubclass(list, abc.MutableSequence)    # True
```

与「鸭子类型」可并存：既可以用 **`isinstance(x, abc.Sequence)`** 做宽检查，也可以继续按实际支持的方法使用对象。更细的讨论见：`chapter-01/12-collections-abc-container-api.md`。

---

## 四、两套划分的交叉（书里常用总表）

| 类型 | 可变 / 不可变 | 扁平 / 容器 | 适用场景（笔记级） |
| :--- | :--- | :--- | :--- |
| `list` | 可变 | 容器 | 通用异构数据、业务结构 |
| `tuple` | 不可变 | 容器 | 轻量记录、多返回值、需哈希时作键的一部分（元素须可哈希） |
| `str` | 不可变 | 扁平 | 文本 |
| `bytes` | 不可变 | 扁平 | 二进制只读数据、IO |
| `bytearray` | 可变 | 扁平 | 需原地改的字节缓冲 |
| `array.array` | 可变 | 扁平 | 大规模同构数值、与 C/文件格式对接 |
| `collections.deque` | 可变 | 容器 | 双端队列、滑动窗口 |

---

## 五、设计思想小结（可抄进笔记）

1. **容器序列**：为**动态类型与异构**服务，用**引用槽位**换通用性，牺牲部分内存密度与缓存友好性。
2. **扁平序列**：为**同构数据**服务，用**定宽/字节语义**换紧凑与吞吐，牺牲「一篮装万物」。
3. **可变 / 不可变**：在**数据一致性、可哈希、安全共享**与**原地修改效率**之间做产品级划分；两套轴（扁平/容器 × 可变/不可变）**交叉**即可覆盖常见内置序列选型。

---

## 六、延伸阅读

- 以 `a = 123` 串起来的零基础总览：`04-python-object-model-a-equals-123.md`
- 内存与 `PyObject*`：`02-container-vs-flat-sequences.md`
- 第 2 章路线：`01-rich-sequences-chapter2-overview.md`
