# 第 7 章「函数是一等对象」— 本目录说明

本目录对应《流畅的 Python》（第二版）**第 7 章：函数是一等对象**。

本章回答的核心问题是：**在 Python 里，函数和普通数据一样，都是运行时存在的对象**——可以绑定到名字、放进容器、当作参数传入、当作返回值传出。这是高阶函数、闭包、装饰器等机制的公共地基。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-functions-as-first-class-objects-overview.md` | 7.x 开篇：什么是「一等对象」、为什么函数算一等、Guido 的表述、与后续小节的关系 |
| `02-examples-7-1-7-2-function-object-and-map.md` | 示例 7-1 / 7-2：`__doc__`/`type`、`fact=factorial`、`map`；常见函数属性；Callable 分类 |
| `03-higher-order-functions.md` | 7.3 高阶函数：`sorted(key=)`、`map`/`filter` 与推导式、`reduce` 与 `sum`、`all`/`any` |
| `first_class_functions_demo.py` | 配套：开篇四条件 + 书中 7-1/7-2 与属性演示 |
| `higher_order_functions_demo.py` | 配套：7.3 `sorted`/`map`/`filter`/`reduce`/`all`/`any` 可运行对照 |
| `04-lambda-expressions.md` | 7.4 `lambda`：语法限制、示例 7-7、反模式、与 `def` 对照、重构四步 |
| `lambda_expressions_demo.py` | 配套：7.4 `sorted`/`map`/`filter`、`__name__`、优先 `def` |
| `05-nine-kinds-of-callables.md` | 7.5 9 种可调用对象：`callable()`、内置/方法/类/实例、generator/coroutine/async generator |
| `callable_objects_demo.py` | 配套：7.5 列出 9 类 callable，并展示调用后返回的对象类型 |
| `06-user-defined-callable-types.md` | 7.6 用户定义可调用类型：实现 `__call__`，以 BingoCage 为例 |
| `user_defined_callable_demo.py` | 配套：7.6 BingoCage（`pick` / `__call__` / 抽空报错） |
| `07-advanced-argument-features.md` | 7.7 参数特性：`*args`/`**kwargs`、仅限关键字、`/` 仅限位置、`tag` 示例 |
| `tag_and_positional_only_demo.py` | 配套：7.7 `tag` 多种调用 + `/` 的 TypeError 证据 |
| `08-functional-tools-operator-and-functools.md` | 7.8 `operator` 与 `functools`：`mul/add/itemgetter/attrgetter/methodcaller`、`partial` 冻结参数 |
| `functional_tools_demo.py` | 配套：7.8 operator + partial 的可运行对照（含 partial 自省） |

---

## 运行

在仓库根目录执行：

```bash
python part-2-functions-as-objects/chapter-07/first_class_functions_demo.py
python part-2-functions-as-objects/chapter-07/higher_order_functions_demo.py
python part-2-functions-as-objects/chapter-07/lambda_expressions_demo.py
python part-2-functions-as-objects/chapter-07/callable_objects_demo.py
python part-2-functions-as-objects/chapter-07/user_defined_callable_demo.py
python part-2-functions-as-objects/chapter-07/tag_and_positional_only_demo.py
python part-2-functions-as-objects/chapter-07/functional_tools_demo.py
```
