# 序列的两套分类：《流畅的 Python》视角（可变/不可变 × 扁平/容器 + `collections.abc`）

> **本篇定位**：把《流畅的 Python》里序列的两套分类（**可变/不可变**、**扁平/容器**）与 **`collections.abc` 的接口层次**串起来，并解释「虚拟子类」与 `register`。  
> **前置**：对象头、`ob_type` 等实现直觉见 `04-python-object-model-a-equals-123.md`。  
> **深入**：扁平 vs 容器的存储布局与选型见 `02-container-vs-flat-sequences.md`；可变/不可变与 hashable 规则见 `05-mutability-open-api-and-hash.md`；一页纸骨架见 `01-rich-sequences-chapter2-overview.md` §二。

---

## 一、扁平序列 vs 容器序列（先给一句话）

| 维度 | **扁平序列（Flat Sequence）** | **容器序列（Container Sequence）** |
| :--- | :--- | :--- |
| **存储内容** | 载荷区直接放**原始机器级编码**（字节、定宽整数/浮点等） | 槽位里是**对象引用**，指向堆上的独立对象 |
| **内存布局** | 连续、紧凑；元素一般**不再各自占一个完整 `PyObject` 壳**（相对「一堆小标量 float」而言） | 多层间接；元素常为完整 Python 对象，开销更大 |
| **典型代表** | `str`、`bytes`、`bytearray`、`array.array` | `list`、`tuple`、`collections.deque` |
| **限制** | **同构**、不能当通用「装任意对象」的篮子 | **可异构**、可嵌套 |

---

## 二、为什么扁平更紧凑：以 `float` 为例（只保留直觉）

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

## 三、可变序列 vs 不可变序列（设计权衡 + ABC + 虚拟子类）

### 1. 分类

| 可变 / 不可变 | 含义（笔记级） | 典型内置序列 |
| :--- | :--- | :--- |
| **可变** | 可原地改元素、增删（视类型而定） | `list`、`bytearray`、`array.array`、`collections.deque` |
| **不可变** | 创建后不能改元素、不能增删槽位 | `tuple`、`str`、`bytes` |

### 2. 为什么有的是可变，有的是不可变？（安全 vs 性能 vs 语义）

本质是在不同场景下换一组**默认保证**：

| 特性 | **不可变**（`tuple`、`str`、`bytes`） | **可变**（`list`、`bytearray`、`deque` 等） |
| :--- | :--- | :--- |
| **核心优势** | 可哈希（在元素可哈希的前提下）、易共享、无副作用顾虑 | 原地修改、少分配新对象、适合频繁更新 |
| **语义** | 偏「值」：内容不变则行为稳定 | 偏「容器状态」：同一对象可被多处看到其变化 |
| **典型用途** | 常量数据、需要作 `dict`/`set` 键的**不可变**组合、跨线程只读共享 | 动态列表、队列、缓冲 |

- **不可变**：把 `tuple` 传给函数，调用方通常**不担心**被偷偷原地改掉（仍要注意**可变元素**，如 `tuple` 里嵌 `list`）。
- **可变**：避免「每次小改都新建整段序列」的开销；`list` 等底层还有**预留容量**等策略（实现细节），与「可 growing」语义一致。

### 3. 底层直觉（和内存模型对齐）

- **不可变**：对象一旦建成，**语义上**内容不再变；实现上可配合**驻留/复用**（如小字符串、小整数），哈希结果稳定。
- **可变**：允许**原地**更新，内部常带**额外容量**与长度管理；**同一对象**被多处引用时，一处修改会**被所有人看见**——因此默认**不可哈希**，也不宜当作「不会变的键」。

### 4. `collections.abc` 中的接口层次（概念）

内置序列**并不**都在 Python 层写成 `class list(MutableSequence)`，但 **`collections.abc`** 描述了**统一协议**：

| ABC | 角色（笔记级） |
| :--- | :--- |
| **`Collection`** | 可迭代、有长度、支持 `in`：`__iter__`、`__len__`、`__contains__` |
| **`Reversible`** | 支持 `__reversed__` |
| **`Sequence`** | 序列语义（如 `__getitem__`）；混入 `index`、`count` 等默认实现 |
| **`MutableSequence`** | 在 `Sequence` 之上增加**原地修改**：`append`、`pop`、`extend`、`insert` 等 |

**MRO 细节**随版本可能微调；记**「`MutableSequence` 的方法集 ⊃ `Sequence` 的方法集」**（只读操作 + 修改操作）。

### 5. 「可变序列继承了不可变序列的方法」是什么意思？

这句话指的是**接口 / 方法集合上的包含关系**，**不是**说 `list` 在 Python 里 **`class list(tuple)`** 这种类继承。

- **`Sequence`**（只读侧）：`__getitem__`、`__iter__`、`__contains__`、`index`、`count` 等。
- **`MutableSequence`**：**包含上述只读能力**，并**额外**有 `append`、`pop`、`__setitem__`、`__delitem__` 等。

因此：**可变序列能做的「读」操作，与不可变序列在协议上对齐；再多一批「写」操作。**

```python
t = (1, 2, 3)
# t[0] = 0   # TypeError：不可变
# t.append(4)  # AttributeError

lst = [1, 2, 3]
lst[0] = 0     # OK
lst.append(4)  # OK
lst[0]         # 只读访问与 tuple 一样「能用」
```

### 6. 为什么是「虚拟子类」而不是直接继承？

- **真实继承**：你写的 `class B(A)`，`A` 在 `B.__bases__` 里。
- **虚拟子类**：`list`、`tuple` 等**内置类型**早在 **`collections.abc`** 之前就用 C 实现好了，**不能**再改写成「继承某个 ABC」。于是 CPython 用 **`register`**（及内置等价注册）把它们登记为 `Sequence` / `MutableSequence` 的**虚拟子类**。

**常见原因（笔记级）**

1. **历史与实现**：内置类型与 ABC 不同步诞生，**松耦合**：用协议 + 可选注册，而不是强制所有序列继承同一棵 Python 类树。  
2. **`isinstance` / `issubclass`**：注册后仍可得 `isinstance([], abc.MutableSequence) is True`，同时 **`list.__bases__` 仍是 `(object,)`**：

```python
from collections import abc

isinstance((1, 2, 3), abc.Sequence)      # True
isinstance([1, 2, 3], abc.MutableSequence)  # True
list.__bases__  # (<class 'object'>,)，一般不含 abc.MutableSequence
```

3. **自定义类**：若只实现 `__len__`、`__getitem__` 等，**鸭子类型**上可当序列用；但若要让 **`isinstance(x, abc.Sequence)`** 为真，通常需要 **`abc.Sequence.register(YourClass)`** 或**显式继承** `abc.Sequence`（见下节脚本）。

**不要混淆**：「能当序列用」≠「`isinstance(..., Sequence)` 一定为真」；后者依赖**注册/继承**或你使用的类型检查策略（如 `typing.Protocol` 的运行时方案等，另论）。

可运行示例：`part-1-data-structures/chapter-02/sequence_virtual_subclass_demo.py`

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
- 可变/不可变的**开放接口**与哈希：`05-mutability-open-api-and-hash.md`
- 内存与 `PyObject*`：`02-container-vs-flat-sequences.md`
- 第 2 章路线：`01-rich-sequences-chapter2-overview.md`
- 容器 ABC 与 `FrenchDeck`：`chapter-01/12-collections-abc-container-api.md`
- 虚拟子类演示脚本：`sequence_virtual_subclass_demo.py`
