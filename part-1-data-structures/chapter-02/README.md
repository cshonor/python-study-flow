# 第 2 章「丰富的序列」— 本目录说明

本目录对应《流畅的 Python》**第 2 章**：系统理解内置序列、推导式与生成器、元组与拆包、模式匹配、切片与序列运算等。

建议从这里开始读：[`01-第2章富序列与协议总览.md`](01-第2章富序列与协议总览.md)（先把“序列到底是什么、有哪些能力”讲清楚）。

---

## 文件一览（建议顺序）

| 顺序 | 文件 | 说明 |
|------|------|------|
| 01 | `01-第2章富序列与协议总览.md` | 序列的整体概念、为什么“协议”比“继承”更重要 |
| 02 | `02-容器序列与扁平序列.md` | 对象模型 → 容器/扁平 → 可变性 / hashable → `collections.abc` |
| 03 | `03-列表推导式与生成器表达式.md` | 列表推导式与生成器表达式 |
| 04 | `04-元组作记录与拆包.md` | 元组作记录 / 不可变列表、`*` 拆包、嵌套拆包 |
| 05 | `05-match-case序列模式匹配.md` | Python 3.10+ `match/case` 序列模式 |
| 06 | `06-切片与slice对象.md` | 切片、`slice` 对象、切片赋值 |
| 07 | `07-序列拼接重复与嵌套列表陷阱.md` | 序列 `+` / `*` 与嵌套列表陷阱 |
| 08 | `08-sort与sorted及key.md` | `list.sort()` 与 `sorted()`、`key`、稳定排序 |

上层索引另见：`../README.md` 中「`chapter-02/` 笔记与脚本」表。

---

## 笔记文件一览（`01`–`08` 连续编号）

| 文件 | 主题 |
|------|------|
| `01-第2章富序列与协议总览.md` | 开篇与路线 |
| `02-容器序列与扁平序列.md` | 合并版主文档（含对象头、ABC 等） |
| `03-列表推导式与生成器表达式.md` | listcomp / genexp |
| `04-元组作记录与拆包.md` | 元组与拆包 |
| `05-match-case序列模式匹配.md` | `match/case` |
| `06-切片与slice对象.md` | 切片 |
| `07-序列拼接重复与嵌套列表陷阱.md` | `+` / `*` 与浅拷贝陷阱 |
| `08-sort与sorted及key.md` | 原地 `sort` vs `sorted`、`key` 进阶 |

> 历史上曾用 `03`–`05` 文件名做「已并入 `02`」的跳转短页；若你本地仍有旧文件，以 `02` 为准即可。

---

## 配套脚本（在仓库根目录执行）

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

| 脚本 | 说明 |
|------|------|
| `02_container_vs_flat_memory_demo.py` | 与 `02`：`list` vs `array.array` 的 `getsizeof` 粗测 |
| `02_sequence_virtual_subclass_demo.py` | 与 `02`：`abc.Sequence.register` 与虚拟子类 |
| `03_listcomps_and_genexps_demo.py` | 与 `03` 配套 |
| `04_tuples_as_records_and_unpaking_demo.py` | 与 `04` 配套 |
| `05_pattern_matching_sequence_demo.py` | 与 `05` 配套（需 Python 3.10+） |
| `06_slicing_demo.py` | 与 `06` 配套 |
| `07_sequence_plus_mul_and_nested_list_trap_demo.py` | 与 `07` 配套 |
| `08_list_sort_vs_sorted_demo.py` | 与 `08` 配套 |

---

## 与第 1 章

自定义序列行为（如 `FrenchDeck`）见 `../chapter-01/`；本章聚焦**内置序列**的设计与日常用法。
