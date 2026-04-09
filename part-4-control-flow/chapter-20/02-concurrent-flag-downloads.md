# 20.2 并发网络下载：`ThreadPoolExecutor` 与 Future（国旗示例）

## 实验在证明什么

用同一批 **I/O 密集** 任务（批量 HTTP 下载）对比：

| 方案 | 调度方式 | 典型耗时（相对顺序） |
|------|----------|----------------------|
| **顺序** | 单线程逐个请求 | 基准 1x |
| **线程池** | `ThreadPoolExecutor`，I/O 等待时可切换 | 明显加速（常见数倍） |
| **协程** | 事件循环 + 异步 HTTP（书中 `httpx` / 第 21 章深入） | 常与线程池接近，超高并发时开销优势更明显 |

结论：**网络/磁盘等待越久，并发收益越大**；线程与协程的差异更多在“调度模型与规模”，而不是“谁一定更快一点点”。

---

## 顺序版：`flags.py` 思路

- `get_flag(cc)`：构造 URL，`GET`，`raise_for_status()`，返回 `bytes`
- `save_flag(img, name)`：写入本地目录
- `download_many`：`for cc in sorted(cc_list): ...`

这是性能基准，也是线程/协程版要**复用**的核心逻辑。

---

## 线程池版：`ThreadPoolExecutor`

### `map`（示例 20-3）

```python
with ThreadPoolExecutor() as executor:
    res = executor.map(download_one, sorted(cc_list))
return len(list(res))
```

要点：

- `with` 退出时会 `shutdown(wait=True)`，等所有线程结束
- `map` 返回迭代器，**消费结果时才真正驱动等待**（所以常见写法是 `list(res)` 或循环取完）
- Python 3.8+ 默认 `max_workers = min(32, os.cpu_count() + 4)`，对 I/O 任务通常够用

### Future：`submit` + `as_completed`（示例 20-4 / 20-5）

- `submit` **立即**返回 `Future`，主线程可先打印 “Scheduled …”
- `as_completed(futures)` 按**完成顺序**产出 Future，因此输出顺序与提交顺序无关
- 业务上若要对齐输入顺序，应在结果里携带 `cc`（本 demo 的 `download_one` 返回 `cc`）

---

## Future 速查

| 方法 | 作用 |
|------|------|
| `.done()` | 是否已完成（非阻塞） |
| `.result(timeout=...)` | 阻塞取结果；任务异常会在此重新抛出 |
| `.add_done_callback(fn)` | 完成后回调（由执行器线程调用，注意线程安全） |

注意：`concurrent.futures.Future` 与 `asyncio.Future` **不是同一个类型**，协程代码里不要混用。

---

## 避坑

- **CPU 密集**不要用线程池硬扛 → 用 `ProcessPoolExecutor` 或把计算放到别的模型里
- **不要盲目无限并发** → 线程池/连接池/服务器都会有限额；书中用固定池大小就是在控压
- **必须设超时** → 避免坏网络把线程长期占满

---

## 配套代码

`flags_threadpool_download_demo.py`：

- 顺序 / `map` 线程池 / `submit`+`as_completed`（演示 Future）
- asyncio：若已安装 `httpx` 则用异步客户端；否则用 `asyncio.to_thread` 回退
- 默认下载目录在脚本同级的 `downloaded_flags/`（可改）

图灵示例里的 CDN 链接可能随时间失效（HTTP 404）。可用 **`--mock`**：对每个国家码 `sleep` 一小段时间并写入最小 GIF，专门用来对比「顺序 vs 线程池 vs asyncio」的结构与耗时：

```bash
python flags_threadpool_download_demo.py all --mock -n 20
```
