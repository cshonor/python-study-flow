"""
粗略对比 list 与 array.array 的 sys.getsizeof（CPython）。

注意：getsizeof(list) 不含每个元素对象；list 存 float 时每个元素常是独立 PyFloat。
详见：02-容器序列与扁平序列.md 第 5 节。

运行：python part-1-data-structures/chapter-02/container_vs_flat_memory_demo.py
"""

from __future__ import annotations

import sys
from array import array


def main() -> None:
    n = 50_000
    values = [1.0] * n

    lst = list(values)
    arr = array("d", values)

    print(f"n = {n}")
    print("sys.getsizeof（仅对象自身头部/缓冲区，含义不同，勿跨类型硬比绝对值）")
    print(f"  list:         {sys.getsizeof(lst):>10}")
    print(f"  array('d'):   {sys.getsizeof(arr):>10}")
    if lst:
        print(f"  单个 PyFloat: {sys.getsizeof(lst[0]):>10}（list 每个元素常指向此类对象）")

    # 粗略：list 侧元素对象规模量级（n 次 float 对象）
    approx_floats = n * sys.getsizeof(lst[0]) if lst else 0
    print("\n粗略量级（把 list 每个元素当成独立 float 对象相加，仅作直觉：）")
    print(f"  list 元素对象约: {approx_floats:>12} + list 壳 {sys.getsizeof(lst)}")
    print(f"  array 单缓冲约:  {sys.getsizeof(arr):>12}（同构紧排）")


if __name__ == "__main__":
    main()
