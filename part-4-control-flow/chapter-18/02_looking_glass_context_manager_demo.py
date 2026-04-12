"""Ch. 18.2: Context managers & with blocks — protocol + contextlib tools."""

from __future__ import annotations

import contextlib
import os
import sys
import tempfile
from collections.abc import Generator, Iterable, Iterator
from contextlib import ExitStack
from pathlib import Path
from typing import IO, TypeVar


T = TypeVar("T")


class LookingGlass:
    """Reverse writes to stdout inside the with block."""

    def __enter__(self) -> str:
        self._original_write = sys.stdout.write
        sys.stdout.write = self._reverse_write  # type: ignore[method-assign]
        return "JABBERWOCKY"

    def _reverse_write(self, text: str) -> int:
        return self._original_write(text[::-1])  # type: ignore[attr-defined]

    def __exit__(self, exc_type, exc_value, traceback) -> bool | None:
        sys.stdout.write = self._original_write  # type: ignore[attr-defined]
        if exc_type is ZeroDivisionError:
            print("Please DO NOT divide by zero!")
            return True
        return None


@contextlib.contextmanager
def looking_glass() -> Generator[str, None, None]:
    original_write = sys.stdout.write

    def reverse_write(text: str) -> int:
        return original_write(text[::-1])

    sys.stdout.write = reverse_write  # type: ignore[method-assign]
    msg = ""
    try:
        yield "JABBERWOCKY"
    except ZeroDivisionError:
        msg = "Please DO NOT divide by zero!"
    finally:
        sys.stdout.write = original_write  # type: ignore[method-assign]
        if msg:
            print(msg)


@contextlib.contextmanager
def inplace(
    path: str | os.PathLike[str],
    *,
    encoding: str = "utf-8",
) -> Generator[tuple[IO[str], IO[str]], None, None]:
    """
    Minimal in-place edit helper:
    - opens input file for reading
    - opens a temporary file in same directory for writing
    - on success, atomically replaces original with temp
    """

    src = Path(path)
    tmp_name = None
    out_fh: IO[str] | None = None

    with src.open("r", encoding=encoding, newline="") as in_fh:
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding=encoding,
                newline="",
                delete=False,
                dir=str(src.parent),
                prefix=src.name + ".",
                suffix=".tmp",
            ) as tmp:
                tmp_name = tmp.name
                out_fh = tmp
                yield (in_fh, out_fh)
        except BaseException:
            if tmp_name:
                with contextlib.suppress(OSError):
                    os.unlink(tmp_name)
            raise

    if not tmp_name:
        raise RuntimeError("temp file was not created")

    os.replace(tmp_name, src)


def chunked(it: Iterable[T], n: int) -> Iterator[list[T]]:
    buf: list[T] = []
    for x in it:
        buf.append(x)
        if len(buf) == n:
            yield buf
            buf = []
    if buf:
        yield buf


def demo_protocol_class() -> None:
    print("== class-based context manager ==")
    with LookingGlass() as what:
        print("Alice, Kitty and Snowdrop.")
        print("what ->", what)
    print()

    print("== class-based: swallowing ZeroDivisionError ==")
    with LookingGlass():
        print("Before 1/0")
        _ = 1 / 0
        print("Unreachable")
    print("After 1/0 (exception swallowed)")
    print()


def demo_contextmanager_decorator() -> None:
    print("== @contextmanager generator-based ==")
    with looking_glass() as what:
        print("The time has come.")
        print("what ->", what)
    print()

    print("== generator-based: swallowing ZeroDivisionError ==")
    with looking_glass():
        print("Before 1/0")
        _ = 1 / 0
        print("Unreachable")
    print("After 1/0 (exception swallowed)")
    print()


def demo_contextlib_helpers() -> None:
    print("== contextlib.suppress / nullcontext ==")
    with contextlib.suppress(FileNotFoundError):
        os.unlink("definitely-not-here.tmp")
    print("suppress(FileNotFoundError) done")

    verbose = False
    with (contextlib.nullcontext() if not verbose else LookingGlass()):
        print("nullcontext keeps output normal")
    print()


def demo_parenthesized_multi_with(tmp_dir: Path) -> None:
    print("== parenthesized multi-with (Py 3.10+) ==")
    a = tmp_dir / "a.txt"
    b = tmp_dir / "b.txt"
    with (
        a.open("w", encoding="utf-8") as fa,
        b.open("w", encoding="utf-8") as fb,
    ):
        fa.write("A\n")
        fb.write("B\n")
    print("wrote", a.name, "and", b.name)
    print()


def demo_exitstack(tmp_dir: Path) -> None:
    print("== ExitStack: open many files dynamically ==")
    paths = [tmp_dir / f"n{i}.txt" for i in range(3)]
    with ExitStack() as stack:
        fhs = [stack.enter_context(p.open("w", encoding="utf-8")) for p in paths]
        for i, fh in enumerate(fhs):
            fh.write(f"file {i}\n")
    print("wrote", ", ".join(p.name for p in paths))
    print()


def demo_inplace(tmp_dir: Path) -> None:
    print("== inplace edit: rewrite file safely ==")
    p = tmp_dir / "data.txt"
    p.write_text("a\nb\nc\n", encoding="utf-8")

    with inplace(p) as (infh, outfh):
        for batch in chunked((line.strip() for line in infh), 2):
            outfh.write(",".join(batch) + "\n")

    print("after inplace edit ->")
    print(p.read_text(encoding="utf-8"), end="")
    print()


def main() -> None:
    demo_protocol_class()
    demo_contextmanager_decorator()
    demo_contextlib_helpers()

    with tempfile.TemporaryDirectory(prefix="ch18-ctx-") as d:
        tmp_dir = Path(d)
        demo_parenthesized_multi_with(tmp_dir)
        demo_exitstack(tmp_dir)
        demo_inplace(tmp_dir)


if __name__ == "__main__":
    main()

