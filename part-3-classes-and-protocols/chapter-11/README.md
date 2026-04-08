# 第 11 章「符合 Python 风格的对象」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 11 章：**符合 Python 风格的对象（A Pythonic Object）**。

这一章会用 `Vector2d` 作为贯穿案例，系统演示如何通过 **特殊方法（dunder methods）** 让自定义对象在行为上“像内置类型一样自然”：

- 让 `repr()` / `str()` / `bytes()` / `format()` 等内置机制能理解你的对象
- 让对象可迭代、可哈希、可比较（在合理的语义下）
- 在需要时用 `__slots__` 做内存优化（并理解它的限制）

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-special-methods-cheatsheet.md` | 常用特殊方法速查表（按“协议/能力”归类），并给出 `Vector2d` 开发清单 |
| `02-repr-str-bytes-format-vector2d.md` | `repr` vs `str`，以及 `bytes()`/`format()`：用最小 `Vector2d` 一次做对四个协议 |
| `vector2d_repr_demo.py` | 配套：`Vector2d` 的 `__repr__`/`__str__`/`__bytes__`/`__format__` 可运行示例 |

---

## 运行

在仓库根目录执行：

```bash
python part-3-classes-and-protocols/chapter-11/vector2d_repr_demo.py
```

