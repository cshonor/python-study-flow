# Python 序列与对象模型（合并版）：对象头 → 容器/扁平 → 可变性/哈希 → ABC

> **你要的一篇到底**：本文件把原 `02/03/04/05` 四篇合并成一个主文档，按“先对象模型、再序列实现、再接口/抽象、最后可变性与 key 规则”的顺序组织。  
> **配套脚本**：`container_vs_flat_memory_demo.py`、`sequence_virtual_subclass_demo.py`。

---

## 目录（建议按顺序读）

- 一、对象模型：名字绑定到对象、对象头、`ob_type`
- 二、容器序列 vs 扁平序列：载荷到底存什么
- 三、可变 vs 不可变：开放不开放“改自己”的接口
- 四、hashable 与 dict key：tuple 里藏 list 的坑
- 五、`collections.abc`：`Sequence` / `MutableSequence` 与虚拟子类
- 六、选型与小实验（`getsizeof`）

---

## 一、对象模型总览（CPython 实现直觉）

### 1. `a = 123` 到底发生了什么？

- `a` 是**名字**（标识符），不是装值的小盒子。
- `123` 求值产生一个 **`int` 对象**（CPython 中是 `PyLongObject`）。
- 赋值的语义是：**名字 `a` 绑定到该对象**（名字存放在当前栈帧/命名空间结构里）。

### 2. 对象头：`ob_refcnt` 与 `ob_type`

每个对象结构体开头都有统一的对象头（教学里叫 `PyObject_HEAD` / `PyObject_VAR_HEAD`），常记两样：

- **`ob_refcnt`**：引用计数
- **`ob_type`**：类型指针，类型为 **`PyTypeObject*`**

`ob_type` 的作用就是：让解释器知道“这是什么类型”，从而走对应的加法、取长度、repr 等实现逻辑（动态分派）。

> 一句话：**`ob_type` 是对象的类型身份证，指向它的类型对象（行为表）。**

---

## 二、容器序列 vs 扁平序列：载荷到底存什么？

### 1. 一句话

- **容器序列**（`list` / `tuple` / `deque`）：载荷是**对象引用槽位**（指向堆上的独立对象）→ **可异构**。
- **扁平序列**（`array.array` / `bytes` / `bytearray` / `str`）：载荷是**同构的连续缓冲**（原始编码）→ **紧凑但受限**。

### 2. 对照表

| 维度 | **容器序列** | **扁平序列** |
| :--- | :--- | :--- |
| **载荷层存什么** | 对象引用槽位 | 同构原始数据缓冲 |
| **典型代表** | `list`、`tuple`、`collections.deque` | `array.array`、`str`、`bytes`、`bytearray` |
| **是否异构** | ✅ | ❌（`array` 由类型码约束；`bytes` 为字节；`str` 为 Unicode 文本语义） |

### 3. 两个直觉例子

- `(9.46, 2.08, 4.29)`：每个元素通常是独立 `float` 对象（有对象头）。
- `array('d', [9.46, 2.08, 4.29])`：缓冲里紧排 `double`，通常更省。

---

## 三、可变 vs 不可变：是谁决定的？

> **一句话**：取决于这个类型是否开放“在同一对象身份下修改内容”的接口（协议层常体现为 `__setitem__`、`append`、`pop`…）。

### 1. 行为对比

```python
s = "hello"
# s[0] = "x"  # TypeError：str 不支持按索引写入

lst = [1, 2, 3]
lst[0] = 999   # OK
lst.append(4)  # OK
```

### 2. 重要提醒

`tuple` 自己不可变指的是**槽位绑定不变**；但若它装了可变对象（如 `list`），内层对象仍可变。

---

## 四、hashable 与 dict key（含 tuple 小坑）

字典 key 的最稳记法是：**必须可哈希（hashable）**。

- ✅ 常见可当 key：`str`、`bytes`、数字、`frozenset`、以及**元素全可哈希**的 `tuple`
- ❌ 常见不能当 key：`list`、`dict`、`set`、`bytearray`、`array.array`

### 小坑：`tuple` 不一定可哈希

```python
a = (1, 2, 3)       # ✅ OK
b = (1, [2, 3], 4)  # ❌ TypeError：tuple 内含 list（不可哈希）
```

---

## 五、`collections.abc`：接口层次与虚拟子类

### 1. 接口层次（记住方法集合超集关系就够）

- **`Sequence`**：偏“只读”序列语义（`__getitem__` 等），并混入 `index`、`count`
- **`MutableSequence`**：在 `Sequence` 上加“可原地改”（`append`、`pop`、`__setitem__` 等）

一句话：**`MutableSequence` 的方法集 ⊃ `Sequence` 的方法集**。

### 2. 为什么是虚拟子类？

内置 `list`/`tuple` 早就用 C 实现了，后来才有 ABC；因此它们不是通过 `__bases__` 继承 ABC，而是通过注册成为**虚拟子类**，从而让 `isinstance(x, abc.Sequence)` 这类检查成立。

可运行演示：`part-1-data-structures/chapter-02/sequence_virtual_subclass_demo.py`

---

## 六、选型与小实验

### 1. 选型表（极简）

| 场景 | 推荐 |
| :--- | :--- |
| 业务异构数据 | `list` / `tuple` |
| 同构数值批量 | `array.array`（或科学计算用 `numpy`） |
| 字节 IO | `bytes` / `bytearray` |
| 队列/滑动窗口 | `collections.deque` |

### 2. `getsizeof` 粗略感受（注意局限）

`sys.getsizeof(list)` 通常不含元素对象本体；演示脚本只给数量级直觉：

```bash
python part-1-data-structures/chapter-02/container_vs_flat_memory_demo.py
```
