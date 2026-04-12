"""
Demo for 07-9.7 nonlocal 与名字解析：闭包里为什么 += 会炸（以及完整查找规则）.md (Fluent Python 9.7).

Shows:
- why count += 1 triggers UnboundLocalError without nonlocal
- fixed version using nonlocal
- global vs nonlocal behavior
- a stateful decorator using nonlocal to count calls
"""

from __future__ import annotations

from functools import wraps


def make_averager_broken():
    count = 0
    total = 0.0

    def averager(new_value: float) -> float:
        # Rebinding makes count/total local, so reads happen before they are bound.
        count += 1  # noqa: F823
        total += float(new_value)  # noqa: F823
        return total / count

    return averager


def make_averager_fixed():
    count = 0
    total = 0.0

    def averager(new_value: float) -> float:
        nonlocal count, total
        count += 1
        total += float(new_value)
        return total / count

    return averager


module_level = 100


def global_demo() -> None:
    global module_level
    module_level += 1


def counted(func):
    calls = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        print(f"{func.__name__} calls -> {calls}")
        return func(*args, **kwargs)

    return wrapper


@counted
def greet(name: str) -> str:
    return f"hi {name}"


def main() -> None:
    print("=== nonlocal pitfall (broken averager) ===")
    broken = make_averager_broken()
    try:
        print(broken(10))
    except Exception as e:
        print(type(e).__name__ + ":", e)

    print("\n=== fixed with nonlocal ===")
    avg = make_averager_fixed()
    print(avg(10), avg(11), avg(12))

    print("\n=== global demo (module scope) ===")
    print("module_level(before) ->", module_level)
    global_demo()
    print("module_level(after) ->", module_level)

    print("\n=== stateful decorator (nonlocal counter) ===")
    print(greet("A"))
    print(greet("B"))
    print(greet("C"))


if __name__ == "__main__":
    main()

