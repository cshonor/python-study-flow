# Part 1：Python 数据结构与特殊方法

本部分对应《流畅的 Python》**数据模型与基础容器**相关章节，聚焦：内置序列/映射、**特殊方法（魔术方法）**，以及用 **组合** 让自定义类表现得像序列。

---

## 目录说明

| 目录 | 对应（本书章节编号按你本地划分） | 说明 |
|------|----------------------------------|------|
| `chapter-01/` | 第 1–6 章范围的学习材料 | 当前主要笔记与示例脚本均在此 |
| `chapter-02/` | 第 2 章「丰富的序列」等 | 开篇、容器/扁平、`PyObject*`、ABC、对象模型、可变/不可变协议：`01`…`08` |
| `chapter-03/` | 第 3 章「字典和集合」 | `01`–`06`（含三种映射 API）；见该目录 `README` |
| `chapter-04/` … `chapter-06/` | 预留 | 可按章填充 |

每章目录内约定：**两位编号**的 `NN-主题.md` 为笔记，同名主题的 `*_demo.py` 为可运行示例（见下）。

---

## 核心知识点

- **Python 数据模型**：对象、类型与协议；特殊方法由解释器**隐式**调用（优先写 `len(x)`，而非 `x.__len__()`）。
- **常用特殊方法**（示例）：
  - `__repr__` / `__str__`：字符串表示
  - `__len__`、`__getitem__`、`__setitem__`：`len`、`[]` 取值、赋值（如支持 `random.shuffle` 写回）
  - `__contains__`：`in` 运算符（可实现 set / bisect 等优化）
- **内置数据结构**：`list`、`tuple`、`namedtuple`、`dict`、`set` / `frozenset` 等；`array.array` 与 `namedtuple` 的字段名列表**不是同一概念**。
- **组合模式**：用 `self._cards` 等内部容器 + 委托 `__len__` / `__getitem__` / `__setitem__`，得到 **Pythonic** 序列行为。
- **排序与工具**：`sorted(..., key=自定义函数)`；`random.choice` / `shuffle` 与序列协议的关系。
- **容器抽象**：`collections.abc`（`Sized` / `Iterable` / `Container` / `Sequence` 等）用于理解协议与类型注解；**鸭子类型**与 **`isinstance` + `register()`** 可并存。

更系统的特殊方法对照与分类见：`chapter-01/11-special-methods-implicit-invocation.md`。  
容器 ABC 与 `FrenchDeck` 的对照见：`chapter-01/12-collections-abc-container-api.md`。

---

## `chapter-01/` 笔记与脚本（当前进度）

笔记（按编号顺序，主题简述）：

| 编号 | 文件（前缀） | 主题简述 |
|------|----------------|----------|
| 01 | `01-python-list-tuple-array` | list / tuple / array / namedtuple 对比 |
| 02–04 | `02`…`04` | 基础语法、魔法方法与类属性/推导式等 |
| 05 | `05-python-namedtuple-usage-guide` | `namedtuple` 参数、`rename`、与 `array` 区别 |
| 06 | `06-class-vs-namedtuple-attributes` | 普通类与 namedtuple 的属性与可读性 |
| 07 | `07-pythonic-french-deck-namedtuple-and-class` | `Card` + `FrenchDeck` 协作 |
| 08 | `08-random-choice-and-special-methods` | `random.choice` 与 `__len__` / `__getitem__` |
| 09 | `09-dunder-getitem-and-contains` | `__getitem__`、`__contains__` 与 set / bisect 优化 |
| 10 | `10-french-deck-composition-setitem-shuffle` | 组合、`__setitem__`、`shuffle`、`spades_high` |
| 11 | `11-special-methods-implicit-invocation` | 隐式调用原则 + 对照表 + 三类归纳 |
| 12 | `12-collections-abc-container-api` | `collections.abc`、Collection / Sequence / Mapping / Set、鸭子类型 |

可运行脚本（均在 `chapter-01/`）：

| 脚本 | 说明 |
|------|------|
| `french_deck_demo.py` | 基础 `FrenchDeck` + `Card` |
| `french_deck_shuffle_demo.py` | `__setitem__`、`shuffle`、`spades_high`、权重打印 |
| `namedtuple_usage_demo.py` | 与 `05` 笔记配套 |
| `random_choice_special_methods_demo.py` | 与 `08` 笔记配套 |
| `getitem_contains_demo.py` | 与 `09` 笔记配套 |
| `collections_abc_minimal_demo.py` | 与 `12` 笔记配套（`isinstance` + `Sequence.register`） |

在仓库根目录执行示例：

```bash
python part-1-data-structures/chapter-01/french_deck_shuffle_demo.py
```

---

## `chapter-02/` 笔记与脚本

