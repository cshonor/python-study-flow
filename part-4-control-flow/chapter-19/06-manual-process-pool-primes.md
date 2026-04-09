# 19.6：自建进程池与 CPU 密集型并发（素数批量检测）

## 本节在练什么

- **手动搭一个最小进程池**：任务队列 + 结果队列 + `worker` 循环 + **毒药丸**结束协议
- 用 **CPU 密集的 `is_prime`** 对比：**顺序**、**多线程**、**多进程**
- 为后面 `concurrent.futures.ProcessPoolExecutor` 打底：Executor 本质上也是“进程 + 队列 + 协议”的封装

---

## 顺序版：基准线

逐个检测、打印每条耗时与结果，总耗时 ≈ 各任务耗时之和（无并行）。

---

## 自建进程池：队列 + worker + 毒药丸

| 组件 | 作用 |
|------|------|
| **任务队列** | 主进程放入待检测整数 |
| **结果队列** | worker 放入 `PrimeResult(n, prime, elapsed)`，带上 `n` 才能对乱序结果做归因 |
| **worker** | `while` 取任务；遇到终止信号则退出 |
| **毒药丸** | 用固定整数（如 `0`）表示“没任务了”，比 `None` 更省事（且与 `SimpleQueue[int]` 一致） |

### 重要细节：每个 worker 一枚毒药丸

若只往任务队列里放 **一个** `0`，只有**拿到那个 0 的**那个进程会退出；其余进程会永远阻塞在 `get()` 上。

正确做法：启动 `procs` 个 worker 时，在全部真实任务入队之后，再 **`put(0)` 共 `procs` 次**（或等价地保证每个 worker 都能收到一枚终止信号）。

---

## `SimpleQueue`（进程间）

`multiprocessing.SimpleQueue` 比 `Queue` 更轻，适合“传整数 / 小结构体”这类简单 IPC；复杂对象仍需 pickle，仍要考虑开销。

---

## 性能直觉（与线程对比）

- **多进程**：每个进程独立解释器与 GIL，CPU 密集可吃满多核；进程数一般取 **`cpu_count()`** 附近，再往上常因调度/争用收益变小甚至略差。
- **多线程（CPython + 纯 Python CPU 循环）**：GIL 下多线程往往**不能加速**这类任务，甚至可能比单线程更慢（切换与争用）。

---

## 配套代码

`manual_process_pool_primes_demo.py`：

- `sequential`：顺序基准
- `threads N`：N 个线程 + `queue.Queue`（CPU 密集，通常不加速）
- `procs N`：N 个进程 + `SimpleQueue`（CPU 密集，可加速）

示例：

```text
python manual_process_pool_primes_demo.py sequential
python manual_process_pool_primes_demo.py threads 6
python manual_process_pool_primes_demo.py procs 6
```

可用 `--quick` 换一组较小数字，便于本地秒级跑通。
