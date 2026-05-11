# 第 19 章开篇：Python 并发模型（Concurrency vs Parallelism）

## 先把两个词分清

引用 Rob Pike 在《Concurrency Is Not Parallelism》里的非正式定义（足够好用）：

| 概念 | 一句话 | 关键点 |
|------|--------|--------|
| **并发（Concurrency）** | 同时处理多件事 | **结构与调度**：任务被组织起来、交替推进 |
| **并行（Parallelism）** | 同时做多件事 | **执行与硬件**：多核上真正同时跑 |

关系：

- **并行是并发的子集**：并行一定并发；并发不一定并行。

---

## 为什么容易混：术语在不同领域被复用

很多争论来自“同词异义/异词同义”。开篇先用 Pike 的说法统一口径，后面讨论线程/协程/进程时就不容易跑偏。

---

## 直观类比（记住就够）

- **并发**：一个厨师做 10 道菜，靠切换步骤让每道都在推进。
- **并行**：10 个厨师各做 1 道菜，物理上同时操作。

对应到计算机：

- 单核 CPU 跑很多任务：靠调度轮转 → **并发**
- 多核 CPU 真同时跑多个任务：→ **并行**

---

## Python 并发的三条路（本章主线）

Python 里谈「同时推进多件事」，常见就三类：**线程、协程、多进程**。下面与后文各节一致，可直接当**背诵卡片**用。

### 1）线程 `threading`

- **模型**：**多线程并发**（同一进程内多线程）。  
- **调度**：操作系统内核调度。  
- **GIL**：CPython 有**全局解释器锁**，同一时刻通常**只有一个线程在执行 Python 字节码**。  
- **效果**：  
  - **I/O 密集**（网络、磁盘、数据库等待）：往往**很有效**（阻塞等待时可能释放 GIL，让别的线程跑）。  
  - **CPU 密集**（纯 Python 算力循环）：**很难靠多线程并行加速**，有时还更慢。  
- **开销**：相对小；线程共享地址空间，通信简单。  
- **一句话**：**普通 I/O 并发常用线程；CPU 密集别指望线程“多核起飞”。**

### 2）协程 `asyncio`（原生协程）

- **模型**：**单线程内的并发**（用户态协作式：在 `await` 处主动让出）。  
- **调度**：**事件循环**；没有内核级「线程切换」那种成本。  
- **GIL**：全程单线程跑你的协程代码路径时，**不指望用多线程绕 GIL**；重点是**别在协程里写长时间占着循环不 `await` 的阻塞**。  
- **效果**：  
  - **高并发 I/O**（大量连接/请求）：在生态配套齐全时，往往**吞吐高、单位连接成本低**。  
  - **要求**：阻塞 I/O 要换成**异步库**（如 `aiohttp` / `asyncpg` 等），否则会把事件循环堵死。  
- **开销**：**极小**；单进程内可挂大量协程任务。  
- **一句话**：**高并发 I/O 的利器；但必须吃异步生态。**

### 3）多进程 `multiprocessing`

- **模型**：**多进程并行**（每个进程各自一份 CPython 解释器与用户态状态）。  
- **调度**：操作系统内核调度。  
- **GIL**：**每个进程各有一把 GIL** → 多进程能**真并行**跑 CPU 密集（多核）。  
- **效果**：  
  - **CPU 密集**：在 CPython 下往往是**正经利用多核**的路线之一。  
  - **代价**：进程创建与销毁更重、内存不共享、**IPC** 更费心思。  
- **开销**：**大**。  
- **一句话**：**CPU 密集想并行，多进程是主力候选；重，但真并行。**

---

### 一表看懂（面试/复习）

| 技术 | 核心机制 | GIL / 并行感 | 最佳场景 | 典型开销 |
|------|----------|----------------|----------|----------|
| **`threading`** | 多线程并发 | 有 GIL；CPU 字节码层面伪并行 | **普通 I/O 密集** | 相对小 |
| **`asyncio`** | 单线程 + 事件循环 | 不靠多线程并行 CPU | **高并发 I/O**（异步生态齐全） | 极小 |
| **`multiprocessing`** | 多进程 | 每进程独立 GIL → **CPU 可真正并行** | **CPU 密集** | 大 |

---

### 最简选型口诀（本章核心）

- **CPU 密集 → 多进程**（或进程池 / `concurrent.futures.ProcessPoolExecutor`，见后文）。  
- **普通 I/O 密集 → 多线程**（或线程池 / `ThreadPoolExecutor`）。  
- **超高并发 I/O、且愿意全面异步化 → `asyncio`**。

---

### 极简可复制：三条路各一段（REPL / 小文件均可）

下面三段彼此独立；**多进程**在 Windows 上务必放在 **`if __name__ == "__main__":`** 里再跑（与全章其它 `multiprocessing` 示例一致）。

**线程（I/O 等待）**

```python
import threading
import time


def work(i: int) -> None:
    time.sleep(0.2)
    print("thread done", i)


threads = [threading.Thread(target=work, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("all joined")
```

**协程（I/O 等待）**

```python
import asyncio


async def work(i: int) -> None:
    await asyncio.sleep(0.2)
    print("async done", i)


async def main() -> None:
    await asyncio.gather(*(work(i) for i in range(3)))


asyncio.run(main())
```

**多进程（纯 CPU 小循环；整段保存为 `.py` 再运行）**

```python
from multiprocessing import Process


def cpu(i: int) -> None:
    _ = sum(range(50_000))
    print("proc done", i)


if __name__ == "__main__":
    procs = [Process(target=cpu, args=(i,)) for i in range(3)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print("all joined")
```

---

## 配套代码（整章对照跑）

`00_concurrency_vs_parallelism_demo.py`：

- 用**同一量级**的任务分别跑 **`ThreadPoolExecutor`（I/O）**、**`asyncio`（I/O）**、**线程池（CPU）**、**`ProcessPoolExecutor`（CPU）**  
- I/O 用 `sleep` / `asyncio.sleep`；CPU 用纯 Python 循环  
- 观察：哪些是**并发结构**，哪些能**并行加速**

仓库根目录：

```bash
python part-4-control-flow/chapter-19/00_concurrency_vs_parallelism_demo.py
```

