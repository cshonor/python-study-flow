# 第 14 章「继承：瑕瑜互见」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 14 章：**继承：瑕瑜互见**。

本章的主题不是“如何用继承复用代码”，而是更接近工程实践的视角：

- 继承的真实语义是什么
- 为什么继承常常带来紧耦合与维护风险
- Python 的多重继承与 `super()` 如何配合（MRO）
- 什么时候应该用组合/委托，什么时候才考虑继承（尤其是 Mixin）

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-inheritance-intro.md` | 14.1 开篇导读：继承的本质、坑点与本章学习路线 |
| `02-super.md` | 14.2 `super()`：单继承的正确扩展方式 + 多重继承的协作式调用 |
| `super_last_updated_ordereddict_demo.py` | 配套：`LastUpdatedOrderedDict`（正确 `super()` vs 硬编码父类名） |
| `super_mro_diamond_demo.py` | 配套：菱形继承 + MRO 下 `super()` 的真实调用顺序 |
| `03-subclassing-builtin-types.md` | 14.3 子类化内置类型的坑：`dict`/`list`/`str` 与 `User*` 替代 |
| `builtin_subclass_pitfalls_demo.py` | 配套：`dict`/`list` 子类陷阱与 `UserDict`/`UserList` 修复 |
| `04-multiple-inheritance-and-mro.md` | 14.4 多重继承与 MRO：钻石问题、协作式 `super()`、调用链中断 |
| `mro_diamond_root_ab_leaf_demo.py` | 配套：`Root/A/B/Leaf` + `LeafUA`（MRO 与调用链输出） |
| `06-real-world-multiple-inheritance.md` | 14.6 实战收尾：标准库/框架里的 mixin 组合范式与反模式 |
| `real_world_mixins_demo.py` | 配套：`ThreadingMixIn` + 迷你 CBV mixin + Tkinter MRO（可选） |
| `07-multiple-inheritance-survival-guide.md` | 14.7 收官：继承与多重继承的避坑终极指南（10 条军规） |
| `inheritance-cheatsheet.md` | 可打印速查表：继承 / `super()` / MRO / Mixin |

---

## 运行

```bash
python part-3-classes-and-protocols/chapter-14/super_last_updated_ordereddict_demo.py
python part-3-classes-and-protocols/chapter-14/super_mro_diamond_demo.py
python part-3-classes-and-protocols/chapter-14/builtin_subclass_pitfalls_demo.py
python part-3-classes-and-protocols/chapter-14/mro_diamond_root_ab_leaf_demo.py
python part-3-classes-and-protocols/chapter-14/real_world_mixins_demo.py
```

