# 4.9 Unicode 数据库：`unicodedata`（按名识别字符 + 按字符解析数值）

这一节的目标是把 `unicodedata` 的两类能力用到“能直接干活”的程度：

1. **识别字符**：这个字符到底是什么？（名字、类别、组合标记、是否控制符/空白符等）
2. **解析数值语义**：这个“看起来像数字”的字符到底代表多少？（圈码数字、罗马数字、分数等）

配套脚本：

- `09_unicode_char_finder.py`：按关键字搜索 Unicode 字符名（类似书里的 `cf.py`）
- `09_unicode_numeric_demo.py`：演示 `digit`/`numeric`/`isdecimal`/`isdigit`/`isnumeric` 的差异与用法

---

## 零、新手清爽版（只记这些）

### 本节在讲什么？

**`unicodedata` 是标准库里的「字符身份证查询口」**：官方全名、类别、组合性、**数字/分数/罗马数字的数值语义**等，都能按规则查出来。

典型困惑它帮你落地：

- **`µ`** 是微符号还是希腊 **`μ`**？（配合 **`name()`**、码点、**`NFKC`** 对照 **`07`**）  
- **`½`** 怎么变成 **`0.5`**？（**`numeric()`**）  
- 某个生僻符号到底叫什么？（**`name()`** + **`09_unicode_char_finder.py`**）

### 功能 1：查官方名字 — `unicodedata.name(ch)`

```python
import unicodedata

unicodedata.name("A")   # LATIN CAPITAL LETTER A
unicodedata.name("♛")   # BLACK CHESS QUEEN
```

**没有名字的字符**（不少控制符如 **`"\n"`**）会 **`ValueError`**，不是返回 `None`：

```python
try:
    name = unicodedata.name(ch)
except ValueError:
    name = None
```

详见 **§二·2.1**。

### 功能 2：按名字关键词搜字符 — `09_unicode_char_finder.py`

在仓库根目录：

```bash
python part-1-data-structures/chapter-04/09_unicode_char_finder.py CAT EYES

```

输出示例：`U+1F638 … GRINNING CAT FACE WITH SMILING EYES`（与 **§二·2.2** 一致）。

### 功能 3：判断「像数字的字符」— **`str` 上三个方法**

**`isdecimal()`** ⊂ **`isdigit()`** ⊂ **`isnumeric()`**（真子集关系，单字符上记忆即可）。

| 方法 | 严格度 | 直觉 |
| :--- | :--- | :--- |
| **`isdecimal()`** | 最严 | 主要是「十进制数字」形态（如 **`0`–`9`** 及同类 Nd） |
| **`isdigit()`** | 居中 |包含数字字形（0-9 + ① ② ³ 这类） |
| **`isnumeric()`** | 最宽 | 所有有数值语义的字符（0-9、①、½、Ⅳ、一、贰 等）|

它们是 **`str`** 的方法，不是 **`unicodedata`** 模块下的三个函数——别记混。完整例子见 **`09_unicode_numeric_demo.py`**、**§三**。

```python
# 测试字符
c1 = "5"    # 普通数字
c2 = "⑤"   # 圈码数字
c3 = "½"    # 分数
c4 = "一"   # 中文数字

print("普通数字 5：")
print(" isdecimal:", c1.isdecimal())  # True
print(" isdigit:  ", c1.isdigit())    # True
print(" isnumeric:", c1.isnumeric())  # True

print("\n圈码 ⑤：")
print(" isdecimal:", c2.isdecimal())  # False
print(" isdigit:  ", c2.isdigit())    # True
print(" isnumeric:", c2.isnumeric())  # True

print("\n分数 ½：")
print(" isdecimal:", c3.isdecimal())  # False
print(" isdigit:  ", c3.isdigit())    # False
print(" isnumeric:", c3.isnumeric())  # True

print("\n中文 一：")
print(" isdecimal:", c4.isdecimal())  # False
print(" isdigit:  ", c4.isdigit())    # False
print(" isnumeric:", c4.isnumeric())  # True
```

### 功能 4：转成真正的数 — `digit()` vs `numeric()`

- **`unicodedata.digit(ch)`**：偏「整数数字字符」→ **`int`**；否则 **`ValueError`**。  
- **`unicodedata.numeric(ch)`**：更宽，**`½` → 0.5**、**`Ⅳ` → 4.0**、**`③` → 3.0** 等 → **`float`**。

```python
import unicodedata

print(unicodedata.digit("5"))   # 5（int）
print(unicodedata.digit("③"))  # 3（int）
print(unicodedata.digit("²"))   # 2（int）
# print(unicodedata.digit("½")) # 报错：ValueError
```
解析流水线：**先试 `digit`，再 `numeric`**，失败再按业务报错或跳过（**§三·3.3**）。

### 常用落地

- **数据清洗**：控制符、不可见字符、奇怪符号（**`name` / `category` / `combining`** 等，**§四**）  
- **用户输入标准化**：圈码、罗马、分数 → 数值  
- **小工具**：按名搜 emoji / 数学符号（**`09_unicode_char_finder.py`**）

### 四句口诀

1. **`unicodedata`：查字符身份与数值语义的官方入口**  
2. **`name()`：有则返回全名，无则抛错，要 `try`**  
3. **数字判断：`isdecimal` < `isdigit` < `isnumeric`（在 `str` 上）**  
4. **转数值：`digit` 偏整，`numeric` 更宽（含分数）**

