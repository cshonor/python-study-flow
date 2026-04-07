# 第 2 章「丰富的序列」— 本目录说明

本目录对应《流畅的 Python》**第 2 章**：系统理解内置序列、推导式与生成器、元组与拆包、模式匹配、切片与序列运算等。

**建议从这里开始读**：[`01-rich-sequences-chapter2-overview.md`](01-rich-sequences-chapter2-overview.md)（本章主题、书内骨架、学习优先级）。

---

## 学习路线（与 `01` 一致）

| 优先级 | 建议阅读 | 说明 |
|--------|----------|------|
| 0 | `01-rich-sequences-chapter2-overview.md` | 全章地图与优先级 |
| 1 | `02-container-vs-flat-sequences.md` | **合并主文档**：对象模型 → 容器/扁平 → 可变性 / hashable → ABC |
| 2 | `03-listcomps-and-genexps.md` | 列表推导式与生成器表达式 |
| 3 | `04-tuples-as-records-and-unpacking.md` | 元组作记录 / 不可变列表、`*` 拆包、嵌套拆包 |
| 4 | `05-structural-pattern-matching-sequence-patterns.md` | Python 3.10+ `match/case` 序列模式 |
| 5 | `06-slicing.md` | 切片、`slice` 对象、切片赋值 |
| 6 | `07-sequence-plus-mul-and-nested-list-trap.md` | 序列 `+` / `*` 与嵌套列表陷阱 |

上层索引另见：`../README.md` 中「`chapter-02/` 笔记与脚本」表。

---

## 笔记文件一览（`01`–`07` 连续编号）

| 文件 | 主题 |
|------|------|
| `01-rich-sequences-chapter2-overview.md` | 开篇与路线 |
| `02-container-vs-flat-sequences.md` | 合并版主文档（含对象头、ABC 等） |
| `03-listcomps-and-genexps.md` | listcomp / genexp |
| `04-tuples-as-records-and-unpacking.md` | 元组与拆包 |
| `05-structural-pattern-matching-sequence-patterns.md` | `match/case` |
| `06-slicing.md` | 切片 |
| `07-sequence-plus-mul-and-nested-list-trap.md` | `+` / `*` 与浅拷贝陷阱 |

> 历史上曾用 `03`–`05` 文件名做「已并入 `02`」的跳转短页；若你本地仍有旧文件，以 `02` 为准即可。

---

## 配套脚本（在仓库根目录执行）

```bash
python part-1-data-structures/chapter-02/container_vs_flat_memory_demo.py
python part-1-data-structures/chapter-02/sequence_virtual_subclass_demo.py
python part-1-data-structures/chapter-02/listcomps_and_genexps_demo.py
python part-1-data-structures/chapter-02/tuples_as_records_and_unpaking_demo.py
python part-1-data-structures/chapter-02/pattern_matching_sequence_demo.py
python part-1-data-structures/chapter-02/slicing_demo.py
python part-1-data-structures/chapter-02/sequence_plus_mul_and_nested_list_trap_demo.py
```

| 脚本 | 说明 |
|------|------|
| `container_vs_flat_memory_demo.py` | `list` vs `array.array` 的 `getsizeof` 粗测 |
| `sequence_virtual_subclass_demo.py` | `abc.Sequence.register` 与虚拟子类 |
| `listcomps_and_genexps_demo.py` | 与 `03` 配套 |
| `tuples_as_records_and_unpaking_demo.py` | 与 `04` 配套 |
| `pattern_matching_sequence_demo.py` | 与 `05` 配套（需 Python 3.10+） |
| `slicing_demo.py` | 与 `06` 配套 |
| `sequence_plus_mul_and_nested_list_trap_demo.py` | 与 `07` 配套 |

---

## 与第 1 章

自定义序列行为（如 `FrenchDeck`）见 `../chapter-01/`；本章聚焦**内置序列**的设计与日常用法。
