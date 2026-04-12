"""
Demo for 04-7.4 匿名函数：lambda 表达式.md (Fluent Python 7.4)

Run from repo root:
  python part-2-functions-as-objects/chapter-07/04_lambda_expressions_demo.py
"""


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_ex_7_7_sorted_key() -> None:
    section("Ex 7-7: sorted(..., key=lambda word: word[::-1])")
    fruits = [
        "strawberry",
        "fig",
        "apple",
        "cherry",
        "raspberry",
        "banana",
    ]
    out = sorted(fruits, key=lambda word: word[::-1])
    print(out)


def demo_map_filter() -> None:
    section("map / filter with lambda")
    numbers = [1, 2, 3, 4, 5]
    squared = list(map(lambda x: x**2, numbers))
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print("squared:", squared)
    print("evens:", evens)


def demo_lambda_vs_def_names() -> None:
    section("lambda is anonymous (__name__ == '<lambda>')")
    f = lambda x: x + 1

    def g(x: int) -> int:
        return x + 1

    print("f.__name__:", f.__name__)
    print("g.__name__:", g.__name__)


def demo_prefer_def_over_assignment() -> None:
    section("Prefer def over: add = lambda x, y: x + y")

    def add(x: int, y: int) -> int:
        return x + y

    print("add(2, 3):", add(2, 3))


def main() -> None:
    demo_ex_7_7_sorted_key()
    demo_map_filter()
    demo_lambda_vs_def_names()
    demo_prefer_def_over_assignment()


if __name__ == "__main__":
    main()
