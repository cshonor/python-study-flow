"""Ch. 21 intro: show how blocking calls freeze the event loop."""

from __future__ import annotations

import asyncio
import time


async def ticker(label: str, interval: float, ticks: int) -> None:
    for i in range(ticks):
        print(f"{label} tick {i}", flush=True)
        await asyncio.sleep(interval)


def blocking_work(seconds: float) -> str:
    time.sleep(seconds)
    return "done"


async def bad_blocking_in_event_loop() -> None:
    print("\n== BAD: blocking call inside event loop ==")
    t = asyncio.create_task(ticker("ticker", 0.2, 10))
    # This blocks the entire event loop.
    blocking_work(1.5)
    await t


async def good_offload_to_thread() -> None:
    print("\n== GOOD: offload blocking work to a thread ==")
    t = asyncio.create_task(ticker("ticker", 0.2, 10))
    await asyncio.to_thread(blocking_work, 1.5)
    await t


def main() -> None:
    asyncio.run(bad_blocking_in_event_loop())
    asyncio.run(good_offload_to_thread())


if __name__ == "__main__":
    main()

