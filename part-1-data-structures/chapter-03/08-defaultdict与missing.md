# 缺键要默认值：`defaultdict` 为什么好用？它和 `__missing__` 又是什么关系？

你已经在上一节看到：为了实现“缺了就建一个空 list 然后 append”，我们可以写 `if`、`get`、`setdefault`……都行，但总感觉有点绕。

`defaultdict` 的核心价值就是：**把“缺键时怎么办”变成类型的一部分**。你不需要每次都写一遍初始化逻辑，而是把规则交给 `default_factory`。

这一篇会把两件事讲透：

1. **`defaultdict` 的行为规则**：什么时候会调用 `default_factory`？什么时候不会？
2. **`__missing__` 的本质**：为什么 `defaultdict` 能做到自动补默认值？（它其实就是在缺键时用到了 `__missing__` 钩子）

---

## 纲领：`defaultdict(……)` 括号里到底是什么？

**先记一句结论**：`defaultdict(...)` 里填的是 **「造默认值的工厂」**（`default_factory`）——能 **无参 `()` 一下**就吐出一个「空壳默认值」的**类型名或函数**；**不是**塞已经造好的 `[]` / `{}`，**也不是**随便一个变量名。

### 和普通 `dict` 对比：为什么缺键会炸？

```python
d: dict[str, list[int]] = {}
# d["k"].append(1)  # KeyError：键 "k" 根本不存在，没有对象可以 append
```

普通映射里：**键不存在 = 没有 value**，自然不能对「不存在的值」做 **`append`**。

### `defaultdict` 多做了哪一步？

你写 **`defaultdict(list)`**，人话就是：

> 以后只要用 **`dd[k]`** 碰到**还不存在的 `k`**，就**先替我调用 `list()`**，造一个 **`[]`** 写进 **`dd[k]`**，再把这份列表交给我用。

同理（缺键时自动 **`工厂()`**）：

- **`defaultdict(list)`** → **`list()`** → **`[]`**  
- **`defaultdict(set)`** → **`set()`** → **空集合**  
- **`defaultdict(int)`** → **`int()`** → **`0`**  
- **`defaultdict(dict)`** → **`dict()`** → **`{}`**

### `list` / `set` / … 在这里扮演的角色

`list`、`set`、`int`、`dict`……在这里都是**类型对象**，同时也是**构造函数**：**`list()`** 产出 **`[]`**，**`set()`** 产出空集，**`int()`** 产出 **`0`**，**`dict()`** 产出 **`{}`**。

**`defaultdict` 的规则**可以记成一句：

> **键不存在** → **自动调用你括号里那个东西 `()`** → **生成空对象** → **塞进该键** → **再把这个对象返回给你**。

所以你有时觉得「括号里的 `list` 没啥存在感」——是因为**初始化发生在缺键那一次**，后台悄悄做完，你只感觉到「不报错、直接能 `append` / `add`」。

### 对照两种工厂（直觉）

**`defaultdict(list)` + `dd["a"].append(1)`**（`"a"` 原先不存在时）大致等价于后台顺序：

1. 发现 **`"a"`** 不在映射里  
2. 执行 **`list()`** → **`[]`**，写入 **`dd["a"]`**  
3. 在这个 **`[]` 上执行 `.append(1)`**

**`defaultdict(set)` + `dd["a"].add(1)`** 同理：缺键时先 **`set()`**，再 **`.add(1)`**。

### 终极一句

括号里的 **`list` / `set` / `int` / `dict`**……是**「无参就能吐出空默认值」的构造器**；作用是：**键不存在时，先给你补一个对应类型的空壳，再让你在上面增删改，不 `KeyError`。**  
（**零参铁律**、**`lambda:`**、**有参函数反例**：见 **§四 · 第 3 节**。）

---

## 零、一行看懂：`defaultdict(list)` 在干嘛

下面这段**可直接运行**：

```python
from collections import defaultdict

dd = defaultdict(list)
dd["new-key"].append(1)
print(dd)  # defaultdict(list, {'new-key': [1]})
```

