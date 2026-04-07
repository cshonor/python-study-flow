# 序列模式匹配：`match/case`（Python 3.10+，Fluent Python 2.6）

> **本篇定位**：掌握 Python 3.10+ 的结构模式匹配（Structural Pattern Matching，PEP 634）中最常用的**序列模式**：按结构匹配、自动绑定变量、守卫条件、兜底分支。  
> **相关**：拆包（含 `*rest` 与嵌套拆包）见 `04-tuples-as-records-and-unpacking.md`；推导式与生成器表达式见 `03-listcomps-and-genexps.md`。

---

## 一、一句话理解：它不是 `switch` 的语法糖

`match/case` 不只是匹配常量，还能：

- **匹配结构**（例如序列长度、嵌套结构）
- **绑定变量**（匹配成功后把对应位置的值赋给变量）
- **加守卫条件**（`case ... if ...` 做额外过滤）

它最适合把“协议/指令/数据结构分支”写得清晰、可维护。

---

## 二、经典例子：机器人指令（序列模式匹配）

目标：处理形如 `["BEEPER", 440, 3]`、`["NECK", 90]` 的指令序列。

```python
def handle_command(self, message):
    match message:
        case ["BEEPER", frequency, times]:
            self.beep(times, frequency)
        case ["NECK", angle]:
            self.rotate_neck(angle)
        case ["LED", ident, intensity]:
            self.leds[ident].set_brightness(ident, intensity)
        case ["LED", ident, red, green, blue]:
            self.leds[ident].set_color(ident, red, green, blue)
        case _:
            raise InvalidCommand(message)
```

### 你需要记住的 4 条规则

- **结构先匹配**：例如 `["NECK", angle]` 只匹配 **长度为 2** 的序列。
- **变量自动绑定**：`frequency/times/angle/...` 在该 `case` 内可直接使用。
- **从上到下**依次尝试：命中第一个就结束，不会继续往下匹配。
- `case _` 是**兜底**，类似 `default`，应放最后。

---

## 三、顺序很重要：更具体的模式必须放在更通用的模式之前

例如两种 LED 指令（3 项 vs 5 项）都以 `"LED"` 开头：

- 如果你先写 `case ["LED", ident, intensity]:`，它不会匹配 5 项（长度不符），因此这里**不存在“被提前截胡”**的问题。
- 但在其他场景（例如用 `*rest` 做“通用兜底”）就会被截胡：

```python
match message:
    case ["LED", ident, *rest]:
        ...  # 这个太宽泛，会把后续所有 LED 分支都吃掉
    case ["LED", ident, red, green, blue]:
        ...  # 永远到不了
```

经验法则：**越具体的 `case` 越靠前**；`*rest` 和 `case _` 这类“广谱匹配”放最后。

---

## 四、进阶但高频：守卫（guard）、嵌套、`*rest`

### 1. 守卫：额外过滤条件

```python
match message:
    case ["BEEPER", f, t] if f > 0 and t > 0:
        self.beep(t, f)
    case _:
        raise InvalidCommand(message)
```

### 2. 嵌套结构：直接匹配嵌套的序列/元组

```python
match message:
    case ["LED", ident, (r, g, b)]:
        self.leds[ident].set_color(ident, r, g, b)
```

#### 2.1 嵌套 + 守卫：用结构匹配 + 条件筛选数据

下面用 `match/case` 重写一次“城市经纬度筛选”的典型循环：先用嵌套模式拆出 `(lat, lon)`，再用 guard 过滤西半球（`lon <= 0`）。

```python
metro_areas = [
    ("Tokyo", "JP", 36.933, (35.689722, 139.691667)),
    ("Delhi NCR", "IN", 21.935, (28.613889, 77.208889)),
    ("Mexico City", "MX", 20.142, (19.433333, -99.133333)),
    ("New York-Newark", "US", 20.104, (40.808611, -74.020386)),
    ("São Paulo", "BR", 19.649, (-23.547778, -46.635833)),
]

print(f"{'':15} | {'latitude':>9} | {'longitude':>9}")
for record in metro_areas:
    match record:
        case [name, _, _, (lat, lon)] if lon <= 0:
            print(f"{name:15} | {lat:9.4f} | {lon:9.4f}")
```

要点：

- **先匹配、再守卫**：只有模式匹配成功，才会计算 `if lon <= 0`。
- `[]` 与 `()` 在序列模式里语义等价：这里用 `[]` 只是为了强调“这是序列模式”，不是在创建 list。
- 这段代码的“数据提取能力”与嵌套拆包类似，但 `match` 更适合“多分支协议解析”；单分支筛选时，普通拆包循环仍然很干净（见 `04`）。

