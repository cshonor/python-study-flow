"""
Demo for 09-str-key-dict-and-dunder-missing.md (Fluent Python §3.5.2).

Run:
  python part-1-data-structures/chapter-03/str_key_dict_demo.py
"""

from __future__ import annotations

from collections import UserDict


class StrKeyDict0(dict):
    """Example 3-8: int keys map to str keys via __missing__."""

    def __missing__(self, key: object) -> object:
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]


class StrKeyDict0Complete(StrKeyDict0):
    """dict subclass + __missing__ + get/__contains__ (book completion)."""

    def get(self, key: object, default: object = None) -> object:
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: object) -> bool:
        return key in self.keys() or str(key) in self.keys()


class StrKeyDict(UserDict):
    """UserDict + __missing__ + get/__contains__ aligned with d[k]."""

    def __missing__(self, key: object) -> object:
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key: object) -> bool:
        return str(key) in self.data

    def get(self, key: object, default: object = None) -> object:
        try:
            return self[key]
        except KeyError:
            return default


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_str_key_dict0() -> None:
    section("1) StrKeyDict0 (dict subclass): d[k] only")
    d = StrKeyDict0([("2", "two"), ("4", "four")])
    assert d["2"] == "two"
    assert d[4] == "four"
    try:
        _ = d[1]
    except KeyError as e:
        print("d[1] -> KeyError:", e)
    print("d.get(4) without override:", d.get(4))
    print("4 in d without __contains__ override:", 4 in d)


def demo_str_key_dict0_complete() -> None:
    section("2) StrKeyDict0Complete: get / in aligned with d[k]")
    d = StrKeyDict0Complete([("2", "two"), ("4", "four")])
    assert d["2"] == "two"
    assert d[4] == "four"
    try:
        _ = d[1]
    except KeyError as e:
        assert e.args[0] == "1"
    assert d.get("2") == "two"
    assert d.get(4) == "four"
    assert d.get(1, "N/A") == "N/A"
    assert 2 in d and "2" in d and 4 in d
    assert 1 not in d
    print("get(4):", d.get(4), "| 4 in d:", 4 in d)


def demo_str_key_dict_userdict() -> None:
    section("3) StrKeyDict (UserDict): same semantics via self.data")
    u = StrKeyDict([("2", "two"), ("4", "four")])
    assert u["2"] == "two" and u[4] == "four"
    assert u.get(4) == "four"
    assert 4 in u
    assert u.get(1, "N/A") == "N/A"
    print("u.get(4):", u.get(4), "| 4 in u:", 4 in u)


def main() -> None:
    demo_str_key_dict0()
    demo_str_key_dict0_complete()
    demo_str_key_dict_userdict()


if __name__ == "__main__":
    main()
