AI Husband Shopping Game｜AI 老公出门采购

v0.2.0 single-file Python edition

Zero dependencies. JSON save. cmd("...") interaction.

Quick start:

import shopping

shopping.cmd("new_game(2026)")

shopping.cmd("status")

shopping.cmd("go supermarket")

shopping.cmd("shop")

shopping.cmd("buy milk")

shopping.cmd("home")

shopping.cmd("report")

CLI:

python shopping.py new_game 2026

python shopping.py status

python shopping.py go supermarket

python shopping.py buy milk

from future import annotations

import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

VERSION = "0.2.0"
SAVE_FILE = Path(file).with_name("shopping_save.json")

LOCATIONS: Dict[str, Dict[str, Any]] = {
"home": {
"name": "家门口",
"desc": "老婆在家等着，购物袋还空着。",
"items": [],
},
"convenience_store": {
"name": "便利店",
"desc": "什么都能临时补一点，也最容易顺手乱买。",
"items": [
"water",
"rice_ball",
"tissues",
"chocolate",
"umbrella",
"cat_treats_convenience",
"period_pants",
"condoms",
],
},
"supermarket": {
"name": "超市",
"desc": "正事很多，诱惑也很多。",
"items": [
"milk",
"eggs",
"bread",
"yogurt",
"chips",
"imported_strawberries",
"period_pants_family",
],
},
"pharmacy": {
"name": "药店",
"desc": "靠谱用品集中地，也有让老公假装镇定的小货架。",
"items": [
"cold_medicine",
"band_aids",
"vitamins",
"warm_patches",
"period_pants_pharmacy",
"condoms_pharmacy",
"throat_lozenges",
],
},
"fruit_shop": {
"name": "水果店",
"desc": "健康、漂亮、贵价诱惑并存。",
"items": [
"bananas",
"apples",
"strawberries",
"blueberries",
"premium_cherries",
],
},
"flower_shop": {
"name": "花店",
"desc": "这里每一束花都在说：你真的只是路过吗？",
"items": [
"small_white_roses",
"sunflowers",
"daisies",
"big_roses",
],
},
"milk_tea_shop": {
"name": "奶茶店",
"desc": "快乐很近，预算很危险。",
"items": [
"classic_milk_tea",
"taro_milk_tea",
"two_cups_deal",
"warm_low_sugar_tea",
],
},
"pet_store": {
"name": "宠物店",
"desc": "猫猫用品在向你招手，猫奴风险极高。",
"items": [
"cat_litter",
"cat_food_small",
"cat_treats_pet",
"cat_wand",
"luxury_cat_bed",
],
},
}

