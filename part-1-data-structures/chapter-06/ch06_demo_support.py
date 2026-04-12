"""
第 6 章各演示脚本的公用小工具（分节标题、控制台安全打印）。

脚本说明：
- 由 `02`–`07` 及 `01` 导航脚本导入；勿单独当作章节演示运行。
"""

from __future__ import annotations


def section(title: str) -> None:
    """打印分节标题（等宽分隔线）。"""
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def safe(obj: object) -> object:
    """窄控制台（如 Windows GBK）下安全打印：字符串用 ascii() 转义。"""
    return ascii(obj) if isinstance(obj, str) else obj
