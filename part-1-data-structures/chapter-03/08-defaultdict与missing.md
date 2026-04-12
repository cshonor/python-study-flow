# 缺键要默认值：`defaultdict` 为什么好用？它和 `__missing__` 又是什么关系？

你已经在上一节看到：为了实现“缺了就建一个空 list 然后 append”，我们可以写 `if`、`get`、`setdefault`……都行，但总感觉有点绕。

`defaultdict` 的核心价值就是：**把“缺键时怎么办”变成类型的一部分**。你不需要每次都写一遍初始化逻辑，而是把规则交给 `default_factory`。

这一篇会把两件事讲透：

1. **`defaultdict` 的行为规则**：什么时候会调用 `default_factory`？什么时候不会？\n2. **`__missing__` 的本质**：为什么 `defaultdict` 能做到自动补默认值？（它其实就是在缺键时用到了 `__missing__` 钩子）

---

## 一、为什么需要专门机制？

在 `dict` 里存**可变值**时，若缺键要初始化，手写 `if`、`get`、`setdefault` 都能做，但 **`defaultdict`** 把「缺键 → 建默认值」固化进类型本身：**`d[k]` 一条路径完成**，见示例 3-6。

---

## 二、`defaultdict` 原理（§3.5.1）

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

## 四、常见 `default_factory`

| 工厂 | 默认值 | 用途 |
| :--- | :--- | :--- |
| `list` | `[]` | 索引、分组、多值 |
| `int` | `0` | 计数、`+= 1` |
| `set` | `set()` | 去重分组 |
| `dict` | `{}` | 嵌套一层（更深常配合 **`lambda`/`lambda: defaultdict(...)`**） |

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

见 `defaultdict_and_missing_demo.py`（`defaultdict(list)` 索引、`get` 对比、`int` 计数、嵌套、`__missing__` 子类）。

**下一篇**：§3.5.2 **`StrKeyDict0` / `UserDict` + `__missing__`** 见 `09-字符串键字典与missing.md`。
