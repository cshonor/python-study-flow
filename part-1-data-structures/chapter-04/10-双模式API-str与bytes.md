# 4.10 支持 str 和 bytes 的双模式 API【新手清爽排版版】

（结构清晰、重点加粗、新手能一眼抓住规则）

配套脚本：`10_dual_mode_api_demo.py`（与本节对照阅读）。

---

## 一、本节核心问题

**同一个函数，你传 `str` 和传 `bytes`，行为完全不一样。**

最容易踩坑的两个模块：

1. **`re`**（正则表达式）
2. **`os`**（文件操作）

不懂这个，你会写出：

- 正则明明写对，却匹配不到
- 文件名明明存在，却找不到
- 跨平台直接翻车

---

## 二、什么是双模式 API？

**同一个函数，同时支持 `str` 和 `bytes`。**

规则：

- 传 **`str`** → 按**文本 / Unicode** 处理  
- 传 **`bytes`** → 按**原始字节**处理  

**类型决定行为。** 不能把 `bytes` 当 Unicode 文本用，又期待 `\d` 按“全世界数字”匹配；也不能在需要原始文件名字节时，只用 `str` 硬编码猜测编码。

---

## 三、`re` 正则：`str` 模式 vs `bytes` 模式（差异巨大）

### 铁律 1：类型必须一致

**正则类型必须和待匹配文本类型一致。**

- `str` 正则 → 只能匹配 `str`
- `bytes` 正则 → 只能匹配 `bytes`

类型不匹配会直接 `TypeError`。

### 铁律 2：元字符完全不一样（超级重要）

| 符号 | `str` 模式（文本模式） | `bytes` 模式（字节模式） |
|------|------------------------|--------------------------|
| `\d` | 匹配 Unicode 数字（多语言数字） | 只匹配 `0-9` |
| `\w` | 匹配 Unicode 字母 / 数字 / 下划线等 | 只匹配 ASCII 字母 / 数字 / 下划线 |
| `\s` | 匹配 Unicode 空白 | 只匹配 ASCII 空白 |

**示例直觉（脚本里也有）：** 同一段含**泰米尔数字**的文本，在 `str` 下 `\d+` 能匹配到泰米尔数字和 ASCII 数字；换成 `bytes` 后，UTF-8 字节序列不会被 `rb"\d"` 当成“数字”，往往只剩 ASCII 数字能匹配。**这不是 bug，是语义不同。**

### 结论

- **处理文字 → 永远用 `str` 正则**
- **处理字节协议 / 明确只要 ASCII 字节流 → 才用 `bytes` 正则**

### 想只匹配英文数字？

**不要用 `bytes` 取巧**，在 `str` 上收窄即可：

```python
re.compile(r"\d+", re.ASCII)
```

输入输出仍是 `str`，只是把 `\d/\w/\s` 的语义限制在 ASCII。

---

## 四、`os` 文件模块：`str` 文件名 vs `bytes` 文件名

### 系统真相

- **类 Unix：文件名本质是 bytes**（内核不替你“懂 Unicode”）
- Python 给你 `str` 路径，是为了日常好用；**`bytes` 入口还在，就是为了边界情况**

### 两个用法

1. `os.listdir(".")` → 返回 **`list[str]`**（正常开发用这个）
2. `os.listdir(b".")` → 返回 **`list[bytes]`**（乱码名、无法可靠 decode 的名字、要保留原始字节时）

### 正确转换方式（不要自己乱 `encode` / `decode`）

- `str` → `bytes`：**`os.fsencode(path)`**
- `bytes` → `str`：**`os.fsdecode(path)`**

这是标准库为**文件系统边界**准备的转换（配合 `sys.getfilesystemencoding()`、`surrogateescape` 等约定），比手写编码名更安全。

---

## 五、新手最稳最佳实践（背这一段就够）

### 正则怎么写？

1. **99% 场景：用 `str` 正则**
2. 要限制成英文数字等：加 **`re.ASCII`**
3. **`bytes` 正则只用来处理二进制协议**，别拿来当“全文搜索捷径”

### 文件操作怎么写？

1. **业务里尽量全程 `str` 路径**
2. **遇到鬼畜文件名**：再用 `os.listdir(b"...")` 等 **bytes** 入口兜底
3. **`str` ↔ `bytes` 在文件系统边界：只用 `os.fsencode` / `os.fsdecode`**

---

## 六、新手必背 4 句总结

1. **双模式 API：传 `str` 按文本，传 `bytes` 按字节**
2. **`\d` `\w` `\s` 在 `str` 和 `bytes` 下完全不同**
3. **文字永远用 `str` 正则；别用 `bytes` 正则冒充“只匹配英文”**
4. **文件名在系统边界转换：用 `os.fsencode` / `os.fsdecode`**

---

## 七、可运行对照

在仓库根目录执行：

```bash
python part-1-data-structures/chapter-04/10_dual_mode_api_demo.py
```

脚本会演示：`re` 在 `str` / `bytes` / `re.ASCII` 下的差异，以及 `os.listdir(str)` vs `listdir(bytes)`、`fsencode` / `fsdecode` 的效果。
