"""
按 Unicode 官方名称关键字查找字符（思路接近《流畅的 Python》中的 cf.py）。

Unicode character finder (similar spirit to Fluent Python's cf.py).

Usage:
  python part-1-data-structures/chapter-04/09_unicode_char_finder.py CAT EYES
  python part-1-data-structures/chapter-04/09_unicode_char_finder.py BLACK QUEEN --limit 20

Notes:
- This scans all Unicode code points (0x0000..0x10FFFF), skipping surrogate range.
- Output uses ascii() for safe printing on Windows consoles.

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import argparse
import sys
import unicodedata


START = 0x0000
END = 0x110000  # 上界不包含
SURROGATE_START = 0xD800
SURROGATE_END = 0xE000  # 上界不包含（代理区需跳过）


def iter_named_chars():
    """遍历可命名字符：码点 → 字符 → unicodedata.name（无名称则跳过）。"""
    for cp in range(START, END):
        if SURROGATE_START <= cp < SURROGATE_END:
            continue
        ch = chr(cp)
        try:
            nm = unicodedata.name(ch)
        except ValueError:
            continue
        yield cp, ch, nm


def match_all_words(name: str, query_words: set[str]) -> bool:
    """判断官方名称中的词集合是否包含用户查询的每一个词（name 已规范为大写空格分隔）。"""
    words = set(name.split())
    return query_words.issubset(words)


def main(argv: list[str]) -> int:
    """解析命令行，扫描全码表并打印匹配行。"""
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("words", nargs="+", help="Unicode name keywords (case-insensitive)")
    ap.add_argument("--limit", type=int, default=100, help="Max results to print (default: 100)")
    args = ap.parse_args(argv)

    query_words = {w.upper() for w in args.words if w.strip()}
    if not query_words:
        ap.print_help()
        return 2

    printed = 0
    for cp, ch, nm in iter_named_chars():
        # 名称通常已大写，仍 upper 一次以免边缘实现差异
        if match_all_words(nm.upper(), query_words):
            print(f"U+{cp:04X} {ascii(ch)} {nm}")
            printed += 1
            if printed >= args.limit:
                break

    if printed == 0:
        print("No matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

