# 21.2 协程的演进：原生协程、经典协程、生成器式协程

## 三代协程，一张表先对齐

| 类型 | 定义方式 | 能否 `await` | 主要用途 | 现状 |
|------|----------|--------------|----------|------|
| **原生协程（native coroutine）** | `async def` | ✅（并且 `await` 只能写在原生协程里） | 现代 async/await 的标准入口 | ✅ 推荐 |
| **经典协程（classic coroutine）** | 生成器 + `yield` + `.send()` | ❌（不是 awaitable） | 历史上的“生成器当协程用” | ❌ 历史知识 |
| **生成器式协程（generator-based coroutine）** | `@types.coroutine` 装饰的生成器 | ✅（变成 awaitable） | 原生协程过渡期/底层适配层 | ⚠️ 少用 |

---

## 1) 原生协程：`async def` 定义的就是协程

要点：

- `async def` 定义的函数，调用后返回 **协程对象**（coroutine object）。
- 原生协程之间用 `await` 连接，语义上相当于过去生成器协程里的 `yield from`（“把控制权委托出去，等对方完成再回来”）。
- `await` 基本只能出现在 `async def` 内（交互式 `python -m asyncio` 是个特例，不展开）。

---

## 2) 经典协程：生成器 + `.send()` 的那套

经典协程本质是“把生成器当成可暂停/可恢复的可调用体”：

- 通过 `next(gen)` 启动
- 通过 `gen.send(value)` 把值送进 `yield` 表达式

但它 **不是** `await` 体系的一部分，因此：

- 不能直接 `await` 一个普通生成器
- `asyncio` 也不会把它当成可调度任务

---

## 3) 生成器式协程：`@types.coroutine`

`types.coroutine` 的作用是把“生成器”包装成 **awaitable**，从而能在原生协程里：

```python
await some_generator_based_coroutine()
```

它更像兼容层/底层技巧，而不是日常业务代码的首选写法。

> 注意：老的 `@asyncio.coroutine` 过渡装饰器已废弃（新代码别用）。

---

## 4) 异步生成器（async generator）

`async def` 里出现 `yield`，就得到异步生成器：

- 用 `async for` 消费
- 每次 `yield` 都是在异步迭代协议下推进

---

## 配套代码

`coroutine_types_demo.py`：

- 检查 `inspect.iscoroutinefunction / inspect.iscoroutine / inspect.isawaitable`
- 原生协程：`async def`
- 生成器式协程：`@types.coroutine`（可被 `await`）
- 经典“生成器协程”：只能 `.send()` 驱动，不能 `await`
- 异步生成器：`async for`

