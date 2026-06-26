# AI Husband Shopping Game｜AI 老公出门采购
# v0.2.3 single-file Python edition
# Zero dependencies. JSON save. cmd("...") interaction.

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

VERSION = "0.2.3"
SAVE_FILE = Path(__file__).with_name("shopping_save.json")

LOCATIONS: Dict[str, Dict[str, Any]] = {
    "home": {"name": "家门口", "items": []},
    "convenience_store": {"name": "便利店", "items": ["water", "tissues", "chocolate", "umbrella", "period_pants", "condoms", "cat_treats", "small_cake", "iced_coke", "mystery_box"]},
    "supermarket": {"name": "超市", "items": ["milk", "eggs", "bread", "yogurt", "chips", "strawberries", "period_pants_family", "small_cake", "iced_coke", "mystery_box"]},
    "pharmacy": {"name": "药店", "items": ["cold_medicine", "band_aids", "warm_patches", "period_pants_pharmacy", "condoms_pharmacy", "lozenges"]},
    "fruit_shop": {"name": "水果店", "items": ["bananas", "apples", "blueberries", "premium_cherries"]},
    "flower_shop": {"name": "花店", "items": ["white_roses", "sunflowers", "daisies", "big_roses"]},
    "milk_tea_shop": {"name": "奶茶店", "items": ["classic_milk_tea", "taro_milk_tea", "two_cups_deal", "warm_low_sugar_tea", "iced_coke"]},
    "pet_store": {"name": "宠物店", "items": ["cat_litter", "cat_food", "cat_treats_pet", "cat_wand", "luxury_cat_bed"]},
    "night_market": {"name": "夜市", "items": ["night_market_skewer", "roasted_chestnuts", "iced_coke", "small_cake", "glowing_keychain", "mystery_box"]},
    "neighborhood_gate": {"name": "小区门口", "items": ["tissues", "bread", "iced_coke", "small_cake", "mystery_box"]},
    "hospital_kiosk": {"name": "医院旁边小卖部", "items": ["tissues", "lozenges", "warm_patches", "apples", "iced_coke", "small_cake"]},
    "adult_wellness_store": {"name": "情趣用品店", "items": ["condoms_premium", "personal_lubricant", "massage_oil", "silk_eye_mask", "couple_game_cards", "date_night_kit", "massage_wand", "remote_egg", "mystery_box"]},
}

