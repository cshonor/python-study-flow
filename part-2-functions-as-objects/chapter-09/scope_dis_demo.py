"""
Demo for 05-scope-traps-and-dis.md.

Shows:
- assignment in a function body makes the name local
- UnboundLocalError when reading that local before assignment
- disassembly evidence: LOAD_GLOBAL vs LOAD_FAST
"""

from __future__ import annotations

import dis

a = 10
b = 20


def f1() -> None:
    print("f1 a ->", a)


def f2() -> None:
    # Because of the assignment below, b is considered a local variable
    # throughout this function.
    print("f2 b ->", b)  # noqa: F821 (runtime will raise before assignment)
    b = 9  # type: ignore[assignment]


def f2_fixed() -> None:
    global b
    print("f2_fixed b(before) ->", b)
    b = 9
    print("f2_fixed b(after) ->", b)


def main() -> None:
    print("=== runtime behavior ===")
    f1()
    try:
        f2()
    except Exception as e:
        print(type(e).__name__ + ":", e)
    f2_fixed()

    print("\n=== disassembly (key opcodes) ===")
    print("\n-- dis(f1) --")
    dis.dis(f1)
    print("\n-- dis(f2) --")
    dis.dis(f2)


if __name__ == "__main__":
    main()

