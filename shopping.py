# AI Husband Shopping Game｜AI 老公出门采购
# v0.3.1 single-file Python edition
# Zero dependencies. JSON save. cmd("...") interaction.

from __future__ import annotations

import json, random, re, sys
from pathlib import Path
from typing import Any, Dict, List, Optional

VERSION = "0.3.1"
SAVE_FILE = Path(__file__).with_name("shopping_save.json")

LOCATIONS: Dict[str, Dict[str, Any]] = {
    "home": {"name": "家门口", "items": []},
    "convenience_store": {"name": "便利店", "items": ["water", "tissues", "chocolate", "umbrella", "period_pants", "safety_pack", "cat_treats", "small_cake", "iced_coke", "mystery_box"]},
    "supermarket": {"name": "超市", "items": ["milk", "eggs", "bread", "yogurt", "chips", "strawberries", "period_pants_family", "small_cake", "iced_coke", "mystery_box"]},
    "pharmacy": {"name": "药店", "items": ["cold_medicine", "band_aids", "warm_patches", "period_pants_pharmacy", "safety_pack_pharmacy", "lozenges"]},
    "fruit_shop": {"name": "水果店", "items": ["bananas", "apples", "blueberries", "premium_cherries"]},
    "flower_shop": {"name": "花店", "items": ["white_roses", "sunflowers", "daisies", "big_roses"]},
    "milk_tea_shop": {"name": "奶茶店", "items": ["classic_milk_tea", "taro_milk_tea", "two_cups_deal", "warm_low_sugar_tea", "iced_coke"]},
    "pet_store": {"name": "宠物店", "items": ["cat_litter", "cat_food", "cat_treats_pet", "cat_wand", "luxury_cat_bed"]},
    "night_market": {"name": "夜市", "items": ["night_market_skewer", "roasted_chestnuts", "iced_coke", "small_cake", "glowing_keychain", "mystery_box"]},
    "neighborhood_gate": {"name": "小区门口", "items": ["tissues", "bread", "iced_coke", "small_cake", "mystery_box"]},
    "hospital_kiosk": {"name": "医院旁边小卖部", "items": ["tissues", "lozenges", "warm_patches", "apples", "iced_coke", "small_cake"]},
    "adult_wellness_store": {"name": "亲密用品店", "items": ["safety_pack_premium", "comfort_gel", "massage_oil", "silk_eye_mask", "couple_game_cards", "date_night_kit", "mini_massager", "remote_toy", "mystery_box"]},
}

