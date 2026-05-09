# 第 7 章「函数是一等对象」— 本目录说明

本目录对应《流畅的 Python》（第二版）**第 7 章：函数是一等对象**。

本章回答的核心问题是：**在 Python 里，函数和普通数据一样，都是运行时存在的对象**——可以绑定到名字、放进容器、当作参数传入、当作返回值传出。这是高阶函数、闭包、装饰器等机制的公共地基。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-第 7 章开篇：函数作为「一等对象」是什么意思.md` | 7.x 开篇：**§零 极简背诵**（四条件 + 口诀 + 误区：一等≠高阶）+ Guido 表述与后文衔接 |
| `02-示例 7-1 7-2：函数是对象、可赋值、可传给 map（高阶函数）.md` | 7-1/7-2：**§一** 出处 + 可运行代码 + 期望输出 + `function` vs `builtin_function_or_method`；`map`、属性表、Callable |
| `03-7.3 高阶函数（Higher-Order Function）.md` | 7.3 高阶函数：`sorted(key=)`、`map`/`filter` 与推导式、`reduce` 与 `sum`、`all`/`any` |
| `01_first_class_functions_demo.py` | 配套：开篇四条件 + 书中 7-1/7-2 与属性演示 |
| `03_higher_order_functions_demo.py` | 配套：7.3 `sorted`/`map`/`filter`/`reduce`/`all`/`any` 可运行对照 |
| `04-7.4 匿名函数：lambda 表达式.md` | 7.4 `lambda`：语法限制、示例 7-7、反模式、与 `def` 对照、重构四步 |
| `04_lambda_expressions_demo.py` | 配套：7.4 `sorted`/`map`/`filter`、`__name__`、优先 `def` |
| `05-7.5 Python 的 9 种可调用对象（Callable）：谁能用 ()，以及怎么安全判断.md` | 7.5 9 种可调用对象：`callable()`、内置/方法/类/实例、generator/coroutine/async generator |
| `05_callable_objects_demo.py` | 配套：7.5 列出 9 类 callable，并展示调用后返回的对象类型 |
| `06-7.6 用户定义的可调用类型：实现 __call__ 让“实例像函数一样工作”.md` | 7.6 用户定义可调用类型：实现 `__call__`，以 BingoCage 为例 |
| `06_user_defined_callable_demo.py` | 配套：7.6 BingoCage（`pick` / `__call__` / 抽空报错） |
| `07-7.7 从位置参数到仅限关键字参数： args、 kwargs、 与.md` | 7.7 参数特性：`*args`/`**kwargs`、仅限关键字、`/` 仅限位置、`tag` 示例 |
| `07_tag_and_positional_only_demo.py` | 配套：7.7 `tag` 多种调用 + `/` 的 TypeError 证据 |
| `08-7.8 支持函数式编程的包：operator 与 functools.partial.md` | 7.8 `operator` 与 `functools`：`mul/add/itemgetter/attrgetter/methodcaller`、`partial` 冻结参数 |
| `08_functional_tools_demo.py` | 配套：7.8 operator + partial 的可运行对照（含 partial 自省） |

---

## 运行

在仓库根目录执行：

```bash
python part-2-functions-as-objects/chapter-07/01_first_class_functions_demo.py
python part-2-functions-as-objects/chapter-07/03_higher_order_functions_demo.py
python part-2-functions-as-objects/chapter-07/04_lambda_expressions_demo.py
python part-2-functions-as-objects/chapter-07/05_callable_objects_demo.py
python part-2-functions-as-objects/chapter-07/06_user_defined_callable_demo.py
python part-2-functions-as-objects/chapter-07/07_tag_and_positional_only_demo.py
python part-2-functions-as-objects/chapter-07/08_functional_tools_demo.py
```
