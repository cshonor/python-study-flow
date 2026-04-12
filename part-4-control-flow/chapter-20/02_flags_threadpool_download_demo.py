"""Ch. 20.2: Sequential vs ThreadPoolExecutor vs asyncio flag downloads (Fluent Python style)."""

from __future__ import annotations

import argparse
import asyncio
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

POP20_CC = (
    "CH IN US ID BR PK NG BD RU JP "
    "MX PH VN ET EG DE IR TR CD FR"
).split()

BASE_URL = "http://mp.ituring.com.cn/files"
DEST_DIR = Path(__file__).resolve().parent / "downloaded_flags"

# 1x1 transparent GIF — offline-friendly stand-in when the book CDN is down.
_MINI_GIF = bytes.fromhex(
    "47494638396101000100800000ffffff00000021f90401000000002c"
    "00000000010001000002024401003b"
)


def save_flag(img: bytes, filename: str) -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    (DEST_DIR / filename).write_bytes(img)


def get_flag(cc: str) -> bytes:
    url = f"{BASE_URL}/{cc}/{cc}.gif".lower()
    req = urllib.request.Request(url, headers={"User-Agent": "FluentPython-Study/1.0"})
    with urllib.request.urlopen(req, timeout=10.0) as resp:
        return resp.read()


def get_flag_mock(cc: str, delay_s: float) -> bytes:
    """Simulate network latency without hitting the CDN (URLs may 404 over time)."""
    time.sleep(delay_s)
    return _MINI_GIF


def download_one(cc: str, *, mock: bool = False, mock_delay_s: float = 0.05) -> str:
    image = get_flag_mock(cc, mock_delay_s) if mock else get_flag(cc)
    save_flag(image, f"{cc}.gif")
    print(cc, end=" ", flush=True)
    return cc


def timed(label: str, fn: Callable[[], object]) -> float:
    t0 = time.perf_counter()
    fn()
    elapsed = time.perf_counter() - t0
    print(f"\n[{label}] {elapsed:.2f}s")
    return elapsed


def download_many_sequential(cc_list: list[str], *, mock: bool, mock_delay_s: float) -> int:
    for cc in sorted(cc_list):
        download_one(cc, mock=mock, mock_delay_s=mock_delay_s)
    return len(cc_list)


def _download_one_kw(mock: bool, mock_delay_s: float) -> Callable[[str], str]:
    return lambda cc: download_one(cc, mock=mock, mock_delay_s=mock_delay_s)


def download_many_threadpool_map(
    cc_list: list[str], *, mock: bool, mock_delay_s: float
) -> int:
    fn = _download_one_kw(mock, mock_delay_s)
    with ThreadPoolExecutor() as executor:
        list(executor.map(fn, sorted(cc_list)))
    return len(cc_list)


def download_many_threadpool_futures_demo(
    cc_list: list[str], *, mock: bool, mock_delay_s: float, max_workers: int = 3
) -> int:
    """Book-style: submit + as_completed; small slice to show scheduling."""
    sample = sorted(cc_list)[:5]
    fn = _download_one_kw(mock, mock_delay_s)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        to_do = []
        for cc in sample:
            fut = executor.submit(fn, cc)
            to_do.append(fut)
            print(f"\nScheduled for {cc}: {fut!r}")

        for fut in as_completed(to_do):
            res = fut.result()
            print(f"\n{fut!r} result: {res!r}")
    return len(sample)


async def download_many_asyncio(
    cc_list: list[str], *, mock: bool, mock_delay_s: float
) -> int:
    """
    Prefer native async I/O (httpx) when available; else asyncio.to_thread fallback.
    """
    if mock:
        return await _download_many_asyncio_to_thread(
            cc_list, mock=True, mock_delay_s=mock_delay_s
        )

    try:
        import httpx
    except ImportError:
        return await _download_many_asyncio_to_thread(
            cc_list, mock=False, mock_delay_s=mock_delay_s
        )

    async with httpx.AsyncClient(
        timeout=10.0,
        follow_redirects=True,
        headers={"User-Agent": "FluentPython-Study/1.0"},
    ) as client:

        async def one(cc: str) -> str:
            url = f"{BASE_URL}/{cc}/{cc}.gif".lower()
            resp = await client.get(url)
            resp.raise_for_status()
            save_flag(resp.content, f"{cc}.gif")
            print(cc, end=" ", flush=True)
            return cc

        await asyncio.gather(*(one(cc) for cc in sorted(cc_list)))
    return len(cc_list)


async def _download_many_asyncio_to_thread(
    cc_list: list[str], *, mock: bool, mock_delay_s: float
) -> int:
    loop = asyncio.get_running_loop()
    fn = _download_one_kw(mock, mock_delay_s)

    async def one(cc: str) -> str:
        return await loop.run_in_executor(None, fn, cc)

    await asyncio.gather(*(one(cc) for cc in sorted(cc_list)))
    return len(cc_list)


def main() -> None:
    parser = argparse.ArgumentParser(description="Flag download benchmarks (Ch. 20.2)")
    parser.add_argument(
        "mode",
        nargs="?",
        default="all",
        choices=("sequential", "threadpool", "futures", "asyncio", "all"),
        help="sequential | threadpool | futures | asyncio | all",
    )
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=20,
        help="how many country codes from POP20 (max 20)",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="skip real HTTP; sleep+mini GIF per code (CDN may 404)",
    )
    parser.add_argument(
        "--mock-delay",
        type=float,
        default=0.05,
        help="seconds simulated per download in --mock mode (default 0.05)",
    )
    args = parser.parse_args()

    n = max(1, min(args.count, len(POP20_CC)))
    codes = POP20_CC[:n]
    mock = args.mock
    delay = max(0.0, args.mock_delay)

    if args.mode in ("sequential", "all"):
        timed(
            "sequential",
            lambda: download_many_sequential(codes, mock=mock, mock_delay_s=delay),
        )
    if args.mode in ("threadpool", "all"):
        timed(
            "ThreadPoolExecutor.map",
            lambda: download_many_threadpool_map(
                codes, mock=mock, mock_delay_s=delay
            ),
        )
    if args.mode in ("futures", "all"):
        print("\n--- submit + as_completed (first 5 codes) ---")
        timed(
            "ThreadPoolExecutor futures demo",
            lambda: download_many_threadpool_futures_demo(
                codes, mock=mock, mock_delay_s=delay
            ),
        )
    if args.mode in ("asyncio", "all"):
        if not mock:
            try:
                import httpx  # noqa: F401
            except ImportError:
                print(
                    "\n[asyncio] httpx not installed; using asyncio.to_thread fallback "
                    "(install httpx for book-style async client).",
                    file=sys.stderr,
                )

        async def run_async() -> None:
            await download_many_asyncio(codes, mock=mock, mock_delay_s=delay)

        timed("asyncio", lambda: asyncio.run(run_async()))


if __name__ == "__main__":
    main()