**和普通 `dict` 的对比**：普通映射用 **`d[k]`** 取不存在的键会 **`KeyError`**，更不能对「不存在的值」直接 **`append`**。

```python
d: dict[str, list[int]] = {}
# d["new-key"].append(1)  # KeyError: 'new-key'
```

**`defaultdict(list)` 在缺键时做的事**（走 **`dd[k]`** 这一条路时）：

1. 发现 **`k` 尚不存在**  
2. 调用工厂 **`list()`** → 得到 **`[]`**，**写入** `dd[k]`，再把这个列表引用交给你  
3. 于是可以立刻 **`.append(...)`**，无需先写 **`if k not in dd: dd[k] = []`**

**常见用途**：分组、多值列表、词索引式累加（与 **`07-可变值与词索引.md`**、**`06-dict-defaultdict与OrderedDict对照.md`** 同一脉络；按标的/因子做多条时间序列，也是「**键 → 列表**」同一种结构）。

```python
dd = defaultdict(list)
dd["a"].append(1)
dd["a"].append(2)
dd["b"].append(99)
assert dict(dd) == {"a": [1, 2], "b": [99]}
```

**一句话**：**`defaultdict(list)` ≈ 缺键时自动给你空列表的映射**；量化/数据处理里高频写法就是 **`d[key].append(row)`**。

### 常见误解两则（大白话）

#### 1）是不是所有 key 的 **value 类型** 都必须一样？

**对。**`defaultdict(list)` 等于定死一条规矩：**缺键时用 `list()` 造默认值**，所以每个键挂上的 **value 都是「列表」这一类**；不会出现这个键是 `list`、那个键是 `int`（除非你换成 **`defaultdict(int)`** 等**另一种**映射）。

补充：列表里 **`append` 的元素**可以类型不一（一般不推荐乱混），但 **value 作为容器**，在「工厂是 **`list`**」的前提下**清一色是 `list` 实例**。

#### 2）所有 key **共用一个大列表**，还是 **各有一个专属列表**？

**各有一个、互不共用。**每遇到**新的**缺键访问，就 **`list()` 一次** → **新的 `[]`**，只绑定到**当前这个 key**。这和 **`dict.fromkeys(keys, [])`：第二个实参只求值一次、全键指向同一个列表**（见 **`07-可变值与词索引.md`** **§四**）是**反例对照**。

```python
from collections import defaultdict

dd = defaultdict(list)
dd["key1"].append(1)
dd["key1"].append(2)
dd["key2"].append(99)
dd["key2"].append(100)
assert dd["key1"] == [1, 2] and dd["key2"] == [99, 100]
assert dd["key1"] is not dd["key2"]  # 两只不同的 list 对象
```

**比喻**：像一排**独立抽屉**——`"key1"` 拉出来的是 **1 号抽屉里那只空盒**（本键专属列表），和 `"key2"` 的盒子**不是同一只**。

**两句记住**：

1. **`defaultdict(工厂)`** → 缺键时造出来的 **value「种类」**由**这一个工厂**统一。  
2. **不同 key** → **各自一份**工厂产品（例如各自一个 **`list`**），**不共用**同一对象。

---

## 一、为什么需要专门机制？

在 `dict` 里存**可变值**时，若缺键要初始化，手写 `if`、`get`、`setdefault` 都能做，但 **`defaultdict`** 把「缺键 → 建默认值」固化进类型本身：**`d[k]` 一条路径完成**，见示例 3-6。

---

## 二、`defaultdict` 原理（§3.5.1）

（**§纲领**用大白话说了「括号里是工厂、缺键时 `工厂()`」；这里是同一套规则的**术语版**。）

```python
from collections import defaultdict

dd = defaultdict(list)
dd["new-key"].append(1)
```

- 构造时传入 **`default_factory`**：**可调用对象**，无参调用时产生默认值（如 `list` → `[]`）。  
- 仅当通过 **`__getitem__`**（**`d[k]`**）访问**不存在的键**时：调用 **`default_factory()`**，把结果**写入** `d[k]` 并返回引用。  
- **`default_factory` 为 `None`**（含 `defaultdict()` 未传参）：行为与 **`dict`** 一致，缺键仍 **`KeyError`**（不会把 `None` 当工厂去调用）。  
- **`get(k)`** 不触发工厂（与 `07` 一致）。

