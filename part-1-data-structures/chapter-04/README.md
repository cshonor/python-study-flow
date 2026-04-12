# 第 4 章「Unicode 文本与字节序列」— 本目录说明

本目录对应《流畅的 Python》**第 4 章**：`str` 与 `bytes`、编解码、Unicode 规范化、排序与双模式 API 等。

建议从这里开始读：[`01-第4章Unicode文本与字节总览.md`](01-第4章Unicode文本与字节总览.md)（先把 `str`/`bytes` 的边界讲清楚）。

---

## 文件一览（建议顺序）

| 顺序 | 文件 | 说明 |
|------|------|------|
| 01 | `01-第4章Unicode文本与字节总览.md` | `str`/`bytes` 的整体框架与关键原则 |
| 02 | `02-码点编码与编解码错误.md` | 字符/码点/编码/字节、`encode`/`decode`、`errors=` |
| 03 | `03-IO编码排查清单.md` | I/O 编码排查清单：文件/子进程/控制台 |
| 04 | `04-bytes与bytearray.md` | `bytes`/`bytearray` 详解：索引切片、可变性、`fromhex`、避坑 |
| 05 | `05-常见编码与codecs.md` | 常见编码与 codec：多编码 bytes 对照表、兼容性与乱码直觉 |
| 06 | `06-编解码问题排查与修复.md` | 编解码问题处理：三类异常、BOM、检测与落地模板 |
| 07 | `07-Unicode规范化.md` | Unicode 规范化：NFC/NFD/NFKC/NFKD、casefold、比较工具函数 |
| 08 | `08-Unicode文本排序.md` | Unicode 文本排序：默认码点顺序、locale 局限、pyuca（UCA） |
| 09 | `09-Unicode数据库与unicodedata.md` | Unicode 数据库：`unicodedata` 字符识别与数值语义解析 |
| 10 | `10-双模式API-str与bytes.md` | 双模式 API：`re` 与 `os` 的 str/bytes 行为差异与最佳实践 |

---

## 配套脚本（在仓库根目录执行）

```bash
python part-1-data-structures/chapter-04/unicode_bytes_quickstart_demo.py
python part-1-data-structures/chapter-04/codepoints_encoding_demo.py
python part-1-data-structures/chapter-04/io_encoding_troubleshoot_demo.py
python part-1-data-structures/chapter-04/bytes_bytearray_demo.py
python part-1-data-structures/chapter-04/codecs_encodings_table_demo.py
python part-1-data-structures/chapter-04/encoding_decoding_fixes_demo.py
python part-1-data-structures/chapter-04/unicode_normalization_demo.py
python part-1-data-structures/chapter-04/unicode_sorting_demo.py
python part-1-data-structures/chapter-04/unicode_numeric_demo.py
python part-1-data-structures/chapter-04/unicode_char_finder.py CAT EYES --limit 20
python part-1-data-structures/chapter-04/dual_mode_api_demo.py
```

| 脚本 | 说明 |
|------|------|
| `unicode_bytes_quickstart_demo.py` | 与 `01` 配套：`encode`/`decode`、字面量、`errors=` |
| `codepoints_encoding_demo.py` | 与 `02` 配套：码点与 UTF-8 字节、错误与 `errors=`、控制台边界 |
| `io_encoding_troubleshoot_demo.py` | 与 `03` 配套：文件/子进程/控制台排查套路 |
| `bytes_bytearray_demo.py` | 与 `04` 配套：索引/切片差异、不可变 vs 可变、`fromhex` |
| `codecs_encodings_table_demo.py` | 与 `05` 配套：同一字符在不同编码下的 hex bytes 对照表 |
| `encoding_decoding_fixes_demo.py` | 与 `06` 配套：Encode/Decode 错误、BOM、非 UTF-8 源码的最小复现 |
| `unicode_normalization_demo.py` | 与 `07` 配套：组合字符、NFC/NFD/NFKC、casefold 与比较工具函数 |
| `unicode_sorting_demo.py` | 与 `08` 配套：默认排序 vs locale vs pyuca（若已安装） |
| `unicode_numeric_demo.py` | 与 `09` 配套：digit/numeric 与 isdecimal/isdigit/isnumeric 对照 |
| `unicode_char_finder.py` | 与 `09` 配套：按 Unicode 名称关键字搜索字符（类似 cf.py） |
| `dual_mode_api_demo.py` | 与 `10` 配套：`re`（Unicode vs ASCII-ish）+ `os`（str vs bytes 路径） |

---

## 与前几章

第 2 章序列与对象模型见 `../chapter-02/`；第 3 章字典与集合见 `../chapter-03/`。本章的 **`str`** 与 **`bytes`** 是后续读写文件、网络与 `async` 的公共基础。
