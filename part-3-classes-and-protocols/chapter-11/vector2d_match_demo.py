"""
Demo for 07-positional-pattern-matching.md (Fluent Python 11.8).

Shows keyword pattern matching vs positional pattern matching for Vector2d.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_vector2d():
    here = Path(__file__).resolve().parent
    src = here / "vector2d_repr_demo.py"
    spec = importlib.util.spec_from_file_location("_vector2d_repr_demo", src)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {src}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Vector2d


def classify(v) -> str:
    match v:
        case v.__class__(0, 0):
            return "null"
        case v.__class__(0, _):
            return "vertical"
        case v.__class__(_, 0):
            return "horizontal"
        case v.__class__(x, y) if x == y:
            return "diagonal"
        case _:
            return "awesome"


def keyword_match(v) -> str:
    match v:
        case v.__class__(y=0):
            return "y==0"
        case v.__class__(x=0):
            return "x==0"
        case _:
            return "other"


def main() -> None:
    Vector2d = load_vector2d()
    vectors = [
        Vector2d(0, 0),
        Vector2d(0, 2),
        Vector2d(3, 0),
        Vector2d(2, 2),
        Vector2d(3, 4),
    ]

    print("=== positional patterns (needs __match_args__) ===")
    for v in vectors:
        print(v, "->", classify(v))

    print("\n=== keyword patterns (always available) ===")
    for v in vectors:
        print(v, "->", keyword_match(v))


if __name__ == "__main__":
    main()

