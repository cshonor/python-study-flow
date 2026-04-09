# 第 20 章开篇：并发执行器与 Future（`concurrent.futures`）

## 开篇一句话：99% 的并发需求

Michele Simionato 的观点可以浓缩成一句：

- **批量提交一堆相互独立的任务 → 收集结果**

第 19 章你能手写“池 + 队列 + 收割结果”的底层机制；第 20 章则是把这件事交给标准库的生产级封装：`concurrent.futures`。

---

## 两个主角：Executor 与 Future

| 概念 | 是什么 | 你得到什么 |
|------|--------|------------|
| **`Executor`** | “执行器”抽象（提交任务的地方） | `submit`/`map` 等统一 API |
| **`Future`** | “将来会有结果”的对象 | 结果、异常、完成回调、取消、状态 |

两种执行器实现（API 一致，可互换）：

- **`ThreadPoolExecutor`**：线程池，常用于 **I/O 密集**
- **`ProcessPoolExecutor`**：进程池，常用于 **CPU 密集**（多核并行）

---

## Future：异步任务的统一抽象

Future 的核心能力：

- **立即返回**：`submit` 不阻塞，先给你一个 `Future`
- **取结果**：`future.result()`（必要时阻塞等待）
- **异常传播**：任务里抛的异常，会在 `result()` 处重新抛出
- **回调**：`add_done_callback(fn)` 任务完成后触发
- **批量收割**：`as_completed(futures)` 按完成顺序迭代

这也是第 21 章 `asyncio`（协程）能“统一管理异步任务”的认知基石之一。

---

## 与第 19 / 21 章的衔接

- **第 19 章**：理解并发/并行、线程/进程的底层现实（尤其是 GIL 与多核）
- **第 20 章**：用执行器把“提交任务 + 收集结果”写成几行（适合大多数业务）
- **第 21 章**：事件循环与协程（另一套并发结构），但仍能用 Future/Task 一类抽象来理解“将来的结果”

---

## 配套代码

`executors_and_futures_demo.py`：

- 同一批任务用 `ThreadPoolExecutor` / `ProcessPoolExecutor`
- 演示 `submit` / `Future.result()` / `as_completed`
- 演示异常如何通过 Future 传播
- 演示 `add_done_callback` 的最小用法

