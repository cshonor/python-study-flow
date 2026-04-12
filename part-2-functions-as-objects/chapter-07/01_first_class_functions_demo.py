"""
Demos for chapter 7 notes:
  - 01-第 7 章开篇：函数作为「一等对象」是什么意思.md
  - 02-示例 7-1 7-2：函数是对象、可赋值、可传给 map（高阶函数）.md

Run from repo root:
  python part-2-functions-as-objects/chapter-07/01_first_class_functions_demo.py
"""


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def factorial(n: int) -> int:
    """returns n!"""
    return 1 if n < 2 else n * factorial(n - 1)


def demo_example_7_1_function_as_object() -> None:
    section("Ex 7-1: function object has __doc__, type, __class__")
    print("factorial.__doc__:", repr(factorial.__doc__))
    print("type(factorial):", type(factorial))
    print("factorial.__class__:", factorial.__class__)
    print("type(factorial) is factorial.__class__:", type(factorial) is factorial.__class__)


def demo_example_7_2_assign_and_map() -> None:
    section("Ex 7-2: alias + map(factorial, range(11))")
    fact = factorial
    print("fact is factorial:", fact is factorial)
    print("fact(5):", fact(5))
    mapped = list(map(factorial, range(11)))
    print("list(map(factorial, range(11))):", mapped)


def annotated_sample(a: int, b: str = "x") -> bool:
    """sample for __annotations__ / __defaults__"""
    return True


def demo_common_function_attributes() -> None:
    section("Function attrs: __name__, __defaults__, __annotations__, __code__")
    print("factorial.__name__:", factorial.__name__)
    print("annotated_sample.__defaults__:", annotated_sample.__defaults__)
    print("annotated_sample.__kwdefaults__:", annotated_sample.__kwdefaults__)
    print("annotated_sample.__annotations__:", annotated_sample.__annotations__)
    print("annotated_sample.__code__.co_argcount:", annotated_sample.__code__.co_argcount)


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
    demo_example_7_1_function_as_object()
    demo_example_7_2_assign_and_map()
    demo_common_function_attributes()
    demo_assign_and_identity()
    demo_container_of_callables()
    demo_higher_order_sorted()
    demo_return_callable()
    demo_callable_instance()


if __name__ == "__main__":
    main()