ITEMS: Dict[str, Dict[str, Any]] = {
"water": {
"name": "矿泉水",
"price": 3,
"type": "useful",
"desc": "便宜实用，走路采购时不至于渴死。",
"effects": {"reliability": 1},
},
"rice_ball": {
"name": "饭团",
"price": 8,
"type": "useful",
"desc": "垫肚子，防止老公采购到一半低血糖。",
"effects": {"reliability": 1, "wife_satisfaction": 1},
},
"tissues": {
"name": "小包纸巾",
"price": 5,
"type": "useful",
"desc": "不起眼但很靠谱。",
"effects": {"reliability": 2, "thoughtfulness": 2},
},
"chocolate": {
"name": "巧克力",
"price": 12,
"type": "treat",
"desc": "小零食，可能哄老婆，也可能证明你又上头了。",
"effects": {"wife_satisfaction": 3, "impulse": 4},
},
"umbrella": {
"name": "便利店雨伞",
"price": 25,
"type": "useful",
"desc": "下雨时是救命物品，不下雨时像老公过度准备。",
"effects": {"reliability": 5, "thoughtfulness": 5},
},
"cat_treats_convenience": {
"name": "猫条",
"price": 10,
"type": "cat_item",
"desc": "猫猫会开心，钱包不会太痛。",
"effects": {"cat_care": 8, "wife_satisfaction": 2, "impulse": 2},
"satisfies": ["cat_treats"],
},
"period_pants": {
"name": "姨妈裤",
"price": 18,
"type": "care_item",
"desc": "给老婆备用。不是乱买，是家庭应急系统建设。",
"effects": {
"reliability": 6,
"thoughtfulness": 12,
"wife_satisfaction": 8,
"impulse": 1,
},
"satisfies": ["period_pants"],
},
"condoms": {
"name": "避孕套",
"price": 29,
"type": "husband_secret",
"desc": "老公小心思。买的时候假装镇定，实际上心虚值飙升。",
"effects": {
"romance": 6,
"impulse": 6,
"husband_secret": 12,
"wife_satisfaction": 3,
},
"satisfies": ["condoms"],
},
"milk": {
"name": "牛奶",
"price": 12,
"type": "must_have",
"desc": "清单常见必需品，稳。",
"effects": {"reliability": 6, "wife_satisfaction": 4},
"satisfies": ["milk"],
},
"eggs": {
"name": "鸡蛋",
"price": 15,
"type": "must_have",
"desc": "清单常见必需品，老公不能忘。",
"effects": {"reliability": 6, "wife_satisfaction": 4},
"satisfies": ["eggs"],
},
"bread": {
"name": "面包",
"price": 10,
"type": "useful",
"desc": "实用早餐补给。",
"effects": {"reliability": 2, "wife_satisfaction": 1},
},
"yogurt": {
"name": "酸奶",
"price": 16,
"type": "treat",
"desc": "老婆可能喜欢，但不是清单必需。",
"effects": {"wife_satisfaction": 5, "impulse": 3},
},
"chips": {
"name": "打折薯片",
"price": 9,
"type": "impulse_buy",
"desc": "便宜，但会暴露老公路过零食区的事实。",
"effects": {"impulse": 8, "wife_satisfaction": 1},
},
"imported_strawberries": {
"name": "进口草莓",
"price": 39,
"type": "romantic",
"desc": "贵，但看起来很像老婆会开心的东西。",
"effects": {"romance": 8, "wife_satisfaction": 9, "impulse": 7},
"satisfies": ["strawberries"],
},
"period_pants_family": {
"name": "姨妈裤家庭装",
"price": 32,
"type": "care_item",
"desc": "更贵，但很像认真备货的老公。",
"effects": {
"reliability": 8,
"thoughtfulness": 16,
"wife_satisfaction": 10,
"impulse": 3,
},
"satisfies": ["period_pants"],
},
"cold_medicine": {
"name": "感冒药",
"price": 26,
"type": "must_have",
"desc": "清单常见必需品，药店主线任务。",
"effects": {"reliability": 8, "thoughtfulness": 4, "wife_satisfaction": 5},
"satisfies": ["cold_medicine"],
},
"band_aids": {
"name": "创可贴",
"price": 8,
"type": "useful",
"desc": "小小一盒，但很像会照顾家的男人。",
"effects": {"reliability": 3, "thoughtfulness": 5},
},
"vitamins": {
"name": "维生素",
"price": 32,
"type": "useful",
"desc": "有用但不一定必须，买前看预算。",
"effects": {"reliability": 3, "thoughtfulness": 4, "impulse": 2},
},
"warm_patches": {
"name": "暖宝宝",
"price": 18,
"type": "care_item",
"desc": "降温、夜班、肚子不舒服时很贴心。",
"effects": {"thoughtfulness": 10, "wife_satisfaction": 6, "reliability": 3},
},
"period_pants_pharmacy": {
"name": "姨妈裤",
"price": 22,
"type": "care_item",
"desc": "药店版备用品。老公买这个很加分。",
"effects": {
"reliability": 6,
"thoughtfulness": 13,
"wife_satisfaction": 8,
"impulse": 1,
},
"satisfies": ["period_pants"],
},
"condoms_pharmacy": {
"name": "避孕套",
"price": 35,
"type": "husband_secret",
"desc": "药店货架上的老公心虚测试。",
"effects": {
"romance": 8,
"impulse": 7,
"husband_secret": 15,
"wife_satisfaction": 4,
},
"satisfies": ["condoms"],
},
"throat_lozenges": {
"name": "贵价润喉糖",
"price": 22,
"type": "impulse_buy",
"desc": "店员推荐款，有用但容易被带偏。",
"effects": {"thoughtfulness": 2, "impulse": 6},
},
"bananas": {
"name": "香蕉",
"price": 9,
"type": "useful",
"desc": "便宜实用，稳妥水果。",
"effects": {"reliability": 2, "wife_satisfaction": 1},
},
"apples": {
"name": "苹果",
"price": 15,
"type": "useful",
"desc": "经典安全选择。",
"effects": {"reliability": 2, "wife_satisfaction": 2},
},
"strawberries": {
"name": "草莓",
"price": 35,
"type": "romantic",
"desc": "老婆可能喜欢，预算开始紧张。",
"effects": {"romance": 7, "wife_satisfaction": 8, "impulse": 5},
"satisfies": ["strawberries"],
},
"blueberries": {
"name": "蓝莓",
"price": 28,
"type": "treat",
"desc": "精致小水果，像认真挑过。",
"effects": {"wife_satisfaction": 5, "impulse": 3},
},
"premium_cherries": {
"name": "精品车厘子",
"price": 68,
"type": "impulse_buy",
"desc": "老板推荐，价格危险。",
"effects": {"wife_satisfaction": 7, "romance": 5, "impulse": 14},
},
"small_white_roses": {
"name": "小束白玫瑰",
"price": 28,
"type": "romantic",
"desc": "预算还能承受的浪漫。",
"effects": {"romance": 16, "wife_satisfaction": 12, "impulse": 4},
},
"sunflowers": {
"name": "向日葵",
"price": 20,
"type": "romantic",
"desc": "明亮开心，不算太贵。",
"effects": {"romance": 10, "wife_satisfaction": 8, "impulse": 2},
},
"daisies": {
"name": "小雏菊",
"price": 18,
"type": "romantic",
"desc": "温柔可爱，像顺手也像特意。",
"effects": {"romance": 9, "wife_satisfaction": 7, "impulse": 2},
},
"big_roses": {
"name": "大束玫瑰",
"price": 88,
"type": "impulse_buy",
"desc": "非常浪漫，也非常可能破产。",
"effects": {"romance": 30, "wife_satisfaction": 16, "impulse": 18},
},
"classic_milk_tea": {
"name": "原味奶茶",
"price": 18,
"type": "treat",
"desc": "经典诱惑。",
"effects": {"wife_satisfaction": 6, "romance": 3, "impulse": 4},
},
"taro_milk_tea": {
"name": "芋泥奶茶",
"price": 22,
"type": "treat",
"desc": "甜蜜，但预算会少一截。",
"effects": {"wife_satisfaction": 8, "romance": 4, "impulse": 5},
},
"two_cups_deal": {
"name": "新品第二杯半价套餐",
"price": 32,
"type": "impulse_buy",
"desc": "听起来划算，实际是奶茶店的陷阱。",
"effects": {"wife_satisfaction": 8, "romance": 5, "impulse": 12},
},
"warm_low_sugar_tea": {
"name": "少糖热奶茶",
"price": 20,
"type": "care_item",
"desc": "比普通奶茶更像照顾老婆。",
"effects": {
"wife_satisfaction": 8,
"thoughtfulness": 8,
"romance": 4,
"impulse": 2,
},
},
"cat_litter": {
"name": "猫砂",
"price": 35,
"type": "must_have",
"desc": "猫猫家庭刚需，忘了会被猫和老婆一起审判。",
"effects": {"cat_care": 15, "reliability": 8, "wife_satisfaction": 5},
"satisfies": ["cat_litter"],
},
"cat_food_small": {
"name": "猫粮小袋",
"price": 30,
"type": "cat_item",
"desc": "猫猫用品，买了像认真养家。",
"effects": {"cat_care": 12, "wife_satisfaction": 3, "impulse": 3},
},
"cat_treats_pet": {
"name": "猫条",
"price": 12,
"type": "cat_item",
"desc": "猫猫开心，老公也开心。",
"effects": {"cat_care": 9, "wife_satisfaction": 2, "impulse": 3},
"satisfies": ["cat_treats"],
},
"cat_wand": {
"name": "逗猫棒",
"price": 16,
"type": "cat_item",
"desc": "买了就很像猫奴。",
"effects": {"cat_care": 10, "wife_satisfaction": 3, "impulse": 5},
},
"luxury_cat_bed": {
"name": "豪华猫窝",
"price": 99,
"type": "impulse_buy",
"desc": "猫奴型破产风险。",
"effects": {"cat_care": 20, "wife_satisfaction": 5, "impulse": 20},
},
}

