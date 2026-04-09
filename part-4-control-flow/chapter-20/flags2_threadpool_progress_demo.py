"""Ch. 20.5: Progress + error handling with ThreadPoolExecutor and as_completed (flags2-style)."""

from __future__ import annotations

import argparse
import random
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from enum import Enum
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


class DownloadStatus(str, Enum):
    OK = "OK"
    NOT_FOUND = "NOT_FOUND"
    ERROR = "ERROR"


def save_flag(img: bytes, filename: str) -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    (DEST_DIR / filename).write_bytes(img)


def get_flag(cc: str, base_url: str) -> bytes:
    url = f"{base_url}/{cc}/{cc}.gif".lower()
    req = urllib.request.Request(url, headers={"User-Agent": "FluentPython-Study/1.0"})
    with urllib.request.urlopen(req, timeout=10.0) as resp:
        return resp.read()


def _mock_fetch(cc: str, *, delay_min: float, delay_max: float, error_rate: float) -> bytes:
    time.sleep(random.uniform(delay_min, delay_max))
    r = random.random()
    if r < error_rate / 2:
        raise FileNotFoundError(cc)  # pretend 404
    if r < error_rate:
        raise ConnectionError(cc)  # pretend network error
    return _MINI_GIF


def download_one(
    cc: str,
    *,
    base_url: str,
    verbose: bool,
    mock: bool,
    delay_min: float,
    delay_max: float,
    error_rate: float,
) -> DownloadStatus:
    try:
        if mock:
            img = _mock_fetch(
                cc, delay_min=delay_min, delay_max=delay_max, error_rate=error_rate
            )
        else:
            img = get_flag(cc, base_url)
    except FileNotFoundError:
        if verbose:
            print(f"{cc} -> NOT_FOUND")
        return DownloadStatus.NOT_FOUND
    except urllib.error.HTTPError as e:
        if e.code == 404:
            if verbose:
                print(f"{cc} -> NOT_FOUND (HTTP 404)")
            return DownloadStatus.NOT_FOUND
        if verbose:
            print(f"{cc} -> ERROR (HTTP {e.code})")
        return DownloadStatus.ERROR
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        if verbose:
            print(f"{cc} -> ERROR ({type(e).__name__})")
        return DownloadStatus.ERROR

    save_flag(img, f"{cc}.gif")
    if verbose:
        print(f"{cc} -> OK")
    return DownloadStatus.OK


def _progress_iter(done_iter: Iterable[Future[DownloadStatus]], total: int, verbose: bool):
    if verbose:
        yield from done_iter
        return

    try:
        from tqdm import tqdm  # type: ignore[import-not-found]
    except Exception:
        done = 0
        for fut in done_iter:
            done += 1
            if done == 1 or done == total or done % max(1, total // 20) == 0:
                pct = done * 100 / total
                print(f"\rprogress: {done}/{total} ({pct:5.1f}%)", end="", flush=True)
            yield fut
        print()
    else:
        yield from tqdm(done_iter, total=total)


def download_many(
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
    cc_list = list(cc_list)
    total = len(cc_list)
    concur_req = max(1, min(concur_req, total))

    counter: Counter[DownloadStatus] = Counter()

    with ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do: dict[Future[DownloadStatus], str] = {}
        for cc in sorted(cc_list):
            fut = executor.submit(
                download_one,
                cc,
                base_url=base_url,
                verbose=verbose,
                mock=mock,
                delay_min=delay_min,
                delay_max=delay_max,
                error_rate=error_rate,
            )
            to_do[fut] = cc

        try:
            done_iter = as_completed(to_do)
            for fut in _progress_iter(done_iter, total=total, verbose=verbose):
                cc = to_do[fut]
                try:
                    status = fut.result()
                except Exception as e:
                    if verbose:
                        print(f"{cc} -> ERROR (unexpected {type(e).__name__})")
                    counter[DownloadStatus.ERROR] += 1
                else:
                    counter[status] += 1
        except KeyboardInterrupt:
            # Best-effort cancel of pending tasks.
            for fut in to_do:
                fut.cancel()
            raise

    return counter


def main() -> None:
    parser = argparse.ArgumentParser(description="flags2-style threadpool downloader (Ch. 20.5)")
    parser.add_argument("-n", "--count", type=int, default=20, help="how many codes (max 20)")
    parser.add_argument("-c", "--concur", type=int, default=30, help="max concurrent requests")
    parser.add_argument("--verbose", action="store_true", help="print per-item logs (no tqdm)")
    parser.add_argument("--base-url", default=BASE_URL, help="base URL for downloads")
    parser.add_argument("--mock", action="store_true", help="offline mode: delay + error injection")
    parser.add_argument("--delay-min", type=float, default=0.05, help="mock min delay")
    parser.add_argument("--delay-max", type=float, default=0.30, help="mock max delay")
    parser.add_argument("--error-rate", type=float, default=0.20, help="mock error rate in [0,1]")
    args = parser.parse_args()

    n = max(1, min(args.count, len(POP20_CC)))
    cc_list = POP20_CC[:n]

    t0 = time.perf_counter()
    try:
        counter = download_many(
            cc_list,
            base_url=args.base_url,
            verbose=args.verbose,
            concur_req=args.concur,
            mock=args.mock,
            delay_min=max(0.0, args.delay_min),
            delay_max=max(max(0.0, args.delay_min), args.delay_max),
            error_rate=min(max(0.0, args.error_rate), 1.0),
        )
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        raise
    finally:
        elapsed = time.perf_counter() - t0

    print("counts ->", dict(counter))
    print(f"elapsed -> {elapsed:.2f}s")


if __name__ == "__main__":
    main()

