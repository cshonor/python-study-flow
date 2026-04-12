# Part 1：Python 数据结构与特殊方法

本部分对应《流畅的 Python》**数据模型与基础容器**相关章节，聚焦：内置序列/映射、**特殊方法（魔术方法）**，以及用 **组合** 让自定义类表现得像序列。

---

## 目录说明

| 目录 | 对应（本书章节编号按你本地划分） | 说明 |
|------|----------------------------------|------|
| `chapter-01/` | 第 1–6 章范围的学习材料 | 当前主要笔记与示例脚本均在此 |
| `chapter-02/` | 第 2 章「丰富的序列」等 | 开篇、容器/扁平、`PyObject*`、ABC、对象模型、可变/不可变协议：`01`…`08` |
| `chapter-03/` | 第 3 章「字典和集合」 | `01`–`14`（含 §3.6 / §3.8 / §3.10–§3.12）；见该目录 `README` |
| `chapter-04/` | 第 4 章「Unicode 文本与字节序列」 | `01` 开篇；见该目录 `README` |
| `chapter-05/` | 第 5 章「数据类构建器」 | `01`–`07` 笔记；`namedtuple` / `typing.NamedTuple` / `@dataclass` / `TypedDict` + 配套 demo |
| `chapter-06/` | 第 6 章「对象引用、可变性和垃圾回收」 | `01`–`07` 笔记；变量/对象/引用、浅深拷贝、参数传递、GC、弱引用 |

第 7 章「函数是一等对象」等材料在 **`part-2-functions-as-objects/`**（本书 Part 2 对应目录），见该 Part 内 `README` 与 `chapter-07/`。

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

更系统的特殊方法对照与分类见：`chapter-01/11-特殊方法隐式调用与对照表.md`。  
容器 ABC 与 `FrenchDeck` 的对照见：`chapter-01/12-collections-abc容器API.md`。

---

## `chapter-01/` 笔记与脚本（当前进度）

笔记（按编号顺序，主题简述）：

| 编号 | 文件（前缀） | 主题简述 |
|------|----------------|----------|
| 01 | `01-python-list-tuple-array` | list / tuple / array / namedtuple 对比 |
| 02–04 | `02`…`04` | 基础语法、魔法方法与类属性/推导式等 |
| 05 | `05-namedtuple用法指南与rename参数` | `namedtuple` 参数、`rename`、与 `array` 区别 |
| 06 | `06-普通类与namedtuple属性及可读性` | 普通类与 namedtuple 的属性与可读性 |
| 07 | `07-Pythonic法式扑克牌namedtuple与类` | `Card` + `FrenchDeck` 协作 |
| 08 | `08-random-choice与特殊方法lengetitem` | `random.choice` 与 `__len__` / `__getitem__` |
| 09 | `09-getitem与contains及成员检测优化` | `__getitem__`、`__contains__` 与 set / bisect 优化 |
| 10 | `10-法式扑克牌组合setitem与洗牌` | 组合、`__setitem__`、`shuffle`、`spades_high` |
| 11 | `11-特殊方法隐式调用与对照表` | 隐式调用原则 + 对照表 + 三类归纳 |
| 12 | `12-collections-abc容器API` | `collections.abc`、Collection / Sequence / Mapping / Set、鸭子类型 |

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

本章目录内另有 **`chapter-02/README.md`**：以 `01-第2章富序列与协议总览.md` 为入口的笔记与脚本一览。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第2章富序列与协议总览.md` | 第 2 章开篇：序列能力、协议视角、常见坑与练习 |
| 02 | `02-容器序列与扁平序列.md` | **合并版主文档**：对象头→容器/扁平→可变性/hashable→ABC |
| 03 | `03-列表推导式与生成器表达式.md` | 列表推导式 vs 生成器表达式：模板、可读性与坑 |
| 04 | `04-元组作记录与拆包.md` | 元组的双重角色：结构化记录与拆包（含选型与避坑） |
| 05 | `05-match-case序列模式匹配.md` | Python 3.10+ `match/case`：序列模式匹配、守卫与 `*rest` |
| 06 | `06-切片与slice对象.md` | 切片：左闭右开、步距、`slice` 对象、切片赋值与 `...` |
| 07 | `07-序列拼接重复与嵌套列表陷阱.md` | `+`/`*` 运算与嵌套列表陷阱（浅拷贝引用共享） |
| 08 | `08-sort与sorted及key.md` | `list.sort()` 与 `sorted()`、`key`、稳定排序 |

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

本章目录内另有 **`chapter-03/README.md`**：以 `01-第3章字典与集合总览.md` 为入口。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第3章字典与集合总览.md` | 第 3 章开篇：dict/set、hashable、常见行为与坑 |
| 02 | `02-字典推导式与集合推导式.md` | 3.2.1 字典推导式、集合推导式、避坑 |
| 03 | `03-映射拆包与字典合并.md` | 3.2.2 `**`（PEP 448）、3.2.3 `|` / `|=`（PEP 584） |
| 04 | `04-csv-DictReader与match-case.md` | `csv.DictReader` 与映射模式 `match/case` |
| 05 | `05-Mapping抽象与可哈希.md` | `Mapping`/`MutableMapping`、可哈希、`**rest` 映射模式 |
| 06 | `06-dict-defaultdict与OrderedDict对照.md` | §3.4.2 `dict` / `defaultdict` / `OrderedDict` 方法对照 |
| 07 | `07-可变值与词索引.md` | §3.4.3 可变值与词索引：`get`/`setdefault`/`defaultdict` |
| 08 | `08-defaultdict与missing.md` | §3.5 `defaultdict`、`__missing__` |
| 09 | `09-字符串键字典与missing.md` | §3.5.2 `StrKeyDict0`、`UserDict`、`__missing__` |
| 10 | `10-OrderedDict-ChainMap-Counter.md` | §3.6 `OrderedDict`、`ChainMap`、`Counter` |
| 11 | `11-Counter与shelve及UserDict子类化.md` | §3.6 续：`Counter`、`shelve`、`UserDict` |
| 12 | `12-字典视图.md` | §3.8 `keys`/`values`/`items` 视图 |
| 13 | `13-集合与frozenset.md` | §3.10–§3.11 `set` / `frozenset` |
| 14 | `14-字典视图集合运算.md` | §3.12 字典视图与 `frozenset` 对照 |

