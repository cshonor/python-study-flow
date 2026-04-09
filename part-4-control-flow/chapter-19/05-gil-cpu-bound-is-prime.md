# 19.5：GIL 对 CPU 密集型任务的真实影响（`is_prime`）

把 19.4 的 `slow()`（`sleep`）替换成纯 CPU 计算：素数检测 `is_prime(n)`。

我们关心的是：**旋转指针还能不能转？** 以及 **为什么**。

---

## `is_prime`：典型 CPU 密集型（几乎不主动让出）

```python
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True
```

要点：

- 这类纯 Python 循环没有 I/O，不会像 `sleep` 那样“自然释放 GIL”。
- 但 CPython 会周期性切换线程（默认大约 5ms 一次），这会影响线程版的可观察行为。

---

## 三个结论（把“会不会转”说清）

| 模型 | 指针会转吗 | 关键原因 |
|------|------------|----------|
| **进程** | ✅ 会 | 独立解释器与独立 GIL；OS 调度进程，彼此不抢同一个 GIL |
| **线程** | ✅ 会（通常） | CPython 会周期性让出 GIL；spinner 线程仍能抢到片段时间打印动画 |
| **协程（直接跑 `is_prime`）** | ❌ 不会 | 没有 `await` 就不会让出控制权；事件循环被 CPU 计算彻底堵住 |

注意：线程版“会转”不代表“CPU 会更快”。对于 CPU 密集型，线程更多时候只是在争用 GIL + 增加切换开销。

---

## 协程版的两种“补救”

### 1）权宜之计：在循环里 `await asyncio.sleep(0)`

- 让出控制权给事件循环 → 指针能动
- 代价：增加调度开销 → 总耗时通常变长

### 2）推荐：把 CPU 任务丢给进程池（executor）

- 事件循环继续负责 UI/网络等 I/O
- CPU 计算在进程里跑（绕开 GIL）

---

## 配套代码

`prime_spinner_gil_demo.py`：

- `thread`：线程 + `is_prime`
- `process`：进程 + `is_prime`
- `asyncio-block`：协程，但直接跑 `is_prime`（指针冻结）
- `asyncio-yield`：协程版 `is_prime_async` 周期性 `await sleep(0)`（能转但变慢）
- `asyncio-exec-proc`：协程 + 进程池执行 `is_prime`（推荐）

用法：

- `python prime_spinner_gil_demo.py thread`
- `python prime_spinner_gil_demo.py process`
- `python prime_spinner_gil_demo.py asyncio-block`
- `python prime_spinner_gil_demo.py asyncio-yield`
- `python prime_spinner_gil_demo.py asyncio-exec-proc`

