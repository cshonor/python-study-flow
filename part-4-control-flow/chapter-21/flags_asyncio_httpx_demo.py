"""Ch. 21.4-21.5: Awaitables + asyncio async HTTP download demo (httpx, with mock fallback)."""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path
from typing import Iterable


POP20_CC = (
    "CH IN US ID BR PK NG BD RU JP "
    "MX PH VN ET EG DE IR TR CD FR"
).split()

BASE_URL = "http://mp.ituring.com.cn/files"
DEST_DIR = Path(__file__).resolve().parent / "downloaded_flags"

# 1x1 transparent GIF — used for --mock mode.
_MINI_GIF = bytes.fromhex(
    "47494638396101000100800000ffffff00000021f90401000000002c"
    "00000000010001000002024401003b"
)


def save_flag(img: bytes, filename: str) -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    (DEST_DIR / filename).write_bytes(img)


async def awaitable_vs_task_demo() -> None:
    async def work(n: int) -> int:
        await asyncio.sleep(0.05)
        return n * 10

    print("== awaitable vs Task ==")
    # Direct await: sequential (this coroutine waits right away)
    a = await work(1)
    print("await work(1) ->", a)

    # create_task: schedule concurrently
    t2 = asyncio.create_task(work(2))
    t3 = asyncio.create_task(work(3))
    print("created tasks ->", type(t2).__name__, type(t3).__name__)
    b, c = await asyncio.gather(t2, t3)
    print("await gather(tasks) ->", (b, c))
    print()


async def _download_one_mock(cc: str, delay_s: float) -> str:
    await asyncio.sleep(delay_s)
    save_flag(_MINI_GIF, f"{cc}.gif")
    return cc


async def _download_one_httpx(client, cc: str, base_url: str) -> str:
    url = f"{base_url}/{cc}/{cc}.gif".lower()
    resp = await client.get(url, timeout=10.0, follow_redirects=True)
    resp.raise_for_status()
    save_flag(resp.content, f"{cc}.gif")
    return cc


async def download_many(
    cc_list: list[str],
    *,
    base_url: str,
    mock: bool,
    mock_delay: float,
    mode: str,
) -> int:
    cc_list = sorted(cc_list)

    if mock:
        coros = [_download_one_mock(cc, mock_delay) for cc in cc_list]
        if mode == "gather":
            res = await asyncio.gather(*coros)
            print(" ".join(res), flush=True)
            return len(res)
        # as_completed
        done = 0
        for coro in asyncio.as_completed(coros):
            cc = await coro
            print(cc, end=" ", flush=True)
            done += 1
        print()
        return done

    try:
        import httpx  # type: ignore
    except ImportError:
        print("[need httpx] Install with: pip install httpx", file=sys.stderr)
        print("Tip: run with --mock to test without network.", file=sys.stderr)
        return 0

    async with httpx.AsyncClient(headers={"User-Agent": "FluentPython-Study/1.0"}) as client:
        coros = [_download_one_httpx(client, cc, base_url) for cc in cc_list]
        if mode == "gather":
            res = await asyncio.gather(*coros)
            print(" ".join(res), flush=True)
            return len(res)
        done = 0
        for coro in asyncio.as_completed(coros):
            cc = await coro
            print(cc, end=" ", flush=True)
            done += 1
        print()
        return done


def pick_codes(n: int) -> list[str]:
    n = max(1, min(n, len(POP20_CC)))
    return POP20_CC[:n]


def main() -> None:
    p = argparse.ArgumentParser(description="asyncio + httpx flags demo (Ch. 21.4-21.5)")
    p.add_argument("--mode", choices=("gather", "as_completed"), default="as_completed")
    p.add_argument("-n", "--count", type=int, default=20)
    p.add_argument("--base-url", default=BASE_URL)
    p.add_argument("--mock", action="store_true", help="offline mode: sleep + mini GIF")
    p.add_argument("--mock-delay", type=float, default=0.05)
    p.add_argument("--no-awaitable-demo", action="store_true")
    args = p.parse_args()

    async def runner() -> None:
        if not args.no_awaitable_demo:
            await awaitable_vs_task_demo()

        codes = pick_codes(args.count)
        t0 = time.perf_counter()
        n = await download_many(
            codes,
            base_url=args.base_url,
            mock=args.mock,
            mock_delay=max(0.0, args.mock_delay),
            mode=args.mode,
        )
        print(f"[{args.mode}] downloaded: {n}  elapsed: {time.perf_counter() - t0:.2f}s")

    asyncio.run(runner())


if __name__ == "__main__":
    main()

