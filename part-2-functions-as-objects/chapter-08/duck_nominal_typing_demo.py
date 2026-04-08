"""
Demo for 04-types-defined-by-operations.md (Fluent Python 8.4)

Run from repo root:
  python part-2-functions-as-objects/chapter-08/duck_nominal_typing_demo.py

Optional:
  mypy part-2-functions-as-objects/chapter-08/duck_nominal_typing_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


class Bird:
    pass


class Duck(Bird):
    def quack(self) -> None:
        print("Quack!")


def alert(birdie):
    """No type hints: mypy typically does not check the body (gradual typing)."""
    birdie.quack()


def alert_duck(birdie: Duck) -> None:
    birdie.quack()


def alert_bird(birdie: Bird) -> None:
    birdie.quack()  # error: Bird has no attribute "quack"


def try_call(label: str, fn, arg) -> None:
    try:
        print(f"{label} -> ", end="")
        fn(arg)
        print("ok")
    except Exception as e:
        print(type(e).__name__ + ":", e)


def main() -> None:
    daffy = Duck()
    woody = Bird()

    section("Case 1: Duck instance (daffy)")
    try_call("alert", alert, daffy)
    try_call("alert_duck", alert_duck, daffy)
    try_call("alert_bird", alert_bird, daffy)

    section("Case 2: Bird instance (woody)")
    try_call("alert", alert, woody)
    # Direct calls (not via generic helper) so mypy reports incompatible arg for alert_duck(woody).
    try:
        print("alert_duck -> ", end="")
        alert_duck(woody)
        print("ok")
    except Exception as e:
        print(type(e).__name__ + ":", e)
    try:
        print("alert_bird -> ", end="")
        alert_bird(woody)
        print("ok")
    except Exception as e:
        print(type(e).__name__ + ":", e)


if __name__ == "__main__":
    main()
