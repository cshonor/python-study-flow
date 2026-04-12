"""
Demo for 08-11.11 使用 __slots__ 节省空间：为什么省、怎么用、怎么继承.md.

Small-scale memory comparison using tracemalloc.
This is not a microbenchmark; it just makes the "dict vs slots" difference visible.
"""

from __future__ import annotations

import gc
import tracemalloc


class PlainPoint:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class SlottedPoint:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


def allocated_bytes_for(cls, n: int) -> int:
    gc.collect()
    tracemalloc.start()
    before = tracemalloc.take_snapshot()
    objs = [cls(i * 0.5, i * 1.5) for i in range(n)]
    after = tracemalloc.take_snapshot()
    # keep objs alive until after snapshot
    _ = objs[-1]
    stats = after.compare_to(before, "filename")
    total = sum(s.size_diff for s in stats)
    tracemalloc.stop()
    return total


def main() -> None:
    n = 200_000
    plain = allocated_bytes_for(PlainPoint, n)
    slotted = allocated_bytes_for(SlottedPoint, n)

    print("N =", n)
    print("PlainPoint allocated (bytes)  ->", plain)
    print("SlottedPoint allocated (bytes)->", slotted)
    if slotted > 0:
        print("ratio plain/slotted ->", round(plain / slotted, 2))


if __name__ == "__main__":
    main()

