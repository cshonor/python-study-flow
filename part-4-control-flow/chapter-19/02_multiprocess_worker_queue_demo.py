"""
Ch. 19 supplement: multiprocess cooperation via Queue (task fan-out + result gather).

Run from repo root:
  python part-4-control-flow/chapter-19/02_multiprocess_worker_queue_demo.py

Requires: if __name__ == "__main__" guard (Windows spawn).
"""

from __future__ import annotations

import os
from multiprocessing import Process, Queue


def worker(task_q: Queue, result_q: Queue) -> None:
    while True:
        item = task_q.get()
        if item is None:
            break
        task_id, n = item
        # tiny CPU-ish work (deterministic)
        acc = sum(k * k for k in range(1, n + 1))
        result_q.put((task_id, acc))


def main() -> None:
    n_workers = min(4, os.cpu_count() or 1)
    task_q: Queue = Queue()
    result_q: Queue = Queue()

    tasks: list[tuple[int, int]] = [(i, 25_000 + i * 500) for i in range(8)]
    for t in tasks:
        task_q.put(t)
    for _ in range(n_workers):
        task_q.put(None)

    workers = [
        Process(target=worker, args=(task_q, result_q)) for _ in range(n_workers)
    ]
    for p in workers:
        p.start()
    for p in workers:
        p.join()

    results = [result_q.get() for _ in tasks]
    results.sort(key=lambda x: x[0])
    print("workers:", n_workers, "tasks:", len(tasks))
    for tid, acc in results:
        print(f"  task {tid} -> acc(last term^2) hint {acc % 997}")


if __name__ == "__main__":
    main()
