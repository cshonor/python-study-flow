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

