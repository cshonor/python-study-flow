# 9.8 计时装饰器（clock）：从最小可用到“可用于生产”的三个修复

这一节用一个非常典型的计时装饰器 `clock` 把装饰器写法走完整：**先写能跑的最小版**，再把它一步步修到“能安全复用”。你最后要形成肌肉记忆的优化点只有三个：

- wrapper 必须支持 `*args, **kwargs`（不然一遇到关键字参数就炸）
- 必须用 `functools.wraps`（不然函数元信息会丢）
- 计时代码应该尽量“无侵入”：只记录、打印、然后原样返回结果

配套脚本：`clock_decorator_demo.py`。

---

## 一、基础版（能跑，但有坑）

```python
import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result
    return clocked
```

这段代码已经包含了装饰器的全部本质：

- `clocked` 是闭包：它捕获了自由变量 `func`
- `@clock` 等价于：`func = clock(func)`
- 计时逻辑发生在 wrapper 每次调用时

### 基础版的两个缺陷

1. **不支持关键字参数**：wrapper 只有 `*args`，调用 `f(x=1)` 会报错。
2. **覆盖元信息**：`func.__name__`/`__doc__`/签名都会变成 wrapper 的（例如 `__name__ == "clocked"`），影响调试、文档、框架（路由/依赖注入）等。

---

## 二、优化版（生产级最低要求）

```python
import time
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_list = [repr(a) for a in args]
        arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
        arg_str = ", ".join(arg_list)
        print(f"[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}")
        return result
    return clocked
```

修复点：

- `*args, **kwargs`：兼容所有调用方式
- `@wraps(func)`：把元信息从原函数复制到 wrapper（名字、文档、模块、注解等）
- 打印参数：把 `args` 与 `kwargs` 都纳入输出

---

## 三、验证：递归函数与“装饰发生在导入时”

用 `factorial` 递归调用时，你会看到每一层都被计时并打印：这说明装饰后的 `factorial` 已经被替换成 wrapper，并在递归过程中被反复调用。

同时也别忘了前面章节的结论：**装饰过程发生在导入时**，wrapper 的定义与返回只发生一次；真正“每次调用都做的事”是在 wrapper 里面。

---

## 四、小结（最容易背错但最重要的三句话）

1. **装饰器 = 函数替换**：`@clock` 等价于 `func = clock(func)`。
2. **wrapper 要写成 `(*args, **kwargs)`**，否则装饰器不可复用。
3. **自定义装饰器基本都应该 `@wraps(func)`**，否则你得到的是“行为正确但工具链难用”的函数。