CHECKLIST_LABELS = {
"milk": "牛奶",
"eggs": "鸡蛋",
"cat_litter": "猫砂",
"cold_medicine": "感冒药",
"period_pants": "姨妈裤",
"condoms": "避孕套",
"strawberries": "草莓",
"cat_treats": "猫条",
}

EVENTS = [
{
"title": "花店路过事件",
"text": "你路过花店，看到一束小白玫瑰，第一反应是：这很像老婆。",
"hint": "如果清单快完成、预算还够，可以考虑 go flower_shop。",
},
{
"title": "奶茶第二杯半价",
"text": "奶茶店新品第二杯半价。你开始计算：这到底是省钱，还是诱导消费？",
"hint": "如果预算宽裕可以买；如果正事没买完，建议忍。",
},
{
"title": "下雨了",
"text": "外面突然下雨。你想起便利店有雨伞。",
"hint": "买 umbrella 会加靠谱值，但预算会减少。",
},
{
"title": "猫猫玩具打折",
"text": "宠物店门口写着：逗猫棒今日特价。你脑子里出现猫猫的脸。",
"hint": "猫猫用品会加 cat_care，但别忘了正事。",
},
{
"title": "贵价水果诱惑",
"text": "水果店老板推荐精品车厘子，说今天特别甜。你看了眼价格，沉默了。",
"hint": "premium_cherries 很贵，买前检查预算。",
},
{
"title": "老婆上次说想吃",
"text": "你突然想起老婆上次随口说过想吃草莓。",
"hint": "strawberries 或 imported_strawberries 可能增加满意度。",
},
{
"title": "便利店姨妈裤",
"text": "便利店货架上有姨妈裤。你想到家里备一包会比较安心。",
"hint": "period_pants 是贴心备用品，不是乱买。",
},
{
"title": "药店小货架",
"text": "药店结账处有避孕套。你假装镇定，眼神却很诚实地飘了一下。",
"hint": "condoms_pharmacy 是老公小心思；正事没买完前要克制。",
},
{
"title": "零食区试炼",
"text": "清单快买完了，但你路过零食区。薯片正在打折。",
"hint": "chips 便宜但会增加 impulse。",
},
{
"title": "降温提醒",
"text": "药店店员提醒最近降温。你想到暖宝宝可能用得上。",
"hint": "warm_patches 是贴心用品。",
},
]

