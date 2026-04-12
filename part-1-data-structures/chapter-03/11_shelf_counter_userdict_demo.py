"""
Demo for 11-Counter与shelve及UserDict子类化.md (Fluent Python §3.6 cont.).

Run:
  python part-1-data-structures/chapter-03/11_shelf_counter_userdict_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import shelve
import tempfile
from collections import Counter, UserDict
from pathlib import Path


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_counter() -> None:
    section("1) Counter: from str, update, most_common, + / - / & / |")
    ct = Counter("abracadabra")
    print("Counter('abracadabra'):", ct)
    ct.update("aaaaazzz")
    print("after update('aaaaazzz'):", ct)
    print("most_common(3):", ct.most_common(3))

    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2, c=1)
    print("c1 + c2:", c1 + c2)
    print("c1 - c2:", c1 - c2)
    print("c1 & c2 (min counts):", c1 & c2)
    print("c1 | c2 (max counts):", c1 | c2)


def demo_shelve() -> None:
    section("2) shelve: str keys, pickle values, context manager")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "demo_shelf"
        with shelve.open(str(path)) as db:
            db["user"] = {"name": "Ada", "score": 42}
            db["tags"] = ["python", "mapping"]
            print("stored keys:", list(db.keys()))
            print("db['user']:", db["user"])
            db.sync()


def demo_userdict_update() -> None:
    section("3) UserDict: MutableMapping.update -> __setitem__")

    class UpperKeyDict(UserDict):
        def __setitem__(self, key, value) -> None:
            self.data[str(key).upper()] = value

    m = UpperKeyDict()
    m["a"] = 1
    m.update(b=2, c=3)
    print("after __setitem__ and update:", dict(m))


def main() -> None:
    demo_counter()
    demo_shelve()
    demo_userdict_update()


if __name__ == "__main__":
    main()
