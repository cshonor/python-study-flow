# `lis.py`：用 `match/case` 写一个 Scheme 子集解释器（18.3）

## 本节看什么

- **目标**：读懂 Norvig 的 `lis.py`（一个 Scheme 子集解释器），并看清 Python 3.10+ 的 `match/case` 如何把解释器的“语法分派”写得又短又清楚。
- **收获**：把“词法分析 → 语法分析(AST) → 求值(evaluate) → 环境(Environment) → REPL”这条链路串起来。

---

## Scheme：统一的 S 表达式

- **没有“语句/表达式”之分**：一切都是表达式，求值有结果（或 `None`）。
- **前置表示法**：`(+ x 13)` 代替 `x + 13`。
- **数据即代码**：`(quote (...))` 把代码当数据传递（不求值）。

术语对照：

- **Atom（原子）**：数值或 `Symbol`（标识符）
- **Expression（表达式）**：Atom 或嵌套列表（AST）

---

## 三块核心：类型、解析、环境

### 类型（最小 AST）

- `Symbol = str`
- `Atom = int | float | Symbol`
- `Expression = Atom | list[Expression]`

### 解析器：源码 → AST（嵌套列表）

典型三段：

- `tokenize`: 给括号加空格再 `split`
- `read_from_tokens`: 递归下降，遇 `(` 就读到配对 `)`，生成 list
- `parse`: 包装入口

### 环境：名字 → 值

用 `ChainMap` 维护“局部覆盖全局”的链式作用域。为了支持 Scheme 的 `set!`（更新已存在绑定），通常补一个 `change` 方法：从近到远找到第一个包含 `name` 的映射并更新。

---

## 灵魂：`evaluate`（用 `match/case` 做语法分派）

解释器最像“一个大分发器”：看到不同形状的 AST，就走不同语义。

`match/case` 的好处是它能直接按“结构”匹配：

- **类型模式**：`case int(x) | float(x)`
- **序列解构**：`case ['if', test, conseq, alt]`
- **捕获 + 守卫**：`case ['lambda', [*parms], *body] if body: ...`

常见分支（Scheme 的“特殊形式”）：

- **`quote`**：不求值，直接返回后面的表达式
- **`if`**：只求值其中一个分支（短路）
- **`define`**：创建绑定（变量或具名函数）
- **`set!`**：更新已有绑定（类似 Python 的 `nonlocal`/`global` 语义）
- **`lambda`**：创建闭包（`Procedure` 捕获定义时环境）
- **函数调用**：`[func_exp, *args]`，先求值函数，再求值参数，再调用

未命中任何模式 → `SyntaxError`（通常把原表达式格式化后报错）。

---

## 关键字与“特殊求值规则”

为什么 `quote/if/define/set!/lambda` 必须被当作关键字？

- 因为它们**改变求值策略**：例如 `quote` 不求值；`if` 只求值一个分支；`define`/`set!` 影响环境。

这和 Python 的 `if/def/return/yield` 类似：不是普通函数调用，解释器必须特殊处理。

---

## 配套代码

`lispy_match_case_demo.py`：

- 解析器：`tokenize/parse/read_from_tokens`
- 环境：`Environment(ChainMap)` + `.change` 支持 `set!`
- 求值：`evaluate` 用 `match/case` 覆盖最小 Scheme 子集
- 演示：直接跑一组 Scheme 表达式（含闭包与 `set!`），无需手动 REPL

