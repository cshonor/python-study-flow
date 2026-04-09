# `if` 之外的 `else`：`for/else`、`while/else`、`try/else`（18.4）

## 一条总规则（别按 `if/else` 理解）

`else` 不只属于 `if`。在 `for/while/try` 里，它的语义非常统一：

| 组合 | `else` 何时执行 | 可以把它读作 |
|------|------------------|--------------|
| **`for/else`** | 循环**正常结束**（没有 `break`） | “遍历完还没 `break`，那就…” |
| **`while/else`** | 条件变为假而**正常退出**（没有 `break`） | “没被 `break` 打断，那就…” |
| **`try/else`** | `try` 块**没有抛出异常** | “try 成功了，那就…” |

要点：这里的 `else` 更像一个没出现在语法里的 `then`（“先做这个，再做那个”），而不是 `if` 的分支对立面。

---

## `for/else`：查找时最顺手

经典写法：遍历寻找目标，找到就 `break`；遍历完没找到，就走 `else`。

```python
for item in items:
    if is_target(item):
        found = item
        break
else:
    raise LookupError("not found")
```

优势：避免写额外的 `found = False` 标记变量。

---

## `while/else`：重试/轮询的“自然收尾”

`while` 常用于“最多重试 N 次”或“轮询直到条件满足”：

- `break`：表示“命中了/成功了/提前终止了”
- `else`：表示“没命中，一直循环到条件为假（通常是超时/次数耗尽）”

---

## `try/else`：把“风险代码”和“成功后的逻辑”分开

`try/else` 的推荐用法是：

- `try`：只放**可能抛出你准备捕获的异常**的语句
- `except`：处理预期异常
- `else`：放**只有在 try 成功时才运行**的后续逻辑

对比：

```python
# 不推荐：after_call 的异常也会被 except 吃掉（误捕获）
try:
    dangerous_call()
    after_call()
except OSError:
    handle()

# 推荐：try 只包危险操作；else 表达“成功后再做”
try:
    dangerous_call()
except OSError:
    handle()
else:
    after_call()
```

规则补充：`else` 里抛出的异常，不会被前面的 `except` 捕获（这正是它“分离关注点”的价值）。

---

## EAFP vs LBYL（理解 `try/else` 的背景）

| 风格 | 核心 | 常见写法 |
|------|------|----------|
| **EAFP** | 先做，失败再捕获 | `try: x = d[k] except KeyError: ...` |
| **LBYL** | 先检查，再做 | `if k in d: ... else: ...` |

EAFP 往往更短、更不容易在并发/竞态条件下写出“检查与使用之间被改掉”的 bug；`try/else` 是 EAFP 写法里很自然的一块拼图。

---

## 配套代码

`else_clauses_demo.py`：覆盖

- `for/else`：查找失败走 `else`
- `while/else`：重试耗尽走 `else`
- `try/else`：仅当 `try` 无异常才执行 `else`
- EAFP vs LBYL：用最小例子对照

