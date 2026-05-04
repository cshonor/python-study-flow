# 序列模式匹配：`match/case`（Python 3.10+，§2.6）

下面先读 **§零 超级人话版**（不搞术语，先建立直觉），再读 **§核心定位** 及后文（规则、速查、练习与附录）。

配套脚本：`05_pattern_matching_sequence_demo.py`（需 Python 3.10+）。

---

## 零、超级人话版（不讲术语，一眼懂）

### 1. 一句话

以前你要写一堆：**先瞅第一个元素像啥，再数长度，再取下标**。

`match/case` 干的事更简单：**直接看这一条数据「长得是不是某个模板」**；长得像，`case` 里写的名字就**自动对应到槽位**，不用 `msg[0]`、`msg[1]`。

### 2. 最土的例子：指令就两种格式

消息格式固定：`["开灯", 亮度]` 或 `["左转", 角度]`。

**用 if（啰嗦）**：

```python
msg = ["左转", 90]

if msg[0] == "左转" and len(msg) == 2:
    jiaodu = msg[1]
    print("转", jiaodu)

elif msg[0] == "开灯" and len(msg) == 2:
    liangdu = msg[1]
    print("亮度", liangdu)
```

麻烦在哪：自己管长度、自己写下标，分支多了就乱。

**用 match/case（干净）**：

```python
msg = ["左转", 90]

match msg:
    case ["左转", jiaodu]:
        print("转", jiaodu)
    case ["开灯", liangdu]:
        print("亮度", liangdu)
    case _:
        print("看不懂你发的啥")
```

新手记三句就够：

1. **长得和模板一模一样才算匹配**（几个元素、各是什么位置，都要对）。  
   例如 `["左转", 90]` 一共两项 → **从上到下**找，**第一个能对上的**就是 `case ["左转", jiaodu]:`，于是 `jiaodu` 自动是 `90`。  
2. **`jiaodu`、`liangdu` 这些名字**是你在模板里起的；匹配成功就带上**对应槽位**的值，不用下标。  
3. **`case _`** = 上面谁都不像 → 兜底。

### 3. 顺序：越「死板、挑剔」的越靠前

两种开灯：简单 `["开灯", 50]`；调 RGB `["开灯", 10, 20, 30]`。

**别这样写**（带 `*` 的太宽，后面白写）：

```python
match msg:
    case ["开灯", *rest]:
        pass  # 很多「开灯」消息都会先进这里
    case ["开灯", r, g, b]:
        pass  # 往往永远轮不到
```

**人话规则**：**越具体、越长、越挑形状的 `case`，越往上放；越大而化之的放最后。**

### 4. 守卫：「长得像」之后再多卡一道

**先看像不像**（例如是不是三个槽的 `["除法", 谁, 谁]`），**像了再算后面的 `if`**。

```python
match cmd:
    case ["除法", a, b] if b != 0:
        print(a / b)
```

### 5. 啥时候用 match？啥时候老实 if？

| 用 `match/case` 更爽 | 继续 `if/elif` 就行 |
| --- | --- |
| 消息、指令、格式相对固定；列表或嵌套、一堆形状分支 | 纯比大小、几个简单布尔 |

### 6. 四句口诀（背熟够用）

1. `match` 看**长得像什么结构**。  
2. `case` 写**模板**，对上就自动拆变量。  
3. **具体在前，笼统在后**。  
4. **`case _` 兜底**（或故意不写兜底，用 `MatchError` 逼人写全分支，见 **§九 附录**）。

---

## 核心定位

**不是 `if/elif` 语法糖，也不是简单 `switch`。**

核心价值：**把数据形状、结构、长度、嵌套直接写进分支，边匹配边解构绑定变量**，特别适合**协议解析、指令分发、AST/DSL 语法校验、结构化数据分支**。本篇正文以**序列模式**（`list` / `tuple` 等线性形状）为主；**字典行、`csv.DictReader` 与映射模式**见 **§九 附录**。下面各节在用人话打底子之上，把规则写细（含英文标识，方便你对照官方文档）。

---

## 一、核心本质