本章目录内另有 **`chapter-02/README.md`**：以 `01-rich-sequences-chapter2-overview.md` 为入口的学习路线、全部笔记与脚本一览。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-rich-sequences-chapter2-overview.md` | 第 2 章路线、**Fluent Python 本章骨架**（§二）、学习优先级 |
| 02 | `02-container-vs-flat-sequences.md` | **合并版主文档**：对象头→容器/扁平→可变性/hashable→ABC |
| 03 | `03-listcomps-and-genexps.md` | 列表推导式 vs 生成器表达式：模板、可读性准则、面试题 |
| 04 | `04-tuples-as-records-and-unpacking.md` | 元组的双重角色：结构化记录与拆包（含选型与避坑） |
| 05 | `05-structural-pattern-matching-sequence-patterns.md` | Python 3.10+ `match/case`：序列模式匹配、守卫与 `*rest` |
| 06 | `06-slicing.md` | 切片：左闭右开、步距、`slice` 对象、切片赋值与 `...` |
| 07 | `07-sequence-plus-mul-and-nested-list-trap.md` | `+`/`*` 运算与嵌套列表陷阱（浅拷贝引用共享） |
| 08 | `08-list-sort-vs-sorted.md` | `list.sort()` 与 `sorted()`、`key`、稳定排序 |

| 脚本 | 说明 |
|------|------|
| `container_vs_flat_memory_demo.py` | `list` 与 `array.array` 的 `sys.getsizeof` 粗略对比（含注释与局限） |
| `sequence_virtual_subclass_demo.py` | `abc.Sequence.register` 与 `isinstance`（虚拟子类） |
| `listcomps_and_genexps_demo.py` | 列表推导式 / genexp / map+filter / 作用域 / `:=` 演示 |
| `tuples_as_records_and_unpaking_demo.py` | 元组作为记录、`*` 拆包、嵌套拆包、hashable 判断 |
| `pattern_matching_sequence_demo.py` | Python 3.10+ `match/case`：序列模式、guard、`*rest` 顺序坑 |
| `slicing_demo.py` | 切片：步距/反转、命名 `slice`、切片赋值与 `Ellipsis` |
| `sequence_plus_mul_and_nested_list_trap_demo.py` | 序列 `+`/`*` 与 `[[]]*n` 引用共享陷阱 |
| `list_sort_vs_sorted_demo.py` | `list.sort` / `sorted` / `key` / `itemgetter` / 稳定排序 |

```bash
python part-1-data-structures/chapter-02/container_vs_flat_memory_demo.py
python part-1-data-structures/chapter-02/sequence_virtual_subclass_demo.py
python part-1-data-structures/chapter-02/listcomps_and_genexps_demo.py
python part-1-data-structures/chapter-02/tuples_as_records_and_unpaking_demo.py
python part-1-data-structures/chapter-02/pattern_matching_sequence_demo.py
python part-1-data-structures/chapter-02/slicing_demo.py
python part-1-data-structures/chapter-02/sequence_plus_mul_and_nested_list_trap_demo.py
python part-1-data-structures/chapter-02/list_sort_vs_sorted_demo.py
```

---

## `chapter-03/` 笔记与脚本

本章目录内另有 **`chapter-03/README.md`**：以 `01-dicts-and-sets-chapter3-overview.md` 为入口。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-dicts-and-sets-chapter3-overview.md` | 第 3 章开篇：dict/set 定位、知识地图、哈希与可哈希、**面试速记** |
| 02 | `02-dict-comprehension.md` | 3.2.1 字典推导式、集合推导式、避坑 |
| 03 | `03-mapping-unpack-and-merge.md` | 3.2.2 `**`（PEP 448）、3.2.3 `|` / `|=`（PEP 584） |
| 04 | `04-csv-dictreader-pattern-matching.md` | `csv.DictReader` 与映射模式 `match/case` |
| 05 | `05-mapping-abc-and-hashable.md` | `Mapping`/`MutableMapping`、可哈希、`**rest` 映射模式 |
| 06 | `06-dict-defaultdict-ordereddict-api.md` | §3.4.2 `dict` / `defaultdict` / `OrderedDict` 方法对照 |

| 脚本 | 说明 |
|------|------|
| `dict_and_set_quickstart_demo.py` | `get`/`setdefault`、`Counter`、集合运算、`frozenset` 作键 |
| `dict_comprehension_demo.py` | 区号示例、`sorted`+`if`、重复键、自测题答案 |
| `dict_unpack_merge_demo.py` | `**` 调用/字面量、`{**d1, **d2}`、`|` / `|=`、`ChainMap` |
| `csv_dictreader_pattern_matching_demo.py` | `DictReader` + `match` / `if`（3.10+） |
| `mapping_abc_hashable_demo.py` | `**rest`、`isinstance(Mapping)`、`hash`、`frozen` dataclass |
| `mapping_types_three_way_demo.py` | 三种映射、`fromkeys` 陷阱、`OrderedDict.move_to_end` |

```bash
python part-1-data-structures/chapter-03/dict_and_set_quickstart_demo.py
python part-1-data-structures/chapter-03/dict_comprehension_demo.py
python part-1-data-structures/chapter-03/dict_unpack_merge_demo.py
python part-1-data-structures/chapter-03/csv_dictreader_pattern_matching_demo.py
python part-1-data-structures/chapter-03/mapping_abc_hashable_demo.py
python part-1-data-structures/chapter-03/mapping_types_three_way_demo.py
```

---

## 学习目标

能熟练使用内置数据结构，并能为自定义类型实现合适的特殊方法，使对象在 **`len` / `[]` / `for` / `in` / 排序 / 洗牌** 等场景下行为清晰、符合 Python 习惯。