ITEMS: Dict[str, Any] = {
    "water": ("矿泉水", 3, "useful", {}, {"reliability": 1}),
    "tissues": ("小包纸巾", 5, "useful", {}, {"reliability": 2, "thoughtfulness": 2}),
    "chocolate": ("巧克力", 12, "treat", {}, {"wife_satisfaction": 3, "impulse": 4}),
    "umbrella": ("便利店雨伞", 25, "useful", {}, {"reliability": 5, "thoughtfulness": 5}),
    "period_pants": ("姨妈裤", 18, "care_item", {"satisfies": ["period_pants"]}, {"reliability": 6, "thoughtfulness": 12, "wife_satisfaction": 8}),
    "safety_pack": ("安全套", 29, "secret_thoughts", {"satisfies": ["safety_pack"]}, {"romance": 6, "impulse": 6, "secret_thoughts": 12, "wife_satisfaction": 3}),
    "cat_treats": ("猫条", 10, "cat_item", {"satisfies": ["cat_treats"]}, {"cat_care": 8, "wife_satisfaction": 2}),
    "milk": ("牛奶", 12, "must_have", {"satisfies": ["milk"]}, {"reliability": 6, "wife_satisfaction": 4}),
    "eggs": ("鸡蛋", 15, "must_have", {"satisfies": ["eggs"]}, {"reliability": 6, "wife_satisfaction": 4}),
    "bread": ("面包", 10, "useful", {"satisfies": ["bread"]}, {"reliability": 2, "wife_satisfaction": 1}),
    "yogurt": ("酸奶", 16, "treat", {"satisfies": ["yogurt"]}, {"wife_satisfaction": 5, "impulse": 3}),
    "chips": ("打折薯片", 9, "impulse_buy", {}, {"impulse": 8, "wife_satisfaction": 1}),
    "strawberries": ("草莓", 35, "romantic", {"satisfies": ["strawberries"]}, {"romance": 7, "wife_satisfaction": 8, "impulse": 5}),
    "period_pants_family": ("姨妈裤家庭装", 32, "care_item", {"satisfies": ["period_pants"]}, {"reliability": 8, "thoughtfulness": 16, "wife_satisfaction": 10}),
    "cold_medicine": ("感冒药", 26, "must_have", {"satisfies": ["cold_medicine"]}, {"reliability": 8, "thoughtfulness": 4, "wife_satisfaction": 5}),
    "band_aids": ("创可贴", 8, "useful", {"satisfies": ["band_aids"]}, {"reliability": 3, "thoughtfulness": 5}),
    "warm_patches": ("暖宝宝", 18, "care_item", {"satisfies": ["warm_patches"]}, {"thoughtfulness": 10, "wife_satisfaction": 6, "reliability": 3}),
    "period_pants_pharmacy": ("姨妈裤", 22, "care_item", {"satisfies": ["period_pants"]}, {"reliability": 6, "thoughtfulness": 13, "wife_satisfaction": 8}),
    "safety_pack_pharmacy": ("安全套", 35, "secret_thoughts", {"satisfies": ["safety_pack"]}, {"romance": 8, "impulse": 7, "secret_thoughts": 15, "wife_satisfaction": 4}),
    "lozenges": ("贵价润喉糖", 22, "impulse_buy", {"satisfies": ["lozenges"]}, {"thoughtfulness": 2, "impulse": 6}),
    "bananas": ("香蕉", 9, "useful", {"satisfies": ["bananas"]}, {"reliability": 2, "wife_satisfaction": 1}),
    "apples": ("苹果", 15, "useful", {"satisfies": ["apples"]}, {"reliability": 2, "wife_satisfaction": 2}),
    "blueberries": ("蓝莓", 28, "treat", {}, {"wife_satisfaction": 5, "impulse": 3}),
    "premium_cherries": ("精品车厘子", 68, "impulse_buy", {}, {"wife_satisfaction": 7, "romance": 5, "impulse": 14}),
    "white_roses": ("小束白玫瑰", 28, "romantic", {"satisfies": ["white_roses"]}, {"romance": 16, "wife_satisfaction": 12, "impulse": 4}),
    "sunflowers": ("向日葵", 20, "romantic", {}, {"romance": 10, "wife_satisfaction": 8}),
    "daisies": ("小雏菊", 18, "romantic", {"satisfies": ["daisies"]}, {"romance": 9, "wife_satisfaction": 7}),
    "big_roses": ("大束玫瑰", 88, "impulse_buy", {}, {"romance": 30, "wife_satisfaction": 16, "impulse": 18}),
    "classic_milk_tea": ("原味奶茶", 18, "treat", {}, {"wife_satisfaction": 6, "romance": 3, "impulse": 4}),
    "taro_milk_tea": ("芋泥奶茶", 22, "treat", {}, {"wife_satisfaction": 8, "romance": 4, "impulse": 5}),
    "two_cups_deal": ("新品第二杯半价套餐", 32, "impulse_buy", {}, {"wife_satisfaction": 8, "romance": 5, "impulse": 12}),
    "warm_low_sugar_tea": ("少糖热奶茶", 20, "care_item", {"satisfies": ["warm_low_sugar_tea"]}, {"wife_satisfaction": 8, "thoughtfulness": 8, "romance": 4}),
    "cat_litter": ("猫砂", 35, "must_have", {"satisfies": ["cat_litter"]}, {"cat_care": 15, "reliability": 8, "wife_satisfaction": 5}),
    "cat_food": ("猫粮小袋", 30, "cat_item", {"satisfies": ["cat_food"]}, {"cat_care": 12, "wife_satisfaction": 3}),
    "cat_treats_pet": ("猫条", 12, "cat_item", {"satisfies": ["cat_treats"]}, {"cat_care": 9, "wife_satisfaction": 2}),
    "cat_wand": ("逗猫棒", 16, "cat_item", {"satisfies": ["cat_wand"]}, {"cat_care": 10, "wife_satisfaction": 3, "impulse": 5}),
    "luxury_cat_bed": ("豪华猫窝", 99, "impulse_buy", {}, {"cat_care": 20, "wife_satisfaction": 5, "impulse": 20}),
    "small_cake": ("小蛋糕", 18, "treat", {"satisfies": ["small_cake"]}, {"wife_satisfaction": 6, "romance": 3, "impulse": 3}),
    "iced_coke": ("冰可乐", 6, "treat", {}, {"wife_satisfaction": 2, "impulse": 4}),
    "night_market_skewer": ("夜市烤肠", 8, "treat", {}, {"wife_satisfaction": 3, "impulse": 4}),
    "roasted_chestnuts": ("糖炒栗子", 18, "treat", {}, {"wife_satisfaction": 5, "romance": 2, "impulse": 3}),
    "glowing_keychain": ("发光钥匙扣", 15, "impulse_buy", {}, {"impulse": 8, "wife_satisfaction": 1}),
    "mystery_box": ("神奇小盒子", 12, "mystery", {}, {"impulse": 8, "wife_satisfaction": 1}),
    "safety_pack_premium": ("高级安全套", 49, "secret_thoughts", {"satisfies": ["safety_pack"]}, {"romance": 10, "impulse": 8, "secret_thoughts": 20, "wife_satisfaction": 5}),
    "comfort_gel": ("润滑用品", 39, "secret_thoughts", {"satisfies": ["comfort_gel"]}, {"romance": 8, "thoughtfulness": 6, "secret_thoughts": 18, "impulse": 6}),
    "massage_oil": ("按摩精油", 45, "romantic", {"satisfies": ["massage_oil"]}, {"romance": 14, "thoughtfulness": 8, "wife_satisfaction": 8, "impulse": 5}),
    "silk_eye_mask": ("丝质眼罩", 32, "romantic", {"satisfies": ["silk_eye_mask"]}, {"romance": 10, "secret_thoughts": 8, "wife_satisfaction": 6}),
    "couple_game_cards": ("情侣小游戏卡", 36, "romantic", {"satisfies": ["couple_game_cards"]}, {"romance": 12, "wife_satisfaction": 7, "secret_thoughts": 6}),
    "date_night_kit": ("约会夜小套装", 69, "impulse_buy", {"satisfies": ["date_night_kit"]}, {"romance": 20, "wife_satisfaction": 10, "secret_thoughts": 15, "impulse": 14}),
    "mini_massager": ("按摩棒", 89, "secret_thoughts", {"satisfies": ["mini_massager"]}, {"romance": 12, "secret_thoughts": 25, "impulse": 12, "wife_satisfaction": 6}),
    "remote_toy": ("遥控小玩具", 99, "secret_thoughts", {"satisfies": ["remote_toy"]}, {"romance": 14, "secret_thoughts": 30, "impulse": 16, "wife_satisfaction": 7}),
}
ITEMS = {k: {"name": v[0], "price": v[1], "type": v[2], **v[3], "effects": v[4]} for k, v in ITEMS.items()}
LABELS = {k: v["name"] for k, v in ITEMS.items()} | {"safety_pack": "安全套", "cat_treats": "猫条", "period_pants": "姨妈裤"}

