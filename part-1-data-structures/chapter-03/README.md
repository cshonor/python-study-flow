# 第 3 章「字典和集合」— 本目录说明

本目录对应《流畅的 Python》**第 3 章**：字典与集合、哈希表直觉、缺失键处理、`collections` 变体等。

**建议从这里开始读**：[`01-dicts-and-sets-chapter3-overview.md`](01-dicts-and-sets-chapter3-overview.md)（本章主题、知识地图、**面试速记**）。

---

## 学习路线与文件一览

| 优先级 | 文件 | 说明 |
|--------|------|------|
| 0 | `01-dicts-and-sets-chapter3-overview.md` | 开篇、框架、概念准备、面试速记 |
| 1 | `02-dict-comprehension.md` | 3.2.1 字典推导式、与 `dict()` 对照、集合推导式 |
| 2 | `03-mapping-unpack-and-merge.md` | 3.2.2 `**` 拆包（PEP 448）、3.2.3 `|` / `|=`（PEP 584） |
| 3 | `04-csv-dictreader-pattern-matching.md` | `csv.DictReader` 行数据与映射模式 `match/case`（3.10+） |
| 4 | `05-mapping-abc-and-hashable.md` | §3.4 `Mapping`/`MutableMapping`；§3.4.1 可哈希；`**rest` 模式 |
| 5 | `06-dict-defaultdict-ordereddict-api.md` | §3.4.2 `dict` / `defaultdict` / `OrderedDict` API 对照 |

---

## 配套脚本（在仓库根目录执行）

```bash
python part-1-data-structures/chapter-03/dict_and_set_quickstart_demo.py
python part-1-data-structures/chapter-03/dict_comprehension_demo.py
python part-1-data-structures/chapter-03/dict_unpack_merge_demo.py
python part-1-data-structures/chapter-03/csv_dictreader_pattern_matching_demo.py
python part-1-data-structures/chapter-03/mapping_abc_hashable_demo.py
python part-1-data-structures/chapter-03/mapping_types_three_way_demo.py
```

| 脚本 | 说明 |
|------|------|
| `dict_and_set_quickstart_demo.py` | `get`/`setdefault`、`Counter` 词频、`set` 运算、`frozenset` 作键 |
| `dict_comprehension_demo.py` | 与 `02` 配套：区号示例、过滤、重复键、`set` 推导式、自测答案 |
| `dict_unpack_merge_demo.py` | 与 `03` 配套：PEP 448、`**` 合并、`|` / `|=`、`update`、`ChainMap` |
| `csv_dictreader_pattern_matching_demo.py` | 与 `04` 配套：`DictReader` + `match` / `if` 对照 |
| `mapping_abc_hashable_demo.py` | 与 `05` 配套：`**rest`、`isinstance`、`hash`、`frozen` dataclass |
| `mapping_types_three_way_demo.py` | 与 `06` 配套：三种映射差异、`fromkeys` 陷阱、`User` 可哈希 |

---

## 与第 2 章

序列、可哈希、`tuple` 作键等前置见 `../chapter-02/02-container-vs-flat-sequences.md`。**序列模式** `match/case` 见 `../chapter-02/05-structural-pattern-matching-sequence-patterns.md`。