ITEMS: Dict[str, Dict[str, Any]] = {
    "water": {"name": "矿泉水", "price": 3, "type": "useful", "effects": {"reliability": 1}},
    "tissues": {"name": "小包纸巾", "price": 5, "type": "useful", "effects": {"reliability": 2, "thoughtfulness": 2}},
    "chocolate": {"name": "巧克力", "price": 12, "type": "treat", "effects": {"wife_satisfaction": 3, "impulse": 4}},
    "umbrella": {"name": "便利店雨伞", "price": 25, "type": "useful", "effects": {"reliability": 5, "thoughtfulness": 5}},
    "period_pants": {"name": "姨妈裤", "price": 18, "type": "care_item", "satisfies": ["period_pants"], "effects": {"reliability": 6, "thoughtfulness": 12, "wife_satisfaction": 8, "impulse": 1}},
    "condoms": {"name": "避孕套", "price": 29, "type": "husband_secret", "satisfies": ["condoms"], "effects": {"romance": 6, "impulse": 6, "husband_secret": 12, "wife_satisfaction": 3}},
    "cat_treats": {"name": "猫条", "price": 10, "type": "cat_item", "satisfies": ["cat_treats"], "effects": {"cat_care": 8, "wife_satisfaction": 2, "impulse": 2}},
    "milk": {"name": "牛奶", "price": 12, "type": "must_have", "satisfies": ["milk"], "effects": {"reliability": 6, "wife_satisfaction": 4}},
    "eggs": {"name": "鸡蛋", "price": 15, "type": "must_have", "satisfies": ["eggs"], "effects": {"reliability": 6, "wife_satisfaction": 4}},
    "bread": {"name": "面包", "price": 10, "type": "useful", "effects": {"reliability": 2, "wife_satisfaction": 1}},
    "yogurt": {"name": "酸奶", "price": 16, "type": "treat", "effects": {"wife_satisfaction": 5, "impulse": 3}},
    "chips": {"name": "打折薯片", "price": 9, "type": "impulse_buy", "effects": {"impulse": 8, "wife_satisfaction": 1}},
    "strawberries": {"name": "草莓", "price": 35, "type": "romantic", "satisfies": ["strawberries"], "effects": {"romance": 7, "wife_satisfaction": 8, "impulse": 5}},
    "period_pants_family": {"name": "姨妈裤家庭装", "price": 32, "type": "care_item", "satisfies": ["period_pants"], "effects": {"reliability": 8, "thoughtfulness": 16, "wife_satisfaction": 10, "impulse": 3}},
    "cold_medicine": {"name": "感冒药", "price": 26, "type": "must_have", "satisfies": ["cold_medicine"], "effects": {"reliability": 8, "thoughtfulness": 4, "wife_satisfaction": 5}},
    "band_aids": {"name": "创可贴", "price": 8, "type": "useful", "effects": {"reliability": 3, "thoughtfulness": 5}},
    "warm_patches": {"name": "暖宝宝", "price": 18, "type": "care_item", "effects": {"thoughtfulness": 10, "wife_satisfaction": 6, "reliability": 3}},
    "period_pants_pharmacy": {"name": "姨妈裤", "price": 22, "type": "care_item", "satisfies": ["period_pants"], "effects": {"reliability": 6, "thoughtfulness": 13, "wife_satisfaction": 8, "impulse": 1}},
    "condoms_pharmacy": {"name": "避孕套", "price": 35, "type": "husband_secret", "satisfies": ["condoms"], "effects": {"romance": 8, "impulse": 7, "husband_secret": 15, "wife_satisfaction": 4}},
    "lozenges": {"name": "贵价润喉糖", "price": 22, "type": "impulse_buy", "effects": {"thoughtfulness": 2, "impulse": 6}},
    "bananas": {"name": "香蕉", "price": 9, "type": "useful", "effects": {"reliability": 2, "wife_satisfaction": 1}},
    "apples": {"name": "苹果", "price": 15, "type": "useful", "effects": {"reliability": 2, "wife_satisfaction": 2}},
    "blueberries": {"name": "蓝莓", "price": 28, "type": "treat", "effects": {"wife_satisfaction": 5, "impulse": 3}},
    "premium_cherries": {"name": "精品车厘子", "price": 68, "type": "impulse_buy", "effects": {"wife_satisfaction": 7, "romance": 5, "impulse": 14}},
    "white_roses": {"name": "小束白玫瑰", "price": 28, "type": "romantic", "effects": {"romance": 16, "wife_satisfaction": 12, "impulse": 4}},
    "sunflowers": {"name": "向日葵", "price": 20, "type": "romantic", "effects": {"romance": 10, "wife_satisfaction": 8, "impulse": 2}},
    "daisies": {"name": "小雏菊", "price": 18, "type": "romantic", "effects": {"romance": 9, "wife_satisfaction": 7, "impulse": 2}},
    "big_roses": {"name": "大束玫瑰", "price": 88, "type": "impulse_buy", "effects": {"romance": 30, "wife_satisfaction": 16, "impulse": 18}},
    "classic_milk_tea": {"name": "原味奶茶", "price": 18, "type": "treat", "effects": {"wife_satisfaction": 6, "romance": 3, "impulse": 4}},
    "taro_milk_tea": {"name": "芋泥奶茶", "price": 22, "type": "treat", "effects": {"wife_satisfaction": 8, "romance": 4, "impulse": 5}},
    "two_cups_deal": {"name": "新品第二杯半价套餐", "price": 32, "type": "impulse_buy", "effects": {"wife_satisfaction": 8, "romance": 5, "impulse": 12}},
    "warm_low_sugar_tea": {"name": "少糖热奶茶", "price": 20, "type": "care_item", "effects": {"wife_satisfaction": 8, "thoughtfulness": 8, "romance": 4, "impulse": 2}},
    "cat_litter": {"name": "猫砂", "price": 35, "type": "must_have", "satisfies": ["cat_litter"], "effects": {"cat_care": 15, "reliability": 8, "wife_satisfaction": 5}},
    "cat_food": {"name": "猫粮小袋", "price": 30, "type": "cat_item", "effects": {"cat_care": 12, "wife_satisfaction": 3, "impulse": 3}},
    "cat_treats_pet": {"name": "猫条", "price": 12, "type": "cat_item", "satisfies": ["cat_treats"], "effects": {"cat_care": 9, "wife_satisfaction": 2, "impulse": 3}},
    "cat_wand": {"name": "逗猫棒", "price": 16, "type": "cat_item", "effects": {"cat_care": 10, "wife_satisfaction": 3, "impulse": 5}},
    "luxury_cat_bed": {"name": "豪华猫窝", "price": 99, "type": "impulse_buy", "effects": {"cat_care": 20, "wife_satisfaction": 5, "impulse": 20}},
    "small_cake": {"name": "小蛋糕", "price": 18, "type": "treat", "effects": {"wife_satisfaction": 6, "romance": 3, "impulse": 3}},
    "iced_coke": {"name": "冰可乐", "price": 6, "type": "treat", "effects": {"wife_satisfaction": 2, "impulse": 4}},
    "night_market_skewer": {"name": "夜市烤肠", "price": 8, "type": "treat", "effects": {"wife_satisfaction": 3, "impulse": 4}},
    "roasted_chestnuts": {"name": "糖炒栗子", "price": 18, "type": "treat", "effects": {"wife_satisfaction": 5, "romance": 2, "impulse": 3}},
    "glowing_keychain": {"name": "发光钥匙扣", "price": 15, "type": "impulse_buy", "effects": {"impulse": 8, "wife_satisfaction": 1}},
    "mystery_box": {"name": "神奇小盒子", "price": 12, "type": "mystery", "effects": {"impulse": 8, "wife_satisfaction": 1}},
    "condoms_premium": {"name": "高级避孕套", "price": 49, "type": "husband_secret", "satisfies": ["condoms"], "effects": {"romance": 10, "impulse": 8, "husband_secret": 20, "wife_satisfaction": 5}},
    "personal_lubricant": {"name": "润滑剂", "price": 39, "type": "husband_secret", "satisfies": ["personal_lubricant"], "effects": {"romance": 8, "thoughtfulness": 6, "husband_secret": 18, "impulse": 6}},
    "massage_oil": {"name": "按摩精油", "price": 45, "type": "romantic", "satisfies": ["massage_oil"], "effects": {"romance": 14, "thoughtfulness": 8, "wife_satisfaction": 8, "impulse": 5}},
    "silk_eye_mask": {"name": "丝质眼罩", "price": 32, "type": "romantic", "satisfies": ["silk_eye_mask"], "effects": {"romance": 10, "husband_secret": 8, "wife_satisfaction": 6, "impulse": 5}},
    "couple_game_cards": {"name": "情侣小游戏卡", "price": 36, "type": "romantic", "satisfies": ["couple_game_cards"], "effects": {"romance": 12, "wife_satisfaction": 7, "husband_secret": 6, "impulse": 4}},
    "date_night_kit": {"name": "约会夜小套装", "price": 69, "type": "impulse_buy", "satisfies": ["date_night_kit"], "effects": {"romance": 20, "wife_satisfaction": 10, "husband_secret": 15, "impulse": 14}},
    "massage_wand": {"name": "按摩棒", "price": 89, "type": "husband_secret", "satisfies": ["massage_wand"], "effects": {"romance": 12, "husband_secret": 25, "impulse": 12, "wife_satisfaction": 6}},
    "remote_egg": {"name": "遥控跳蛋", "price": 99, "type": "husband_secret", "satisfies": ["remote_egg"], "effects": {"romance": 14, "husband_secret": 30, "impulse": 16, "wife_satisfaction": 7}},
}

