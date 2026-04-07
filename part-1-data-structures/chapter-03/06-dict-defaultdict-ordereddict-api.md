# `dict`、`defaultdict`、`OrderedDict`：常用 API 对照（§3.4.2）

> **本篇定位**：《流畅的 Python》**3.4.2**：三种最常用**映射实现**的能力差异与选型；并重申**自定义类可哈希**与 `__eq__`/`__hash__` 契约。  
> **相关**：抽象接口与可哈希定义见 `05-mapping-abc-and-hashable.md`。  
> **配套脚本**：`mapping_types_three_way_demo.py`。

---

## 一、自定义类可哈希（复习）

- 默认实例常**可哈希**（基于 `id`）；若重写 **`__eq__`** 按值比较，须同步定义 **`__hash__`**（或置 `__hash__ = None` 表示不可哈希）。  
- **`__hash__`** 应只依赖**不可变**参与相等性判断的属性。  
- 完整讨论与示例见 **`05-mapping-abc-and-hashable.md`**（及其中 `frozen` dataclass 示例）。

---

## 二、三种类型一句话

| 类型 | 要点 |
| :--- | :--- |
| **`dict`** | 内置映射；**Python 3.7+** 语言规范保证**插入顺序**（与早期「无序 dict」说法不同）。 |
| **`defaultdict`** | 在 **`__getitem__`**（`d[k]`）时若缺键，用 **`default_factory`** 生成默认值；**不**改变 `get()` 行为。 |
| **`OrderedDict`** | 强调**顺序语义**与 **`move_to_end`** 等；在 3.7+ 若仅要「按插入顺序遍历」，多数情况用 **`dict` 即可**。 |

---

## 三、方法对照表（书表 3-1 骨架 + 扩展）

下列为**能力对照**（✅ 支持 / ❌ 不适用或不存在）；**具体 CPython 版本**可能对 `__copy__` 等内部方法暴露与否略有差异，以 **`copy.copy`**、**`help(type)`** 为准。

| 方法 / 属性 | `dict` | `defaultdict` | `OrderedDict` | 说明 |
| :--- | :---: | :---: | :---: | :--- |
| `clear` | ✅ | ✅ | ✅ | 清空 |
| `__contains__` / `k in d` | ✅ | ✅ | ✅ | 成员检测 |
| `copy` / `copy.copy` | ✅ | ✅ | ✅ | 浅拷贝；`defaultdict` **保留** `default_factory` |
| `default_factory` | ❌ | ✅ | ❌ | 缺键时构造默认值 |
| `__delitem__` / `del d[k]` | ✅ | ✅ | ✅ | 删除 |
| `fromkeys` | ✅ | ✅ | ✅ | 见下文「可变默认值」陷阱 |
| `get` | ✅ | ✅ | ✅ | **不**触发 `default_factory` |
| `__getitem__` / `d[k]` | ✅ | ✅ | ✅ | `defaultdict` 缺键时**会**调用工厂 |
| `items` / `keys` / `values` | ✅ | ✅ | ✅ | 动态视图 |
| `__iter__` | ✅ | ✅ | ✅ | 迭代键 |
| `__len__` | ✅ | ✅ | ✅ | 元素个数 |
| `__missing__` | ❌ | ✅ | ❌ | `defaultdict` 内部用于缺键逻辑 |
| `move_to_end` | ❌ | ❌ | ✅ | 调整键顺序 |
| `pop` / `popitem` | ✅ | ✅ | ✅ | `OrderedDict.popitem(last=True)` 可控制 **FIFO/LIFO** |
| `__reversed__` | ✅ | ✅ | ✅ | `reversed(d)` 按**插入顺序** |
| `setdefault` | ✅ | ✅ | ✅ | 与 `default_factory` 的交互见脚本 |
| `update` / `\|=` | ✅ | ✅ | ✅ | 合并 |

---

## 四、必记差异

### 1. `default_factory` 与 `get`

- **`d[k]`** 缺键 → 调 `default_factory`，写入 `d`。  
- **`d.get(k)`** 缺键 → 返回 `default` 参数，**不调** `default_factory`，**不写**入 `d`。

### 2. `fromkeys` 与可变默认值

```python
# 错：所有键共享同一个 list 对象
bad = dict.fromkeys(["a", "b"], [])

# 对：每键独立 list
good = {k: [] for k in ["a", "b"]}
```

### 3. 何时还用 `OrderedDict`

- 需要 **`move_to_end`**、**`popitem` 的 FIFO/LIFO 语义**、或与旧代码/库 API 约定时。  
- 仅「按插入顺序遍历」时，**3.7+ 的 `dict`** 一般足够。

---

## 五、可运行对照

见 `mapping_types_three_way_demo.py`（`defaultdict` 计数、`get` vs `[]`、`fromkeys` 陷阱、`OrderedDict.move_to_end`、可哈希 `User` 类）。
