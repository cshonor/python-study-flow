"""
Demo for 06-切片与slice对象.md

Run:
  python part-1-data-structures/chapter-02/slicing_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_half_open() -> None:
    section("1) half-open slices: [start:stop)")
    l = [10, 20, 30, 40, 50, 60]
    print("l:", l)
    print("l[:2]:", l[:2])
    print("l[2:]:", l[2:])
    assert l[:2] == [10, 20]
    assert l[2:] == [30, 40, 50, 60]
    assert len(l[:2]) == 2
    assert len(l[2:]) == 4


def demo_stride_and_reverse() -> None:
    section("2) stride and reverse")
    s = "bicycle"
    print("s:", s)
    print("s[::3] :", s[::3])
    print("s[::-1]:", s[::-1])
    print("s[::-2]:", s[::-2])
    assert s[::3] == "bye"
    assert s[::-1] == "elcycib"
    assert s[::-2] == "eccb"


def demo_named_slice_objects() -> None:
    section("3) slice objects: naming and reuse")
    SKU = slice(0, 6)
    DESCRIPTION = slice(6, 40)
    UNIT_PRICE = slice(40, 52)

    line = "123456" + "BANANA".ljust(34) + f"{12.50:>12.2f}"
    sku = line[SKU]
    desc = line[DESCRIPTION].rstrip()
    price = float(line[UNIT_PRICE])
    print("sku :", sku)
    print("desc:", desc)
    print("price:", price)
    assert sku == "123456"
    assert desc == "BANANA"
    assert price == 12.50


def demo_slice_assignment_and_del() -> None:
    section("4) slice assignment and del (in-place list edits)")
    l = list(range(10))
    print("start:", l)
    l[2:5] = [20, 30]
    print("replace [2:5] with [20,30]:", l)
    assert l == [0, 1, 20, 30, 5, 6, 7, 8, 9]

    l[2:2] = [111, 222]  # insert at index 2
    print("insert at [2:2]:", l)
    assert l[:4] == [0, 1, 111, 222]

    del l[5:7]
    print("del [5:7]:", l)

    # Right-hand side must be iterable
    try:
        l[0:1] = 100  # type: ignore[assignment]
        raise AssertionError("Expected TypeError for non-iterable RHS")
    except TypeError:
        print("RHS must be iterable (expected TypeError)")


def demo_extended_slice_assignment() -> None:
    section("5) extended slice assignment: step requires matching length")
    l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    l[3::2] = [11, 22, 33, 44]
    print("l after l[3::2] = [11,22,33,44]:", l)
    assert l == [0, 1, 2, 11, 4, 22, 6, 33, 8, 44]

    try:
        l[::2] = [1, 2]  # wrong length
        raise AssertionError("Expected ValueError for wrong-length extended slice")
    except ValueError:
        print("extended slice assignment length must match (expected ValueError)")


def demo_ellipsis_object() -> None:
    section("6) Ellipsis (...) object")
    print("Ellipsis is ...:", Ellipsis is ...)
    print("type(...):", type(...))
    # In practice this matters for multi-dimensional containers (e.g. numpy arrays).


def main() -> None:
    demo_half_open()
    demo_stride_and_reverse()
    demo_named_slice_objects()
    demo_slice_assignment_and_del()
    demo_extended_slice_assignment()
    demo_ellipsis_object()


if __name__ == "__main__":
    main()

