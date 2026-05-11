# 《流畅的 Python》第 9 章：装饰器与闭包 — 学习路线与总览

本文件是 **`chapter-09/`** 的**地图**：把「自底向上」的递进关系，映射到仓库里**已有**的 `01`～`10` 笔记与 **`.py` demo**（文件名仍按本仓库约定：`NN-中文标题.md`、`NN_xxx_demo.py`）。**正文仍以各 `NN-…md` 为准**；此处给**骨架、可复制最小例、易错点**。

---

## 一、整体递进（建议理解的顺序）

下面这条链**在概念上**最好按顺序吃透（与「为什么装饰器绕不开闭包」直接相关）：

1. **一等函数**：函数可当值传来传去（见 [第 7 章](../chapter-07/README.md) 铺底；本章继续用）。  
2. **作用域与 LEGB**：名字到底从哪一层找。  
3. **闭包（closure）**：内层函数携带外层环境。  
4. **`nonlocal`**：闭包里要**改**外层变量时怎么用。  
5. **基础装饰器**：`@` 与高阶函数的关系。  
6. **注册式装饰器**：`import` 时发生了什么。  
7. **计时装饰器 `clock`**：从玩具到可维护。  
8. **`functools`**：`wraps`、`lru_cache` / `cache`、`singledispatch` 等。  
9. **参数化装饰器**：装饰器自己也要参数。  
10. **类式装饰器**：用 `__call__` 组织更复杂的状态。

> **首刷跟书 / 跟目录**：按 **`01` → `02` → … → `10`** 读最顺（见下表）。  
> **二刷自底向上**：可按 **`05` → `06` → `07` → `02` → `03` → …** 把「作用域 / 闭包 / nonlocal」先压实，再回来看装饰器语法糖。

---

## 二、与仓库文件的对应表（点开即读）

| 小节 | 笔记 | 配套脚本（节选） |
|------|------|------------------|
| 9.1 开篇路线 | [01-9.1 …](<./01-9.1 开篇路线：为什么装饰器离不开闭包（以及这章怎么学）.md>) | — |
| 9.2 `@` 做了什么 | [02-9.2 …](<./02-9.2 装饰器基础知识：@ 到底做了什么（以及它什么时候执行）.md>) | `02_decorators_basics_demo.py` |
| 9.3 注册式装饰器 | [03-9.3 …](<./03-9.3 注册式装饰器：为什么 import 一下就“执行了代码”.md>) | `03_registration.py` |
| 9.4 注册（跨模块等） | [04-9.4 …](<./04-9.4 注册装饰器（实战）：装饰器与被装饰对象不在同一模块时怎么组织.md>) | 同主题见 `03` / `10` 中注册片段 |
| 9.5 作用域 / LEGB | [05-9.5 …](<./05-9.5 变量作用域：为什么“函数里一赋值就变局部”（用 dis 看证据）.md>) | `05_scope_dis_demo.py`、`05_scope_closure_nonlocal_demo.py` |
| 9.6 闭包 | [06-9.6 …](<./06-9.6 闭包（Closure）深度理解：累计平均值、自由变量与 cell.md>) | `06_averager_closure_demo.py` |
| 9.7 `nonlocal` | [07-9.7 …](<./07-9.7 nonlocal 与名字解析：闭包里为什么 += 会炸（以及完整查找规则）.md>) | `07_nonlocal_name_resolution_demo.py` |
| 9.8 `clock` | [08-9.8 …](<./08-9.8 计时装饰器（clock）：从最小可用到“可用于生产”的三个修复.md>) | `08_clock_decorator_demo.py` |
| 9.9 `functools` | [09-9.9 …](<./09-9.9 functools 标准库装饰器：缓存（cache lru_cache）与单分派（singledispatch）.md>) | `09_functools_decorators_demo.py`、`02_decorator_and_cache_demo.py` |
| 9.10 参数化 + 类装饰器 | [10-9.10 …](<./10-9.10 参数化装饰器与类式装饰器：让装饰器“可配置”.md>) | `10_parameterized_decorators_demo.py` |

目录级命令汇总：[`README.md`](README.md)。

---

## 三、核心结论（底层三句）

1. **装饰器在形式上**几乎都是：**高阶函数（接收函数、返回可调用对象）+ 闭包（保存状态）**；`@` 只是语法糖：`f = decorator(f)`。  
2. **不懂作用域**：`UnboundLocalError`、`global` / `nonlocal` 为什么会懵。  
3. **不懂闭包**：带状态的装饰器、工厂返回的 `wrapper`，很难改对。

