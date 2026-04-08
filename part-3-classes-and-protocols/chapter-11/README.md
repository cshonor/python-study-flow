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
| `03-alternative-constructor-frombytes.md` | 11.4 备选构造函数：`frombytes` 反序列化（让 `bytes(v)` 可逆） |
| `vector2d_frombytes_demo.py` | 配套：断言 `v == Vector2d.frombytes(bytes(v))`（从 `vector2d_repr_demo.py` 动态加载类） |
| `04-classmethod-vs-staticmethod.md` | 11.5 `classmethod` vs `staticmethod`：调用行为、继承差异与实践建议 |
| `classmethod_staticmethod_demo.py` | 配套：复现 `Demo` 输出；展示 `from_polar`（classmethod）与静态方法误用对比 |
| `05-formatting-display-vector2d.md` | 11.6 格式化显示：`__format__` 与格式规范微语言；`p` 极坐标扩展 |
| `vector2d_format_demo.py` | 配套：`format()` / f-string 对 `Vector2d` 的直角/极坐标格式化输出 |
| `06-hashable-vector2d.md` | 11.7 可哈希的 `Vector2d`：不可变性、`__eq__`/`__hash__` 一致性、set/dict 用法 |
| `vector2d_hash_demo.py` | 配套：验证 `Vector2d` 可哈希并禁止修改坐标（避免哈希漂移） |
| `07-positional-pattern-matching.md` | 11.8 位置模式匹配：`__match_args__` 让 `case Vector2d(x, y)` 可用 |
| `vector2d_match_demo.py` | 配套：关键字模式 vs 位置模式的 `match-case` 示例 |
| `vector2d_v3.py` | 11.9 第 3 版 `Vector2d`（整合版）：包含 doctest，可一键验证全功能 |
| `08-slots-memory-optimization.md` | 11.11 `__slots__` 节省空间：原理、继承规则、weakref 与 cached_property 取舍 |
| `slots_inheritance_demo.py` | 配套：`__dict__`/动态属性/继承/weakref 行为演示 |
| `slots_memory_demo.py` | 配套：用 `tracemalloc` 对比 slots vs 普通类的分配量（小规模） |

---

## 运行

在仓库根目录执行：

```bash
python part-3-classes-and-protocols/chapter-11/vector2d_repr_demo.py
python part-3-classes-and-protocols/chapter-11/vector2d_frombytes_demo.py
python part-3-classes-and-protocols/chapter-11/classmethod_staticmethod_demo.py
python part-3-classes-and-protocols/chapter-11/vector2d_format_demo.py
python part-3-classes-and-protocols/chapter-11/vector2d_hash_demo.py
python part-3-classes-and-protocols/chapter-11/vector2d_match_demo.py
python -m doctest part-3-classes-and-protocols/chapter-11/vector2d_v3.py
python part-3-classes-and-protocols/chapter-11/slots_inheritance_demo.py
python part-3-classes-and-protocols/chapter-11/slots_memory_demo.py
```