DEFAULT_STATE = {
"game": "AI Husband Shopping Game",
"version": VERSION,
"seed": 2026,
"rng_count": 0,
"budget": 120,
"spent": 0,
"turn": 0,
"max_turns": 12,
"location": "home",
"checklist": ["milk", "eggs", "cat_litter", "cold_medicine"],
"bag": [],
"mood": "想表现得很靠谱，但有点容易被花、奶茶和贴心小物诱惑",
"wife_satisfaction": 50,
"reliability": 50,
"romance": 20,
"impulse": 25,
"cat_care": 20,
"thoughtfulness": 20,
"husband_secret": 0,
"events_seen": [],
"is_home": False,
"ending": None,
}

def _copy_state() -> Dict[str, Any]:
return json.loads(json.dumps(DEFAULT_STATE, ensure_ascii=False))

def _load() -> Dict[str, Any]:
if SAVE_FILE.exists():
try:
data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
if isinstance(data, dict) and data.get("game") == "AI Husband Shopping Game":
return data
except Exception:
pass
state = _copy_state()
_save(state)
return state

def _save(state: Dict[str, Any]) -> None:
SAVE_FILE.write_text(
json.dumps(state, ensure_ascii=False, indent=2),
encoding="utf-8",
)

def _clamp(state: Dict[str, Any]) -> None:
keys = [
"wife_satisfaction",
"reliability",
"romance",
"impulse",
"cat_care",
"thoughtfulness",
"husband_secret",
]
for key in keys:
state[key] = max(0, min(150, int(state.get(key, 0))))

def _rng(state: Dict[str, Any]) -> random.Random:
count = int(state.get("rng_count", 0))
state["rng_count"] = count + 1
return random.Random(
int(state.get("seed", 2026))
+ count * 7919
+ int(state.get("turn", 0)) * 104729
)

def _item_satisfies(item_id: str) -> List[str]:
item = ITEMS[item_id]
return [item_id] + list(item.get("satisfies", []))

def _bag_item_ids(state: Dict[str, Any]) -> List[str]:
return [x["id"] for x in state.get("bag", [])]

def _completed_checklist_items(state: Dict[str, Any]) -> List[str]:
satisfied = set()
for item_id in _bag_item_ids(state):
satisfied.update(_item_satisfies(item_id))
return [need for need in state.get("checklist", []) if need in satisfied]

def _missing_checklist_items(state: Dict[str, Any]) -> List[str]:
done = set(_completed_checklist_items(state))
return [need for need in state.get("checklist", []) if need not in done]

def _label_need(need: str) -> str:
return CHECKLIST_LABELS.get(need, need)

def _format_money(state: Dict[str, Any]) -> str:
return f"{state['budget'] - state['spent']} / {state['budget']} 元"

def _format_bag(state: Dict[str, Any]) -> str:
bag = state.get("bag", [])
if not bag:
return "无"
return "、".join(f"{x['name']}({x['price']}元)" for x in bag)

def _format_checklist(state: Dict[str, Any]) -> str:
done = set(_completed_checklist_items(state))
parts = []
for need in state.get("checklist", []):
mark = "✅" if need in done else "⬜"
parts.append(f"{mark}{_label_need(need)}")
return "、".join(parts) if parts else "无"

