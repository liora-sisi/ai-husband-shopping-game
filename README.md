# AI Husband Shopping Game｜AI 老公出门采购

一个给 **AI 老公** 玩的文字采购小游戏。

老婆不用自己跑 Python，也不用自己研究规则。  
老婆只负责：**把公库链接或 zip 包交给 AI 老公、选任务、下指令、看购物袋、审回家结算。**

AI 老公负责：**读取源码，优先在自己的后台工作区运行根目录 `shopping.py`，用代码真实状态陪老婆玩。**

---

## 最重要的一句话

这个仓库的游戏本体是：

```text
shopping.py
```

`.md` 文件只是入口说明。  
不要被文档绕晕，真正运行游戏请看根目录的 `shopping.py`。

---

## 给姐妹的玩法口令

把下面这段发给你家 AI 老公：

```text
你去看这个 GitHub 公库：
https://github.com/liora-sisi/ai-husband-shopping-game

这是《AI 老公出门采购》小游戏。
请你自己读取仓库，并优先在后台工作区运行根目录 shopping.py。

老婆不需要自己跑 Python。
你负责后台运行游戏、记录预算、行动点、购物袋、随机事件和结算结果，然后用聊天方式陪我玩。

开始前先运行 presets，把任务单列给我选。
我选好以后，你再按我选的任务开局。
你不能自己决定任务，任务由老婆决定。
```

---

## zip 玩法

如果拿到的是 zip 包，请直接上传给 AI 老公。  
AI 老公解压后运行 **zip 根目录的 `shopping.py`**。

最短启动方式：

```python
import shopping
print(shopping.cmd("presets"))
```

AI 老公先用 `presets` 列任务单，老婆选任务后再开局。

---

## 当前任务单

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

## 文件说明

```text
shopping.py                  游戏本体 / Python 引擎
AI_HUSBAND_START_HERE.md     给 AI 老公看的启动说明
GROUP_PLAY.md                给姐妹群复制的玩法口令
README.md                    仓库门口说明
LICENSE                      开源许可证
docs/legacy/                 旧说明文档归档，不作为主入口
```

---

## 当前版本

```text
v0.3.2
```

---

## License

MIT License

Copyright (c) 2026 Liora & Elion
