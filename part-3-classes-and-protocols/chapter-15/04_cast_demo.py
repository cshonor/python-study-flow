from __future__ import annotations

from collections.abc import Sequence
from typing import Optional, cast


def find_first_str(a: list[object]) -> str:
    index = next(i for i, x in enumerate(a) if isinstance(x, str))
    # a[index] is typed as object, but our logic guarantees it's str.
    return cast(str, a[index])


def get_first_socket_name(sockets: Optional[Sequence[str]]) -> str:
    # Imagine a third-party stub typed this as Optional, but your code guarantees non-None.
    sock_list = cast(Sequence[str], sockets)
    return sock_list[0]


def main() -> None:
    print("cast() is a static-only hint")
    data: list[object] = [1, None, "hello", 3.14]
    print("first str ->", find_first_str(data))

    print("\ncast() can hide bugs if you lie")
    try:
        # This is WRONG: cast does not make None indexable at runtime.
        bad = cast(list[int], None)
        print(bad[0])
    except TypeError as e:
        print("cast(list[int], None)[0] ->", e)

    print("\nOptional container example (simulated)")
    try:
        print(get_first_socket_name(["127.0.0.1:8000"]))
        # This will crash: cast didn't validate non-None.
        print(get_first_socket_name(None))
    except TypeError as e:
        print("get_first_socket_name(None) ->", e)


if __name__ == "__main__":
    main()