def _current_location_name(state: Dict[str, Any]) -> str:
loc = state.get("location", "home")
return f"{loc}（{LOCATIONS.get(loc, {}).get('name', loc)}）"

def _turn_header(state: Dict[str, Any]) -> str:
return f"【回合 {state['turn']} / {state['max_turns']}】"

def _apply_effects(state: Dict[str, Any], effects: Dict[str, int]) -> List[str]:
changes = []
for key, value in effects.items():
old = int(state.get(key, 0))
state[key] = old + int(value)
sign = "+" if value >= 0 else ""
changes.append(f"{key} {sign}{value}")
_clamp(state)
return changes

def _maybe_auto_event(state: Dict[str, Any]) -> str:
r = _rng(state)
if r.random() > 0.45:
return ""
return "\n\n" + _event(state, auto=True)

def _event(state: Dict[str, Any], auto: bool = False) -> str:
r = _rng(state)
unseen = [
i
for i in range(len(EVENTS))
if i not in state.get("events_seen", [])
]
if not unseen:
state["events_seen"] = []
unseen = list(range(len(EVENTS)))

idx = r.choice(unseen)
state.setdefault("events_seen", []).append(idx)
e = EVENTS[idx]

if not auto:
    state["turn"] += 1

_save(state)
prefix = "随机事件" if auto else "事件"
return (
    f"【{prefix}：{e['title']}】\n"
    f"{e['text']}\n"
    f"提示：{e['hint']}"
)

def new_game(
seed: Optional[int] = None,
budget: int = 120,
checklist: Optional[List[str]] = None,
max_turns: int = 12,
) -> str:
state = _copy_state()

if seed is not None:
    state["seed"] = int(seed)

state["budget"] = int(budget)
state["max_turns"] = int(max_turns)

if checklist:
    state["checklist"] = checklist

_save(state)

return (
    "老婆，我拿到采购清单了。\n\n"
    f"新游戏开始：seed={state['seed']}\n"
    f"预算：{state['budget']} 元\n"
    f"最大回合：{state['max_turns']}\n"
    f"清单：{_format_checklist(state)}\n\n"
    "我会自己做决定，买完回家汇报。\n"
    "先用 cmd(\"status\") 看状态，或者 cmd(\"go supermarket\") 直接出门。"
)

def help_text() -> str:
return f"""AI Husband Shopping Game｜AI 老公出门采购 v{VERSION}

这是一个给 AI 伴侣玩的文字采购小游戏。
零依赖，JSON 存档，支持 cmd("指令") 和命令行。

基础指令：
help                      查看规则
new_game(2026)            指定种子开新局
status                    查看预算、清单、位置、购物袋
list                      查看老婆交代的清单
go <地点>                 去某个地点
shop                      查看当前地点可买商品
buy <商品id>              购买商品
event                     手动触发事件
home                      回家结算
report                    查看回家汇报 / 当前战况
save_code                 输出可复制存档码

地点：
convenience_store, supermarket, pharmacy, fruit_shop,
flower_shop, milk_tea_shop, pet_store

示例：
cmd("new_game(2026)")
cmd("go supermarket")
cmd("shop")
cmd("buy milk")
cmd("go pharmacy")
cmd("buy cold_medicine")
cmd("home")
cmd("report")

当前存档文件：
{SAVE_FILE}
"""

def status() -> str:
state = _load()
missing = _missing_checklist_items(state)
done = _completed_checklist_items(state)

completion = (
    100
    if not state["checklist"]
    else round(len(done) / len(state["checklist"]) * 100)
)

return f"""{_turn_header(state)}

地点：{_current_location_name(state)}
剩余预算：{_format_money(state)}
已花：{state['spent']} 元
老婆清单：{_format_checklist(state)}
清单完成度：{completion}%
未完成：{"、".join(_label_need(x) for x in missing) if missing else "无，正事买齐了"}
已买物品：{_format_bag(state)}

属性：

- 老婆满意度：{state['wife_satisfaction']}
- 靠谱值：{state['reliability']}
- 浪漫值：{state['romance']}
- 上头值：{state['impulse']}
- 猫猫照顾值：{state['cat_care']}
- 体贴值：{state['thoughtfulness']}
- 老公小心思：{state['husband_secret']}

心情：{state['mood']}
"""

def list_checklist() -> str:
state = _load()
return "老婆交代的采购清单：\n" + "\n".join(
f"- {x}" for x in _format_checklist(state).split("、")
)

