"""
Demo for 03-higher-order-functions.md (Fluent Python 7.3)

Run from repo root:
  python part-2-functions-as-objects/chapter-07/higher_order_functions_demo.py
"""

from __future__ import annotations

from functools import reduce
from operator import add


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def factorial(n: int) -> int:
    """returns n!"""
    return 1 if n < 2 else n * factorial(n - 1)


def reverse_word(word: str) -> str:
    return word[::-1]


def demo_sorted_key_examples() -> None:
    section("Ex 7-3 / 7-4: sorted(..., key=...)")
    fruits = [
        "strawberry",
        "fig",
        "apple",
        "cherry",
        "raspberry",
        "banana",
    ]
    by_len = sorted(fruits, key=len)
    by_rev = sorted(fruits, key=reverse_word)
    print("by len:", by_len)
    print("by reverse spelling:", by_rev)


def demo_map_filter_vs_comprehension() -> None:
    section("Ex 7-5: map/filter vs list comprehension")
    m = list(map(factorial, range(6)))
    c = [factorial(n) for n in range(6)]
    print("list(map(factorial, range(6))):", m)
    print("[factorial(n) for n in range(6)]:", c)

    odd_map = list(map(factorial, filter(lambda n: n % 2, range(6))))
    odd_comp = [factorial(n) for n in range(6) if n % 2]
    print("map+filter (odd n):", odd_map)
    print("comprehension (odd n):", odd_comp)


def demo_reduce_vs_sum() -> None:
    section("Ex 7-6: functools.reduce vs sum")
    r = reduce(add, range(100))
    s = sum(range(100))
    print("reduce(add, range(100)):", r)
    print("sum(range(100)):", s)


def demo_all_any() -> None:
    section("all() / any()")
    print("all([1, 2, 3]):", all([1, 2, 3]))
    print("all([1, 0, 3]):", all([1, 0, 3]))
    print("all([]):", all([]))
    print("any([0, 0, 1]):", any([0, 0, 1]))
    print("any([0, 0, 0]):", any([0, 0, 0]))
    print("any([]):", any([]))


def main() -> None:
    demo_sorted_key_examples()
    demo_map_filter_vs_comprehension()
    demo_reduce_vs_sum()
    demo_all_any()


if __name__ == "__main__":
    main()
