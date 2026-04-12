"""
Demo for 04-10.4 命令模式：把“面向对象回调”还原成 Python 回调.md (Fluent Python 10.4).

Includes:
- Invoker (MenuItem) holding a callable command
- Receiver (Document) implementing operations
- simple commands as functions / lambdas
- MacroCommand (callable object combining commands)
- minimal undo stack with UndoableCommand
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass


class Document:
    def __init__(self) -> None:
        self.text = ""
        self.is_open = False

    def open(self) -> None:
        self.is_open = True
        print("Document.open()")

    def close(self) -> None:
        self.is_open = False
        print("Document.close()")

    def paste(self, s: str) -> None:
        self.text += s
        print(f"Document.paste({s!r}) -> text={self.text!r}")

    def delete_last(self, n: int) -> str:
        removed = self.text[-n:]
        self.text = self.text[:-n]
        print(f"Document.delete_last({n}) -> removed={removed!r} text={self.text!r}")
        return removed


@dataclass(frozen=True)
class MenuItem:
    label: str
    command: Callable[[], None]

    def click(self) -> None:
        print(f"[Menu] {self.label}")
        self.command()


class MacroCommand:
    def __init__(self, commands: list[Callable[[], None]] | tuple[Callable[[], None], ...]) -> None:
        self.commands = list(commands)

    def __call__(self) -> None:
        for cmd in self.commands:
            cmd()


@dataclass
class UndoableCommand:
    do: Callable[[], None]
    undo: Callable[[], None]

    def __call__(self) -> None:
        self.do()


class UndoStack:
    def __init__(self) -> None:
        self._stack: list[Callable[[], None]] = []

    def push_undo(self, undo: Callable[[], None]) -> None:
        self._stack.append(undo)

    def undo(self) -> None:
        if not self._stack:
            print("[Undo] nothing to undo")
            return
        action = self._stack.pop()
        print("[Undo] running undo")
        action()


def main() -> None:
    doc = Document()
    undo_stack = UndoStack()

    # simple commands (functions/lambdas)
    open_cmd = lambda: doc.open()
    close_cmd = lambda: doc.close()

    def paste_hello() -> None:
        doc.paste("hello ")
        undo_stack.push_undo(lambda: doc.delete_last(len("hello ")))

    def paste_world() -> None:
        doc.paste("world")
        undo_stack.push_undo(lambda: doc.delete_last(len("world")))

    # invoker
    menu = [
        MenuItem("Open", open_cmd),
        MenuItem("Paste hello", paste_hello),
        MenuItem("Paste world", paste_world),
        MenuItem("Close", close_cmd),
    ]

    print("=== simple commands ===")
    for item in menu:
        item.click()

    print("\n=== undo last two operations ===")
    undo_stack.undo()
    undo_stack.undo()
    undo_stack.undo()

    print("\n=== macro command (callable object) ===")
    macro = MacroCommand([open_cmd, paste_hello, paste_world, close_cmd])
    MenuItem("Open+Paste+Close (macro)", macro).click()

    print("\n=== explicit undoable command object ===")
    def do_upper() -> None:
        old = doc.text
        doc.text = doc.text.upper()
        print("do_upper ->", doc.text)
        undo_stack.push_undo(lambda: setattr(doc, "text", old))

    upper = UndoableCommand(do=do_upper, undo=lambda: None)  # undo is pushed into stack in do_upper
    upper()
    undo_stack.undo()
    print("text ->", doc.text)


if __name__ == "__main__":
    main()

