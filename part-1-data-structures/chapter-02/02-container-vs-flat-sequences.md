# Python 容器序列 vs 扁平序列：底层设计与原理剖析（聚焦：存储布局）

> **本篇定位**：只讲一件事——**序列的载荷到底是「对象引用」还是「原始数据缓冲」**，以及由此带来的取舍与选型。  
> **前置**：如果你对「名字绑定到对象、对象头、`ob_type`、`PyObject*`」还不稳，先看 `04-python-object-model-a-equals-123.md`。  
> **相关**：可变/不可变与 hashable 规则见 `05-mutability-open-api-and-hash.md`；ABC 与虚拟子类见 `03-sequence-flat-container-mutable-immutable-abc.md`。

---

## 一、扁平序列 vs 容器序列：一句话区分 + 对照表

### 一句话

- **容器序列**（`list` / `tuple` / `deque`）：内部是**引用**；每个引用指向堆上的独立对象；**可异构**；灵活、通用，相对更占空间、访问路径更长。
- **扁平序列**（`array.array` / `str` / `bytes` / `bytearray`）：内部是**同构载荷的连续缓冲**（定宽或字节语义）；**不能塞任意 Python 对象**；紧凑、适合大批量同构数据或二进制。

### 对照表

| 维度 | **容器序列** | **扁平序列** |
| :--- | :--- | :--- |
| **本质（概念）** | **引用**的序列 | **连续缓冲区**里的同构原始数据 |
| **典型代表** | `list`、`tuple`、`collections.deque` | `array.array`、`str`、`bytes`、`bytearray` |
| **元素类型** | **可异构** | **同构**（`array` 由类型码约束；`str`/`bytes` 各自一种元素语义） |
| **能否放 `list`/自定义对象** | 可以 | **不可以**（只能按类型的「元素」编码） |

**`tuple` 补充**：不可变的是「槽位不能换绑定」；若元素是可变对象（如内层 `list`），仍可通过该对象修改内容。

---

## 二、「扁平序列里是不是只能放基本数据类型？」

**在「能放什么 Python 对象」这个意义上：可以记成「只能放一种内置元素语义，不能混类型、不能嵌 Python 对象」。**

更具体：

- `array.array('i')`：C 风格有符号整型（一种类型码）。
- `array.array('d')`：`double`（一种类型码）。
- `str`：**文本**，元素语义是 Unicode 字符（**不是**随便混 `int` 与 `str`）。
- `bytes` / `bytearray`：**0–255 的字节值**。

它们**不能像 `list` 那样**装「另一个 `list`、元组、自定义实例」等一般对象；**扁平序列不是装 `PyObject*` 的通用容器**。

---

## 三、四句话终极总结（可原样抄进笔记）

1. Python 没有 C 式「栈里嵌值」模型；**常用说法**是：**对象在堆、名字是引用**（实现细节如小对象池不改变语义）。
2. **`list`、`tuple`、`deque` 都是容器序列**：内部是引用，**可异构**，灵活、通用，相对更占空间、访问更间接。
3. **`array.array`、`str`、`bytes`、`bytearray` 是扁平序列**：内部是同构连续缓冲，**不能混类型、不能当通用对象容器**。
4. **基础类型**常记为：`int`、`float`、`bool`、`complex`、`str`、`bytes`、`bytearray`；**容器序列**可以指向它们，也可以指向**任意其他对象**。

---

## 四、图解思路：内存结构的直观对比

### 容器序列示例 `(9.46, 'cat', [2.08, 4.29])`

- 外层是 **`tuple` 对象**。
- 内部通常是**三个槽位**，各保存一个**引用**，分别指向堆上的 `float`、`str`、`list`（该 `list` 再引用其元素）。
- **特点**：可混类型、可嵌套；多一层间接；缓存友好性通常不如紧凑块。

### 扁平序列示例 `array('d', [9.46, 2.08, 4.29])`

- 外层是 **`array` 对象**。
- 内部是**连续缓冲区**，按 `double` 宽度排布**原始字节**。
- **特点**：相对「`list` 里一万个独立 `float` 对象」更省；**只能**保持 `double` 这一种载荷。

---

## 五、为什么会有这两种设计？（设计初衷）

这是 Python 在**通用动态语义**与**数值/二进制性能**之间的折中。

- **容器序列**：动态类型需要「一篮装万物」；若只有一种扁平数值块，无法自然混放不同类型与变长对象。
- **扁平序列**：弥补纯对象层在大规模**同构**数据上的密度与吞吐；代价是失去「随便塞对象」的自由。

设计哲学可记两句：`list`/`tuple` 偏 **Dynamic & Generic**；`array`/`bytes` 等偏 **Performance & Density**。

---

## 六、实战选型建议

| 场景 | 推荐类型 | 理由 |
| :--- | :--- | :--- |
| 混合类型、业务对象、嵌套结构 | **`list` / `tuple`** | 与动态模型最贴合 |
| 双端频繁增删、仍要异构元素 | **`collections.deque`** | API 与复杂度适合队列场景 |
| 大量同构数值、贴近二进制或 C | **`array.array`** | 紧凑缓冲 |
| 文本 | **`str`** | 专用字符序列 |
| 不可变字节流 | **`bytes`** | 扁平、可哈希（不可变） |
| 可变字节缓冲 | **`bytearray`** | 原地修改 |
| 科学计算矩阵/向量 | **`numpy.ndarray` 等** | 生态与向量化（第三方库） |

---

## 七、代码侧验证（粗略）

`sys.getsizeof` **不等于**进程总占用：`list` 的测量通常**不含**所有元素对象本身的大小。演示脚本只做**数量级感受**，见：

`part-1-data-structures/chapter-02/container_vs_flat_memory_demo.py`

```bash
python part-1-data-structures/chapter-02/container_vs_flat_memory_demo.py
```

---
## 八、延伸阅读

- 以 `a = 123` 串起来的对象模型总览（`PyLongObject`、对象头、序列对照）：`04-python-object-model-a-equals-123.md`
- 可变 / 不可变与 `collections.abc`、`PyFloatObject` 与交叉总表：`03-sequence-flat-container-mutable-immutable-abc.md`
- 可变/不可变与 hashable（dict key 规则、tuple 小坑）：`05-mutability-open-api-and-hash.md`
