"""
Demo for 07-Unicode规范化.md

Run:
  python part-1-data-structures/chapter-04/07_unicode_normalization_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import unicodedata


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def uplus(s: str) -> str:
    return " ".join(f"U+{ord(ch):04X}" for ch in s)


def names(s: str) -> str:
    out: list[str] = []
    for ch in s:
        try:
            out.append(unicodedata.name(ch))
        except ValueError:
            out.append("<no name>")
    return " | ".join(out)


def nfc_equal(a: str, b: str) -> bool:
    return unicodedata.normalize("NFC", a) == unicodedata.normalize("NFC", b)


def fold_equal(a: str, b: str) -> bool:
    return (
        unicodedata.normalize("NFC", a).casefold()
        == unicodedata.normalize("NFC", b).casefold()
    )


def shave_marks(txt: str) -> str:
    norm = unicodedata.normalize("NFD", txt)
    shaved = "".join(c for c in norm if not unicodedata.combining(c))
    return unicodedata.normalize("NFC", shaved)


def demo_combining_characters() -> None:
    section("1) Combining characters: looks same, but different code points")
    s1 = "café"  # precomposed é
    s2 = "cafe\u0301"  # e + COMBINING ACUTE ACCENT
    print("s1:", ascii(s1), "len:", len(s1), "u+:", uplus(s1))
    print("s2:", ascii(s2), "len:", len(s2), "u+:", uplus(s2))
    print("s1 == s2:", s1 == s2)
    print("names(s1):", names(s1))
    print("names(s2):", names(s2))

    nfc1 = unicodedata.normalize("NFC", s1)
    nfc2 = unicodedata.normalize("NFC", s2)
    nfd1 = unicodedata.normalize("NFD", s1)
    nfd2 = unicodedata.normalize("NFD", s2)
    print("NFC lens:", len(nfc1), len(nfc2), "equal:", nfc1 == nfc2)
    print("NFD lens:", len(nfd1), len(nfd2), "equal:", nfd1 == nfd2)


def demo_compatibility_normalization() -> None:
    section("2) Compatibility normalization (NFKC): useful for search, risky for storage")
    samples = {
        "OHM SIGN": "\u2126",  # Ω
        "GREEK OMEGA": "\u03A9",  # Ω
        "MICRO SIGN": "\u00B5",  # µ
        "GREEK MU": "\u03BC",  # μ
        "ONE HALF": "\N{VULGAR FRACTION ONE HALF}",  # ½
    }
    for label, ch in samples.items():
        nfc = unicodedata.normalize("NFC", ch)
        nfkc = unicodedata.normalize("NFKC", ch)
        print(f"{label:10} ch={ascii(ch)} U+{ord(ch):04X} name={unicodedata.name(ch)}")
        print("  NFC :", ascii(nfc), f"U+{ord(nfc):04X}", unicodedata.name(nfc))
        if len(nfkc) == 1:
            print("  NFKC:", ascii(nfkc), f"U+{ord(nfkc):04X}", unicodedata.name(nfkc))
        else:
            print("  NFKC:", ascii(nfkc), "u+:", uplus(nfkc))


def demo_casefold() -> None:
    section("3) casefold(): stronger than lower() for Unicode comparisons")
    a = "Straße"
    b = "strasse"
    print("a:", ascii(a), "casefold:", ascii(a.casefold()))
    print("b:", ascii(b), "casefold:", ascii(b.casefold()))
    print("a == b:", a == b)
    print("fold_equal(a,b):", fold_equal(a, b))


def demo_helpers() -> None:
    section("4) Helper functions: nfc_equal / fold_equal / shave_marks")
    s1 = "café"
    s2 = "cafe\u0301"
    print("raw == :", s1 == s2)
    print("nfc_equal:", nfc_equal(s1, s2))
    print("fold_equal:", fold_equal(s1, s2))

    order = "“Herr Voß: • ½ cup of OEtker™ caffè latte”"
    print("order (ascii-safe):", ascii(order))
    shaved = shave_marks(order)
    print("shave_marks(order):", ascii(shaved))


def main() -> None:
    demo_combining_characters()
    demo_compatibility_normalization()
    demo_casefold()
    demo_helpers()


if __name__ == "__main__":
    main()

