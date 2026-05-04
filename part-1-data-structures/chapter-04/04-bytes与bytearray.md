# `bytes` 与 `bytearray`：别把 `b'...'` 当字符串（第 4 章 4.2 重点）

这一节要把 3 件事讲清楚：

- **`str` 和 `bytes` 是两种完全不同的数据**：`str` 是文本（Unicode 码点序列），`bytes` 是原始字节（0–255 的整数序列）。
- **`bytes` 不可变，`bytearray` 可变**：要不要“改内容”，决定你用哪一个。
- **最常见的新手坑**：`b'abc'[0]` 不是 `'a'`，而是 `97`；以及“中文不能写成 `b'咖啡'`”。

配套脚本：`04_bytes_bytearray_demo.py`。

---

## 一、先把一句话说死：`bytes` 不是字符串

你看到 `b'cafe'` 很像字符串，但它不是 `str`，而是 **bytes 字面量**。

- `str`：给人看的文本（码点序列），例如 `"咖啡"`、`"hello"`。
- `bytes`：给机器存储/传输的字节序列，例如网络包、文件内容、图片数据。

Python 3 会强制你把这两者区分开：你不能把 `str` 和 `bytes` 混在一起拼接/比较/写入（除非显式转换）。

---

## 二、`bytes` 的核心特性：元素是整数（0–255）

### 2.1 索引：返回 `int`

```python
b = b"cafe"
assert b[0] == 99  # 成立 → 索引得 int；'c' 的 ASCII 为 99
assert isinstance(b[0], int)  # 成立 → bytes 单元素类型为 int
```

这就是很多人第一眼会懵的地方：**bytes 的“单个元素”是一个字节值**，自然表现为 0–255 的整数。

### 2.2 切片：返回新的 `bytes`

```python
b = b"cafe"
assert b[0:1] == b"c"  # 成立 → 切片得长度为 1 的 bytes
assert isinstance(b[0:1], bytes)  # 成立 → bytes 切片类型仍为 bytes
```

把这条规律记住，你就不会混淆这两个表达式：

- `b[i]` → `int`
- `b[i:i+1]` → `bytes`（长度为 1 的 bytes）

---

## 三、怎么创建 `bytes`？

### 3.1 方式 1：字面量 `b'...'`（只能直接写 ASCII）

```python
b_cafe = b"cafe"
```

为什么“只能直接写 ASCII”？

因为字面量 `b"..."` 里每一个字符都必须能直接落到单字节（0–255）上。中文是 Unicode 字符，不可能“天然就是一个字节”，所以你必须先决定它用什么编码变成哪些字节。

> 你会在代码里看到有人写 `b'\xe4\xb8\xad'` 这种：那是手写 UTF-8 的字节值，不是把中文“直接写进 bytes”。

### 3.2 方式 2：从 `str` 编码（最常用）

```python
text = "你好"
raw = text.encode("utf-8")
assert isinstance(raw, bytes)  # 成立 → encode 得到 bytes

back = raw.decode("utf-8")
assert back == "你好"  # 成立 → decode 还原原文本
```

把这段当作“边界转换模板”：

- `str` → `bytes`：`encode(...)`
- `bytes` → `str`：`decode(...)`

---

## 四、`bytes` 不可变：你不能原地改它

```python
b = b"cafe"
# b[0] = 88  # TypeError: 'bytes' object does not support item assignment
```

不可变带来的好处：

- 更安全：不会被某个函数“顺手改掉”。
- 可作为 `dict` 的 key / 放进 `set`（前提是内容本身就是字节序列，当然满足可哈希）。

---

## 五、`bytearray`：`bytes` 的可变版本

`bytearray` 和 `bytes` 最大的区别就一个：**它能改**。

```python
ba = bytearray(b"cafe")
ba[0] = 67                 # 'C'
assert ba == bytearray(b"Cafe")  # 成立 → 首字节已改为 67（'C'）
```

什么时候你会更倾向于 `bytearray`？

- 你确实要在字节层面频繁修改内容（拼接、替换、就地写入缓冲区）。
- 你不想每次修改都创建一个全新的 `bytes` 对象。

---

## 六、十六进制与 `fromhex`：非常常用的“看得懂的 bytes”

做协议/抓包/排查编码时，你经常拿到的是十六进制表示（更适合人类阅读）。

```python
raw = bytes.fromhex("1B 48 CE AB")   # 空格会被忽略
assert raw == b"\x1bH\xce\xab"  # 成立 → 十六进制串解析为对应字节序列
```

一个非常实用的技巧：

- **展示 bytes**：用 `raw.hex(" ")` 输出成十六进制，更像抓包工具看到的样子。
- **展示 str**：用 `ascii(text)` 输出，避免 Windows 控制台编码导致的“打印阶段报错”。

---

## 七、总结（当成你的“避坑清单”）

1. **看到 `b'...'` 就要警觉**：这是 `bytes`，不是字符串。  
2. **永远记住索引规则**：`b[i]` 是 `int`，`b[i:i+1]` 才是 `bytes`。  
3. **中文/非 ASCII 一律走编码**：`"你好".encode("utf-8")`，不要幻想 `b"你好"`。  
4. **需要改就用 `bytearray`**：否则优先用 `bytes`（更安全、可哈希）。  
5. **排查用 hex/ascii**：`raw.hex(" ")` 和 `ascii(text)` 是跨平台输出的“保命招”。  

---

## 八、可运行对照

运行：

```bash
python part-1-data-structures/chapter-04/04_bytes_bytearray_demo.py
```

