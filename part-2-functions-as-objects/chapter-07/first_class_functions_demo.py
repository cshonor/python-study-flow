"""
Demo for 01-functions-as-first-class-objects-overview.md

Run from repo root:
  python part-2-functions-as-objects/chapter-07/first_class_functions_demo.py
"""


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def factorial(n: int) -> int:
    return 1 if n < 2 else n * factorial(n - 1)


def demo_assign_and_identity() -> None:
    section("1) Function object: assign alias, same behavior")
    f = factorial
    print("f is factorial:", f is factorial)
    print("f(5), factorial(5):", f(5), factorial(5))
    print("type(factorial):", type(factorial))


def demo_container_of_callables() -> None:
    section("2) Store callables in a list")
    registry: list[tuple[object, tuple[object, ...]]] = [
        (len, ("hello",)),
        (str.lower, ("ABC",)),
        (factorial, (5,)),
    ]
    for fn, args in registry:
        out = fn(*args)  # type: ignore[operator]
        print(fn.__name__, "->", out)


def demo_higher_order_sorted() -> None:
    section("3) Pass function as argument (sorted key=)")
    fruits = ["strawberry", "fig", "apple", "cherry"]
    print("by len:", sorted(fruits, key=len))


def make_pow(n: int):
    return lambda x: x**n


def demo_return_callable() -> None:
    section("4) Return a function (factory + lambda)")
    square = make_pow(2)
    cube = make_pow(3)
    print("square(3), cube(2):", square(3), cube(2))


class Multiplier:
    def __init__(self, factor: int) -> None:
        self.factor = factor

    def __call__(self, x: int) -> int:
        return self.factor * x


def demo_callable_instance() -> None:
    section("5) User-defined callable (__call__)")
    triple = Multiplier(3)
    print("triple(4):", triple(4))
    print("callable(triple):", callable(triple))


def main() -> None:
    demo_assign_and_identity()
    demo_container_of_callables()
    demo_higher_order_sorted()
    demo_return_callable()
    demo_callable_instance()


if __name__ == "__main__":
    main()
