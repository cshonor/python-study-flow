# 5.3 典型的具名元组：`collections.namedtuple` 从入门到进阶（以及与 `typing.NamedTuple` 的边界）

这一节要让你把 `namedtuple` 用到“随手就能写、还能读懂别人高质量代码”的程度。  
你会学到三块内容：

1. **基础定义与使用**：像 tuple 一样轻量，但字段可读  
2. **核心 API**：`_fields` / `_make` / `_asdict` / `_replace`  
3. **进阶与避坑**：默认值、动态注入方法、以及和 `typing.NamedTuple` 的关键区别

配套脚本：`03_namedtuple_typical_demo.py`（把每一个点都跑出来）。

---

## 〇、一段代码看全（与脚本第 1、2 节一致）

下面可以直接复制进 REPL 或 `.py` 里跑一遍；**注释里是典型输出**，以你本机为准。

```python
from collections import namedtuple

# 1) 定义：类名字符串与 typename 一致；字段可用空格分隔字符串或列表
City = namedtuple("City", "name country population coordinates")
# 等价写法：namedtuple("City", ["name", "country", "population", "coordinates"])

tokyo = City("Tokyo", "JP", 36.933, (35.689722, 139.691667))
print(tokyo)                    # City(name='Tokyo', country='JP', ...)
print(tokyo.name, tokyo[0])     # Tokyo Tokyo
print(City._fields)             # ('name', 'country', 'population', 'coordinates')

delhi = City._make(("Delhi NCR", "IN", 21.935, (28.613889, 77.208889)))
print(delhi._asdict())          # {'name': 'Delhi NCR', 'country': 'IN', ...}

tokyo2 = tokyo._replace(population=37.0)
print(tokyo.population, tokyo2.population)  # 36.933 37.0  （原实例不变）

# 2) 默认值：defaults 从右往左对齐最后几个字段
Coordinate = namedtuple("Coordinate", "lat lon reference", defaults=[None])
print(Coordinate(0, 0))              # Coordinate(lat=0, lon=0, reference=None)
print(Coordinate(0, 0, "GPS"))       # reference 显式给出
```

**tuple 老本行**（同一 `City` 实例上都能用）：

```python
name, country, pop, coord = tokyo   # 解包
assert "JP" in tokyo                # 成员检测按元素
assert len(tokyo) == 4
assert hash(tokyo) == hash(tuple(tokyo))  # 全字段可哈希时实例可哈希
```

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
# 字段较多时更清晰：
# City = namedtuple("City", ["name", "country", "population", "coordinates"])
```

**注意**：第一个参数是**类名**（`typename`），一般与赋值左侧同名，例如 `City = namedtuple("City", ...)`。

### 2.2 实例化与访问：点语法与下标语法都可用

```python
tokyo = City("Tokyo", "JP", 36.933, (35.689722, 139.691667))

tokyo.name         # 'Tokyo'
tokyo[0]           # 'Tokyo'
tuple(tokyo)       # ('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
```

为什么点语法更推荐？

- 可读性更强：`city.population` 比 `city[2]` 更像“字段”
- 但 tuple 特性仍在：能解包、能迭代、能用于需要 tuple 的 API

**迭代与解包示例**：

```python
for field_value in tokyo:
    print(field_value)

name, country, pop, coord = tokyo
```

---

## 三、5.3.2 核心 API（你需要真正会用的 4 个）

假定已有 `City` 与 `tokyo`（见 **§〇** 或 **§二**）。四个 API 的用途可以记成：**列字段、从序列造、转 dict、带替换拷贝**。

### 3.0 四个 API 一口气跑完（复制即用）

```python
from collections import namedtuple

City = namedtuple("City", "name country population coordinates")
tokyo = City("Tokyo", "JP", 36.933, (35.689722, 139.691667))

# ① _fields：类属性，拿到字段名元组
print(City._fields)           # ('name', 'country', 'population', 'coordinates')
print(list(zip(City._fields, tokyo)))  # [('name', 'Tokyo'), ('country', 'JP'), ...]

# ② _make：长度必须与字段数一致，顺序对应 _fields
row = ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889))
delhi = City._make(row)
assert delhi == City(*row)    # 与解包构造等价；_make 强调「来自一整行数据」

# ③ _asdict：浅层映射（值仍是原对象，不递归「拆成基本类型」）
d = delhi._asdict()
print(d["name"], type(d["coordinates"]))  # Delhi NCR <class 'tuple'>

