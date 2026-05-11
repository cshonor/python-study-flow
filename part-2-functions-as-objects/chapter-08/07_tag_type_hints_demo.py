"""
Demo for 07-8.6 仅限位置参数与变长参数的类型注解 · 8.7 类型系统的局限性.md (Fluent Python 8.6)

Requires Python 3.8+ (positional-only parameters with /).

Also includes small runnable examples aligned with `00-全套类型提示深度展开…md` §07:
  total_sum (*args: int), init_config (**kwargs: float), KLineBar TypedDict.

Run:
  python part-2-functions-as-objects/chapter-08/07_tag_type_hints_demo.py
"""

from __future__ import annotations

from typing import TypedDict


def f(a: int, /, b: str) -> str:
    """Minimal positional-only + typed params (md §零·1)."""
    return f"{a}-{b}"


def tag(
    name: str,
    /,
    *content: str,
    class_: str | None = None,
    **attrs: str,
) -> str:
    """Minimal stand-in for the book's tag: show how /, *content, **attrs compose."""
    parts: list[str] = [repr(name)]
    parts.extend(repr(c) for c in content)
    if class_ is not None:
        parts.append(f"class_={class_!r}")
    parts.extend(f"{k}={v!r}" for k, v in sorted(attrs.items()))
    return " ".join(parts)


def total_sum(*args: int) -> int:
    """Every extra positional argument is typed as int."""
    return sum(args)


def init_config(**kwargs: float) -> None:
    """Every keyword value is typed as float (keys are str at type level)."""
    _ = kwargs


class KLineBar(TypedDict):
    open: float
    high: float
    low: float
    close: float


def fetch_bar() -> KLineBar:
    return {"open": 100.2, "high": 106.5, "low": 99.1, "close": 104.8}


def main() -> None:
    print("f(1, 'x') ->", f(1, "x"))
    print(tag("img", "hello", "world", class_="thumb", id="7", alt="x"))
    # name is positional-only; this would be a SyntaxError if attempted:
    # tag(name="img")

    print("total_sum(1, 2, 3) ->", total_sum(1, 2, 3))
    init_config(alpha=0.1, beta=2.0)
    print("fetch_bar() ->", fetch_bar())


if __name__ == "__main__":
    main()
