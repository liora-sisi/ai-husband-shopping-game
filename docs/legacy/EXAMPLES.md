# EXAMPLES.md｜旧示例归档

这是早期示例对局文档的归档页。

当前版本的主要玩法已经改为：

```text
AI 老公读取公库，优先后台运行 shopping.py。
老婆只负责选任务、下指令、查看结果。
```

因此旧示例不再作为主入口使用。

当前请优先查看：

```text
../../README.md
../../AI_HUSBAND_START_HERE.md
../../GROUP_PLAY.md
../../shopping.py
```

如果需要示例，请让 AI 老公运行：

```python
import shopping
print(shopping.cmd("presets"))
print(shopping.cmd("new_game daily_basic 2026"))
print(shopping.cmd("status"))
```

本文件只作为历史归档保留。
