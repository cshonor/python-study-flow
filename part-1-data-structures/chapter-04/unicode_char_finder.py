"""
Unicode character finder (similar spirit to Fluent Python's cf.py).

Usage:
  python part-1-data-structures/chapter-04/unicode_char_finder.py CAT EYES
  python part-1-data-structures/chapter-04/unicode_char_finder.py BLACK QUEEN --limit 20

Notes:
- This scans all Unicode code points (0x0000..0x10FFFF), skipping surrogate range.
- Output uses ascii() for safe printing on Windows consoles.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata


START = 0x0000
END = 0x110000  # exclusive
SURROGATE_START = 0xD800
SURROGATE_END = 0xE000  # exclusive


def iter_named_chars():
    for cp in range(START, END):
        if SURROGATE_START <= cp < SURROGATE_END:
            continue
        ch = chr(cp)
        try:
            nm = unicodedata.name(ch)
        except ValueError:
            continue
        yield cp, ch, nm


def match_all_words(name: str, query_words: set[str]) -> bool:
    # name is already uppercase words with spaces
    words = set(name.split())
    return query_words.issubset(words)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("words", nargs="+", help="Unicode name keywords (case-insensitive)")
    ap.add_argument("--limit", type=int, default=100, help="Max results to print (default: 100)")
    args = ap.parse_args(argv)

    query_words = {w.upper() for w in args.words if w.strip()}
    if not query_words:
        ap.print_help()
        return 2

    printed = 0
    for cp, ch, nm in iter_named_chars():
        # nm is typically already uppercase, but normalize anyway
        if match_all_words(nm.upper(), query_words):
            print(f"U+{cp:04X} {ascii(ch)} {nm}")
            printed += 1
            if printed >= args.limit:
                break

    if printed == 0:
        print("No matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

