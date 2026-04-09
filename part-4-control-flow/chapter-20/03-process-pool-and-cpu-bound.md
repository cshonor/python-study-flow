# 20.3 `ProcessPoolExecutor`：进程池与 CPU 密集型并发（素数检测）

## 什么时候该用进程池

`ProcessPoolExecutor` 的核心定位很简单：

- **让 CPU 密集型任务在多核上真正并行**
- 绕开 CPython 的 **GIL**：每个子进程都有独立解释器与 GIL

因此经验法则是：

- **I/O 密集** → `ThreadPoolExecutor`（或 `asyncio`）
- **CPU 密集** → `ProcessPoolExecutor`

---

## API 一致性：线程池 ↔ 进程池只差一行

```python
with ThreadPoolExecutor() as ex:
    ...

with ProcessPoolExecutor() as ex:
    ...
```

这一点是 `concurrent.futures` 的设计重点：让你用同一套 `submit` / `map` / `as_completed` 把任务分发给不同“执行后端”。

---

## 素数检测 demo：为什么能体现差异

素数检测（尤其是对大整数）主要是**纯计算**：

- 线程池：多线程会争用同一把 GIL，通常**难以**获得线性加速
- 进程池：子进程可在多个核心上同时跑，才有机会看到真正并行

---

## `Executor.map` 的一个“反直觉点”

`executor.map(fn, items)` 有一个很关键的语义：

- **结果迭代顺序 = 输入顺序**（哪怕后面的任务更早完成）

这会导致一个经典现象：

- 如果第 1 个任务很慢，后面很多任务很快
- 你用 `map` 迭代结果时，会被第 1 个卡住，看不到后面已完成的结果

当你希望“谁先完成先处理”，就用：

- `submit` + `as_completed`

---

## Windows/进程池的坑（一定要记）

在 Windows 上（默认 `spawn` 启动子进程）：

- 被提交到进程池的函数必须是**模块顶层可导入**的（不能是 `lambda` / 内部函数）
- 入口必须用 `if __name__ == '__main__':` 保护

---

## 配套代码

`process_pool_primes_demo.py`：

- 线程池 vs 进程池：同一组数字的素数检测
- `map`（输入序） vs `as_completed`（完成序）的输出对比
- 每个任务返回 `(n, is_prime, elapsed)`，便于观察“长任务卡输出”

