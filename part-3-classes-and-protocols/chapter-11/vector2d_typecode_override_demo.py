"""
Demo for 09-overriding-class-attributes.md (Fluent Python 11.12).

Shows:
- instance attribute overriding a class attribute (typecode)
- subclass overriding class attribute (typecode)
- bytes length changes with typecode ('d' vs 'f')

Uses Vector2d from vector2d_v3.py.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_vector2d_v3():
    here = Path(__file__).resolve().parent
    src = here / "vector2d_v3.py"
    spec = importlib.util.spec_from_file_location("_vector2d_v3", src)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {src}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Vector2d


def main() -> None:
    Vector2d = load_vector2d_v3()

    v = Vector2d(1.1, 2.2)
    b_default = bytes(v)
    print("Vector2d.typecode ->", Vector2d.typecode)
    print("bytes(v) len ->", len(b_default), "typecode byte ->", chr(b_default[0]))

    v.typecode = "f"  # instance override
    b_inst = bytes(v)
    print("\nv.typecode (instance override) ->", v.typecode)
    print("Vector2d.typecode (unchanged) ->", Vector2d.typecode)
    print("bytes(v) len ->", len(b_inst), "typecode byte ->", chr(b_inst[0]))

    class ShortVector2d(Vector2d):
        typecode = "f"

    sv = ShortVector2d(1.1, 2.2)
    b_sub = bytes(sv)
    print("\nShortVector2d.typecode ->", ShortVector2d.typecode)
    print("repr(sv) ->", sv)
    print("bytes(sv) len ->", len(b_sub), "typecode byte ->", chr(b_sub[0]))


if __name__ == "__main__":
    main()

