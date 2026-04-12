"""
Demo for 05-常见编码与codecs.md

Run:
  python part-1-data-structures/chapter-04/codecs_encodings_table_demo.py

Notes:
- Output uses ascii()/hex to avoid Windows console encoding issues.

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

from dataclasses import dataclass


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


@dataclass(frozen=True)
class Cell:
    ok: bool
    value: str  # hex bytes or "*"


def encode_hex(ch: str, encoding: str) -> Cell:
    try:
        b = ch.encode(encoding, errors="strict")
    except UnicodeEncodeError:
        return Cell(ok=False, value="*")
    return Cell(ok=True, value=b.hex(" "))


def print_table(chars: list[str], encodings: list[str]) -> None:
    header = ["char", "U+....", *encodings]
    rows: list[list[str]] = []
    for ch in chars:
        row = [ascii(ch), f"U+{ord(ch):04X}"]
        for enc in encodings:
            row.append(encode_hex(ch, enc).value)
        rows.append(row)

    widths = [len(h) for h in header]
    for r in rows:
        for i, col in enumerate(r):
            widths[i] = max(widths[i], len(col))

    def fmt_row(cols: list[str]) -> str:
        return " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))

    print(fmt_row(header))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt_row(r))


def demo_table() -> None:
    section("1) Same characters, different encodings (hex bytes; * means cannot encode)")
    chars = ["A", "é", "ñ", "€", "中", "—"]
    encodings = [
        "ascii",
        "latin-1",
        "cp1252",
        "gb2312",
        "gbk",
        "utf-8",
        "utf-16le",
    ]
    print_table(chars, encodings)


def demo_same_bytes_different_decodings() -> None:
    section("2) Same bytes, different decodings (why mojibake happens)")
    text = "北京"
    raw_utf8 = text.encode("utf-8")
    print("text (ascii-safe):", ascii(text))
    print("raw_utf8:", raw_utf8)
    print("raw_utf8 hex:", raw_utf8.hex(" "))
    for enc in ("utf-8", "gbk", "latin-1"):
        try:
            out = raw_utf8.decode(enc, errors="strict")
            print(f"decode as {enc!r}:", ascii(out))
        except UnicodeDecodeError as e:
            print(f"decode as {enc!r}: UnicodeDecodeError:", e)


def main() -> None:
    demo_table()
    demo_same_bytes_different_decodings()


if __name__ == "__main__":
    main()

