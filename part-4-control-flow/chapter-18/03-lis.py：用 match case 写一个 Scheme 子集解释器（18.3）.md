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

## `Procedure`：用类实现闭包（18.3.7）

`Procedure` 的定位是“用户定义的 Scheme 过程”：它是一个可调用对象，**保存函数定义时的参数、函数体、以及定义时环境**，因此天然就是闭包。

调用流程（对应 Scheme 的函数调用）：

- **构建局部环境**：把 `parms` 与调用时的实参 `args` 通过 `zip` 绑定成字典
- **组合环境**：`Environment(local, self.env)`（局部在前，捕获环境在后），实现“局部覆盖自由变量”
- **依次求值函数体**：在组合环境里对 `body` 逐个 `evaluate`
- **返回最后一个表达式的值**：Scheme 约定过程返回最后一次求值结果

自由变量的关键点：

- `Procedure` 捕获的是**定义时环境**，不是调用时环境；因此“函数 + 环境”才是闭包。
- Scheme 的 `set!` 更新已有绑定，对应到 Python 里你会联想到 `nonlocal`/`global` 的“向外层作用域写入”。

---

## OR 模式：`case A(x) | B(x)`（18.3.8）

OR 模式用 `|` 连接多个子模式：任意一个匹配成功就进入该分支。

典型用法：

- `case int(x) | float(x): ...` 统一处理数字原子

限制（解释器里很重要）：

- **所有子模式必须绑定同名变量**：比如 `int(x) | float(x)` 可以；`int(a) | float(b)` 不行。
- 在 `case` 里 `|` 是“模式 OR”，不会触发对象的 `__or__`；离开模式匹配上下文后，`|` 才是按位或/集合并集等运算符。

---

## 关键字与“特殊求值规则”

为什么 `quote/if/define/set!/lambda` 必须被当作关键字？

- 因为它们**改变求值策略**：例如 `quote` 不求值；`if` 只求值一个分支；`define`/`set!` 影响环境。

这和 Python 的 `if/def/return/yield` 类似：不是普通函数调用，解释器必须特殊处理。

解释器里经常会在“函数调用”分支加卫语句（guard）：

- 形如 `case [func_exp, *args] if func_exp not in KEYWORDS: ...`
- 目的：避免把 `lambda/if/define/...` 这种“特殊形式”误当作普通调用去环境里查找。

---

## 配套代码

`03_lispy_match_case_demo.py`：

- 解析器：`tokenize/parse/read_from_tokens`
- 环境：`Environment(ChainMap)` + `.change` 支持 `set!`
- 求值：`evaluate` 用 `match/case` 覆盖最小 Scheme 子集
- 演示：直接跑一组 Scheme 表达式（含闭包与 `set!`），无需手动 REPL

