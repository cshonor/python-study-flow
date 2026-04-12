"""
Demo for 06-9.6 闭包（Closure）深度理解：累计平均值、自由变量与 cell.md (Fluent Python 9.6).

Shows:
- class-based callable object vs closure-based averager
- free vars in function.__code__.co_freevars
- closure cells in function.__closure__ and cell_contents
- UnboundLocalError pitfall when rebinding free vars, and the nonlocal fix
"""

from __future__ import annotations


class Averager:
    def __init__(self) -> None:
        self.series: list[float] = []

    def __call__(self, new_value: float) -> float:
        self.series.append(float(new_value))
        return sum(self.series) / len(self.series)


def make_averager_list():
    series: list[float] = []

    def averager(new_value: float) -> float:
        series.append(float(new_value))
        return sum(series) / len(series)

    return averager


def make_averager_nonlocal_broken():
    total = 0.0
    count = 0

    def averager(new_value: float) -> float:
        # This will raise UnboundLocalError because total/count are rebound.
        total += float(new_value)  # noqa: F823
        count += 1  # noqa: F823
        return total / count

    return averager


def make_averager_nonlocal_fixed():
    total = 0.0
    count = 0

    def averager(new_value: float) -> float:
        nonlocal total, count
        total += float(new_value)
        count += 1
        return total / count

    return averager


def show_closure(fn) -> None:
    print("fn ->", fn)
    code = fn.__code__
    print("co_varnames ->", code.co_varnames)
    print("co_freevars ->", code.co_freevars)
    cells = fn.__closure__
    print("__closure__ ->", cells)
    if cells:
        print("cell_contents ->", [c.cell_contents for c in cells])


def main() -> None:
    print("=== class-based callable ===")
    avg_obj = Averager()
    print(avg_obj(10), avg_obj(11), avg_obj(12))
    print("state in instance ->", avg_obj.series)

    print("\n=== closure-based (list) ===")
    avg = make_averager_list()
    print(avg(10), avg(11), avg(12))
    show_closure(avg)

    print("\n=== pitfall: rebinding free vars without nonlocal ===")
    broken = make_averager_nonlocal_broken()
    try:
        print(broken(10))
    except Exception as e:
        print(type(e).__name__ + ":", e)

    print("\n=== fixed with nonlocal ===")
    fixed = make_averager_nonlocal_fixed()
    print(fixed(10), fixed(11), fixed(12))
    show_closure(fixed)


if __name__ == "__main__":
    main()

