"""
Demo for 03-IO编码排查清单.md (Fluent Python ch.4).

Run:
  python part-1-data-structures/chapter-04/03_io_encoding_troubleshoot_demo.py

This demo is designed to run on Windows consoles whose stdout encoding may be GBK.
We therefore use ascii() and hex output to avoid UnicodeEncodeError during printing.

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


def hexdump(b: bytes, n: int = 64) -> str:
    return b[:n].hex(" ")


def demo_types_boundary() -> None:
    section("1) First question: str or bytes?")
    s = "北京"
    b = s.encode("utf-8")
    print("type(s):", type(s), "ascii(s):", ascii(s))
    print("type(b):", type(b), "hexdump(b):", hexdump(b))


def demo_file_io_encoding() -> None:
    section("2) File I/O: explicit encoding beats defaults")
    text = "café 北京"

    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "demo_utf8.txt"
        p.write_text(text, encoding="utf-8")
        raw = p.read_bytes()
        print("written as utf-8, raw head:", hexdump(raw))

        ok = p.read_text(encoding="utf-8")
        print("read_text utf-8 ->", ascii(ok))

        try:
            wrong = p.read_text(encoding="gbk")
            print("read_text gbk (wrong) ->", ascii(wrong))
        except UnicodeDecodeError as e:
            print("read_text gbk -> UnicodeDecodeError:", e)


def demo_errors_policy_decode() -> None:
    section("3) errors= strict / replace / ignore (decode)")
    bad = b"\xff\xfe\x00"
    for policy in ("strict", "replace", "ignore"):
        try:
            out = bad.decode("utf-8", errors=policy)
            print(f"errors={policy!r}:", "ascii(out)=", ascii(out))
        except UnicodeDecodeError as e:
            print(f"errors={policy!r}: UnicodeDecodeError:", e)


def demo_subprocess_text() -> None:
    section("4) Subprocess: text=True + encoding= avoids manual decode")
    # Force the child Python process to emit UTF-8, regardless of Windows console code page.
    cp = subprocess.run(
        [sys.executable, "-X", "utf8", "-c", "print('北京')"],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    print("stdout ascii:", ascii(cp.stdout))


def demo_console_boundary() -> None:
    section("5) Console boundary (stdout encoding)")
    print("sys.getdefaultencoding():", sys.getdefaultencoding())
    print("sys.stdout.encoding:", sys.stdout.encoding)
    print("sys.stdout.errors:", sys.stdout.errors)
    s = "café 北京"
    print("safe via ascii(s):", ascii(s))
    # Avoid printing s directly: it may show mojibake or raise UnicodeEncodeError.


def main() -> None:
    demo_types_boundary()
    demo_file_io_encoding()
    demo_errors_policy_decode()
    demo_subprocess_text()
    demo_console_boundary()


if __name__ == "__main__":
    main()

