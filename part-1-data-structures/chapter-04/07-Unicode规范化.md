# 4.7 Unicode 字符串规范化：看起来一样，但比较却不相等（NFC/NFD/NFKC/NFKD + casefold）

这节解决一个非常“反直觉”的坑：**视觉上完全一样的字符串，在 Python 里可能不相等**。

根因不是 Python “不智能”，而是 Unicode 的设计允许同一个视觉字符用不同的码点序列表示（组合字符/兼容字符）。

你要掌握的结论就 3 条：

1. **比较前先规范化**（通常用 NFC）
2. **大小写不敏感比较用 `casefold()`**（不要只用 `lower()`）
3. **NFKC/NFKD 只能用于搜索/索引，不要用于持久化存储**（可能改变语义/丢失格式）

配套脚本：`07_unicode_normalization_demo.py`。

---

## 一、核心坑：组合字符导致“看起来一样，但不相等”

Unicode 支持 **组合字符（combining characters）**。例如“é”可以表示为：

- **预合成**：`U+00E9`（单个码点）
- **分解形式**：`e`（`U+0065`） + 组合重音 `U+0301`

```python
s1 = "café"       # 预合成 é
s2 = "cafe\u0301" # e + 组合重音
assert s1 != s2  # 成立 → 码点序列不同，值不相等
```

这不是“编码问题”，而是**同一个字符的不同码点序列**。所以：

- `len(s1)` 和 `len(s2)` 也可能不同
- 直接 `==` 比较会失败

---

## 二、解决：`unicodedata.normalize()` 的 4 种形式

Python 用 `unicodedata.normalize(form, s)` 做规范化。

### 2.1 四种形式一张表

| 形式 | 全称 | 核心动作 | 常见用途 |
|---|---|---|---|
| **NFC** | Normalization Form C | **分解再合成**（尽量用预合成字符） | **通用默认**：存储、展示、比较（W3C 常推荐） |
| **NFD** | Normalization Form D | **分解**（拆成“基础字母 + 组合符号”） | 需要单独处理变音符号/重音符号时 |
| **NFKC** | Compatibility Composition | **兼容性分解** + 合成 | 搜索、索引、输入对齐（可能改变语义） |
| **NFKD** | Compatibility Decomposition | **兼容性分解**（不合成） | 搜索、索引、格式转换（更可能“变形”） |

你可以把它们的关系记成一句话：

- **NFC/NFD**：只做“规范等价”的统一（尽量不改变语义）
- **NFKC/NFKD**：会把“兼容字符”也折叠到更基础的表示（更激进）

### 2.2 用 NFC/NFD 把 `café` 对齐

```python
from unicodedata import normalize

s1 = "café"
s2 = "cafe\u0301"

assert normalize("NFC", s1) == normalize("NFC", s2)  # 成立 → NFC 后两者规范等价
assert normalize("NFD", s1) == normalize("NFD", s2)  # 成立 → NFD 后两者规范等价
```

并且你能观察到长度变化：

- NFC 往往更短（更偏预合成）
- NFD 往往更长（拆成多个码点）

### 2.3 兼容性规范化：NFKC/NFKD 的“风险”与用途

Unicode 为了兼容历史，会存在“兼容字符”。例如：

- `OHM SIGN`：`U+2126`（看起来像 Ω）
- 希腊字母大写 Omega：`U+03A9`

以及：

- `½`（`VULGAR FRACTION ONE HALF`）和 `"1/2"`
- `µ`（`MICRO SIGN`）和希腊字母 `μ`

NFKC/NFKD 会把这类兼容字符折叠成更基础的表示，这在 **搜索/索引/输入匹配** 很有用，但在 **存储** 上可能是灾难：

- `½` 可能被展开成多个字符（外观/语义可能变化）
- 上标 `²` 之类在 NFKC 下可能丢掉“上标格式”

所以请把规则记死：

> **NFKC/NFKD：只用于临时对齐（搜索/匹配），不要把结果当“原始数据”保存。**

---

## 三、大小写同一化：`str.casefold()`（比 `lower()` 更彻底）

多语言场景里，“大小写不敏感比较”不要只靠 `lower()`，因为 Unicode 里有很多特殊规则：

- 德语 `ß`（sharp s）在 casefold 后会变成 `ss`
- `µ`（micro sign）在 casefold 后会对齐成希腊字母 `μ`

```python
assert "Straße".casefold() == "strasse".casefold()  # 成立 → casefold 把 ß 对齐为 ss
```

经验法则：

- **要做不区分大小写的比较**：用 `casefold()`  
- `lower()` 更像“英文语境下的小写化”，在 Unicode 上不够彻底

---

## 四、可复用工具函数：规范化比较（nfc_equal / fold_equal）

这是你可以直接复制到项目里的版本。

```python
from unicodedata import normalize

def nfc_equal(a: str, b: str) -> bool:
    \"\"\"区分大小写的等价比较：NFC 规范化后比较。\"\"\"
    return normalize("NFC", a) == normalize("NFC", b)

def fold_equal(a: str, b: str) -> bool:
    \"\"\"大小写不敏感的等价比较：NFC + casefold。\"\"\"
    return normalize("NFC", a).casefold() == normalize("NFC", b).casefold()
```

什么时候用哪个？

- 只是想解决“组合字符导致的不相等” → `nfc_equal`
- 还要“忽略大小写” → `fold_equal`

---

## 五、极端规范化：去掉变音符号（只用于搜索，不用于业务语义）

有些场景你想把 `café` 当作 `cafe` 来匹配（搜索、URL 友好、索引）。这会改变语义，所以一定要当作“搜索键”而不是“真实数据”。

思路：

1. 用 NFD 分解出组合字符
2. 过滤掉所有组合标记（Mn）
3. 再 NFC 合成回去

```python
import unicodedata

def shave_marks(txt: str) -> str:
    \"\"\"去掉组合重音等标记（只适合搜索/索引）。\"\"\"
    norm = unicodedata.normalize("NFD", txt)
    shaved = "".join(c for c in norm if not unicodedata.combining(c))
    return unicodedata.normalize("NFC", shaved)
```

---

## 六、实战最佳实践（直接落地）

### 6.1 存储 / 传输 / 精确比较

- **默认用 NFC 统一**（特别是你要做去重、字典 key、数据库唯一约束时）
- 比较时做：`normalize("NFC", s)`

### 6.2 大小写不敏感比较

- 做：`normalize("NFC", s).casefold()`

### 6.3 搜索 / 索引（更宽松）

- 可以用：`normalize("NFKC", s).casefold()`
- 或者在需要时额外 `shave_marks`（但要明确会改变语义）

---

## 七、可运行对照

运行：

```bash
python part-1-data-structures/chapter-04/07_unicode_normalization_demo.py
```

脚本会打印：

- `café` 两种表示的码点序列与长度差异
- NFC/NFD 后的对齐结果
- NFKC 折叠兼容字符（`Ω`/`µ`/`½`）的效果
- `casefold()` 对 `ß` 的效果
- `nfc_equal` / `fold_equal` / `shave_marks` 的实战对比

