# 13.5.6–13.5.8 虚拟子类、`__subclasshook__` 与结构类型（runtime structural typing）

这几节回答的是一个“看似矛盾但很 Python”的问题：

> 既然 ABC（大鹅类型）是名义类型（看继承/标签），为什么它又能在运行时表现出结构类型（看方法是否存在）的味道？

答案在两套机制里：

- **虚拟子类（virtual subclass）**：`SomeABC.register(SomeClass)` 手动贴标签
- **`__subclasshook__`**：在 ABC 上定义“自动识别”规则（由 `ABCMeta` 调用）

它们把鸭子类型（结构）与大鹅类型（名义）连接了起来。

---

## 一、虚拟子类：`register` 只是“类型标签”，不是继承

### 1）定义

虚拟子类指：

- **不继承**某 ABC
- 通过 `ABC.register(Cls)`（或 `@ABC.register` 装饰器）注册
- 让 `issubclass(Cls, ABC)` / `isinstance(obj, ABC)` 返回 `True`

### 2）最容易踩的坑（也是本节重点）

`register` 的效果只有一个：**改变 `isinstance/issubclass` 的结果**。

它不会：

- **把 ABC 的具体方法“注入”到子类里**（不会继承）
- **检查被注册类是否真的实现了抽象方法**（不校验）

因此注册是一种“承诺”：

- 你对外声明：“这个类在行为上满足该 ABC 的接口”
- 但 Python 不替你验证

---

## 二、示例：`TomboList` 注册为 `Tombola` 的虚拟子类

用 `@Tombola.register` 装饰 `TomboList` 之后：

- `TomboList.__mro__` 里**不会出现** `Tombola`
- 但 `isinstance(TomboList(...), Tombola)` 为真

进一步验证“不会继承方法”：

- 即使 `Tombola` 定义了 `loaded/inspect` 具体方法，`TomboList` 也**不会自动拥有**它们  
  （因为根本没进入 MRO）

---

## 三、`__subclasshook__`：让 ABC 支持运行时“结构识别”

`__subclasshook__` 是 ABC 的一个类方法钩子，用来定制：

- `issubclass(C, SomeABC)` 的判断逻辑

它必须返回：

- `True`：认定为子类
- `False`：认定不是子类
- `NotImplemented`：交回默认继承/注册规则处理

### 标准库示例：`collections.abc.Sized`

`Sized` 的结构含义就是“有 `__len__`”。因此它会通过 `__subclasshook__` 在运行时做一个结构检查：

- 只要某个类在其 `__mro__` 链上定义了 `__len__`，就会被 `isinstance(x, Sized)` 识别为真

这就是“ABC 里的结构类型”：**runtime structural typing**。

---

## 四、结构类型与名义类型在 ABC 中如何共存？

你可以把它理解为两层：

- **名义层（nominal）**：真实继承 / `register` 贴标签
- **结构层（structural）**：`__subclasshook__` 做“像不像”的自动识别

它们可以叠加：一个类既可以被注册，也可以被 `__subclasshook__` 判定为真。

---

## 五、实践建议（书中的态度）

- **业务代码**：优先写“鸭子类型”代码，把协议当接口用（少依赖 `isinstance`）
- **框架/库**：可以用 `collections.abc` 的 ABC 作为对外接口契约
- **虚拟子类**：适合给第三方/内置类型“贴标签”，但要清楚它不做校验、不提供继承
- **`__subclasshook__`**：自定义时要非常谨慎；它只能检查“方法是否存在”，很难检查“语义是否正确/签名是否兼容”

---

## 配套代码

对应可运行示例见 `virtual_subclass_and_subclasshook_demo.py`：

- `register`：证明“贴标签但不继承、不校验”
- `Sized.__subclasshook__`：证明“运行时结构识别”

