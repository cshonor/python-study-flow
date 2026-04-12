"""
Demo for 09-Unicode数据库与unicodedata.md (numeric semantics).

Run:
  python part-1-data-structures/chapter-04/09_unicode_numeric_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import unicodedata


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def try_name(ch: str) -> str:
    try:
        return unicodedata.name(ch)
    except ValueError:
        return "<no name>"


def try_digit(ch: str) -> str:
    try:
        return str(unicodedata.digit(ch))
    except ValueError:
        return "-"


def try_numeric(ch: str) -> str:
    try:
        return str(unicodedata.numeric(ch))
    except ValueError:
        return "-"


def demo_numeric() -> None:
    section("1) isdecimal / isdigit / isnumeric + unicodedata.digit/numeric")
    samples = [
        "0",
        "9",
        "①",  # circled digit one
        "²",  # superscript two
        "Ⅷ",  # roman numeral eight
        "½",  # fraction
        "四",  # CJK numeric (numeric=True)
        "٣",  # ARABIC-INDIC DIGIT THREE
    ]

    header = [
        "ch",
        "U+",
        "name",
        "isdecimal",
        "isdigit",
        "isnumeric",
        "digit()",
        "numeric()",
    ]

    rows: list[list[str]] = []
    for ch in samples:
        rows.append(
            [
                ascii(ch),
                f"U+{ord(ch):04X}",
                try_name(ch),
                str(ch.isdecimal()),
                str(ch.isdigit()),
                str(ch.isnumeric()),
                try_digit(ch),
                try_numeric(ch),
            ]
        )

    widths = [len(h) for h in header]
    for r in rows:
        for i, col in enumerate(r):
            widths[i] = max(widths[i], len(col))

    def fmt(cols: list[str]) -> str:
        return " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))

    print(fmt(header))
    print("-+-".join("-" * w for w in widths))
    for r in rows:
        print(fmt(r))


def demo_int_vs_numeric() -> None:
    section("2) Why int(ch) is not enough")
    for ch in ["½", "Ⅷ", "①"]:
        print("ch:", ascii(ch), "name:", try_name(ch))
        try:
            v = int(ch)
        except Exception as e:
            # Print exception message safely; some consoles can't encode the original character.
            print("  int(ch) ->", type(e).__name__ + ":", ascii(str(e)))
        print("  unicodedata.numeric(ch) ->", try_numeric(ch))


def main() -> None:
    demo_numeric()
    demo_int_vs_numeric()


if __name__ == "__main__":
    main()

