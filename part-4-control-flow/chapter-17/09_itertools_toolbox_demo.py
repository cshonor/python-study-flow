"""Ch. 17.9: standard library iterator/generator toolbox (grouped demos)."""

from __future__ import annotations

import itertools
import operator


def vowels_only(s: str) -> bool:
    return s.lower() in "aeiou"


def show(title: str, value) -> None:
    print(f"== {title} ==")
    print(value)
    print()


def main() -> None:
    # 1) filtering
    data = list("Aardvark")
    show("filter vowels", list(filter(vowels_only, data)))
    show("filterfalse vowels", list(itertools.filterfalse(vowels_only, data)))
    show("compress", list(itertools.compress("ABCDEF", [1, 0, 1, 0, 0, 1])))
    show("islice", list(itertools.islice(range(10), 2, 8, 2)))

    # 2) mapping
    show("map square", list(map(lambda x: x * x, range(6))))
    show("starmap pow", list(itertools.starmap(pow, [(2, 3), (3, 2), (10, 1)])))
    show("accumulate sum", list(itertools.accumulate([1, 2, 3, 4])))
    show("accumulate mul", list(itertools.accumulate([1, 2, 3, 4], operator.mul)))
    show("enumerate", list(enumerate("ABC", start=1)))

    # 3) merging
    show("chain", list(itertools.chain("ABC", range(3))))
    show("chain.from_iterable", list(itertools.chain.from_iterable([[1, 2], [3, 4]])))
    show("zip", list(zip("ABC", range(10))))
    show("zip_longest", list(itertools.zip_longest("ABC", range(5), fillvalue="?")))
    show("product", list(itertools.product("AB", range(2))))

    # 4) infinite / expanding (always slice!)
    show("count (slice)", list(itertools.islice(itertools.count(1, 0.5), 6)))
    show("cycle (slice)", list(itertools.islice(itertools.cycle("ABC"), 10)))
    show("repeat", list(itertools.repeat(7, 3)))
    show("pairwise", list(itertools.pairwise(range(6))))

    # 5) rearranging / grouping
    animals = ["duck", "eagle", "emu", "fox", "goat", "gnu", "hare", "ibis"]
    animals_sorted = sorted(animals, key=len)
    grouped = [(k, list(g)) for k, g in itertools.groupby(animals_sorted, key=len)]
    show("groupby (after sort by len)", grouped)
    show("reversed (sequence only)", list(reversed([1, 2, 3])))

    it = iter("ABCDE")
    it1, it2 = itertools.tee(it, 2)
    show("tee #1", list(it1))
    show("tee #2", list(it2))

    # 6) combinatorics
    show("permutations", list(itertools.permutations("ABC", 2)))
    show("combinations", list(itertools.combinations("ABC", 2)))
    show(
        "combinations_with_replacement",
        list(itertools.combinations_with_replacement("ABC", 2)),
    )


if __name__ == "__main__":
    main()

