# 9.3 注册式装饰器：为什么 `import` 一下就“执行了代码”

这一节对应书里的经典例子：`registration.py`。它用一个全局 `registry` 列表收集被装饰的函数引用，重点不是“注册表有多厉害”，而是帮你看清：

- **装饰器在模块导入/执行到函数定义处时就会运行**；
- **函数体不会在导入时执行**，只有你调用函数时才执行；
- `if __name__ == "__main__"` 用来隔离“作为脚本运行”和“作为库被导入”两种场景。

配套脚本：`registration.py`。

---

## 一、核心代码（逐行看执行时机）

```python
registry = []

def register(func):
    print(f"running register {func}")
    registry.append(func)
    return func

@register
def f1():
    print("running f1")

@register
def f2():
    print("running f2")

def f3():
    print("running f3")

def main():
    print("running main()")
    print("registry ->", registry)
    f1()
    f2()
    f3()

if __name__ == "__main__":
    main()
```

你可以把 `@register` 读成一条“赋值语句”：

```python
f1 = register(f1)
f2 = register(f2)
```

于是“导入时”就发生了两件事：

- 执行 `register(...)`（打印 + append）；
- 把 `f1` / `f2` 名字重新绑定到装饰器返回值（这里返回原函数，所以行为不变）。

---

## 二、两种运行场景：脚本运行 vs 作为库导入

### 场景 1：直接运行 `registration.py`

```bash
python part-2-functions-as-objects/chapter-09/registration.py
```

典型输出顺序（地址会不同）：  

1. `running register ...`（两次）——模块执行到 `@register` 时就触发  
2. `running main()`——因为作为脚本运行，`__name__ == "__main__"` 成立  
3. `registry -> [...]`——注册表里已经有 `f1`、`f2`  
4. `running f1/f2/f3`——函数体只有在被调用时才执行

### 场景 2：导入模块（作为库）

在 REPL / 其它模块里：

```python
import registration
registration.registry
```

你会看到：

- 导入时同样打印两次 `running register ...`（注册发生在导入阶段）
- 但 `main()` 不会执行（因为 `__name__` 是模块名而不是 `__main__`）

---

## 三、结论（你必须形成肌肉记忆的点）

- **装饰器代码（装饰过程）在导入时执行**，所以装饰器可能带来“导入即副作用”。  
- **被装饰函数的函数体不会导入时运行**，只有调用才运行。  
- `if __name__ == "__main__"` 是隔离副作用的基本工具：  
  - 导入时只做定义/注册  
  - 直接运行时才执行“主流程”

