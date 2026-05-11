# 第 9 章「装饰器和闭包」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 9 章：**装饰器和闭包（Decorators and Closures）**。

这一章的主线，是把三个概念连起来：

- Python 的**作用域规则（LEGB）**决定了名字如何解析；
- **闭包（closure）**让函数“带着环境一起走”，从而能保存状态；
- **装饰器（decorator）**利用“函数是一等对象 + 闭包”，在不改动被装饰函数源码的前提下增强行为。

**整章总览（10 步递进、最小可复制例、易错点、与 `01`～`10` 映射）**：[00 第 9 章学习路线与总览](<00-流畅的Python第9章装饰器与闭包学习路线与总览.md>)。

---

## 核心概念（开篇就要抓住的点）

### 什么是装饰器？
装饰器是 Python 里用来**增强函数行为**的语法糖：在**不修改原函数代码**的前提下，为函数“叠加”额外能力（日志、性能统计、缓存、权限校验等）。

一个直观例子：给一个计算函数加上缓存，让重复输入直接复用结果，而不是每次都重新计算。

### 为什么装饰器离不开闭包？
装饰器的本质是**高阶函数**。它之所以能“记住并修改外部变量”，关键就在于**闭包**：

- 闭包像一个“小盒子”，能记住它创建时的环境变量（自由变量）；
- 即使离开创建环境，仍能访问这些变量，从而让函数“带状态地运行”；
- 当你需要在闭包里**修改**某个非局部变量时，`nonlocal` 就派上用场（否则会因为赋值语句把名字判定为局部变量而出错/失效）。

---

## 这一章怎么学（按顺序走最稳）

| 阶段 | 核心内容 | 你需要搞懂的问题 |
|---|---|---|
| 基础篇 | 变量作用域规则（LEGB） | Python 如何判断一个变量是局部的、非局部的还是全局的？ |
| 核心篇 | 闭包与 `nonlocal` | 闭包是怎么工作的？`nonlocal` 解决了什么问题？ |
| 入门篇 | 简单的装饰器 | 如何实现一个基础的“注册式”装饰器？ |
| 进阶篇 | 标准库装饰器 | 如何使用 `@lru_cache`（缓存）、`@singledispatch`（多态分发）？ |
| 高级篇 | 参数化装饰器 | 如何给装饰器本身传递参数？ |

如果你刚开始学第 9 章，建议按这个顺序推进：

1. 先搞懂 Python 的变量作用域规则（LEGB）
2. 再理解闭包的概念，并用 `nonlocal` 解决变量修改问题
3. 然后从最简单的无参装饰器开始写起
4. 最后再挑战参数化装饰器

---

## 为什么这一章很重要？
这是 Python 从“脚本级入门”到“工程级开发”的关键分水岭：

- **写框架/库必备**：几乎所有 Python Web 框架（如 Flask、FastAPI）和工具库都大量使用装饰器。
- **写出优雅的代码**：用装饰器处理横切关注点（日志、权限校验等），让业务逻辑更清晰。
- **性能优化利器**：`@lru_cache` 这类装饰器，能直接缓解重复计算带来的性能瓶颈。

---

