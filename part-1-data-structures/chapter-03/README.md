# 第 3 章「字典和集合」— 本目录说明

本目录对应《流畅的 Python》**第 3 章**：字典与集合、哈希表直觉、缺失键处理、`collections` 变体等。

建议从这里开始读：[`01-第3章字典与集合总览.md`](01-第3章字典与集合总览.md)（把 `dict/set` 这些核心概念先讲清楚）。

---

## 文件一览（建议顺序）

| 顺序 | 文件 | 说明 |
|------|------|------|
| 01 | `01-第3章字典与集合总览.md` | `dict`/`set` 为什么重要、hashable、常见行为与坑 |
| 02 | `02-字典推导式与集合推导式.md` | 3.2.1 字典推导式、与 `dict()` 对照、集合推导式 |
| 03 | `03-映射拆包与字典合并.md` | 3.2.2 `**` 拆包（PEP 448）、3.2.3 `|` / `|=`（PEP 584） |
| 04 | `04-csv-DictReader与match-case.md` | `csv.DictReader` 行数据与映射模式 `match/case`（3.10+） |
| 05 | `05-Mapping抽象与可哈希.md` | §3.4 `Mapping`/`MutableMapping`；§3.4.1 可哈希；`**rest` 模式 |
| 06 | `06-dict-defaultdict与OrderedDict对照.md` | §3.4.2 `dict` / `defaultdict` / `OrderedDict` API 对照 |
| 07 | `07-可变值与词索引.md` | §3.4.3 可变值更新：词索引、`get`/`setdefault`/`defaultdict` |
| 08 | `08-defaultdict与missing.md` | §3.5 `defaultdict`、`__missing__` |
| 09 | `09-字符串键字典与missing.md` | §3.5.2 `StrKeyDict0`、`UserDict`、`__missing__` |
| 10 | `10-OrderedDict-ChainMap-Counter.md` | §3.6 `OrderedDict`、`ChainMap`、`Counter` |
| 11 | `11-Counter与shelve及UserDict子类化.md` | §3.6 续：`Counter` 深化、`shelve`、`UserDict` |
| 12 | `12-字典视图.md` | §3.8 `keys`/`values`/`items` 字典视图 |
| 13 | `13-集合与frozenset.md` | §3.10–§3.11 `set`/`frozenset`、运算与实现直觉 |
| 14 | `14-字典视图集合运算.md` | §3.12 `dict_keys`/`dict_items` 集合运算与 `frozenset` 对照 |

---

## 配套脚本（在仓库根目录执行）

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

| 脚本 | 说明 |
|------|------|
| `01_dict_and_set_quickstart_demo.py` | `get`/`setdefault`、`Counter` 词频、`set` 运算、`frozenset` 作键 |
| `02_dict_comprehension_demo.py` | 与 `02` 配套：区号示例、过滤、重复键、`set` 推导式、自测答案 |
| `03_dict_unpack_merge_demo.py` | 与 `03` 配套：PEP 448、`**` 合并、`|` / `|=`、`update`、`ChainMap` |
| `04_csv_dictreader_pattern_matching_demo.py` | 与 `04` 配套：`DictReader` + `match` / `if` 对照 |
| `05_mapping_abc_hashable_demo.py` | 与 `05` 配套：`**rest`、`isinstance`、`hash`、`frozen` dataclass |
| `06_mapping_types_three_way_demo.py` | 与 `06` 配套：三种映射差异、`fromkeys` 陷阱、`User` 可哈希 |
| `07_zen_word_index_demo.py` | 与 `07` 配套：《禅》节选词索引、默认实参求值、`defaultdict` 工厂 |
| `08_defaultdict_and_missing_demo.py` | 与 `08` 配套：§3.5、`get` 不插入、`__missing__` 子类 |
| `09_str_key_dict_demo.py` | 与 `09` 配套：`StrKeyDict0`、`StrKeyDict`（`get`/`in`） |
| `10_dict_variants_demo.py` | 与 `10` 配套：`OrderedDict`、`ChainMap`、`Counter` |
| `11_shelf_counter_userdict_demo.py` | 与 `11` 配套：`Counter` 运算、`shelve`、`UserDict` |
| `12_dict_views_demo.py` | 与 `12` 配套：§3.8 字典视图 |
| `13_set_theory_demo.py` | 与 `13` 配套：`set`/`frozenset`、运算 |
| `14_dict_view_setops_demo.py` | 与 `14` 配套：§3.12 视图集合运算 |

---

## 与第 2 章

序列、可哈希、`tuple` 作键等前置见 `../chapter-02/02-容器序列与扁平序列.md`。**序列模式** `match/case` 见 `../chapter-02/05-match-case序列模式匹配.md`。
