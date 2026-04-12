from __future__ import annotations

from collections import OrderedDict


class LastUpdatedOrderedDict(OrderedDict):
    """Store items in update order."""

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
        self.move_to_end(key)


class NotRecommended(OrderedDict):
    """Anti-pattern: hard-code parent class name."""

    def __setitem__(self, key, value) -> None:
        OrderedDict.__setitem__(self, key, value)
        self.move_to_end(key)


def main() -> None:
    print("super() version")
    d = LastUpdatedOrderedDict()
    d["a"] = 1
    d["b"] = 2
    d["a"] = 3
    print(list(d.items()))  # [('b', 2), ('a', 3)]

    print("\nhard-coded parent version (still works in single inheritance)")
    d2 = NotRecommended()
    d2["a"] = 1
    d2["b"] = 2
    d2["a"] = 3
    print(list(d2.items()))


if __name__ == "__main__":
    main()

