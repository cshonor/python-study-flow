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
| `chapter-05/` | 第 5 章「数据类构建器」 | `01`–`07` 笔记；演示脚本为 `01_`…`07_*.py` 与篇号对齐 |
| `chapter-06/` | 第 6 章「对象引用、可变性和垃圾回收」 | `01`–`07` 笔记 + 同编号 `NN_*.py`（`01` 为导航）；引用、拷贝、传参、GC |

第 7 章「函数是一等对象」等材料在 **`part-2-functions-as-objects/`**（本书 Part 2 对应目录）；**Part 2 总览（两条主梁 + 7–10 章一条线）**见 `part-2-functions-as-objects/00-Part2-第7-10章-两条主梁与章序.md`，其余见该 Part 内 `README` 与各章 `chapter-0x/README.md`。

每章目录内约定：**两位编号**的 `NN-主题.md` 为笔记；**`NN_` 前缀**的 `NN_描述_demo.py` 为与篇号对齐的可运行示例（`chapter-01` 仅部分篇目有脚本；`chapter-02` 的 `02` 篇对应两个 `02_*.py`；`chapter-04` 的 `09` 篇对应 `09_unicode_numeric_demo.py` 与 `09_unicode_char_finder.py`）。

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
| `05_namedtuple_usage_demo.py` | 与 `05` 笔记配套 |
| `07_french_deck_demo.py` | 与 `07` 配套：基础 `FrenchDeck` + `Card` |
| `08_random_choice_special_methods_demo.py` | 与 `08` 配套：`random.choice` 与特殊方法 |
| `09_getitem_contains_demo.py` | 与 `09` 配套：`__getitem__` / `__contains__` |
| `10_french_deck_shuffle_demo.py` | 与 `10` 配套：`__setitem__`、`shuffle`、`spades_high` |
| `12_collections_abc_minimal_demo.py` | 与 `12` 配套：`collections.abc` / `isinstance` |

在仓库根目录执行示例：

```bash
python part-1-data-structures/chapter-01/05_namedtuple_usage_demo.py
python part-1-data-structures/chapter-01/07_french_deck_demo.py
python part-1-data-structures/chapter-01/08_random_choice_special_methods_demo.py
python part-1-data-structures/chapter-01/09_getitem_contains_demo.py
python part-1-data-structures/chapter-01/10_french_deck_shuffle_demo.py
python part-1-data-structures/chapter-01/12_collections_abc_minimal_demo.py
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
| `02_container_vs_flat_memory_demo.py` | 与 `02`：`list` / `array.array` 的 `getsizeof` 粗测 |
| `02_sequence_virtual_subclass_demo.py` | 与 `02`：`abc.Sequence.register` 虚拟子类 |
| `03_listcomps_and_genexps_demo.py` | 与 `03`：列表推导式 / genexp / `:=` 等 |
| `04_tuples_as_records_and_unpaking_demo.py` | 与 `04`：元组记录与拆包 |
| `05_pattern_matching_sequence_demo.py` | 与 `05`：`match/case`（需 3.10+） |
| `06_slicing_demo.py` | 与 `06`：切片与 `slice` |
| `07_sequence_plus_mul_and_nested_list_trap_demo.py` | 与 `07`：`+`/`*` 与嵌套列表陷阱 |
| `08_list_sort_vs_sorted_demo.py` | 与 `08`：`sort` / `sorted` / `key` |

```bash
python part-1-data-structures/chapter-02/02_container_vs_flat_memory_demo.py
python part-1-data-structures/chapter-02/02_sequence_virtual_subclass_demo.py
python part-1-data-structures/chapter-02/03_listcomps_and_genexps_demo.py
python part-1-data-structures/chapter-02/04_tuples_as_records_and_unpaking_demo.py
python part-1-data-structures/chapter-02/05_pattern_matching_sequence_demo.py
python part-1-data-structures/chapter-02/06_slicing_demo.py
python part-1-data-structures/chapter-02/07_sequence_plus_mul_and_nested_list_trap_demo.py
python part-1-data-structures/chapter-02/08_list_sort_vs_sorted_demo.py
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
| `01_dict_and_set_quickstart_demo.py` | 与 `01`：`get`/`setdefault`、`Counter`、集合运算 |
| `02_dict_comprehension_demo.py` | 与 `02`：字典/集合推导式 |
| `03_dict_unpack_merge_demo.py` | 与 `03`：`**`、`|=`、`ChainMap` |
| `04_csv_dictreader_pattern_matching_demo.py` | 与 `04`：`DictReader` + `match`（3.10+） |
| `05_mapping_abc_hashable_demo.py` | 与 `05`：`Mapping`、可哈希 |
| `06_mapping_types_three_way_demo.py` | 与 `06`：`dict` / `defaultdict` / `OrderedDict` |
| `07_zen_word_index_demo.py` | 与 `07`：词索引与 `defaultdict` |
| `08_defaultdict_and_missing_demo.py` | 与 `08`：`defaultdict`、`__missing__` |
| `09_str_key_dict_demo.py` | 与 `09`：字符串键与 `UserDict` |
| `10_dict_variants_demo.py` | 与 `10`：`OrderedDict` / `ChainMap` / `Counter` |
| `11_shelf_counter_userdict_demo.py` | 与 `11`：`shelve`、`UserDict` |
| `12_dict_views_demo.py` | 与 `12`：字典视图 |
| `13_set_theory_demo.py` | 与 `13`：`set` / `frozenset` |
| `14_dict_view_setops_demo.py` | 与 `14`：视图集合运算 |

