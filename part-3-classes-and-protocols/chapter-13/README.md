# 第 13 章「接口、协议和抽象基类」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 13 章：**接口、协议和抽象基类**。

本章开篇核心观点是 GoF 的那句原则：

> **对接口编程，而不是对实现编程。**

在 Python 语境下，“接口”常常不是 `interface` 关键字，而是以 **协议（protocol）/抽象基类（ABC）/类型提示** 等形式出现。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-interfaces-protocols-abcs-overview.md` | 第 13 章开篇：四种“类型系统”视角与适用场景 |
| `02-type-chart-and-four-type-systems.md` | 13.2 类型图：检查时机 × 类型依据（四象限理解） |
| `03-dynamic-vs-static-protocols.md` | 13.3 两种协议：动态协议 vs 静态协议（`Protocol`） |
| `04-programming-by-duck-typing.md` | 13.4 利用鸭子类型编程：序列协议、猴子补丁与快速失败 |
| `05-goose-typing-abcs.md` | 13.5 大鹅类型：用抽象基类（ABC）表示接口契约 |
| `06-virtual-subclasses-and-subclasshook.md` | 13.5.6–13.5.8 虚拟子类、`__subclasshook__` 与结构类型 |
| `07-static-protocols.md` | 13.6 静态协议：`typing.Protocol` 与静态鸭子类型 |
| `typesystems_duck_goose_protocol_demo.py` | 配套：鸭子类型 vs 大鹅类型（ABC）vs `Protocol` 对比演示 |
| `dynamic_static_protocols_demo.py` | 配套：`Vowels` 动态协议 + `Protocol` 静态协议对比 |
| `duck_typing_practice_demo.py` | 配套：`FrenchDeck` + monkey patching + fail fast |
| `goose_typing_abcs_demo.py` | 配套：`MutableSequence` + `Tombola` ABC + 虚拟子类注册 |
| `virtual_subclass_and_subclasshook_demo.py` | 配套：`register()` 虚拟子类 + `Sized.__subclasshook__` 结构识别 |
| `static_protocols_demo.py` | 配套：`Protocol` / `runtime_checkable` / 窄协议示例 |

---

## 运行

```bash
python part-3-classes-and-protocols/chapter-13/typesystems_duck_goose_protocol_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/dynamic_static_protocols_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/duck_typing_practice_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/goose_typing_abcs_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/virtual_subclass_and_subclasshook_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/static_protocols_demo.py
```

