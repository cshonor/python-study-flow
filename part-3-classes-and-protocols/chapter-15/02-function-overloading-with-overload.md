# 15.x 函数重载（Function Overloading）：`typing.overload` 的工程化用法

Python 运行时**没有**传统意义上的“函数重载”（同名函数多份实现，按参数自动分派）。  
但在**静态类型检查**层面（mypy/pyright/IDE），我们可以用 `typing.overload` 给同一个函数声明**多组类型签名**，从而让：

- 自动补全更准确
- 返回类型推导更精确
- “返回值依赖入参类型”的 API 在类型层面可表达

> 重要：`@overload` **只影响静态检查**。运行时仍然只有一个真正的实现函数。

---

## 一、什么时候需要 `@overload`？

只在一种场景里“非常值得”：

- **返回值类型取决于参数类型**（或关键参数组合）

例如：

- 传入 `str` → 返回单个对象
- 传入 `list[str]` → 返回对象列表

如果只是为了支持“不同参数个数/默认参数”，很多时候用普通默认参数、`*args/**kwargs` 就够了。

---

## 二、书里 `sum` 的核心思路（泛型 + start）

`sum` 的关键在于第二个参数 `start`：

- 不给 `start`，默认从 `0` 开始加 → 返回值类型会和元素类型一起“混合”
- 给了 `start`，返回值类型往往会跟 `start` 更一致

这类函数的难点是：**类型关系**比“具体算法”更复杂，因此 typeshed 会用重载把不同签名拆开。

---

## 三、书里 `max` 的重载为什么复杂？（key/default/iterable/varargs 组合爆炸）

`max` 有几条会导致签名数量爆炸的轴：

- **iterable 形式**：`max(iterable, ...)`
- **多参数形式**：`max(a, b, *rest, ...)`
- **可选 `key`**：比较的是 `key(x)`，但返回仍是原始 `x`
- **可选 `default`**：仅 iterable 形式适用，用于空迭代器

工程化写法通常按“核心组合”拆成几类重载（你图片里那 4 类），而不是把所有边界都写成巨型单签名。

---

## 四、用 `Protocol` 表达“可比较能力”

如果你想表达“这个类型能参与比较”，比起枚举所有名义类型，更贴近 Python 的做法是：

- 定义一个窄协议（例如支持 `__lt__` 或 `__gt__`）
- 用 `TypeVar(bound=...)` 把“能力约束”绑定到泛型上

这就是静态鸭子类型：你不关心它是什么类，只关心它能做什么操作。

---

## 五、与你项目最相关的两类模板

### 1）量化：单值 vs 批量（返回类型不同）

你仓库里的最小实现见 `overload_demo.py`，用重载表达：

- `float -> float`
- `list[float] -> list[float]`

运行：

```bash
python part-3-classes-and-protocols/chapter-15/overload_demo.py
```

### 2）“max 风格”API：`key`/`default`/iterable/varargs

你仓库里的可运行示例见 `max_like_overload_demo.py`，用一组可读的重载覆盖核心组合，并提供一个小实现函数验证运行时行为。

运行：

```bash
python part-3-classes-and-protocols/chapter-15/max_like_overload_demo.py
```

---

## 六、最佳实践（踩坑最少的写法）

- **每个 `@overload` 函数体只写 `...`**（或 `pass`），真正实现写在最后一个同名函数里
- **重载要“少而精”**：覆盖主要业务分支即可，避免无意义的签名爆炸
- **重载顺序**：从更具体到更一般（有时能减少类型检查器歧义）
- **必要时引入窄协议**（`Protocol`）：用“能力”约束，而不是用“名义类型”枚举

