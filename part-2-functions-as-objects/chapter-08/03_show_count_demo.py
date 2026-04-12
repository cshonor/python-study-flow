"""
Demo for 03-8.3 渐进式类型实践：从 0 注解到可检查的函数签名（show_count 实战）.md (Fluent Python 8.3)

Run from repo root:
  python part-2-functions-as-objects/chapter-08/03_show_count_demo.py
"""

from __future__ import annotations

from typing import Optional


def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
    if count == 1:
        return f"1 {singular}"
    count_str = str(count) if count else "no"
    if plural is None:
        plural = singular + "s"
    return f"{count_str} {plural}"


def main() -> None:
    assert show_count(99, "bird") == "99 birds"
    assert show_count(1, "bird") == "1 bird"
    assert show_count(0, "bird") == "no birds"
    assert show_count(3, "mouse", "mice") == "3 mice"
    print("All assertions passed.")


if __name__ == "__main__":
    main()

