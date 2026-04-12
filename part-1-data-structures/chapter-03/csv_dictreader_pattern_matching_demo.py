"""
Demo for 04-csv-DictReader与match-case.md

Requires Python 3.10+ for match/case (PEP 634).

Run:
  python part-1-data-structures/chapter-03/csv_dictreader_pattern_matching_demo.py
"""

from __future__ import annotations

import csv
import sys
from io import StringIO


SAMPLE_CSV = """type,id,note
user,42,alice
order,7,book
user,150,vip
other,0,skip
"""


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def process_rows_match(rows: csv.DictReader) -> None:
    for row in rows:
        match row:
            case {"type": "user", "id": sid} if sid.isdigit() and int(sid) > 100:
                print("  VIP user (id>100):", sid, row.get("note", ""))
            case {"type": "user", "id": user_id}:
                print("  user:", user_id, row.get("note", ""))
            case {"type": "order", "id": order_id}:
                print("  order:", order_id, row.get("note", ""))
            case _:
                print("  unknown row:", row)


def process_rows_if(rows: csv.DictReader) -> None:
    for row in rows:
        t = row.get("type")
        sid = row.get("id")
        if t == "user" and sid is not None and sid.isdigit() and int(sid) > 100:
            print("  VIP user (id>100):", sid, row.get("note", ""))
        elif t == "user" and "id" in row:
            print("  user:", row["id"], row.get("note", ""))
        elif t == "order" and "id" in row:
            print("  order:", row["id"], row.get("note", ""))
        else:
            print("  unknown row:", row)


def main() -> None:
    section("1) csv.DictReader + match/case (3.10+)")
    if sys.version_info < (3, 10):
        print("Need Python 3.10+ for match/case; skipping.")
        return
    f = StringIO(SAMPLE_CSV)
    process_rows_match(csv.DictReader(f))

    section("2) equivalent if/elif (any supported Python 3.x)")
    f2 = StringIO(SAMPLE_CSV)
    process_rows_if(csv.DictReader(f2))


if __name__ == "__main__":
    main()
