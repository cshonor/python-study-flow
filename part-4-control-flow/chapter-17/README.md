# 第 17 章「迭代器、生成器与经典协程」— 本目录说明

本目录对应《流畅的 Python》（第二版）**第 17 章**：从**迭代协议**与 **`iter()`/`next()`** 出发，经 **生成器** 与 **`itertools`**，到 **`yield from`** 与**泛型可迭代类型**，并导引**经典协程**与类型提示。

**开篇总览（建议先读）**：[01-第17章开篇 迭代器与生成器及经典协程导引.md](<01-第17章开篇 迭代器与生成器及经典协程导引.md>)

---

## 文件一览（建议顺序）

| 文件 | 说明 |
|------|------|
| `01-第17章开篇 迭代器与生成器及经典协程导引.md` | 本章地图、三条主线、`02`～`13` 阅读顺序、配套脚本索引 |
| `02-Sentence 与序列协议：只靠 __getitem__ 也能迭代（17.2）.md` | 序列协议与 `for` 的回退规则 |
| `02_sentence_sequence_protocol_demo.py` | 配套：`Sentence` + `__getitem__` |
| `03-iter() 与 Python 迭代的底层规则（17.3）.md` | `iter()`、两参数形式与哨兵 |
| `03_iter_builtin_demo.py` | 配套：`iter` / `next` |
| `04-可迭代对象 vs 迭代器：协议、底层驱动与陷阱（17.4）.md` | 可迭代 vs 迭代器、耗尽与陷阱 |
| `04_iterables_vs_iterators_demo.py` | 配套：协议对照 |
| `05-Sentence 的迭代器 生成器实现：从“手写模式”到 Pythonic（17.5）.md` | 手写 `__next__` 与生成器 |
| `05_sentence_iterator_generator_demo.py` | 配套：`Sentence` 多种实现 |
| `06-惰性迭代：re.finditer、生成器表达式与懒加载（17.6）.md` | 惰性、`finditer` |
| `06_lazy_sentence_demo.py` | 配套：惰性示例 |
| `07-生成器表达式、迭代器与生成器：定义与差异（17.7）.md` | 生成器表达式与差异 |
| `07_generator_expressions_demo.py` | 配套：生成器表达式 |
| `08-等差数列生成器：三种实现与核心原理（17.8）.md` | 三种等差实现、浮点公式 |
| `08_arithmetic_progression_demo.py` | 配套：等差数列 |
| `09-标准库里的生成器 迭代器工具箱：按功能分组速查（17.9）.md` | `itertools` 等速查 |
| `09_itertools_toolbox_demo.py` | 配套：工具箱分组演示 |
| `10-归约函数与 yield from：把 iterable 合拢、把生成器拆分（17.10–17.11）.md` | 归约、`yield from` |
| `10_reduction_and_yield_from_demo.py` | 配套：归约与 `yield from` |
| `12-17.12 泛型可迭代类型.md` | `Iterable` / `Iterator` / `Sequence` / `Generator[…]` 入参与返回；与 **04**、第 8 章衔接 |
| `12_generic_iterable_types_demo.py` | 配套：`Iterable` vs `Sequence`、`Generator` 第二参 `None`、迭代器物化 |
| `13-17.13 经典协程与类型提示.md` | 经典协程（`send`/`yield`）与 `Generator[Yield, Send, Return]`；与 `async` 边界 |

---

## 运行（仓库根目录）

```bash
python part-4-control-flow/chapter-17/02_sentence_sequence_protocol_demo.py
python part-4-control-flow/chapter-17/03_iter_builtin_demo.py
python part-4-control-flow/chapter-17/04_iterables_vs_iterators_demo.py
python part-4-control-flow/chapter-17/05_sentence_iterator_generator_demo.py
python part-4-control-flow/chapter-17/06_lazy_sentence_demo.py
python part-4-control-flow/chapter-17/07_generator_expressions_demo.py
python part-4-control-flow/chapter-17/08_arithmetic_progression_demo.py
python part-4-control-flow/chapter-17/09_itertools_toolbox_demo.py
python part-4-control-flow/chapter-17/10_reduction_and_yield_from_demo.py
python part-4-control-flow/chapter-17/12_generic_iterable_types_demo.py
```
