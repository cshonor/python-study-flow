# 第 12 章「序列的特殊方法」— 本目录说明

本目录对应《流畅的 Python》（第二版）第 12 章：**序列的特殊方法（Special Methods for Sequences）**。

本章的主线是把第 11 章的向量对象思路升级成一个更“标准库级”的 **不可变序列类型**：多维 `Vector`。

你会从最小的序列协议开始（`__len__` / `__getitem__`），逐步获得：

- `len(v)`、索引 `v[i]`、切片 `v[i:j:k]`
- 自然的迭代/拆包（由 `__getitem__` 带来的序列行为）
- 更完整的数值语义与格式化扩展（后续小节）
- `__getattr__` 做动态属性访问（如 `v.x` / `v.y` / `v.z`）

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|---|---|
| `01-12.1 开篇导读：从“向量对象”到“不可变序列”.md` | 12.1 开篇导读：从“向量对象”到“不可变序列” |
| `02-12.2 Vector：用户定义的序列类型（组合模式）与 __len__ __getitem__.md` | 12.2 实现 `__len__` 与 `__getitem__`：索引/切片与返回新 `Vector` |
| `03-12.3 Vector 第 1 版：与 Vector2d 行为兼容（从二维到 N 维）.md` | 12.3 `Vector` 第 1 版：与 `Vector2d` 行为兼容（从二维到 N 维） |
| `04-协议与鸭子类型：Python 的“非正式接口”.md` | 协议与鸭子类型：Python 的“非正式接口”（含 PEP 544 `Protocol`） |
| `05-12.3 Vector 第 2 版：实现序列协议与切片（slice → 同类型新实例）.md` | 12.3 `Vector` 第 2 版：实现序列协议与切片（slice → `Vector`） |
| `06-12.6 Vector 第 3 版：动态属性存取（__getattr__）与不可变性（__setattr__ __slots__）.md` | 12.6 `Vector` 第 3 版：动态属性（`__getattr__`）与不可变性（`__setattr__`/`__slots__`） |
| `07-12.7 Vector 第 4 版：哈希与快速等值测试（map-reduce）.md` | 12.7 `Vector` 第 4 版：可哈希（`__hash__`）与快速等值比较（`zip`/`all`） |
| `08-12.8 Vector 第 5 版：自定义格式化与超球面坐标（h 后缀）.md` | 12.8 `Vector` 第 5 版：自定义格式化（笛卡尔/超球面，`h` 后缀） |
| `02_vector_len_getitem_demo.py` | 配套：最小可运行 `Vector`（N 维、不可变、支持索引/切片） |
| `03_vector_v1_compat_demo.py` | 配套：`Vector` v1（repr 截断、bytes/frombytes、eq/abs/bool） |
| `04_protocols_duck_typing_demo.py` | 配套：`FrenchDeck` 序列协议 + `typing.Protocol` 静态协议演示 |
| `05_vector_v2_sequence_demo.py` | 配套：`Vector` v2（v1 + `__len__`/`__getitem__` + 切片返回同类型） |
| `06_vector_v3_dynamic_attrs_demo.py` | 配套：`Vector` v3（动态属性 `x/y/z/t` + 禁止赋值） |
| `07_vector_v4_hash_eq_demo.py` | 配套：`Vector` v4（可哈希 + 更快的等值比较） |
| `08_vector_v5_format_demo.py` | 配套：`Vector` v5（`__format__` + 超球面坐标 `h`） |

---

## 运行

在仓库根目录执行：

```bash
python part-3-classes-and-protocols/chapter-12/02_vector_len_getitem_demo.py
```

或运行 v1 兼容版示例：

```bash
python part-3-classes-and-protocols/chapter-12/03_vector_v1_compat_demo.py
```

协议与鸭子类型示例：

```bash
python part-3-classes-and-protocols/chapter-12/04_protocols_duck_typing_demo.py
```

`Vector` v2（序列协议 + 切片）示例：

```bash
python part-3-classes-and-protocols/chapter-12/05_vector_v2_sequence_demo.py
```

`Vector` v3（动态属性 + `__setattr__`/`__slots__`）示例：

```bash
python part-3-classes-and-protocols/chapter-12/06_vector_v3_dynamic_attrs_demo.py
```

`Vector` v4（可哈希 + 快速等值比较）示例：

```bash
python part-3-classes-and-protocols/chapter-12/07_vector_v4_hash_eq_demo.py
```

`Vector` v5（自定义格式化 + `h` 超球面坐标）示例：

```bash
python part-3-classes-and-protocols/chapter-12/08_vector_v5_format_demo.py
```

