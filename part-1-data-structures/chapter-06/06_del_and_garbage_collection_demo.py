"""
对应笔记：06-del与垃圾回收.md

Run:
  python part-1-data-structures/chapter-06/06_del_and_garbage_collection_demo.py

脚本说明：
- 教学演示：`del` 解绑、GC、弱引用与 finalize；请与笔记对照。
"""

from __future__ import annotations

import gc
import weakref
from dataclasses import dataclass

from ch06_demo_support import safe, section


def demo_del_and_gc_basics() -> None:
    section("12) del removes a name; GC frees objects when unreachable")

    class Tracker:
        def __init__(self, label: str) -> None:
            self.label = label

        def __repr__(self) -> str:
            return f"Tracker({safe(self.label)})"

    obj = Tracker("alive")
    w = weakref.ref(obj)
    print("weakref before del:", w())

    del obj
    gc.collect()
    print("weakref after del + gc.collect():", w())


def demo_weakref_cache_like() -> None:
    section("13) Weak references: cache entries vanish after GC")

    @dataclass(eq=True, frozen=True)
    class Key:
        name: str

    cache: weakref.WeakKeyDictionary[Key, str] = weakref.WeakKeyDictionary()
    k = Key("k1")
    cache[k] = "payload"
    print("cache has k:", k in cache, "| size:", len(cache))

    w = weakref.ref(k)
    del k
    gc.collect()
    print("key weakref after del+gc:", w())
    print("cache size after key collected:", len(cache))


def demo_del_is_unbinding_not_deleting() -> None:
    section("19) del removes a name, not an object (alias keeps it alive)")

    class Box:
        def __init__(self, payload: list[int]) -> None:
            self.payload = payload

        def __repr__(self) -> str:
            return f"Box(payload={self.payload!r})"

    a = Box([1, 2])
    b = a
    w = weakref.ref(a)
    print("weakref before del a:", w())
    del a
    print("after del a -> b:", b)
    print("weakref still alive (because b exists):", w())

    b = Box([3])
    gc.collect()
    print("after rebinding b and gc.collect() -> weakref:", w())


def demo_cycle_and_gc_collect() -> None:
    section("20) Cycle + gc.collect(): unreachable cycles are reclaimed")

    class Node:
        def __init__(self, name: str) -> None:
            self.name = name
            self.other: Node | None = None

        def __repr__(self) -> str:
            return f"Node({safe(self.name)})"

    n1 = Node("n1")
    n2 = Node("n2")
    n1.other = n2
    n2.other = n1

    w1 = weakref.ref(n1)
    w2 = weakref.ref(n2)
    del n1, n2

    collected = gc.collect()
    print("gc.collect() -> collected:", collected)
    print("weakrefs after collect:", w1(), w2())


def demo_weakref_finalize_callback() -> None:
    section("21) weakref.finalize: callback runs when last strong ref is gone")

    calls: list[str] = []

    def bye(label: str) -> None:
        calls.append(label)
        print("finalize callback:", safe(label))

    s1 = {1, 2, 3}
    s2 = s1
    ender = weakref.finalize(s1, bye, "set collected")
    print("ender.alive (start):", ender.alive)
    del s1
    print("ender.alive after del s1:", ender.alive)
    s2 = "spam"
    gc.collect()
    print("ender.alive after dropping s2 + collect:", ender.alive)
    print("calls:", calls)


def main() -> None:
    demo_del_and_gc_basics()
    demo_weakref_cache_like()
    demo_del_is_unbinding_not_deleting()
    demo_cycle_and_gc_collect()
    demo_weakref_finalize_callback()


if __name__ == "__main__":
    main()
