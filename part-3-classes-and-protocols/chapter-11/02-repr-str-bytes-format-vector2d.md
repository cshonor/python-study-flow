# 11.x `repr()` vs `str()`：用 `Vector2d` 一次做对 `__repr__`/`__str__`/`__bytes__`/`__format__`

这节解决一个非常常见、但很容易“实现了还能踩坑”的主题：对象的表示（representation）。

在 Python 里，`repr(obj)` 与 `str(obj)` 不是“两个名字而已”，它们对应两套不同的意图：

- **`repr` 面向开发者**：尽量无歧义，利于调试；理想情况下能帮助你重建对象。
- **`str` 面向用户**：更友好、更可读，适合展示。

此外还有两个常见接口：

- `bytes(obj)` → `__bytes__`
- `format(obj, spec)` / f-string → `__format__`

配套脚本：`vector2d_repr_demo.py`。

---

## 一、`__repr__` vs `__str__`：最低要求与兜底行为

| 特殊方法 | 被谁调用 | 推荐风格 |
|---|---|---|
| `__repr__` | `repr(obj)`、交互式回显 | 信息更全、尽量无歧义（常用 `ClassName(x, y)` 或 `ClassName(x=..., y=...)`） |
| `__str__` | `str(obj)`、`print(obj)` | 面向用户，可更简洁 |

如果你不实现 `__str__`，Python 会回退使用 `__repr__`。

---

## 二、Python 3 的返回类型规则（很重要）

在 **Python 3** 中：

- `__repr__` / `__str__` / `__format__` **必须返回 `str`**
- 只有 `__bytes__` 应该返回 `bytes`

否则会触发 `TypeError`（这也是 Python 2 与 Python 3 的关键差异之一）。

---

## 三、`Vector2d` 的一个最小但完整实现

下面这份实现满足：

- `repr(v)`：开发者友好
- `str(v)`：用户友好
- `bytes(v)`：固定二进制格式（“类型码 + 两个浮点”）
- `format(v, spec)`：支持两种模式
  - 默认：`(x, y)`（直角坐标）
  - 以 `'p'` 结尾：`<r, theta>`（极坐标），`spec` 作用到数字本身（如 `.2f`）

细节见配套 `vector2d_repr_demo.py`。

