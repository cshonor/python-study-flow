# 9.4 注册装饰器（实战）：装饰器与被装饰对象不在同一模块时怎么组织

第 9 章前面你已经看到装饰器的本质是：

```python
target = decorate(target)
```

但在工程里，“装饰器和被装饰函数写在同一个文件”只是最简单的一种情况。本节关心的是更常见的实践场景：**装饰器定义在一个模块里，被装饰函数分散在很多模块里**。

这时注册式装饰器（registration decorator）会非常自然：导入时把函数“登记”到一个注册表里，后续统一处理（路由、命令、插件、策略等）。

配套：`registration.py` 与 `03-registration-decorator-import-time.md`。

---

## 一、两种常见写法

### 1）常规（包装式）装饰器：返回 `wrapper`

特征：

- 装饰器返回一个新函数（或其他可调用对象）
- 新函数在内部调用原函数并增强行为（日志、计时、重试、缓存……）

```python
from __future__ import annotations

from collections.abc import Callable
from functools import wraps

def log_calls(func: Callable[..., object]) -> Callable[..., object]:
    @wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        print("calling", func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

这种写法通常“就地生效”：你调用被装饰函数时，增强逻辑就会执行。

### 2）注册式装饰器：登记到 `registry`，通常返回原函数

特征：

- 装饰器的核心工作不是包装，而是**登记元信息**
- 常见做法是“返回原函数”，保持调用语义不变

```python
from collections.abc import Callable

registry: list[Callable[[], None]] = []

def register(func: Callable[[], None]) -> Callable[[], None]:
    registry.append(func)
    return func
```

这种写法的价值在于：**被装饰对象可以分散在多个模块**，只要被导入就会自动注册。

---

## 二、为什么工程里更常见“装饰器在 A 模块，函数在 B/C/D 模块”？

因为你往往需要一个“中心”来管理能力：

- **Web 路由**：`@app.get("/path")` 登记路由表（FastAPI/Starlette 风格）
- **命令系统**：`@cli.command()` 登记子命令（Click/Typer 风格）
- **插件系统**：`@plugin("name")` 登记插件工厂
- **策略/规则**：`@rule("v2")` 登记某种规则实现

注册表的形态通常是：

- `list[callable]`：简单、保持顺序
- `dict[str, callable]`：按名字查找
- 更复杂的结构：按 group/version/priority 分桶

---

## 三、关键提醒：注册发生在“导入时”

注册式装饰器往往天然具有“导入即副作用”：

- **导入了模块** → 执行装饰过程 → 函数进入注册表

这既是强大之处，也是坑点来源：

- 你必须确保“需要注册的模块”会被导入
- 也必须避免装饰器里做重活（网络、I/O、耗时计算），否则导入会变慢/变脆弱

实战里常见的做法是：

- 装饰器只做登记（纯内存操作）
- 真正的初始化放到程序启动的显式阶段执行

