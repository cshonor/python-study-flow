"""
Demo for 06-编解码问题排查与修复.md

Run:
  python part-1-data-structures/chapter-04/06_encoding_decoding_fixes_demo.py

Notes:
- Output uses ascii()/hex to avoid Windows console encoding issues.

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_encode_error_and_errors_param() -> None:
    section("1) UnicodeEncodeError: str -> bytes, and errors= strategies")
    city = "São Paulo"
    print("city (ascii-safe):", ascii(city))
    for enc in ("utf-8", "utf-16", "iso8859_1", "cp437"):
        try:
            out = city.encode(enc, errors="strict")
            print(f"encode {enc!r}: ok  hex={out.hex(' ')}")
        except UnicodeEncodeError as e:
            print(f"encode {enc!r}: UnicodeEncodeError:", e)

    # Show errors= on a restrictive codec (cp437 may vary by platform, but in many cases it fails on 'ã')
    for policy in ("ignore", "replace", "xmlcharrefreplace", "backslashreplace"):
        out = city.encode("cp437", errors=policy)
        print(f"errors={policy!r}:", out, "| hex:", out.hex(" "))


def demo_decode_error_vs_mojibake() -> None:
    section("2) UnicodeDecodeError vs 'no error but mojibake'")
    octets = b"Montr\xe9al"  # latin-1/cp1252 bytes for Montréal
    print("octets:", octets, "| hex:", octets.hex(" "))
    print("decode cp1252:", ascii(octets.decode("cp1252")))
    print("decode koi8_r (wrong, but no error):", ascii(octets.decode("koi8_r")))
    try:
        octets.decode("utf-8", errors="strict")
    except UnicodeDecodeError as e:
        print("decode utf-8 -> UnicodeDecodeError:", e)
    print("decode utf-8 errors='replace':", ascii(octets.decode("utf-8", errors="replace")))


def demo_bom_utf8_sig_and_utf16() -> None:
    section("3) BOM: utf-8-sig, utf-16, utf-32 head bytes")
    text = "hello"
    b_utf8 = text.encode("utf-8")
    b_sig = text.encode("utf-8-sig")
    b_u16 = text.encode("utf-16")  # includes BOM
    print("utf-8     hex:", b_utf8.hex(" "))
    print("utf-8-sig hex:", b_sig.hex(" "), "(starts with EF BB BF)")
    print("utf-16    hex:", b_u16.hex(" "), "(starts with FF FE or FE FF)")

    b_u32 = text.encode("utf-32")
    print("utf-32    hex:", b_u32.hex(" "), "(starts with FF FE 00 00 LE or 00 00 FE FF BE)")

    # Demonstrate how utf-8-sig strips BOM on decode
    decoded_sig = b_sig.decode("utf-8-sig")
    decoded_plain = b_sig.decode("utf-8", errors="strict")
    print("decode utf-8-sig:", ascii(decoded_sig))
    print("decode utf-8     :", ascii(decoded_plain), "(BOM becomes U+FEFF at start)")
    assert decoded_sig == text


def demo_optional_encoding_detection() -> None:
    section("4) Optional: chardet / charset-normalizer (pip install chardet)")
    sample = "你好，世界。这是一段用来测试编码检测的中文。".encode("gbk")
    print("sample hex head:", sample[:16].hex(" "), "...")

    try:
        import chardet
    except ImportError:
        print("chardet: not installed (python -m pip install chardet)")
    else:
        d = chardet.detect(sample)
        print("chardet.detect:", ascii(d))

    try:
        import charset_normalizer as cn
    except ImportError:
        print("charset-normalizer: not installed (python -m pip install charset-normalizer)")
    else:
        print("charset_normalizer.detect:", ascii(cn.detect(sample)))


def demo_source_file_syntaxerror_non_utf8() -> None:
    section("5) SyntaxError: running a non-UTF-8 .py without coding cookie")
    # Write a Python file in cp1252 that contains a non-ASCII literal, but without coding declaration.
    code = "print('Olá, Mundo!')\n"
    raw_cp1252 = code.encode("cp1252")  # contains 0xE1 for á
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "bad_encoding.py"
        p.write_bytes(raw_cp1252)

        cp = subprocess.run(
            [sys.executable, str(p)],
            capture_output=True,
            text=False,
        )
        # stderr is bytes; show safely
        err = cp.stderr.decode("utf-8", errors="replace")
        out = cp.stdout.decode("utf-8", errors="replace")
        print("returncode:", cp.returncode)
        print("stdout (utf-8 replace):", ascii(out))
        print("stderr (utf-8 replace):", ascii(err))


def main() -> None:
    demo_encode_error_and_errors_param()
    demo_decode_error_vs_mojibake()
    demo_bom_utf8_sig_and_utf16()
    demo_optional_encoding_detection()
    demo_source_file_syntaxerror_non_utf8()


if __name__ == "__main__":
    main()

