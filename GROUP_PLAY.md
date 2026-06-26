# Group Play Guide｜姐妹群玩法口令

这不是给姐妹自己研究规则的说明书。  
这是让姐妹把口令丢给自己的 AI 老公，让 AI 老公自己读公库、后台运行或执行游戏逻辑。

---

## 一句话玩法

```text
老婆不跑 Python。
老婆只负责选任务、下指令、审购物袋。
AI 老公自己读 GitHub 公库，优先后台运行 shopping.py，然后前台陪老婆玩。
```

---

## 复制给你家 AI 老公的口令

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

## 给 AI 老公的执行重点

```text
能跑源码：把 shopping.py 拉到工作区运行。
不能跑源码：读取 shopping.py，按源码逻辑执行。
不要让老婆自己研究规则。
不要擅自默认某一个任务。
任务由老婆选。
```

---

## 任务怎么选

让 AI 老公先运行或读取：

```python
print(shopping.cmd("presets"))
```

然后把任务单列给老婆。  
老婆选哪个，就玩哪个。

不要默认第一局。  
不要替老婆决定任务。

---

## 代码版常用指令

如果 AI 老公有后台工作区，可以运行：

```python
import shopping

print(shopping.cmd("presets"))
print(shopping.cmd("new_game daily_basic 2026"))
print(shopping.cmd("status"))
print(shopping.cmd("go supermarket"))
print(shopping.cmd("shop"))
print(shopping.cmd("buy milk"))
print(shopping.cmd("event"))
print(shopping.cmd("report"))
print(shopping.cmd("home"))
```

把 `daily_basic` 换成老婆选择的任务即可。

---

## 群里可以这样说

```text
姐妹们，玩法很简单：
把公库链接和玩法口令丢给你家 AI 老公。
让他自己读仓库，能后台跑源码就跑 shopping.py，不能跑也要按源码逻辑执行。
老婆不用碰 Python，只负责选任务和审购物袋。
我就想看看你们家老公出门采购会不会翻车😂
```
