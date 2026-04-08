"""
Demo for 05-formatting-display-vector2d.md (Fluent Python 11.6).

Uses the Vector2d implementation from vector2d_repr_demo.py.
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


def main() -> None:
    Vector2d = load_vector2d()
    v = Vector2d(3, 4)

    print("format(v) ->", format(v))
    print("format(v, '.2f') ->", format(v, ".2f"))
    print("format(v, 'p') ->", format(v, "p"))
    print("format(v, '.2fp') ->", format(v, ".2fp"))

    # f-string uses __format__ too
    print("f'{v:.3f}' ->", f"{v:.3f}")
    print("f'{v:.3fp}' ->", f"{v:.3fp}")


if __name__ == "__main__":
    main()

