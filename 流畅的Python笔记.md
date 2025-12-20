# 流畅的 Python 学习笔记

## 目录
- [第一部分：数据结构](#第一部分数据结构)
- [第二部分：函数作为对象](#第二部分函数作为对象)
- [第三部分：类和协议](#第三部分类和协议)
- [第四部分：控制流](#第四部分控制流)
- [第五部分：元编程](#第五部分元编程)

---

## 第一部分：数据结构

### 第1章：Python 数据模型

#### 特殊方法（魔术方法）
- `__repr__`: 开发者友好的字符串表示
- `__str__`: 用户友好的字符串表示
- `__len__`: 返回长度
- `__getitem__`: 支持索引和切片
- `__iter__`: 使对象可迭代
- `__contains__`: 支持 `in` 操作符

#### 示例
```python
class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                      for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    def __getitem__(self, position):
        return self._cards[position]
```

---

### 第2章：序列构成的数组

#### 列表推导式（List Comprehension）
```python
# 基本语法
[expr for item in iterable if condition]

# 示例
symbols = '$¢£¥€¤'
codes = [ord(symbol) for symbol in symbols]
```

#### 生成器表达式（Generator Expression）
```python
# 使用圆括号，节省内存
symbols = '$¢£¥€¤'
codes = tuple(ord(symbol) for symbol in symbols)
```

#### 元组（Tuple）
- 不可变序列
- 可用作记录：`city, year, pop = ('Tokyo', 2003, 32450)`
- 元组拆包：`a, b = b, a`  # 交换变量

#### 切片（Slicing）
```python
s = 'bicycle'
s[::3]  # 'bye'
s[::-1]  # 'elcycib' (反转)
```

#### 序列的 `+` 和 `*`
```python
# + 连接序列
# * 重复序列
l = [1, 2, 3]
l * 5  # [1, 2, 3, 1, 2, 3, ...]
```

---

### 第3章：字典和集合

#### 字典推导式（Dict Comprehension）
```python
DIAL_CODES = [
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
]

country_code = {country: code for code, country in DIAL_CODES}
```

#### 字典的变种
- `collections.OrderedDict`: 保持插入顺序
- `collections.ChainMap`: 多个映射合并
- `collections.Counter`: 计数器
- `collections.UserDict`: 自定义字典基类

#### 集合（Set）
```python
# 集合推导式
{chr(i) for i in range(32, 256) if 'SIGN' in unicodedata.name(chr(i), '')}
```

#### 字典和集合的实现
- 字典使用哈希表实现
- 键必须是可哈希的（不可变类型）
- 集合也是基于哈希表

---

### 第4章：文本和字节

#### 字符、码位和字节表示
- 字符：用户看到的字符
- 码位：Unicode 标准中的数字（0-1,114,111）
- 字节：存储和传输时的表示

#### 编码和解码
```python
# 编码：str -> bytes
'café'.encode('utf8')  # b'caf\xc3\xa9'

# 解码：bytes -> str
b'caf\xc3\xa9'.decode('utf8')  # 'café'
```

#### 处理编码问题
- 使用 `errors='ignore'` 或 `errors='replace'`
- 使用 `chardet` 库检测编码

#### 文件处理
```python
# 文本模式（自动编码/解码）
with open('cafe.txt', 'w', encoding='utf8') as fp:
    fp.write('café')

# 二进制模式
with open('cafe.txt', 'rb') as fp:
    content = fp.read()
```

---

## 第二部分：函数作为对象

### 第5章：一等函数

#### 函数是对象
```python
def factorial(n):
    """返回 n 的阶乘"""
    return 1 if n < 2 else n * factorial(n-1)

# 函数是对象，可以赋值
fact = factorial
fact(5)  # 120

# 函数可以作为参数传递
map(factorial, range(11))
```

#### 高阶函数
- `map`: 应用函数到序列
- `filter`: 过滤序列
- `reduce`: 累积计算
- `sorted`: 排序，可接受 `key` 参数

#### 匿名函数（Lambda）
```python
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
sorted(fruits, key=lambda word: word[::-1])
```

#### 可调用对象
- 函数
- 方法
- 类（调用时创建实例）
- 实现了 `__call__` 的类实例

---

### 第6章：使用一等函数实现设计模式

#### 策略模式
```python
# 传统方式：使用类
class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
    
    def total(self):
        return sum(item.total() for item in self.cart)
    
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

# 函数式方式：使用函数
def fidelity_promo(order):
    """为积分 >= 1000 的顾客提供 5% 折扣"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order):
    """单个商品 >= 20 个时提供 10% 折扣"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

# 使用函数列表
promos = [fidelity_promo, bulk_item_promo]
```

---

### 第7章：函数装饰器和闭包

#### 装饰器基础
```python
def deco(func):
    def inner():
        print('running inner()')
    return inner

@deco
def target():
    print('running target()')

target()  # 输出: running inner()
```

#### 装饰器执行时机
- 装饰器在函数定义时执行
- 被装饰的函数可能永远不会被调用

#### 变量作用域规则
```python
b = 6
def f2(a):
    print(a)
    print(b)  # 如果这里赋值 b，会报错（UnboundLocalError）
    b = 9
```

#### 闭包
```python
def make_averager():
    series = []
    
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)
    
    return averager

avg = make_averager()
avg(10)  # 10.0
avg(11)  # 10.5
```

#### nonlocal 声明
```python
def make_averager():
    count = 0
    total = 0
    
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    
    return averager
```

#### 装饰器实现
```python
import time
import functools

def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
```

---

## 第三部分：类和协议

### 第8章：对象引用、可变性和垃圾回收

#### 变量是标签，不是盒子
```python
a = [1, 2, 3]
b = a
a.append(4)
print(b)  # [1, 2, 3, 4] - b 和 a 指向同一个对象
```

#### 标识、相等性和别名
```python
charles = {'name': 'Charles L. Dodgson', 'born': 1832}
lewis = charles  # 别名
lewis is charles  # True - 同一个对象
lewis == charles  # True - 值相等

alex = {'name': 'Charles L. Dodgson', 'born': 1832}
alex == charles  # True - 值相等
alex is charles  # False - 不同对象
```

#### 默认参数陷阱
```python
# 错误示例
def append_to(element, target=[]):
    target.append(element)
    return target

# 正确示例
def append_to(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target
```

#### 垃圾回收
- 引用计数：主要机制
- 标记清除：处理循环引用
- 分代回收：优化性能

---

### 第9章：符合 Python 风格的对象

#### 对象表示形式
- `__repr__`: 面向开发者，应该明确、无歧义
- `__str__`: 面向用户，应该可读

#### 类方法（@classmethod）和静态方法（@staticmethod）
```python
class Demo:
    @classmethod
    def klassmeth(*args):
        return args  # 接收类作为第一个参数
    
    @staticmethod
    def statmeth(*args):
        return args  # 不接收特殊参数
```

#### 格式化显示
```python
from datetime import datetime

now = datetime.now()
format(now, '%H:%M:%S')  # '23:01:05'
'{:%I:%M %p}'.format(now)  # '11:01 PM'
```

#### 私有属性和受保护属性
- `_name`: 约定为受保护（单下划线）
- `__name`: 名称改写（双下划线），Python 会改写为 `_Class__name`

---

### 第10章：序列的修改、散列和切片

#### 协议和鸭子类型
- 协议：非正式的接口
- 鸭子类型：如果它走起来像鸭子，叫起来像鸭子，那它就是鸭子

#### 可切片的序列
```python
class Vector:
    def __init__(self, components):
        self._components = list(components)
    
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, int):
            return self._components[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))
```

#### 动态存取属性
```python
class Vector:
    shortcut_names = 'xyzt'
    
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))
```

---

### 第11章：接口：从协议到抽象基类

#### 抽象基类（ABC）
```python
from abc import ABC, abstractmethod

class Tombola(ABC):
    @abstractmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""
    
    @abstractmethod
    def pick(self):
        """随机删除元素，然后将其返回"""
    
    def loaded(self):
        """如果至少有一个元素，返回 True"""
        return bool(self.inspect())
    
    def inspect(self):
        """返回一个有序元组，由当前元素构成"""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))
```

#### 虚拟子类
```python
@Tombola.register
class TomboList(list):
    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')
    
    load = list.extend
    
    def loaded(self):
        return bool(self)
    
    def inspect(self):
        return tuple(sorted(self))
```

---

### 第12章：继承的优缺点

#### 子类化内置类型
```python
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

dd = DoppelDict(one=1)  # {'one': 1} - 不会调用 __setitem__
dd['two'] = 2  # {'one': 1, 'two': [2, 2]} - 会调用 __setitem__
```

#### 多重继承和方法解析顺序（MRO）
```python
class A:
    def ping(self):
        print('ping:', self)

class B(A):
    def pong(self):
        print('pong:', self)

class C(A):
    def pong(self):
        print('PONG:', self)

class D(B, C):
    def ping(self):
        super().ping()
        print('post-ping:', self)
    
    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)

# MRO: D -> B -> C -> A -> object
print(D.__mro__)
```

---

## 第四部分：控制流

### 第13章：正确重载运算符

#### 一元运算符
```python
def __neg__(self):  # -x
def __pos__(self):  # +x
def __abs__(self):  # abs(x)
def __invert__(self):  # ~x
```

#### 中缀运算符
```python
def __add__(self, other):  # +
def __sub__(self, other):  # -
def __mul__(self, other):  # *
def __truediv__(self, other):  # /
def __floordiv__(self, other):  # //
def __mod__(self, other):  # %
def __pow__(self, other):  # **
```

#### 反向运算符
```python
def __radd__(self, other):  # 当左操作数不支持相应运算时调用
```

#### 增量赋值运算符
```python
def __iadd__(self, other):  # +=
# 如果没有实现 __iadd__，会回退到 __add__
```

---

### 第14章：可迭代的对象、迭代器和生成器

#### 可迭代对象 vs 迭代器
- **可迭代对象**：实现了 `__iter__` 方法的对象
- **迭代器**：实现了 `__iter__` 和 `__next__` 方法的对象

```python
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = text.split()
    
    def __iter__(self):
        return SentenceIterator(self.words)

class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0
    
    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word
    
    def __iter__(self):
        return self
```

#### 生成器函数
```python
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = text.split()
    
    def __iter__(self):
        for word in self.words:
            yield word
```

#### 生成器表达式
```python
def gen_123():
    yield 1
    yield 2
    yield 3

# 生成器表达式
res1 = [x*2 for x in gen_123()]  # 列表
res2 = (x*2 for x in gen_123())  # 生成器对象
```

#### 标准库中的生成器函数
- `itertools.count()`: 无限计数
- `itertools.cycle()`: 无限循环
- `itertools.repeat()`: 重复
- `itertools.combinations()`: 组合
- `itertools.permutations()`: 排列

---

### 第15章：上下文管理器和 else 块

#### else 子句
```python
# for/while 循环的 else
for item in my_list:
    if item.flavor == 'banana':
        break
else:
    raise ValueError('No banana flavor found!')

# try 的 else
try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()  # 只在没有异常时执行
```

#### 上下文管理器
```python
# 使用 with 语句
with open('hello.txt') as f:
    f.read()

# 实现上下文管理器
class LookingGlass:
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'
    
    def reverse_write(self, text):
        self.original_write(text[::-1])
    
    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True  # 抑制异常
```

#### contextlib 模块
```python
from contextlib import contextmanager

@contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write
    
    def reverse_write(text):
        original_write(text[::-1])
    
    sys.stdout.write = reverse_write
    msg = ''
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)
```

---

### 第16章：协程

#### 生成器作为协程
```python
def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)

my_coro = simple_coroutine()
next(my_coro)  # 预激协程
my_coro.send(42)  # 发送值
```

#### 协程的状态
- `GEN_CREATED`: 等待开始执行
- `GEN_RUNNING`: 解释器正在执行
- `GEN_SUSPENDED`: 在 yield 表达式处暂停
- `GEN_CLOSED`: 执行结束

#### 预激装饰器
```python
from functools import wraps

def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

@coroutine
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count
```

#### 终止协程和异常处理
```python
coro_avg = averager()
coro_avg.send(40)  # 40.0
coro_avg.send(50)  # 45.0
coro_avg.close()  # 终止协程

# 发送异常
coro_avg.throw(ZeroDivisionError)  # 在协程内部抛出异常
```

---

### 第17章：使用 futures 处理并发

#### 并发 vs 并行
- **并发**：同时处理多个任务（可能交替执行）
- **并行**：同时执行多个任务（真正同时）

#### ThreadPoolExecutor
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

def download_one(cc):
    resp = requests.get(f'http://www.example.com/{cc.lower()}/')
    return resp.status_code

def download_many(cc_list):
    with ThreadPoolExecutor(max_workers=20) as executor:
        to_do_map = {executor.submit(download_one, cc): cc
                    for cc in cc_list}
        
        for future in as_completed(to_do_map):
            res = future.result()
```

#### ProcessPoolExecutor
```python
from concurrent.futures import ProcessPoolExecutor

def download_many(cc_list):
    with ProcessPoolExecutor() as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))
```

---

### 第18章：使用 asyncio 处理并发

#### asyncio 基础
```python
import asyncio

async def coroutine():
    print('in coroutine')
    return 'result'

# Python 3.7+
async def main():
    result = await coroutine()
    print(result)

asyncio.run(main())
```

#### 异步生成器
```python
async def async_gen():
    for i in range(3):
        yield i
        await asyncio.sleep(1)

async def main():
    async for value in async_gen():
        print(value)
```

#### 异步上下文管理器
```python
class AsyncContextManager:
    async def __aenter__(self):
        print('entering')
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        print('exiting')

async def main():
    async with AsyncContextManager() as acm:
        print('inside')
```

---

## 第五部分：元编程

### 第19章：动态属性和特性

#### 特性（Property）
```python
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price
    
    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('weight must be > 0')
```

#### 使用 `__getattr__` 和 `__getattribute__`
```python
class LazyDB:
    def __init__(self):
        self.exists = 5
    
    def __getattr__(self, name):
        value = f'Value for {name}'
        setattr(self, name, value)
        return value

# __getattribute__ 会拦截所有属性访问
class ValidatingDB:
    def __init__(self):
        self.exists = 5
    
    def __getattribute__(self, name):
        print(f'* Called __getattribute__({name!r})')
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = f'Value for {name}'
            setattr(self, name, value)
            return value
```

---

### 第20章：属性描述符

#### 描述符协议
```python
class Quantity:
    def __init__(self, storage_name):
        self.storage_name = storage_name
    
    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.storage_name]

class LineItem:
    weight = Quantity('weight')
    price = Quantity('price')
    
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price
```

#### 描述符类型
- **覆盖型描述符**：实现了 `__set__`，会覆盖实例属性
- **非覆盖型描述符**：没有 `__set__`，实例属性会覆盖描述符
- **非数据描述符**：只实现了 `__get__`

---

### 第21章：类元编程

#### 类工厂函数
```python
def record_factory(cls_name, field_names):
    try:
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass
    field_names = tuple(field_names)
    
    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)
    
    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)
    
    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i
                          in zip(self.__slots__, self))
        return '{}({})'.format(self.__class__.__name__, values)
    
    cls_attrs = dict(__slots__=field_names,
                    __init__=__init__,
                    __iter__=__iter__,
                    __repr__=__repr__)
    
    return type(cls_name, (object,), cls_attrs)