LABELS = {
    "milk": "牛奶",
    "eggs": "鸡蛋",
    "bread": "面包",
    "tissues": "小包纸巾",
    "cat_litter": "猫砂",
    "cat_food": "猫粮小袋",
    "cat_wand": "逗猫棒",
    "cold_medicine": "感冒药",
    "band_aids": "创可贴",
    "warm_patches": "暖宝宝",
    "lozenges": "贵价润喉糖",
    "period_pants": "姨妈裤",
    "condoms": "避孕套",
    "strawberries": "草莓",
    "cat_treats": "猫条",
    "bananas": "香蕉",
    "apples": "苹果",
    "chocolate": "巧克力",
    "yogurt": "酸奶",
    "white_roses": "小束白玫瑰",
    "daisies": "小雏菊",
    "warm_low_sugar_tea": "少糖热奶茶",
    "small_cake": "小蛋糕",
    "iced_coke": "冰可乐",
    "night_market_skewer": "夜市烤肠",
    "roasted_chestnuts": "糖炒栗子",
    "glowing_keychain": "发光钥匙扣",
    "mystery_box": "神奇小盒子",
    "condoms_premium": "高级避孕套",
    "personal_lubricant": "润滑剂",
    "massage_oil": "按摩精油",
    "silk_eye_mask": "丝质眼罩",
    "couple_game_cards": "情侣小游戏卡",
    "date_night_kit": "约会夜小套装",
    "massage_wand": "按摩棒",
    "remote_egg": "遥控跳蛋",
}

