# 21.4–21.5 Awaitable 与 `asyncio` 异步 HTTP 下载（国旗示例）

## 21.4：什么是 Awaitable（“可被 `await` 的东西”）

`await` 处理的对象叫 **awaitable**。类比：

- `for` 需要 iterable
- `await` 需要 awaitable

常见两类（终端用户最常遇到）：

1. **原生协程对象**：调用 `async def` 得到的对象  
   - `coro = some_async_fn()`  
   - `await coro`
2. **`asyncio.Task`**：用 `asyncio.create_task(coro)` 把协程“提交给事件循环后台运行”得到的对象  
   - `task = asyncio.create_task(coro)`  
   - `await task`（等待其完成并取结果）

底层上，任何实现 `__await__` 的对象都可以被 `await`（例如 `asyncio.Future` / `Task`）。

---

## `await coro()` vs `create_task(coro())`

| 写法 | 行为 | 什么时候用 |
|------|------|------------|
| `await coro()` | 直接等待它完成（当前协程暂停，直到结果返回） | 顺序流程，需要结果才能继续 |
| `task = create_task(coro())` | 立刻把它交给事件循环，自己继续往下跑 | 并发启动多个子任务、后台任务 |

一句话：**`create_task` 负责“启动并发”，`await` 负责“等待结果”**。

---

## 21.5：异步 HTTP 下载的骨架（`httpx.AsyncClient`）

异步 I/O 的关键是：I/O 必须是可 `await` 的 API，否则会阻塞事件循环。

典型结构：

- `async with AsyncClient() as client:` 管理连接池/资源生命周期（异步上下文管理器）
- `await client.get(...)` 发起非阻塞请求
- 用 `asyncio.gather(*aws)` 等待一批 awaitables 完成（按提交顺序返回）

---

## `gather` vs `as_completed`（异步世界的两种收割方式）

| 工具 | 结果顺序 | 适合 |
|------|----------|------|
| `asyncio.gather(*aws)` | **提交顺序** | “我要等全部完成，再一起拿结果” |
| `asyncio.as_completed(aws)` | **完成顺序** | 实时反馈/进度条/谁先完成先处理 |

---

## 异步铁律：别把阻塞塞进事件循环

异步不是“只改语法”就变快。真正的收益来自：

- 所有 I/O 都用异步 API
- CPU 密集或同步 I/O 必须移出事件循环（`asyncio.to_thread` / 进程池）

否则一个阻塞点就能让整个 loop 停摆（见 `async_blocking_pitfall_demo.py`）。

---

## 配套代码

`flags_asyncio_httpx_demo.py`：

- `awaitable`/`Task` 的最小演示（`create_task` vs 直接 `await`）
- `httpx.AsyncClient` 异步下载（若安装了 `httpx`）
- `--mock` 离线模式：用 sleep + 最小 GIF 模拟网络（CDN 404 时也能跑通）
- `gather` 与 `as_completed` 的输出差异

