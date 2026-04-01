# Python namedtuple 具名元组使用详解

## 1. 什么是 namedtuple
`namedtuple` 是 Python 内置的**具名元组**，属于 `collections` 模块。

- 本质是一个**轻量级、不可变的类**
- 用法像元组 `tuple`，但可以通过**字段名**访问元素
- 比手动写 class 更简洁，比普通元组可读性更强

## 2. 基本语法结构

```python
from collections import namedtuple

# 创建具名元组类型
类型名 = namedtuple(类型名称字符串, 字段名字符串/可迭代对象)

# 创建实例
实例 = 类型名(值1, 值2, ...)
```

你看到的典型写法：
```python
Card = namedtuple('Card', ['rank', 'suit'])
```

### 参数说明
1. **第一个参数**：`'Card'`
   具名元组的**类型名称**，一般和变量名保持一致。

2. **第二个参数**：`['rank', 'suit']`
   这是一个**列表（你说的数组）**，里面是字段名。
   也可以写成空格分隔的字符串：
   ```python
   Card = namedtuple('Card', 'rank suit')
   ```

## 3. 完整示例（以扑克牌为例）

### 3.1 定义具名元组
```python
from collections import namedtuple

# 定义：名字是 Card，字段是 rank 和 suit
Card = namedtuple('Card', ['rank', 'suit'])
```

### 3.2 创建实例
```python
# 传入对应字段的值
card1 = Card('A', 'spade')
card2 = Card('K', 'heart')
```

### 3.3 访问方式
```python
# 1. 通过字段名访问（推荐，可读性高）
print(card1.rank)   # A
print(card1.suit)   # spade

# 2. 像元组一样通过下标访问
print(card1[0])     # A
print(card1[1])     # spade
```

### 3.4 遍历与解包
```python
# 遍历
for v in card1:
    print(v)

# 解包
rank, suit = card1
```

## 4. 常用实用方法

namedtuple 自带几个非常方便的方法：

### 4.1 _make()：从可迭代对象创建实例
```python
data = ['Q', 'club']
card3 = Card._make(data)
```

### 4.2 _asdict()：转为字典
```python
print(card1._asdict())
# OrderedDict([('rank', 'A'), ('suit', 'spade')])
```

### 4.3 _replace()：创建新实例（不可修改原对象）
```python
new_card = card1._replace(rank='2')
```

## 5. 特点与注意事项

1. **不可变**
   和 tuple 一样，创建后不能修改字段值：
   ```python
   # card1.rank = 'B'  # 报错
   ```

2. **是 tuple 的子类**
   所有 tuple 操作都支持：索引、切片、拼接、比较等。

3. **比普通 class 更轻量**
   不需要写 `__init__`，内存占用更低。

4. **非常适合结构化数据**
   如：K线、订单、坐标、配置项、返回值等。

## 6. 适用场景

- 函数需要返回多个结构化值
- 读取 CSV/数据库行记录
- 量化策略中的订单、持仓、K线数据
- 不想定义完整类，但需要清晰字段名

## 7. 总结

- `namedtuple` 来自 `collections`
- 第一个参数：类型名（字符串）
- 第二个参数：字段列表（列表或字符串）
- 实例可通过 `.字段名` 或 `[下标]` 访问
- 不可变、轻量、可读性强