**新手常见误区**：一上来只背 `@` 模板。更稳的顺序是：**LEGB → 闭包 → `nonlocal` → `@`**。

---

## 四、极简可复制示例（与正文不冲突的最小核）

### 4.1 `@` 等价于「把函数名重新赋值」

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"即将执行：{func.__name__}")
        result = func(*args, **kwargs)
        print("执行完毕")
        return result
    return wrapper


@simple_decorator
def add(a: int, b: int) -> int:
    return a + b


# 与下面一行等价（定义结束时发生）：
# add = simple_decorator(add)

print(add(10, 20))
```

### 4.2 注册式：`import` 时就会跑装饰器函数体

```python
strategy_registry: list[object] = []


def register_strategy(func: object) -> object:
    print(f"注册：{getattr(func, '__name__', func)}")
    strategy_registry.append(func)
    return func


@register_strategy
def macd_strategy() -> str:
    return "MACD"


@register_strategy
def rsi_strategy() -> str:
    return "RSI"


print("已注册：", [getattr(f, "__name__", str(f)) for f in strategy_registry])
```

更完整的「import 时机」对照见 **`03_registration.py`**。

### 4.3 LEGB 经典坑：先读后写同一名字

```python
count = 100


def test_scope() -> None:
    print(count)  # UnboundLocalError：本函数对 count 有赋值，整体视为局部名
    count = 200
```

修法：只读不写全局则不要在本函数赋值；要改模块全局用 **`global count`**；要改**外层函数**的变量用 **`nonlocal`**（见 **07**）。

用 **`dis.dis(test_scope)`** 看字节码：失败分支里常见 **`LOAD_FAST`**，而不是去读全局的 **`LOAD_GLOBAL`**（细节见 **05**）。

### 4.4 闭包：状态挂在「内层函数 + cell」上

```python
def avg_calculator():
    history: list[float] = []

    def add_and_calc(new_val: float) -> float:
        history.append(new_val)
        return sum(history) / len(history)

    return add_and_calc


avg = avg_calculator()
print(avg(10))  # 10.0
print(avg(20))  # 15.0
```

要对**数值累加器**用 `+=` 改外层变量，需 **`nonlocal`**（错误/正确对照见 **06 / 07**）。

### 4.5 `functools.wraps`：避免 `__name__` / docstring 丢光

工业里 `wrapper` 上叠 **`@functools.wraps(func)`**（完整写法与三项修复见 **08**）。

### 4.6 `lru_cache`：参数必须可哈希；`n` 别乱大到离谱

```python
import functools


@functools.lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(fibonacci(35))  # 演示即可；n 过大既慢也易产生超大整数
```

**注意**：`lru_cache` 要求参数都可 **`hash`**；递归深度受 **`sys.getrecursionlimit()`** 约束，教学示例用**中等 `n`** 即可。更全对比见 **`09_functools_decorators_demo.py`**。

### 4.7 参数化装饰器：多一层「工厂」

```python
import functools
import time


def clock(*, precision: int = 6):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            t0 = time.perf_counter()
            res = func(*args, **kwargs)
            dt = time.perf_counter() - t0
            print(f"{func.__name__} 耗时: {dt:.{precision}f}s")
            return res
        return wrapper
    return decorator


@clock(precision=8)
def backtest() -> None:
    pass


backtest()
```

类式装饰器（`__call__` + `update_wrapper`）见 **10** 与 **`10_parameterized_decorators_demo.py`**。

---

## 五、量化 / 工程落地清单（对照用）

1. 给策略、因子、回测入口统一加**计时 / 日志**，先定位热点再优化。  
2. 对**纯函数、重复输入**用 **`cache` / `lru_cache`** 降重复算（注意哈希与内存）。  
3. 用**注册表**自动收集策略/因子，减少手写维护列表。  
4. 横切关注点（鉴权、风控、异常捕获）用装饰器收口，业务函数保持「瘦」。

---

## 六、GitHub / 本仓库说明

- 本仓库**已拆成** `01`～`10` 多篇 Markdown，并各有 **`.py`** 对照；**不建议**再改成「全英文无编号」文件名，否则会断链接、也难与篇号对齐。  
- 新增的这一份 **`00-…总览.md`** 用于：**归档、导航、复制最小例**；修订以 **`README.md` 文件一览**为准同步。

---

## 七、官方与延伸阅读（查阅）

- 《流畅的 Python》第二版第 9 章原文结构。  
- 标准库：**`functools`**、`inspect`、 **`dis`**（配合 **05** 看字节码）。

若要**一键运行本章全部 demo**：见 [`README.md`](README.md) 底部命令块。
