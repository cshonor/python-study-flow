# python-study-flow

《流畅的 Python》(Fluent Python) 系统化学习与笔记仓库。

本仓库按书籍核心知识点分为 **5 个 Part**，每个 Part 下再按 **`chapter-xx`** 分章；每章内用**两位编号**的 `.md` 笔记 + 可选 **`.py` 演示脚本**，方便对照《流畅的 Python》逐章夯实，并为后续量化、数据分析与 AI 工程打基础。

## 学习架构

| 模块 | 核心内容 | 关键技能 |
| :--- | :--- | :--- |
| 📚 Part 1 | 数据结构与特殊方法 | 序列、映射、集合，`__len__`、`__getitem__`、`__setitem__` 等 |
| 🧩 Part 2 | 函数作为对象与一等公民 | 高阶函数、闭包、装饰器、函数式编程 |
| 🏗️ Part 3 | 类与面向对象协议 | 自定义类型、继承、鸭子类型、抽象基类 |
| ⚡ Part 4 | 控制流与并发 | 上下文管理器、协程、异步、并发模型 |
| 🧠 Part 5 | 元编程与高级技巧 | 描述符、元类、动态属性等 |

## 目录结构

```text
python-study-flow/
├── README.md                          # 本说明
├── 流畅的Python笔记.md                 # 全书要点汇总（第 1–21 章等）
├── part-1-data-structures/            # Part 1：数据结构 / 数据模型
│   ├── README.md
│   └── chapter-01/                    # 示例：第 1 章相关笔记与 demo
│       ├── 01-*.md … 12-*.md          # 按学习顺序编号的笔记
│       ├── 05_namedtuple_usage_demo.py
│       ├── 07_french_deck_demo.py
│       ├── 08_random_choice_special_methods_demo.py
│       ├── 09_getitem_contains_demo.py
│       ├── 10_french_deck_shuffle_demo.py
│       ├── 12_collections_abc_minimal_demo.py
│       └── …
├── part-2-functions-as-objects/
├── part-3-classes-and-protocols/
├── part-4-control-flow/
└── part-5-metaprogramming/
```

各 Part 下的 **`chapter-xx`** 与书中章节对应关系以该 Part 内 `README.md` 为准；空章节目录可用 `.gitkeep` 占位以便提交。

## 使用方式

1. 先读 `流畅的Python笔记.md` 或对应 Part / 章下的编号 `.md`。
2. 有同名主题时，运行同目录下的 `.py` 做实验（建议 Python 3.10+）。
3. 示例（Part 1、第 1 章）：

```bash
python part-1-data-structures/chapter-01/07_french_deck_demo.py
python part-1-data-structures/chapter-01/10_french_deck_shuffle_demo.py
python part-1-data-structures/chapter-01/05_namedtuple_usage_demo.py
```

Windows 终端若中文乱码，可先执行 `chcp 65001` 或使用 UTF-8 终端。

## 依赖

笔记与当前示例以**标准库**为主；若后续引入第三方库，会在仓库根目录补充 `requirements.txt`。
