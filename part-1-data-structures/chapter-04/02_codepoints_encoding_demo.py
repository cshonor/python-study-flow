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
    section("2) len(str) vs len(str.encode('utf-8')) (UTF-8 widths)")
    samples = [
        ("ASCII", "a"),
        ("Latin-1-ish", "café"),
        ("CJK", "\u4e2d"),
        ("emoji", "\U0001f600"),
    ]
    for label, s in samples:
        raw = s.encode("utf-8")
        print(
            f"{label}:",
            ascii(s),
            "len(str):",
            len(s),
            "len(utf-8):",
            len(raw),
            "bytes:",
            list(raw),
        )


def demo_decode_wrong_codec() -> None:
    section("3) UnicodeDecodeError: wrong codec or illegal bytes")
    text = "北京"
    raw_utf8 = text.encode("utf-8")
    print("raw_utf8:", raw_utf8)
    print("decode utf-8:", ascii(raw_utf8.decode("utf-8")))
    # UTF-8 bytes are often *valid* GBK byte patterns -> mojibake, not always an exception.
    wrong = raw_utf8.decode("gbk")
    print("decode gbk (wrong, often mojibake):", ascii(wrong))
    try:
        raw_utf8.decode("ascii")
    except UnicodeDecodeError as e:
        print("decode ascii (always fails for these bytes) -> UnicodeDecodeError:", e)

    try:
        b"\xff".decode("utf-8")
    except UnicodeDecodeError as e:
        print("invalid utf-8 start byte -> UnicodeDecodeError:", e)


def demo_unicode_encode_error() -> None:
    section("4) UnicodeEncodeError: str -> bytes (codec too small)")
    smile = "\U0001F600"
    print("emoji as ascii(s):", ascii(smile))
    print("encode utf-8 ok:", smile.encode("utf-8"))
    try:
        smile.encode("gbk")
    except UnicodeEncodeError as e:
        print("encode gbk -> UnicodeEncodeError:", e)

    try:
        "北京".encode("ascii")
    except UnicodeEncodeError as e:
        print("encode ascii (CJK) -> UnicodeEncodeError:", e)


def demo_errors_policy() -> None:
    section("5) errors= strict / replace / ignore (decode + encode)")
    bad = b"\xff\xfe\x00"
    print("decode side:")
    for policy in ("strict", "replace", "ignore"):
        try:
            out = bad.decode("utf-8", errors=policy)
            print(f"  decode errors={policy!r}:", "ascii(out)=", ascii(out))
        except UnicodeDecodeError as e:
            print(f"  decode errors={policy!r}: UnicodeDecodeError:", e)

    s = "北京"
    print("encode side (target ascii):")
    for policy in ("strict", "replace", "ignore"):
        try:
            out = s.encode("ascii", errors=policy)
            print(f"  encode errors={policy!r}: out=", out)
        except UnicodeEncodeError as e:
            print(f"  encode errors={policy!r}: UnicodeEncodeError:", e)


def demo_hex_roundtrip() -> None:
    section("6) hex <-> bytes: fromhex, hex(' '), packet style")
    raw = bytes.fromhex("1B 48 CE AB")
    print("fromhex('1B 48 CE AB'):", raw, "==", b"\x1b\x48\xce\xab", raw == b"\x1b\x48\xce\xab")

    packet = bytes.fromhex("01 02 03 04 68 65 6c 6c 6f")
    print("fromhex packet:", packet)
    print("packet.hex(' '):", packet.hex(" "))
    print("compact:", packet.hex())

    try:
        bytes.fromhex("1")  # odd length
    except ValueError as e:
        print("fromhex odd length -> ValueError:", e)

    print("ascii(CJK + emoji):", ascii("\u5317\u4eac\N{GRINNING FACE}"))


def demo_stdout_encoding_trap() -> None:
    section("7) Console boundary: sys.stdout.encoding & why ascii() helps")
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
    demo_unicode_encode_error()
    demo_errors_policy()
    demo_hex_roundtrip()
    demo_stdout_encoding_trap()


if __name__ == "__main__":
    main()

