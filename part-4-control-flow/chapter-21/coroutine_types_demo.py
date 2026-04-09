"""Ch. 21.2: Native coroutines vs classic generator coroutines vs @types.coroutine."""

from __future__ import annotations

import asyncio
import inspect
import types
from collections.abc import AsyncGenerator, Generator


async def native_coro(x: int) -> int:
    await asyncio.sleep(0)
    return x + 1


@types.coroutine
def generator_based_coro(x: int) -> Generator[object, None, int]:
    # This generator is awaitable because of @types.coroutine.
    yield from asyncio.sleep(0)
    return x + 10


def classic_generator_coroutine() -> Generator[str, int, str]:
    # "Classic coroutine": driven by next()/send(), NOT awaitable.
    total = 0
    while True:
        n = yield f"total={total}"
        total += n


async def async_gen(n: int) -> AsyncGenerator[int, None]:
    for i in range(n):
        await asyncio.sleep(0)
        yield i


async def main() -> None:
    print("== inspect helpers ==")
    print("native_coro is coroutinefunction ->", inspect.iscoroutinefunction(native_coro))
    print(
        "generator_based_coro is coroutinefunction ->",
        inspect.iscoroutinefunction(generator_based_coro),
    )
    print(
        "classic_generator_coroutine is generatorfunction ->",
        inspect.isgeneratorfunction(classic_generator_coroutine),
    )
    print()

    print("== native coroutine object ==")
    c1 = native_coro(1)
    print("inspect.iscoroutine(c1) ->", inspect.iscoroutine(c1))
    print("inspect.isawaitable(c1) ->", inspect.isawaitable(c1))
    print("await native_coro(1) ->", await c1)
    print()

    print("== generator-based coroutine (awaitable) ==")
    c2 = generator_based_coro(1)
    print("inspect.iscoroutine(c2) ->", inspect.iscoroutine(c2))
    print("inspect.isawaitable(c2) ->", inspect.isawaitable(c2))
    print("await generator_based_coro(1) ->", await c2)
    print()

    print("== classic generator coroutine (send-driven) ==")
    g = classic_generator_coroutine()
    print("inspect.isawaitable(g) ->", inspect.isawaitable(g))
    print("next(g) ->", next(g))
    print("g.send(10) ->", g.send(10))
    print("g.send(7) ->", g.send(7))
    print()

    print("== async generator ==")
    out: list[int] = []
    async for i in async_gen(5):
        out.append(i)
    print("async for ->", out)


if __name__ == "__main__":
    asyncio.run(main())

