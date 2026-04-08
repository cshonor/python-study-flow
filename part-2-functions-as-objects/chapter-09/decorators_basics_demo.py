"""
Demo for 02-decorators-basics.md.

Shows that:
- @deco is just syntax sugar for: target = deco(target)
- decoration runs at import time (when executing the def with @)
- the decorated name is rebound to the returned callable (often an inner wrapper)
"""

from __future__ import annotations

from collections.abc import Callable


def deco(func: Callable[[], None]) -> Callable[[], None]:
    print(f"deco() running at import time; decorating: {func!r}")

    def inner() -> None:
        print("inner(): before calling original function")
        func()
        print("inner(): after calling original function")

    return inner


@deco
def target() -> None:
    print("target(): running original function body")


def main() -> None:
    print("main(): starting")
    print("target name now refers to:", target)
    target()


if __name__ == "__main__":
    main()

