"""
Demo for 04-bytes-and-bytearray.md

Run:
  python part-1-data-structures/chapter-04/bytes_bytearray_demo.py
"""

from __future__ import annotations


def section(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def demo_bytes_index_slice() -> None:
    section("1) bytes: index -> int, slice -> bytes")
    b = b"cafe"
    print("b:", b)
    print("b[0]:", b[0], "type:", type(b[0]).__name__)
    print("b[0:1]:", b[0:1], "type:", type(b[0:1]).__name__)
    assert isinstance(b[0], int)
    assert isinstance(b[0:1], bytes)


def demo_literal_ascii_only() -> None:
    section("2) bytes literal is for ASCII (use encoding for others)")
    b_cafe = b"cafe"
    print("b_cafe:", b_cafe)
    # NOTE: don't include b'咖啡' here; that would be a SyntaxError at parse time.
    print("To make bytes from non-ASCII text, use 'text'.encode('utf-8').")


def demo_encode_decode() -> None:
    section("3) str <-> bytes: encode/decode with explicit encoding")
    text = "你好"
    raw = text.encode("utf-8")
    print("text (ascii-safe):", ascii(text))
    print("raw bytes:", raw)
    print("raw hex:", raw.hex(" "))
    back = raw.decode("utf-8")
    print("back (ascii-safe):", ascii(back))
    assert back == text


def demo_bytes_immutable_bytearray_mutable() -> None:
    section("4) bytes is immutable; bytearray is mutable")
    b = b"cafe"
    print("bytes:", b)
    try:
        b[0] = 67  # type: ignore[misc]
    except TypeError as e:
        print("bytes assignment -> TypeError:", e)

    ba = bytearray(b"cafe")
    print("bytearray before:", ba)
    ba[0] = 67  # 'C'
    print("bytearray after :", ba)
    assert ba == bytearray(b"Cafe")


def demo_fromhex_and_hex() -> None:
    section("5) fromhex() and hex() are practical for debugging")
    raw = bytes.fromhex("1B 48 CE AB")
    print("raw:", raw)
    print("raw.hex(' '):", raw.hex(" "))
    assert raw == b"\x1bH\xce\xab"


def main() -> None:
    demo_bytes_index_slice()
    demo_literal_ascii_only()
    demo_encode_decode()
    demo_bytes_immutable_bytearray_mutable()
    demo_fromhex_and_hex()


if __name__ == "__main__":
    main()

