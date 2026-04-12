# 第 3 章「字典和集合」— 本目录说明

本目录对应《流畅的 Python》**第 3 章**：字典与集合、哈希表直觉、缺失键处理、`collections` 变体等。

建议从这里开始读：[`01-dicts-and-sets-chapter3-overview.md`](01-dicts-and-sets-chapter3-overview.md)（把 `dict/set` 这些核心概念先讲清楚）。

---

## 文件一览（建议顺序）

| 顺序 | 文件 | 说明 |
|------|------|------|
| 01 | `01-dicts-and-sets-chapter3-overview.md` | `dict`/`set` 为什么重要、hashable、常见行为与坑 |
| 1 | `02-dict-comprehension.md` | 3.2.1 字典推导式、与 `dict()` 对照、集合推导式 |
| 2 | `03-mapping-unpack-and-merge.md` | 3.2.2 `**` 拆包（PEP 448）、3.2.3 `|` / `|=`（PEP 584） |
| 3 | `04-csv-dictreader-pattern-matching.md` | `csv.DictReader` 行数据与映射模式 `match/case`（3.10+） |
| 4 | `05-mapping-abc-and-hashable.md` | §3.4 `Mapping`/`MutableMapping`；§3.4.1 可哈希；`**rest` 模式 |
| 5 | `06-dict-defaultdict-ordereddict-api.md` | §3.4.2 `dict` / `defaultdict` / `OrderedDict` API 对照 |
| 6 | `07-dict-mutable-values-indexing.md` | §3.4.3 可变值更新：词索引、`get`/`setdefault`/`defaultdict` |
| 7 | `08-defaultdict-and-missing.md` | §3.5 `defaultdict`、`__missing__` |
| 8 | `09-str-key-dict-and-dunder-missing.md` | §3.5.2 `StrKeyDict0`、`UserDict`、`__missing__` |
| 9 | `10-dict-variants-ordered-chain-counter.md` | §3.6 `OrderedDict`、`ChainMap`、`Counter` |
| 10 | `11-counter-shelve-and-userdict-subclassing.md` | §3.6 续：`Counter` 深化、`shelve`、`UserDict` |
| 11 | `12-dict-views.md` | §3.8 `keys`/`values`/`items` 字典视图 |
| 12 | `13-sets-and-frozenset.md` | §3.10–§3.11 `set`/`frozenset`、运算与实现直觉 |
| 13 | `14-dict-view-set-operations.md` | §3.12 `dict_keys`/`dict_items` 集合运算与 `frozenset` 对照 |

---

## 配套脚本（在仓库根目录执行）

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

| 脚本 | 说明 |
|------|------|
| `dict_and_set_quickstart_demo.py` | `get`/`setdefault`、`Counter` 词频、`set` 运算、`frozenset` 作键 |
| `dict_comprehension_demo.py` | 与 `02` 配套：区号示例、过滤、重复键、`set` 推导式、自测答案 |
| `dict_unpack_merge_demo.py` | 与 `03` 配套：PEP 448、`**` 合并、`|` / `|=`、`update`、`ChainMap` |
| `csv_dictreader_pattern_matching_demo.py` | 与 `04` 配套：`DictReader` + `match` / `if` 对照 |
| `mapping_abc_hashable_demo.py` | 与 `05` 配套：`**rest`、`isinstance`、`hash`、`frozen` dataclass |
| `mapping_types_three_way_demo.py` | 与 `06` 配套：三种映射差异、`fromkeys` 陷阱、`User` 可哈希 |
| `zen_word_index_demo.py` | 与 `07` 配套：《禅》节选词索引、默认实参求值、`defaultdict` 工厂 |
| `defaultdict_and_missing_demo.py` | 与 `08` 配套：§3.5、`get` 不插入、`__missing__` 子类 |
| `str_key_dict_demo.py` | 与 `09` 配套：`StrKeyDict0`、`StrKeyDict`（`get`/`in`） |
| `dict_variants_demo.py` | 与 `10` 配套：`OrderedDict`、`ChainMap`、`Counter` |
| `shelf_counter_userdict_demo.py` | 与 `11` 配套：`Counter` 运算、`shelve`、`UserDict` |
| `dict_views_demo.py` | 与 `12` 配套：§3.8 字典视图 |
| `set_theory_demo.py` | 与 `13` 配套：`set`/`frozenset`、运算 |
| `dict_view_setops_demo.py` | 与 `14` 配套：§3.12 视图集合运算 |

---

## 与第 2 章

序列、可哈希、`tuple` 作键等前置见 `../chapter-02/02-容器序列与扁平序列.md`。**序列模式** `match/case` 见 `../chapter-02/05-match-case序列模式匹配.md`。