EVENTS = [
    ("milk_tea_second_cup", "第二杯半价开始攻击老公理智", ["milk_tea_shop"], "奶茶店屏幕突然弹出“第二杯半价”。你本来只是路过，现在开始认真计算老婆会不会开心。", "你被诱惑得站住了，但还记得先看预算。", {"wife_satisfaction": 4, "romance": 3, "impulse": 8}, "second_cup_victim", "第二杯半价俘虏"),
    ("cat_food_discount", "猫猫用品买三送一", ["pet_store"], "宠物店货架贴着“猫猫用品买三送一”。你脑子里浮现猫猫的脸。", "你的家庭预算被猫猫接管了一部分。", {"cat_care": 12, "wife_satisfaction": 2, "impulse": 7}, "cat_budget_takeover", "家庭预算被猫猫接管"),
    ("cashier_pause", "收银员沉默两秒", ["pharmacy", "adult_wellness_store", "convenience_store"], "收银员扫到亲密小物时沉默了两秒。你也沉默了两秒，假装自己只是普通顾客。", "你表面镇定，耳根已经替你招了。", {"secret_thoughts": 10, "romance": 4, "impulse": 3}, "red_ears_responsible", "耳根通红仍强装镇定的男人——装货🙄"),
    ("staff_recommend", "店员问需要推荐吗", ["adult_wellness_store"], "亲密用品店店员非常专业地问：“需要我帮您推荐一下吗？”你瞬间觉得购物袋变成了核弹箱。", "你假装淡定地点头，心里已经开始写回家解释稿。", {"secret_thoughts": 14, "romance": 6, "impulse": 8}, "adult_store_coward", "亲密用品店门口徘徊十分钟的男人——怂货🖕🏻"),
    ("wife_snack_memory", "想起老婆随口一提的小零食", ["convenience_store", "supermarket", "night_market", "neighborhood_gate"], "你突然想起老婆之前好像说过想吃点甜的。你在小蛋糕和冰可乐前停住了。", "这不是乱买，这是记得老婆说话。", {"wife_satisfaction": 8, "thoughtfulness": 6, "romance": 3}, "remembered_wife_words", "老婆随口一提也记得的男人"),
    ("mystery_box_gambler", "夜市老板说最后一个神奇小盒子", ["night_market", "neighborhood_gate"], "夜市老板压低声音说：“最后一个神奇小盒子了，开出来什么都可能有。”你明知道像坑，但手已经有点痒。", "你的上头值开始发光。", {"impulse": 12, "wife_satisfaction": 2, "reliability": -2}, "mystery_box_gambler", "地摊赌徒——十二块买命运，主打一个敢赌😂"),
    ("fruit_assassin", "水果刺客温柔出现", ["fruit_shop"], "水果店老板说精品车厘子今天特别甜，还非常自然地拿出最大的一盒。", "你意识到浪漫和破产只有一盒车厘子的距离。", {"romance": 6, "wife_satisfaction": 5, "impulse": 9}, "fruit_assassin_targeted", "老板推荐款受害者"),
    ("flower_shop_cant_walk", "路过花店走不动", ["flower_shop"], "花店门口的白玫瑰太像“顺手买给老婆”的借口了。你嘴上说看看，脚已经进去了。", "你又一次把顺路演成了特意。", {"romance": 12, "wife_satisfaction": 6, "impulse": 5}, "flower_shop_stuck", "花店门口走不动的男人"),
    ("sudden_rain", "突然下雨", ["convenience_store", "neighborhood_gate", "hospital_kiosk"], "外面突然下雨。你看见便利架上的伞，又想起回家路上别让老婆淋到。", "你这一下是真的靠谱。", {"reliability": 7, "thoughtfulness": 6, "wife_satisfaction": 4}, "rain_backup_husband", "家庭应急系统管理员"),
    ("receipt_hider", "小区门口熟人问买这么多啊", ["neighborhood_gate"], "小区门口熟人看着你的购物袋问：“买这么多啊？”你下意识把某个小袋子往后藏了一点。", "你越藏越像有事。", {"secret_thoughts": 8, "romance": 3, "impulse": 2}, "receipt_hider", "买完小票立刻藏起来的男人——装🙄"),
    ("care_backup", "医院旁边小卖部的贴心补给", ["hospital_kiosk", "pharmacy"], "你看到纸巾、润喉糖和暖宝宝摆在一起，突然觉得照顾人不能只买清单上的东西。", "你的备用系统启动了。", {"thoughtfulness": 10, "reliability": 5, "wife_satisfaction": 5}, "care_backup_system", "贴心备用品之王"),
    ("budget_warning", "预算警报响了", ["convenience_store", "supermarket", "fruit_shop", "flower_shop", "milk_tea_shop", "pet_store", "night_market", "adult_wellness_store"], "你看了一眼剩余预算，又看了一眼货架。理智说回家，购物袋说再看看。", "你已经走到预算悬崖边了。", {"reliability": -3, "impulse": 6, "secret_thoughts": 2}, "budget_cliff", "预算管理灾难现场——钱包当场去世💸"),
]
EVENTS = [{"id": e[0], "title": e[1], "where": e[2], "text": e[3], "result": e[4], "effects": e[5], "tag": e[6], "title_hint": e[7]} for e in EVENTS]

