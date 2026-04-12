from __future__ import annotations

from typing import Optional, TypeGuard


def is_non_empty_str(x: object) -> TypeGuard[str]:
    return isinstance(x, str) and bool(x)


def parse_price(raw: str | float | None) -> Optional[float]:
    if raw is None:
        return None
    if isinstance(raw, float):
        return raw
    raw = raw.strip()
    if not raw:
        return None
    return float(raw)


def main() -> None:
    values: list[object] = ["", " 42.0 ", None, 3.5, "bad"]

    print("TypeGuard demo")
    for v in values:
        if is_non_empty_str(v):
            # here v is a str for type checkers
            print("non-empty str:", v, "len:", len(v))

    print("\nUnion/Optional narrowing demo")
    for v in values:
        try:
            print(v, "->", parse_price(v))  # type: ignore[arg-type]
        except Exception as e:
            print(v, "-> error:", e)


if __name__ == "__main__":
    main()

