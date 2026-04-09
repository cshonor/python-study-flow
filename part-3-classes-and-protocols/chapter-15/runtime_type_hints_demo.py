from __future__ import annotations

import inspect
from typing import Any, get_type_hints


def add(a: int, b: int) -> int:
    return a + b


def validate_call(fn, /, *args: Any, **kwargs: Any) -> Any:
    """Very small demo: read annotations at runtime.

    This is NOT a full validator; it shows that annotations are accessible
    and can drive lightweight checks/metadata use.
    """

    hints = get_type_hints(fn)
    sig = inspect.signature(fn)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()

    for name, value in bound.arguments.items():
        expected = hints.get(name)
        if expected is None:
            continue
        if not isinstance(value, expected):
            raise TypeError(f"{name}: expected {expected}, got {type(value)}")

    result = fn(*args, **kwargs)
    expected_ret = hints.get("return")
    if expected_ret is not None and not isinstance(result, expected_ret):
        raise TypeError(f"return: expected {expected_ret}, got {type(result)}")
    return result


def main() -> None:
    print("type hints:", get_type_hints(add))
    print("validate_call(add, 1, 2) ->", validate_call(add, 1, 2))
    try:
        validate_call(add, "1", 2)  # type: ignore[arg-type]
    except TypeError as e:
        print("validate_call(add, '1', 2) ->", e)


if __name__ == "__main__":
    main()