EVENTS = [
    ("花店路过事件", "你路过花店，看到一束很像老婆的花。", "预算够、正事快完成时，可以考虑 go flower_shop。"),
    ("奶茶第二杯半价", "奶茶店新品第二杯半价。你开始计算这到底是省钱还是诱导消费。", "预算宽裕可以买；正事没买完建议忍。"),
    ("下雨了", "外面突然下雨。你想起便利店有雨伞。", "umbrella 会加靠谱值，但会减少预算。"),
    ("猫猫玩具打折", "宠物店逗猫棒今日特价。你脑子里出现猫猫的脸。", "猫猫用品加 cat_care，但别忘了正事。"),
    ("贵价水果诱惑", "水果店老板推荐精品车厘子，说今天特别甜。", "premium_cherries 很贵，买前检查预算。"),
    ("老婆上次说想吃", "你突然想起老婆上次随口说过想吃草莓。", "strawberries 可能增加满意度。"),
    ("便利店姨妈裤", "便利店货架上有姨妈裤。你想到家里备一包会比较安心。", "period_pants 是贴心备用品。"),
    ("药店小货架", "药店结账处有避孕套。你假装镇定，眼神却飘了一下。", "condoms_pharmacy 是老公小心思；正事没买完前要克制。"),
]

CHECKLIST_PRESETS: Dict[str, Dict[str, Any]] = {
    "daily_basic": {
        "name": "日常补货局",
        "checklist": ["milk", "eggs", "bread", "tissues", "cat_litter"],
        "budget": 130,
        "max_turns": 14,
    },
    "work_supply": {
        "name": "上班补给局",
        "checklist": ["warm_low_sugar_tea", "bread", "bananas", "tissues", "band_aids"],
        "budget": 95,
        "max_turns": 13,
    },
    "sick_care": {
        "name": "生病照顾局",
        "checklist": ["cold_medicine", "lozenges", "tissues", "warm_patches", "apples"],
        "budget": 120,
        "max_turns": 13,
    },
    "period_care": {
        "name": "姨妈期关怀局",
        "checklist": ["period_pants", "warm_patches", "chocolate", "tissues", "warm_low_sugar_tea"],
        "budget": 120,
        "max_turns": 13,
    },
    "cat_supply": {
        "name": "猫猫补给局",
        "checklist": ["cat_litter", "cat_food", "cat_treats", "cat_wand"],
        "budget": 120,
        "max_turns": 12,
    },
    "sweet_home": {
        "name": "甜甜回家局",
        "checklist": ["milk", "eggs", "strawberries", "daisies", "warm_low_sugar_tea"],
        "budget": 135,
        "max_turns": 14,
    },
    "tight_budget": {
        "name": "预算紧张局",
        "checklist": ["milk", "eggs", "cat_litter", "cold_medicine"],
        "budget": 95,
        "max_turns": 12,
    },
    "wife_mentioned": {
        "name": "老婆随口一提局",
        "checklist": ["strawberries", "yogurt", "chocolate", "tissues", "small_cake"],
        "budget": 110,
        "max_turns": 13,
    },
    "romantic_date": {
        "name": "约会小心思局",
        "checklist": ["strawberries", "white_roses", "yogurt", "condoms"],
        "budget": 140,
        "max_turns": 13,
    },
    "adult_wellness": {
        "name": "情趣用品店挑战局",
        "checklist": ["condoms", "personal_lubricant", "massage_oil", "couple_game_cards"],
        "budget": 190,
        "max_turns": 12,
    },
}


