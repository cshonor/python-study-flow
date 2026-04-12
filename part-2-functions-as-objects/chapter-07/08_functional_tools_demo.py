"""
Demo for 08-7.8 支持函数式编程的包：operator 与 functools.partial.md (Fluent Python 7.8)

Run from repo root:
  python part-2-functions-as-objects/chapter-07/08_functional_tools_demo.py
"""

from __future__ import annotations

import unicodedata
from collections import namedtuple
from functools import partial, reduce
from operator import add, attrgetter, itemgetter, methodcaller, mul


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def safe(obj: object) -> object:
    # Avoid UnicodeEncodeError in Windows consoles (GBK etc.)
    return ascii(obj) if isinstance(obj, str) else obj


def factorial_lambda(n: int) -> int:
    return reduce(lambda a, b: a * b, range(1, n + 1), 1)


def factorial_operator(n: int) -> int:
    return reduce(mul, range(1, n + 1), 1)


def tag(name: str, *content: str, class_: str | None = None, **attrs: str) -> str:
    if class_ is not None:
        attrs["class"] = class_
    if attrs:
        pairs = [f'{k}="{v}"' for k, v in sorted(attrs.items())]
        start_tag = f"<{name} {' '.join(pairs)}>"
    else:
        start_tag = f"<{name}>"
    if content:
        body = "\n".join(content)
        return f"{start_tag}\n{body}\n</{name}>"
    return start_tag


def demo_operator_mul_add() -> None:
    section("operator.mul/add vs lambda (factorial)")
    for n in (0, 1, 5, 6):
        print("n:", n, "| lambda:", factorial_lambda(n), "| operator:", factorial_operator(n))


def demo_itemgetter() -> None:
    section("itemgetter: pick fields by index")
    metro_data = [
        ("Tokyo", "JP", 36933000),
        ("Delhi NCR", "IN", 21935000),
        ("New York", "US", 8406000),
        ("Sao Paulo", "BR", 19649552),
    ]
    by_cc = sorted(metro_data, key=itemgetter(1))
    print("sorted by country code:", by_cc)
    cc_name = itemgetter(0, 1)
    print("cc_name(metro_data[0]):", cc_name(metro_data[0]))


def demo_attrgetter() -> None:
    section("attrgetter: pick attributes (including nested)")
    LatLon = namedtuple("LatLon", "lat lon")
    Metropolis = namedtuple("Metropolis", "name cc pop coord")
    metro_areas = [
        Metropolis("Tokyo", "JP", 36933000, LatLon(35.6897, 139.6917)),
        Metropolis("Delhi NCR", "IN", 21935000, LatLon(28.6139, 77.2090)),
        Metropolis("New York", "US", 8406000, LatLon(40.7128, -74.0060)),
        Metropolis("Sao Paulo", "BR", 19649552, LatLon(-23.5478, -46.6358)),
    ]
    name_lat = attrgetter("name", "coord.lat")
    for city in sorted(metro_areas, key=attrgetter("coord.lat")):
        print("name, lat:", tuple(safe(x) for x in name_lat(city)))


def demo_methodcaller() -> None:
    section("methodcaller: call a method by name")
    s = "The time has come"
    upcase = methodcaller("upper")
    hyphenate = methodcaller("replace", " ", "-")
    print("upper:", upcase(s))
    print("replace:", hyphenate(s))


def demo_partial() -> None:
    section("functools.partial: freeze args/kwargs")
    triple = partial(mul, 3)
    print("triple(7):", triple(7))
    print("list(map(triple, range(1, 6))):", list(map(triple, range(1, 6))))
    print("triple.func:", triple.func)
    print("triple.args:", triple.args)
    print("triple.keywords:", triple.keywords)

    nfc = partial(unicodedata.normalize, "NFC")
    print("nfc('cafe\\u0301'):", safe(nfc("cafe\u0301")))

    picture = partial(tag, "img", class_="pic-frame")
    print("picture(src=...):", picture(src="sunset.jpg"))
    print("picture.func:", picture.func.__name__)
    print("picture.args:", picture.args)
    print("picture.keywords:", picture.keywords)


def demo_reduce_vs_sum() -> None:
    section("reduce(add, ...) vs sum(...)")
    r = reduce(add, range(100))
    s = sum(range(100))
    print("reduce(add, range(100)):", r)
    print("sum(range(100)):", s)


def main() -> None:
    demo_operator_mul_add()
    demo_itemgetter()
    demo_attrgetter()
    demo_methodcaller()
    demo_partial()
    demo_reduce_vs_sum()


if __name__ == "__main__":
    main()

