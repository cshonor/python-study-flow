# 第 15 章「类型提示进阶」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 15 章：**类型提示进阶（More About Type Hints）**。

本章承接第 8 章的类型提示基础，目标是把类型提示真正用到“工程级代码”的日常问题里：接口规范、重载、结构化数据、类型收窄、泛型与型变、以及泛型协议（`Protocol`）。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-15.1 开篇导读：为什么大型项目更需要类型规范.md` | 15.1 开篇导读：为什么大型项目更需要类型规范 |
| `02-15.x 函数重载（Function Overloading）：typing.overload 的工程化用法.md` | 函数重载：`@overload` 的适用边界与 `max` 风格签名设计 |
| `03-15.3 TypedDict 深度解读：用字典做“结构化记录”的静态契约.md` | 15.3 `TypedDict`：结构化字典的静态契约与 JSON/Any 局限 |
| `04-15.4 类型校正：typing.cast()（静态检查的“逃生舱”）.md` | 15.4 类型校正：`typing.cast()` 的原理、边界与避坑 |
| `05-15.5 在运行时读取类型提示：__annotations__、get_type_hints 与最佳实践.md` | 15.5 运行时读取类型提示：`get_type_hints` 与工程化封装 |
| `06-15.6 实现一个泛型类（Generic Class）：用 TypeVar + Generic[T] 写可复用组件.md` | 15.6 实现泛型类：`TypeVar` + `Generic[T]` 的通用组件套路 |
| `07-15.7 型变（Variance）：协变 逆变 不变到底在约束什么？.md` | 15.7 型变：协变/逆变/不变与“输出/输入”经验法则 |
| `08-15.8 泛化静态协议（Generic Static Protocol）：Protocol + 泛型 + 型变.md` | 15.8 泛化静态协议：泛型 `Protocol` + 协变/逆变 |
| `02_overload_demo.py` | `@overload`：同名函数多组签名（静态层面） |
| `02_max_like_02_overload_demo.py` | 复杂重载范式：`max` 风格的 iterable/varargs + `key`/`default` 组合 |
| `03_typeddict_demo.py` | `TypedDict`：给“数据字典”定义键-值契约 |
| `04_cast_demo.py` | `cast()`：静态校正 vs 运行时无效果（含误区演示） |
| `04_type_narrowing_demo.py` | 类型收窄：`isinstance` / `assert` / 守卫函数 |
| `05_runtime_type_hints_demo.py` | 运行时访问类型提示：`get_type_hints` / 轻量校验 |
| `05_reading_type_hints_demo.py` | 运行时读取注解：`__annotations__` vs `get_type_hints` |
| `07_generics_variance_demo.py` | 泛型与型变：协变/逆变/不变的直觉与常见坑 |
| `08_generic_protocol_demo.py` | 泛型协议：用 `Protocol` 表达“能力接口” |
| `06_generic_class_lotto_demo.py` | 泛型类：`LottoBlower[T]`（pick/load/inspect 的类型一致性） |
| `07_variance_vending_trash_demo.py` | 型变直觉：不变售货机 / 协变只读售货机 / 逆变垃圾桶 |
| `08_generic_static_protocol_demo.py` | 泛化协议：`SupportsAbs[R_co]` / `RandomPicker[T_co]`（含 runtime_checkable） |

---

## 运行

```bash
python part-3-classes-and-protocols/chapter-15/02_overload_demo.py
python part-3-classes-and-protocols/chapter-15/02_max_like_02_overload_demo.py
python part-3-classes-and-protocols/chapter-15/03_typeddict_demo.py
python part-3-classes-and-protocols/chapter-15/04_cast_demo.py
python part-3-classes-and-protocols/chapter-15/04_type_narrowing_demo.py
python part-3-classes-and-protocols/chapter-15/05_runtime_type_hints_demo.py
python part-3-classes-and-protocols/chapter-15/05_reading_type_hints_demo.py
python part-3-classes-and-protocols/chapter-15/07_generics_variance_demo.py
python part-3-classes-and-protocols/chapter-15/08_generic_protocol_demo.py
python part-3-classes-and-protocols/chapter-15/06_generic_class_lotto_demo.py
python part-3-classes-and-protocols/chapter-15/07_variance_vending_trash_demo.py
python part-3-classes-and-protocols/chapter-15/08_generic_static_protocol_demo.py
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

