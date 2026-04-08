"""
Demo for 07-positional-varargs-and-type-limits.md (Fluent Python 8.6)

Requires Python 3.8+ (positional-only parameters with /).

Run:
  python part-2-functions-as-objects/chapter-08/tag_type_hints_demo.py
"""

from __future__ import annotations


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


def main() -> None:
    print(tag("img", "hello", "world", class_="thumb", id="7", alt="x"))
    # name is positional-only; this would be a SyntaxError if attempted:
    # tag(name="img")


if __name__ == "__main__":
    main()