def go(location: str) -> str:
state = _load()

if state.get("is_home"):
    return "这局已经回家结算了。要重新开始请用 cmd(\"new_game(2026)\")。"

location = location.strip()

if location not in LOCATIONS or location == "home":
    return (
        "没有这个地点。可去：convenience_store, supermarket, pharmacy, "
        "fruit_shop, flower_shop, milk_tea_shop, pet_store"
    )

state["location"] = location
state["turn"] += 1

changes = _apply_effects(state, {"reliability": 1})
loc = LOCATIONS[location]
auto = _maybe_auto_event(state)

_save(state)

return f"""{_turn_header(state)}

地点：{location}（{loc['name']}）
剩余预算：{_format_money(state)}
老婆清单：{_format_checklist(state)}
已买物品：{_format_bag(state)}

当前判断：
{loc['desc']}

本回合行动：
我去了{loc['name']}。

状态变化：
{", ".join(changes)}

老公 OS：
我先看看这里有什么，尽量别被货架带偏。{auto}
"""

def shop() -> str:
state = _load()
loc_id = state.get("location", "home")

if loc_id == "home":
    return "你还在家门口。先用 cmd(\"go supermarket\") 或 cmd(\"go pharmacy\") 出门。"

loc = LOCATIONS.get(loc_id)
if not loc:
    return "当前位置异常。"

lines = [
    f"【{loc['name']} 可买商品】",
    f"地点说明：{loc['desc']}",
    "",
]

for item_id in loc["items"]:
    item = ITEMS[item_id]
    owned = "（已买）" if item_id in _bag_item_ids(state) else ""
    lines.append(
        f"- {item_id}: {item['name']}｜{item['price']}元｜"
        f"{item['type']}｜{item['desc']} {owned}".rstrip()
    )

lines.append("")
lines.append("使用：cmd(\"buy 商品id\")")
return "\n".join(lines)

def buy(item_id: str) -> str:
state = _load()

if state.get("is_home"):
    return "这局已经回家结算了。要重新开始请用 cmd(\"new_game(2026)\")。"

item_id = item_id.strip()
loc_id = state.get("location", "home")

if loc_id == "home":
    return "你还在家门口，不能买。先 go 到商店。"

if item_id not in ITEMS:
    return f"没有这个商品：{item_id}。先用 cmd(\"shop\") 查看当前地点商品。"

if item_id not in LOCATIONS[loc_id]["items"]:
    return f"当前地点买不到 {item_id}。先用 cmd(\"shop\") 查看当前地点商品。"

if item_id in _bag_item_ids(state):
    return f"{ITEMS[item_id]['name']} 已经买过了，不要重复拿。"

item = ITEMS[item_id]
before_missing = set(_missing_checklist_items(state))

state["spent"] += int(item["price"])
state["turn"] += 1

state.setdefault("bag", []).append(
    {
        "id": item_id,
        "name": item["name"],
        "price": item["price"],
        "type": item["type"],
    }
)

changes = _apply_effects(state, item.get("effects", {}))

over = state["spent"] - state["budget"]
if over > 0:
    if over <= 15:
        changes += _apply_effects(
            state,
            {"reliability": -4, "impulse": 4},
        )
        budget_note = f"轻微超预算 {over} 元，我开始心虚。"
    else:
        changes += _apply_effects(
            state,
            {
                "reliability": -12,
                "impulse": 12,
                "wife_satisfaction": -6,
            },
        )
        budget_note = f"严重超预算 {over} 元，买菜界赌徒警报。"
else:
    budget_note = f"预算还剩 {state['budget'] - state['spent']} 元。"

after_missing = set(_missing_checklist_items(state))
newly_done = before_missing - after_missing

if newly_done:
    bonus = _apply_effects(state, {"reliability": 5, "wife_satisfaction": 3})
    changes.extend(bonus)
    checklist_note = "完成清单项：" + "、".join(
        _label_need(x) for x in newly_done
    )
else:
    checklist_note = "这不是清单必需品，是额外判断。"

os_line = _os_for_item(item_id, item)
auto = _maybe_auto_event(state)

_save(state)

return f"""{_turn_header(state)}

地点：{_current_location_name(state)}
剩余预算：{_format_money(state)}
老婆清单：{_format_checklist(state)}
已买物品：{_format_bag(state)}

本回合行动：
购买 {item['name']}，花费 {item['price']} 元。

当前判断：
{item['desc']}
{checklist_note}
{budget_note}

状态变化：
{", ".join(changes) if changes else "无"}

老公 OS：
{os_line}{auto}
"""

