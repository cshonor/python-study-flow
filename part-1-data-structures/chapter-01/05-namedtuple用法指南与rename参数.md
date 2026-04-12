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
TypeName = namedtuple(typename, field_names)

# 创建实例
instance = TypeName(value1, value2, ...)
```

你看到的典型写法：

```python
Card = namedtuple('Card', ['rank', 'suit'])
```

### 参数说明
### 2.1 参数说明（必选 + 可选）

#### 2.1.1 `typename`（必选）
- **含义**：类型名（字符串），也就是生成的类名
- **示例**：`'Card'`

#### 2.1.2 `field_names`（必选）
- **含义**：字段名的**可迭代集合**；每一项都是字段名字符串
- **最常见写法**：传 `list`（你口语说的“数组”指的就是这里的 list）

```python
Card = namedtuple('Card', ['rank', 'suit'])
```

也可以写成空格分隔的字符串，或传 `tuple`：

```python
Card = namedtuple('Card', 'rank suit')
Card = namedtuple('Card', ('rank', 'suit'))
```

##### `field_names` 和 `array.array` 无关

- `array.array` 面向的是**同类型数值存储**（int/float 等）
- `namedtuple` 的 `field_names` 面向的是**字段名字符串**（定义“属性标签”）

#### 2.1.3 `rename`（可选，默认 `False`）
当 `field_names` 中出现 **Python 关键字**、**重复字段名**、或 **非法标识符** 时：

- `rename=False`：直接报错
- `rename=True`：自动重命名无效字段为 `_0`、`_1`…（保证字段名合法）

```python
from collections import namedtuple

Person = namedtuple('Person', ['name', 'class', 'name'], rename=True)
print(Person._fields)  # ('name', '_1', '_2')
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

### 5.1 关键特性

1. **不可变（immutable）**
   ```python
   # card1.rank = 'B'  # 报错
   ```

2. **是 `tuple` 的子类**
   - 支持索引、迭代、解包、比较等所有元组能力

3. **比手写 class 更省代码**
   - 不用手写 `__init__` / `__repr__` 等常见样板代码

4. **适合结构化数据**
   - 例如：K 线、订单、持仓、坐标、配置项、返回值等

### 5.2 更精确的理解（避免误解）

- `namedtuple('Card', ['rank', 'suit'])` **生成的是一个类**（这里类名是 `Card`），字段名列表是 `rank/suit`。
- 但它**不是“只有属性、没有方法”**：生成的类是 `tuple` 的子类，自带元组的能力，并且还有 `_make()` / `_asdict()` / `_replace()` 等辅助方法。
- 它也**不等价于你手写的普通可变类**：`namedtuple` 实例是不可变对象，字段不能重新赋值（想“改值”用 `_replace()` 生成新实例）。

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

