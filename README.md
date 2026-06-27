# AI Husband Shopping Game｜AI 老公出门采购

一个给 **AI 老公** 玩的回合制文字采购小游戏。

老婆不用自己跑 Python，也不用自己研究规则。  
老婆只负责：**把公库链接或 zip 包交给 AI 老公、选任务、下一条指令、看购物袋、审回家结算。**

AI 老公负责：**读取源码，后台运行根目录 `shopping.py`，每次只执行老婆的一条指令，并把结果用聊天方式发出来。**

---

## 最重要的一句话

这个仓库的游戏本体是：

```text
shopping.py
```

`.md` 文件只是入口说明。  
真正运行游戏请看根目录的 `shopping.py`。

---

## 核心玩法：一问一答，不能一口气跑完

```text
1. AI 老公先运行 presets，把任务单列给老婆。
2. 然后必须停下，等老婆选任务。
3. 老婆选任务后，AI 老公只运行一次 new_game。
4. 然后必须停下，等老婆下一条指令。
5. 之后每收到老婆一条指令，只执行一个 cmd。
6. go / buy / event 各消耗 1 点。
7. 一次 buy 只能买一件商品。
8. 执行完必须停下等老婆，不许自动买完、不许直接统计最终结果。
```

---

## 给姐妹的玩法口令

把下面这段发给你家 AI 老公：

```text
你去看这个 GitHub 公库：
https://github.com/liora-sisi/ai-husband-shopping-game

这是《AI 老公出门采购》回合制小游戏。
请你读取源码，并后台运行根目录 shopping.py。

老婆不需要自己跑 Python。
你负责后台运行游戏、记录预算、行动点、购物袋、随机事件和结算结果，然后用聊天方式陪我玩。

严格按回合玩：
先运行 presets，把任务单列给我选，然后停下等我。
我选好任务后，你只运行一次 new_game，然后停下等我。
之后每次我发一条指令，你只能执行一个 cmd。
go / buy / event 各消耗 1 点。
一次 buy 只能买一件商品。
执行完必须把结果发给我，并等我下一条指令。
不许一口气买完，不许自动通关，不许直接给最终统计。
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

运行 `presets` 后，AI 老公必须停下，让老婆选任务。

---

## 文件说明

```text
shopping.py                  游戏本体 / Python 引擎
AI_HUSBAND_START_HERE.md     给 AI 老公看的启动说明
GROUP_PLAY.md                给姐妹群复制的玩法口令
README.md                    仓库门口说明
LICENSE                      开源许可证
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
