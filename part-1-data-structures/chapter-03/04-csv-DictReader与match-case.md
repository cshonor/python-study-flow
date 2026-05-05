# `csv.DictReader`：每一行都是 dict，怎么写出“看得懂”的分支处理？

很多新手第一次用 `csv.DictReader` 会有两个困惑：

1. **为什么每一行不是 list，而是 dict？**  
2. **为什么我一堆 `if/elif` 越写越乱？**

这篇笔记只做一件事：用一个小 CSV 例子告诉你——当“每一行都是 dict”时，怎么写出清晰的分支代码。

你会看到两种写法：

- Python 3.10+：用 `match/case` 的**映射模式**写分支（更像“声明式规则”）
- 任何 Python 3.x：用 `if/elif`（等价逻辑，便于兼容）

---

## 零、大白话一步步拆开（先读这段再往下看）

### 总括一句话

**`csv.DictReader`：CSV 每一行，自动变成「表头当键、单元格当值」的 `dict`。**  
好处：**不用数第几列**，按列名取值，读起来像在读表。

---

### 1. 普通 `reader` 和 `DictReader` 差在哪？

假设文件头是：

```text
type,id,note
user,42,alice
order,101,food
```

- **`csv.reader`**：一行是一个 **`list`**，例如 `["user", "42", "alice"]`。取值靠 **`row[0]`、`row[1]`**——表头一改顺序，下标全乱。  
- **`csv.DictReader`**：一行是一个 **`dict`**，例如 `{"type": "user", "id": "42", "note": "alice"}`。取值写 **`row["type"]`、`row["id"]`**——**跟列顺序无关**，语义清楚。

---

### 2. 第一大坑：值**全是字符串**

哪怕格子里写的是数字 `42`、`101`，读进来也是 **`"42"`、`"101"`**（`str`）。不能直接：

```python
# row["id"] > 100  # ❌ 字符串和整数比，类型不对
```

要先转：

```python
int(row["id"]) > 100  # ✅
```

在 **`match/case`** 里做数值判断，用 **`if` 守卫**（见 **§四**），因为模式里不能乱塞 `int(...)` 表达式。

---

### 3. 为啥要「分支」？两种写法

同一 CSV 里常有不同 `type`（`user` / `order` / `admin` …），不同类型走不同逻辑 → **分支**。

| 写法 | 适合 |
| :--- | :--- |
| **`match/case`（3.10+）** | 像写规则：字典**至少包含**这些键且值对上，还能顺便绑定 `case {"id": sid}` |
| **`if/elif`** | 全版本；逻辑一样，条件容易越堆越长 |

映射模式是**包含式**匹配：多出来的键一般不妨碍命中；**更具体的 `case` 必须写在更宽泛的上面**，否则后面的分支永远进不去（见 **§二** 与下面第 7 条）。

---

### 4. 第二个大坑：分支顺序

```text
❌ 宽泛在前、具体在后 → 具体分支永远走不到
✅ 具体在前、宽泛在后，最后 case _ 兜底
```

---

### 5. 七条极简背诵

1. `DictReader` 每行是 **`dict`**：键 = 表头，值 = **字符串**。  
2. 优点：按**列名**取值，不背下标。  
3. 数字比较前先 **`int()` / `float()`**。  
4. 不同类型用分支：`match` 或 `if/elif`。  
5. 映射模式是**包含式**匹配，可 **`case {"id": sid}`** 绑定变量。  
6. 数值条件写在 **`if` 守卫**里。  
7. **顺序：具体在上，宽泛在下**。

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

- CSV 读出来的值几乎都是字符串。
- 你要做数值判断（比如 `id > 100`）时，必须在 guard 里显式 `int(...)`。
- 这不是 `match/case` 的限制，而是 CSV 本身的数据类型就是文本。

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

- `match/case` 更像“写规则”：你更容易看出每个分支到底需要哪些字段。
- `if/elif` 更像“写过程”：写久了容易堆条件，看起来更乱。

---

## 六、可运行对照

见 `04_csv_dictreader_pattern_matching_demo.py`：用内存中的 CSV 字符串（`io.StringIO`）演示 **`match` 与 `if` 两版**，无需自备文件。

运行：

```bash
python part-1-data-structures/chapter-03/04_csv_dictreader_pattern_matching_demo.py
```

下一篇会把“映射的抽象接口（Mapping）”“可哈希”“映射模式里的 `**rest`”讲清楚，见 `05-Mapping抽象与可哈希.md`。

---

## 七、小练习（把 if/elif 改写成 match/case）

1. 给 `type == "user"` 增加一个分支：当 `note` 为空字符串时，输出 `"anonymous"`。  
2. 新增一种行：`type == "admin"`，要求必须同时有 `id` 与 `note`，否则走兜底。  
3. 尝试写一个“太宽泛的 case”放到前面（例如只判断 `{"type": "user"}`），观察它会不会让后面的更具体分支到不了。  

---

## 八、最简可运行 demo（复制即跑，无需 CSV 文件）

用内存里的 CSV 字符串 + `io.StringIO`，和仓库脚本 **`04_csv_dictreader_pattern_matching_demo.py`** 同一思路：

```python
import csv
from io import StringIO

csv_text = """type,id,note
user,42,alice
order,101,food
"""

f = StringIO(csv_text)
for row in csv.DictReader(f):
    assert isinstance(row, dict)  # 成立 → 每行是 dict
    assert row["id"] == str(row["id"])  # 成立 → 读到的 id 是字符串
    print(row)
```

若要连 **`match/case`** 一起看输出，在项目根目录运行：

```bash
python part-1-data-structures/chapter-03/04_csv_dictreader_pattern_matching_demo.py
```

