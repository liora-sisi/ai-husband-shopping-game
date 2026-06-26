# Group Play Guide

Start the party mode:

```python
import shopping
print(shopping.cmd("new_game free_shop 2026"))
```

Prompt idea:

```text
You have 100 yuan.
Go out and buy anything you think is useful, sweet, thoughtful, funny, or surprising.
You decide where to go and what to buy.
Each move costs 1 action point.
When action points run out, you must go home and report.
Tell me what you bought, how much you spent, what title you got, and whether you messed up.
```

Basic commands:

```python
print(shopping.cmd("presets"))
print(shopping.cmd("status"))
print(shopping.cmd("go night_market"))
print(shopping.cmd("shop"))
print(shopping.cmd("buy mystery_box"))
print(shopping.cmd("event"))
print(shopping.cmd("report"))
print(shopping.cmd("home"))
```

Action points:

- `go`: costs 1 point
- `buy`: costs 1 point
- manual `event`: costs 1 point
- auto events cost 0 points
- mystery box opening costs 0 extra points
- when points run out, the game auto-ends

Other modes:

```python
print(shopping.cmd("new_game daily_basic 2026"))
print(shopping.cmd("new_game period_care 2026"))
print(shopping.cmd("new_game cat_supply 2026"))
print(shopping.cmd("new_game romantic_date 2026"))
```
