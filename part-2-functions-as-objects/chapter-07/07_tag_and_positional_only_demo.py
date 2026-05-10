"""
Demo for 07-7.7 从位置参数到仅限关键字参数： args、 kwargs、 与.md (Fluent Python 7.7)

Run from repo root:
  python part-2-functions-as-objects/chapter-07/07_tag_and_positional_only_demo.py
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


def demo_positional_only_slash() -> None:
    section("positional-only params: /")
    print("divmod_like(10, 3):", divmod_like(10, 3))
    try:
        print(divmod_like(a=10, b=3))  # type: ignore[call-arg]
    except TypeError as e:
        print("TypeError for keywords:", e)


def demo_beginner_walkthrough() -> None:
    """Human-language walkthrough for 07-7.7 大白话新手版 (heavily commented)."""
    section("tag(): *content, class_=, **attrs (+ beginner comments)")
    # 第一个参数 name：标签名，用位置传最直观。
    print(tag("br"))  # 自闭合风格：没有 *content，也没有多余 attrs

    # name="h1"，后面两个位置实参进入 *content 元组。
    print(tag("h1", "Hello"))

    # 多个正文段都进 *content。
    print(tag("p", "Hello", "World"))

    # class_ 在 *content 后面：调用时必须写 class_=...（仅限关键字）。
    print(tag("p", "Hello", class_="sidebar"))

    # src=、title= 等不在签名里的名字，统统进 **attrs 字典。
    print(tag("img", src="sunset.jpg", title="Sunset"))

    # 先做成 dict，再用 ** 解包成「一堆关键字实参」。
    attrs = {"src": "python.png", "title": "Python"}
    print(tag("img", **attrs))

    # 组合：位置 name + *content 两段 + class_= 关键字 + 其它 attrs。
    print(tag("p", "line1", "line2", class_="note", id="p1"))

    # / 示例：只能 divmod_like(10, 3)，不能写 a=、b=。
    print("positional-only OK:", divmod_like(10, 3))


def main() -> None:
    demo_beginner_walkthrough()
    demo_positional_only_slash()


if __name__ == "__main__":
    main()

