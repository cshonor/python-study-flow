# 21.6–21.7 异步上下文管理器 + 生产级异步下载（flags2_asyncio 风格）

## 21.6：异步上下文管理器（Async Context Manager）

### 协议与语法

异步上下文管理器实现：

- `__aenter__`
- `__aexit__`

并用 **`async with`** 进入/退出（只能写在 `async def` 里）。

你可以把它理解为：

- `with` / `__enter__` / `__exit__` 的异步版
- 进入/退出阶段允许 `await`（比如建立/关闭连接、提交/回滚事务）

典型例子：

- `httpx.AsyncClient`：`async with AsyncClient() as client: ...`
- 数据库事务：`async with connection.transaction(): ...`
- `asyncio.Semaphore`：`async with sem:` 自动 acquire/release

---

## 21.7：flags2_asyncio 的“生产级要素”

目标不再只是“能并发”，而是“能用”：

- **进度条/实时反馈**：每完成一个任务就更新
- **错误处理**：404/网络错误/其它异常的区分与统计
- **并发限制**：避免对服务器造成压力（`Semaphore`）
- **不阻塞事件循环**：文件写入等同步操作用 `asyncio.to_thread`

---

## 为什么进度条要用 `asyncio.as_completed`

- `asyncio.gather(*aws)`：结果按 **提交顺序** 返回，适合“一口气等完再处理”
- `asyncio.as_completed(aws)`：按 **完成顺序** 产出 awaitable，适合“实时更新进度/谁先完成先处理”

进度条的关键不是 UI，而是驱动：**只有完成事件发生时才能推进**，因此 `as_completed` 更贴合。

---

## 并发限制：`asyncio.Semaphore`

常用结构：

```python
async with sem:
    ... await 网络请求 ...
```

它能保证同一时刻最多只有 `N` 个协程进入“关键区”（比如发 HTTP 请求）。

---

## 阻塞操作移出事件循环：`asyncio.to_thread`

文件写入是同步 I/O（会阻塞事件循环），典型做法：

```python
await asyncio.to_thread(save_flag, img, filename)
```

这能避免“一个磁盘写入把所有协程都卡住”的问题。

---

## 配套代码

`flags2_asyncio_progress_demo.py`：

- `async with`：管理 `httpx.AsyncClient`（若安装了 httpx）
- `Semaphore`：限制并发
- `asyncio.as_completed`：按完成顺序更新进度
- 错误统计：`Counter[DownloadStatus]`
- `tqdm` 可选依赖；未安装则降级输出
- `--mock`：离线延迟 + 错误注入（CDN 404 也能跑通）

