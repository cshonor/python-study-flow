"""Ch. 17.10-17.11: reduction functions + yield from delegation demos."""

from __future__ import annotations

import itertools
from functools import reduce


def noisy_bools(values: list[bool], label: str):
    for i, v in enumerate(values):
        print(f"{label}: yield[{i}] -> {v}")
        yield v


def demo_all_any_short_circuit() -> None:
    print("== all/any short-circuit ==")
    print("-- all: stops at first False --")
    res_all = all(noisy_bools([True, True, False, True], "all"))
    print("all(...) ->", res_all)
    print()

    print("-- any: stops at first True --")
    res_any = any(noisy_bools([False, False, True, False], "any"))
    print("any(...) ->", res_any)
    print()


def demo_reduce() -> None:
    print("== functools.reduce ==")
    nums = [1, 2, 3, 4]
    print("reduce(add, [1,2,3,4]) ->", reduce(lambda a, b: a + b, nums))
    print("reduce(mul, [1,2,3,4]) ->", reduce(lambda a, b: a * b, nums))
    print()


def chain_yield_from(*iterables):
    for it in iterables:
        yield from it


def demo_yield_from_chain() -> None:
    print("== yield from: chain ==")
    out = list(chain_yield_from("ABC", range(3), ["x", "y"]))
    print("chain_yield_from(...) ->", out)
    print()


def subgen_with_return():
    yield 1
    yield 2
    return "SUBGEN-RETURN-VALUE"


def delegating_gen():
    yield "start"
    rv = yield from subgen_with_return()
    yield f"subgen returned: {rv!r}"
    yield "end"


def demo_yield_from_return_value() -> None:
    print("== yield from: capture subgenerator return value ==")
    print(list(delegating_gen()))
    print()


def tree(cls, level: int = 0):
    yield (cls.__name__, level)
    for sub in cls.__subclasses__():
        yield from tree(sub, level + 1)


def demo_yield_from_tree() -> None:
    print("== yield from: recursive tree traversal (truncated) ==")
    for name, level in itertools.islice(tree(BaseException), 20):
        print(" " * 2 * level + name)
    print("... (truncated)")
    print()


def main() -> None:
    demo_all_any_short_circuit()
    demo_reduce()
    demo_yield_from_chain()
    demo_yield_from_return_value()
    demo_yield_from_tree()


if __name__ == "__main__":
    main()