# ④ _replace：只改你传入的字段，其余从旧实例拷贝；得到新实例，旧的不变
tokyo2 = tokyo._replace(population=37.0)
assert tokyo is not tokyo2 and tokyo.population == 36.933 and tokyo2.population == 37.0
```

### 3.1 `_fields`：字段名元组（自省/反射常用）

```python
City._fields
# ('name', 'country', 'population', 'coordinates')

# 和某一行 zip 成「列名 → 值」，写 CSV / 日志很方便：
dict(zip(City._fields, tokyo))
# {'name': 'Tokyo', 'country': 'JP', 'population': 36.933, 'coordinates': (...)}
```

它让你能“写泛型工具”：

- 自动把对象转成表格/CSV
- 做通用的 debug 打印

### 3.2 `_make(iterable)`：用可迭代对象构造实例（像 `*args` 的安全版）

```python
delhi_data = ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889))
delhi = City._make(delhi_data)

# 与下面等价；从数据库行、CSV 一行、split 后的列表构造时，_make 读起来更直观
assert delhi == City(*delhi_data)
```

你可以把它理解成：

- `City(*delhi_data)` 的等价写法，但语义更明确（“从序列构造”）

**注意**：可迭代对象**长度必须等于字段个数**；否则 `TypeError`。

### 3.3 `_asdict()`：转 dict（便于序列化/展示）

- 把整个 NamedTuple 实例，一键转成普通 dict（字段名 → 值）Python

- Python 3.8+ 返回 普通 dict（有序）Python

- Python 3.1–3.7 返回 OrderedDictPython

```python
from typing import NamedTuple

class City(NamedTuple):
    name: str
    country: str
    population: float
    coordinates: tuple[float, float]

delhi = City(
    name="Delhi NCR",
    country="IN",
    population=21.935,
    coordinates=(28.613889, 77.208889)
)

# 调用 _asdict()
print(delhi._asdict())
# {'name': 'Delhi NCR', 'country': 'IN', 'population': 21.935, 'coordinates': (28.613889, 77.208889)}
```

注意：

- 老书/老版本常说返回 `OrderedDict`  
- 现代 Python（3.7+）里普通 `dict` 也保序，所以你通常会看到它打印出来像普通 dict  

你要记住的是：**它返回的是“键值映射”**，非常适合交给 JSON/日志/模板系统；**只做一层**，不会把里面的 tuple 再拆成更细的字典。

### 3.4 `_replace(**kwargs)`：不可变对象的“修改”

`namedtuple` 不可变，所以“修改”只能是“基于旧对象生成新对象”：

```python
tokyo2 = tokyo._replace(population=37.0)
# tokyo 仍是 36.933；tokyo2 是新实例

# 可同时改多个字段（仍是一次拷贝出一个新实例）
tokyo3 = tokyo._replace(name="東京", country="JP")
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

lat, lon, ref = Coordinate(1.0, 2.0)
assert ref is None
```

把它读成一条规则更好记：

- `defaults` 里的值从右往左对齐字段  

### 4.2 动态注入属性/方法：能做，但要知道代价

`namedtuple` 生成的是普通类，所以你可以动态加方法（与脚本第 3 节一致，这里只保留骨架）：

```python
Card = namedtuple("Card", ["rank", "suit"])

rank_value = {"2": 2, "3": 3, "J": 11, "Q": 12, "K": 13, "A": 14}  # 可按需补全
Card.suit_values = {"spades": 3, "hearts": 2, "diamonds": 1, "clubs": 0}

def overall_rank(self: Card) -> int:
    return rank_value[self.rank] * 4 + Card.suit_values[self.suit]

Card.overall_rank = overall_rank

deck = [Card("2", "spades"), Card("A", "hearts"), Card("A", "spades")]
deck.sort(key=Card.overall_rank)
# deck[-1] 即为 overall_rank 最大的那张；实例上可调用 deck[-1].overall_rank()
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

**与脚本第 4 节一致的最小 `NamedTuple` 例子**（类型注解 + 实例方法写在 class 体内）：

```python
from typing import NamedTuple, get_type_hints

class CoordinateT(NamedTuple):
    lat: float
    lon: float

    def __str__(self) -> str:
        return f"({self.lat:.3f}, {self.lon:.3f})"

c = CoordinateT(55.756, 37.617)
print(c)                       # 走你自定义的 __str__
print(get_type_hints(CoordinateT))  # {'lat': <class 'float'>, 'lon': <class 'float'>}
print(issubclass(CoordinateT, tuple))  # True
```

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

