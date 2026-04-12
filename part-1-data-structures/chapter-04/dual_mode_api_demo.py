"""
Demo for 10-双模式API-str与bytes.md

Run:
  python part-1-data-structures/chapter-04/dual_mode_api_demo.py

Notes:
- Output uses ascii() to avoid Windows console encoding issues.

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def safe(obj: object) -> str:
    return ascii(obj)


def demo_re_str_vs_bytes() -> None:
    section("1) re: str patterns vs bytes patterns (Unicode vs ASCII-ish)")

    re_numbers_str = re.compile(r"\d+")
    re_words_str = re.compile(r"\w+")
    re_numbers_ascii = re.compile(r"\d+", re.ASCII)
    re_words_ascii = re.compile(r"\w+", re.ASCII)

    re_numbers_bytes = re.compile(rb"\d+")
    re_words_bytes = re.compile(rb"\w+")

    # Tamil digits: U+0BE7..U+0BEF (௧௯௨௯ etc.)
    text_str = (
        "Ramanujan saw \u0be7\u0bed\u0be8\u0bef"
        " as 1729 = 1\u00b3 + 12\u00b3 = 9\u00b3 + 10\u00b3."
    )
    text_bytes = text_str.encode("utf-8")

    print("text_str (ascii-safe):", ascii(text_str))
    print("text_bytes hex head:", text_bytes[:80].hex(" "))

    print("\nNumbers via \\d+")
    print("  str        :", safe(re_numbers_str.findall(text_str)))
    print("  str+ASCII  :", safe(re_numbers_ascii.findall(text_str)))
    print("  bytes      :", safe(re_numbers_bytes.findall(text_bytes)))

    print("\nWords via \\w+")
    print("  str        :", safe(re_words_str.findall(text_str)[:12]))
    print("  str+ASCII  :", safe(re_words_ascii.findall(text_str)[:12]))
    print("  bytes      :", safe(re_words_bytes.findall(text_bytes)[:12]))

    print("\nType rule (must match):")
    try:
        re_numbers_str.findall(text_bytes)  # type: ignore[arg-type]
    except TypeError as e:
        print("  str pattern + bytes text -> TypeError:", safe(str(e)))


def demo_os_str_vs_bytes() -> None:
    section("2) os: str vs bytes paths (listdir + fsencode/fsdecode)")
    print("sys.getfilesystemencoding():", sys.getfilesystemencoding())
    print("sys.getfilesystemencodeerrors():", getattr(sys, "getfilesystemencodeerrors", lambda: "?")())

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # Create a file with a Unicode character in its name.
        filename = "digits-of-π.txt"
        p = root / filename
        p.write_text("pi", encoding="utf-8")

        # str path
        names_str = os.listdir(str(root))
        print("listdir(str) (ascii-safe):", safe(names_str))

        # bytes path (keep raw bytes)
        names_bytes = os.listdir(os.fsencode(str(root)))
        print("listdir(bytes) (ascii-safe):", safe(names_bytes))

        bname = os.fsencode(filename)
        print("os.fsencode(filename):", bname, "| hex:", bname.hex(" "))
        print("os.fsdecode(bname):", safe(os.fsdecode(bname)))


def main() -> None:
    demo_re_str_vs_bytes()
    demo_os_str_vs_bytes()


if __name__ == "__main__":
    main()

