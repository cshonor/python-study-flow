# 序列模式匹配：`match/case`（Python 3.10+，Fluent Python 2.6）

> **本篇定位**：掌握 Python 3.10+ 的结构模式匹配（Structural Pattern Matching，PEP 634）中最常用的**序列模式**：按结构匹配、自动绑定变量、守卫条件、兜底分支。  
> **相关**：拆包（含 `*rest` 与嵌套拆包）见 `07-tuples-as-records-and-unpacking.md`；推导式与生成器表达式见 `06-listcomps-and-genexps.md`。

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

