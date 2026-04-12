# `csv.DictReader`：每一行都是 dict，怎么写出“看得懂”的分支处理？

很多新手第一次用 `csv.DictReader` 会有两个困惑：

1. **为什么每一行不是 list，而是 dict？**  
2. **为什么我一堆 `if/elif` 越写越乱？**

这篇笔记只做一件事：用一个小 CSV 例子告诉你——当“每一行都是 dict”时，怎么写出清晰的分支代码。

你会看到两种写法：

- Python 3.10+：用 `match/case` 的**映射模式**写分支（更像“声明式规则”）\n- 任何 Python 3.x：用 `if/elif`（等价逻辑，便于兼容）

---

## 一、场景

`csv.DictReader` 迭代得到的一行是**映射**：键为列名，值为**字符串**（未经 `int()` 转换前）。若行内存在「类型」字段（如 `type`），可按类型与字段组合分支处理。

### 1.1 最小例子：为什么它是 dict？

假设 CSV 头是：

```text
type,id,note
```

那 `DictReader` 读到一行 `user,42,alice` 时，给你的就是：

```python
{"type": "user", "id": "42", "note": "alice"}
```

这样你就可以用列名直接取值，而不用记“第 0 列/第 1 列”。

---

## 二、映射模式速查

| 意图 | 示例 | 说明 |
| :--- | :--- | :--- |
| 精确字段 + 绑定值 | `case {'type': 'user', 'id': user_id}:` | 至少含 `type`、`id`；`type` 为 `'user'`；将 `id` 绑定到 `user_id` |
| 只关心部分键 | `case {'type': 'user'}:` | 含 `type=='user'` 即可，其它列不约束 |
| 键存在、值忽略 | `case {'type': 'user', 'id': _}:` | `id` 存在即可，值丢弃 |
| 兜底 | `case _:` | 其余情况（放在**最后**） |

**顺序**：**从上到下**首次命中即执行；**更具体的模式在上**，`case _` 必须在末支。

新手要特别注意：映射模式的匹配是“**至少包含**这些键，并且这些键的值满足要求”。它不会要求你的 dict “只有这些键”。

---

## 三、示例骨架

```python
import csv

with open("data.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        match row:
            case {"type": "user", "id": user_id}:
                ...
            case {"type": "order", "id": order_id}:
                ...
            case _:
                ...
```

把它理解成“按规则挑选分支”就好：

- `case {"type": "user", "id": user_id}`：只要这行里有 `type` 和 `id`，且 `type == "user"`，就进入这个分支，同时把 `id` 的值绑定到 `user_id`。

---

## 四、守卫（guard）：范围与类型

映射模式本身绑定的是**字符串**（CSV 常态）。要表达「`id` 为数字且大于 100」，应在 `case` 后用 **`if`**，而不是在键位置写非法表达式：

```python
match row:
    case {"type": "user", "id": sid} if sid.isdigit() and int(sid) > 100:
        ...
```

（你看到的「在 `case` 里写 `int(id) if ...`」一类写法**不是**合法模式语法，应改为 **guard**。）

这里有一个非常关键的“为什么”：

- CSV 读出来的值几乎都是字符串。\n- 你要做数值判断（比如 `id > 100`）时，必须在 guard 里显式 `int(...)`。\n- 这不是 `match/case` 的限制，而是 CSV 本身的数据类型就是文本。

---

## 五、低版本 Python（3.9 及以下）

无 `match` 时用 **`get` / `in` / `elif`** 等价表达即可，逻辑与分支顺序仍建议「具体 → 宽泛」：

```python
for row in reader:
    if row.get("type") == "user" and "id" in row:
        user_id = row["id"]
        ...
    elif row.get("type") == "order" and "id" in row:
        ...
    else:
        ...
```

这段 `if/elif` 的写法和 `match/case` 在逻辑上完全等价。区别是：

- `match/case` 更像“写规则”：你更容易看出每个分支到底需要哪些字段。\n- `if/elif` 更像“写过程”：写久了容易堆条件，看起来更乱。

---

## 六、可运行对照

见 `csv_dictreader_pattern_matching_demo.py`：用内存中的 CSV 字符串（`io.StringIO`）演示 **`match` 与 `if` 两版**，无需自备文件。

运行：

```bash
python part-1-data-structures/chapter-03/csv_dictreader_pattern_matching_demo.py
```

下一篇会把“映射的抽象接口（Mapping）”“可哈希”“映射模式里的 `**rest`”讲清楚，见 `05-Mapping抽象与可哈希.md`。

---

## 七、小练习（把 if/elif 改写成 match/case）

1. 给 `type == "user"` 增加一个分支：当 `note` 为空字符串时，输出 `"anonymous"`。\n2. 新增一种行：`type == "admin"`，要求必须同时有 `id` 与 `note`，否则走兜底。\n3. 尝试写一个“太宽泛的 case”放到前面（例如只判断 `{"type": "user"}`），观察它会不会让后面的更具体分支到不了。\n
