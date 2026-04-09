# 第 16 章「运算符重载」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 16 章：**运算符重载（Operator Overloading）**。

本章讨论如何通过**特殊方法（魔术方法）**让自定义类型支持 `+`、`*`、`**` 等中缀运算符，使代码在数值、向量、金融等场景下更贴近数学表达。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-operator-overloading-intro.md` | 16.1 开篇导读：设计哲学、Python vs Java、适用场景与最佳实践 |
| `operator_overloading_intro_demo.py` | 配套：`Decimal` 复利公式 + 轻量量化风格 `Position` 运算符示例 |

---

## 运行

```bash
python part-3-classes-and-protocols/chapter-16/operator_overloading_intro_demo.py
```

---

## GitHub 笔记模板（可复制）

- **定义**：本章要解决什么问题（可读性 / 与内置类型一致 / 反向运算符）？
- **对照表**：运算符 ↔ 特殊方法（如 `+` → `__add__` / `__radd__`）
- **最小示例**：一个可运行 `.py`
- **最佳实践**：语义不变、避免滥用、不可变返回新对象
- **坑点**：`NotImplemented`、`__radd__`、与 `float` 混用等
