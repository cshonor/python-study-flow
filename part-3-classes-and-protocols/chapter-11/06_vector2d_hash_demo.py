"""
Demo for 06-11.7 可哈希的 Vector2d：让它能进 set 当 dict 键.md (Fluent Python 11.7).

Verifies:
- Vector2d is hashable and works in set/dict
- attempts to mutate coordinates fail (helps keep hash stable)
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
    w = Vector2d(3, 4)
    assert v == w
    assert hash(v) == hash(w)

    s = {v}
    assert v in s
    d = {v: "ok"}
    assert d[v] == "ok"

    try:
        v.x = 7  # should fail
    except Exception as e:
        print("mutate v.x ->", type(e).__name__ + ":", e)

    try:
        setattr(v, "_Vector2d__x", 7.0)  # should fail too
    except Exception as e:
        print("mutate _Vector2d__x ->", type(e).__name__ + ":", e)

    print("ok: hashable and stable ->", v, "hash:", hash(v))


if __name__ == "__main__":
    main()

