from __future__ import annotations

from dataclasses import dataclass
import inspect
from typing import Any, get_type_hints


def clip(text: str, max_len: int = 80) -> str:
    return text[:max_len]


@dataclass
class Node:
    value: int
    next: Node | None = None  # forward reference supported via future annotations


class Checked:
    """Demo pattern: centralize runtime type-hint reading."""

    @classmethod
    def fields(cls) -> dict[str, Any]:
        # get_type_hints resolves forward refs and returns real objects
        return get_type_hints(cls)


class User(Checked):
    name: str
    age: int


def main() -> None:
    print("raw __annotations__ (may include strings under future annotations)")
    print("clip.__annotations__ ->", clip.__annotations__)
    print("Node.__annotations__ ->", Node.__annotations__)

    print("\nget_type_hints (resolved)")
    print("get_type_hints(clip) ->", get_type_hints(clip))
    print("get_type_hints(Node) ->", get_type_hints(Node))

    print("\ninspect.get_annotations (stable API; can choose eval_str)")
    print("inspect.get_annotations(clip) ->", inspect.get_annotations(clip))
    print("inspect.get_annotations(Node) ->", inspect.get_annotations(Node))

    print("\nChecked.fields() pattern")
    print("User.fields() ->", User.fields())


if __name__ == "__main__":
    main()

