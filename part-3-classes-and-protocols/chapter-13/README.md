# 第 13 章「接口、协议和抽象基类」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 13 章：**接口、协议和抽象基类**。

本章开篇核心观点是 GoF 的那句原则：

> **对接口编程，而不是对实现编程。**

在 Python 语境下，“接口”常常不是 `interface` 关键字，而是以 **协议（protocol）/抽象基类（ABC）/类型提示** 等形式出现。

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-第 13 章核心解读：接口、协议和抽象基类.md` | 第 13 章开篇：四种“类型系统”视角与适用场景 |
| `02-13.2 类型图与 4 种类型系统：用“检查时机 × 类型依据”看清全局.md` | 13.2 类型图：检查时机 × 类型依据（四象限理解） |
| `03-13.3 两种“协议”：动态协议 vs 静态协议（typing.Protocol）.md` | 13.3 两种协议：动态协议 vs 静态协议（`Protocol`） |
| `04-13.4 利用鸭子类型编程：序列协议、猴子补丁与快速失败.md` | 13.4 利用鸭子类型编程：序列协议、猴子补丁与快速失败 |
| `05-13.5 大鹅类型（Goose Typing）：抽象基类（ABC）表示接口.md` | 13.5 大鹅类型：用抽象基类（ABC）表示接口契约 |
| `06-13.5.6–13.5.8 虚拟子类、__subclasshook__ 与结构类型（runtime structural typing）.md` | 13.5.6–13.5.8 虚拟子类、`__subclasshook__` 与结构类型 |
| `07-13.6 静态协议（Static Protocol）：typing.Protocol 与静态鸭子类型.md` | 13.6 静态协议：`typing.Protocol` 与静态鸭子类型 |
| `01_typesystems_duck_goose_protocol_demo.py` | 配套：鸭子类型 vs 大鹅类型（ABC）vs `Protocol` 对比演示 |
| `03_dynamic_07_static_protocols_demo.py` | 配套：`Vowels` 动态协议 + `Protocol` 静态协议对比 |
| `04_duck_typing_practice_demo.py` | 配套：`FrenchDeck` + monkey patching + fail fast |
| `05_goose_typing_abcs_demo.py` | 配套：`MutableSequence` + `Tombola` ABC + 虚拟子类注册 |
| `06_virtual_subclass_and_subclasshook_demo.py` | 配套：`register()` 虚拟子类 + `Sized.__subclasshook__` 结构识别 |
| `07_static_protocols_demo.py` | 配套：`Protocol` / `runtime_checkable` / 窄协议示例 |

---

## 运行

```bash
python part-3-classes-and-protocols/chapter-13/01_typesystems_duck_goose_protocol_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/03_dynamic_07_static_protocols_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/04_duck_typing_practice_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/05_goose_typing_abcs_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/06_virtual_subclass_and_subclasshook_demo.py
```

```bash
python part-3-classes-and-protocols/chapter-13/07_static_protocols_demo.py
```

