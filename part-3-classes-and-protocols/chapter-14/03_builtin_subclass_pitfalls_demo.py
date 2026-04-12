from __future__ import annotations

from collections import UserDict, UserList


# --- dict pitfalls ---


class DoppelDict(dict):
    """Attempt to change dict write semantics by overriding __setitem__."""

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, [value, value])


class DoppelDict2(UserDict):
    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, [value, value])


class AnswerDict(dict):
    """Attempt to change read semantics by overriding __getitem__."""

    def __getitem__(self, key):
        return 42


class AnswerDict2(UserDict):
    def __getitem__(self, key):
        return 42


def demo_dict() -> None:
    print("dict subclass pitfalls (CPython)")

    dd = DoppelDict(one=1)
    dd["two"] = 2
    dd.update(three=3)
    print("DoppelDict after init/[]/update ->", dd)

    dd2 = DoppelDict2(one=1)
    dd2["two"] = 2
    dd2.update(three=3)
    print("DoppelDict2(UserDict) after init/[]/update ->", dd2)

    ad = AnswerDict(a="foo")
    print("AnswerDict['a'] ->", ad["a"])
    d: dict[str, object] = {}
    d.update(ad)
    print("d.update(AnswerDict) then d['a'] ->", d["a"])

    ad2 = AnswerDict2(a="foo")
    print("AnswerDict2['a'] ->", ad2["a"])
    d2: dict[str, object] = {}
    d2.update(ad2)
    print("d.update(AnswerDict2(UserDict)) then d2['a'] ->", d2["a"])


# --- list pitfalls ---


class BadList(list[int]):
    """Try to keep appended items doubled by overriding append."""

    def append(self, item: int) -> None:  # type: ignore[override]
        super().append(item * 2)


class GoodList(UserList[int]):
    def append(self, item: int) -> None:  # type: ignore[override]
        super().append(item * 2)

    def extend(self, other: list[int]) -> None:  # type: ignore[override]
        # Force reuse of our overridden append to keep the invariant.
        for item in other:
            self.append(item)


def demo_list() -> None:
    print("\nlist subclass pitfalls (CPython)")

    bl = BadList([1, 2])
    bl.append(3)
    bl.extend([4, 5])  # may bypass append override
    print("BadList after append/extend ->", bl)

    gl = GoodList([1, 2])
    gl.append(3)
    gl.extend([4, 5])
    print("GoodList(UserList) after append/extend ->", gl)


def main() -> None:
    demo_dict()
    demo_list()


if __name__ == "__main__":
    main()

