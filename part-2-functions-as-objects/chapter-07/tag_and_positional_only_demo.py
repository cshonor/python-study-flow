"""
Demo for 07-advanced-argument-features.md (Fluent Python 7.7)

Run from repo root:
  python part-2-functions-as-objects/chapter-07/tag_and_positional_only_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def tag(name: str, *content: str, class_: str | None = None, **attrs: str) -> str:
    """Generate one or more HTML tags."""
    if class_ is not None:
        attrs["class"] = class_

    # attrs is a dict; check it directly (not a generator).
    if attrs:
        pairs = [f'{k}="{v}"' for k, v in sorted(attrs.items())]
        start_tag = f"<{name} {' '.join(pairs)}>"
    else:
        start_tag = f"<{name}>"

    if content:
        body = "\n".join(content)
        return f"{start_tag}\n{body}\n</{name}>"
    return start_tag


def divmod_like(a: int, b: int, /) -> tuple[int, int]:
    return (a // b, a % b)


def demo_tag_calls() -> None:
    section("tag(): *content, class_=, **attrs")
    print(tag("br"))
    print(tag("h1", "Hello"))
    print(tag("p", "Hello", "World"))
    print(tag("p", "Hello", class_="sidebar"))
    print(tag("img", src="sunset.jpg", title="Sunset"))

    attrs = {"src": "python.png", "title": "Python"}
    print(tag("img", **attrs))


def demo_positional_only_slash() -> None:
    section("positional-only params: /")
    print("divmod_like(10, 3):", divmod_like(10, 3))
    try:
        print(divmod_like(a=10, b=3))  # type: ignore[call-arg]
    except TypeError as e:
        print("TypeError for keywords:", e)


def main() -> None:
    demo_tag_calls()
    demo_positional_only_slash()


if __name__ == "__main__":
    main()

