# 第 4 章「Unicode 文本与字节序列」— 本目录说明

本目录对应《流畅的 Python》**第 4 章**：`str` 与 `bytes`、编解码、Unicode 规范化、排序与双模式 API 等。

**建议从这里开始读**：[`01-unicode-text-and-bytes-chapter4-overview.md`](01-unicode-text-and-bytes-chapter4-overview.md)（本章主题、知识地图、**面试速记**）。

---

## 学习路线与文件一览

| 优先级 | 文件 | 说明 |
|--------|------|------|
| 0 | `01-unicode-text-and-bytes-chapter4-overview.md` | 开篇、框架、`str`/`bytes` 纲领、学习顺序 |
| 1 | `02-codepoints-encodings-and-errors.md` | 字符/码点/编码/字节、`encode`/`decode`、`errors=` |
| 2 | `03-io-encoding-checklist.md` | I/O 编码排查清单：文件/子进程/控制台 |

---

## 配套脚本（在仓库根目录执行）

```bash
python part-1-data-structures/chapter-04/unicode_bytes_quickstart_demo.py
python part-1-data-structures/chapter-04/codepoints_encoding_demo.py
python part-1-data-structures/chapter-04/io_encoding_troubleshoot_demo.py
```

| 脚本 | 说明 |
|------|------|
| `unicode_bytes_quickstart_demo.py` | 与 `01` 配套：`encode`/`decode`、字面量、`errors=` |
| `codepoints_encoding_demo.py` | 与 `02` 配套：码点与 UTF-8 字节、错误与 `errors=`、控制台边界 |
| `io_encoding_troubleshoot_demo.py` | 与 `03` 配套：文件/子进程/控制台排查套路 |

---

## 与前几章

第 2 章序列与对象模型见 `../chapter-02/`；第 3 章字典与集合见 `../chapter-03/`。本章的 **`str`** 与 **`bytes`** 是后续读写文件、网络与 `async` 的公共基础。
