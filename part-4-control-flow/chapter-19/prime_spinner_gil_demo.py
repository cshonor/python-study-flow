"""Ch. 19.5: show GIL impact with CPU-bound is_prime + spinner.

Usage:
  python prime_spinner_gil_demo.py thread
  python prime_spinner_gil_demo.py process
  python prime_spinner_gil_demo.py asyncio-block
  python prime_spinner_gil_demo.py asyncio-yield
  python prime_spinner_gil_demo.py asyncio-exec-proc

Optional:
  python prime_spinner_gil_demo.py thread 5000111000222021
"""

from __future__ import annotations

import asyncio
import contextlib
import itertools
import math
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import partial
from multiprocessing import Event as MpEvent
from multiprocessing import Process
from threading import Event as ThEvent
from threading import Thread


DEFAULT_N = 50_000_111_000_021  # big-ish; change via CLI if needed


def now() -> float:
    return time.perf_counter()


def _cleanup_line(status_len: int) -> None:
    blanks = " " * status_len
    print(f"\r{blanks}\r", end="", flush=True)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True


async def is_prime_async_yield(n: int, *, yield_every: int = 50_000) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    root = math.isqrt(n)
    checks = 0
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
        checks += 1
        if checks % yield_every == 0:
            await asyncio.sleep(0)
    return True


def spin_thread(msg: str, done: ThEvent) -> None:
    status = ""
    for ch in itertools.cycle(r"\|/-"):
        status = f"\r{ch} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    _cleanup_line(len(status))


def supervisor_thread(n: int) -> bool:
    done = ThEvent()
    spinner = Thread(target=spin_thread, args=("checking prime (thread)...", done))
    spinner.start()
    ok = is_prime(n)
    done.set()
    spinner.join()
    return ok


def spin_process(msg: str, done: MpEvent) -> None:
    status = ""
    for ch in itertools.cycle(r"\|/-"):
        status = f"\r{ch} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    _cleanup_line(len(status))


def supervisor_process(n: int) -> bool:
    done = MpEvent()
    spinner = Process(target=spin_process, args=("checking prime (process)...", done))
    spinner.start()
    ok = is_prime(n)
    done.set()
    spinner.join()
    return ok


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


async def supervisor_asyncio_block(n: int) -> bool:
    spinner = asyncio.create_task(spin_asyncio("checking prime (asyncio-block)..."))
    # This blocks the event loop: spinner won't advance.
    ok = is_prime(n)
    spinner.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await spinner
    return ok


async def supervisor_asyncio_yield(n: int) -> bool:
    spinner = asyncio.create_task(spin_asyncio("checking prime (asyncio-yield)..."))
    ok = await is_prime_async_yield(n)
    spinner.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await spinner
    return ok


async def supervisor_asyncio_exec_proc(n: int) -> bool:
    spinner = asyncio.create_task(spin_asyncio("checking prime (asyncio+proc)..."))
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        ok = await loop.run_in_executor(pool, partial(is_prime, n))
    spinner.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await spinner
    return ok


@dataclass(frozen=True)
class RunResult:
    mode: str
    n: int
    is_prime: bool
    elapsed_s: float


def run(mode: str, n: int) -> RunResult:
    t0 = now()
    if mode == "thread":
        ok = supervisor_thread(n)
    elif mode == "process":
        ok = supervisor_process(n)
    elif mode == "asyncio-block":
        ok = asyncio.run(supervisor_asyncio_block(n))
    elif mode == "asyncio-yield":
        ok = asyncio.run(supervisor_asyncio_yield(n))
    elif mode == "asyncio-exec-proc":
        ok = asyncio.run(supervisor_asyncio_exec_proc(n))
    else:
        raise SystemExit(
            "mode must be: thread | process | asyncio-block | asyncio-yield | asyncio-exec-proc"
        )
    return RunResult(mode=mode, n=n, is_prime=ok, elapsed_s=now() - t0)


def main(argv: list[str]) -> None:
    mode = (argv[1] if len(argv) > 1 else "thread").lower()
    n = int(argv[2]) if len(argv) > 2 else DEFAULT_N
    r = run(mode, n)
    print(f"Answer: is_prime({r.n}) -> {r.is_prime}  ({r.elapsed_s:.3f}s)")


if __name__ == "__main__":
    main(sys.argv)