---

## 三、示例 3-6：词索引（与 `07` 对照）

```python
import collections
import re

WORD_RE = re.compile(r"\w+")
index = collections.defaultdict(list)

with open(sys.argv[1], encoding="utf-8") as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            location = (line_no, match.start() + 1)
            index[word].append(location)
```

核心一行：**`index[word].append(location)`**，无 `setdefault`、无写回。

---

## 四、`default_factory` 能传什么？（类型 / 工厂大全）

**核心规则**：`defaultdict(X)` 里的 **`X` 必须是「无参可调用」**（callable，且 **`X()`** 合法）。缺键时会执行 **`value = X()`**，把 **`value`** 写入该键再返回。  
因此：**内置类型名**（如 **`list`、`int`**）本质是「一调就出一个默认实例」的工厂；**自定义类**也要求 **`__init__(self)` 无额外必填参数**（否则第一次缺键就会 **`TypeError`**）。

```python
from collections import defaultdict
```

### 1. 常用内置「工厂」

#### 1）`list` → `[]`

分组、多值、索引；**`dd[k].append(...)`**。

#### 2）`int` → `0`

计数、累加：**`dd["a"] += 1`** 在缺键时等价于先 **`0`** 再 **`+ 1`**。

```python
dd = defaultdict(int)
dd["a"] += 1
assert dd == {"a": 1}
```

#### 3）`float` → `0.0`

浮点累加、缺键当 **`0.0`**。

```python
dd = defaultdict(float)
assert dd["x"] == 0.0
```

#### 4）`str` → `""`

缺键当空串，再 **`+=`** 拼接（注意与 **`list`** 一样，**高频**时仍要留意拼接效率；大文本常用 **`list` + `join`**）。

```python
dd = defaultdict(str)
dd["name"] += "hello"
assert dd == {"name": "hello"}
```

#### 5）`set` → `set()`

去重、标签集合：**`.add(...)`**。

```python
dd = defaultdict(set)
dd["tags"].add("quant")
dd["tags"].add("python")
assert dd["tags"] == {"quant", "python"}
```

#### 6）`dict` → `{}`

嵌套一层映射：**`dd["user"]["name"] = "Alice"`**（外层缺键时先 **`{}`**，再写内层）。

```python
dd = defaultdict(dict)
dd["stock"]["price"] = 123
assert dd == {"stock": {"price": 123}}
```

#### 7）`tuple` → `()`

缺键得到**空元组**；元组不可变，后续往往整体**替换**为新元组，或配合其它结构使用。

```python
dd = defaultdict(tuple)
assert dd["k"] == () and isinstance(dd["k"], tuple)
```

---

### 2. 自定义工厂（函数 / `lambda` / 类）

**固定默认值**：

```python
def default_val() -> int:
    return 999


dd = defaultdict(default_val)
assert dd["x"] == 999
```

**嵌套 `defaultdict`（量化里多层分组常见）**：

```python
# 外层键 -> 内层键 -> 列表
nested: defaultdict[str, defaultdict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
nested["A股"]["贵州茅台"].append(1800)
assert dict(nested)["A股"]["贵州茅台"] == [1800]
```

**缺键时新建自定义对象**（类须**无参** `__init__` 或仅有默认参数）：

```python
class Stock:
    def __init__(self) -> None:
        self.price = 0.0
        self.vol = 0


dd = defaultdict(Stock)
dd["600000"].price = 12.5
assert dd["600000"].price == 12.5
```

---

### 3. 铁律：**必须是「零参」可调用——为什么有的写 `list`，有的写 `lambda`？**

缺键时，`defaultdict` **只会**执行 **`default_factory()`**：**不会**替你传任何位置参数、关键字参数。因此括号里必须是：**`xxx()` 合法、且不需要你额外塞实参**。

