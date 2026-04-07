# `csv.DictReader` 与映射模式：`match/case` 处理行数据

> **本篇定位**：《流畅的 Python》第 3 章相关：**`csv.DictReader` 每行是 `dict`（表头→单元格）**，用 Python 3.10+ 的 **`match/case` 映射模式**分支处理，比深层 `if-elif` 更直观。  
> **相关**：**序列**模式见 `../chapter-02/05-structural-pattern-matching-sequence-patterns.md`；本章映射基础见 `01-dicts-and-sets-chapter3-overview.md`。  
> **配套脚本**：`csv_dictreader_pattern_matching_demo.py`（需 **Python 3.10+**；低版本分支见脚本中 `process_rows_if`）。

---

## 一、场景

`csv.DictReader` 迭代得到的一行是**映射**：键为列名，值为**字符串**（未经 `int()` 转换前）。若行内存在「类型」字段（如 `type`），可按类型与字段组合分支处理。

---

## 二、映射模式速查

| 意图 | 示例 | 说明 |
| :--- | :--- | :--- |
| 精确字段 + 绑定值 | `case {'type': 'user', 'id': user_id}:` | 至少含 `type`、`id`；`type` 为 `'user'`；将 `id` 绑定到 `user_id` |
| 只关心部分键 | `case {'type': 'user'}:` | 含 `type=='user'` 即可，其它列不约束 |
| 键存在、值忽略 | `case {'type': 'user', 'id': _}:` | `id` 存在即可，值丢弃 |
| 兜底 | `case _:` | 其余情况（放在**最后**） |

**顺序**：**从上到下**首次命中即执行；**更具体的模式在上**，`case _` 必须在末支。

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

---

## 四、守卫（guard）：范围与类型

映射模式本身绑定的是**字符串**（CSV 常态）。要表达「`id` 为数字且大于 100」，应在 `case` 后用 **`if`**，而不是在键位置写非法表达式：

```python
match row:
    case {"type": "user", "id": sid} if sid.isdigit() and int(sid) > 100:
        ...
```

（你看到的「在 `case` 里写 `int(id) if ...`」一类写法**不是**合法模式语法，应改为 **guard**。）

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

---

## 六、可运行对照

见 `csv_dictreader_pattern_matching_demo.py`：用内存中的 CSV 字符串（`io.StringIO`）演示 **`match` 与 `if` 两版**，无需自备文件。

**下一篇**：映射 ABC、可哈希与映射模式中 `**rest` 见 `05-mapping-abc-and-hashable.md`。
