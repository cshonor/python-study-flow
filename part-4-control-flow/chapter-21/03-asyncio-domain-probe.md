# 21.3 `asyncio` 异步并发实战：域名探测（DNS）

## 这个例子为什么适合用 `asyncio`

域名解析（DNS / `getaddrinfo`）属于典型 **I/O 密集**：

- 单个请求大部分时间在等待网络响应
- 我们希望“同时发出很多探测”，让总耗时接近 **最慢那个响应**，而不是所有响应时间之和

---

## 最小结构：`probe` + `as_completed`

核心拆法：

- `probe(domain)`：一个协程，负责探测一个域名
- `main()`：创建一堆 `probe(...)` 协程对象
- `asyncio.as_completed(coros)`：按完成顺序产出可 `await` 的对象 → 实时打印结果

---

## `await` 到底做了什么（读代码的技巧）

把协程当同步代码读，只要记住一句：

- **遇到 `await` 就“暂停当前协程”，把控制权交回事件循环**，事件循环去运行别的协程；等 I/O 完成，再回来继续。

因此：

- `await loop.getaddrinfo(...)` 不会卡死整个程序
- 只会让“当前这一个 probe”挂起，其他 probe 还能继续推进

---

## 两个关键 API

- `asyncio.get_running_loop()`：只能在协程里调用（没有运行中的 loop 会抛 `RuntimeError`）
- `asyncio.run(main())`：建议的入口（自动创建/关闭事件循环）

---

## 配套代码

`blogdom_probe_demo.py`：

- 生成 Python 关键字 + 后缀（默认 `.dev`）
- `probe` 使用 `loop.getaddrinfo` 做异步 DNS 探测
- `asyncio.as_completed` 按完成顺序输出（适配实时反馈/进度条）
- 可选：线程池对照版（同样的任务用 `ThreadPoolExecutor` 跑）

