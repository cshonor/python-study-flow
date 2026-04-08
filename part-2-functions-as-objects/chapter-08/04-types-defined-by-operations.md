# 8.4 类型由受支持的操作定义：鸭子类型 vs 名义类型（静态检查在看什么）

PEP 483 里有一句很“数学味”的定义，但落到工程上你可以这样理解：

> **类型不是“名字”，而是“你能对它做什么”。**

在 Python 运行时，这几乎就是**鸭子类型**：对象能不能参与某种操作，取决于它有没有对应的方法/协议（例如 `__mul__`），而不是它叫不叫某个类名。

一旦你写了**类型注解**，静态检查器（mypy/pyright）就会进入另一种视角：**名义类型（nominal typing）**——它主要按“声明的类型”去检查属性/方法是否存在（再叠加继承关系）。

本节用 `Bird` / `Duck` / `quack()` 的最小例子，把这两种视角的差异跑清楚。

配套脚本：`duck_nominal_typing_demo.py`。

---

## 一、`double(x)`：运行时很宽，静态检查很“较真”

```python
def double(x):
    return x * 2
```

运行时，`x` 可以是很多实现了乘法语义的东西（`int`、`str`、`list`、自定义 `__mul__` 等）。

但如果你强行把参数注解写成“序列”而不保证乘法：

```python
from collections.abc import Sequence

def double(x: Sequence[int]) -> list[int]:
    return x * 2  # mypy 可能报错：Sequence 没有保证 __mul__
```

关键点：

- **运行时**：对象只要有 `__mul__` 就可能成功；
- **静态检查**：更关注“声明的类型是否支持该操作”。

这就是“类型由受支持的操作定义”在静态层的体现：**声明错了，就会误报/漏报**。

---

## 二、鸭子类型（Duck Typing）：运行时看行为

典型写法：

```python
def alert(birdie):
    birdie.quack()
```

- 静态检查器通常对未注解函数很宽松（渐进式类型）；
- **运行时**才真正执行 `birdie.quack()`：没有方法就 `AttributeError`。

---

## 三、名义类型（Nominal Typing）：静态检查看“声明的类型”

```python
class Bird:
    pass

class Duck(Bird):
    def quack(self) -> None:
        print("Quack!")

def alert_duck(birdie: Duck) -> None:
    birdie.quack()

def alert_bird(birdie: Bird) -> None:
    birdie.quack()
```

- `alert_duck`：声明是 `Duck`，`Duck` 有 `quack`，**mypy 通常满意**。
- `alert_bird`：声明是 `Bird`，但 `Bird` **没有** `quack`，**mypy 会报错**（即使运行时传入 `Duck()` 也能跑通——子类有方法）。

这就是本节最核心的对照：

> **静态检查按“注解的名义类型”约束；运行时按“真实对象”执行。**

---

## 四、两组调用：合法 vs 非法（运行时证据）

配套脚本会分别构造：

- `daffy = Duck()`：三个 `alert*` 调用通常都能跑（`Bird` 无 `quack` 的静态问题仍存在，但运行时 `Duck` 有）
- `woody = Bird()`：运行时会暴露 `quack` 不存在的问题；其中一部分 mypy 能提前拦住

---

## 五、结构类型（Structural Typing）预告：`Protocol`

鸭子类型 + 静态检查的结合点之一是 **`typing.Protocol`**（结构子类型）：

- 不强制继承某个类名；
- 只要实现了约定的方法/属性，就可以通过静态检查。

这会在后续小节/第 13 章更深入展开。

---

## 六、运行

```bash
python part-2-functions-as-objects/chapter-08/duck_nominal_typing_demo.py
```

（可选）对单文件跑 mypy：

```bash
mypy part-2-functions-as-objects/chapter-08/duck_nominal_typing_demo.py
```

在 `duck_nominal_typing_demo.py` 上，mypy 通常会报两类问题（与书本叙述一致）：

1. `alert_bird` 函数体里：`Bird` 没有 `quack`（`attr-defined`）。
2. `Case 2` 里直接调用 `alert_duck(woody)`：`Bird` 不能当作 `Duck` 传入（`arg-type`）。

未注解的 `alert` 不在上述检查焦点内（渐进式类型下常忽略未注解函数体）。
