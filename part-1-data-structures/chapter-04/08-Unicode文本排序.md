# 4.8 Unicode 文本排序：别用默认 `sorted()` 排多语言（locale vs UCA/pyuca）

这一节解决一个非常常见、也非常隐蔽的问题：

> **同一批字符串，在不同系统上排序结果不一致**，或者“看起来就是不符合人类语言习惯”。

根因是：Python 默认的字符串比较是按 **Unicode 码点（code point）**做“字典序”，这对英文还凑合，但对带变音符号/特殊字母/多语言文本会很别扭。

配套脚本：`08_unicode_sorting_demo.py`（默认排序 / `locale.strxfrm` / `pyuca` 三套对比，能跑哪个就展示哪个）。

---

## 零、新手清爽版（只记这些）

### 本节解决什么问题？

**用 Python 默认 `sorted()` 排中文、法文、西文、带重音的词 → 顺序往往「怪」，不像人脑里的词典顺序。**

原因：**默认比较 = 按 Unicode 码点从小到大比**，不是按某种「语言排序规则（collation）」。

### 默认 `sorted()` 为什么「不行」？

它不是算错，只是**目标不同**。例如 **`açaí`、`cajá`、`caju`**：机器逐码点比，**不会**自动按葡萄牙语里「重音字母跟基础字母一家」的习惯排。详见 **§一** 示例。

### 方案 1：`locale` + `strxfrm`（跟系统走）

**原理**：`locale.setlocale(LC_COLLATE, ...)` 后，`locale.strxfrm(s)` 生成**可按语言规则比较的键**。

```python
import locale

locale.setlocale(locale.LC_COLLATE, "pt_BR.UTF-8")  # 名字随系统而变
sorted(data, key=locale.strxfrm)
```

**硬伤（正式项目要警惕）**：

1. **跨平台**：同一 locale 名在 Windows / Linux / macOS **常对不上**，CI/服务器易挂。  
2. **全局**：`setlocale` 影响**整个进程**，多线程/库混用风险大。  
3. **运维**：容器里缺语言包时直接不可用。

**结论**：单机脚本、单语言、环境可控时可以玩；**不要**当跨平台多语言产品的唯一依赖。细节见 **§二**。

### 方案 2：`pyuca`（UCA，工程上常作首选）

**是什么**：实现 Unicode 标准里的 **UCA（Unicode Collation Algorithm）**，**不绑系统 locale**，**同版本数据下**各平台结果可对齐（比「纯码点序」更接近通用语言习惯）。

```bash
python -m pip install pyuca
```

```python
chinese = ["张三", "李四", "王五", "赵六"]

# Python 默认排序（按字符编码，非拼音）
print(sorted(chinese))  
# 输出：['张三', '李四', '王五', '赵六']（巧合正确，复杂列表常乱）

# pyuca 排序（严格拼音）
coll = pyuca.Collator()
print(sorted(chinese, key=coll.sort_key))  
# 输出：['李四', '王五', '张三', '赵六']（标准拼音）
```

（与 **`from pyuca import Collator; Collator()`** 等价，与 **`08_unicode_sorting_demo.py`** 一致。）

**仍非魔法**：极个别地区/行业有**电话簿序**等定制规则，UCA 也覆盖不全——那是再下一层定制。见 **§三·3.3**。

### 三种方案怎么选？

| 场景 | 用 |
| :--- | :--- |
| 纯英文或**不在乎**语言序 | 默认 **`sorted()`** |
| 本地一次性脚本、单语言、环境你说了算 | **`locale.strxfrm`**（**§二**） |
| **多语言、要可重复、跨平台、生产** | **`pyuca.Collator`**（**§三**） |

### 三句口诀

1. **默认排序按码点，不是按「语言习惯」**。  
2. **`locale` 排序吃系统、吃全局，别当唯一方案**。  
3. **多语言稳定排序 → 优先 `pyuca`（UCA）**。

下文 **§一～§四** 为展开、对比表与脚本说明。

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

# 只修改“排序规则”这一类别的本地化为 巴西葡萄牙语
locale.setlocale(locale.LC_COLLATE, "pt_BR.UTF-8")

# 假设已有列表
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']

# 按当前 locale 的语言习惯排序
sorted_fruits = sorted(fruits, key=locale.strxfrm)
```
- locale.LC_COLLATE：只管字符串排序规则，不影响日期 / 数字 / 货币。

- pt_BR.UTF-8：巴西葡萄牙语（带重音的字母按葡语习惯排）。

- locale.strxfrm(s)：把字符串 s 转换成符合当前 locale 规则的排序键，用于 sorted 的 key=。
- 
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
python part-1-data-structures/chapter-04/08_unicode_sorting_demo.py
```

与 **§零** 三方案对照；输出用 **`ascii()`** 包一层，避免 Windows 控制台编码影响阅读。

脚本会：

- 先打印默认 `sorted()` 的结果（码点顺序）
- 再尝试 `locale.strxfrm`（如果系统 locale 不可用会说明原因）
- 如果你安装了 `pyuca`，会再打印 `pyuca` 的排序结果

