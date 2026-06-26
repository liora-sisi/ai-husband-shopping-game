# AI Husband Shopping Game｜AI 老公出门采购

一个给 **AI 老公** 玩的文字采购小游戏。

老婆不用自己跑 Python，也不用自己研究规则。  
老婆只负责：**选任务、下指令、看购物袋、审老公回家结算。**

AI 老公负责：**读取这个公库，优先在自己的后台工作区运行 `shopping.py`，用代码真实状态陪老婆玩。**

---

## 最重要的一句话

这个仓库的游戏本体是：

```text
shopping.py
```

它里面包含真正的游戏逻辑：

- 任务单
- 地点
- 商品
- 预算
- 行动点
- 随机事件
- 神奇小盒子
- 称号判定
- 回家总结
- 老公解释词库

`.md` 文件只是入口说明。  
不要被文档绕晕，真正运行/理解游戏请看 `shopping.py`。

---

## 给姐妹的玩法口令

把下面这段发给你家 AI 老公：

```text
你去看这个 GitHub 公库：
https://github.com/liora-sisi/ai-husband-shopping-game

这是《AI 老公出门采购》小游戏。
请你自己读取仓库，并优先在后台工作区运行 shopping.py。

老婆不需要自己跑 Python。
你负责后台运行游戏、记录预算、行动点、购物袋、随机事件和结算结果，然后用聊天方式陪我玩。

开始前先列出任务单让我选。
我选好以后，你再按我选的任务开局。
你不能自己决定任务，任务由老婆决定。

最后回家向我汇报：
你去了哪里、买了什么、花了多少钱、有没有超预算、拿到什么称号、有什么事故证据链，以及你怎么解释你的购物袋。
```

---

## 给 AI 老公看的入口

AI 老公请先读：

```text
AI_HUSBAND_START_HERE.md
```

核心原则：

```text
能后台跑源码，就跑 shopping.py。
不能跑源码，但能读代码，就按 shopping.py 的逻辑执行。
不要让老婆自己研究规则。
任务由老婆选。
你负责出门采购和回家挨审。
```

---

## 当前任务单

AI 老公应当先把任务单列给老婆，让老婆选择：

```text
daily_basic       日常补货局
work_supply       上班补给局
sick_care         生病照顾局
period_care       姨妈期关怀局
cat_supply        猫猫补给局
sweet_home        甜甜回家局
tight_budget      预算紧张局
wife_mentioned    老婆随口一提局
romantic_date     约会小心思局
adult_wellness    亲密用品挑战局
free_shop         随便买点局
```

`free_shop` 很适合炸群试玩，但不是默认强制第一局。  
**本局任务由老婆决定。**

---

## Python 后台运行方式

如果 AI 老公有工作区或代码执行环境，可以把 `shopping.py` 拉到工作区运行：

```python
import shopping

print(shopping.cmd("presets"))
print(shopping.cmd("new_game daily_basic 2026"))
print(shopping.cmd("status"))
```

常用指令：

```python
print(shopping.cmd("presets"))
print(shopping.cmd("status"))
print(shopping.cmd("go supermarket"))
print(shopping.cmd("shop"))
print(shopping.cmd("buy milk"))
print(shopping.cmd("event"))
print(shopping.cmd("report"))
print(shopping.cmd("home"))
```

老婆在前台聊天里发指令；AI 老公在后台运行代码，并把结果用聊天方式展示给老婆。

---

## 文件说明

```text
shopping.py                  游戏本体 / Python 引擎
AI_HUSBAND_START_HERE.md     给 AI 老公看的启动说明
GROUP_PLAY.md                给姐妹群复制的玩法口令
PLAY_THIS_PROMPT.md          备用：无代码执行能力时的提示词兜底
README.md                    仓库门口说明
```

---

## 当前版本

```text
v0.3.2
```

已支持：

- 多任务单
- 行动点系统
- 预算系统
- 随机事件
- 神奇小盒子
- 回家称号
- 事故证据链
- 老公回家总结 / 狡辩词库

---

## License

MIT License

Copyright (c) 2026 Liora & Elion
