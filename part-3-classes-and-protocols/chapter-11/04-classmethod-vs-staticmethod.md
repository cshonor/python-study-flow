# 11.5 `classmethod` vs `staticmethod`：到底差在哪（以及什么时候该用）

这一节的目标是把两件事说清楚：

- `@classmethod` 是“面向类的绑定（绑定到 cls）”，是 **备选构造函数** 的标准工具；
- `@staticmethod` 基本就是“放在类命名空间里的普通函数”，多数情况下用模块函数更直接。

配套脚本：`classmethod_staticmethod_demo.py`（含书中 `Demo` 对照与 `Vector2d.from_polar` 示例）。  

---

## 一、定义与本质

### `@classmethod`

- 第一个参数自动传入 **类本身**（约定名 `cls`）
- 可通过 `cls` 访问类属性，并且在继承体系中会自动指向“实际调用的子类”
- 最常见用途：**备选构造函数**（`frombytes`、`from_polar`、工厂方法）

### `@staticmethod`

- **不**自动传入 `self` / `cls`
- 行为与“模块级函数”相同，只是放在类的命名空间里
- 典型用途：与类逻辑紧密但不依赖类/实例状态的工具函数（但很多时候直接写模块函数更清晰）

---

## 二、书中经典对照：`Demo.klassmeth` vs `Demo.statmeth`

```python
class Demo:
    @classmethod
    def klassmeth(*args):
        return args

    @staticmethod
    def statmeth(*args):
        return args
```

典型结果：

- `Demo.klassmeth()` → `(<class '...Demo'>,)`
- `Demo.klassmeth('spam')` → `(<class '...Demo'>, 'spam')`
- `Demo.statmeth()` → `()`
- `Demo.statmeth('spam')` → `('spam',)`

核心区别：**`classmethod` 多出来的第一个参数永远是类对象**。

---

## 三、继承上的关键差异：为什么备选构造函数要用 `cls(...)`

假设有子类 `SubVector2d(Vector2d)`：

- `SubVector2d.frombytes(...)` 应该返回 `SubVector2d`
- `SubVector2d.from_polar(...)` 也应该返回 `SubVector2d`

这就要求你在实现里用 `cls(...)`，而不是硬编码 `Vector2d(...)`。

---

## 四、一个“静态方法的典型误用”

当你需要根据“调用者是谁”创建实例时，**静态方法**做不到自动指向子类：

- `@staticmethod def from_polar(...): return Vector2d(...)`  
  子类调用仍会返回 `Vector2d`，这通常不是你想要的行为。

因此：**备选构造函数用 `classmethod`，不是 `staticmethod`。**

