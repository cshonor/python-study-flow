"""Ch. 17.7: generator expressions vs generator functions; iterator vs generator."""

from __future__ import annotations

from collections.abc import Iterator


def squares_genexpr(n: int):
    return (x * x for x in range(1, n + 1))


def squares_genfunc(n: int):
    for x in range(1, n + 1):
        yield x * x


class CountDown(Iterator[int]):
    """Manual iterator: explicit __next__ and state."""

    def __init__(self, start: int) -> None:
        self._cur = start

    def __iter__(self) -> "CountDown":
        return self

    def __next__(self) -> int:
        if self._cur <= 0:
            raise StopIteration
        value = self._cur
        self._cur -= 1
        return value


def countdown_gen(start: int):
    """Generator version of CountDown."""

    for x in range(start, 0, -1):
        yield x


def main() -> None:
    print("== generator expression vs generator function ==")
    print("genexpr ->", list(squares_genexpr(5)))
    print("genfunc ->", list(squares_genfunc(5)))
    print()

    print("== generators are one-shot iterators ==")
    g = squares_genexpr(3)
    print("list #1 ->", list(g))
    print("list #2 ->", list(g), "(exhausted)")
    print()

    print("== iterator class vs generator ==")
    it = CountDown(3)
    print("CountDown ->", list(it))
    print("CountDown again ->", list(it), "(exhausted)")
    print("countdown_gen ->", list(countdown_gen(3)))
    print()

    print("== generator expression parentheses gotcha ==")

    def f(a, b) -> tuple[int, int]:
        return a, b

    # When not the sole argument, the generator expression must be parenthesized.
    pair = f(1, next((x for x in range(10) if x > 3)))
    print("ok ->", pair)


if __name__ == "__main__":
    main()

