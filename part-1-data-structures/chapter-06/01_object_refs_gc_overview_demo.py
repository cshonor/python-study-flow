"""
对应笔记：01-第6章对象引用可变性与GC总览.md

本章演示已按小节拆成独立脚本（见下方列表），便于与 02–07 各篇笔记一一对应运行。

Run（仓库根目录）：
  python part-1-data-structures/chapter-06/02_variable_not_a_box_demo.py
  python part-1-data-structures/chapter-06/03_identity_equality_aliasing_demo.py
  …（其余见 main() 输出）

脚本说明：
- 教学演示：本文件只做「导航」；具体证据输出在对应编号的脚本里。
"""

from __future__ import annotations

import sys

from ch06_demo_support import section


def main() -> None:
    print("Python:", sys.version.split()[0])
    section("第 6 章：与笔记编号对应的演示脚本")
    scripts = [
        ("01", "01_object_refs_gc_overview_demo.py", "总览 / 导航（本文件）"),
        ("02", "02_variable_not_a_box_demo.py", "变量是标签、Gizmo"),
        ("03", "03_identity_equality_aliasing_demo.py", "同一性、相等、别名、元组相对不可变"),
        ("04", "04_shallow_copy_and_deepcopy_demo.py", "浅拷贝 / 深拷贝 / Bus"),
        ("05", "05_call_by_sharing_mutable_defaults_demo.py", "共享传参、可变默认、HauntedBus/TwilightBus"),
        ("06", "06_del_and_garbage_collection_demo.py", "del、GC、弱引用"),
        ("07", "07_immutable_type_tricks_demo.py", "不可变技巧、驻留提示"),
    ]
    for num, fname, desc in scripts:
        cmd = f"python part-1-data-structures/chapter-06/{fname}"
        print(f"  {num}  {cmd}")
        print(f"      {desc}")


if __name__ == "__main__":
    main()
