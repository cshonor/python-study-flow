"""Ch. 20.4: Understand Executor.map scheduling vs as_completed."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from time import perf_counter, sleep, strftime


def display(*args: object) -> None:
    print(strftime("[%H:%M:%S]"), *args, flush=True)


def loiter(n: int) -> int:
    indent = "\t" * n
    display(f"{indent}loiter({n}): doing nothing for {n}s...")
    sleep(n)
    display(f"{indent}loiter({n}): done.")
    return n * 10


def demo_map() -> None:
    display("== map: results are yielded in input order ==")
    with ThreadPoolExecutor(max_workers=3) as ex:
        t0 = perf_counter()
        results = ex.map(loiter, range(5))
        display("results iterator created (no blocking yet).")
        display("Waiting for individual results (input order):")
        for i, result in enumerate(results):
            display(f"result {i}: {result}")
        display(f"[map] total: {perf_counter() - t0:.2f}s")
    print()


def demo_as_completed() -> None:
    display("== submit + as_completed: results in completion order ==")
    with ThreadPoolExecutor(max_workers=3) as ex:
        t0 = perf_counter()
        futures = [ex.submit(loiter, n) for n in range(5)]
        display("futures scheduled.")
        for fut in as_completed(futures):
            display("completed:", fut.result())
        display(f"[as_completed] total: {perf_counter() - t0:.2f}s")
    print()


def main() -> None:
    display("Script starting.")
    demo_map()
    demo_as_completed()


if __name__ == "__main__":
    main()

