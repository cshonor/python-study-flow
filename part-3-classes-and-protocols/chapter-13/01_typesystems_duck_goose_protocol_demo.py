from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Protocol, runtime_checkable


# --- Duck typing: "sequence protocol" by behavior (len + getitem) ---


class MiniSeq:
    """A minimal user-defined sequence: no inheritance, just behavior."""

    def __init__(self, items: list[int]) -> None:
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


# --- Goose typing: ABCs for runtime checks (isinstance / issubclass) ---


class RealSequence(Sequence[int]):
    """A Sequence ABC subclass must provide required abstract methods."""

    def __init__(self, items: Iterable[int]) -> None:
        self._items = list(items)

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]


# --- Static duck typing: Protocol (PEP 544) ---


class SizedGetItem(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, index: int) -> int: ...


@runtime_checkable
class RuntimeSizedGetItem(Protocol):
    def __len__(self) -> int: ...

    def __getitem__(self, index: int) -> int: ...


def first_item(x: SizedGetItem) -> int:
    # Type checkers validate structural compatibility.
    return x[0]


def main() -> None:
    duck = MiniSeq([10, 20, 30])
    goose = RealSequence([10, 20, 30])

    print("duck typing (behavior)")
    print("len(duck) ->", len(duck))
    print("duck[1:] ->", duck[1:])
    print("isinstance(duck, Sequence) ->", isinstance(duck, Sequence))
    print("first_item(duck) ->", first_item(duck))

    print("\ngoose typing (ABC)")
    print("len(goose) ->", len(goose))
    print("isinstance(goose, Sequence) ->", isinstance(goose, Sequence))
    print("first_item(goose) ->", first_item(goose))

    print("\nProtocol at runtime (optional)")
    print("isinstance(duck, RuntimeSizedGetItem) ->", isinstance(duck, RuntimeSizedGetItem))
    print(
        "isinstance(goose, RuntimeSizedGetItem) ->",
        isinstance(goose, RuntimeSizedGetItem),
    )


if __name__ == "__main__":
    main()

