"""
Demo for 12-17.12 泛型可迭代类型.md (Fluent Python 17.12)

Run from repo root:
  python part-4-control-flow/chapter-17/12_generic_iterable_types_demo.py

Optional:
  python -m mypy part-4-control-flow/chapter-17/12_generic_iterable_types_demo.py
"""

from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator, Sequence


def total_length(lines: Iterable[str]) -> int:
    """只遍历：入参用最宽的 Iterable。"""
    return sum(len(line) for line in lines)


def second_item(items: Sequence[str]) -> str:
    """需要下标：入参用 Sequence。"""
    return items[1]


def count_up(n: int) -> Generator[int, None, None]:
    """不 send：Generator 的第二类型参数写 None。"""
    for i in range(n):
        yield i


def as_lines(it: Iterator[str]) -> list[str]:
    """把一次性迭代器物化成 list。"""
    return list(it)


def main() -> None:
    print("total_length:", total_length(["aa", "bbb"]))
    print("second_item:", second_item(("x", "y", "z")))
    gen = count_up(3)
    print("count_up:", list(gen))
    it = iter(["once", "twice"])
    print("as_lines:", as_lines(it))


if __name__ == "__main__":
    main()
