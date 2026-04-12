"""
Demo for 01-第4章Unicode文本与字节总览.md (Fluent Python ch.4).

Run:
  python part-1-data-structures/chapter-04/01_unicode_bytes_quickstart_demo.py

Note: prints use ascii() so output is safe on narrow console code pages (e.g. Windows GBK).

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_str_bytes_literals() -> None:
    section("1) str vs bytes literals")
    s = "caf\u00e9"
    b = b"caf\xc3\xa9"
    print("str repr:", ascii(s), "len chars:", len(s))
    print("bytes utf-8:", b, "len(bytes):", len(b))


def demo_encode_decode() -> None:
    section("2) encode() / decode()")
    s = "\u5317\u4eac"
    raw = s.encode("utf-8")
    print("utf-8 bytes list:", list(raw))
    print("round-trip ascii:", ascii(raw.decode("utf-8")))


def demo_errors() -> None:
    section("3) decode with errors=replace / ignore")
    bad = b"\xff\xfe\x00"
    for policy in ("strict", "replace", "ignore"):
        try:
            out = bad.decode("utf-8", errors=policy)
            print(f"errors={policy!r}: ascii(out)={ascii(out)}")
        except UnicodeDecodeError as e:
            print(f"errors={policy!r}: UnicodeDecodeError: {e}")


def main() -> None:
    demo_str_bytes_literals()
    demo_encode_decode()
    demo_errors()


if __name__ == "__main__":
    main()
