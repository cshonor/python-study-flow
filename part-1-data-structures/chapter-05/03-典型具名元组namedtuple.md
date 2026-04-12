# 5.3 典型的具名元组：`collections.namedtuple` 从入门到进阶（以及与 `typing.NamedTuple` 的边界）

这一节要让你把 `namedtuple` 用到“随手就能写、还能读懂别人高质量代码”的程度。  
你会学到三块内容：

1. **基础定义与使用**：像 tuple 一样轻量，但字段可读  
2. **核心 API**：`_fields` / `_make` / `_asdict` / `_replace`  
3. **进阶与避坑**：默认值、动态注入方法、以及和 `typing.NamedTuple` 的关键区别

配套脚本：`03_namedtuple_typical_demo.py`（把每一个点都跑出来）。

---

## 一、先把定位说死：`namedtuple` 是“tuple 子类工厂”

`collections.namedtuple` 不是类，而是一个**工厂函数**：你给它“类名 + 字段名”，它返回一个新类。

这个新类的本质是：

- **它是 `tuple` 的子类**（不可变）
- 但多了“字段名访问”（`obj.name`）和一组元操作方法

---

## 二、5.3.1 基础定义与使用（示例：City）

### 2.1 创建类：字段名可以用字符串或可迭代对象

```python
from collections import namedtuple

City = namedtuple("City", "name country population coordinates")
```

### 2.2 实例化与访问：点语法与下标语法都可用

```python
tokyo = City("Tokyo", "JP", 36.933, (35.689722, 139.691667))

tokyo.name   # 'Tokyo'
tokyo[0]     # 'Tokyo'
```

为什么点语法更推荐？

- 可读性更强：`city.population` 比 `city[2]` 更像“字段”
- 但 tuple 特性仍在：能解包、能迭代、能用于需要 tuple 的 API

---

## 三、5.3.2 核心 API（你需要真正会用的 4 个）

### 3.1 `_fields`：字段名元组（自省/反射常用）

```python
City._fields
# ('name', 'country', 'population', 'coordinates')
```

它让你能“写泛型工具”：

- 自动把对象转成表格/CSV
- 做通用的 debug 打印

### 3.2 `_make(iterable)`：用可迭代对象构造实例（像 `*args` 的安全版）

```python
delhi_data = ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889))
delhi = City._make(delhi_data)
```

你可以把它理解成：

- `City(*delhi_data)` 的等价写法，但语义更明确（“从序列构造”）

### 3.3 `_asdict()`：转 dict（便于序列化/展示）

```python
delhi._asdict()
```

注意：

- 老书/老版本常说返回 `OrderedDict`  
- 现代 Python（3.7+）里普通 `dict` 也保序，所以你通常会看到它打印出来像普通 dict  

你要记住的是：**它返回的是“键值映射”**，非常适合交给 JSON/日志/模板系统。

### 3.4 `_replace(**kwargs)`：不可变对象的“修改”

`namedtuple` 不可变，所以“修改”只能是“基于旧对象生成新对象”：

```python
tokyo2 = tokyo._replace(population=37.0)
```

你会在很多不可变数据结构里见到这种模式：**copy-with**。

---

## 四、5.3.3 进阶：默认值与动态语言技巧

### 4.1 默认值：`defaults=...`（右侧 N 个字段）

`namedtuple` 支持 `defaults`（为最右边的 N 个字段提供默认值）：

```python
Coordinate = namedtuple("Coordinate", "lat lon reference", defaults=[None])

Coordinate(0, 0)          # reference 使用默认值 None
Coordinate(0, 0, "GPS")   # 显式提供 reference
```

把它读成一条规则更好记：

- `defaults` 里的值从右往左对齐字段  

### 4.2 动态注入属性/方法：能做，但要知道代价

`namedtuple` 生成的是普通类，所以你可以动态加方法：

```python
Card = namedtuple("Card", "rank suit")

def overall_rank(self):
    ...

Card.overall_rank = overall_rank
```

这种写法的优点：

- 体现 Python 的动态能力，短脚本/教学 demo 很方便

缺点（更重要）：

- 对读代码的人不友好：方法不是在 class 体里定义的，跳转/查找更费劲
- 工程里更推荐：用 `typing.NamedTuple`（class 语法）或 `@dataclass`

---

## 五、`namedtuple` vs `typing.NamedTuple`：你必须分清的区别

| 维度 | `collections.namedtuple` | `typing.NamedTuple` |
|---|---|---|
| 类型提示 | ❌ | ✅ |
| 写法 | 常见是函数式 | ✅ 支持 class 语法（更可读） |
| 父类 | `tuple` | `tuple` |
| 扩展方法 | 能动态加，但不推荐 | ✅ 直接在 class 里写方法（推荐） |
| 典型用途 | 极简只读记录、性能敏感 | 现代代码库：只读数据 + 类型检查 |

一句话总结：

- 你要“轻量只读记录 + 类型提示” → **`typing.NamedTuple`**
- 你要“轻量只读记录，快速写完就跑” → **`namedtuple`**

---

## 六、避坑清单（新手最容易踩）

1. **不可变**：不能给字段赋值（会 `AttributeError`）。  
2. **字段名要求**：必须是合法标识符；别用关键字、别以下划线开头（避免与内部属性冲突）。  
3. **`_asdict()` 是“转映射”**：适合序列化；但别误以为它会递归转换子对象（它只转换一层）。  
4. **动态注入要节制**：写 demo 可以，写业务最好别这么干。  

---

## 七、可运行对照

运行：

```bash
python part-1-data-structures/chapter-05/03_namedtuple_typical_demo.py
```

脚本覆盖：

- `City` 的基础创建与访问
- `_fields/_make/_asdict/_replace`
- `defaults=...` 默认值
- 动态注入方法（Card 排序）
- 与 `typing.NamedTuple` 的对比（类型注解与方法）

