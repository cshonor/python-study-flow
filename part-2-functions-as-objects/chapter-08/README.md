# 第 8 章「函数中的类型提示」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 8 章：**函数中的类型提示（Type Hints）**。

这一章要建立一个非常关键的正确认识：

- Python **仍是动态类型语言**；
- 类型提示 **不改变运行时行为**（解释器默认不强制校验类型）；
- 类型提示主要服务于 **人** 与 **工具**（IDE、静态检查器如 mypy/pyright）。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-type-hints-in-functions-overview.md` | 第 8 章开篇：PEP 484、渐进式类型、动态/静态的边界、Guido 的态度 |
| `type_hints_mypy_demo.py` | 配套：同一段代码“运行没问题，但 mypy 会报错”的对照证据 |
| `02-gradual-typing.md` | 8.2 渐进式类型：可选性、Any、运行时边界、落地原则与误区 |
| `gradual_typing_demo.py` | 配套：Any 逃生舱、逐步收紧边界、运行时 vs 静态检查的对照 |
| `03-gradual-typing-in-practice.md` | 8.3 渐进式类型实践：`show_count` 从无注解到 Optional/None 默认值 |
| `show_count_demo.py` | 配套：`show_count` 最终版 + 断言用例 |
| `04-types-defined-by-operations.md` | 8.4 类型由受支持的操作定义：鸭子类型 vs 名义类型、`double`/`Sequence` 与静态检查的错位 |
| `duck_nominal_typing_demo.py` | 配套：`Bird`/`Duck`/`quack`，无注解 vs 注解下 mypy 与运行时的对照 |
| `05-types-in-annotations.md` | 8.5 注解中可用的类型：`Any`/`object`、简单类型、`Optional`/`Union`、泛型容器、元组、`Mapping`/`Sequence`、语法演进 |
| `types_in_annotations_demo.py` | 配套：`parse_token`、`tokenize`、`NamedTuple`、`Mapping` 入参等可运行片段 |
| `06-types-in-annotations-advanced.md` | 8.5（续）进阶：类型别名、`Iterable`/`Sequence`、`TypeVar`（受限/有界）、`AnyStr`、`Protocol`、`Callable`、`NoReturn` |
| `types_advanced_demo.py` | 配套：`FromTo` 别名、`SupportsLessThan` + `top`、`apply_func`、`fatal_error` |

---

## 运行

在仓库根目录执行：

```bash
python part-2-functions-as-objects/chapter-08/type_hints_mypy_demo.py
python part-2-functions-as-objects/chapter-08/gradual_typing_demo.py
python part-2-functions-as-objects/chapter-08/show_count_demo.py
python part-2-functions-as-objects/chapter-08/duck_nominal_typing_demo.py
python part-2-functions-as-objects/chapter-08/types_in_annotations_demo.py
python part-2-functions-as-objects/chapter-08/types_advanced_demo.py
```

如果你装了 mypy，还可以做静态检查：

```bash
mypy part-2-functions-as-objects/chapter-08/type_hints_mypy_demo.py
mypy part-2-functions-as-objects/chapter-08/duck_nominal_typing_demo.py
mypy part-2-functions-as-objects/chapter-08/types_in_annotations_demo.py
mypy part-2-functions-as-objects/chapter-08/types_advanced_demo.py
```

