# `Counter` 深化、`shelve` 与继承 `UserDict`（§3.6 续）

这一篇把第 3 章里最容易“看过就忘”的 3 个点讲细一点：

- **`Counter`**：除了计数，还能做“多重集运算”（`+ - & |`）\n- **`shelve`**：一个“像 dict 一样用”的持久化键值存储（但有严格边界）\n- **`UserDict`**：为什么很多时候“自定义映射”更推荐继承它，而不是直接继承 `dict`

配套脚本：`shelf_counter_userdict_demo.py`。

---

## 一、`collections.Counter`（§3.6.3 续）

### 1. 定位

- **`Counter`** 是 **`dict` 子类**，值为**非负整数计数**（实现上可暂为负，见文档）；适合**可哈希对象**的频次统计。  
- 可视为**多重集（multiset）**：键为元素，值为出现次数。

### 2. 构造与累加

- 可从**可迭代对象**、**映射**或**关键字参数**构造；**`update`** 为**累加**计数，而非覆盖整条记录（与「普通 `dict.update` 覆盖同键」的直觉略有不同，需注意）。

### 3. 集合式运算（计数视角）

- **`+` / `-`**：按元素计数相加减（结果中**去掉**计数为 **0** 及以下的键）。  
- **`&` / `|`**：分别取各键计数的 **min** / **max**。  
- 具体边界以当前 CPython 文档为准；见 `shelf_counter_userdict_demo.py`。

### 4. 常用 API

- **`most_common(n)`**：返回计数最高的若干项（**`n=None`** 时全部排序列出）。  
- 其余与 **`dict`** 兼容；缺省访问不存在的键返回 **0**（与普通 **`dict`** 不同）。

---

## 二、`shelve.Shelf`（§3.6.4）

### 1. 定位

- **`shelve`** 提供基于文件的**持久化键值存储**，值以 **`pickle`** 序列化；对象实现 **`MutableMapping`**，用法上接近「可落地的 **`dict`**」。  
- **键**：须为 **字符串**（`str`）。  
- **值**：须为 **`pickle` 可序列化**的对象。

### 2. 使用要点

- 赋值后数据会写回存储（实现依赖 **`dbm`** 后端；**`sync()`** 可强制刷盘，**`close()`** 关闭；推荐 **`with shelve.open(...) as db:`** 管理资源）。  
- **`pickle` 不可用于不可信数据**：不要打开来源不明的 **`shelve`** 文件。  
- 适合**小到中等**本地持久化；大数据与并发写入应选数据库等专业方案。

---

## 三、子类化映射：优先 `UserDict` 而非 `dict`（§3.6.5）

### 1. 结论

- 书中建议：实现**自定义映射**时，**子类化 `collections.UserDict`**，而不是直接继承内置 **`dict`**。  
- **`UserDict`** 内部用 **`self.data`** 持有真正的 **`dict`**，自定义逻辑通过重写少量方法委托到 **`self.data`**，扩展点清晰。

### 2. 为何少直接继承 `dict`

- CPython 对内置 **`dict`** 做了大量**捷径**与 C 层实现；子类重写 **`__getitem__` / `__setitem__` / `__contains__`** 等时，**部分方法可能不会按你预期走到 Python 层**，或出现**递归**、**遗漏路径**（例如某些内部路径不调用你重写的钩子）。  
- **`UserDict`** 路径统一，且继承 **`MutableMapping`** 后，**`update`** 等最终会调用你定义的 **`__setitem__`**，便于保证「所有写入都经同一套键规范化」。

### 3. `Mapping.get` 与 `MutableMapping.update`

- **`Mapping.get`**：可在抽象基类层面提供默认实现；**`UserDict`** 子类通常**不必**为「配合 `__missing__`」再手写一遍 **`get`**（若需与 **`d[k]`** 完全一致，仍可用 **`try: return self[key]`** 写法，见 **`09`**）。  
- **`MutableMapping.update`**：可从映射、键值对可迭代对象、`**kwargs` 加载；内部会调用 **`__setitem__`**，从而触发你在子类中的键转换等逻辑。

### 4. 与 `StrKeyDict` 的关系

- **`StrKeyDict`**（示例 3-9）的完整对比（**`StrKeyDict0` 继承 `dict`** vs **`StrKeyDict` 继承 `UserDict`**）与代码见 **`09-str-key-dict-and-dunder-missing.md`** 及 **`str_key_dict_demo.py`**。  
- 若在 **`UserDict`** 子类中实现 **`__setitem__(self, key, value): self.data[str(key)] = value`**，则从写入路径上**统一键类型**；再配合 **`__missing__`**、**`__contains__`** 与（可选）**`get`**，行为可完整对齐业务预期。

### 5. 不可变映射（与 §3.7 衔接）

- 标准库没有「内置不可变 **`dict`**」；常见做法是 **`Mapping` + 组合**：内部持有一份映射，对外只暴露只读接口，对 **`__setitem__` / `__delitem__` / `clear`** 等**改写为抛 `TypeError`**。  
- 接口分类与 **`Mapping`/`MutableMapping`** 见 **`05-mapping-abc-and-hashable.md`**。

---

## 四、小结

| 主题 | 要点 |
| :--- | :--- |
| **`Counter`** | 计数、`update` 累加、**`most_common`**、集合式 **`+` / `-` / `&` / `|`** |
| **`shelve`** | 持久化、**键为 str**、值为 **`pickle` 安全边界** |
| **`UserDict`** | 自定义映射的**推荐基类**；与 **`StrKeyDict`**、**`09`** 对照阅读 |

---

## 五、可运行对照

见 **`shelve_counter_userdict_demo.py`**（`Counter` 字符串与运算、`shelve` 临时文件、**`UserDict` + `update`** 走 **`__setitem__`**）。
