# 第 4 章「Unicode 文本与字节序列」— 本目录说明

本目录对应《流畅的 Python》**第 4 章**：`str` 与 `bytes`、编解码、Unicode 规范化、排序与双模式 API 等。

建议从这里开始读：[`01-unicode-text-and-bytes-chapter4-overview.md`](01-unicode-text-and-bytes-chapter4-overview.md)（先把 `str`/`bytes` 的边界讲清楚）。

---

## 文件一览（建议顺序）

| 顺序 | 文件 | 说明 |
|------|------|------|
| 01 | `01-unicode-text-and-bytes-chapter4-overview.md` | `str`/`bytes` 的整体框架与关键原则 |
| 02 | `02-codepoints-encodings-and-errors.md` | 字符/码点/编码/字节、`encode`/`decode`、`errors=` |
| 03 | `03-io-encoding-checklist.md` | I/O 编码排查清单：文件/子进程/控制台 |
| 04 | `04-bytes-and-bytearray.md` | `bytes`/`bytearray` 详解：索引切片、可变性、`fromhex`、避坑 |
| 05 | `05-codecs-and-common-encodings.md` | 常见编码与 codec：多编码 bytes 对照表、兼容性与乱码直觉 |

---

## 配套脚本（在仓库根目录执行）

```bash
python part-1-data-structures/chapter-04/unicode_bytes_quickstart_demo.py
python part-1-data-structures/chapter-04/codepoints_encoding_demo.py
python part-1-data-structures/chapter-04/io_encoding_troubleshoot_demo.py
python part-1-data-structures/chapter-04/bytes_bytearray_demo.py
python part-1-data-structures/chapter-04/codecs_encodings_table_demo.py
```

| 脚本 | 说明 |
|------|------|
| `unicode_bytes_quickstart_demo.py` | 与 `01` 配套：`encode`/`decode`、字面量、`errors=` |
| `codepoints_encoding_demo.py` | 与 `02` 配套：码点与 UTF-8 字节、错误与 `errors=`、控制台边界 |
| `io_encoding_troubleshoot_demo.py` | 与 `03` 配套：文件/子进程/控制台排查套路 |
| `bytes_bytearray_demo.py` | 与 `04` 配套：索引/切片差异、不可变 vs 可变、`fromhex` |
| `codecs_encodings_table_demo.py` | 与 `05` 配套：同一字符在不同编码下的 hex bytes 对照表 |

---

## 与前几章

第 2 章序列与对象模型见 `../chapter-02/`；第 3 章字典与集合见 `../chapter-03/`。本章的 **`str`** 与 **`bytes`** 是后续读写文件、网络与 `async` 的公共基础。
