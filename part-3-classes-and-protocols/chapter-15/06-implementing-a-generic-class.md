# 15.6 实现一个泛型类（Generic Class）：用 `TypeVar` + `Generic[T]` 写可复用组件

这一节的目标很明确：把“同一份业务逻辑”抽象成一个可复用类，并且在静态类型层面保证它的输入输出一致。

你可以把 Python 的泛型理解为：

- **对类型检查器的承诺**：这里的 `T` 在整个类/方法里保持一致
- **对运行时的零成本**：`LottoBlower[int]` 和 `LottoBlower[str]` 运行时仍是同一个类（泛型主要服务静态检查）

---

## 一、核心术语速记

| 术语 | 含义 | 示例 |
|---|---|---|
| **泛型** | 含有类型变量的类型 | `LottoBlower[T]` |
| **形式类型参数** | 泛型声明里的 `TypeVar` | `T` |
| **参数化类型** | 用具体类型实参“填充”后的类型 | `LottoBlower[int]` |
| **具体类型参数** | 你填进去的具体类型 | `int` |

---

## 二、实现套路：`TypeVar` → `Generic[T]` → 用 `T` 约束参数/返回值

实现一个泛型类的最小套路：

1. 定义 `T = TypeVar('T')`
2. 类继承 `Generic[T]`
3. 在方法签名里用 `T` 约束：
   - `__init__(items: Iterable[T])`
   - `load(items: Iterable[T])`
   - `pick() -> T`
   - `inspect() -> tuple[T, ...]`

---

## 三、案例：泛型摇奖机 `LottoBlower[T]`

为什么这个例子很典型：

- 逻辑完全和元素类型无关（只是“装进去、随机取出”）
- 但我们希望：装进去的是 `T`，取出来的也必须是 `T`

这样在工程里你就能写出：

- `LottoBlower[int]`：只装 int
- `LottoBlower[str]`：只装 str
- `LottoBlower[Order]`：只装订单对象

配套可运行代码见 `generic_class_lotto_demo.py`。

---

## 四、泛型的边界：静态有用，运行时不“变身”

`LottoBlower[int]` 的主要价值：

- mypy/IDE 能推导 `pick()` 返回 `int`
- `load()` 不允许你传 `str` 的 iterable（静态层面报错）

但运行时：

- Python 不会自动检查 `load()` 传入的元素类型
- 运行时校验需要你自己写（或用 Pydantic 等工具）

---

## 对应代码

- `generic_class_lotto_demo.py`

