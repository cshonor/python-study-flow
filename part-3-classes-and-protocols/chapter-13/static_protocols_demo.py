from __future__ import annotations

import numbers
import random
from collections.abc import Iterable
from typing import Any, Protocol, TypeVar, runtime_checkable


# --- 13.6.1: Protocol for "x * 2 returns same type" ---

T_co = TypeVar("T_co", covariant=True)


class Repeatable(Protocol[T_co]):
    def __mul__(self: T_co, n: int) -> T_co: ...


RT = TypeVar("RT", bound=Repeatable[Any])


def double(x: RT) -> RT:
    return x * 2


# --- 13.6.2: runtime_checkable Protocol (optional runtime isinstance) ---


@runtime_checkable
class SupportsComplex(Protocol):
    def __complex__(self) -> complex: ...


def fromcomplex(z: SupportsComplex) -> tuple[float, float]:
    c = complex(z)
    return (c.real, c.imag)


# --- 13.6.5–13.6.8: narrow protocol example + extension idea ---


@runtime_checkable
class RandomPicker(Protocol):
    def pick(self) -> Any: ...


class SimplePicker:
    def __init__(self, items: Iterable[Any]) -> None:
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self) -> Any:
        return self._items.pop()


def main() -> None:
    print("Protocol-based type hint (runtime still duck typed)")
    print("double(21) ->", double(21))
    print("double('Py') ->", double("Py"))

    print("\n@runtime_checkable Protocol")
    print("fromcomplex(3+4j) ->", fromcomplex(3 + 4j))
    print("isinstance(3+4j, SupportsComplex) ->", isinstance(3 + 4j, SupportsComplex))

    class OddComplex:
        def __complex__(self) -> complex:
            return 1 + 2j

    print("fromcomplex(OddComplex()) ->", fromcomplex(OddComplex()))
    print("isinstance(OddComplex(), SupportsComplex) ->", isinstance(OddComplex(), SupportsComplex))

    print("\nNarrow protocol: RandomPicker")
    picker = SimplePicker([1, 2, 3])
    print("isinstance(picker, RandomPicker) ->", isinstance(picker, RandomPicker))
    print("picker.pick() ->", picker.pick())

    print("\nNumbers ABC vs 'supports X' thinking")
    x: Any = 1 + 2j
    print("isinstance(x, numbers.Real) ->", isinstance(x, numbers.Real))
    print("isinstance(x, SupportsComplex) ->", isinstance(x, SupportsComplex))
    try:
        float(x)
    except TypeError as e:
        print("float(x) ->", e)
    print("complex(x) ->", complex(x))


if __name__ == "__main__":
    main()

