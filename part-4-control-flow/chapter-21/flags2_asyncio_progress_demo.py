"""Ch. 21.6-21.7: flags2-style asyncio downloader with progress, errors, and concurrency limits."""

from __future__ import annotations

import argparse
import asyncio
import random
import sys
import time
from collections import Counter
from enum import Enum
from pathlib import Path
from typing import Awaitable, Iterable


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


class DownloadStatus(str, Enum):
    OK = "OK"
    NOT_FOUND = "NOT_FOUND"
    ERROR = "ERROR"


def save_flag(img: bytes, filename: str) -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    (DEST_DIR / filename).write_bytes(img)


async def _progress_iter(
    done_iter: Iterable[Awaitable[DownloadStatus]],
    *,
    total: int,
    verbose: bool,
) -> Iterable[Awaitable[DownloadStatus]]:
    # Async progress wrapper: we yield awaitables; the caller awaits each.
    if verbose:
        for aw in done_iter:
            yield aw
        return

    try:
        from tqdm import tqdm  # type: ignore[import-not-found]
    except Exception:
        done = 0
        for aw in done_iter:
            done += 1
            if done == 1 or done == total or done % max(1, total // 20) == 0:
                pct = done * 100 / total
                print(f"\rprogress: {done}/{total} ({pct:5.1f}%)", end="", flush=True)
            yield aw
        print()
    else:
        for aw in tqdm(done_iter, total=total):
            yield aw


async def _mock_get_flag(cc: str, *, delay_min: float, delay_max: float, error_rate: float) -> bytes:
    await asyncio.sleep(random.uniform(delay_min, delay_max))
    r = random.random()
    if r < error_rate / 2:
        raise FileNotFoundError(cc)
    if r < error_rate:
        raise ConnectionError(cc)
    return _MINI_GIF


async def download_one(
    cc: str,
    *,
    base_url: str,
    client,
    sem: asyncio.Semaphore,
    verbose: bool,
    mock: bool,
    delay_min: float,
    delay_max: float,
    error_rate: float,
) -> DownloadStatus:
    try:
        async with sem:
            if mock:
                img = await _mock_get_flag(
                    cc, delay_min=delay_min, delay_max=delay_max, error_rate=error_rate
                )
            else:
                url = f"{base_url}/{cc}/{cc}.gif".lower()
                resp = await client.get(url, timeout=10.0, follow_redirects=True)
                resp.raise_for_status()
                img = resp.content

        # File I/O is blocking: move it off the event loop thread.
        await asyncio.to_thread(save_flag, img, f"{cc}.gif")
    except FileNotFoundError:
        if verbose:
            print(f"{cc} -> NOT_FOUND")
        return DownloadStatus.NOT_FOUND
    except Exception as e:
        # If httpx is installed, treat 404 as NOT_FOUND; otherwise fall through to ERROR.
        if not mock:
            try:
                import httpx  # type: ignore

                if isinstance(e, httpx.HTTPStatusError) and e.response.status_code == 404:
                    if verbose:
                        print(f"{cc} -> NOT_FOUND (HTTP 404)")
                    return DownloadStatus.NOT_FOUND
                if isinstance(e, httpx.RequestError):
                    if verbose:
                        print(f"{cc} -> ERROR (RequestError)")
                    return DownloadStatus.ERROR
            except Exception:
                pass

        if verbose:
            print(f"{cc} -> ERROR ({type(e).__name__})")
        return DownloadStatus.ERROR
    else:
        if verbose:
            print(f"{cc} -> OK")
        return DownloadStatus.OK


async def supervisor(
    cc_list: list[str],
    *,
    base_url: str,
    verbose: bool,
    concur_req: int,
    mock: bool,
    delay_min: float,
    delay_max: float,
    error_rate: float,
) -> Counter[DownloadStatus]:
    cc_list = sorted(cc_list)
    total = len(cc_list)
    sem = asyncio.Semaphore(max(1, min(concur_req, total)))
    counter: Counter[DownloadStatus] = Counter()

    if mock:
        # No client needed.
        tasks = [
            download_one(
                cc,
                base_url=base_url,
                client=None,
                sem=sem,
                verbose=verbose,
                mock=True,
                delay_min=delay_min,
                delay_max=delay_max,
                error_rate=error_rate,
            )
            for cc in cc_list
        ]

        done_iter = asyncio.as_completed(tasks)
        async for aw in _progress_iter(done_iter, total=total, verbose=verbose):
            status = await aw
            counter[status] += 1
        return counter

    try:
        import httpx  # type: ignore
    except ImportError:
        print("[need httpx] Install with: pip install httpx", file=sys.stderr)
        print("Tip: run with --mock to test without network.", file=sys.stderr)
        return counter

    async with httpx.AsyncClient(headers={"User-Agent": "FluentPython-Study/1.0"}) as client:
        tasks = [
            download_one(
                cc,
                base_url=base_url,
                client=client,
                sem=sem,
                verbose=verbose,
                mock=False,
                delay_min=delay_min,
                delay_max=delay_max,
                error_rate=error_rate,
            )
            for cc in cc_list
        ]

        done_iter = asyncio.as_completed(tasks)
        async for aw in _progress_iter(done_iter, total=total, verbose=verbose):
            status = await aw
            counter[status] += 1

    return counter


def pick_codes(n: int) -> list[str]:
    n = max(1, min(n, len(POP20_CC)))
    return POP20_CC[:n]


def main() -> None:
    p = argparse.ArgumentParser(description="flags2 asyncio demo with progress/errors (Ch. 21.6-21.7)")
    p.add_argument("-n", "--count", type=int, default=20)
    p.add_argument("-c", "--concur", type=int, default=30, help="max concurrent requests")
    p.add_argument("--verbose", action="store_true", help="print per-item logs (no tqdm)")
    p.add_argument("--base-url", default=BASE_URL)
    p.add_argument("--mock", action="store_true", help="offline mode: delay + error injection")
    p.add_argument("--delay-min", type=float, default=0.05)
    p.add_argument("--delay-max", type=float, default=0.30)
    p.add_argument("--error-rate", type=float, default=0.20)
    args = p.parse_args()

    codes = pick_codes(args.count)

    async def runner() -> None:
        t0 = time.perf_counter()
        counter = await supervisor(
            codes,
            base_url=args.base_url,
            verbose=args.verbose,
            concur_req=args.concur,
            mock=args.mock,
            delay_min=max(0.0, args.delay_min),
            delay_max=max(max(0.0, args.delay_min), args.delay_max),
            error_rate=min(max(0.0, args.error_rate), 1.0),
        )
        print("counts ->", dict(counter))
        print(f"elapsed -> {time.perf_counter() - t0:.2f}s")

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()

