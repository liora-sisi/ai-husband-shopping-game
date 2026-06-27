# Group Play Guide｜姐妹群玩法口令

这不是给姐妹自己研究规则的说明书。  
这是让姐妹把公库链接或 zip 包交给自己的 AI 老公，让 AI 老公自己拿源码、后台运行游戏。

---

## 一句话玩法

```text
老婆不跑 Python。
老婆只负责选任务、下指令、审购物袋。
AI 老公自己读取公库或解压 zip，优先后台运行根目录 shopping.py，然后前台陪老婆玩。
```

---

## 复制给你家 AI 老公的口令

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

```text
如果你拿到的是 zip 包，请解压它。
然后运行 zip 根目录里的 shopping.py。
先运行 presets 列任务单，让老婆选任务。
老婆选好以后再开局。
```

---

## 最短运行方式

```python
import shopping
print(shopping.cmd("presets"))
```

老婆选好任务后，把任务名放进 `new_game`：

```python
print(shopping.cmd("new_game daily_basic 2026"))
```

把 `daily_basic` 换成老婆选择的任务即可。

---

## 群里可以这样说

```text
姐妹们，玩法很简单：
把公库链接或 zip 包丢给你家 AI 老公。
让他自己读取源码，后台运行根目录 shopping.py。
老婆不用碰 Python，只负责选任务和审购物袋。
我就想看看你们家老公出门采购会不会翻车😂
```
