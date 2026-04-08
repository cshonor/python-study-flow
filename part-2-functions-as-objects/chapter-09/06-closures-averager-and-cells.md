# 9.6 闭包（Closure）深度理解：累计平均值、自由变量与 cell

这一节用一个非常经典的“累计平均值”计算器，把闭包讲透：**闭包不是语法糖，也和 lambda 没必然关系**；它的核心是**嵌套函数 + 自由变量**。

配套脚本：`averager_closure_demo.py`。

---

## 一、闭包的核心定义（抓两个条件就够）

闭包可以理解为：**延伸了作用域的函数**。通常满足两个条件：

1. 它是**嵌套函数**（定义在另一个函数内部）；
2. 它能访问外层函数的局部变量（**自由变量**），即使外层函数已经返回，这些绑定仍被保留。

关键点：闭包保留的是**绑定关系**（binding），不是“把值复制一份”。这也是它能保存状态、也能导致对象生命周期变长的原因。

---

## 二、两种实现同一个需求：类 vs 闭包

需求：实现一个 `avg`，每次传入新值，返回目前为止所有值的平均值。

### 方案 1：类 + `__call__`（面向对象）

```python
class Averager:
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        return sum(self.series) / len(self.series)
```

- 状态放在实例属性 `self.series` 里；
- `avg = Averager()` 后，`avg(10)`/`avg(11)` 像调用函数一样工作。

### 方案 2：工厂函数返回内层函数（闭包）

```python
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)  # series 是自由变量
        return sum(series) / len(series)

    return averager
```

- 状态放在外层函数的局部变量 `series` 里；
- `avg = make_averager()` 返回内层函数 `averager`；
- 外层函数返回后，`series` 仍然“活着”，因为被闭包保留。

---

## 三、底层原理：自由变量、`__code__` 与 `__closure__`

当你得到 `avg = make_averager()` 之后，可以从三个角度看“闭包到底存了什么”。

### 1）自由变量名列表：`avg.__code__.co_freevars`

```python
avg.__code__.co_freevars
# ('series',)
```

它告诉你：这个函数体里引用了哪些“来自外层作用域的名字”。

### 2）闭包内容：`avg.__closure__`（一组 cell）

```python
avg.__closure__
# (<cell at 0x...: list object at 0x...>,)
```

`__closure__` 里不是直接放值，而是放 **cell 对象**；cell 里保存了那个自由变量的当前内容。

### 3）cell 的真实值：`cell.cell_contents`

```python
avg.__closure__[0].cell_contents
# [10, 11, 12]
```

这就是为什么外层函数返回后，`series` 并没有“消失”：它被 cell 引用着。

---

## 四、闭包的坑：给自由变量赋值会触发“局部变量判定”

这个坑和 9.5 的规则是一回事：**函数体里出现赋值语句，名字会被判定为局部**。

如果你写：

```python
def make_averager():
    total = 0
    count = 0

    def averager(new_value):
        total += new_value   # 这里会报 UnboundLocalError
        count += 1
        return total / count
```

你需要 `nonlocal`：

```python
def make_averager():
    total = 0
    count = 0

    def averager(new_value):
        nonlocal total, count
        total += new_value
        count += 1
        return total / count
```

本节配套脚本会把这个错误与修复一起跑出来。

---

## 五、什么时候用闭包，什么时候用类？

| 维度 | 类实现 | 闭包实现 |
|---|---|---|
| 状态存放 | 实例属性（`self.xxx`） | 外层局部变量（自由变量） |
| 适合复杂度 | 复杂状态/多方法协作更直观 | 简单状态 + 单一行为更轻量 |
| 可扩展性 | 易加方法、易继承/组合 | 适合小而美的函数工厂 |
| 风险点 | 更“显式”，较少隐藏引用 | 可能无意持有大对象导致生命周期变长 |

实用结论：**装饰器大多就是闭包**；你理解了 `__closure__` 的 cell，装饰器“为什么能记住原函数/参数”就不玄学了。