| 脚本 | 说明 |
|------|------|
| `dict_and_set_quickstart_demo.py` | `get`/`setdefault`、`Counter`、集合运算、`frozenset` 作键 |
| `dict_comprehension_demo.py` | 区号示例、`sorted`+`if`、重复键、自测题答案 |
| `dict_unpack_merge_demo.py` | `**` 调用/字面量、`{**d1, **d2}`、`|` / `|=`、`ChainMap` |
| `csv_dictreader_pattern_matching_demo.py` | `DictReader` + `match` / `if`（3.10+） |
| `mapping_abc_hashable_demo.py` | `**rest`、`isinstance(Mapping)`、`hash`、`frozen` dataclass |
| `mapping_types_three_way_demo.py` | 三种映射、`fromkeys` 陷阱、`OrderedDict.move_to_end` |
| `zen_word_index_demo.py` | §3.4.3 词索引、默认实参求值、`defaultdict` 工厂 |
| `defaultdict_and_missing_demo.py` | §3.5、`get` 不插入、嵌套、`__missing__` |
| `str_key_dict_demo.py` | `StrKeyDict0`、`StrKeyDict`（`get`/`in` 与 `d[k]` 一致） |
| `dict_variants_demo.py` | §3.6 三种映射变体 |
| `shelf_counter_userdict_demo.py` | §3.6 续：`Counter` / `shelve` / `UserDict` |
| `dict_views_demo.py` | §3.8 字典视图 |
| `set_theory_demo.py` | §3.10–§3.11 集合 |
| `dict_view_setops_demo.py` | §3.12 视图集合运算 |

```bash
python part-1-data-structures/chapter-03/dict_and_set_quickstart_demo.py
python part-1-data-structures/chapter-03/dict_comprehension_demo.py
python part-1-data-structures/chapter-03/dict_unpack_merge_demo.py
python part-1-data-structures/chapter-03/csv_dictreader_pattern_matching_demo.py
python part-1-data-structures/chapter-03/mapping_abc_hashable_demo.py
python part-1-data-structures/chapter-03/mapping_types_three_way_demo.py
python part-1-data-structures/chapter-03/zen_word_index_demo.py
python part-1-data-structures/chapter-03/defaultdict_and_missing_demo.py
python part-1-data-structures/chapter-03/str_key_dict_demo.py
python part-1-data-structures/chapter-03/dict_variants_demo.py
python part-1-data-structures/chapter-03/shelf_counter_userdict_demo.py
python part-1-data-structures/chapter-03/dict_views_demo.py
python part-1-data-structures/chapter-03/set_theory_demo.py
python part-1-data-structures/chapter-03/dict_view_setops_demo.py
```

---

## `chapter-04/` 笔记与脚本

