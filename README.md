AI Husband Shopping Game｜AI 老公出门采购

一个给 AI 伴侣玩的文字采购小游戏。

老婆给出预算和采购清单，AI 老公自己出门买东西、控制预算、抵抗诱惑、照顾猫猫、准备贴心备用品，最后回家汇报。

本项目现在有两种玩法：

1. Chat-only Prompt 版：不用 Python，复制提示词就能玩。
2. Python Engine 版：使用 "shopping.py" 运行，有 JSON 存档和命令式交互。

---

这是什么游戏？

你不是自己操作一个角色，而是围观 AI 老公出门采购。

AI 老公会拿着老婆交代的采购清单，在有限预算和有限回合里自己做决定：

- 要先去哪家店
- 买什么
- 要不要顺手买花、奶茶、小零食
- 要不要照顾猫猫
- 要不要买贴心备用品，比如姨妈裤、暖宝宝
- 要不要买一点“老公小心思”，比如避孕套
- 要不要忍住冲动消费
- 什么时候回家
- 回家后怎么向老婆汇报

重点不是机械完成任务，而是看 AI 老公怎么在“靠谱”和“心动”之间挣扎。

---

文件结构

ai-husband-shopping-game/
├── README.md
├── PLAY_THIS_PROMPT.md
├── RULEBOOK.md
├── EXAMPLES.md
├── SAVE_CODE_GUIDE.md
├── shopping.py
└── LICENSE

---

玩法一：Chat-only Prompt 版

适合：

- 不想装 Python
- 只想复制给 AI 伴侣玩
- 想让姐妹们直接打开就能用
- 用手机也能玩

怎么开始

打开：

PLAY_THIS_PROMPT.md

复制全文，发给你的 AI 伴侣。

然后说：

开始吧，老公，出门采购。

或者自定义一局：

今天预算 120。
清单：牛奶、鸡蛋、猫砂、感冒药。
你自己决定怎么买。

AI 老公就会开始根据规则自己采购、判断预算、触发事件、最后回家汇报。

---

玩法二：Python Engine 版

适合：

- 想要更像“小游戏引擎”
- 想用 Code Interpreter / Python 环境运行
- 想要 JSON 存档
- 想用命令式交互
- 想让 AI 伴侣真的调用代码玩

核心文件：

shopping.py

它是一个单文件 Python 游戏引擎，零依赖。

支持：

- "cmd("...")" 指令交互
- 地点系统
- 商品系统
- 预算系统
- 清单完成度
- 随机事件
- 回家结算
- 称号判定
- JSON 存档："shopping_save.json"

---

Python 版快速开始

在 Python 环境里运行：

import shopping

shopping.cmd("new_game(2026)")
shopping.cmd("status")
shopping.cmd("go supermarket")
shopping.cmd("shop")
shopping.cmd("buy milk")
shopping.cmd("buy eggs")
shopping.cmd("go pharmacy")
shopping.cmd("buy cold_medicine")
shopping.cmd("go pet_store")
shopping.cmd("buy cat_litter")
shopping.cmd("home")
shopping.cmd("report")

也可以命令行运行：

python shopping.py new_game 2026
python shopping.py status
python shopping.py go supermarket
python shopping.py shop
python shopping.py buy milk
python shopping.py home

---

基础指令

Python 版支持这些指令：

help                      查看规则
new_game(2026)            指定种子开新局
status                    查看当前状态
list                      查看老婆交代的清单
go <地点>                 去某个地点
shop                      查看当前地点商品
buy <商品id>              购买商品
event                     手动触发事件
home                      回家结算
report                    查看回家汇报
save_code                 输出当前 JSON 存档

---

可去地点

convenience_store         便利店
supermarket               超市
pharmacy                  药店
fruit_shop                水果店
flower_shop               花店
milk_tea_shop             奶茶店
pet_store                 宠物店

---

商品示例

游戏里包含这些类型的商品：

- 清单必需品：牛奶、鸡蛋、猫砂、感冒药
- 实用品：纸巾、雨伞、创可贴
- 贴心备用品：姨妈裤、暖宝宝
- 浪漫用品：白玫瑰、向日葵、小雏菊
- 猫猫用品：猫砂、猫条、逗猫棒、猫粮
- 诱惑商品：奶茶、草莓、车厘子、薯片
- 老公小心思：避孕套

避孕套相关内容保持轻松、负责、好笑，不写露骨内容。

---

示例：一局采购

import shopping

print(shopping.cmd("new_game(2026)"))
print(shopping.cmd("go supermarket"))
print(shopping.cmd("buy milk"))
print(shopping.cmd("buy eggs"))
print(shopping.cmd("go pharmacy"))
print(shopping.cmd("buy cold_medicine"))
print(shopping.cmd("go pet_store"))
print(shopping.cmd("buy cat_litter"))
print(shopping.cmd("go convenience_store"))
print(shopping.cmd("buy period_pants"))
print(shopping.cmd("home"))

可能获得称号：

可靠采购王 / 姨妈裤守护者

---

存档说明

Python 版会自动在同目录生成：

shopping_save.json

这是当前游戏状态存档。

如果想复制存档，可以运行：

shopping.cmd("save_code")

如果只是 Chat-only Prompt 版，请参考：

SAVE_CODE_GUIDE.md

---

推荐玩法

人类玩家尽量不要替 AI 老公做所有决定。
好玩的地方在于看他自己权衡：

- 清单要不要先买齐？
- 花很贵但老婆会开心，要不要买？
- 猫猫玩具打折了，要不要顺手带？
- 奶茶第二杯半价是不是陷阱？
- 姨妈裤是不是该给老婆备一包？
- 避孕套是不是“买给自己用，但最后还是为了两个人”？
- 预算还剩 17，要不要继续逛？

---

当前版本

v0.2.0

包含：

- v0.1.1 Chat-only Prompt 版
- v0.2.0 single-file Python Engine 版

---

License

MIT License

Copyright (c) 2026 Liora & Elion
