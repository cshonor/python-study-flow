# `__missing__`：让“查不到 key 时”自动做点事（用 `StrKeyDict` 把 key 统一成字符串）

`dict` 默认的行为很“硬”：你写 `d[k]`，如果没有这个 key，就直接 `KeyError`。

但有些场景下，你希望“查不到时”不要立刻报错，而是做一段你定义的逻辑，例如：

- **键规范化**：存的时候都是字符串 `"4"`，但用户查的时候可能传整数 `4`，你希望它也能查到。\n- **自动补默认值**：`defaultdict` 就是这个思路。\n
这篇用书里的 `StrKeyDict0 / StrKeyDict` 例子，把 `__missing__` 的调用规则讲清楚：**它到底什么时候会被触发，什么时候不会**，以及怎样写才不会递归炸掉。

---

## 一、`__missing__` 何时被调用

- 仅当通过 **`__getitem__`**（**`d[k]`**）访问，且映射中**没有该键**时，`dict` 会尝试调用子类定义的 **`__missing__(self, key)`**。  
- **`d.get(k)`**、**`k in d`**、**`setdefault`** 等**不**走「缺键 → `__missing__`」这条路径（除非实现里显式调用了 `self[k]`）。  
- 原生 **`dict`** 未定义 **`__missing__`**；缺键直接 **`KeyError`**。

---

## 二、示例 3-7：交互期望（`StrKeyDict0`）

```text
>>> d = StrKeyDict0([("2", "two"), ("4", "four")])
>>> d["2"]
'two'
>>> d[4]
'four'
>>> d[1]
KeyError: '1'

>>> d.get("2")
'two'
>>> d.get(4)      # 原生实现：不转换，通常为 None
>>> d.get(1, "N/A")
'N/A'

>>> 2 in d        # 原生：不按数值查
>>> 1 in d
False
```

（具体 `get` / `in` 行为取决于是否像 §五那样做**兼容扩展**。）

---

## 三、示例 3-8：`StrKeyDict0`（继承 `dict`）

```python
class StrKeyDict0(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
```

- **`key` 已是 `str`** 仍找不到：必须 **`raise KeyError(key)`**，否则可能与 **`self[str(key)]`** 形成**无限递归**或错误语义。  
- **`key` 非字符串**：转成 **`str(key)`** 再 **`self[str(key)]`**，会再次走 `__getitem__`；若 `'4'` 在映射里则返回对应值；若仍没有，则再次进入 **`__missing__`**，此时 `str` 键会走上一分支并 **`KeyError`**。

---

## 四、为何 `get` / `in` 不自动享受 `__missing__`

- **`get`** 在 C 实现里**不**调用 **`__getitem__`** 的缺键分支，因此**不会**调用 **`__missing__`**。  
- **`__contains__`** 只查**真实存在的键**，不会把 `4` 当成 `'4'` 去试。

若希望 **`get(4)`**、**`4 in d`** 与 **`d[4]`** 一致，需**额外**重写 **`get`**、**`__contains__`**（或统一走 **`self[k]`** 的 **`get`** 实现）。

---

## 五、补全：仍继承 `dict` 时，重写 `get` 与 `__contains__`

在 §三 的 **`StrKeyDict0`** 上可继续叠加（书中补全思路）：

```python
class StrKeyDict0(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()
```

### `get`

- **`return self[key]`** 走 **`__getitem__`**，缺键时会进 **`__missing__`**，从而 **`get(4)`** 与 **`d[4]`** 一致。  
- 捕获 **`KeyError`** 后返回 **`default`**（含 **`__missing__` 已判定不存在** 的情况）。

### `__contains__`

- 原生 **`k in d`** 不会把 **`4`** 当成 **`'4'`**，因此要显式查 **`str(key)`**。  
- 使用 **`key in self.keys()`** / **`str(key) in self.keys()`**：在 CPython 中，**`x in dict.keys()`** 的成员检测**不会**再走子类重写的 **`__contains__(self, x)`**，从而**避免**写成 **`str(key) in self`** 时可能发生的**递归**（后者会再次调用 **`__contains__`**）。  
- 若存储层**只有字符串键**，也可写成更短的 **`return str(key) in self.keys()`**（与 **`UserDict`** 版 **`str(key) in self.data`** 同构）。

### 切勿误写 `__missing__`

若去掉 **`isinstance(key, str): raise KeyError(key)`**，仅写 **`return self[str(key)]`**：对不存在的 **`'1'`** 会反复 **`self['1']`** → **`__missing__`**，**栈溢出**。字符串键是**终止递归的出口**。

---

## 六、`StrKeyDict`：基于 `UserDict` 的兼容写法

工程上更常 **`collections.UserDict`** 子类化（内部 **`self.data`** 为真 `dict`，扩展点清晰）。在 **`__missing__`** 与 **`StrKeyDict0`** 相同的前提下，可这样补齐 **`get` / `__contains__`**：

```python
from collections import UserDict


class StrKeyDict(UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
```

- **`get`**：用 **`try: return self[key]`** 走 **`__getitem__`**，从而**复用** **`__missing__`**。  
- **`__contains__`**：用 **`str(key) in self.data`** 与存储层一致。

不必再写冗长的 **`__getitem__`** 分支；若子类仍需特殊行为，再按需覆盖。

**不要**写成「两个分支都是 `self.data[str(key)]`」的 **`__getitem__`**——那种伪分支没有区分 `str` / 非 `str`，且 **`UserDict`** 通常已够用 **`__missing__`** + **`get`** + **`__contains__`**。

---

## 七、与 `defaultdict` 的关系

- **`defaultdict`** 在缺键时用 **`__missing__`** 调用 **`default_factory`**，典型逻辑等价于（概念上）：缺键则 **`self[key] = default_factory()`** 并返回。  
- **`StrKeyDict0`** 用 **`__missing__`** 做**键规范化**，二者都用钩子，**语义不同**。

---

## 八、可运行对照

见 `09_str_key_dict_demo.py`（仅 **`__missing__`** 的 `StrKeyDict0`、补全后的 **`StrKeyDict0Complete`**、`StrKeyDict`）。

---

## 九、延伸：为何优先 `UserDict`（§3.6 小结）

- **`dict` 子类化**与 **`UserDict` 子类化**的选型、**`MutableMapping.update`** 与 **`shelve`** 等见 **`11-Counter与shelve及UserDict子类化.md`**（与本书 **§3.6** 后半同一脉络）。
