# 4.10 支持 `str` 和 `bytes` 的双模式 API：`re` 与 `os` 的坑一次讲透

这一节要解决的核心问题是：**同一个标准库 API，传 `str` 和传 `bytes`，行为可能完全不同**。  
如果你没意识到这一点，很容易写出“看起来没错、但匹配不到/找不到文件/跨平台翻车”的代码。

最典型的两类双模式 API：

- `re`：正则表达式（`str` 模式是 Unicode-aware，`bytes` 模式几乎是 ASCII-aware）
- `os`：文件系统（很多系统把文件名当 bytes；Python 用 `str` 做抽象，但仍保留 bytes 入口）

配套脚本：`10_dual_mode_api_demo.py`。

---

## 一、什么叫“双模式 API”？

所谓“双模式”就是：**同一个函数/模块同时支持 `str` 与 `bytes`**，并且：

- 你传入 `str` → 它以“Unicode 文本”的语义运行，返回也通常是 `str`
- 你传入 `bytes` → 它以“原始字节”的语义运行，返回也通常是 `bytes`

关键点：**类型决定语义**。  
你不能“把 bytes 当文本用”又期待它按 Unicode 规则做事；也不能“把 str 当 bytes 用”又期待它保持原始字节不变。

---

## 二、4.10.1 `re`：`str` 正则 vs `bytes` 正则（差异巨大）

### 2.1 一条铁律：pattern 与 text 类型必须一致

- `re.compile(r"...")`（`str` pattern）只能匹配 `str` 文本  
- `re.compile(rb"...")`（`bytes` pattern）只能匹配 `bytes` 文本  

类型不一致会直接抛 `TypeError`，这点反而不容易踩坑。

真正容易踩坑的是：**元字符在 bytes 模式下“变窄了”**。

### 2.2 元字符差异：`\d` / `\w` / `\s`

| 元字符 | `str` 模式（Unicode 正则） | `bytes` 模式（近似 ASCII 正则） |
|---|---|---|
| `\d` | 匹配 Unicode 数字（多语言数字） | 只匹配 ASCII `0-9` |
| `\w` | 匹配 Unicode 字母/数字/下划线 | 只匹配 ASCII 字母/数字/下划线 |
| `\s` | 匹配 Unicode 空白 | 只匹配 ASCII 空白 |

### 2.3 关键示例（Ramanujan）：泰米尔数字在 bytes 模式下会“消失”

脚本里会构造这段文本（包含泰米尔数字）：

- `str` 模式下 `\d+` 会匹配到泰米尔数字与 ASCII 数字
- `bytes` 模式下 `\d+` 只会匹配 ASCII 数字（泰米尔数字的 UTF-8 字节序列根本不可能被 `rb"\d"` 命中）

结论（务实版）：

- **处理“文本”就用 `str` 正则**（Unicode-aware）  
- 只有在你明确要处理“字节协议/ASCII 字节流”时才用 `bytes` 正则  

### 2.4 想在 `str` 模式下“只按 ASCII”匹配？用 `re.ASCII`

你不必切换到 bytes 模式，可以写：

```python
re.compile(r"\d+", re.ASCII)
```

这会把 `\d/\w/\s` 的语义收窄到 ASCII 范围，但仍保持输入/输出是 `str`。

---

## 三、4.10.2 `os`：文件系统 API 的 `str` / `bytes` 双入口

### 3.1 先理解：很多系统里“文件名本质是 bytes”

尤其在类 Unix 系统里，内核不理解 Unicode；文件名就是 bytes 序列。  
Python 提供 `str` 形式的文件名是为了开发体验，但仍然保留 bytes 入口，以便处理“无法正确解码”的文件名。

### 3.2 `os.listdir('.')` vs `os.listdir(b'.')`

- `os.listdir(".")` → 返回 `list[str]`
- `os.listdir(b".")` → 返回 `list[bytes]`

它们的区别不是“好坏”，而是：

- `str` 版本会按文件系统编码做 decode/encode（更适合绝大多数正常场景）
- `bytes` 版本会保留原始 bytes（适合处理“鬼符文件名”、跨系统传输原始名字等）

### 3.3 正确的转换工具：`os.fsencode` / `os.fsdecode`

不要手写 `path.encode(...)` / `path.decode(...)` 去猜文件系统编码。  
用标准库给你的工具：

- `os.fsencode(pathlike_or_str)` → `bytes`
- `os.fsdecode(pathlike_or_bytes)` → `str`

它们遵循 `sys.getfilesystemencoding()` / `surrogateescape` 等约定，专门用于文件系统边界。

---

## 四、落地建议（你写项目时照这个做就很稳）

### 4.1 正则最佳实践

1. **文本处理：统一用 `str` + `re` 的 Unicode 语义**  
2. **需要 ASCII-only：在 `str` 正则上加 `re.ASCII`**  
3. bytes 正则只用于“字节协议/ASCII 字节流”这类明确需求  

### 4.2 文件系统最佳实践（Unicode 三明治）

1. **尽早解码成 `str`，尽量在业务逻辑里只用 `str`**  
2. **遇到无法解码的文件名，再用 bytes 入口兜底**（`os.listdir(b".")` 等）  
3. `str` ↔ `bytes` 在文件系统边界用 `os.fsencode/fsdecode`  

---

## 五、可运行对照

运行：

```bash
python part-1-data-structures/chapter-04/10_dual_mode_api_demo.py
```

脚本会展示：

- `re`：`str` vs `bytes` 模式下 `\d/\w` 的差异（含 `re.ASCII`）
- `os`：`listdir(str)` vs `listdir(bytes)`、文件系统编码、`fsencode/fsdecode` 的效果

