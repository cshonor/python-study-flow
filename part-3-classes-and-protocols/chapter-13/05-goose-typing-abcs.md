# 13.5 大鹅类型（Goose Typing）：抽象基类（ABC）表示接口

这一节的主线是：在保持 Python 动态灵活的前提下，**用抽象基类（ABC）给协议加一把“运行时检查”的安全锁**。

你可以把它理解为：

- **鸭子类型**：你像什么就能当什么用（结构 + 运行时）
- **大鹅类型**：你“被标记为/声明为”什么，运行时就能检查你是不是它（名义 + 运行时）

本章用“Goose Typing（大鹅类型）”这个绰号强调：ABC 更像“生物分类学”的血缘标签（名义类型），而不是只看外形相似。

---

## 一、大鹅类型的本质：抽象类表示接口

ABC 的价值主要在三点：

- **接口契约更明确**：继承某个 ABC（或被注册为虚拟子类）就等于声明“我支持这个接口”
- **运行时可检查**：`isinstance(x, SomeABC)` / `issubclass(...)`
- **快速失败**：缺少必要抽象方法的子类，实例化时就会抛 `TypeError`

---

## 二、13.5.1 子类化标准库 ABC：从 `FrenchDeck` 到 `FrenchDeck2`

### 1）鸭子类型的 `FrenchDeck`：序列能用，但 `shuffle` 不行

只实现 `__len__` + `__getitem__` 的类，像“只读序列”：

- `len(deck)`、索引、切片、迭代都能用
- 但 `random.shuffle(deck)` 会失败，因为 `shuffle` 需要就地交换元素 → 需要 `__setitem__`

### 2）继承 `MutableSequence`：把“可变序列接口”变成显式契约

继承 `collections.abc.MutableSequence` 后：

- **必须实现**：`__len__`、`__getitem__`、`__setitem__`、`__delitem__`、`insert`
- **自动获得**：`append`、`extend`、`reverse`、`pop`、`remove`、`__iadd__` 等一堆现成方法

这就是 ABC 的“规范化协议”：你实现最小抽象集，它就能提供更多默认实现。

---

## 三、13.5.2 `collections.abc`：容器接口的“命名体系”

`collections.abc` 把常见的容器接口拆成一组可组合的 ABC（例如 `Iterable`、`Sized`、`Container`、`Sequence`、`Mapping`、`Set`…）。

理解它的一个好处是：你在写框架/库时，检查的往往不是 `list`/`dict`，而是：

- `isinstance(x, Sequence)`
- `isinstance(x, Mapping)`
- `isinstance(x, Iterable)`

这样才能把“接口依赖”从“具体实现”里剥离出来。

---

## 四、13.5.3 自定义 ABC：`Tombola`（抽象方法 + 具体方法）

自定义 ABC 的经典示例是 `Tombola`：

- 抽象方法：`load(iterable)`、`pick()`
- 具体方法：`loaded()`、`inspect()`  
  具体方法只依赖抽象方法，从而对所有子类复用

设计要点：

- `pick()` 约定空时抛 `LookupError`（和 `IndexError`/`KeyError` 同属一脉）
- 抽象基类的具体方法应该只依赖“接口契约”，而不依赖某个子类的内部结构

---

## 五、虚拟子类（virtual subclass）：注册而非继承

有些时候你无法/不想修改原类让它继承 ABC（例如第三方类、内置类型、旧代码）：

- 可以用 `SomeABC.register(SomeClass)` 把它注册为“虚拟子类”
- 这样 `isinstance(x, SomeABC)` 会通过

但要注意：

- **注册不会自动补齐方法**：它只是在类型系统层面贴了标签
- 你仍然需要确保该类在行为上满足 ABC 的接口要求，否则运行时照样可能报错

---

## 配套代码

对应可运行示例见 `goose_typing_abcs_demo.py`：

- `FrenchDeck` vs `FrenchDeck2(MutableSequence)`：`shuffle`、自动方法、运行时检查
- `Tombola(ABC)`：抽象方法/具体方法、快速失败、虚拟子类注册

