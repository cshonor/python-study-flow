"""Insert a standard Chinese 脚本说明 block into part-1-data-structures demo modules."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PART1 = ROOT / "part-1-data-structures"

MARKER = "脚本说明："

SNIPPET = (
    "\n\n脚本说明：\n"
    "- 教学演示：请在仓库根目录运行；终端为分步打印，请与 `part-1-data-structures` 下同章 Markdown 笔记对照。\n"
)


def _prepend_docstring(raw: str, path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    cmd = f"python {rel}"
    if path.name == "french_deck_demo.py":
        title = (
            "法式扑克牌最小示例：`collections.namedtuple` 定义单张牌，"
            "普通类 `FrenchDeck` 实现 `__len__` / `__getitem__`。"
        )
    elif path.name == "random_choice_special_methods_demo.py":
        title = "演示 `random.choice` 如何依赖 `__len__` 与 `__getitem__` 从自定义“序列”中取样。"
    else:
        title = f"配套脚本：{path.name}"

    block = f'"""{title}\n\n运行（仓库根目录）：\n  {cmd}{SNIPPET}"""\n\n'
    return block + raw


def _patch_existing_docstring(raw: str, tree: ast.Module) -> str | None:
    first = tree.body[0]
    if not isinstance(first, ast.Expr):
        return None
    val = first.value
    if not isinstance(val, ast.Constant) or not isinstance(val.value, str):
        return None
    inner = val.value
    if MARKER in inner:
        return None
    seg = ast.get_source_segment(raw, first)
    if seg is None:
        return None
    new_inner = inner.rstrip("\n") + SNIPPET
    if seg.startswith("'''"):
        new_seg = "'''" + new_inner + "'''"
    else:
        new_seg = '"""' + new_inner + '"""'
    return raw.replace(seg, new_seg, 1)


def process_file(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if MARKER in raw:
        return "skip_marker"

    tree = ast.parse(raw)
    first = tree.body[0] if tree.body else None
    if (
        isinstance(first, ast.Expr)
        and isinstance(first.value, ast.Constant)
        and isinstance(first.value.value, str)
    ):
        new_raw = _patch_existing_docstring(raw, tree)
        if new_raw is not None:
            path.write_text(new_raw, encoding="utf-8", newline="")
            return "patched_docstring"
        return "skip_nochange"

    new_raw = _prepend_docstring(raw, path)
    path.write_text(new_raw, encoding="utf-8", newline="")
    return "prepended"


def main() -> int:
    changed = 0
    for path in sorted(PART1.rglob("*.py")):
        status = process_file(path)
        if status not in ("skip_marker", "skip_nochange"):
            print(status, path.relative_to(ROOT))
            changed += 1
    print("done, changed:", changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
