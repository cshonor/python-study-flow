"""
Demo for 08-Unicode文本排序.md

Run:
  python part-1-data-structures/chapter-04/08_unicode_sorting_demo.py

This demo tries three strategies:
1) Default sorted() (code point order)
2) locale.strxfrm (if locale is available on this OS)
3) pyuca (if installed)

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import locale
from typing import Callable


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def safe(obj: object) -> str:
    """
    Make output safe on Windows consoles with non-UTF encodings.
    """
    if isinstance(obj, str):
        return ascii(obj)
    return ascii(obj)


def try_locale_sort_key(locale_name: str) -> Callable[[str], str] | None:
    """
    Try to set LC_COLLATE and return locale.strxfrm.
    Returns None if the locale is unavailable.
    """

    try:
        locale.setlocale(locale.LC_COLLATE, locale_name)
    except locale.Error:
        return None
    return locale.strxfrm


def try_pyuca_sort_key() -> Callable[[str], object] | None:
    try:
        import pyuca  # type: ignore
    except Exception:
        return None
    coll = pyuca.Collator()
    return coll.sort_key


def main() -> None:
    fruits = ["caju", "atemoia", "cajá", "açaí", "acerola"]

    section("1) Default sorted() (code point order)")
    print(safe(sorted(fruits)))

    section("2) locale.strxfrm (depends on OS locale)")
    # A few common names across platforms; Windows often uses different names.
    candidates = [
        "pt_BR.UTF-8",
        "pt_BR.utf8",
        "Portuguese_Brazil.1252",
        "Portuguese_Brazil",
    ]
    key = None
    picked = None
    for name in candidates:
        key = try_locale_sort_key(name)
        if key is not None:
            picked = name
            break
    if key is None:
        print("locale not available on this system for candidates:", candidates)
    else:
        print("using locale:", picked)
        print(safe(sorted(fruits, key=key)))

    section("3) pyuca (UCA, cross-platform) if installed")
    pyuca_key = try_pyuca_sort_key()
    if pyuca_key is None:
        print("pyuca not installed. Install with: pip install pyuca")
    else:
        print(safe(sorted(fruits, key=pyuca_key)))


if __name__ == "__main__":
    main()

