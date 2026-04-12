"""
演示：collections.abc.Sequence 与 register() 虚拟子类。

与 `02-容器序列与扁平序列.md`（ABC / 虚拟子类）配套。

运行：python part-1-data-structures/chapter-02/sequence_virtual_subclass_demo.py
"""

from __future__ import annotations

from collections import abc


class MyListSequence:
    """最小序列：只实现 __len__ / __getitem__（委托给 list）。"""

    def __init__(self, items: list) -> None:
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int):
        return self._items[index]


def main() -> None:
    x = MyListSequence([10, 20, 30])

    print("before register:")
    print(f"  isinstance(x, abc.Sequence) -> {isinstance(x, abc.Sequence)}")
    print(f"  MyListSequence.__bases__ -> {MyListSequence.__bases__}")

    abc.Sequence.register(MyListSequence)

    print("after abc.Sequence.register(MyListSequence):")
    print(f"  isinstance(x, abc.Sequence) -> {isinstance(x, abc.Sequence)}")
    print(f"  MyListSequence.__bases__ -> {MyListSequence.__bases__}  # still no explicit subclass of Sequence")

    print("\nbuiltins (virtual subclass, registered in CPython):")
    print(f"  list.__bases__ -> {list.__bases__}")
    print(f"  isinstance([1], abc.MutableSequence) -> {isinstance([1], abc.MutableSequence)}")


if __name__ == "__main__":
    main()
