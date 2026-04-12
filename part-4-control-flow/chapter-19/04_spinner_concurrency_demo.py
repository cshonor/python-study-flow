"""Ch. 19.4: spinner "hello concurrency" with threads/processes/asyncio.

Usage:
  python 04_spinner_concurrency_demo.py thread
  python 04_spinner_concurrency_demo.py process
  python 04_spinner_concurrency_demo.py asyncio
"""

from __future__ import annotations

import asyncio
import contextlib
import itertools
import sys
import time
from multiprocessing import Event as MpEvent
from multiprocessing import Process
from threading import Event as ThEvent
from threading import Thread


def _cleanup_line(status_len: int) -> None:
    blanks = " " * status_len
    print(f"\r{blanks}\r", end="", flush=True)


def slow() -> int:
    time.sleep(3)
    return 42


def spin_thread(msg: str, done: ThEvent) -> None:
    status = ""
    for ch in itertools.cycle(r"\|/-"):
        status = f"\r{ch} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    _cleanup_line(len(status))


def supervisor_thread() -> int:
    done = ThEvent()
    spinner = Thread(target=spin_thread, args=("thinking!", done))
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


def spin_process(msg: str, done: MpEvent) -> None:
    status = ""
    for ch in itertools.cycle(r"\|/-"):
        status = f"\r{ch} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    _cleanup_line(len(status))


def supervisor_process() -> int:
    done = MpEvent()
    spinner = Process(target=spin_process, args=("thinking!", done))
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


async def spin_asyncio(msg: str) -> None:
    status = ""
    try:
        for ch in itertools.cycle(r"\|/-"):
            status = f"\r{ch} {msg}"
            print(status, end="", flush=True)
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        _cleanup_line(len(status))
        raise


async def slow_asyncio() -> int:
    await asyncio.sleep(3)
    return 42


async def supervisor_asyncio() -> int:
    spinner = asyncio.create_task(spin_asyncio("thinking!"))
    result = await slow_asyncio()
    spinner.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await spinner
    return result


def main(argv: list[str]) -> None:
    mode = (argv[1] if len(argv) > 1 else "thread").lower()
    if mode == "thread":
        result = supervisor_thread()
    elif mode == "process":
        result = supervisor_process()
    elif mode in {"asyncio", "async"}:
        result = asyncio.run(supervisor_asyncio())
    else:
        raise SystemExit("mode must be: thread | process | asyncio")

    print(f"Answer: {result}")


if __name__ == "__main__":
    main(sys.argv)

