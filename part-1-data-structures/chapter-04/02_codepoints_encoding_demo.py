"""
Demo for 02-码点编码与编解码错误.md (Fluent Python ch.4).

Run:
  python part-1-data-structures/chapter-04/02_codepoints_encoding_demo.py

Notes:
- This workspace uses a Windows console with stdout encoding often set to GBK.
- To avoid UnicodeEncodeError in console output, this demo prints most text via ascii().

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import sys


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def uplus(s: str) -> str:
    return " ".join(f"U+{ord(ch):04X}" for ch in s)


def demo_codepoints() -> None:
    section("1) Characters -> code points (ord/chr, U+....)")
    samples = ["A", "é", "中", "€"]
    for ch in samples:
        print("ch:", ascii(ch), "ord:", ord(ch), "U+:", uplus(ch), "chr:", ascii(chr(ord(ch))))


def demo_utf8_bytes_length() -> None:
    section("2) len(str) vs len(str.encode('utf-8'))")
    s = "café"
    raw = s.encode("utf-8")
    print("s:", ascii(s), "len(s):", len(s))
    print("utf-8 bytes:", raw, "len(bytes):", len(raw), "byte values:", list(raw))


def demo_decode_wrong_codec() -> None:
    section("3) Same bytes, different decodings")
    text = "北京"
    raw_utf8 = text.encode("utf-8")
    print("raw_utf8:", raw_utf8)
    print("decode utf-8:", ascii(raw_utf8.decode("utf-8")))
    try:
        # Deliberately wrong: interpret UTF-8 bytes using GBK.
        wrong = raw_utf8.decode("gbk")
        print("decode gbk (wrong):", ascii(wrong))
    except UnicodeDecodeError as e:
        print("decode gbk -> UnicodeDecodeError:", e)


def demo_errors_policy() -> None:
    section("4) errors= strict / replace / ignore (decode)")
    bad = b"\xff\xfe\x00"
    for policy in ("strict", "replace", "ignore"):
        try:
            out = bad.decode("utf-8", errors=policy)
            print(f"errors={policy!r}:", "ascii(out)=", ascii(out))
        except UnicodeDecodeError as e:
            print(f"errors={policy!r}: UnicodeDecodeError:", e)


def demo_stdout_encoding_trap() -> None:
    section("5) Console boundary: sys.stdout.encoding & why ascii() helps")
    print("sys.getdefaultencoding():", sys.getdefaultencoding())
    print("sys.stdout.encoding:", sys.stdout.encoding)
    print("sys.stdout.errors:", sys.stdout.errors)
    s = "北京"
    print("safe print via ascii(s):", ascii(s))
    # DO NOT print s directly here: it may show mojibake on some consoles.


def main() -> None:
    demo_codepoints()
    demo_utf8_bytes_length()
    demo_decode_wrong_codec()
    demo_errors_policy()
    demo_stdout_encoding_trap()


if __name__ == "__main__":
    main()

