"""
Demo for 10-sequence-plus-mul-and-nested-list-trap.md

Run:
  python part-1-data-structures/chapter-02/sequence_plus_mul_and_nested_list_trap_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_plus_and_mul_create_new_outer_objects() -> None:
    section("1) + and * create new outer objects")
    a = [1, 2]
    b = [3, 4]
    c = a + b
    print("a:", a, "id:", id(a))
    print("b:", b, "id:", id(b))
    print("c = a + b:", c, "id:", id(c))
    assert c == [1, 2, 3, 4]
    assert c is not a and c is not b

    s = "ab"
    t = s * 3
    print("s:", s, "-> t:", t)
    assert t == "ababab"


def demo_nested_list_trap() -> None:
    section("2) nested list trap: [[]] * n shares the same list")
    board = [[]] * 3
    print("board:", board)
    print("board[0] is board[1] is board[2] ->", board[0] is board[1] is board[2])
    assert board[0] is board[1] is board[2]

    board[0].append("x")
    print("after board[0].append('x'):", board)
    assert board == [["x"], ["x"], ["x"]]


def demo_correct_board_init() -> None:
    section("3) correct: listcomp creates independent rows")
    board = [["_"] * 3 for _ in range(3)]
    print("start:", board)
    board[1][2] = "X"
    print("after board[1][2] = 'X':", board)
    assert board == [["_", "_", "_"], ["_", "_", "X"], ["_", "_", "_"]]
    assert board[0] is not board[1] and board[1] is not board[2]


def main() -> None:
    demo_plus_and_mul_create_new_outer_objects()
    demo_nested_list_trap()
    demo_correct_board_init()


if __name__ == "__main__":
    main()

