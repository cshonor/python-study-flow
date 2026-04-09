from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import NoReturn, Protocol, TypeVar, overload


class SupportsLessThan(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


T = TypeVar("T")
LT = TypeVar("LT", bound=SupportsLessThan)
K = TypeVar("K", bound=SupportsLessThan)


@overload
def max_like(__iterable: Iterable[LT], /) -> LT: ...


@overload
def max_like(__iterable: Iterable[T], /, *, key: Callable[[T], K]) -> T: ...


@overload
def max_like(__iterable: Iterable[LT], /, *, default: LT) -> LT: ...


@overload
def max_like(__iterable: Iterable[T], /, *, key: Callable[[T], K], default: T) -> T: ...


@overload
def max_like(__arg1: LT, __arg2: LT, /, *args: LT) -> LT: ...


@overload
def max_like(__arg1: T, __arg2: T, /, *args: T, key: Callable[[T], K]) -> T: ...


def _empty_iterable_error() -> NoReturn:
    raise ValueError("max_like() arg is an empty iterable")


def max_like(*args, **kwargs):
    """A tiny 'max' re-implementation to demonstrate overload patterns.

    The overloads cover these main axes:
    - iterable vs multiple positional args
    - key callable present vs absent
    - default present vs absent (iterable form)
    """

    key = kwargs.pop("key", None)
    default_sentinel = object()
    default = kwargs.pop("default", default_sentinel)
    if kwargs:
        raise TypeError(f"unexpected keyword arguments: {sorted(kwargs)}")

    if len(args) == 0:
        raise TypeError("max_like expected at least 1 argument")

    if len(args) == 1:
        it = iter(args[0])
        try:
            best = next(it)
        except StopIteration:
            if default is not default_sentinel:
                return default
            _empty_iterable_error()

        if key is None:
            for x in it:
                if x > best:
                    best = x
            return best

        best_key = key(best)
        for x in it:
            kx = key(x)
            if kx > best_key:
                best, best_key = x, kx
        return best

    # multiple positional args form
    it = iter(args)
    best = next(it)
    if key is None:
        for x in it:
            if x > best:
                best = x
        return best

    best_key = key(best)
    for x in it:
        kx = key(x)
        if kx > best_key:
            best, best_key = x, kx
    return best


def main() -> None:
    print("iterable form (no key/default)")
    print(max_like([3, 1, 4, 2]))

    print("\niterable form (key)")
    words = ["pear", "banana", "fig"]
    print(max_like(words, key=len))

    print("\niterable form (default on empty)")
    print(max_like([], default=0))
    print(max_like([], key=len, default=""))

    print("\nvarargs form (no key)")
    print(max_like(3, 1, 4, 2))

    print("\nvarargs form (key)")
    print(max_like("a", "bbb", "cc", key=len))


if __name__ == "__main__":
    main()

