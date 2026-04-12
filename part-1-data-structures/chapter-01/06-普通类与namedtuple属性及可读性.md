# 普通类 vs namedtuple 实例属性赋值与可读性对比（完整笔记）

## 1. 普通类的实例属性：靠 `__init__` + `self.xxx` 来赋值
普通类的实例属性，**是在方法里面手动赋值上去的**。
最典型就是 `__init__` 构造方法：

```python
class Card:
    def __init__(self, rank, suit):
        self.rank = rank   # 手动给实例绑属性
        self.suit = suit   # 看得见 = 赋值
```

- 实例属性是**动态绑上去**的
- 靠 `self` 来区分“属于这个实例”
- 你能在代码里**清晰看到哪些属性存在**
- 之后也可以在其他方法里继续加/改属性

```python
def change_rank(self, new_rank):
    self.rank = new_rank  # 普通类可以在方法里改实例属性
```

所以你的理解完全对：
**普通类的实例属性，是通过方法（尤其是 __init__）用 self 来赋值、修改的。**

---

## 2. namedtuple 的实例属性：靠 `__new__` 隐式赋值，不是手动绑的
具名元组没有 `__init__`，它内部用的是 `__new__` 方法来创建实例。

```python
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])
c = Card('A', 'spades')
```

过程是：
1. 你声明字段 `['rank', 'suit']`
2. `namedtuple` 自动生成类
3. 创建实例时，通过 `__new__` 一次性把值塞进去
4. **自动完成赋值，你看不到任何 self.xxx = xxx**

关键点：
- 它的字段**本质就是实例属性**
- 但赋值是底层自动完成，不是你写 `=` 赋的
- 而且**一旦创建就不能改**（immutable）

你的理解非常准：
**具名元组是 new 实例的时候一次性赋值，属性都是实例属性，没有类属性什么事。**

---

## 3. 你的核心困惑：Python 类太“黑盒”，看不到实例有哪些属性
你这句话说得非常真实，我完全懂：

> “如果我不懂 Python 魔法方法，又看不到 self.xxx 赋值，我根本不知道这个类实例到底有哪些属性。”

这确实是 Python 动态语言的特点：
**属性可以随时绑，不写在类里也能存在。**

### 3.1 普通类的问题
你看到一个类：

```python
class User:
    pass
```

你完全不知道它将来会有：

```python
u = User()
u.name = "Tom"
u.age = 20
```

**代码里不写 self，外部根本看不出来有什么属性。**

### 3.1.1 底层：`__dict__` 与「`__init__` 不限制属性集合」

一句话结论：**Python 允许在 `__init__` 之外，给实例动态挂上任意新属性**；只要没上 `__slots__` 等限制，实例一般都有一个 **`__dict__`**，普通属性读写本质是在这个**命名空间字典**里增删键值。

```python
class User:
    def __init__(self, name: str) -> None:
        self.name = name


user = User("张三")
user.sex = "男"
user.money = 9999
user.age = 20

print(user.__dict__)
# {'name': '张三', 'sex': '男', 'money': 9999, 'age': 20}
```

要点：

- `__init__` 只是**常用**的初始化入口，并不等于「实例只能有这些键」。
- `self.xxx = ...` 与在类外 `user.xxx = ...`，多数情况下都会落到**实例的 `__dict__`**（或描述符协议，但心智模型上先记住字典这一层即可）。

和 Java / C# 这类**静态字段模型**对比：那些语言里「类体没声明的字段」往往**不能**随便挂；Python 则是**鸭子类型 + 动态命名空间**，灵活性高，代价是**结构不写在类上就不可见**。

工程上为什么不鼓励乱挂零散属性：

- 读类定义猜不出实例长什么样，维护成本高。
- 拼写错误会变成**悄悄多出一个新属性**（`Sex` 与 `sex` 是两个键）。
- 缺少 IDE 补全与静态类型检查（除非你上了 `dataclass` / `TypedDict` / `Protocol` 等约束）。

常见替代：

1. **在 `__init__` 里把字段都建出来**（哪怕先赋 `None` / 默认值），让「有哪些键」一眼可见。
2. **`@dataclass`**：先声明字段再生成 `__init__`，兼顾可读性与类型注解。
3. **`__slots__`**：显式列出允许的属性名，**禁止**再动态塞进陌生属性（会 `AttributeError`）。

```python
class LockedUser:
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name


u = LockedUser("a")
# u.sex = "男"  # AttributeError: 未在 __slots__ 声明
```

读第三方框架（例如 LangChain 一类大量「运行时挂属性 / 猴子补丁」的生态）时，**`__dict__`、实例命名空间、描述符**这套基础会反复出现；看不懂「属性从哪来」，往往就是卡在这里。

### 3.2 namedtuple 反而更清晰
`namedtuple` 强制你一开始就声明字段：

```python
Card = namedtuple('Card', ['rank', 'suit'])
```

你一眼就知道实例一定有：
- rank
- suit

而且**不能乱加属性**，非常明确。

### 3.3 现代 Python 怎么解决“看不见属性”的问题
后来 Python 新增了更清晰的结构，就是为了治你说的这个毛病：

- `@dataclass`（数据类）
- `attrs`
- `pydantic`

它们都像 namedtuple 一样：
**先声明字段，再创建实例，一眼看懂有哪些属性。**

---

## 4. 最终总结（极简版）

1. **普通类**
   - 实例属性靠 `__init__` 里 `self.xxx = xxx` 赋值
   - 可以在任意方法里修改、新增
   - 不写代码就看不到有哪些属性，对新手不友好

2. **namedtuple 具名元组**
   - 没有 `__init__`，靠 `__new__` 创建时一次性赋值
   - 字段都是**实例属性**，没有自定义类属性
   - 不可修改，结构固定

3. **你的真实痛点**
   - Python 普通类太动态，看不到实例有哪些属性
   - 不懂魔法方法、看不到 self 赋值，就完全猜不到结构
   - namedtuple / dataclass 就是为了解决这个问题，让结构**可见、固定、清晰**

---

## 5. 补充：`__setattr__` 与「赋值时谁先执行」（极简）

当你写 `self.x = 1` 或 `obj.x = 1` 时，若类实现了 `__setattr__`，通常会**先进入** `__setattr__`；你在里面怎么写，决定了是走「普通字典赋值」、走描述符、还是做校验/代理。

```python
class Trace:
    def __setattr__(self, name: str, value: object) -> None:
        print("setattr", name, "->", value)
        super().__setattr__(name, value)


t = Trace()
t.a = 1
```

心智模型：**点号赋值** →（可能）`__setattr__` → 最终落到实例存储（常见是 `__dict__`，或 `__slots__` 的固定槽位）。更细的属性访问链（`__getattribute__` / `__getattr__` / 描述符）在后续 OOP 章节再展开即可。

