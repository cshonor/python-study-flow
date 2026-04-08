# 9.10 参数化装饰器与类式装饰器：让装饰器“可配置”

到目前为止你看到的装饰器大多是：

```python
@deco
def f(...): ...
```

它的等价形式是：

```python
f = deco(f)
```

但一旦你想让装饰器“接收参数”（开关、格式、注册表选择……），就必须升级为：

```python
@deco(arg)
def f(...): ...
```

等价形式变成：

```python
f = deco(arg)(f)
```

也就是说：**装饰器参数会先喂给外层函数，外层函数返回真正的装饰器**。

配套脚本：`parameterized_decorators_demo.py`。

---

## 一、为什么需要参数化装饰器？

常规装饰器逻辑是固定的，而参数化装饰器让你能做这些事：

- **开关控制**：`active=True/False` 决定是否注册/是否启用
- **自定义配置**：计时装饰器 `fmt=...` 自定义日志输出
- **选择目标**：把注册信息存到不同 registry（list/set/dict 或分组 registry）

---

## 二、方案 1：参数化“注册装饰器”（工厂函数模式）

关键：三层结构里，最外层只负责**接收参数并返回装饰器**。

```python
registry: set[callable] = set()

def register(active: bool = True):
    def decorate(func):
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate
```

使用时要注意一条规则：

- **即使使用默认参数，也要写 `@register()`**（因为你需要先调用工厂函数拿到真正装饰器）。

---

## 三、方案 2：参数化 clock（自定义输出格式）

同样的三层结构：

1. `clock(fmt)`：接收参数
2. `decorate(func)`：接收被装饰对象
3. `clocked(*args, **kwargs)`：每次调用时执行的 wrapper

实践上建议同时做到：

- wrapper 支持 `*args, **kwargs`
- 使用 `functools.wraps(func)` 保留元信息

---

## 四、方案 3：类式装饰器（`__call__`）

类式写法的核心是：**实例可调用**就能当装饰器用。

```python
class Clock:
    def __init__(self, fmt=DEFAULT_FMT):
        self.fmt = fmt

    def __call__(self, func):
        def clocked(*args, **kwargs):
            ...
        return clocked
```

优势（工程视角）：

- 配置状态放在 `self` 上，更直观
- 容易扩展（继承/组合）
- 当装饰器需要较多配置/方法时，代码结构更清晰

---

## 五、三种写法对比（简表）

| 方案 | 是否可配置 | 状态放哪 | 适合场景 |
|---|---:|---|---|
| 普通装饰器 | 否 | 闭包 | 简单增强（日志/计时/重试等） |
| 工厂函数装饰器 | 是 | 闭包（外层参数） | 少量配置、开关、选择 registry |
| 类式装饰器 | 是 | `self` | 配置多、需要扩展、工程化 |

