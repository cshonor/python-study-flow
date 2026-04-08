# 第 10 章「用一等函数实现设计模式」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 10 章：**用一等函数实现设计模式（Design Patterns with First-Class Functions）**。

这一章的核心态度来自一句话：

> **符合模式并不表示做得对。** —— Ralph Johnson

本章关注的不是“照着 GoF 的类图写代码”，而是理解模式要解决的问题，并用 Python 的语言特性把实现**大幅简化**——其中最关键的特性就是 **函数是一等对象**。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-design-patterns-with-first-class-functions-overview.md` | 第 10 章开篇导读：为什么动态语言会让许多模式“消失或简化”；策略/命令模式预告 |
| `02-strategy-pattern-class-vs-function.md` | 10.2 策略模式：类实现 vs 函数式重构；best_promo 的收集方式；装饰器自动注册 |
| `strategy_promotions_demo.py` | 配套：折扣策略（类式/函数式）、best_promo、装饰器自动注册策略 |
| `03-strategy-auto-registration-with-decorator.md` | 10.3 用装饰器自动注册策略：零维护 `best_promo`；可选的分组注册 |
| `strategy_auto_register_demo.py` | 配套：`@promotion` 自动登记；`best_promo` 无需维护列表；分组注册示例 |
| `04-command-pattern-functions-and-callables.md` | 10.4 命令模式：回调的面向对象替代品；用函数/可调用对象简化；宏命令与撤销思路 |
| `command_pattern_demo.py` | 配套：Menu invoker + Document receiver；MacroCommand；最小 undo 栈 |

---

## 运行

在仓库根目录执行：

```bash
python part-2-functions-as-objects/chapter-10/strategy_promotions_demo.py
python part-2-functions-as-objects/chapter-10/strategy_auto_register_demo.py
python part-2-functions-as-objects/chapter-10/command_pattern_demo.py
```

