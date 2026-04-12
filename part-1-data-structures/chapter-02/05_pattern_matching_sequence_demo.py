"""
Demo for 05-match-case序列模式匹配.md

Requires:
  Python 3.10+ (match/case)

Run:
  python part-1-data-structures/chapter-02/05_pattern_matching_sequence_demo.py

脚本说明：
- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def safe_text(s: str) -> str:
    """Render Unicode safely in non-UTF8 consoles (e.g. GBK)."""
    return s.encode("unicode_escape").decode("ascii")


class InvalidCommand(Exception):
    pass


class Symbol(str):
    """A tiny stand-in for Scheme symbols (demo only)."""


@dataclass(frozen=True, slots=True)
class Procedure:
    parms: list[Symbol]
    body: list[object]
    env: dict[Symbol, object]


class Robot:
    def __init__(self) -> None:
        self.events: list[str] = []

    def beep(self, times: int, frequency: int) -> None:
        self.events.append(f"beep(times={times}, frequency={frequency})")

    def rotate_neck(self, angle: int) -> None:
        self.events.append(f"neck(angle={angle})")

    def set_led_brightness(self, ident: int, intensity: int) -> None:
        self.events.append(f"led[{ident}].brightness({intensity})")

    def set_led_color(self, ident: int, r: int, g: int, b: int) -> None:
        self.events.append(f"led[{ident}].color({r},{g},{b})")

    def handle_command(self, message: object) -> None:
        match message:
            case ["BEEPER", frequency, times]:
                self.beep(times, frequency)
            case ["NECK", angle]:
                self.rotate_neck(angle)
            case ["LED", ident, intensity]:
                self.set_led_brightness(ident, intensity)
            case ["LED", ident, red, green, blue]:
                self.set_led_color(ident, red, green, blue)
            case _:
                raise InvalidCommand(message)


def demo_tiny_evaluator_forms() -> None:
    section("4) tiny evaluator-style matching (quote/if/lambda/define)")
    env: dict[Symbol, object] = {}

    def eval_form(exp: object) -> object:
        match exp:
            case ["quote", value]:
                return value
            case ["define", Symbol() as name, value]:
                env[name] = eval_form(value)
                return None
            case ["if", test, consequence, alternative]:
                return eval_form(consequence) if eval_form(test) else eval_form(alternative)
            case ["lambda", [*parms], *body] if body:
                # demo only: build a minimal Procedure object
                return Procedure(parms, body, env)
            case ["define", [Symbol() as name, *parms], *body] if body:
                env[name] = Procedure(parms, body, env)
                return None
            case _:
                raise SyntaxError(f"bad form: {exp!r}")

    print("quote:", eval_form(["quote", 42]))
    eval_form(["define", Symbol("x"), ["quote", 10]])
    print("define x ->", env[Symbol("x")])
    print("if:", eval_form(["if", ["quote", True], ["quote", "yes"], ["quote", "no"]]))
    print(
        "lambda:",
        eval_form(["lambda", [Symbol("n")], ["quote", "body1"], ["quote", "body2"]]),
    )
    eval_form(
        [
            "define",
            [Symbol("square"), Symbol("x")],
            ["quote", "(* x x)"],
        ]
    )
    print("define (square x) ->", env[Symbol("square")])


def demo_command_matching() -> None:
    section("1) command matching with sequence patterns")
    bot = Robot()
    commands: list[object] = [
        ["BEEPER", 440, 3],
        ["NECK", 90],
        ["LED", 1, 128],
        ["LED", 2, 255, 10, 0],
    ]
    for cmd in commands:
        bot.handle_command(cmd)

    for e in bot.events:
        print(e)
    assert bot.events[0].startswith("beep(")


def demo_guard_and_nested_pattern() -> None:
    section("2) nested pattern + guard (metro_areas)")
    metro_areas = [
        ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
        ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889)),
        ("Mexico City", "MX", 20.142, (19.433333, -99.133333)),
        ("New York-Newark", "US", 20.104, (40.808611, -74.020386)),
        ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
    ]

    print(f"{'':15} | {'latitude':>9} | {'longitude':>9}")
    for record in metro_areas:
        match record:
            case [name, _, _, (lat, lon)] if lon <= 0:
                print(f"{safe_text(name):15} | {lat:9.4f} | {lon:9.4f}")
            case _:
                pass


def demo_star_rest_ordering_pitfall() -> None:
    section("3) ordering pitfall: *rest can swallow specific cases")
    message = ["LED", 7, 1, 2, 3]

    def bad(m: object) -> str:
        match m:
            case ["LED", ident, *rest]:
                return f"generic LED ident={ident} rest={rest}"
            case ["LED", ident, r, g, b]:
                return f"RGB LED ident={ident} rgb={r,g,b}"
            case _:
                return "unknown"

    def good(m: object) -> str:
        match m:
            case ["LED", ident, r, g, b]:
                return f"RGB LED ident={ident} rgb={r,g,b}"
            case ["LED", ident, *rest]:
                return f"generic LED ident={ident} rest={rest}"
            case _:
                return "unknown"

    print("bad :", bad(message))
    print("good:", good(message))
    assert bad(message).startswith("generic LED")
    assert good(message).startswith("RGB LED")


def main() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit("This demo requires Python 3.10+ for match/case.")

    demo_command_matching()
    demo_guard_and_nested_pattern()
    demo_star_rest_ordering_pitfall()
    demo_tiny_evaluator_forms()


if __name__ == "__main__":
    main()

