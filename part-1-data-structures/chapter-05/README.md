# 第 5 章「数据类构建器」— 本目录说明

本目录对应《流畅的 Python》（第二版）**第 5 章：数据类构建器**：从 `namedtuple`、`typing.NamedTuple` 演进到 `@dataclass`，以及它们和 `TypedDict` 的边界。

建议从这里开始跑 demo：`data_class_builders_demo.py`（一次性对比三种构建方式 + TypedDict）。

---

## 文件一览（当前）

| 文件 | 说明 |
|---|---|
| `01-data-class-builders-notes.md` | 第 5 章学习笔记（围绕“怎么选、差异在哪、坑在哪里”写） |
| `02-coordinate-overview-and-feature-matrix.md` | 5.2 入门：用 Coordinate 对比手写类与三种构建器 + 功能总表 |
| `03-typical-namedtuple.md` | 5.3 典型具名元组：namedtuple 的核心语法、API 与进阶技巧 |
| `04-typed-namedtuple.md` | 5.4 带类型的具名元组：`typing.NamedTuple` 深度解析 |
| `05-type-hints-primer.md` | 5.5 类型提示入门：注解的本质、运行时行为、三类类结构对比 |
| `06-dataclass-deep-dive.md` | 5.6 `@dataclass` 详解：参数、field、`__post_init__`、`ClassVar`、`InitVar`、实战建模 |
| `07-08-dataclass-code-smell-and-pattern-matching.md` | 5.7 & 5.8 数据类代码异味与模式匹配：设计原则 + `match/case` 类模式 |
| `data_class_builders_demo.py` | `namedtuple` / `typing.NamedTuple` / `@dataclass` / `TypedDict` 对比 demo |
| `coordinate_builders_demo.py` | Coordinate 专项：`_asdict/_replace` vs `asdict/replace`、类型注解与 make_dataclass |
| `namedtuple_typical_demo.py` | namedtuple 专项：`_fields/_make/_asdict/_replace`、defaults、动态注入、与 NamedTuple 对比 |
| `typed_namedtuple_demo.py` | `typing.NamedTuple` 专项：默认值、注解读取、不可变性、与 dataclass 对比 |
| `type_hints_primer_demo.py` | 5.5 配套：普通类/NamedTuple/dataclass 的注解与运行时行为对比 |
| `dataclass_deep_dive_demo.py` | 5.6 配套：`@dataclass` 全要点综合 demo（参数/field/post_init/ClassVar/InitVar/案例） |
| `dataclass_code_smell_and_match_demo.py` | 5.7/5.8 配套：代码异味提示 + `match/case`（关键字/位置/序列）对照 |

---

## 运行

在仓库根目录执行：

```bash
python part-1-data-structures/chapter-05/data_class_builders_demo.py
python part-1-data-structures/chapter-05/coordinate_builders_demo.py
python part-1-data-structures/chapter-05/namedtuple_typical_demo.py
python part-1-data-structures/chapter-05/typed_namedtuple_demo.py
python part-1-data-structures/chapter-05/type_hints_primer_demo.py
python part-1-data-structures/chapter-05/dataclass_deep_dive_demo.py
python part-1-data-structures/chapter-05/dataclass_code_smell_and_match_demo.py
```