```bash
python part-1-data-structures/chapter-03/01_dict_and_set_quickstart_demo.py
python part-1-data-structures/chapter-03/02_dict_comprehension_demo.py
python part-1-data-structures/chapter-03/03_dict_unpack_merge_demo.py
python part-1-data-structures/chapter-03/04_csv_dictreader_pattern_matching_demo.py
python part-1-data-structures/chapter-03/05_mapping_abc_hashable_demo.py
python part-1-data-structures/chapter-03/06_mapping_types_three_way_demo.py
python part-1-data-structures/chapter-03/07_zen_word_index_demo.py
python part-1-data-structures/chapter-03/08_defaultdict_and_missing_demo.py
python part-1-data-structures/chapter-03/09_str_key_dict_demo.py
python part-1-data-structures/chapter-03/10_dict_variants_demo.py
python part-1-data-structures/chapter-03/11_shelf_counter_userdict_demo.py
python part-1-data-structures/chapter-03/12_dict_views_demo.py
python part-1-data-structures/chapter-03/13_set_theory_demo.py
python part-1-data-structures/chapter-03/14_dict_view_setops_demo.py
```

---

## `chapter-04/` 笔记与脚本

本章目录内另有 **`chapter-04/README.md`**：以 `01-第4章Unicode文本与字节总览.md` 为入口。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第4章Unicode文本与字节总览.md` | 第 4 章开篇：`str`/`bytes`、ASCII·Unicode·UTF-8 分层、编解码边界 |
| 02 | `02-码点编码与编解码错误.md` | 字符/码点/编码/字节，编解码异常、`errors=`、`fromhex`/`hex` |
| 03 | `03-IO编码排查清单.md` | I/O 编码排查清单：文件/子进程/控制台 |
| 04 | `04-bytes与bytearray.md` | `bytes`/`bytearray`：索引切片、可变性、`fromhex` |
| 05 | `05-常见编码与codecs.md` | 常见编码与 codec、多编码 bytes 对照 |
| 06 | `06-编解码问题排查与修复.md` | 三类异常、BOM、检测与修复模板 |
| 07 | `07-Unicode规范化.md` | 新手 §零 速记、NFC/NFD/NFKC、casefold、比较工具函数 |
| 08 | `08-Unicode文本排序.md` | 新手 §零、码点序、locale、UCA（pyuca） |
| 09 | `09-Unicode数据库与unicodedata.md` | 新手 §零、`unicodedata`、`name`、`digit`/`numeric` |
| 10 | `10-双模式API-str与bytes.md` | **新手清爽版**：`re` / `os` 等 str 与 bytes 双模式 |

| 脚本 | 说明 |
|------|------|
| `01_unicode_bytes_quickstart_demo.py` | 与 `01`：`encode`/`decode`、`errors=` |
| `02_codepoints_encoding_demo.py` | 与 `02`：码点、UTF-8、`errors=` |
| `03_io_encoding_troubleshoot_demo.py` | 与 `03`：I/O 编码排查 |
| `04_bytes_bytearray_demo.py` | 与 `04`：`bytes`/`bytearray` |
| `05_codecs_encodings_table_demo.py` | 与 `05`：编码与 codecs |
| `06_encoding_decoding_fixes_demo.py` | 与 `06`：编解码修复 |
| `07_unicode_normalization_demo.py` | 与 `07`：规范化 |
| `08_unicode_sorting_demo.py` | 与 `08`：排序 |
| `09_unicode_numeric_demo.py` / `09_unicode_char_finder.py` | 与 `09`：`unicodedata` / 按名查字符 |
| `10_dual_mode_api_demo.py` | 与 `10`：str/bytes 双模式 API |

```bash
python part-1-data-structures/chapter-04/01_unicode_bytes_quickstart_demo.py
python part-1-data-structures/chapter-04/02_codepoints_encoding_demo.py
python part-1-data-structures/chapter-04/03_io_encoding_troubleshoot_demo.py
python part-1-data-structures/chapter-04/04_bytes_bytearray_demo.py
python part-1-data-structures/chapter-04/05_codecs_encodings_table_demo.py
python part-1-data-structures/chapter-04/06_encoding_decoding_fixes_demo.py
python part-1-data-structures/chapter-04/07_unicode_normalization_demo.py
python part-1-data-structures/chapter-04/08_unicode_sorting_demo.py
python part-1-data-structures/chapter-04/09_unicode_numeric_demo.py
python part-1-data-structures/chapter-04/09_unicode_char_finder.py CAT EYES --limit 20
python part-1-data-structures/chapter-04/10_dual_mode_api_demo.py
```

---

## `chapter-05/` 笔记与脚本

本章目录内另有 **`chapter-05/README.md`**：以 `01-第5章数据类构建器笔记.md` 为主线。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第5章数据类构建器笔记.md` | **超清爽新手笔记**：选型、`namedtuple`/`NamedTuple`/`dataclass`/`TypedDict` |
| 02 | `02-Coordinate与三种构建器功能矩阵.md` | Coordinate 与手写类 / `namedtuple` / `NamedTuple` / `@dataclass` 对照 |
| 03 | `03-典型具名元组namedtuple.md` | `namedtuple`：§〇 一段跑通 + API/示例（对齐 `03_namedtuple_typical_demo.py`） |
| 04 | `04-typing-NamedTuple详解.md` | `typing.NamedTuple` 与类型注解 |
| 05 | `05-类型提示入门.md` | 类型提示基础与运行时行为 |
| 06 | `06-dataclass详解.md` | `@dataclass`：**§零 参数背诵版**；`field`、`__post_init__` 等 |
| 07 | `07-08-数据类异味与match-case.md` | 数据类反模式与 `match/case` 类模式 |

