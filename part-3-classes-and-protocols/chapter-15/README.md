# 第 15 章「类型提示进阶」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 15 章：**类型提示进阶（More About Type Hints）**。

本章承接第 8 章的类型提示基础，目标是把类型提示真正用到“工程级代码”的日常问题里：接口规范、重载、结构化数据、类型收窄、泛型与型变、以及泛型协议（`Protocol`）。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-type-hints-advanced-intro.md` | 15.1 开篇导读：为什么大型项目更需要类型规范 |
| `overload_demo.py` | `@overload`：同名函数多组签名（静态层面） |
| `typeddict_demo.py` | `TypedDict`：给“数据字典”定义键-值契约 |
| `type_narrowing_demo.py` | 类型收窄：`isinstance` / `assert` / 守卫函数 |
| `runtime_type_hints_demo.py` | 运行时访问类型提示：`get_type_hints` / 轻量校验 |
| `generics_variance_demo.py` | 泛型与型变：协变/逆变/不变的直觉与常见坑 |
| `generic_protocol_demo.py` | 泛型协议：用 `Protocol` 表达“能力接口” |

---

## 运行

```bash
python part-3-classes-and-protocols/chapter-15/overload_demo.py
python part-3-classes-and-protocols/chapter-15/typeddict_demo.py
python part-3-classes-and-protocols/chapter-15/type_narrowing_demo.py
python part-3-classes-and-protocols/chapter-15/runtime_type_hints_demo.py
python part-3-classes-and-protocols/chapter-15/generics_variance_demo.py
python part-3-classes-and-protocols/chapter-15/generic_protocol_demo.py
```

---

## GitHub 笔记模板（你可以直接复制）

建议每个小节都按这个结构沉淀：

- **定义/目标**：这一节解决什么工程问题？
- **核心规则**：1–5 条即可
- **最小可运行示例**：一个 `.py` 文件，能直接运行
- **静态检查要点**：写出“类型检查器会报什么错/为什么”
- **坑点记录**：你自己踩过的坑 + 规避方式
- **迁移建议**：如何把它用到你的项目（FastAPI / Agent / 量化 / Web3）