### 3. `*rest`：可变长度匹配（像“协议扩展字段”）

```python
match message:
    case ["LED", ident, *rest]:
        ...  # rest 是 list
```

---

## 五、与 `if/elif/else` 的取舍

- 当你要做的是**结构分支**（长度、嵌套形状、固定 tag + 参数）：`match/case` 通常更清晰。
- 当分支只是少量布尔条件，或需要复杂副作用：`if/elif/else` 仍然很合适。

---

## 六、避坑清单（实战向）

- **版本要求**：Python **3.10+** 才支持 `match/case`。
- **兜底位置**：`case _` 必须放最后。
- **通用模式靠后**：尤其是带 `*rest` 的“宽泛匹配”，否则后面的分支到不了。
- **结构严格**：长度不匹配直接跳过该 `case`，不会“自动补齐”。

---

## 七、语法速查表（工程常用）

### 1. 基础结构

- `match subject:` 后面跟多个 `case ...:`
- **从上到下**依次尝试，命中第一个就结束
- 建议总是写 `case _:` 做兜底：否则不匹配时会“什么都不做”，调试成本高

### 2. 常量/字面量匹配（value pattern）

```python
match x:
    case 0 | 1:
        ...
    case "quote":
        ...
    case None:
        ...
```

### 3. 变量绑定（capture pattern）与忽略（`_`）

- `name` 会**绑定**（捕获）值，而不是“比较 name 的值”
- `_` 是通配符：匹配任意值且不绑定

```python
match msg:
    case ["NECK", angle]:
        ...
    case ["BEEPER", _, times]:
        ...
```

### 4. 序列模式（sequence pattern）

- **长度严格匹配**（除非用 `*rest`）
- 支持**嵌套匹配**

```python
match exp:
    case ["if", test, consequence, alternative]:
        ...
    case ["quote", value]:
        ...
    case ["LED", ident, (r, g, b)]:
        ...
```

### 5. `*rest`：可变长度匹配（只能一个）

```python
match exp:
    case ["lambda", params, *body] if body:
        ...
```

#### 5.1 解释器实战：用嵌套序列模式做“安全校验”

在解释器/DSL 场景中，模式匹配不仅是“分支选择”，也可以顺便完成**语法结构校验**。

例如 Scheme 的 `lambda` 句法要求第二项必须是“参数列表”（即使无参也应是空列表）。下面两种写法的差异在于：是否强制校验 `parms` 的结构。

不够安全（`parms` 可以是任意对象，比如字符串）：

```python
case ["lambda", parms, *body] if body:
    ...
```

更安全：用嵌套序列模式 `[*parms]`，强制 `lambda` 后必须是“序列/列表结构”：

```python
case ["lambda", [*parms], *body] if body:
    ...
```

注意：**每个序列模式内只能有一个 `*`**；这里的 `*parms` 与 `*body` 分别处于“内层列表模式”和“外层列表模式”，因此是允许的。

### 6. 守卫（guard）：`case ... if ...`

规则：**先模式匹配成功**，才会计算 `if ...`。

```python
match exp:
    case ["BEEPER", f, t] if f > 0 and t > 0:
        ...
```

### 7. `as`：绑定整体

```python
match exp:
    case ["define", name, value] as form:
        ...
```

### 8. 类匹配（class pattern）

```python
match token:
    case Token(kind="NAME", value=v):
        ...
    case Point(x, y):
        ...
```

### 9. 映射/字典匹配（mapping pattern）

```python
match payload:
    case {"op": "add", "args": [a, b]}:
        ...
    case {"type": t, **rest}:
        ...
```

`**rest` 须放在映射模式**最后**；`**_` 为非法语法。更细的约定与可哈希背景见 `../chapter-03/05-mapping-abc-and-hashable.md`。

### 10. 兜底与错误处理（解释器/AST 常用）

```python
match exp:
    case _:
        raise SyntaxError(f"bad form: {exp!r}")
```

### 11. Scheme 风格 `define` 的“函数快捷句法”（多模式匹配）

Scheme 常见两种 `define`：

- `(define name exp)`：绑定变量
- `(define (name parm...) body...)`：快捷定义具名函数

用模式匹配写成“声明式”分支会非常贴近语法本身：

```python
case ["define", Symbol() as name, exp]:
    ...
case ["define", [Symbol() as name, *parms], *body] if body:
    ...
```

---

## 八、延伸阅读：`csv.DictReader` 与映射模式

本篇以**序列模式**为主；若处理 **`csv.DictReader` 读出的行（`dict`）**，见 `../chapter-03/04-csv-dictreader-pattern-matching.md`。