| 你放的 `xxx` | 缺键时实际调用 | 常见？ |
| :--- | :--- | :--- |
| **`list`** | **`list()`** → **`[]`** | ✅ 类型名即零参构造 |
| **`int` / `set` / `dict` / …** | **`int()`** 等 | ✅ 同上 |
| **`def f(): ...`**（无参） | **`f()`** | ✅ 自定义常数、复杂初始化 |
| **`def g(a): ...`**（有必填参） | **`g()`** | ❌ 第一次缺键就会 **`TypeError`** |
| **`lambda: …`** | **`(lambda:…)()`** | ✅ 体里可以闭包捕获「你想要的默认」 |

**为什么 `list` 能直接写？** 因为 **`list()`** 本来就不要参数，正好符合「零参工厂」。

**为什么有时必须 `lambda`？** 当你要的默认**不是**「某类型的空壳」（不是单纯的 **`list()`/`int()`**），而是**固定数**、**带初值的列表/字典** 时，没有对应的内置「零参类型名」，就用 **`lambda: 固定值`** 包成**零参**可调用。

```python
dd = defaultdict(lambda: 999)
assert dd["x"] == 999

dd2 = defaultdict(lambda: [1, 2, 3])
assert dd2["y"] == [1, 2, 3]

dd3 = defaultdict(lambda: {"name": "quant"})
assert dd3["z"] == {"name": "quant"}
```

**有参函数不能直塞**（缺键时没人给 `a` 传值）：

```python
def bad_func(a: int) -> int:
    return a


# dd = defaultdict(bad_func)
# dd["k"]  # TypeError: missing 1 required positional argument: 'a'
```

**也不能把「已经造好的实例」当工厂**（例如 **`defaultdict([1, 2, 3])`**）：`[1, 2, 3]` **不是**可调用的工厂；缺键时没法 **`()`** 一下变出新对象。

**一句记**：**`defaultdict(xxx)` → `xxx` 必须零参可调用；要带「馅儿」的默认 → `lambda:`。**

---

### 4. 速记表（日常分组 / 量化常用）

| 写法 | `default_factory()` 结果 | 典型用途 |
| :--- | :--- | :--- |
| **`defaultdict(list)`** | **`[]`** | 追加、分组、多值 |
| **`defaultdict(set)`** | **`set()`** | 去重、标签 |
| **`defaultdict(int)`** | **`0`** | 计数、**`+=`** |
| **`defaultdict(float)`** | **`0.0`** | 浮点累加 |
| **`defaultdict(str)`** | **`""`** | 缺键当空串再拼接 |
| **`defaultdict(dict)`** | **`{}`** | 嵌套一层 dict |
| **`defaultdict(tuple)`** | **`()`** | 缺键空元组（较少改原地） |
| **`lambda: …`** | 自定义 | 非无参构造、固定非空默认、**嵌套 `defaultdict`** |

---

## 五、注意与避坑

1. **`get` 不触发**：`dd.get(k)` 缺键为 `None`，**不插入**默认值。  
2. **`setdefault` vs `defaultdict`**：见 `07` §六；高频、固定工厂优先 **`defaultdict`**。  
3. **嵌套**：`defaultdict(dict)` 可写出 `dd["user"]["name"] = "Alice"`；更深结构常用 **`lambda: defaultdict(...)`** 避免手写层级。  
4. **与 `setdefault` 的 `[]` 求值**：`defaultdict(list)` 在键**已存在**时**不会**重复调用 `list()`（对比 `07` §四）。

---

## 六、`dict.__missing__(self, key)`

- **`dict` 子类**可定义 **`__missing__`**：仅当 **`__getitem__`**（`d[k]`）缺键时，解释器会调用它（**`defaultdict` 用此机制**实现工厂）。  
- 典型职责：计算默认值、**写入** `self[key]` 并返回，或 **`raise KeyError`**。  
- 适合：**单类内封装**复杂缺键策略；一般业务 **`defaultdict`** 更简单。

---

## 七、可运行对照

见 `08_defaultdict_and_missing_demo.py`（`defaultdict(list)` 索引、`get` 对比、`int` 计数、嵌套、`__missing__` 子类）。

**下一篇**：§3.5.2 **`StrKeyDict0` / `UserDict` + `__missing__`** 见 `09-字符串键字典与missing.md`。
