"""
Demo for 07-序列拼接重复与嵌套列表陷阱.md

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


def demo_weird_board_outer_mul() -> None:
    section("4) wrong: (['_']*3) repeated by outer *3 - same row object")
    weird = [["_"] * 3] * 3
    print("weird rows same object?", weird[0] is weird[1] is weird[2])
    assert weird[0] is weird[1] is weird[2]
    weird[1][2] = "O"
    print("after weird[1][2] = 'O':", weird)
    assert weird == [
        ["_", "_", "O"],
        ["_", "_", "O"],
        ["_", "_", "O"],
    ]


def demo_append_same_row_loop() -> None:
    section("5) wrong: append the same row in a loop")
    row = ["_"] * 3
    bad: list[list[str]] = []
    for _ in range(3):
        bad.append(row)
    print("bad[0] is bad[1]?", bad[0] is bad[1])
    assert bad[0] is bad[1] is bad[2]
    bad[0][0] = "!"
    print("after bad[0][0] = '!':", bad)


def demo_row_copy_ok() -> None:
    section("6) ok: row.copy() each iteration")
    row = ["_"] * 3
    ok = [row.copy() for _ in range(3)]
    ok[1][2] = "X"
    print(ok)
    assert ok[0][2] == "_" and ok[1][2] == "X"


def main() -> None:
    demo_plus_and_mul_create_new_outer_objects()
    demo_nested_list_trap()
    demo_correct_board_init()
    demo_weird_board_outer_mul()
    demo_append_same_row_loop()
    demo_row_copy_ok()


if __name__ == "__main__":
    main()