```bash
python part-1-data-structures/chapter-05/01_data_class_builders_demo.py
python part-1-data-structures/chapter-05/02_coordinate_builders_demo.py
python part-1-data-structures/chapter-05/03_namedtuple_typical_demo.py
python part-1-data-structures/chapter-05/04_typed_namedtuple_demo.py
python part-1-data-structures/chapter-05/05_type_hints_primer_demo.py
python part-1-data-structures/chapter-05/06_dataclass_deep_dive_demo.py
python part-1-data-structures/chapter-05/07_dataclass_code_smell_and_match_demo.py
```

---

## `chapter-06/` 笔记与脚本

本章目录内另有 **`chapter-06/README.md`**：以 `01-第6章对象引用可变性与GC总览.md` 为入口。

| 编号 | 文件 | 主题简述 |
|------|------|----------|
| 01 | `01-第6章对象引用可变性与GC总览.md` | 变量/对象/引用、可变性、拷贝、GC 总览 |
| 02 | `02-变量不是盒子.md` | 变量是标签、赋值与别名 |
| 03 | `03-同一性相等与别名.md` | `is`/`==`、别名与元组相对不可变 |
| 04 | `04-浅拷贝为默认.md` | 文首**大白话速通** + 浅拷贝速查 + 赋值/浅/深对比、`copy`/`deepcopy` |
| 05 | `05-共享传参与可变默认参数.md` | **§零** call by sharing 背诵 + 可变默认参数；与 `04` 浅拷贝对照 |
| 06 | `06-del与垃圾回收.md` | `del`、引用计数、循环 GC、弱引用 |
| 07 | `07-不可变类型技巧.md` | 驻留、`intern`、`is` 边界 |

脚本与笔记编号一致：`01_object_refs_gc_overview_demo.py`（导航）、`02_variable_not_a_box_demo.py` … `07_immutable_type_tricks_demo.py`（详见 `chapter-06/README.md`）。

```bash
python part-1-data-structures/chapter-06/01_object_refs_gc_overview_demo.py
python part-1-data-structures/chapter-06/02_variable_not_a_box_demo.py
python part-1-data-structures/chapter-06/03_identity_equality_aliasing_demo.py
python part-1-data-structures/chapter-06/04_shallow_copy_and_deepcopy_demo.py
python part-1-data-structures/chapter-06/05_call_by_sharing_mutable_defaults_demo.py
python part-1-data-structures/chapter-06/06_del_and_garbage_collection_demo.py
python part-1-data-structures/chapter-06/07_immutable_type_tricks_demo.py
```

---

## 备注

本部分的所有笔记都以“能看懂、能跑起来、能避坑”为目标：每篇尽量把概念、直觉、常见错误、可运行示例放在一起，方便边读边验证。
