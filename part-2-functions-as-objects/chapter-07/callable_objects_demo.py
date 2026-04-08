"""
Demo for 05-nine-kinds-of-callables.md (Fluent Python 7.5)

Run from repo root:
  python part-2-functions-as-objects/chapter-07/callable_objects_demo.py
"""

from __future__ import annotations

import asyncio
import inspect
from types import BuiltinFunctionType, BuiltinMethodType, FunctionType, MethodType


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def show(label: str, obj: object) -> None:
    print(label)
    print("  callable:", callable(obj))
    print("  type:", type(obj))
    # inspect helpers (best-effort; some return False for builtins)
    print("  inspect.isfunction:", inspect.isfunction(obj))
    print("  inspect.ismethod:", inspect.ismethod(obj))
    print("  inspect.isbuiltin:", inspect.isbuiltin(obj))
    print("  inspect.isclass:", inspect.isclass(obj))


def user_defined_function(x: int) -> int:
    return x + 1


class Adder:
    def __call__(self, x: int, y: int) -> int:
        return x + y


def gen_func(n: int):
    for i in range(n):
        yield i


async def coro_func(x: int) -> int:
    await asyncio.sleep(0)
    return x + 1


async def async_gen_func(n: int):
    for i in range(n):
        await asyncio.sleep(0)
        yield i


def demo_nine_kinds() -> None:
    section("7.5: callable kinds (overview)")

    # 1) user-defined function
    show("1) user-defined function (def)", user_defined_function)

    # 2) builtin function
    show("2) builtin function", len)
    print("  isinstance(len, BuiltinFunctionType):", isinstance(len, BuiltinFunctionType))

    # 3) builtin method (bound on builtin instances)
    d = {}
    show("3) builtin method (dict.get bound)", d.get)
    print("  isinstance(d.get, BuiltinMethodType):", isinstance(d.get, BuiltinMethodType))

    # 4) method (bound Python method)
    class C:
        def m(self) -> str:
            return "m"

    c = C()
    show("4) method (C().m bound)", c.m)
    print("  isinstance(c.m, MethodType):", isinstance(c.m, MethodType))

    # 5) class (calling constructs instance)
    show("5) class (type object)", str)

    # 6) user-defined callable instance (__call__)
    add = Adder()
    show("6) callable instance (__call__)", add)

    # 7) generator function
    show("7) generator function", gen_func)
    g = gen_func(3)
    print("  gen_func(3) returns:", type(g))
    print("  list(gen_func(3)):", list(gen_func(3)))

    # 8) coroutine function
    show("8) coroutine function (async def)", coro_func)
    coro = coro_func(10)
    print("  coro_func(10) returns:", type(coro))
    print("  asyncio.run(coro_func(10)):", asyncio.run(coro_func(10)))
    # close the earlier coroutine object to avoid warnings
    coro.close()

    # 9) async generator function
    show("9) async generator function (async def + yield)", async_gen_func)
    agen = async_gen_func(3)
    print("  async_gen_func(3) returns:", type(agen))

    async def consume_async_gen() -> list[int]:
        out: list[int] = []
        async for item in async_gen_func(3):
            out.append(item)
        return out

    print("  asyncio.run(consume_async_gen()):", asyncio.run(consume_async_gen()))
    # close async generator to be neat
    asyncio.run(agen.aclose())


def demo_callable_quick_check() -> None:
    section("callable(obj) quick check")
    for obj in (abs, str, "Ni!"):
        print(repr(obj), "->", callable(obj))


def main() -> None:
    demo_callable_quick_check()
    demo_nine_kinds()


if __name__ == "__main__":
    main()

