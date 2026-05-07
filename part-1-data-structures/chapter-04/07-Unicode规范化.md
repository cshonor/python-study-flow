# 4.7 Unicode 字符串规范化：看起来一样，但比较却不相等（NFC/NFD/NFKC/NFKD + casefold）

这节解决一个非常“反直觉”的坑：**视觉上完全一样的字符串，在 Python 里可能不相等**。

根因不是 Python “不智能”，而是 Unicode 的设计允许同一个视觉字符用不同的码点序列表示（组合字符/兼容字符）。

你要掌握的结论就 3 条：

1. **比较前先规范化**（通常用 NFC）
2. **大小写不敏感比较用 `casefold()`**（不要只用 `lower()`）
3. **NFKC/NFKD 只能用于搜索/索引，不要用于持久化存储**（可能改变语义/丢失格式）

配套脚本：`07_unicode_normalization_demo.py`。

---

## 零、新手清爽版（只记这些也能用）

### 核心一句话

**两个字看起来一样，Python 却说不相等**——因为 Unicode 允许**同一视觉字形**用**不同码点序列**表示。  
**比较、去重、做 key 前**，通常要先 **`unicodedata.normalize("NFC", s)`**。（**NFC** 不是万能：少数「兼容字形」要对齐得用 **NFKC**，见下文 **§二·2.3**。）

### 你一定会踩的坑

`café` 两种合法写法：

- **一个码点**：`U+00E9`（预合成 é）
- **两个码点**：`e`（`U+0065`）+ **组合重音** `U+0301`

肉眼一样 → **码点不同** → **`s1 != s2`** 可以成立。这不是编码乱码，是**规范化**问题。

### 四种形式，先记两个

| 形式 | 干什么 | 你什么时候用 |
| :--- | :--- | :--- |
| **NFC** | 分解再合成，**尽量预合成** | **默认**：存库、传输、**精确比较**、字典 key |
| **NFD** | **彻底拆开**（字母 + 组合符号） | 要单独处理重音/变音符号时 |
| **NFKC / NFKD** | 连**兼容字符**也折叠（如 ½→1/2、上标²→2） | **只做搜索/匹配**；**不要**当权威数据存库 |

### 大小写不敏感：用 `casefold()`，别只靠 `lower()`

例如德语 **`ß`**：`lower()` 往往还是 **`ß`**；**`casefold()`** 会对齐成与 **`ss`** 可比的形式。做法：**先 NFC，再 `casefold()`**。

### 三句口诀

1. **看起来一样 ≠ 码点一样**  
2. **比较前习惯带一层 `normalize("NFC", …)`**  
3. **忽略大小写：`NFC` + `casefold()`，别只信 `lower()`**

### 10 秒看懂四形式（示意图）

```text
同一视觉的字，Unicode 里可能有多套「合法码点配方」
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   【NFC】                    【NFD】
   合成·尽量短                拆开·字母+记号分行
   存库 / 默认比较            处理变音、笔画记号
        │                       │
        └───────────┬───────────┘
                    ▼
        【NFKC / NFKD】更猛：连「兼容区」的字形也压扁
                    │
                    └── 只给搜索/索引用，写完就扔，别当原件存档
```

### 直接可用的比较

```python
from unicodedata import normalize

def nfc_equal(a: str, b: str) -> bool:
    return normalize("NFC", a) == normalize("NFC", b)

def fold_equal(a: str, b: str) -> bool:
    return normalize("NFC", a).casefold() == normalize("NFC", b).casefold()
```

下文 **§一～§六** 是同一套知识的展开、例子与 **`shave_marks`** 搜索向技巧。

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
    """区分大小写的等价比较：NFC 规范化后比较。"""
    return normalize("NFC", a) == normalize("NFC", b)

def fold_equal(a: str, b: str) -> bool:
    """大小写不敏感的等价比较：NFC + casefold。"""
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
    """去掉组合重音等标记（只适合搜索/索引）。"""
    norm = unicodedata.normalize("NFD", txt)
    shaved = "".join(c for c in norm if not unicodedata.combining(c))
    return unicodedata.normalize("NFC", shaved)
