# 第 6 章「对象引用、可变性和垃圾回收」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 6 章：**对象引用、可变性和垃圾回收**。

建议先读：[`01-第6章对象引用可变性与GC总览.md`](01-第6章对象引用可变性与GC总览.md)。

这一章偏“底层直觉”，但它直接决定你能不能解释清楚并避开这些高频坑：

- “为什么我改了一个列表，另一个变量也变了？”
- “`is` 和 `==` 到底差在哪？”
- “`del` 是不是把对象删掉了？”
- “默认参数为什么会污染后续调用？”
- “浅拷贝/深拷贝到底拷贝了什么？”
- “为什么有时候对象‘应该被回收’却还活着？”

---

## 文件一览（建议顺序）

| 顺序 | 文件 | 说明 |
|---|---|---|
| 01 | `01-第6章对象引用可变性与GC总览.md` | 第 6 章开篇导读：变量/对象/引用、可变性、拷贝、参数传递、GC、弱引用（配大量可运行例子） |
| 02 | `02-变量不是盒子.md` | 6.2 深入：变量是标签不是盒子；赋值先右后左；别名与术语纠正（含 Gizmo 证据） |
| 03 | `03-同一性相等与别名.md` | 6.3 深入：同一性 vs 相等性（`is`/`==`）、别名风险、`None` 判断、元组相对不可变与 hash |
| 04 | `04-浅拷贝为默认.md` | 6.4：文首**大白话速通**（外壳/内层共享 + 口诀）+ **浅拷贝方式速查** + 嵌套陷阱；`copy` vs `deepcopy` |
| 05 | `05-共享传参与可变默认参数.md` | 6.5：文首**大白话速通**（共享传参 + 两后果 + 可变默认 + 速查表）+ **§零** 背诵 + `+=`、HauntedBus/TwilightBus、`__defaults__` |
| 06 | `06-del与垃圾回收.md` | 6.6 深入：`del` 的解绑语义、引用计数与循环 GC、弱引用与 `weakref.finalize`、排查入口 |
| 07 | `07-不可变类型技巧.md` | 6.7 深入：不可变对象复用/驻留（tuple/frozenset/str/int）、`sys.intern`、`is` 的边界 |

### 脚本（与上表编号一一对应）

| 编号 | 脚本 | 说明 |
|---|---|---|
| — | `ch06_demo_support.py` | 公用：`section()` / `safe()`，被下列脚本导入 |
| 01 | `01_object_refs_gc_overview_demo.py` | 导航：列出 01–07 各脚本及运行命令 |
| 02 | `02_variable_not_a_box_demo.py` | 与 `02` 笔记配套 |
| 03 | `03_identity_equality_aliasing_demo.py` | 与 `03` 笔记配套 |
| 04 | `04_shallow_copy_and_deepcopy_demo.py` | 与 `04` 笔记配套 |
| 05 | `05_call_by_sharing_mutable_defaults_demo.py` | 与 `05` 笔记配套 |
| 06 | `06_del_and_garbage_collection_demo.py` | 与 `06` 笔记配套 |
| 07 | `07_immutable_type_tricks_demo.py` | 与 `07` 笔记配套 |

---

## 运行

在仓库根目录执行（任选一篇对应的脚本）：

```bash
python part-1-data-structures/chapter-06/01_object_refs_gc_overview_demo.py
python part-1-data-structures/chapter-06/02_variable_not_a_box_demo.py
python part-1-data-structures/chapter-06/03_identity_equality_aliasing_demo.py
python part-1-data-structures/chapter-06/04_shallow_copy_and_deepcopy_demo.py
python part-1-data-structures/chapter-06/05_call_by_sharing_mutable_defaults_demo.py
python part-1-data-structures/chapter-06/06_del_and_garbage_collection_demo.py
python part-1-data-structures/chapter-06/07_immutable_type_tricks_demo.py
```
