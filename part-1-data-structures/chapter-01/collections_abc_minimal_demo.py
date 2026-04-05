"""
最小示例：__len__ + __getitem__（+ __contains__）与 collections.abc 的 isinstance 对比。

要点：即使没有 __iter__，for 仍可能通过「下标 0,1,2…」协议工作；这与 Iterable ABC 的
isinstance 检测不是同一件事。部分 ABC 也可用 register() 显式登记虚拟子类。

对应笔记：12-collections-abc-container-api.md
"""

from __future__ import annotations

from collections import abc


class MiniSeq:
    """不继承任何 ABC：长度 + 下标 + 成员检测。"""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def __contains__(self, item) -> bool:
        return item in self._items


def main() -> None:
    m = MiniSeq([10, 20, 30])

    print("1) 实际用法（鸭子类型，看行为）")
    print("   len(m) =", len(m))
    print("   list(m) =", list(m))
    print("   20 in m =", 20 in m)

    checks = [
        ("Sized", abc.Sized),
        ("Iterable", abc.Iterable),
        ("Container", abc.Container),
        ("Collection", abc.Collection),
        ("Sequence", abc.Sequence),
        ("Reversible", abc.Reversible),
    ]
    print("\n2) isinstance（未 register 时，以你本机 CPython 为准）")
    for name, cls in checks:
        print(f"   {name:12} -> {isinstance(m, cls)}")

    abc.Sequence.register(MiniSeq)
    print("\n3) 执行 Sequence.register(MiniSeq) 之后")
    print(f"   Sequence     -> {isinstance(m, abc.Sequence)}")
    print(f"   Iterable     -> {isinstance(m, abc.Iterable)}")
    print(f"   Collection   -> {isinstance(m, abc.Collection)}")


if __name__ == "__main__":
    main()
