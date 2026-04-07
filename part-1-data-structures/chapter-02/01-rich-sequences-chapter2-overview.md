# 第 2 章「丰富的序列」开篇：先建立一套能“推导出来”的序列直觉

学序列（`list` / `tuple` / `str` / `bytes` …）最容易走偏：把它学成“背 API”。  
更省力、也更接近《流畅的 Python》的方式是：先把序列放进同一个框架里理解——**可变性**、**存储方式**、**常见操作的语义**。有了这套直觉，你遇到新容器时也更容易“猜对它会怎么表现”。

---

## 一、先把“序列”当成一种协议（而不是某几个类型的集合）

很多初学者说“序列就是 list/tuple/str”。这没错，但更关键的一步是理解：

- **序列是一组行为（协议）**：只要一个对象支持 `__len__` 和 `__getitem__`（至少能用整数下标访问），它就能参与很多“像序列一样”的操作：`len(x)`、`x[i]`、切片、迭代、成员测试等。
- **内置序列只是最常见的实现**：`list`、`tuple`、`str`、`bytes`、`bytearray`、`array.array`、`collections.deque` ……它们解决的是不同问题：可变性、内存占用、速度、语义清晰度。

为什么先讲“协议”很重要？

- 因为工程里更常做的是**选容器**：这组数据该用什么存，才能更清晰/更省内存/更快。
- 而“选容器”靠背 API 很难，靠**分类直觉**更稳。

---

## 二、两套分类抓住了 80% 的差异

### 2.1 按可变性：能不能在“同一个对象身份”上改内容？

| 类别 | 代表 | 直觉 |
| :--- | :--- | :--- |
| **可变序列** | `list`、`bytearray`、`array.array`、`collections.deque` | 可以原地修改（增删/改元素） |
| **不可变序列** | `tuple`、`str`、`bytes` | 不能原地修改；“改动”意味着创建新对象 |

这里最常见的坑是对 `tuple` 的误解：

- `tuple` 的“不变”指的是**槽位绑定不变**，不是“深度不可变”。  
  如果 `tuple` 里装了 `list`，你仍然能修改那个 `list`。

### 2.2 按存储：容器序列 vs 扁平序列（本章最值钱的直觉）

| 类别 | 代表 | 底层直觉 | 工程含义 |
| :--- | :--- | :--- | :--- |
| **容器序列** | `list`、`tuple`、`deque` | 载荷是**对象引用槽位**（你可以粗略把它想成“指针列表”） | 能装任意对象（异构/可嵌套）；但每个元素都是“一个对象” |
| **扁平序列** | `str`、`bytes`、`bytearray`、`array.array` | 载荷是**同构原始数据的连续内存** | 更紧凑、更省内存；元素类型受限（字节/字符语义/类型码） |

把这张表理解透，你就更容易明白：

- 为什么装很多数值时，`array('d')` 往往比 `list[float]` 更省内存。
- 为什么 `bytes`/`bytearray` 适合 I/O 边界（它们本质是字节缓冲），而 `str` 适合“人类文本”。

下一篇 `02-container-vs-flat-sequences.md` 会把这个分类和 CPython 对象模型串起来，让你知道“省内存到底省在哪”。

---

## 三、本章会反复用到的 3 个能力点（它们决定你写出来的代码像不像 Python）

### 3.1 推导式与生成器表达式：本质是“要不要一次性把结果放进内存”

- **列表推导式（listcomp）**：一次性构造 `list`，直观、常用，但会把结果全部放进内存。
- **生成器表达式（genexp）**：惰性产出元素，常被 `sum/any/all/max/min/tuple` 等“消费端”边取边用。

你要形成的判断是：

- 结果要反复遍历/索引吗？如果是，通常需要 `list`。
- 结果只会被消费一次、且可能很大吗？如果是，优先 genexp。

### 3.2 元组：既是“不可变列表”，更常是“轻量记录（record）”

- **不可变列表视角**：位置有意义，例如 `(x, y)`。
- **记录视角**：字段组合有意义，例如一行 CSV 可以用 `(city, country, population)` 表达。

后面你会发现：拆包（unpacking）、排序 `key=`、模式匹配都在用“把元组当记录”的思想。

### 3.3 切片与排序：序列 API 的核心手感

- **切片**：理解左闭右开、步长、负索引、切片赋值。
- **排序**：理解 `sorted(...)` 返回新列表；`list.sort()` 原地排序且返回 `None`；`key=` 的含义是“先映射，再比较”。

---

## 四、建议边读边跑的示例（都在仓库里）

在仓库根目录执行：

```bash
python part-1-data-structures/chapter-02/container_vs_flat_memory_demo.py
python part-1-data-structures/chapter-02/listcomps_and_genexps_demo.py
python part-1-data-structures/chapter-02/tuples_as_records_and_unpaking_demo.py
python part-1-data-structures/chapter-02/slicing_demo.py
python part-1-data-structures/chapter-02/list_sort_vs_sorted_demo.py
```

---

## 五、小练习（写完再对照对应 demo）

1. **选型题**：你有 10 万个 `float`，只读、要节省内存，选 `list` 还是 `array('d')`？用“容器序列 vs 扁平序列”的语言解释原因。  
2. **推导式题**：把 `['  A', 'b ', '', ' C  ']` 清洗为 `['a', 'b', 'c']`（去空、`strip`、`lower`）。写 listcomp 和 genexp 两种版本。  
3. **切片题**：给定 `s = 'abcdef'`，写出：取偶数位字符、倒序、每隔 2 个取 1 个的切片表达式。  