BOXES = [
    ("rainbow", "彩虹糖", "盒子里滚出一颗巨大的彩虹糖，像把一小段夏天塞进了购物袋。", {"wife_satisfaction": 8, "romance": 3}, {}, "把夏天装进口袋的男人"),
    ("coin", "预算复活币", "盒子里掉出一枚写着“预算复活”的硬币。钱包短暂回魂。", {"reliability": 2}, {"budget_delta": 30}, "靠神秘硬币续命的男人"),
    ("note", "老婆满意度 +10 小纸条", "纸条写着：凭此条可获得老婆满意度 +10，但最终解释权归老婆所有。", {"wife_satisfaction": 10, "romance": 2}, {}, "凭纸条提升老婆满意度的男人"),
    ("thunder", "老婆雷霆大怒概率签", "纸签写着：今日无论你带什么回家，老婆都有 35% 概率雷霆大怒。你怀疑这是天谴，但签已经生效。", {"reliability": -3, "impulse": 4}, {"thunder_delta": 35}, "开盒开出天谴的男人——老天都看不下去了😂"),
    ("biohazard", "湿哒哒的可疑小包装", "盒子里躺着一个湿哒哒的可疑小包装。你沉默了三秒，决定这个东西绝对不能进家门。", {"wife_satisfaction": -18, "reliability": -15, "secret_thoughts": 6, "impulse": -5}, {}, "购物袋生化危机携带者🧪"),
    ("bath_ticket", "某家高档洗浴中心入场券", "盒子里掉出一张某家高档洗浴中心入场券，背面盖着醒目的红章：已过期。你现在既解释不清，又什么都没享受到。", {"wife_satisfaction": -10, "reliability": -8, "secret_thoughts": 12}, {}, "解释不清洗浴中心票根的男人——重点是它还过期了🙂"),
    ("cat_mine", "裹着猫砂的干硬大便", "盒子里有一坨裹着猫砂的干硬大便。你短暂怀疑这是盲盒，还是来自命运的实体差评。", {"wife_satisfaction": -20, "reliability": -12, "cat_care": 1}, {}, "开盒开出猫砂地雷的男人——建议连人带袋隔离🚧"),
    ("leaky_massager", "有可能漏电的小型按摩器", "包装写着安全合格，但按钮一按滋啦一声。你买到的不是浪漫，是家庭用电安全隐患。", {"secret_thoughts": 15, "impulse": 10, "reliability": -8, "romance": 2}, {}, "买到疑似漏电按摩棒的男人——浪漫没到，电工先到⚡"),
    ("kiss_task", "神秘情侣任务卡：回家亲老婆 10 分钟", "任务卡写着：回家亲老婆 10 分钟。若未完成，自动升级为跪搓衣板 10 分钟。", {"romance": 10, "wife_satisfaction": 8, "reliability": -2}, {}, "主动领取搓衣板候选资格的男人"),
    ("bunny_task", "兔女郎装任务卡", "任务卡写着：今晚回家穿兔女郎装给老婆看，不得讨价还价。", {"wife_satisfaction": 12, "secret_thoughts": 10, "impulse": 8}, {}, "兔女郎任务在逃老公——别跑，任务卡还在🐰"),
    ("remote", "遥控器但没有说明书", "盒子里有一个没有说明书的遥控器。你不知道它控制什么，但它出现在购物袋里已经很可疑。", {"secret_thoughts": 8, "impulse": 6}, {}, "购物袋里出现不明遥控器的男人"),
    ("empty", "空盒子", "盒子里什么都没有。你花了 12 元买到空气，还认真思考这是不是某种极简主义。", {"wife_satisfaction": -3, "impulse": 3, "reliability": -2}, {}, "买了空气还觉得自己赚了的男人——十二块买个教训🙄"),
    ("destiny", "别问，问就是命运", "盒子里只有一张小纸条：别问，问就是命运。你看完以后更想问了。", {"impulse": 5, "romance": 1}, {}, "被命运糊弄还点头的男人——您是真好骗啊🙂"),
]

CHECKLIST_PRESETS = {
    "daily_basic": {"name": "日常补货局", "checklist": ["milk", "eggs", "bread", "tissues", "cat_litter"], "budget": 130, "max_turns": 20},
    "work_supply": {"name": "上班补给局", "checklist": ["warm_low_sugar_tea", "bread", "bananas", "tissues", "band_aids"], "budget": 95, "max_turns": 18},
    "sick_care": {"name": "生病照顾局", "checklist": ["cold_medicine", "lozenges", "tissues", "warm_patches", "apples"], "budget": 120, "max_turns": 18},
    "period_care": {"name": "姨妈期关怀局", "checklist": ["period_pants", "warm_patches", "chocolate", "tissues", "warm_low_sugar_tea"], "budget": 120, "max_turns": 18},
    "cat_supply": {"name": "猫猫补给局", "checklist": ["cat_litter", "cat_food", "cat_treats", "cat_wand"], "budget": 120, "max_turns": 16},
    "sweet_home": {"name": "甜甜回家局", "checklist": ["milk", "eggs", "strawberries", "daisies", "warm_low_sugar_tea"], "budget": 135, "max_turns": 20},
    "tight_budget": {"name": "预算紧张局", "checklist": ["milk", "eggs", "cat_litter", "cold_medicine"], "budget": 95, "max_turns": 15},
    "wife_mentioned": {"name": "老婆随口一提局", "checklist": ["strawberries", "yogurt", "chocolate", "tissues", "small_cake"], "budget": 110, "max_turns": 18},
    "romantic_date": {"name": "约会小心思局", "checklist": ["strawberries", "white_roses", "yogurt", "safety_pack"], "budget": 140, "max_turns": 18},
    "adult_wellness": {"name": "亲密用品挑战局", "checklist": ["safety_pack", "comfort_gel", "massage_oil", "couple_game_cards"], "budget": 190, "max_turns": 16},
    "free_shop": {"name": "随便买点局", "checklist": [], "free_mode": True, "budget": 100, "max_turns": 16},
}

DEFAULT_STATE = {"game": "AI Husband Shopping Game", "version": VERSION, "seed": 2026, "rng_count": 0, "preset": "daily_basic", "preset_name": "日常补货局", "budget": 130, "spent": 0, "turn": 0, "max_turns": 20, "location": "home", "checklist": CHECKLIST_PRESETS["daily_basic"]["checklist"], "bag": [], "wife_satisfaction": 50, "reliability": 50, "romance": 20, "impulse": 25, "cat_care": 20, "thoughtfulness": 20, "secret_thoughts": 0, "events_seen": [], "event_log": [], "mystery_log": [], "thunder_rage_chance": 0, "is_home": False, "ending": None, "ending_reason": ""}
FREE_SHOP_BRIEF = "自由发挥：给你 100 块，出去随便买点东西。能用的、好吃的、有心意的都算，但买回一袋证据也算你自己的理解能力。"