1. 匹配**结构**：序列长度、嵌套层级、固定前缀标签。  
2. 自动**绑定变量**：匹配成功即解构赋值，不必手写索引。  
3. 支持**守卫条件**：`case ... if 额外判断`（**先模式匹配成功，再求值 `if`**）。  
4. **从上到下**尝试，命中第一个即终止；兜底分支放最后。

---

## 二、基础序列匹配（机器人指令经典示例）

```python
def handle_command(message):
    match message:
        # 严格匹配长度 2：标签 + 角度
        case ["NECK", angle]:
            print(f"转动颈部：{angle}°")
        # 严格匹配长度 3：标签 + 频率 + 次数
        case ["BEEPER", freq, times]:
            print(f"蜂鸣 {times} 次，频率：{freq}")
        # 兜底：非法指令
        case _:
            raise ValueError("无效指令")
```

### 四条铁律

1. **结构严格匹配**：长度不对则跳过当前 `case`，不会模糊匹配或自动补位。  
2. **位置自动绑定**：模式里的名字在该 `case` 块内直接可用。  
3. **顺序优先**：更具体的分支必须写在更宽泛的分支**上面**。  
4. **`case _`**：万能兜底，习惯上放**末尾**（见附录：未命中时的 `MatchError`）。

---

## 三、关键避坑：分支顺序与 `*rest` 广谱匹配

### 错误写法（被 `*rest` 截胡，后续分支永远走不到）

```python
match msg:
    case ["LED", ident, *rest]:  # 太宽泛，吃掉所有以 LED 开头、长度 ≥ 3 的序列
        pass
    case ["LED", ident, r, g, b]:  # 永远无法命中（若上面已能匹配）
        pass
```

### 正确原则

**越具体 → 越靠前；带 `*rest`、通配兜底 → 放最后。**

---

## 四、高频进阶用法

### 1. 守卫 Guard：结构对了再附加条件

只匹配合法数值时：**先结构匹配成功，才会执行 `if` 守卫**。

```python
match msg:
    case ["BEEPER", f, t] if f > 0 and t > 0:
        print("合法蜂鸣指令")
    case _:
        raise ValueError("参数非法")
```

### 2. 嵌套序列匹配：一键解构嵌套数据

```python
metro_areas = [
    ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
    ("Mexico City", "MX", 20.142, (19.433333, -99.133333)),
]

for rec in metro_areas:
    match rec:
        case [name, _, _, (lat, lon)] if lon <= 0:
            print(name, lat, lon)
```

**小知识点**：序列模式写成 `[...]` 或 `(...)`，匹配时**不区分** `list` / `tuple`（都是“序列形状”）；括号风格多为书写习惯（与“正在新建一个 list 字面量”无关）。

### 3. `*rest`：可变长度与协议扩展字段

捕获尾部剩余项；在**同一层**序列模式里，带名字的 `*` **最多一个**（内层、外层各有一层序列模式时，可以各有一个 `*`，见附录）。

```python
match cmd:
    case ["LOG", level, *msg_args]:
        print(f"[{level}] 日志内容：{msg_args}")
```

### 4. `as`：绑定“整个 subject”

`case 模式 as 名字` 里，`名字` 绑定的是 **`match` 的 subject**（整段被匹配的对象），不是模式中某一截子序列。

```python
match form:
    case ["define", name, val] as full_expr:
        assert full_expr is form  # 成立 → as 绑定的是 match 的 subject
        print("变量名：", name)
        print("完整表达式：", full_expr)
```

### 5. 嵌套校验（DSL / 解释器）

强制第二层必须是“序列”，避免 `parms` 混进字符串、数字等非列表结构。

```python
# 不够严：parms 可以是任意对象
case ["lambda", parms, *body]:
    pass

# 更严：第二项必须是序列，并拆到 parms
case ["lambda", [*parms], *body] if body:
    pass
```

---

## 五、`match` 与 `if/elif` 取舍

| 更适合 `match/case` | 更适合 `if/elif` |
| --- | --- |
| 结构化数据、固定协议、嵌套分支、边解构边校验 | 纯布尔分支、流程杂、副作用多的业务编排 |

---

## 六、实战避坑清单

