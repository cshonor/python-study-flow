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
| `01-第 8 章开篇：函数中的类型提示（Type Hints）到底是什么.md` | 第 8 章开篇：PEP 484、渐进式类型、动态/静态的边界、Guido 的态度 |
| `01_type_hints_mypy_demo.py` | 配套：同一段代码“运行没问题，但 mypy 会报错”的对照证据 |
| `02-8.2 渐进式类型系统（Gradual Typing）：Python 类型提示的设计哲学与落地方式.md` | 8.2 渐进式类型：可选性、Any、运行时边界、落地原则与误区 |
| `02_gradual_typing_demo.py` | 配套：Any 逃生舱、逐步收紧边界、运行时 vs 静态检查的对照 |
| `03-8.3 渐进式类型实践：从 0 注解到可检查的函数签名（show_count 实战）.md` | 8.3 渐进式类型实践：`show_count` 从无注解到 Optional/None 默认值 |
| `03_show_count_demo.py` | 配套：`show_count` 最终版 + 断言用例 |
| `04-8.4 类型由受支持的操作定义：鸭子类型 vs 名义类型（静态检查在看什么）.md` | 8.4：文首**大白话速通**（鸭子/名义/`Protocol`）+ `double`/`Sequence` 错位；`04_duck_nominal_typing_demo.py` 含 **`Goose`/`Quackable`** |
| `04_duck_nominal_typing_demo.py` | 配套：`Bird`/`Duck`/`quack`，无注解 vs 注解下 mypy 与运行时的对照 |
| `05-8.5 注解中可用的类型：从 Any 到泛型容器与抽象基类.md` | 8.5 注解中可用的类型：`Any`/`object`、简单类型、`Optional`/`Union`、泛型容器、元组、`Mapping`/`Sequence`、语法演进 |
| `05_types_in_annotations_demo.py` | 配套：`parse_token`、`tokenize`、`NamedTuple`、`Mapping` 入参等可运行片段 |
| `06-8.5（续）类型提示进阶：别名、TypeVar、Protocol、Callable、NoReturn.md` | 8.5（续）进阶：类型别名、`Iterable`/`Sequence`、`TypeVar`（受限/有界）、`AnyStr`、`Protocol`、`Callable`、`NoReturn` |
| `06_types_advanced_demo.py` | 配套：`FromTo` 别名、`SupportsLessThan` + `top`、`apply_func`、`fatal_error` |
| `07-8.6 仅限位置参数与变长参数的类型注解 · 8.7 类型系统的局限性.md` | 8.6 仅限位置参数与 `*`/`**` 注解；8.7 类型系统局限性（误报/漏报）与测试 |
| `07_tag_type_hints_demo.py` | 配套：`tag(name, /, *content, class_=..., **attrs)` 最小可运行示例 |

---

## 运行

在仓库根目录执行：

```bash
python part-2-functions-as-objects/chapter-08/01_type_hints_mypy_demo.py
python part-2-functions-as-objects/chapter-08/02_gradual_typing_demo.py
python part-2-functions-as-objects/chapter-08/03_show_count_demo.py
python part-2-functions-as-objects/chapter-08/04_duck_nominal_typing_demo.py
python part-2-functions-as-objects/chapter-08/05_types_in_annotations_demo.py
python part-2-functions-as-objects/chapter-08/06_types_advanced_demo.py
python part-2-functions-as-objects/chapter-08/07_tag_type_hints_demo.py
```

如果你装了 mypy，还可以做静态检查：

```bash
mypy part-2-functions-as-objects/chapter-08/01_type_hints_mypy_demo.py
mypy part-2-functions-as-objects/chapter-08/04_duck_nominal_typing_demo.py
mypy part-2-functions-as-objects/chapter-08/05_types_in_annotations_demo.py
mypy part-2-functions-as-objects/chapter-08/06_types_advanced_demo.py
mypy part-2-functions-as-objects/chapter-08/07_tag_type_hints_demo.py
```

