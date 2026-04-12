from __future__ import annotations

from typing import Generic, TypeVar


class Beverage:
    def __repr__(self) -> str:
        return "Beverage()"


class Juice(Beverage):
    def __repr__(self) -> str:
        return "Juice()"


class OrangeJuice(Juice):
    def __repr__(self) -> str:
        return "OrangeJuice()"


# --- Invariant dispenser (read + write) ---

T = TypeVar("T")


class BeverageDispenser(Generic[T]):
    """Invariant: can accept and dispense T (read+write)."""

    def __init__(self, item: T) -> None:
        self._item = item

    def install(self, item: T) -> None:
        self._item = item

    def dispense(self) -> T:
        return self._item


# --- Covariant dispenser (read-only / producer) ---

T_co = TypeVar("T_co", covariant=True)


class ReadOnlyDispenser(Generic[T_co]):
    def __init__(self, item: T_co) -> None:
        self._item = item

    def dispense(self) -> T_co:
        return self._item


# --- Contravariant trash can (write-only / consumer) ---

T_contra = TypeVar("T_contra", contravariant=True)


class TrashCan(Generic[T_contra]):
    def put(self, refuse: T_contra) -> None:
        print("put:", refuse)


class Refuse:
    def __repr__(self) -> str:
        return "Refuse()"


class Biodegradable(Refuse):
    def __repr__(self) -> str:
        return "Biodegradable()"


class Compostable(Biodegradable):
    def __repr__(self) -> str:
        return "Compostable()"


def main() -> None:
    print("Invariant: BeverageDispenser[T] (read+write)")
    inv = BeverageDispenser(Juice())
    print("dispense ->", inv.dispense())
    inv.install(OrangeJuice())
    print("dispense ->", inv.dispense())

    print("\nCovariant: ReadOnlyDispenser[T_co] (read-only)")
    ro_orange: ReadOnlyDispenser[OrangeJuice] = ReadOnlyDispenser(OrangeJuice())
    ro_bev: ReadOnlyDispenser[Beverage] = ro_orange
    print("ro_bev.dispense() ->", ro_bev.dispense())

    print("\nContravariant: TrashCan[T_contra] (write-only)")
    can_refuse: TrashCan[Refuse] = TrashCan()
    can_bio: TrashCan[Biodegradable] = can_refuse
    can_bio.put(Compostable())


if __name__ == "__main__":
    main()

