# 4.8 Unicode 文本排序：别用默认 `sorted()` 排多语言（locale vs UCA/pyuca）

这一节解决一个非常常见、也非常隐蔽的问题：

> **同一批字符串，在不同系统上排序结果不一致**，或者“看起来就是不符合人类语言习惯”。

根因是：Python 默认的字符串比较是按 **Unicode 码点（code point）**做“字典序”，这对英文还凑合，但对带变音符号/特殊字母/多语言文本会很别扭。

配套脚本：`unicode_sorting_demo.py`（默认排序 / `locale.strxfrm` / `pyuca` 三套对比，能跑哪个就展示哪个）。

---

## 一、核心问题：默认排序按码点，不按语言习惯

### 1.1 默认排序是“码点顺序”

```python
fruits = ["caju", "atemoia", "cajá", "açaí", "acerola"]
print(sorted(fruits))
```

你看到的结果，本质上是把字符串当作“码点序列”，从左到右逐个比大小。

问题在于：

- 语言排序（collation）通常会把 `á/ã/ç/ñ` 视为“与 a/c/n 相关、但带附加规则”的字母；
- 而码点顺序只是一串整数的比较，并不懂“葡萄牙语/西班牙语”的规则。

所以“默认排序”并不是错，它只是**不是你想要的那种排序**。

---

## 二、方案 1：`locale.strxfrm`（依赖系统区域设置）

### 2.1 它是怎么工作的？

`locale.strxfrm(s)` 会把字符串转换成一个“可比较的键”，这个键的比较规则来自 **当前进程的 locale**（通常由 `locale.setlocale` 设置）。

```python
import locale

# 注意：这一步会影响整个进程（全局状态）
locale.setlocale(locale.LC_COLLATE, "pt_BR.UTF-8")
sorted_fruits = sorted(fruits, key=locale.strxfrm)
```

### 2.2 三个致命问题（你写项目时必须知道）

1. **平台依赖**：同一个 locale 名字在 Windows/Linux/macOS 可能完全不可用（尤其 Windows）。  
2. **全局副作用**：`setlocale` 改的是**进程级全局状态**，多线程/第三方库下风险大。  
3. **不可移植**：你在自己机器上跑通，并不代表 CI/服务器/用户机器能跑通。

结论（务实版）：

- 你可以在“单机脚本/单语言/可控环境”里用它；
- 但不要把它当成“跨平台、多语言排序”的长期方案。

---

## 三、方案 2：`pyuca`（Unicode Collation Algorithm，跨平台一致）

### 3.1 为什么它更适合工程？

`pyuca` 实现了 Unicode 官方的 **UCA（Unicode Collation Algorithm）**，特点是：

- **纯 Python / 跨平台一致**：Windows/Linux/macOS 排序结果一致  
- **不改系统 locale**：没有全局副作用  
- **更接近“语言习惯排序”的标准化方案**（至少比码点顺序靠谱得多）

### 3.2 最小用法

安装：

```bash
pip install pyuca
```

使用：

```python
import pyuca

coll = pyuca.Collator()
sorted_fruits = sorted(fruits, key=coll.sort_key)
```

### 3.3 现实边界

`pyuca` 给的是“Unicode 标准排序”，但某些语言/行业会有更特殊的规则（例如电话簿顺序）。这种属于少数，需要更定制的 collation（另一个话题）。

---

## 四、三种方案对比（你应该怎么选）

| 方案 | 跨平台一致 | 是否依赖系统语言包 | 是否有全局副作用 | 适合 |
|---|---|---|---|---|
| 默认 `sorted()` | ✅（一致，但按码点） | ❌ | ❌ | 纯英文/不在乎语言习惯 |
| `locale.strxfrm` | ❌ | ✅ | ✅（`setlocale`） | 单机脚本、单语言、可控环境 |
| `pyuca.Collator` | ✅ | ❌ | ❌ | 多语言、Windows、生产环境优先 |

---

## 五、可运行对照

运行：

```bash
python part-1-data-structures/chapter-04/unicode_sorting_demo.py
```

脚本会：

- 先打印默认 `sorted()` 的结果（码点顺序）
- 再尝试 `locale.strxfrm`（如果系统 locale 不可用会说明原因）
- 如果你安装了 `pyuca`，会再打印 `pyuca` 的排序结果

