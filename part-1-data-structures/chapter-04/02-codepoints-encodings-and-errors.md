# 字符、码点、编码与错误处理（第 4 章入门）

> **本篇定位**：《流畅的 Python》第 4 章的第一组核心概念：把 **字符（character）**、**码点（code point）**、**编码（encoding）**、**字节（bytes）** 的关系讲透，并掌握 `encode`/`decode` 的常见异常与 `errors=` 策略。  
> **前置**：本章导读见 `01-unicode-text-and-bytes-chapter4-overview.md`。  
> **配套脚本**：`codepoints_encoding_demo.py`（输出使用 `ascii()`，适配 Windows 控制台编码差异）。

---

## 一、四个词一张图（心智模型）

- **字符**：人类理解的符号，例如 `A`、`中`、`€`、`é`。  
- **码点**：Unicode 为字符分配的编号，例如 `A` 是 `U+0041`，`中` 是 `U+4E2D`。  
- **编码**：把「码点序列」翻译为「字节序列」的规则，例如 UTF-8、UTF-16、GBK。  
- **字节**：最终落在磁盘 / 网络 / 进程间传输的 0–255 数字序列。

在 Python 3 里，你只要牢记两句话：

- **`str` 是文本（码点序列）**：面向人类语义。  
- **`bytes`/`bytearray` 是字节序列**：面向存储与传输。

因此跨越边界的动作必须显式发生：

- **编码**：`str.encode(encoding)` → `bytes`  
- **解码**：`bytes.decode(encoding)` → `str`

---

## 二、`ord` / `chr`：字符与码点的桥

- `ord(ch)`：字符 → 码点整数  
- `chr(cp)`：码点整数 → 字符

你可以用它们把“看不见的码点编号”变成可验证的事实，例如把字符打印成 `U+....` 形式。

---

## 三、为什么 UTF-8 下「字节数」可能比「字符数」多

- `len(s)` 是**字符数**（更准确说：码点数）。  
- `len(s.encode('utf-8'))` 是**字节数**。

ASCII 字符（如 `A`、`b`）在 UTF-8 中都是 1 字节；但很多字符（中文、emoji、带音标字符等）会占用 2–4 个字节。

---

## 四、两类经典异常：`DecodeError` vs `EncodeError`

### 1) `UnicodeDecodeError`

把 **bytes** 按“错误的编码”解释为文本时失败。

典型场景：拿到一段 **UTF-8** 字节，却用 **GBK** 去 `decode()`（或反之）。

### 2) `UnicodeEncodeError`

把 **str** 写成字节时，目标编码无法表示某些字符时失败。

典型场景：Windows 控制台的 `sys.stdout.encoding` 可能是 **GBK**，当你 `print()` 含某些字符（例如替换符 `\ufffd`、组合音标等）时，**输出阶段**就会触发“编码失败”。  
这也是为什么在 Windows 上你可能看到一种现象：**逻辑上解码成功**，但 **打印时乱码/报错**。

---

## 五、`errors=`：当你必须“继续走下去”

`encode`/`decode` 都支持 `errors=`，常用策略：

- **`'strict'`**：默认，遇到问题直接抛异常（最安全）。  
- **`'replace'`**：用替换字符代替（解码常见为 `\ufffd`）。  
- **`'ignore'`**：直接丢弃无法处理的部分。

策略选型取决于业务目标：日志/监控可能优先“不断流”，协议解析或数据清洗通常更偏向 `'strict'`（宁可失败也不要悄悄吞掉错误）。

---

## 六、实践原则（再次强调）

- **尽早解码，最晚编码**。  
- **文本文件读写显式 `encoding=`**：不要依赖平台默认编码。  
- 遇到乱码/异常时，优先定位“到底是哪一步在 `encode` 或 `decode`”，再决定修复编码参数或错误处理策略。

---

## 七、可运行对照

见 **`codepoints_encoding_demo.py`**：

- `ord/chr` 与 `U+....` 格式化  
- `len(str)` vs `len(utf8_bytes)`  
- 同一段 bytes 用不同编码 `decode` 的差异  
- `errors='strict'/'replace'/'ignore'` 行为对比  
- `sys.stdout.encoding` / `sys.stdout.errors` 的观测（解释为何 Windows 上 `print` 常成为“最后一道坑”）

