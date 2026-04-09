"""Ch. 18.4: else clauses beyond if — for/else, while/else, try/else."""

from __future__ import annotations


def demo_for_else_find() -> None:
    print("== for/else: search ==")
    fruits = ["apple", "pear", "peach"]
    target = "banana"

    for f in fruits:
        if f == target:
            print("found:", f)
            break
    else:
        print("not found -> else runs")
    print()


def demo_while_else_retry() -> None:
    print("== while/else: retry loop ==")
    attempts = 3
    ok_at = 10  # never succeeds in 3 attempts
    i = 0
    while i < attempts:
        i += 1
        if i == ok_at:
            print("success on attempt", i)
            break
    else:
        print("no break (attempts exhausted) -> else runs")
    print()


def demo_try_else() -> None:
    print("== try/else: success path ==")
    text = "42"
    try:
        n = int(text)
    except ValueError:
        print("bad int")
    else:
        print("parsed:", n, "(else runs because no exception)")
    print()

    print("== try/else: else skipped on exception ==")
    text = "not-a-number"
    try:
        n = int(text)
    except ValueError:
        print("bad int (except runs)")
    else:
        print("parsed:", n)  # unreachable
    print()


def demo_eafp_vs_lbyl() -> None:
    print("== EAFP vs LBYL ==")
    d = {"a": 1}

    # LBYL
    key = "b"
    if key in d:
        v1 = d[key]
    else:
        v1 = 0
    print("LBYL ->", v1)

    # EAFP
    try:
        v2 = d[key]
    except KeyError:
        v2 = 0
    else:
        v2 += 100  # only when lookup succeeded
    print("EAFP (+ try/else) ->", v2)
    print()


def main() -> None:
    demo_for_else_find()
    demo_while_else_retry()
    demo_try_else()
    demo_eafp_vs_lbyl()


if __name__ == "__main__":
    main()

