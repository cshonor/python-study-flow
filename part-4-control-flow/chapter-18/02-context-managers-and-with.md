# 上下文管理器与 `with` 块：协议、`contextlib` 与实战（18.2）

## `with` 的定位：`try/finally` 的语法糖

- **核心价值**：把“获取资源/准备环境”与“清理/还原”打包，确保离开 `with` 块时一定执行清理（正常结束、`return`、异常、`sys.exit()` 都一样）。
- **类比**：上下文管理器之于 `with`，就像迭代器之于 `for`。

---

## 协议：`__enter__` / `__exit__`

| 方法 | 调用时机 | 作用 |
|------|----------|------|
| `__enter__(self)` | `with` 块开始前 | 获取资源/准备环境；返回值绑定到 `as` 子句 |
| `__exit__(self, exc_type, exc_value, traceback)` | 离开块时（含异常） | 释放资源/还原环境；可选择吞掉异常 |

`__exit__` 的三个异常参数：

- **`exc_type`**：异常类；无异常为 `None`
- **`exc_value`**：异常实例；无异常为 `None`
- **`traceback`**：traceback 对象；无异常为 `None`

异常是否“吞掉”的规则：

- `__exit__` **返回真值** → 异常被视为已处理，不向外抛出
- 返回 `None` / 假值 → 异常继续向外传播

---

## 最常见例子：文件对象

```python
with open("mirror.py", encoding="utf-8") as fp:
    src = fp.read(60)
```

要点：

- `open()` 返回的文件对象实现了上下文管理器协议。
- `__enter__` 通常返回文件对象自身，因此 `fp` 绑定它。
- `with` **不创建新作用域**；块外仍能访问 `fp`，但离开块后文件已关闭（IO 操作会失败）。

---

## 示例：`LookingGlass`（类式上下文管理器）

目标：进入 `with` 时把 `sys.stdout.write` 临时替换为“反向写入”；退出时恢复。并演示：特定异常（如 `ZeroDivisionError`）可以在 `__exit__` 中被吞掉。

关键设计点：

- **`__enter__`**：保存原始 `write`，安装替代方法，返回 `as` 绑定值（不必是 `self`）
- **`__exit__`**：恢复原始 `write`；按需处理异常并选择是否吞掉

（完整可运行代码见 `looking_glass_context_manager_demo.py`）

---

## `contextlib`：更省事的上下文管理器工具箱

| 工具 | 作用 | 典型用途 |
|------|------|----------|
| `@contextmanager` | 生成器函数 → 上下文管理器 | 快速实现 `__enter__/__exit__` |
| `closing` | 给只有 `close()` 的对象补 `with` | 包装“类文件/连接”对象 |
| `suppress` | 忽略指定异常 | 删除不存在的文件等“可忽略失败” |
| `nullcontext` | 空操作上下文 | 条件分支里统一写成 `with` |
| `ExitStack` | 动态管理多个上下文（LIFO 退出） | 批量打开文件/组合多个上下文 |
| `ContextDecorator` | 让上下文可当装饰器 | “装饰器 + with”二合一 |
| `AbstractContextManager` | 抽象基类 | 规范类式实现 |

---

## `@contextmanager`：生成器式实现的关键点

`yield` 把函数切成两段：

- `yield` 前：相当于 `__enter__`
- `yield` 产出的值：绑定到 `as`
- `yield` 后：相当于 `__exit__`

最重要的坑：

- **必须用 `try/finally` 把 `yield` 包起来**，确保 `with` 块抛异常时仍会执行“恢复/清理”逻辑。

---

## Python 3.10+：括号式“并行 with”

把多个上下文放在一个 `with` 中，避免嵌套右漂移：

```python
with (
    open("a.txt", "w", encoding="utf-8") as fa,
    open("b.txt", "w", encoding="utf-8") as fb,
):
    fa.write("A")
    fb.write("B")
```

---

## 实战套路：就地修改文件（in-place edit）

需求：读原文件逐行处理，但输出写回同一路径。安全做法通常是：

- 写到临时文件
- 成功后用 `os.replace` 原子替换
- 失败则保留原文件不变（或从备份恢复）

这个套路很适合用 `@contextmanager` 封装（见 demo）。

---

## 配套代码

`looking_glass_context_manager_demo.py`：包含

- `LookingGlass`（类式协议实现）
- `looking_glass()`（`@contextmanager` 生成器式实现）
- `suppress` / `nullcontext` / `ExitStack`
- Python 3.10+ 括号式多上下文
- `inplace()`：安全“就地改文件”的最小实现与演示