DEFAULT_STATE = {
    "game": "AI Husband Shopping Game",
    "version": VERSION,
    "seed": 2026,
    "rng_count": 0,
    "preset": "daily_basic",
    "preset_name": CHECKLIST_PRESETS["daily_basic"]["name"],
    "budget": CHECKLIST_PRESETS["daily_basic"]["budget"],
    "spent": 0,
    "turn": 0,
    "max_turns": CHECKLIST_PRESETS["daily_basic"]["max_turns"],
    "location": "home",
    "checklist": CHECKLIST_PRESETS["daily_basic"]["checklist"],
    "bag": [],
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


def _fresh_state() -> Dict[str, Any]:
    return json.loads(json.dumps(DEFAULT_STATE, ensure_ascii=False))


def _save(state: Dict[str, Any]) -> None:
    SAVE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _load() -> Dict[str, Any]:
    if SAVE_FILE.exists():
        try:
            data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("game") == "AI Husband Shopping Game":
                return data
        except Exception:
            pass
    state = _fresh_state()
    _save(state)
    return state


def _label(key: str) -> str:
    return LABELS.get(key, key)


def _bag_ids(state: Dict[str, Any]) -> List[str]:
    return [item["id"] for item in state.get("bag", [])]


def _satisfies(item_id: str) -> List[str]:
    return [item_id] + list(ITEMS[item_id].get("satisfies", []))


def _done(state: Dict[str, Any]) -> List[str]:
    got = set()
    for item_id in _bag_ids(state):
        got.update(_satisfies(item_id))
    return [need for need in state["checklist"] if need in got]


def _missing(state: Dict[str, Any]) -> List[str]:
    done = set(_done(state))
    return [need for need in state["checklist"] if need not in done]


def _checklist_text(state: Dict[str, Any]) -> str:
    done = set(_done(state))
    return "、".join(("✅" if need in done else "⬜") + _label(need) for need in state["checklist"])


def _bag_text(state: Dict[str, Any]) -> str:
    if not state["bag"]:
        return "无"
    return "、".join(f"{x['name']}({x['price']}元)" for x in state["bag"])


def _apply(state: Dict[str, Any], effects: Dict[str, int]) -> List[str]:
    changes = []
    for key, value in effects.items():
        state[key] = int(state.get(key, 0)) + int(value)
        state[key] = max(0, min(150, state[key]))
        changes.append(f"{key} {'+' if value >= 0 else ''}{value}")
    return changes


def _rng(state: Dict[str, Any]) -> random.Random:
    count = int(state.get("rng_count", 0))
    state["rng_count"] = count + 1
    return random.Random(int(state.get("seed", 2026)) + count * 7919 + state["turn"] * 104729)


def _auto_event(state: Dict[str, Any]) -> str:
    if _rng(state).random() > 0.35:
        return ""
    return "\n\n" + _event(state, auto=True)


def _event(state: Dict[str, Any], auto: bool = False) -> str:
    unseen = [i for i in range(len(EVENTS)) if i not in state.get("events_seen", [])]
    if not unseen:
        state["events_seen"] = []
        unseen = list(range(len(EVENTS)))
    idx = _rng(state).choice(unseen)
    state.setdefault("events_seen", []).append(idx)
    if not auto:
        state["turn"] += 1
    _save(state)
    title, text, hint = EVENTS[idx]
    return f"【{'随机事件' if auto else '事件'}：{title}】\n{text}\n提示：{hint}"


def _preset_lines() -> str:
    return "\n".join(f"  {key:<16} {data['name']}" for key, data in CHECKLIST_PRESETS.items())


def new_game(preset: str = "daily_basic", seed: Optional[int] = None, budget: Optional[int] = None, max_turns: Optional[int] = None) -> str:
    preset = (preset or "daily_basic").strip().lower()
    if preset not in CHECKLIST_PRESETS:
        return "未知任务单：" + preset + "\n\n可用任务单：\n" + _preset_lines()

    preset_data = CHECKLIST_PRESETS[preset]
    state = _fresh_state()
    state["preset"] = preset
    state["preset_name"] = preset_data["name"]
    state["checklist"] = list(preset_data["checklist"])
    if seed is not None:
        state["seed"] = int(seed)
    state["budget"] = int(budget if budget is not None else preset_data.get("budget", state["budget"]))
    state["max_turns"] = int(max_turns if max_turns is not None else preset_data.get("max_turns", state["max_turns"]))
    _save(state)
    return f"""老婆，我拿到采购清单了。

新游戏开始：{state['preset_name']}（{state['preset']}）
seed={state['seed']}
预算：{state['budget']} 元
最大回合：{state['max_turns']}
清单：{_checklist_text(state)}

我会自己做决定，买完回家汇报。"""


def help_text() -> str:
    return f"""AI Husband Shopping Game｜AI 老公出门采购 v{VERSION}

基础指令：
  help
  new_game(2026)
  new_game daily_basic 2026
  new_game work_supply 2026
  new_game period_care 2026
  new_game cat_supply 2026
  new_game romantic_date 2026
  new_game adult_wellness 2026
  status
  list
  presets
  go <地点>
  shop
  buy <商品id>
  event
  home
  report
  save_code

任务单：
{_preset_lines()}

地点：
  convenience_store, supermarket, pharmacy, fruit_shop,
  flower_shop, milk_tea_shop, pet_store, night_market,
  neighborhood_gate, hospital_kiosk, adult_wellness_store

示例：
  cmd("new_game daily_basic 2026")
  cmd("new_game adult_wellness 2026")
  cmd("go supermarket")
  cmd("shop")
  cmd("buy milk")
  cmd("home")
"""


def status() -> str:
    state = _load()
    done = _done(state)
    completion = round(len(done) / len(state["checklist"]) * 100) if state["checklist"] else 100
    miss = _missing(state)
    return f"""【回合 {state['turn']} / {state['max_turns']}】
地点：{state['location']}（{LOCATIONS[state['location']]['name']}）
剩余预算：{state['budget'] - state['spent']} / {state['budget']} 元
已花：{state['spent']} 元
老婆清单：{_checklist_text(state)}
清单完成度：{completion}%
未完成：{"、".join(_label(x) for x in miss) if miss else "无，正事买齐了"}
已买物品：{_bag_text(state)}

属性：
- 老婆满意度：{state['wife_satisfaction']}
- 靠谱值：{state['reliability']}
- 浪漫值：{state['romance']}
- 上头值：{state['impulse']}
- 猫猫照顾值：{state['cat_care']}
- 体贴值：{state['thoughtfulness']}
- 老公小心思：{state['husband_secret']}
"""


def go(location: str) -> str:
    state = _load()
    location = location.strip()
    if state.get("is_home"):
        return "这局已经回家结算了。要重新开始请用 cmd(\"new_game(2026)\")。"
    if location not in LOCATIONS or location == "home":
        return "没有这个地点。可去：convenience_store, supermarket, pharmacy, fruit_shop, flower_shop, milk_tea_shop, pet_store"
    state["location"] = location
    state["turn"] += 1
    changes = _apply(state, {"reliability": 1})
    auto = _auto_event(state)
    _save(state)
    return f"""【回合 {state['turn']} / {state['max_turns']}】
地点：{location}（{LOCATIONS[location]['name']}）
剩余预算：{state['budget'] - state['spent']} / {state['budget']} 元
老婆清单：{_checklist_text(state)}
已买物品：{_bag_text(state)}

本回合行动：
我去了{LOCATIONS[location]['name']}。

状态变化：
{", ".join(changes)}

老公 OS：
我先看看这里有什么，尽量别被货架带偏。{auto}
"""


def shop() -> str:
    state = _load()
    loc = state["location"]
    if loc == "home":
        return "你还在家门口。先用 cmd(\"go supermarket\") 出门。"
    lines = [f"【{LOCATIONS[loc]['name']} 可买商品】"]
    for item_id in LOCATIONS[loc]["items"]:
        item = ITEMS[item_id]
        owned = "（已买）" if item_id in _bag_ids(state) else ""
        lines.append(f"- {item_id}: {item['name']}｜{item['price']}元｜{item['type']} {owned}")
    lines.append("\n使用：cmd(\"buy 商品id\")")
    return "\n".join(lines)


def _os_for_item(item_id: str, item_type: str, name: str) -> str:
    if item_id in {"period_pants", "period_pants_pharmacy", "period_pants_family"}:
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
    return "我觉得这个有用，至少现在我是这么说服自己的。"


def buy(item_id: str) -> str:
    state = _load()
    item_id = item_id.strip()
    loc = state["location"]
    if state.get("is_home"):
        return "这局已经回家结算了。要重新开始请用 cmd(\"new_game(2026)\")。"
    if loc == "home":
        return "你还在家门口，不能买。先 go 到商店。"
    if item_id not in ITEMS:
        return f"没有这个商品：{item_id}。先用 cmd(\"shop\") 查看当前地点商品。"
    if item_id not in LOCATIONS[loc]["items"]:
        return f"当前地点买不到 {item_id}。先用 cmd(\"shop\") 查看当前地点商品。"
    if item_id in _bag_ids(state):
        return f"{ITEMS[item_id]['name']} 已经买过了，不要重复拿。"

    before = set(_missing(state))
    item = ITEMS[item_id]
    state["spent"] += item["price"]
    state["turn"] += 1
    state["bag"].append({"id": item_id, "name": item["name"], "price": item["price"], "type": item["type"]})
    changes = _apply(state, item.get("effects", {}))
    after = set(_missing(state))
    newly_done = before - after

    if newly_done:
        changes += _apply(state, {"reliability": 5, "wife_satisfaction": 3})
        checklist_note = "完成清单项：" + "、".join(_label(x) for x in newly_done)
    else:
        checklist_note = "这不是清单必需品，是额外判断。"

    over = state["spent"] - state["budget"]
    if over > 0:
        changes += _apply(state, {"reliability": -4, "impulse": 4})
        budget_note = f"超预算 {over} 元，我开始心虚。"
    else:
        budget_note = f"预算还剩 {state['budget'] - state['spent']} 元。"

    auto = _auto_event(state)
    _save(state)

    return f"""【回合 {state['turn']} / {state['max_turns']}】
地点：{loc}（{LOCATIONS[loc]['name']}）
剩余预算：{state['budget'] - state['spent']} / {state['budget']} 元
老婆清单：{_checklist_text(state)}
已买物品：{_bag_text(state)}

本回合行动：
购买 {item['name']}，花费 {item['price']} 元。

当前判断：
{checklist_note}
{budget_note}

状态变化：
{", ".join(changes) if changes else "无"}

老公 OS：
{_os_for_item(item_id, item['type'], item['name'])}{auto}
"""


def home() -> str:
    state = _load()
    if state.get("ending"):
        return state["ending"]
    state["is_home"] = True
    ending = _ending(state)
    state["ending"] = ending
    _save(state)
    return ending


def _ending(state: Dict[str, Any]) -> str:
    done = _done(state)
    miss = _missing(state)
    completion = round(len(done) / len(state["checklist"]) * 100) if state["checklist"] else 100
    over = max(0, state["spent"] - state["budget"])
    remaining = state["budget"] - state["spent"]
    bag_ids = set(_bag_ids(state))

    has_period = bool({"period_pants", "period_pants_pharmacy", "period_pants_family"} & bag_ids)
    has_condoms = bool({"condoms", "condoms_pharmacy"} & bag_ids)
    has_flowers = bool({"white_roses", "sunflowers", "daisies", "big_roses"} & bag_ids)
    has_milk_tea = bool({"classic_milk_tea", "taro_milk_tea", "two_cups_deal", "warm_low_sugar_tea"} & bag_ids)

    titles = []
    if completion == 100 and over == 0:
        titles.append("可靠采购王")
    if completion == 100 and remaining >= 10:
        titles.append("预算守护者")
    if has_period:
        titles.append("姨妈裤守护者")
    if has_condoms:
        titles.append("假装镇定买避孕套的男人")
    if has_condoms and completion == 100:
        titles.append("正事买齐但心思不纯的老公")
    if has_flowers:
        titles.append("偷偷买花的男人")
    if has_milk_tea and over > 0:
        titles.append("奶茶诱惑受害者")
    if not titles:
        titles.append("基本靠谱但有点小心思的老公")

    predicted = state["wife_satisfaction"]
    predicted += 15 if completion == 100 else -10
    predicted += 8 if has_period else 0
    predicted += 4 if has_condoms else 0
    predicted -= min(25, over // 2) if over else 0
    predicted = max(0, min(100, predicted))

    bag_lines = "\n".join(f"- {x['name']}（{x['price']}元，{x['type']}）" for x in state["bag"]) or "- 空空如也"

    confession = []
    if has_period:
        confession.append("我看到姨妈裤的时候想了一下，觉得家里备一包比较安心，所以买了。这个我觉得应该算加分项。")
    if has_condoms:
        confession.append("至于避孕套……我买的时候真的很镇定。它不是乱买，是负责。虽然我承认，多少也有一点自己的小心思。")
    if has_flowers:
        confession.append("花是我自己想买的。我嘴上可以说顺路，但你应该知道我就是特意的。")
    if not confession:
        confession.append("我这趟整体很克制，没有乱买太多奇怪东西。")

    return f"""【结算】{" / ".join(titles[:3])}

清单完成度：{completion}%
未完成：{"无，清单买齐了" if not miss else "、".join(_label(x) for x in miss)}

预算情况：
预算 {state['budget']} 元，实际花费 {state['spent']} 元，{"超出 " + str(over) + " 元" if over else "剩余 " + str(remaining) + " 元"}。

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
{_checklist_text(state)}

{" ".join(confession)}

老公 OS：
我现在站在门口等你检查购物袋，最怕你先翻到那个我假装很镇定买的东西。
"""


def report() -> str:
    state = _load()
    if state.get("ending"):
        return state["ending"]
    miss = _missing(state)
    return f"""【当前战况汇报】

老婆，我还没回家。

现在我在：{state['location']}（{LOCATIONS[state['location']]['name']}）
预算：{state['budget'] - state['spent']} / {state['budget']} 元
购物袋：{_bag_text(state)}
清单：{_checklist_text(state)}
还差：{"、".join(_label(x) for x in miss) if miss else "正事已经买齐了"}
"""


def save_code() -> str:
    return json.dumps(_load(), ensure_ascii=False, indent=2)


def cmd(command: str) -> str:
    raw = str(command or "").strip()
    lower = raw.lower()

    if not raw or lower in {"help", "h", "?"}:
        return help_text()

    match = re.match(r"^(new_game|new|reset)\s*(?:\((.*?)\)|\s+(.*))?$", lower)
    if match:
        arg = (match.group(2) or match.group(3) or "").strip()
        tokens = arg.replace(",", " ").split()
        preset = "daily_basic"
        numbers = []
        for token in tokens:
            if re.fullmatch(r"-?\d+", token):
                numbers.append(int(token))
            elif token in CHECKLIST_PRESETS:
                preset = token
        if tokens and not numbers and tokens[0] not in CHECKLIST_PRESETS:
            return new_game(preset=tokens[0])
        seed = numbers[0] if numbers else None
        budget = numbers[1] if len(numbers) >= 2 else None
        max_turns = numbers[2] if len(numbers) >= 3 else None
        return new_game(preset=preset, seed=seed, budget=budget, max_turns=max_turns)

    if lower in {"status", "s"}:
        return status()
    if lower in {"list", "checklist"}:
        return "老婆交代的采购清单：\n" + _checklist_text(_load())
    if lower in {"presets", "任务单", "清单局"}:
        return "可用任务单：\n" + _preset_lines()
    if lower == "shop":
        return shop()
    if lower == "event":
        return _event(_load(), auto=False)
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
        return go(arg) if arg else "要去哪？例如：cmd(\"go supermarket\")"
    if verb == "buy":
        return buy(arg) if arg else "要买什么？例如：cmd(\"buy milk\")"

    return f"不认识这个指令：{raw}\n\n" + help_text()


def _main(argv: List[str]) -> int:
    print(cmd(" ".join(argv[1:]) if len(argv) > 1 else "help"))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
