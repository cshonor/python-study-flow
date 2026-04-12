from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Generic, TypeVar


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


class Box(Generic[T]):
    """Invariant generic (default)."""

    def __init__(self, item: T) -> None:
        self.item = item


class ReadOnlyBox(Generic[T_co]):
    """Covariant: you can treat ReadOnlyBox[Dog] as ReadOnlyBox[Animal]."""

    def __init__(self, item: T_co) -> None:
        self._item = item

    def get(self) -> T_co:
        return self._item


class Sink(Generic[T_contra]):
    """Contravariant: a Sink[Animal] can accept Dog."""

    def put(self, item: T_contra) -> None:
        print("put:", item)


class Animal:
    def __repr__(self) -> str:
        return "Animal()"


class Dog(Animal):
    def __repr__(self) -> str:
        return "Dog()"


def main() -> None:
    print("Sequence is covariant (read-only)")
    dogs: list[Dog] = [Dog(), Dog()]
    animals_seq: Sequence[Animal] = dogs
    print("animals_seq[0] ->", animals_seq[0])

    print("\nCallable is contravariant in args, covariant in return (intuition demo)")
    def handle_animal(a: Animal) -> str:
        return "handled " + repr(a)

    handler: Callable[[Dog], str] = handle_animal
    print("handler(Dog()) ->", handler(Dog()))

    print("\nCustom generics variance")
    ro_dog: ReadOnlyBox[Dog] = ReadOnlyBox(Dog())
    ro_animal: ReadOnlyBox[Animal] = ro_dog
    print("ro_animal.get() ->", ro_animal.get())

    sink_animal: Sink[Animal] = Sink()
    sink_dog: Sink[Dog] = sink_animal
    sink_dog.put(Dog())

    print("\nInvariant Box (why invariance exists)")
    box_dog: Box[Dog] = Box(Dog())
    print("box_dog.item ->", box_dog.item)


if __name__ == "__main__":
    main()

