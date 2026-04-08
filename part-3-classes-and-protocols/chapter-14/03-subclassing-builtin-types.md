# 14.3 子类化内置类型很麻烦：`dict`/`list` 等的经典陷阱

这一节要澄清一个很“反直觉”的事实：

> 在 CPython 里，某些内置类型（`dict`/`list`/`str`…）的关键方法由 C 实现，**内部往往不会通过 Python 层的特殊方法分派**，因此可能绕过你在子类里重写的 `__setitem__` / `__getitem__` 等方法。

结果就是：你以为你改了“字典行为”，但只有某些语法路径（如 `d[k] = v`）会走到你的重写；而 `update()` / `__init__()` 等内置实现可能直接走 C 代码路径，把你的重写完全跳过。

---

## 一、经典坑 1：`DoppelDict(dict)` 重写 `__setitem__`

目标：任何写入都把值变成 `[value, value]`。

表面上写起来很合理：

```python
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value, value])
```

但在 CPython 里：

- `dd['two'] = 2` 会触发 `__setitem__`（✅）
- `DoppelDict(one=1)`、`dd.update(three=3)` **可能绕过** `__setitem__`（❌）

这会导致同一个类在不同写入路径下行为不一致。

---

## 二、经典坑 2：`AnswerDict(dict)` 重写 `__getitem__`

目标：无论取什么键都返回 `42`：

```python
class AnswerDict(dict):
    def __getitem__(self, key):
        return 42
```

你会发现：

- `ad['a']` 是 `42`（✅）
- 但 `d = {}; d.update(ad)` 得到的 `d['a']` 仍然是原值 `'foo'`（❌）  
  因为 `dict.update` 在内部并不一定通过 `__getitem__` 去读取源映射的值。

---

## 三、为什么会这样？（面向工程的解释）

这不是“继承不工作”，而是：

- 内置类型追求性能，内部操作可能直接访问底层存储结构
- 这种实现方式不保证“每一条内部路径都经过你重写的 Python 方法”

因此：

> **子类化内置类型更适合做“附加 API”，不适合改变其核心语义。**

---

## 四、解决方案 1：用 `collections.User*` 替代

标准库提供了三类“可安全子类化”的包装器：

| 内置类型 | 推荐替代 | 模块 |
|---|---|---|
| `dict` | `collections.UserDict` | `collections` |
| `list` | `collections.UserList` | `collections` |
| `str` | `collections.UserString` | `collections` |

它们的关键优势是：

- 主要逻辑是 **Python 实现**
- 方法调用更遵循常规的“晚绑定”分派
- 子类覆盖的方法在更多路径下能一致生效

---

## 五、解决方案 2：组合优于继承

如果你的目标只是：

- 添加一些工具方法
- 或对外暴露受控的子集 API

更建议用组合（内部持有一个 `dict`/`list` 实例），避免继承带来的耦合与分派陷阱。

---

## 配套代码

对应可运行示例见 `builtin_subclass_pitfalls_demo.py`，包含：

- `dict` 子类的两种反例 + `UserDict` 修复
- `list` 子类的一个常见坑 + `UserList` 修复