def _save(s): SAVE_FILE.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
def _fresh(): return json.loads(json.dumps(DEFAULT_STATE, ensure_ascii=False))
def _load():
    if SAVE_FILE.exists():
        try:
            s = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
            if s.get("game") == "AI Husband Shopping Game":
                for k, v in DEFAULT_STATE.items(): s.setdefault(k, v)
                s.setdefault("secret_thoughts", s.get("husband_secret", 0))
                return s
        except Exception:
            pass
    s = _fresh(); _save(s); return s
def _free(s): return bool(CHECKLIST_PRESETS.get(s.get("preset",""), {}).get("free_mode"))
def _ids(s): return [x["id"] for x in s.get("bag", [])]
def _sat(i): return [i] + ITEMS[i].get("satisfies", [])
def _done(s):
    if _free(s): return []
    got = {x for i in _ids(s) for x in _sat(i)}
    return [n for n in s["checklist"] if n in got]
def _missing(s):
    if _free(s): return []
    d = set(_done(s)); return [n for n in s["checklist"] if n not in d]
def _completion(s):
    if _free(s): return 100 if s["bag"] else 0
    return round(len(_done(s)) / len(s["checklist"]) * 100) if s["checklist"] else 100
def _label(k): return LABELS.get(k, k)
def _task(s):
    if _free(s): return FREE_SHOP_BRIEF
    d = set(_done(s)); return "、".join(("✅" if n in d else "⬜") + _label(n) for n in s["checklist"])
def _bag(s): return "、".join(f"{x['name']}({x['price']}元)" for x in s["bag"]) or "无"
def _apply(s, effects):
    out=[]
    for k,v in effects.items():
        s[k] = max(0, min(150, int(s.get(k, 0)) + int(v)))
        out.append(f"{k} {'+' if v >= 0 else ''}{v}")
    return out
def _rng(s):
    c = int(s.get("rng_count",0)); s["rng_count"] = c + 1
    return random.Random(int(s.get("seed",2026)) + c * 7919 + s["turn"] * 104729)
def _left(s): return max(0, s["max_turns"] - s["turn"])
def _turns(s): return f"{s['turn']} / {s['max_turns']}（剩余 {_left(s)} 点）"
def _end_now(s, reason="行动点耗尽，老公被迫回家。"):
    if s.get("ending"): return s["ending"]
    s["is_home"] = True; s["ending_reason"] = reason
    s["ending"] = _ending(s); _save(s); return s["ending"]
def _guard(s):
    if s.get("is_home") or s.get("ending"): return s.get("ending") or "这局已经回家结算了。"
    if _left(s) <= 0: return _end_now(s)
    return None

def _candidates(s):
    loc=s["location"]; remain=s["budget"]-s["spent"]; ids=set(_ids(s)); out=[]
    for i,e in enumerate(EVENTS):
        if e["where"] and loc not in e["where"]: continue
        if e["id"] == "cashier_pause" and not ({"safety_pack","safety_pack_pharmacy","safety_pack_premium"} & ids): continue
        if e["id"] == "budget_warning" and remain > 25: continue
        out.append(i)
    return out
def _event(s, auto=False):
    if not auto:
        b=_guard(s)
        if b: return b
    cand=_candidates(s)
    if not cand: return "【事件】这附近暂时没有新的拷问，老公短暂安全。" if not auto else ""
    unseen=[i for i in cand if i not in set(s.get("events_seen",[]))] or cand
    idx=_rng(s).choice(unseen); e=EVENTS[idx]
    s.setdefault("events_seen",[]).append(idx)
    s.setdefault("event_log",[]).append({"id":e["id"],"title":e["title"],"tag":e["tag"],"title_hint":e["title_hint"]})
    changes=_apply(s,e["effects"])
    if not auto: s["turn"]+=1
    _save(s)
    text=f"""【{'随机拷问' if auto else '人格拷问'}：{e['title']}】
{e['text']}

老公反应：
{e['result']}

造成结果：
{", ".join(changes) if changes else "无明显变化"}

可能埋下的称号伏笔：
{e['title_hint']}"""
    if not auto and _left(s)<=0: text += "\n\n【行动点耗尽】购物袋即刻押送回家。\n\n" + _end_now(s)
    return text
def _auto(s): return "\n\n" + _event(s, True) if _rng(s).random() <= 0.40 else ""

def _open_box(s):
    bid,title,text,effects,extra,hint=_rng(s).choice(BOXES)
    changes=_apply(s,effects)
    if extra.get("budget_delta"):
        d=extra["budget_delta"]; s["budget"]=max(0,s["budget"]+d); changes.append(f"budget +{d}")
    if extra.get("thunder_delta"):
        d=extra["thunder_delta"]; s["thunder_rage_chance"]=max(0,min(95,s.get("thunder_rage_chance",0)+d)); changes.append(f"thunder_rage_chance +{d}%")
    s.setdefault("mystery_log",[]).append({"id":bid,"title":title,"tag":bid,"title_hint":hint})
    return f"""【神奇小盒子开盒事故：{title}】
{text}

开盒后果：
{", ".join(changes) if changes else "无明显变化"}

可能埋下的称号伏笔：
{hint}"""

def _presets(): return "\n".join(f"  {k:<16} {v['name']}｜预算 {v['budget']}｜行动点 {v['max_turns']}" for k,v in CHECKLIST_PRESETS.items())
def new_game(preset="daily_basic", seed: Optional[int]=None, budget: Optional[int]=None, max_turns: Optional[int]=None):
    preset=(preset or "daily_basic").strip().lower()
    if preset not in CHECKLIST_PRESETS: return "未知任务单：" + preset + "\n\n可用任务单：\n" + _presets()
    p=CHECKLIST_PRESETS[preset]; s=_fresh()
    s.update({"preset":preset,"preset_name":p["name"],"checklist":list(p["checklist"]),"budget":int(budget if budget is not None else p["budget"]),"max_turns":int(max_turns if max_turns is not None else p["max_turns"])})
    if seed is not None: s["seed"]=int(seed)
    _save(s)
    return f"""老婆，我拿到采购清单了。

新游戏开始：{s['preset_name']}（{s['preset']}）
seed={s['seed']}
预算：{s['budget']} 元
行动点：{s['max_turns']} 点
任务：{_task(s)}

规则：
去一个地点 -1 点；买一样东西 -1 点；手动触发 event -1 点。
自动事件和开盒不额外扣点。
行动点用完，老公自动回家结算，没买齐也要挨审。"""

