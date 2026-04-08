from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable


class Vowels:
    """Dynamic protocol demo: only __getitem__ is enough for lots of behaviors."""

    def __getitem__(self, i):
        return "AEIOU"[i]


class HasSpeak(Protocol):
    def speak(self) -> str: ...


@runtime_checkable
class RuntimeHasSpeak(Protocol):
    def speak(self) -> str: ...


class Duck:
    def speak(self) -> str:
        return "quack"


class Silent:
    pass


def call_speak(x: HasSpeak) -> str:
    # Static checkers validate that x has speak() -> str.
    return x.speak()


def main() -> None:
    print("dynamic protocol (Vowels)")
    v = Vowels()
    print("v[0], v[-1] ->", v[0], v[-1])
    print("list(v) ->", list(v))
    print("'E' in v ->", "E" in v)
    print("'Z' in v ->", "Z" in v)
    print("isinstance(v, Iterable) ->", isinstance(v, Iterable))

    print("\nstatic protocol (Protocol) - runtime behavior unchanged")
    print("call_speak(Duck()) ->", call_speak(Duck()))
    try:
        call_speak(Silent())  # type: ignore[arg-type]
    except AttributeError as e:
        print("call_speak(Silent()) ->", e)

    print("\nruntime_checkable Protocol (optional runtime isinstance)")
    print("isinstance(Duck(), RuntimeHasSpeak) ->", isinstance(Duck(), RuntimeHasSpeak))
    print(
        "isinstance(Silent(), RuntimeHasSpeak) ->",
        isinstance(Silent(), RuntimeHasSpeak),
    )


if __name__ == "__main__":
    main()

