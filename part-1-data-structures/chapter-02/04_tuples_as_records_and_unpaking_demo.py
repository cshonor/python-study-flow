"""
Demo for 04-元组作记录与拆包.md

Run:
  python part-1-data-structures/chapter-02/04_tuples_as_records_and_unpaking_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def safe_text(s: str) -> str:
    """Render Unicode safely in non-UTF8 consoles (e.g. GBK)."""
    return s.encode("unicode_escape").decode("ascii")


def demo_tuple_as_record_and_unpacking() -> None:
    section("1) tuple as a record + unpacking + '_' placeholder")
    lax_coordinates = (33.9425, -118.408056)
    lat, lon = lax_coordinates
    print("LAX lat/lon:", lat, lon)

    city, year, pop, chg, area = ("Tokyo", 2003, 32_450, 0.66, 8014)
    print("city record:", city, year, pop, chg, area)

    traveler_ids = [
        ("USA", "31195855"),
        ("BRA", "CE342567"),
        ("ESP", "XDA205856"),
    ]
    for passport in sorted(traveler_ids):
        print("%s/%s" % passport)

    countries = [country for country, _ in traveler_ids]
    print("countries:", countries)


def demo_starred_unpacking() -> None:
    section("2) starred unpacking: capture the rest")
    a, b, *rest = range(5)
    print("a, b, rest:", a, b, rest)
    assert (a, b, rest) == (0, 1, [2, 3, 4])  # 成立 → a=0,b=1,rest=[2,3,4]

    a, b, *rest = range(2)
    print("a, b, rest (empty):", a, b, rest)
    assert rest == []  # 成立 → 无余项时 rest 为 []

    a, *body, c, d = range(5)
    print("a, body, c, d:", a, body, c, d)
    assert (a, body, c, d) == (0, [1, 2], 3, 4)  # 成立 → body 收中间

    *head, b, c, d = range(5)
    print("head, b, c, d:", head, b, c, d)
    assert (head, b, c, d) == ([0, 1], 2, 3, 4)  # 成立 → head 收前段

    first, *_, last = range(6)
    print("first, last:", first, last)
    assert (first, last) == (0, 5)  # 成立 → first=0,last=5


def demo_nested_unpacking() -> None:
    section("3) nested unpacking: metro_areas example")
    metro_areas = [
        ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
        ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889)),
        ("Mexico City", "MX", 20.142, (19.433333, -99.133333)),
        ("New York-Newark", "US", 20.104, (40.808611, -74.020386)),
        ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
    ]

    print(f"{'':15} | {'latitude':>9} | {'longitude':>9}")
    for name, _, _, (lat, lon) in metro_areas:
        if lon <= 0:
            # city name contains non-ascii in sample; escape it for GBK consoles
            print(f"{safe_text(name):15} | {lat:9.4f} | {lon:9.4f}")


def demo_immutability_is_reference_level() -> None:
    section("4) tuple immutability is about references")
    a = (10, "alpha", [1, 2])
    b = (10, "alpha", [1, 2])
    print("a == b:", a == b)
    assert a == b  # 成立 → 结构相同、值相等
    b[-1].append(99)
    print("a == b after inner list change:", a == b)
    assert a != b  # 成立 → 共享槽位内 list 被改，相等性破坏
    print("b:", b)


def demo_hashable_check() -> None:
    section("5) hashable tuples: fixed() helper")

    def fixed(o: object) -> bool:
        try:
            hash(o)
            return True
        except TypeError:
            return False

    tf = (10, "alpha", (1, 2))
    tm = (10, "alpha", [1, 2])

    print("fixed(tf):", fixed(tf))
    print("fixed(tm):", fixed(tm))
    assert fixed(tf) is True  # 成立 → 全不可变，可 hash
    assert fixed(tm) is False  # 成立 → 含 list，不可 hash


def demo_iadd_list_vs_tuple() -> None:
    section("6) += : list in-place (same id) vs tuple new object (id changes)")
    a = [1, 2, 3]
    id_a_before = id(a)
    a += [4, 5]
    print("list id unchanged?", id(a) == id_a_before, "->", a)
    assert id(a) == id_a_before  # 成立 → list += 原地，id 不变
    assert a == [1, 2, 3, 4, 5]  # 成立 → 内容扩展为五元

    t = (1, 2)
    id_t_before = id(t)
    t += (30, 40)
    print("tuple id changed?", id(t) != id_t_before, "->", t)
    assert id(t) != id_t_before  # 成立 → tuple += 建新对象
    assert t == (1, 2, 30, 40)  # 成立 → 绑定到新元组


def demo_tuple_slot_iadd_puzzle() -> None:
    section("7) puzzle: t[2] += [...] when t[2] is a list (TypeError but list mutates)")
    t: tuple[int, int, list[int]] = (1, 2, [30, 40])
    print("before:", t)
    try:
        t[2] += [50, 60]
    except TypeError as e:
        print("TypeError (expected):", e)
    print("after :", t)
    assert t == (1, 2, [30, 40, 50, 60])  # 成立 → 槽内 list 已在 += 第一步被拉长


def main() -> None:
    demo_tuple_as_record_and_unpacking()
    demo_starred_unpacking()
    demo_nested_unpacking()
    demo_immutability_is_reference_level()
    demo_hashable_check()
    demo_iadd_list_vs_tuple()
    demo_tuple_slot_iadd_puzzle()


if __name__ == "__main__":
    main()