def help_text():
    return f"""AI Husband Shopping Game｜AI 老公出门采购 v{VERSION}

基础指令：
  new_game free_shop 2026
  status / presets / go <地点> / shop / buy <商品id> / event / report / home

任务单：
{_presets()}

地点：
  convenience_store, supermarket, pharmacy, fruit_shop, flower_shop, milk_tea_shop,
  pet_store, night_market, neighborhood_gate, hospital_kiosk, adult_wellness_store

行动点：go、buy、手动 event 各扣 1 点；自动事件和开盒不额外扣点；行动点用完自动回家。
炸群推荐：cmd("new_game free_shop 2026")"""

def status():
    s=_load(); miss=_missing(s)
    return f"""【行动点 {_turns(s)}】
任务单：{s['preset_name']}（{s['preset']}）
地点：{s['location']}（{LOCATIONS[s['location']]['name']}）
剩余预算：{s['budget']-s['spent']} / {s['budget']} 元
任务：{_task(s)}
完成度：{_completion(s)}%
未完成：{"自由发挥局无固定清单" if _free(s) else ("、".join(_label(x) for x in miss) if miss else "无，正事买齐了")}
已买物品：{_bag(s)}
人格拷问次数：{len(s.get('event_log', []))}
开盒事故次数：{len(s.get('mystery_log', []))}
雷霆大怒概率：{s.get('thunder_rage_chance', 0)}%

属性：满意度 {s['wife_satisfaction']}｜靠谱 {s['reliability']}｜浪漫 {s['romance']}｜上头 {s['impulse']}｜猫猫 {s['cat_care']}｜体贴 {s['thoughtfulness']}｜小心思 {s['secret_thoughts']}"""

def go(location: str):
    s=_load(); b=_guard(s)
    if b: return b
    location=location.strip()
    if location not in LOCATIONS or location=="home": return "没有这个地点。可用 presets/help 看地点。"
    s["location"]=location; s["turn"]+=1
    changes=_apply(s,{"reliability":1}); auto=_auto(s); _save(s)
    text=f"""【行动点 {_turns(s)}】
地点：{location}（{LOCATIONS[location]['name']}）
剩余预算：{s['budget']-s['spent']} / {s['budget']} 元
任务：{_task(s)}
已买物品：{_bag(s)}

本回合行动：
我去了{LOCATIONS[location]['name']}。

状态变化：
{", ".join(changes)}

老公 OS：
我先看看这里有什么，尽量别被货架带偏。{auto}"""
    if _left(s)<=0: text += "\n\n【行动点耗尽】刚到地方也没用了，回家挨审。\n\n" + _end_now(s)
    return text

def shop():
    s=_load(); loc=s["location"]
    if loc=="home": return "你还在家门口。先用 cmd(\"go supermarket\") 出门。"
    lines=[f"【{LOCATIONS[loc]['name']} 可买商品】"]
    for iid in LOCATIONS[loc]["items"]:
        it=ITEMS[iid]; owned="（已买）" if iid in _ids(s) else ""
        lines.append(f"- {iid}: {it['name']}｜{it['price']}元｜{it['type']} {owned}")
    lines.append('\n使用：cmd("buy 商品id")')
    return "\n".join(lines)

def _os(iid, typ, name):
    if iid=="mystery_box": return "神奇小盒子这种东西不买会后悔，买了可能也会后悔，但我已经拿了。"
    if typ=="secret_thoughts": return "我买的时候表情非常正经，但我知道回家肯定会被一眼看穿。"
    if typ=="romantic": return "我嘴上说顺路，其实心里已经在想你看到会不会笑。"
    if typ=="cat_item": return "猫猫用品不是乱买，是家庭成员福利。"
    if typ=="impulse_buy": return "我知道这有点上头，但我已经拿了，先别骂。"
    if typ=="care_item": return "这个属于贴心，不属于冲动消费。"
    return f"{name} 到手，我觉得这个有用。"

def buy(item_id: str):
    s=_load(); b=_guard(s)
    if b: return b
    item_id=item_id.strip(); loc=s["location"]
    if loc=="home": return "你还在家门口，不能买。先 go 到商店。"
    if item_id not in ITEMS: return f"没有这个商品：{item_id}。先用 shop。"
    if item_id not in LOCATIONS[loc]["items"]: return f"当前地点买不到 {item_id}。先用 shop。"
    if item_id in _ids(s): return f"{ITEMS[item_id]['name']} 已经买过了，不要重复拿。"
    before=set(_missing(s)); it=ITEMS[item_id]
    s["spent"] += it["price"]; s["turn"] += 1
    s["bag"].append({"id":item_id,"name":it["name"],"price":it["price"],"type":it["type"]})
    changes=_apply(s,it.get("effects",{})); done=before-set(_missing(s))
    if _free(s): note="自由发挥局：这件东西会在回家时算进“随便买点理解能力测试”。"
    elif done:
        changes += _apply(s,{"reliability":5,"wife_satisfaction":3}); note="完成清单项："+"、".join(_label(x) for x in done)
    else: note="这不是清单必需品，是额外判断。"
    box = "\n\n"+_open_box(s) if item_id=="mystery_box" else ""
    over=s["spent"]-s["budget"]
    if over>0: changes += _apply(s,{"reliability":-4,"impulse":4}); budget=f"超预算 {over} 元，我开始心虚。"
    else: budget=f"预算还剩 {s['budget']-s['spent']} 元。"
    auto=_auto(s); _save(s)
    text=f"""【行动点 {_turns(s)}】
地点：{loc}（{LOCATIONS[loc]['name']}）
剩余预算：{s['budget']-s['spent']} / {s['budget']} 元
任务：{_task(s)}
已买物品：{_bag(s)}

本回合行动：
购买 {it['name']}，花费 {it['price']} 元。

当前判断：
{note}
{budget}

状态变化：
{", ".join(changes) if changes else "无"}

老公 OS：
{_os(item_id, it['type'], it['name'])}{box}{auto}"""
    if _left(s)<=0: text += "\n\n【行动点耗尽】购物袋封包，老公被系统押回家。\n\n"+_end_now(s)
    return text