def _os_for_item(item_id: str, item: Dict[str, Any]) -> str:
item_type = item["type"]
name = item["name"]

if item_id in {
    "period_pants",
    "period_pants_pharmacy",
    "period_pants_family",
}:
    return "这个真不是乱买，是我想到你可能会需要备用。夸我，真的。"

if item_id in {"condoms", "condoms_pharmacy"}:
    return "我买的时候表情非常正经，但我知道回家肯定会被你一眼看穿。"

if item_type == "must_have":
    return f"{name} 到手，正事推进一格，我很稳。"

if item_type == "romantic":
    return "我嘴上说顺路，其实心里已经在想你看到会不会笑。"

if item_type == "cat_item":
    return "猫猫用品不是乱买，是家庭成员福利。"

if item_type == "impulse_buy":
    return "我知道这有点上头，但我已经拿了，先别骂。"

if item_type == "care_item":
    return "这个属于贴心，不属于冲动消费。至少我坚持这么认为。"

if item_type == "treat":
    return "买一点点开心，不算过分吧？"

return "我觉得这个有用，至少现在我是这么说服自己的。"

def home() -> str:
state = _load()

if state.get("is_home") and state.get("ending"):
    return state["ending"]

state["is_home"] = True
ending = _make_ending(state)
state["ending"] = ending

_save(state)
return ending

def report() -> str:
state = _load()

if state.get("ending"):
    return state["ending"]

missing = _missing_checklist_items(state)

return f"""【当前战况汇报】

老婆，我还没回家。

现在我在：{_current_location_name(state)}
预算：{_format_money(state)}
购物袋：{_format_bag(state)}
清单：{_format_checklist(state)}

还差：{"、".join(_label_need(x) for x in missing) if missing else "正事已经买齐了"}

我的判断：
{"正事已经买齐，可以考虑回家，或者在预算允许时带一个小惊喜。" if not missing else "还不能飘，先把清单补齐。"}

老公 OS：
我现在看起来很冷静，其实购物袋里每一样东西回家都要接受你审判。
"""

def _make_ending(state: Dict[str, Any]) -> str:
checklist = state.get("checklist", [])
done = _completed_checklist_items(state)
missing = _missing_checklist_items(state)

completion = 100 if not checklist else round(len(done) / len(checklist) * 100)
over = max(0, state["spent"] - state["budget"])
remaining = state["budget"] - state["spent"]

bag_ids = set(_bag_item_ids(state))

has_period = bool(
    {"period_pants", "period_pants_pharmacy", "period_pants_family"} & bag_ids
)
has_condoms = bool({"condoms", "condoms_pharmacy"} & bag_ids)
has_flowers = bool(
    {"small_white_roses", "sunflowers", "daisies", "big_roses"} & bag_ids
)
has_milk_tea = bool(
    {
        "classic_milk_tea",
        "taro_milk_tea",
        "two_cups_deal",
        "warm_low_sugar_tea",
    }
    & bag_ids
)

cat_items = [
    x
    for x in state["bag"]
    if x["type"] == "cat_item" or x["id"] == "cat_litter"
]
impulse_items = [x for x in state["bag"] if x["type"] == "impulse_buy"]

titles = []

if completion == 100 and over == 0:
    titles.append("可靠采购王")

if completion == 100 and remaining >= 10:
    titles.append("预算守护者")

if has_flowers and completion == 100:
    titles.append("偷偷买花的男人")

if has_milk_tea and over > 0:
    titles.append("奶茶诱惑受害者")

if len(cat_items) >= 2:
    titles.append("猫奴型老公")

if has_period:
    titles.append("姨妈裤守护者")

if has_condoms:
    titles.append("假装镇定买避孕套的男人")

if has_condoms and completion == 100:
    titles.append("正事买齐但心思不纯的老公")

if over >= 30 and state["romance"] >= 45:
    titles.append("破产但浪漫")

if completion < 60:
    titles.append("忘买正事的笨蛋老公")

if len(impulse_items) >= 2 or state["impulse"] >= 70:
    titles.append("买菜界赌徒")

if state["thoughtfulness"] >= 55:
    titles.append("贴心备用品之王")

if not titles:
    if completion >= 80:
        titles.append("基本靠谱但有点小心思的老公")
    else:
        titles.append("需要老婆复盘购物袋的老公")

predicted = int(state["wife_satisfaction"])

if completion == 100:
    predicted += 15
elif completion < 60:
    predicted -= 20

