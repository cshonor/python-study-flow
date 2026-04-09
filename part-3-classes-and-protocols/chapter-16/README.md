# 第 16 章「运算符重载」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 16 章：**运算符重载（Operator Overloading）**。

本章讨论如何通过**特殊方法（魔术方法）**让自定义类型支持 `+`、`*`、`**` 等中缀运算符，使代码在数值、向量、金融等场景下更贴近数学表达。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-operator-overloading-intro.md` | 16.1 开篇导读：设计哲学、Python vs Java、适用场景与最佳实践 |
| `02-operator-overloading-basics.md` | 16.2 入门：本章范围、运算符重载的三条限制 |
| `03-unary-operators.md` | 16.3 一元运算符：特殊方法、约定、`x != +x` 例外 |
| `04-vector-add-operator-overloading.md` | 16.4 向量 `+`：`__add__` / `__radd__`、分派与 `NotImplemented` |
| `05-vector-scalar-mul-and-matmul.md` | 16.5–16.6 标量 `*` 与 `@` 点积：`__matmul__` / `__rmatmul__` |
| `06-arithmetic-comparison-augmented-assignment.md` | 16.7–16.9 算术表、比较分派、`+=` 与就地方法 |
| `07-mutable-plus-iadd-addable-bingo-cage.md` | 可变容器：`AddableBingoCage` 的 `__add__` / `__iadd__` |
| `operator_overloading_intro_demo.py` | 配套：`Decimal` 复利 + `Position` 中缀示例 |
| `unary_operators_demo.py` | 配套：`Vector` 一元运算符 + `Decimal` / `Counter` 例外 |
| `vector_add_operator_demo.py` | 配套：`Vector` 的 `+` / `*` / `@` / `__eq__` / `+=` 行为 |
| `addable_bingo_cage_demo.py` | 配套：`AddableBingoCage`（`+` 新建，`+=` 原地并 `return self`） |

---

## 运行

```bash
python part-3-classes-and-protocols/chapter-16/operator_overloading_intro_demo.py
python part-3-classes-and-protocols/chapter-16/unary_operators_demo.py
python part-3-classes-and-protocols/chapter-16/vector_add_operator_demo.py
python part-3-classes-and-protocols/chapter-16/addable_bingo_cage_demo.py
```

---

## GitHub 笔记模板（可复制）

- **定义**：本章要解决什么问题（可读性 / 与内置类型一致 / 反向运算符）？
- **对照表**：`+` ↔ `__add__` / `__radd__`；`*` ↔ `__mul__` / `__rmul__`；`@` ↔ `__matmul__` / `__rmatmul__`；一元 ↔ `__neg__` / `__pos__` / `__abs__`
- **最小示例**：一个可运行 `.py`
- **最佳实践**：语义不变、避免滥用、不可变返回新对象
- **坑点**：`NotImplemented`、`__radd__`、比较反射、`==` 与 `is`、`+=` 是否原地、`__iadd__` 须 `return self`