1. **版本**：Python **3.10+** 才有 `match/case`。  
2. **兜底**：需要“吃掉所有剩余情况”时写 `case _:`；若故意不写兜底，未命中会抛 **`MatchError`**（见附录）。  
3. **广谱后置**：`*rest`、过宽序列模式一律靠后。  
4. **长度严格**：不会自动补位、不做模糊长度。  
5. **守卫时机**：先结构匹配，再执行 `if`。

---

## 七、语法速查（工程常用极简版）

| 写法 | 作用 |
| --- | --- |
| `case 1 \| 2` | 多常量或匹配 |
| `case ["TAG", x, y]` | 固定长度序列解构 |
| `case [_, val]` | 忽略某位置，只取目标值 |
| `case [a, *rest]` | 可变长度，捕获剩余 |
| `case pat if cond` | 守卫 |
| `case Cls(x, y)` | 类实例模式（本篇不展开） |
| `case _` | 通配兜底 |

---

## 八、课后练习参考答案

### 练习 1：四则基础指令分发

```python
def handle(message):
    match message:
        case ["ADD", a, b]:
            return a + b
        case ["MUL", a, b]:
            return a * b
        case ["NEG", x]:
            return -x
        case _:
            raise SyntaxError("未知指令")


assert handle(["ADD", 2, 3]) == 5  # 成立 → ADD
assert handle(["MUL", 2, 3]) == 6  # 成立 → MUL
assert handle(["NEG", 7]) == -7  # 成立 → NEG
```

### 练习 2：带守卫的除法（防除 0）

```python
def calc_div(message):
    match message:
        case ["DIV", a, b] if b != 0:
            return a / b
        case ["DIV", _, 0]:
            raise ZeroDivisionError("除数不能为0")
        case _:
            raise ValueError("非法除法指令")


assert calc_div(["DIV", 10, 2]) == 5.0  # 成立 → 正常除法
```

### 练习 3：`*rest` 错误顺序 + 修正版

```python
# 错误版：被广谱分支截胡
def bad_led(msg):
    match msg:
        case ["LED", idx, *rest]:
            return "generic"
        case ["LED", idx, r, g, b]:
            return "rgb"


# 正确版：具体在前，广谱在后
def good_led(msg):
    match msg:
        case ["LED", idx, r, g, b]:
            return "rgb"
        case ["LED", idx, *rest]:
            return "generic"
        case _:
            return "other"


assert bad_led(["LED", 0, 1, 2, 3]) == "generic"  # 成立 → 第一个分支已吃掉
assert good_led(["LED", 0, 1, 2, 3]) == "rgb"  # 成立 → 五元组走 RGB 分支
```

---

## 九、附录（与仓库其余笔记对齐）

### 1. 未命中任何 `case` 时会发生什么？

若不存在能匹配的分支，且**没有**能兜住的 `case _:`，Python 会抛出 **`MatchError`**。因此：

- 想**显式**处理“其余所有情况”→ 写 `case _:`。  
- 想**强制穷尽**（漏了分支就让程序炸）→ 故意不写 `case _:`，靠 `MatchError` 暴露不完整的协议。

### 2. 映射模式与 `csv.DictReader`

本篇以**序列模式**为主。若处理 **`csv.DictReader` 读出的 `dict` 行**，见：`../chapter-03/04-csv-DictReader与match-case.md`。

### 3. 类模式（极简）

```python
match token:
    case Point(x, y):
        ...
```

更系统的数据类与 `match` 结合见第 5 章、第 7 章相关笔记。

### 4. `*` 在嵌套模式里的计数

外层序列模式与**内层**子模式各自遵守“**同一层最多一个**带捕获的 `*`”的规则；例如 `case ["lambda", [*parms], *body]` 中，`*parms` 在内层列表模式，`*body` 在外层，**合法**。

### 5. 配套 demo（建议边看边跑）

```bash
python part-1-data-structures/chapter-02/05_pattern_matching_sequence_demo.py
```

脚本中含：机器人指令多分支、嵌套 + guard、`*rest` 顺序正反例、 evaluator / DSL 风格示例。

---

## 十、小练习（先手写再对照 §八）

1. 实现练习 1 的 `handle`，覆盖 `ADD` / `MUL` / `NEG`，`case _` 兜底。  
2. 实现练习 2 的 `calc_div`（守卫 + 除零分支）。  
3. 实现练习 3 的 `bad_led` / `good_led`，体会顺序差异。  
