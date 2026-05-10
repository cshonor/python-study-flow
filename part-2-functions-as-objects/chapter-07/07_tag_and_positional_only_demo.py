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


def demo_args_vs_kwargs_plain() -> None:
    """Exact minimal `f(*args, **kwargs)` from 07-7.7 大白话 §9·三."""

    def f(*args: object, **kwargs: object) -> None:
        print("args:", args)
        print("kwargs:", kwargs)

    section("*args vs **kwargs: f(1,2,3, name=..., city=...)")
    # 与笔记「李四 / 北京」同结构；此处用 ASCII 避免 Windows 控制台编码乱码。
    f(1, 2, 3, name="Li", city="Beijing")


def demo_parameter_kinds_minimal() -> None:
    """One tiny runnable example per parameter kind (07-7.7 零·二·附)."""

    def pos_only(a: int, b: int, /) -> int:
        return a + b

    def pos_or_kw(c: int, d: int = 0) -> tuple[int, int]:
        return (c, d)

    def with_var_pos(first: int, *rest: int) -> tuple[int, tuple[int, ...]]:
        return (first, rest)

    def kw_after_star(*a: int, e: int, f: int = 100) -> tuple[tuple[int, ...], int, int]:
        return (a, e, f)

    def collect_kw(**kw: str) -> dict[str, str]:
        return kw

    section("five parameter kinds: minimal examples")
    print("1 positional-only:", pos_only(7, 8))
    print("2 pos-or-kw (keywords):", pos_or_kw(c=3, d=4))
    print("2 pos-or-kw (positional + default):", pos_or_kw(3))
    print("3 *args:", with_var_pos(1, 2, 3))
    print("4 keyword-only after *:", kw_after_star(1, 2, 3, e=4))
    print("4 keyword-only (e and f):", kw_after_star(9, e=1, f=2))
    print("5 **kwargs:", collect_kw(a="x", b="y"))


def demo_full_parameter_template() -> None:
    """The full signature from 零·二 / 零·二·附 (Python 3.8+)."""

    def func(
        a: int,
        b: int,
        /,
        c: int,
        d: int = 0,
        *args: int,
        e: int,
        f: int = 1,
        **kwargs: int,
    ) -> None:
        print(
            "binding:",
            {"a": a, "b": b, "c": c, "d": d, "args": args, "e": e, "f": f, "kwargs": kwargs},
        )

    section("full parameter template: func(a,b,/,c,d=0,*args,e,f=1,**kwargs)")
    func(1, 2, 3, 4, 5, 6, e=7, f=8, x=9, y=10)
    try:
        func(1, 2, 3, 4, 5)  # type: ignore[call-arg]
    except TypeError as ex:
        print("missing keyword e ->", ex)


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
    demo_args_vs_kwargs_plain()
    demo_parameter_kinds_minimal()
    demo_full_parameter_template()
    demo_positional_only_slash()


if __name__ == "__main__":
    main()