本章目录内另有 **`chapter-04/README.md`**：以 `01-第4章Unicode文本与字节总览.md` 为入口。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第4章Unicode文本与字节总览.md` | 第 4 章开篇：`str`/`bytes`、Unicode、编解码边界 |
| 02 | `02-码点编码与编解码错误.md` | 字符/码点/编码/字节，编解码异常与 `errors=` |
| 03 | `03-IO编码排查清单.md` | I/O 编码排查清单：文件/子进程/控制台 |
| 04 | `04-bytes与bytearray.md` | `bytes`/`bytearray`：索引切片、可变性、`fromhex` |
| 05 | `05-常见编码与codecs.md` | 常见编码与 codec、多编码 bytes 对照 |
| 06 | `06-编解码问题排查与修复.md` | 三类异常、BOM、检测与修复模板 |
| 07 | `07-Unicode规范化.md` | NFC/NFD/NFKC、casefold、比较工具函数 |
| 08 | `08-Unicode文本排序.md` | 码点序、locale、UCA（pyuca） |
| 09 | `09-Unicode数据库与unicodedata.md` | `unicodedata`、数值语义 |
| 10 | `10-双模式API-str与bytes.md` | `re` / `os` 等 str 与 bytes 双模式 |

| 脚本 | 说明 |
|------|------|
| `unicode_bytes_quickstart_demo.py` | 与 `01` 配套：`encode`/`decode`、`errors=` |
| `codepoints_encoding_demo.py` | 与 `02` 配套：码点、UTF-8 字节与解码差异、`errors=` |
| `io_encoding_troubleshoot_demo.py` | 与 `03` 配套：I/O 编码排查 demo |
| `bytes_bytearray_demo.py` | 与 `04` 配套 |
| `codecs_encodings_table_demo.py` | 与 `05` 配套 |
| `encoding_decoding_fixes_demo.py` | 与 `06` 配套 |
| `unicode_normalization_demo.py` | 与 `07` 配套 |
| `unicode_sorting_demo.py` | 与 `08` 配套 |
| `unicode_numeric_demo.py` / `unicode_char_finder.py` | 与 `09` 配套 |
| `dual_mode_api_demo.py` | 与 `10` 配套 |

```bash
python part-1-data-structures/chapter-04/unicode_bytes_quickstart_demo.py
python part-1-data-structures/chapter-04/codepoints_encoding_demo.py
python part-1-data-structures/chapter-04/io_encoding_troubleshoot_demo.py
python part-1-data-structures/chapter-04/bytes_bytearray_demo.py
python part-1-data-structures/chapter-04/codecs_encodings_table_demo.py
python part-1-data-structures/chapter-04/encoding_decoding_fixes_demo.py
python part-1-data-structures/chapter-04/unicode_normalization_demo.py
python part-1-data-structures/chapter-04/unicode_sorting_demo.py
python part-1-data-structures/chapter-04/unicode_numeric_demo.py
python part-1-data-structures/chapter-04/unicode_char_finder.py CAT EYES --limit 20
python part-1-data-structures/chapter-04/dual_mode_api_demo.py
```

---

## `chapter-05/` 笔记与脚本

本章目录内另有 **`chapter-05/README.md`**：以 `01-第5章数据类构建器笔记.md` 为主线。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第5章数据类构建器笔记.md` | 数据类构建器：选型、差异与常见坑 |
| 02 | `02-Coordinate与三种构建器功能矩阵.md` | Coordinate 与手写类 / `namedtuple` / `NamedTuple` / `@dataclass` 对照 |
| 03 | `03-典型具名元组namedtuple.md` | `collections.namedtuple` 用法与 API |
| 04 | `04-typing-NamedTuple详解.md` | `typing.NamedTuple` 与类型注解 |
| 05 | `05-类型提示入门.md` | 类型提示基础与运行时行为 |
| 06 | `06-dataclass详解.md` | `@dataclass` 参数、`field`、`__post_init__` 等 |
| 07 | `07-08-数据类异味与match-case.md` | 数据类反模式与 `match/case` 类模式 |

```bash
python part-1-data-structures/chapter-05/data_class_builders_demo.py
python part-1-data-structures/chapter-05/coordinate_builders_demo.py
python part-1-data-structures/chapter-05/namedtuple_typical_demo.py
python part-1-data-structures/chapter-05/typed_namedtuple_demo.py
python part-1-data-structures/chapter-05/type_hints_primer_demo.py
python part-1-data-structures/chapter-05/dataclass_deep_dive_demo.py
python part-1-data-structures/chapter-05/dataclass_code_smell_and_match_demo.py
```

---

## `chapter-06/` 笔记与脚本

本章目录内另有 **`chapter-06/README.md`**：以 `01-第6章对象引用可变性与GC总览.md` 为入口。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第6章对象引用可变性与GC总览.md` | 变量/对象/引用、可变性、拷贝、GC 总览 |
| 02 | `02-变量不是盒子.md` | 变量是标签、赋值与别名 |
| 03 | `03-同一性相等与别名.md` | `is`/`==`、别名与元组相对不可变 |
| 04 | `04-浅拷贝为默认.md` | 浅拷贝、`copy`/`deepcopy` |
| 05 | `05-共享传参与可变默认参数.md` | 共享传参、可变默认参数 |
| 06 | `06-del与垃圾回收.md` | `del`、引用计数、循环 GC、弱引用 |
| 07 | `07-不可变类型技巧.md` | 驻留、`intern`、`is` 边界 |

```bash
python part-1-data-structures/chapter-06/object_refs_mutability_gc_demo.py
```

---

## 备注

本部分的所有笔记都以“能看懂、能跑起来、能避坑”为目标：每篇尽量把概念、直觉、常见错误、可运行示例放在一起，方便边读边验证。