## 小提醒
装饰器有个非常容易忽略的点：**装饰发生在导入时**（函数定义被执行时就会完成装饰）。理解这一点，后面读“注册式装饰器”、调试“为什么一导入就有副作用”会轻松很多。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `00-流畅的Python第9章装饰器与闭包学习路线与总览.md` | **总览**：递进骨架、首刷/二刷顺序、`01`～`10` 对照表、极简可运行片段、量化清单 |
| `01-9.1 开篇路线：为什么装饰器离不开闭包（以及这章怎么学）.md` | 开篇路线：LEGB、闭包与 `nonlocal`、装饰器为何重要、以及“装饰发生在导入时” |
| `02-9.2 装饰器基础知识：@ 到底做了什么（以及它什么时候执行）.md` | 装饰器基础：`@` 的等价形式、函数替换、装饰发生在导入时（最小例子） |
| `03-9.3 注册式装饰器：为什么 import 一下就“执行了代码”.md` | 注册式装饰器：`registry` 收集函数引用，脚本运行 vs import 的执行时机对照 |
| `03_registration.py` | 配套：`@register` + 全局 `registry`，展示导入时执行装饰过程 |
| `04-9.4 注册装饰器（实战）：装饰器与被装饰对象不在同一模块时怎么组织.md` | 9.4 注册装饰器实战：包装式 vs 注册式、跨模块组织、工程注意点 |
| `05-9.5 变量作用域：为什么“函数里一赋值就变局部”（用 dis 看证据）.md` | 9.5 作用域陷阱：赋值导致局部、`global` 修复、`dis` 看 `LOAD_GLOBAL`/`LOAD_FAST` |
| `05_scope_dis_demo.py` | 配套：复现 `UnboundLocalError`，并反汇编对比关键字节码指令 |
| `05_scope_closure_nonlocal_demo.py` | 配套：LEGB、自由变量、闭包、`nonlocal` 对比（ASCII 输出，适配 Windows 控制台） |
| `02_decorator_and_cache_demo.py` | 配套：最小装饰器 + `functools.wraps`；`lru_cache` 演示缓存减少重复计算 |
| `06-9.6 闭包（Closure）深度理解：累计平均值、自由变量与 cell.md` | 9.6 闭包深度理解：累计平均值，`co_freevars`/`__closure__`/cell，`nonlocal` 坑与修复 |
| `06_averager_closure_demo.py` | 配套：类实现 vs 闭包实现；打印 `co_freevars` 与 `cell_contents`；演示 `nonlocal` |
| `07-9.7 nonlocal 与名字解析：闭包里为什么 += 会炸（以及完整查找规则）.md` | 9.7 `nonlocal` 与名字解析：`+=` 为何触发局部判定；`global` vs `nonlocal`；查找规则 |
| `07_nonlocal_name_resolution_demo.py` | 配套：复现/修复 `averager`；`global` 示例；带状态装饰器（调用次数统计） |
| `08-9.8 计时装饰器（clock）：从最小可用到“可用于生产”的三个修复.md` | 9.8 计时装饰器：基础版缺陷与三项修复（`**kwargs`、`wraps`、完整参数打印） |
| `08_clock_decorator_demo.py` | 配套：`clock0` vs `clock`；`snooze`/递归 `factorial`；验证 `__name__` 与 kwargs 支持 |
| `09-9.9 functools 标准库装饰器：缓存（cache lru_cache）与单分派（singledispatch）.md` | 9.9 标准库装饰器：`cache`/`lru_cache`、叠放顺序、`singledispatch` 要点 |
| `09_functools_decorators_demo.py` | 配套：Fibonacci（plain vs cache vs lru）；`singledispatch` 的 `htmlize` 示例 |
| `10-9.10 参数化装饰器与类式装饰器：让装饰器“可配置”.md` | 9.10 参数化装饰器与类式装饰器：工厂函数三层结构、class `__call__` 方案 |
| `10_parameterized_decorators_demo.py` | 配套：参数化注册装饰器、带 `fmt` 的 clock、类式 clock（含 `wraps`） |

---

## 运行

在仓库根目录执行：

```bash
python part-2-functions-as-objects/chapter-09/03_registration.py
python part-2-functions-as-objects/chapter-09/02_decorators_basics_demo.py
python part-2-functions-as-objects/chapter-09/05_scope_dis_demo.py
python part-2-functions-as-objects/chapter-09/05_scope_closure_nonlocal_demo.py
python part-2-functions-as-objects/chapter-09/02_decorator_and_cache_demo.py
python part-2-functions-as-objects/chapter-09/06_averager_closure_demo.py
python part-2-functions-as-objects/chapter-09/07_nonlocal_name_resolution_demo.py
python part-2-functions-as-objects/chapter-09/08_clock_decorator_demo.py
python part-2-functions-as-objects/chapter-09/09_functools_decorators_demo.py
python part-2-functions-as-objects/chapter-09/10_parameterized_decorators_demo.py
```
