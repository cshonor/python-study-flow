# 10.3 用装饰器解决策略模式“自动注册”：零维护的 `best_promo`

10.2 的函数式策略模式已经把“策略类”简化成了“策略函数”，但很快会遇到一个工程痛点：

- 如果 `best_promo` 依赖一个 `promos = [...]` 列表  
  → **新增策略时必须手工把函数塞进列表**，漏一次就产生隐性 bug。

本节用 **注册式装饰器**把维护成本降为 0：策略函数只要写上 `@promotion`，就会在**导入时**自动登记到注册表里，`best_promo` 永远不需要改。

配套脚本：`strategy_auto_register_demo.py`。

---

## 一、核心实现：注册装饰器只做登记，不改行为

```python
from collections.abc import Callable
from decimal import Decimal

Promotion = Callable[[Order], Decimal]
promos: list[Promotion] = []

def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)  # 导入时登记
    return promo          # 原样返回：不包装、不改变调用语义

def best_promo(order: Order) -> Decimal:
    return max(promo(order) for promo in promos)
```

关键点：

- **装饰发生在导入时**：模块加载到 `@promotion` 那行就会执行 `promotion(func)`。
- `promotion` **返回原函数**：策略函数仍可单独调用；装饰器只承担“登记”职责。

---

## 二、为什么这个方案能“零维护”

新增策略时，你只做一件事：写函数 + 加 `@promotion`：

```python
@promotion
def bulk_item(order: Order) -> Decimal:
    ...
```

你不需要：

- 修改 `promos` 列表
- 依赖 `_promo` 后缀命名
- 写 `globals()` 或 `inspect` 内省扫描

---

## 三、进阶：带参数的注册装饰器（按组登记）

当业务增长，你可能希望“会员折扣”与“活动折扣”分组：

```python
from collections import defaultdict

groups: dict[str, list[Promotion]] = defaultdict(list)

def promotion(group: str = "default"):
    def decorate(promo: Promotion) -> Promotion:
        groups[group].append(promo)
        return promo
    return decorate
```

注意：这是参数化装饰器，所以即使默认分组也要写 `@promotion()`。

---

## 四、实践建议（避免注册式装饰器踩坑）

- **装饰器只做轻量登记**：别在装饰时做 I/O、网络请求、重计算，否则导入会变慢/变脆。
- **确保模块会被导入**：注册发生在导入时；没导入就没注册（插件系统常见坑）。
- **注册表最好可测试/可重置**：测试用例里可能需要清空注册表，避免跨用例污染。