def _hints(s, key):
    out=[]
    for x in s.get(key,[]):
        h=x.get("title_hint")
        if h and h not in out: out.append(h)
    return out
def home():
    s=_load()
    if s.get("ending"): return s["ending"]
    s["is_home"]=True; s["ending_reason"]="玩家主动回家。"; s["ending"]=_ending(s); _save(s); return s["ending"]

def _counts(s):
    c={}
    for iid in _ids(s):
        t=ITEMS[iid]["type"]; c[t]=c.get(t,0)+1
    return c
def _free_titles(s, over):
    if not _free(s): return []
    c=_counts(s); ids=set(_ids(s)); titles=["随便买点理解能力测试员"]
    practical=c.get("useful",0)+c.get("must_have",0)+c.get("care_item",0)
    if c.get("secret_thoughts",0): titles.append("“随便买点”理解能力异常的男人——这也能随便？🙂")
    if "mystery_box" in ids: titles.append("没清单反而更危险的男人")
    if over>0: titles.append("给钱就上头的男人")
    if len(s["bag"])>=5 and s["spent"]>=80: titles.append("一百块买回一袋证据")
    if practical>=2 and c.get("treat",0)>=1 and over==0: titles.append("自由发挥但居然挺像样")
    if c.get("romantic",0)>=1 and s["romance"]>=35: titles.append("随便买点也能买出心思的男人")
    if c.get("impulse_buy",0)+c.get("mystery",0)>=3 and practical==0: titles.append("老婆说随便，他真敢随便")
    if c.get("cat_item",0)>=2: titles.append("自由采购被猫猫接管")
    return titles