下文 **§一～§四** 为展开与误区；**§五** 为脚本命令。

---

## 一、为什么需要 `unicodedata`？

Unicode 字符非常多（十几万），很多字符你肉眼看不出“它到底是什么”，例如：

- `µ` 是“微符号”还是希腊字母 `μ`？
- `Ω` 是“欧姆符号”还是 `Ω`？
- `½` 这种分数怎么变成数值 0.5？

`unicodedata` 提供了 Python 内置的 Unicode 数据库接口，能把这些问题变成**可查询、可写规则、可自动化**的处理流程。

---

## 二、4.9.1 按名称查找字符：`unicodedata.name()` 与“字符搜索工具”

### 2.1 `name(ch)`：回答“这是什么字符？”

```python
import unicodedata

print(unicodedata.name("A"))   # LATIN CAPITAL LETTER A
print(unicodedata.name("♛"))   # BLACK CHESS QUEEN
```

注意点：

- 对某些字符（例如控制字符 `\n`）没有名字：`unicodedata.name("\n")` 会抛 `ValueError`
- 所以你通常要写成：

```python
try:
    nm = unicodedata.name(ch)
except ValueError:
    nm = None
```

### 2.2 书里的 `cf.py` 思路：按关键字在“名字库”里找字符

核心想法非常朴素：

1. 遍历所有码点 `0x0000..0x10FFFF`
2. 对每个码点 `chr(cp)`，尝试取 `unicodedata.name(...)`
3. 把名字拆成单词（用空格分隔）
4. 用查询词做“子集匹配”（例如同时包含 `CAT` 和 `EYES`）

在仓库里我把它实现成 `09_unicode_char_finder.py`，你可以这样用：

```bash
python part-1-data-structures/chapter-04/09_unicode_char_finder.py CAT EYES
python part-1-data-structures/chapter-04/09_unicode_char_finder.py BLACK QUEEN
```

它会输出形如：

```text
U+1F638 😸 GRINNING CAT FACE WITH SMILING EYES
```

### 2.3 代理区（surrogate）必须跳过

Unicode 的 `U+D800..U+DFFF` 是 UTF-16 代理项范围，不是独立字符。  
遍历码点时应该跳过它们，否则你会得到一堆不该出现的“伪字符”。

---

## 三、4.9.2 字符的数值意义：`digit()` / `numeric()` / `decimal`

### 3.1 为什么 `int(ch)` 不够？

很多“数字”不是 ASCII `'0'..'9'`：

- `½`、`⅓`（分数）
- `①②③`（圈码数字）
- `ⅣⅫ`（罗马数字）
- 某些上标/下标数字

这些字符多数不能直接 `int()`，但它们有明确“数值语义”。

### 3.2 你需要掌握的 3 组 API

#### 3.2.1 三个 `str` 判断方法：`isdecimal/isdigit/isnumeric`

它们的“宽松程度”大致是：

`isdecimal()` ⊂ `isdigit()` ⊂ `isnumeric()`

- `isdecimal()`：最严格，主要是“十进制数字”（Unicode 类别 `Nd`）
- `isdigit()`：更宽，包含一些“数字字符”（如圈码）
- `isnumeric()`：最宽，包含分数、罗马数字等

#### 3.2.2 两个数值解析函数：`unicodedata.digit` vs `unicodedata.numeric`

- `unicodedata.digit(ch)`：适合“能当整数”的数字字符，返回 `int`；否则 `ValueError`
- `unicodedata.numeric(ch)`：更通用，分数/罗马数字也行，返回 `float`；否则 `ValueError`

### 3.3 实战规则：怎么写一个“尽量把数字字符变成数值”的解析逻辑？

常见写法是：

1. 先用 `digit`（更像“整数”）
2. 再 fallback 到 `numeric`（更通用）
3. 解析失败就跳过/报错/记录（看业务）

你可以直接参考 `09_unicode_numeric_demo.py` 里的实现与输出对比。

---

## 四、常见误区与落地场景

### 4.1 误区 1：`name()` 不会返回 `None`

`unicodedata.name(ch)` 对没有名字的字符会 **抛 `ValueError`**，不是返回 `None`。  
所以你要 `try/except`。

### 4.2 误区 2：`latin-1/cp1252` 能解码任意 bytes，所以“不会错”

这恰恰是隐蔽坑：它们“不会报错”不代表“解码正确”。  
这部分已经在 `05/06` 里通过对照表和 demo 展示过了。

### 4.3 典型场景

- **数据清洗**：识别/过滤不可见字符、控制符、奇怪符号（用 `name`/`category`/`combining` 等）
- **用户输入**：把圈码数字、罗马数字、分数字符统一成数值
- **写工具脚本**：类似 `09_unicode_char_finder.py` 的“按名查字符”工具，快速定位 emoji/符号

---

## 五、可运行对照

与 **§零** 口诀对照：先跑 **`09_unicode_numeric_demo.py`** 看 **`isdecimal`/`isdigit`/`isnumeric`** 与 **`digit`/`numeric`** 并排输出。

运行字符搜索工具：

```bash
python part-1-data-structures/chapter-04/09_unicode_char_finder.py CAT EYES
```

运行数值解析 demo：

```bash
python part-1-data-structures/chapter-04/09_unicode_numeric_demo.py
```