```

---

## 六、实战最佳实践（直接落地）

### 6.1 存储 / 传输 / 精确比较

**目标**：同一业务含义的字符串，在磁盘、API、数据库里**只保留一种「权威」码点形态**，避免「肉眼一样、唯一约束却插两条」的灾难。

- **入库 / 写文件 / 发 JSON 前**：对「需要当身份」的文本字段做一次 **`normalize("NFC", s)`**（若来源不可信，可先 **`strip()`** 再 NFC，按业务决定）。  
- **去重**：`set`、**`GROUP BY`**、**唯一索引**——先把候选值都 NFC，再参与哈希或比较；否则 `café` 的两种写法会算成两个 key。  
- **`dict` / 映射 key**：用户输入、外部 ID、标签名等，若要做查找表，**key 用 NFC 后的串**（或存原串 + 单独存 `nfc_key` 列）。  
- **两端比较**：**比较双方**都先 **`normalize("NFC", x)`** 再 **`==`**；只规范一边仍可能对不齐。  
- **仍要注意**：NFC 解决的是 **规范等价**（canonical equivalence）。**兼容等价**（如 `Ω` vs `Ω`、`½` vs `1/2`）要对齐需 **NFKC**，但那属于 **6.3** 的「宽松」层，**不要**写回主数据。

### 6.2 大小写不敏感比较

**目标**：多语言下「算不算同一个词」——比 **`lower()`** 更稳的做法是 **先 NFC，再 `casefold()`**。

- **推荐写法**：`normalize("NFC", s).casefold()`（与 **§四** 的 **`fold_equal`** 一致）。  
- **顺序不要反**：先 NFC 再 casefold。先 casefold 再 NFC 在多数场景也行，但团队统一成「**NFC → casefold**」最省心。  
- **典型收益**：德语 **`Straße`** 与 **`STRASSE`** 一类比较；**`lower()`** 往往仍把 **`ß`** 当 **`ß`**，**`casefold()`** 会按 Unicode 规则对齐到可比形式。  
- **边界**：极个别特殊脚本仍有本地化规则；若业务只服务单一语言，仍建议保留 **NFC + casefold** 作为默认基线。

### 6.3 搜索 / 索引（更宽松）

**目标**：用户搜 **`cafe`** 也能命中 **`café`**；搜 **`1/2`** 也能碰到 **`½`**；日志检索时忽略「全角/兼容字形」差异。  
**代价**：**会改字形、改长度、有时改语义**——产物只能是**派生字段**或**内存里的查询键**，**不能**覆盖 **6.1** 里的权威存盘串。

#### 6.3.1 流水线 A：NFKC + casefold（最常见）

```python
from unicodedata import normalize

def search_key(s: str) -> str:
    """仅用于搜索/索引/去重提示，不可当数据库主存字段。"""
    return normalize("NFKC", s).casefold()
```

- **NFKC** 会折叠**兼容字符**（例：`Ω`→`Ω`、`½`→`1/2`、部分全角数字→半角等，以 Unicode 表为准）。  
- 再 **casefold** 统一大小写，适合「用户输入 vs 库内 NFC 正文」的**宽松匹配**：两边都用 **`search_key(...)`** 比，或只对**查询词**做 **`search_key`** 去扫已 NFC 的列（视性能与安全而定）。  
- **不要**把 **`search_key` 的结果写回**业务主表替换原文；需要持久化时单独建 **`search_vector` / `normalized_query` 列**，并文档写明「可损失信息」。

#### 6.3.2 流水线 B：在 A 之后加 `shave_marks`（更猛，更危险）

**`shave_marks`**（见 **§五**）：**NFD** → 去掉**组合标记**（重音等）→ 再 **NFC**。效果上常把 **`café`** 变成 **`cafe`**。

```python
def search_key_aggressive(s: str) -> str:
    return shave_marks(normalize("NFKC", s)).casefold()
```

（**`shave_marks`** 定义见 **§五**；复制时请两段一起带走。）

- **适用**：「拉丁字母 + 重音」为主的搜索、URL slug、粗粒度建议。  
- **风险**：**语义可能变**（人名、法文词是否仍算同一个词）；**非拉丁文**可能产生意外（依赖具体字符是否靠组合标记区分词义）。  
- **规则**：与 **NFKC 一样**——**只作索引键**，**不**替代用户提交的原始字符串。

#### 6.3.3 怎么选？

| 需求 | 建议 |
| :--- | :--- |
| 精确身份、唯一约束、审计原文 | **6.1**：只 **NFC**，必要时 **6.2** 比大小写 |
| 兼容字形 + 忽略大小写的搜索 | **6.3.1**：**NFKC + casefold** |
| 还要忽略重音（cafe ≈ café） | **6.3.2**：**NFKC → shave_marks → casefold**（接受语义风险） |

落地时：**主存 NFC** + **旁路索引列**存 **`search_key` 或 `search_key_aggressive`**，查询走索引列，展示仍用原文。

---

## 七、可运行对照

运行：

```bash
python part-1-data-structures/chapter-04/07_unicode_normalization_demo.py
```

与 **§零** 口诀对照：脚本用 **`ascii()`** 打印码点差异，避免终端编码干扰。

脚本会打印：

- `café` 两种表示的码点序列与长度差异
- NFC/NFD 后的对齐结果
- NFKC 折叠兼容字符（`Ω`/`µ`/`½`）的效果
- `casefold()` 对 `ß` 的效果
- `nfc_equal` / `fold_equal` / `shave_marks` 的实战对比