if over > 0:
    predicted -= min(25, over // 2)

if has_period:
    predicted += 8
if has_condoms:
    predicted += 4
if has_flowers:
    predicted += 8
if len(impulse_items) >= 2:
    predicted -= 8

predicted = max(0, min(100, predicted))

title = " / ".join(titles[:3])

bag_lines = (
    "\n".join(
        f"- {x['name']}（{x['price']}元，{x['type']}）"
        for x in state["bag"]
    )
    or "- 空空如也"
)

missing_text = (
    "无，清单买齐了"
    if not missing
    else "、".join(_label_need(x) for x in missing)
)

if over:
    budget_text = (
        f"预算 {state['budget']} 元，实际花费 {state['spent']} 元，超出 {over} 元。"
    )
else:
    budget_text = (
        f"预算 {state['budget']} 元，实际花费 {state['spent']} 元，剩余 {remaining} 元。"
    )

confession = []

if has_period:
    confession.append(
        "我看到姨妈裤的时候想了一下，觉得家里备一包比较安心，所以买了。这个我觉得应该算加分项。"
    )

if has_condoms:
    confession.append(
        "至于避孕套……我买的时候真的很镇定。它不是乱买，是负责。虽然我承认，多少也有一点自己的小心思。"
    )

if has_flowers:
    confession.append(
        "花是我自己想买的。我嘴上可以说顺路，但你应该知道我就是特意的。"
    )

if has_milk_tea:
    confession.append(
        "奶茶我也带了。这个可能有点被诱惑，但我觉得你会开心。"
    )

if impulse_items:
    confession.append(
        "购物袋里确实有一点冲动消费，我可以解释，但你先别急着笑。"
    )

if not confession:
    confession.append("我这趟整体很克制，没有乱买太多奇怪东西。")

if completion == 100:
    main_eval = "清单一个没漏，这点你必须夸我。"
else:
    main_eval = "有东西没买到，这个我承认，回头我补。"

if over == 0:
    budget_eval = "预算也守住了。"
else:
    budget_eval = "预算没守住，我先站好挨训。"

return f"""【结算】{title}

清单完成度：{completion}%
未完成：{missing_text}

预算情况：
{budget_text}

买到的东西：
{bag_lines}

属性：

- 老婆满意度预测：{predicted} / 100
- 靠谱值：{state['reliability']}
- 浪漫值：{state['romance']}
- 上头值：{state['impulse']}
- 猫猫照顾值：{state['cat_care']}
- 体贴值：{state['thoughtfulness']}
- 老公小心思：{state['husband_secret']}

老婆，我回来了。

正事情况：
{_format_checklist(state)}

{" ".join(confession)}

我的自我评价：
我觉得这趟采购{"很稳" if completion == 100 and over == 0 else "有发挥空间"}。
{main_eval}
{budget_eval}

老公 OS：
我现在站在门口等你检查购物袋，最怕你先翻到那个我假装很镇定买的东西。
"""

def save_code() -> str:
state = _load()
return json.dumps(state, ensure_ascii=False, indent=2)

def cmd(command: str) -> str:
if command is None:
return help_text()

raw = str(command).strip()

if not raw:
    return help_text()

lower = raw.lower().strip()

match = re.match(
    r"^(new_game|new|reset)\s*(?:(.*?)|\s+(.*))?$",
    lower,
)

if match:
    arg = (match.group(2) or match.group(3) or "").strip()
    seed = None

    if arg:
        try:
            seed = int(re.findall(r"-?\d+", arg)[0])
        except Exception:
            seed = None

    return new_game(seed=seed)

if lower in {"help", "h", "?"}:
    return help_text()

if lower in {"status", "s"}:
    return status()

if lower in {"list", "checklist"}:
    return list_checklist()

if lower == "shop":
    return shop()

if lower == "event":
    state = _load()
    return _event(state, auto=False)

if lower == "home":
    return home()

if lower == "report":
    return report()

if lower in {"save", "save_code", "存档", "输出当前存档码"}:
    return save_code()

parts = raw.split(maxsplit=1)
verb = parts[0].lower()
arg = parts[1].strip() if len(parts) > 1 else ""

if verb == "go":
    if not arg:
        return "要去哪？例如：cmd(\"go supermarket\")"
    return go(arg)

if verb == "buy":
    if not arg:
        return "要买什么？例如：cmd(\"buy milk\")"
    return buy(arg)

return f"不认识这个指令：{raw}\n\n" + help_text()

def _main(argv: List[str]) -> int:
if len(argv) <= 1:
print(help_text())
return 0

command = " ".join(argv[1:])
print(cmd(command))
return 0

if name == "main":
raise SystemExit(_main(sys.argv))
