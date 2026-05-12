"""
Ch. 9.2 supplement: plain function vs class method (self) vs decorator — no mixing.

Run from repo root:
  python part-2-functions-as-objects/chapter-09/02_decorator_self_method_compare_demo.py
"""

from __future__ import annotations


# --- 1) 写在 class 外面的 def：普通函数 / 装饰器外层，不需要 self ---
def outer(func):
    print(f"[outer] wrapping {func.__name__} (no self - not a method)")
    return func


@outer
def standalone():
    print("standalone()")


# --- 2) 写在 class 里面：普通实例方法，第一个参数习惯叫 self ---
class Person:
    def run(self) -> None:
        print("Person.run(self)")

    @staticmethod
    def hop() -> None:
        print("Person.hop() - staticmethod, no self")

    @classmethod
    def tag(cls) -> None:
        print(f"Person.tag(cls={cls.__name__})")


# --- 3) 装饰器 = 高阶函数：@deco 等价于 f = deco(f) ---
def deco(f):
    return f


@deco
def hi() -> None:
    print("hi()")


def main() -> None:
    print("== 1) decorator as plain function (no self) ==")
    standalone()
    print()

    print("== 2) class methods ==")
    Person().run()
    Person.hop()
    Person.tag()
    print()

    print("== 3) @deco is just hi = deco(hi) ==")
    hi()


if __name__ == "__main__":
    main()
