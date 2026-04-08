# 10.4 命令模式：把“面向对象回调”还原成 Python 回调

GoF 对命令模式有一句很直白的评价：

> **命令模式是回调机制的面向对象替代品。**

在 Java/C++ 里，为了把“要执行的动作”封装成对象、并让调用者只依赖统一接口，通常会写：

- `Command.execute()`
- 一堆只实现 `execute()` 的具体命令类

但在 Python 里，**函数本来就能当回调传递**，所以很多“命令类”会自然退化为：

- 一个函数（无状态）
- 或一个可调用对象（需要组合/保存状态时）

配套脚本：`command_pattern_demo.py`（含普通命令、宏命令、最小撤销栈）。  

---

## 一、经典结构（理解它在解决什么）

命令模式想解决的核心是解耦：

- **Invoker（调用者）**：例如菜单按钮 `MenuItem`，只负责触发
- **Receiver（接收者）**：例如 `Document`，真正实现动作
- **Command（命令）**：把“动作”封装起来（通常一个 `execute()`）

在 Python 的视角里，Invoker 只需要依赖一件事：

> **它拿到的东西能不能被调用**（callable）。

---

## 二、Python 极简版：函数就是命令

当一个命令不需要保存状态，直接用函数当命令是最自然的：

```python
def open_file(path: str) -> None: ...
def paste() -> None: ...

menu["Open"] = lambda: open_file("x.txt")
menu["Paste"] = paste
```

Invoker 的逻辑只剩一句：`command()`。

---

## 三、宏命令：用 `__call__` 保存命令列表（组合 + 状态）

当你需要“组合多个命令并复用”，最常见的写法是可调用对象：

```python
class MacroCommand:
    def __init__(self, commands):
        self.commands = list(commands)

    def __call__(self):
        for cmd in self.commands:
            cmd()
```

优点：

- `MacroCommand(...)()` 像函数一样调用
- `self.commands` 存状态（组合关系）
- 兼容任意可调用对象（函数、lambda、其它宏命令）

---

## 四、带撤销（undo）：闭包 or 可调用对象

当一个命令需要 `undo()`，就要保存“反向动作”或必要的上下文。

常见两种写法：

- **闭包**：把 `do` / `undo` 存在返回的函数对象上（轻巧但不够显式）
- **可调用对象**：`__call__` 执行，`undo()` 撤销（更清晰、更易扩展）

本章配套 demo 里会给出一个最小“撤销栈”示例，帮助你把思路跑通。

