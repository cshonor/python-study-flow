"""
Small test-style demo for Vector2d.frombytes.

Run from repo root:
  python part-3-classes-and-protocols/chapter-11/03_vector2d_frombytes_demo.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_vector2d():
    here = Path(__file__).resolve().parent
    src = here / "02_vector2d_repr_demo.py"
    spec = importlib.util.spec_from_file_location("_vector2d_repr_demo", src)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {src}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Vector2d


def main() -> None:
    Vector2d = load_vector2d()
    v = Vector2d(3, 4)
    octets = bytes(v)
    v2 = Vector2d.frombytes(octets)
    assert v == v2, (v, v2)
    print("ok:", v, "->", octets, "->", v2)


if __name__ == "__main__":
    main()