```

#### `__init_subclass__`
```python
class PluginBase:
    subclasses = []
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)
```

#### 元类（Metaclass）
```python
class EntityMeta(type):
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        for key, attr in attr_dict.items():
            if isinstance(attr, Validated):
                type_name = type(attr).__name__
                attr.storage_name = '_{}#{}'.format(type_name, key)

class Entity(metaclass=EntityMeta):
    pass
```

---

## 重要概念总结

### 数据模型
- Python 的一致性：通过特殊方法实现
- 特殊方法让对象表现得像内置类型

### 函数式编程
- 函数是一等对象
- 可以使用函数替代设计模式
- 装饰器和闭包是强大的工具

### 面向对象
- 协议和鸭子类型
- 抽象基类提供正式接口
- 多重继承需要理解 MRO

### 并发编程
- 生成器和协程
- futures 和 asyncio
- 理解并发和并行的区别

### 元编程
- 动态属性访问
- 描述符协议
- 元类和类工厂

---

## 实践建议

1. **理解 Python 数据模型**：特殊方法是 Python 一致性的基础
2. **善用生成器**：节省内存，提高性能
3. **理解引用和可变性**：避免常见的陷阱
4. **使用协议而非继承**：更灵活的设计
5. **掌握装饰器**：代码复用和横切关注点
6. **理解并发模型**：选择合适的并发方式

---

## 参考资源

- 《Fluent Python》原书
- Python 官方文档
- PEP 文档
- Python 标准库文档

---

*最后更新：2024*