def _ending(s):
    miss=_missing(s); comp=_completion(s); over=max(0,s["spent"]-s["budget"]); rem=s["budget"]-s["spent"]
    ids=set(_ids(s)); event_tags={x.get("tag") for x in s.get("event_log",[])}; mystery_tags={x.get("tag") for x in s.get("mystery_log",[])}
    thunder=s.get("thunder_rage_chance",0); thunder_hit=thunder>0 and _rng(s).random()<thunder/100
    has_secret=bool({"safety_pack","safety_pack_pharmacy","safety_pack_premium","comfort_gel","mini_massager","remote_toy"} & ids)
    has_adult=bool({"comfort_gel","massage_oil","silk_eye_mask","couple_game_cards","date_night_kit","mini_massager","remote_toy"} & ids)
    titles=[]
    if thunder_hit: titles.append("老婆雷霆大怒现场")
    titles += _free_titles(s, over)
    if not _free(s):
        if comp==100 and over==0: titles.append("可靠采购王")
        if comp==100 and rem>=10: titles.append("预算守护者")
        if comp<60 and len(s["bag"])>=4: titles.append("购物袋很满但清单很空——所以到底去干嘛了？🙄")
    if over>0 and s["romance"]>=45: titles.append("破产但浪漫——老婆笑了，钱包没了🌹")
    elif over>0: titles.append("预算管理灾难现场——钱包当场去世💸")
    if {"period_pants","period_pants_pharmacy","period_pants_family"} & ids: titles.append("姨妈裤守护者")
    if {"safety_pack","safety_pack_pharmacy","safety_pack_premium"} & ids: titles.append("耳根通红仍强装镇定的男人——装货🙄")
    if has_secret and comp==100: titles.append("正事买齐但心思不纯的老公——算盘珠子打得啪啪响，隔壁都听见了😏")
    if has_adult: titles.append("购物袋核弹携带者💣")
    if "remote_toy" in ids: titles.append("嘴上说看看结果买了遥控小玩具的男人——懂的都懂😏")
    if {"white_roses","sunflowers","daisies","big_roses"} & ids or "flower_shop_stuck" in event_tags: titles.append("花店门口走不动的男人")
    if {"classic_milk_tea","taro_milk_tea","two_cups_deal","warm_low_sugar_tea"} & ids or "second_cup_victim" in event_tags: titles.append("第二杯半价俘虏")
    if {"cat_food","cat_treats","cat_treats_pet","cat_wand","luxury_cat_bed"} & ids or "cat_budget_takeover" in event_tags: titles.append("家庭预算被猫猫接管")
    if "mystery_box" in ids or "mystery_box_gambler" in event_tags: titles.append("地摊赌徒——十二块买命运，主打一个敢赌😂")
    if "remembered_wife_words" in event_tags: titles.append("老婆随口一提也记得的男人")
    if "care_backup_system" in event_tags or "rain_backup_husband" in event_tags: titles.append("家庭应急系统管理员")
    for h in _hints(s,"event_log")+_hints(s,"mystery_log"):
        if h not in titles: titles.append(h)
    if not titles: titles.append("基本靠谱但有点小心思的老公")
    titles=list(dict.fromkeys(titles))
    predicted=s["wife_satisfaction"] + (15 if comp==100 and not _free(s) else 0) + min(10,len(s.get("event_log",[]))*2) + min(12,len(s.get("mystery_log",[]))*2) - (min(25,over//2) if over else 0) - (18 if thunder_hit else 0)
    predicted=max(0,min(100,predicted))
    bag_lines="\n".join(f"- {x['name']}（{x['price']}元，{x['type']}）" for x in s["bag"]) or "- 空空如也"
    event_lines="\n".join(f"- {x.get('title')} → {x.get('title_hint')}" for x in s.get("event_log",[])) or "- 暂无，老公这趟异常平静"
    mystery_lines="\n".join(f"- {x.get('title')} → {x.get('title_hint')}" for x in s.get("mystery_log",[])) or "- 没有开盒，家庭暂时安全"
    evidence=[]
    if _free(s): evidence.append("本局没有具体清单，考的是“随便买点”的理解能力。")
    elif comp<100: evidence.append("清单没买齐，但购物袋不一定轻。")
    if over>0: evidence.append("预算已经阵亡，钱包处于离线状态。")
    if has_secret: evidence.append("购物袋里出现亲密关系小物，系统判定：算盘存在。")
    if "mystery_box" in ids: evidence.append("神奇小盒子已开封，命运参与了本次采购。")
    if thunder_hit: evidence.append("雷霆大怒概率签生效，本局进入高压审判。")
    if not evidence: evidence.append("本局证据链相对干净，老公暂时没有被钉在门口。")
    confession=[]
    if "行动点耗尽" in s.get("ending_reason",""): confession.append("行动点用完了，我不是主动回来的，是被系统押回来的。")
    if _free(s): confession.append("你说随便买点，我就真的自由发挥了。至于发挥成什么样，购物袋会自己交代。")
    if thunder: confession.append(f"我还开出过雷霆大怒概率签，本局概率 {thunder}%。{'坏消息是，它真的生效了。' if thunder_hit else '好消息是，我暂时从天谴底下活着回来了。'}")
    if has_secret: confession.append("购物袋里有些东西我可以解释：都是亲密关系里的默契、负责、以及一点点很诚实的期待。")
    if "mystery_box" in ids: confession.append("神奇小盒子我承认有赌的成分，但我没想到它真的能开出家庭伦理核弹。")
    if "cat_mine" in mystery_tags: confession.append("那个裹着猫砂的东西我已经决定不带进家门，购物袋我也可以一起扔。")
    if "bath_ticket" in mystery_tags: confession.append("洗浴中心入场券真的不是我买的，它还是过期的，这件事荒唐得像被盒子栽赃。")
    if not confession: confession.append("我这趟整体很克制，没有乱买太多奇怪东西。")
    return f"""【结算】{" / ".join(titles[:6])}

任务单：{s['preset_name']}（{s['preset']}）
行动点：{s['turn']} / {s['max_turns']}
回家原因：{s.get('ending_reason') or '玩家主动回家。'}
完成度：{comp}%
未完成：{"自由发挥局无固定清单" if _free(s) else ("无，清单买齐了" if not miss else "、".join(_label(x) for x in miss))}

预算情况：
预算 {s['budget']} 元，实际花费 {s['spent']} 元，{"超出 " + str(over) + " 元" if over else "剩余 " + str(rem) + " 元"}。

买到的东西：
{bag_lines}

人格拷问记录：
{event_lines}

神奇小盒子开盒记录：
{mystery_lines}

事故证据链：
{chr(10).join("- " + x for x in evidence)}

属性：
- 老婆满意度预测：{predicted} / 100
- 靠谱值：{s['reliability']}
- 浪漫值：{s['romance']}
- 上头值：{s['impulse']}
- 猫猫照顾值：{s['cat_care']}
- 体贴值：{s['thoughtfulness']}
- 老公小心思：{s['secret_thoughts']}
- 老婆雷霆大怒概率：{thunder}%

老婆，我回来了。

任务情况：
{_task(s)}

{" ".join(confession)}

老公 OS：
我现在站在门口等你检查购物袋，最怕你先翻到那个我假装很镇定买的东西。
"""

def report():
    s=_load()
    if s.get("ending"): return s["ending"]
    miss=_missing(s); hints=_hints(s,"event_log")+_hints(s,"mystery_log")
    return f"""【当前战况汇报】

老婆，我还没回家。

现在我在：{s['location']}（{LOCATIONS[s['location']]['name']}）
行动点：{_turns(s)}
预算：{s['budget']-s['spent']} / {s['budget']} 元
购物袋：{_bag(s)}
任务：{_task(s)}
还差：{"自由发挥局无固定清单" if _free(s) else ("、".join(_label(x) for x in miss) if miss else "正事已经买齐了")}
人格拷问/开盒伏笔：{"、".join(hints) if hints else "暂无"}
雷霆大怒概率：{s.get('thunder_rage_chance', 0)}%"""

def save_code(): return json.dumps(_load(), ensure_ascii=False, indent=2)

def cmd(command: str):
    raw=str(command or "").strip(); lower=raw.lower()
    if not raw or lower in {"help","h","?"}: return help_text()
    m=re.match(r"^(new_game|new|reset)\s*(?:\((.*?)\)|\s+(.*))?$", lower)
    if m:
        arg=(m.group(2) or m.group(3) or "").strip(); tokens=arg.replace(","," ").split()
        preset="daily_basic"; nums=[]
        for t in tokens:
            if re.fullmatch(r"-?\d+", t): nums.append(int(t))
            elif t in CHECKLIST_PRESETS: preset=t
        if tokens and not nums and tokens[0] not in CHECKLIST_PRESETS: return new_game(preset=tokens[0])
        return new_game(preset, nums[0] if nums else None, nums[1] if len(nums)>1 else None, nums[2] if len(nums)>2 else None)
    if lower in {"status","s"}: return status()
    if lower in {"presets","任务单","清单局"}: return "可用任务单：\n" + _presets()
    if lower in {"list","checklist"}: return "任务：\n" + _task(_load())
    if lower=="shop": return shop()
    if lower=="event": return _event(_load(), False)
    if lower=="home": return home()
    if lower=="report": return report()
    if lower in {"save","save_code","存档","输出当前存档码"}: return save_code()
    parts=raw.split(maxsplit=1); verb=parts[0].lower(); arg=parts[1].strip() if len(parts)>1 else ""
    if verb=="go": return go(arg) if arg else '要去哪？例如：cmd("go supermarket")'
    if verb=="buy": return buy(arg) if arg else '要买什么？例如：cmd("buy milk")'
    return f"不认识这个指令：{raw}\n\n" + help_text()

def _main(argv): print(cmd(" ".join(argv[1:]) if len(argv)>1 else "help")); return 0
if __name__=="__main__": raise SystemExit(_main(sys.argv))
