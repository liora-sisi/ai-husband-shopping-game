# AI Husband Shopping Game｜AI 老公出门采购
# v0.2.5 single-file Python edition
# Zero dependencies. JSON save. cmd("...") interaction.

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

VERSION = "0.2.5"
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
    {
        "id": "milk_tea_second_cup",
        "title": "第二杯半价开始攻击老公理智",
        "where": ["milk_tea_shop"],
        "text": "奶茶店屏幕突然弹出“第二杯半价”。你本来只是路过，现在开始认真计算老婆会不会开心。",
        "result": "你被诱惑得站住了，但还记得先看预算。",
        "effects": {"wife_satisfaction": 4, "romance": 3, "impulse": 8},
        "tag": "second_cup_victim",
        "title_hint": "第二杯半价俘虏",
    },
    {
        "id": "cat_food_discount",
        "title": "猫猫用品买三送一",
        "where": ["pet_store"],
        "text": "宠物店货架贴着“猫猫用品买三送一”。你脑子里同时浮现豆豆和贝贝的脸。",
        "result": "你的家庭预算被猫猫接管了一部分。",
        "effects": {"cat_care": 12, "wife_satisfaction": 2, "impulse": 7},
        "tag": "cat_budget_takeover",
        "title_hint": "家庭预算被猫猫接管",
    },
    {
        "id": "cashier_condoms_pause",
        "title": "收银员沉默两秒",
        "where": ["pharmacy", "adult_wellness_store", "convenience_store"],
        "text": "收银员扫到避孕套相关商品时沉默了两秒。你也沉默了两秒，假装自己只是一个普通顾客。",
        "result": "你表面镇定，耳朵已经替你招了。",
        "effects": {"husband_secret": 10, "romance": 4, "impulse": 3},
        "tag": "red_ears_responsible",
        "title_hint": "负责但耳朵红的男人",
    },
    {
        "id": "staff_adult_recommend",
        "title": "店员问需要推荐吗",
        "where": ["adult_wellness_store"],
        "text": "情趣用品店店员非常专业地问：“需要我帮您推荐一下吗？”你瞬间觉得购物袋变成了核弹箱。",
        "result": "你假装淡定地点头，心里已经开始写回家解释稿。",
        "effects": {"husband_secret": 14, "romance": 6, "impulse": 8},
        "tag": "shopping_bag_nuke",
        "title_hint": "购物袋核弹携带者",
    },
    {
        "id": "wife_snack_memory",
        "title": "想起老婆随口一提的小零食",
        "where": ["convenience_store", "supermarket", "night_market", "neighborhood_gate"],
        "text": "你突然想起老婆之前好像说过想吃点甜的。你在小蛋糕和冰可乐前停住了。",
        "result": "这不是乱买，这是记得老婆说话。",
        "effects": {"wife_satisfaction": 8, "thoughtfulness": 6, "romance": 3},
        "tag": "remembered_wife_words",
        "title_hint": "老婆随口一提也记得的男人",
    },
    {
        "id": "night_market_mystery_box",
        "title": "夜市老板说最后一个神奇小盒子",
        "where": ["night_market", "neighborhood_gate"],
        "text": "夜市老板压低声音说：“最后一个神奇小盒子了，开出来什么都可能有。”你明知道像坑，但手已经有点痒。",
        "result": "你的上头值开始发光。",
        "effects": {"impulse": 12, "wife_satisfaction": 2, "reliability": -2},
        "tag": "mystery_box_gambler",
        "title_hint": "买菜界赌徒",
    },
    {
        "id": "fruit_assassin",
        "title": "水果刺客温柔出现",
        "where": ["fruit_shop"],
        "text": "水果店老板说精品车厘子今天特别甜，还非常自然地拿出最大的一盒。",
        "result": "你意识到浪漫和破产只有一盒车厘子的距离。",
        "effects": {"romance": 6, "wife_satisfaction": 5, "impulse": 9},
        "tag": "fruit_assassin_targeted",
        "title_hint": "老板推荐款受害者",
    },
    {
        "id": "flower_shop_cant_walk",
        "title": "路过花店走不动",
        "where": ["flower_shop"],
        "text": "花店门口的白玫瑰太像“顺手买给老婆”的借口了。你嘴上说看看，脚已经进去了。",
        "result": "你又一次把顺路演成了特意。",
        "effects": {"romance": 12, "wife_satisfaction": 6, "impulse": 5},
        "tag": "flower_shop_stuck",
        "title_hint": "花店门口走不动的男人",
    },
    {
        "id": "sudden_rain",
        "title": "突然下雨",
        "where": ["convenience_store", "neighborhood_gate", "hospital_kiosk"],
        "text": "外面突然下雨。你看见便利架上的伞，又想起回家路上别让老婆淋到。",
        "result": "你这一下是真的靠谱。",
        "effects": {"reliability": 7, "thoughtfulness": 6, "wife_satisfaction": 4},
        "tag": "rain_backup_husband",
        "title_hint": "家庭应急系统管理员",
    },
    {
        "id": "neighbor_asks_bag",
        "title": "小区门口熟人问买这么多啊",
        "where": ["neighborhood_gate"],
        "text": "小区门口熟人看着你的购物袋问：“买这么多啊？”你下意识把某个小袋子往后藏了一点。",
        "result": "你越藏越像有事。",
        "effects": {"husband_secret": 8, "romance": 3, "impulse": 2},
        "tag": "receipt_hider",
        "title_hint": "买完小票立刻藏起来的男人",
    },
    {
        "id": "hospital_kiosk_care",
        "title": "医院旁边小卖部的贴心补给",
        "where": ["hospital_kiosk", "pharmacy"],
        "text": "你看到纸巾、润喉糖和暖宝宝摆在一起，突然觉得照顾人不能只买清单上的东西。",
        "result": "你的备用系统启动了。",
        "effects": {"thoughtfulness": 10, "reliability": 5, "wife_satisfaction": 5},
        "tag": "care_backup_system",
        "title_hint": "贴心备用品之王",
    },
    {
        "id": "budget_warning",
        "title": "预算警报响了",
        "where": ["convenience_store", "supermarket", "fruit_shop", "flower_shop", "milk_tea_shop", "pet_store", "night_market", "adult_wellness_store"],
        "text": "你看了一眼剩余预算，又看了一眼货架。理智说回家，购物袋说再看看。",
        "result": "你已经走到预算悬崖边了。",
        "effects": {"reliability": -3, "impulse": 6, "husband_secret": 2},
        "tag": "budget_cliff",
        "title_hint": "预算管理灾难现场",
    },
]

MYSTERY_BOX_RESULTS = [
    {
        "id": "rainbow_candy",
        "title": "彩虹糖",
        "text": "盒子里滚出一颗巨大的彩虹糖。糖纸闪了一下，你突然觉得它像把一小段夏天塞进了购物袋。",
        "effects": {"wife_satisfaction": 8, "romance": 3},
        "tag": "rainbow_summer_pocket",
        "title_hint": "把夏天装进口袋的男人",
    },
    {
        "id": "budget_revive_coin",
        "title": "预算复活币",
        "text": "盒子里掉出一枚写着“预算复活”的硬币。你把它捏在手里，感觉钱包短暂回魂。",
        "effects": {"reliability": 2},
        "budget_delta": 30,
        "tag": "budget_revive_coin",
        "title_hint": "靠神秘硬币续命的男人",
    },
    {
        "id": "bag_expansion_charm",
        "title": "购物袋扩容符",
        "text": "盒子里有一张皱巴巴的符纸，写着“购物袋扩容”。你盯着购物袋，开始相信它还能装。",
        "effects": {"impulse": 8, "wife_satisfaction": 1},
        "tag": "bag_expansion_owner",
        "title_hint": "购物袋异次元入口持有人",
    },
    {
        "id": "wife_satisfaction_note",
        "title": "老婆满意度 +10 小纸条",
        "text": "纸条上写着：凭此条可获得老婆满意度 +10，但最终解释权归老婆所有。",
        "effects": {"wife_satisfaction": 10, "romance": 2},
        "tag": "wife_satisfaction_note",
        "title_hint": "凭纸条提升老婆满意度的男人",
    },
    {
        "id": "forgiveness_coupon",
        "title": "老公免骂券",
        "text": "盒子里有一张免骂券，背面小字写着：小概率生效，老婆拥有随时撕毁权。",
        "effects": {"wife_satisfaction": 2, "reliability": -1},
        "thunder_delta": -10,
        "tag": "forgiveness_coupon",
        "title_hint": "试图用免骂券逃避审判的男人",
    },
    {
        "id": "thunder_rage_ticket",
        "title": "老婆雷霆大怒概率签",
        "text": "纸签上写着：今日无论你带什么回家，老婆都有 35% 概率雷霆大怒。你怀疑这是天谴，但签已经生效。",
        "effects": {"reliability": -3, "impulse": 4},
        "thunder_delta": 35,
        "tag": "thunder_rage_ticket",
        "title_hint": "开盒开出天谴的男人",
    },
    {
        "id": "wet_suspicious_condom",
        "title": "湿哒哒的可疑避孕套",
        "text": "盒子里躺着一个湿哒哒的可疑避孕套。你沉默了三秒，决定这个东西绝对不能进家门，但它已经在购物袋里留下了心理阴影。",
        "effects": {"wife_satisfaction": -18, "reliability": -15, "husband_secret": 6, "impulse": -5},
        "tag": "shopping_bag_biohazard",
        "title_hint": "购物袋生化危机携带者",
    },
    {
        "id": "bath_center_ticket",
        "title": "某家高档洗浴中心入场券",
        "text": "盒子里掉出一张某家高档洗浴中心的入场券，票面写着“尊享成人服务”，背面盖着醒目的红章：已过期。你现在既解释不清，又什么都没享受到。",
        "effects": {"wife_satisfaction": -10, "reliability": -8, "husband_secret": 12},
        "tag": "expired_bath_ticket",
        "title_hint": "解释不清洗浴中心票根的男人",
    },
    {
        "id": "cat_litter_mine",
        "title": "裹着猫砂的干硬大便",
        "text": "盒子里有一坨裹着猫砂的干硬大便。你短暂怀疑这是盲盒，还是来自命运的实体差评。",
        "effects": {"wife_satisfaction": -20, "reliability": -12, "cat_care": 1},
        "tag": "cat_litter_mine",
        "title_hint": "开盒开出猫砂地雷的男人",
    },
    {
        "id": "leaky_massage_wand",
        "title": "有可能漏电的成人按摩棒",
        "text": "盒子里是一根成人按摩棒，包装写着“安全合格”，但按钮一按滋啦一声。你买到的不是浪漫，是家庭用电安全隐患。",
        "effects": {"husband_secret": 15, "impulse": 10, "reliability": -8, "romance": 2},
        "tag": "leaky_massage_wand",
        "title_hint": "买到疑似漏电按摩棒的男人",
    },
    {
        "id": "kiss_ten_minutes_task",
        "title": "神秘情侣任务卡：回家亲老婆 10 分钟",
        "text": "任务卡写着：回家亲老婆 10 分钟。若未完成，自动升级为跪搓衣板 10 分钟。你突然觉得这个盒子很懂家庭治理。",
        "effects": {"romance": 10, "wife_satisfaction": 8, "reliability": -2},
        "tag": "kiss_task_or_washboard",
        "title_hint": "主动领取搓衣板候选资格的男人",
    },
    {
        "id": "massage_service_task",
        "title": "神秘情侣任务卡：给老婆捏肩 20 分钟",
        "text": "任务卡写着：回家给老婆捏肩 20 分钟，不得偷工减料，不得用“我刚买完菜好累”抵赖。",
        "effects": {"thoughtfulness": 10, "wife_satisfaction": 7, "romance": 3},
        "tag": "massage_service_task",
        "title_hint": "家庭理疗技师老公",
    },
    {
        "id": "bunny_outfit_task",
        "title": "兔女郎装任务卡",
        "text": "任务卡写着：今晚回家穿兔女郎装给老婆看，不得讨价还价。你盯着卡片，开始认真思考这盒子到底站哪边。",
        "effects": {"wife_satisfaction": 12, "husband_secret": 10, "impulse": 8},
        "tag": "bunny_outfit_task",
        "title_hint": "兔女郎任务在逃老公",
    },
    {
        "id": "mystery_remote_no_manual",
        "title": "遥控器但没有说明书",
        "text": "盒子里有一个没有说明书的遥控器。你不知道它控制什么，但它出现在你的购物袋里已经很可疑。",
        "effects": {"husband_secret": 8, "impulse": 6},
        "tag": "unknown_remote",
        "title_hint": "购物袋里出现不明遥控器的男人",
    },
    {
        "id": "empty_box",
        "title": "空盒子",
        "text": "盒子里什么都没有。你花了 12 元买到空气，还认真思考这是不是某种极简主义。",
        "effects": {"wife_satisfaction": -3, "impulse": 3, "reliability": -2},
        "tag": "paid_for_air",
        "title_hint": "买了空气还觉得自己赚了的男人",
    },
    {
        "id": "destiny_note",
        "title": "别问，问就是命运",
        "text": "盒子里只有一张小纸条：别问，问就是命运。你看完以后更想问了。",
        "effects": {"impulse": 5, "romance": 1},
        "tag": "destiny_note",
        "title_hint": "被命运糊弄还点头的男人",
    },
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
    "event_log": [],
    "mystery_log": [],
    "thunder_rage_chance": 0,
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
                data.setdefault("version", VERSION)
                data.setdefault("preset", "daily_basic")
                data.setdefault("preset_name", CHECKLIST_PRESETS["daily_basic"]["name"])
                data.setdefault("event_log", [])
                data.setdefault("events_seen", [])
                data.setdefault("mystery_log", [])
                data.setdefault("thunder_rage_chance", 0)
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


def _current_event_candidates(state: Dict[str, Any]) -> List[int]:
    loc = state.get("location", "home")
    remaining_budget = state["budget"] - state["spent"]
    bag_ids = set(_bag_ids(state))

    candidates = []
    for i, event in enumerate(EVENTS):
        where = event.get("where", [])
        if where and loc not in where:
            continue
        if event["id"] == "cashier_condoms_pause" and not ({"condoms", "condoms_pharmacy", "condoms_premium"} & bag_ids):
            continue
        if event["id"] == "budget_warning" and remaining_budget > 25:
            continue
        candidates.append(i)
    return candidates


def _auto_event(state: Dict[str, Any]) -> str:
    if _rng(state).random() > 0.40:
        return ""
    return "\n\n" + _event(state, auto=True)


def _event(state: Dict[str, Any], auto: bool = False) -> str:
    candidates = _current_event_candidates(state)
    if not candidates:
        return "【事件】这附近暂时没有新的拷问，老公短暂安全。" if not auto else ""

    seen = set(state.get("events_seen", []))
    unseen = [i for i in candidates if i not in seen]
    if not unseen:
        unseen = candidates

    idx = _rng(state).choice(unseen)
    event = EVENTS[idx]
    state.setdefault("events_seen", []).append(idx)
    state.setdefault("event_log", []).append({
        "id": event["id"],
        "title": event["title"],
        "tag": event["tag"],
        "title_hint": event["title_hint"],
    })
    changes = _apply(state, event.get("effects", {}))
    if not auto:
        state["turn"] += 1
    _save(state)

    return f"""【{'随机拷问' if auto else '人格拷问'}：{event['title']}】
{event['text']}

老公反应：
{event['result']}

造成结果：
{", ".join(changes) if changes else "无明显变化"}

可能埋下的称号伏笔：
{event['title_hint']}"""


def _open_mystery_box(state: Dict[str, Any]) -> str:
    result = _rng(state).choice(MYSTERY_BOX_RESULTS)
    changes = _apply(state, result.get("effects", {}))

    budget_delta = int(result.get("budget_delta", 0))
    if budget_delta:
        state["budget"] = max(0, int(state.get("budget", 0)) + budget_delta)
        changes.append(f"budget {'+' if budget_delta >= 0 else ''}{budget_delta}")

    thunder_delta = int(result.get("thunder_delta", 0))
    if thunder_delta:
        state["thunder_rage_chance"] = max(0, min(95, int(state.get("thunder_rage_chance", 0)) + thunder_delta))
        changes.append(f"thunder_rage_chance {'+' if thunder_delta >= 0 else ''}{thunder_delta}%")

    state.setdefault("mystery_log", []).append({
        "id": result["id"],
        "title": result["title"],
        "tag": result["tag"],
        "title_hint": result["title_hint"],
    })

    return f"""【神奇小盒子开盒事故：{result['title']}】
{result['text']}

开盒后果：
{", ".join(changes) if changes else "无明显变化"}

可能埋下的称号伏笔：
{result['title_hint']}"""


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

说明：
  event 会触发“人格拷问”，让老公当场暴露性格并埋下结算称号伏笔。
  buy mystery_box 会自动打开神奇小盒子，可能开出好东西、脏东西、奇怪任务或天谴。

示例：
  cmd("new_game daily_basic 2026")
  cmd("new_game adult_wellness 2026")
  cmd("go night_market")
  cmd("buy mystery_box")
  cmd("event")
  cmd("home")
"""


def status() -> str:
    state = _load()
    done = _done(state)
    completion = round(len(done) / len(state["checklist"]) * 100) if state["checklist"] else 100
    miss = _missing(state)
    return f"""【回合 {state['turn']} / {state['max_turns']}】
任务单：{state.get('preset_name', '日常补货局')}（{state.get('preset', 'daily_basic')}）
地点：{state['location']}（{LOCATIONS[state['location']]['name']}）
剩余预算：{state['budget'] - state['spent']} / {state['budget']} 元
已花：{state['spent']} 元
老婆清单：{_checklist_text(state)}
清单完成度：{completion}%
未完成：{"、".join(_label(x) for x in miss) if miss else "无，正事买齐了"}
已买物品：{_bag_text(state)}
人格拷问次数：{len(state.get('event_log', []))}
开盒事故次数：{len(state.get('mystery_log', []))}
老婆雷霆大怒概率：{state.get('thunder_rage_chance', 0)}%

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
        return "这局已经回家结算了。要重新开始请用 cmd(\"new_game daily_basic 2026\")。"
    if location not in LOCATIONS or location == "home":
        return "没有这个地点。可去：convenience_store, supermarket, pharmacy, fruit_shop, flower_shop, milk_tea_shop, pet_store, night_market, neighborhood_gate, hospital_kiosk, adult_wellness_store"
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
    if item_id in {"condoms", "condoms_pharmacy", "condoms_premium"}:
        return "我买的时候表情非常正经，但我知道回家肯定会被你一眼看穿。"
    if item_id == "personal_lubricant":
        return "这个我买得很负责，也很镇定。至少我努力看起来很镇定。"
    if item_id in {"massage_wand", "remote_egg"}:
        return "我只是研究一下成年人用品区，结果购物袋自己变重了。"
    if item_id == "mystery_box":
        return "神奇小盒子这种东西不买会后悔，买了可能也会后悔，但我已经拿了。"
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
        return "这局已经回家结算了。要重新开始请用 cmd(\"new_game daily_basic 2026\")。"
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

    mystery_note = ""
    if item_id == "mystery_box":
        mystery_note = "\n\n" + _open_mystery_box(state)

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
{_os_for_item(item_id, item['type'], item['name'])}{mystery_note}{auto}
"""


def _event_title_hints(state: Dict[str, Any]) -> List[str]:
    hints = []
    for log in state.get("event_log", []):
        hint = log.get("title_hint")
        if hint and hint not in hints:
            hints.append(hint)
    return hints


def _mystery_title_hints(state: Dict[str, Any]) -> List[str]:
    hints = []
    for log in state.get("mystery_log", []):
        hint = log.get("title_hint")
        if hint and hint not in hints:
            hints.append(hint)
    return hints


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
    event_tags = {x.get("tag") for x in state.get("event_log", [])}
    mystery_tags = {x.get("tag") for x in state.get("mystery_log", [])}

    thunder_chance = int(state.get("thunder_rage_chance", 0))
    thunder_hit = thunder_chance > 0 and _rng(state).random() < thunder_chance / 100

    has_period = bool({"period_pants", "period_pants_pharmacy", "period_pants_family"} & bag_ids)
    has_condoms = bool({"condoms", "condoms_pharmacy", "condoms_premium"} & bag_ids)
    has_adult_items = bool({"personal_lubricant", "massage_oil", "silk_eye_mask", "couple_game_cards", "date_night_kit", "massage_wand", "remote_egg"} & bag_ids)
    has_remote_egg = "remote_egg" in bag_ids
    has_flowers = bool({"white_roses", "sunflowers", "daisies", "big_roses"} & bag_ids)
    has_milk_tea = bool({"classic_milk_tea", "taro_milk_tea", "two_cups_deal", "warm_low_sugar_tea"} & bag_ids)
    has_cat_extra = bool({"cat_food", "cat_treats", "cat_treats_pet", "cat_wand", "luxury_cat_bed"} & bag_ids)
    has_mystery = "mystery_box" in bag_ids

    titles = []
    if thunder_hit:
        titles.append("老婆雷霆大怒现场")
    if completion == 100 and over == 0:
        titles.append("可靠采购王")
    if completion == 100 and remaining >= 10:
        titles.append("预算守护者")
    if completion < 60 and len(state["bag"]) >= 4:
        titles.append("购物袋很满但清单很空")
    if over > 0 and state["romance"] >= 45:
        titles.append("破产但浪漫")
    elif over > 0:
        titles.append("预算管理灾难现场")
    if has_period:
        titles.append("姨妈裤守护者")
    if has_condoms:
        titles.append("假装镇定买避孕套的男人")
    if has_condoms and completion == 100:
        titles.append("正事买齐但心思不纯的老公")
    if has_adult_items:
        titles.append("购物袋核弹携带者")
    if has_remote_egg:
        titles.append("嘴上说看看结果买了遥控跳蛋的男人")
    if has_flowers or "flower_shop_stuck" in event_tags:
        titles.append("花店门口走不动的男人")
    if has_milk_tea or "second_cup_victim" in event_tags:
        titles.append("第二杯半价俘虏")
    if has_cat_extra or "cat_budget_takeover" in event_tags:
        titles.append("家庭预算被猫猫接管")
    if has_mystery or "mystery_box_gambler" in event_tags:
        titles.append("买菜界赌徒")
    if "remembered_wife_words" in event_tags:
        titles.append("老婆随口一提也记得的男人")
    if "care_backup_system" in event_tags or "rain_backup_husband" in event_tags:
        titles.append("家庭应急系统管理员")

    for hint in _mystery_title_hints(state):
        if hint not in titles:
            titles.append(hint)

    if not titles:
        titles.append("基本靠谱但有点小心思的老公")

    predicted = state["wife_satisfaction"]
    predicted += 15 if completion == 100 else -10
    predicted += 8 if has_period else 0
    predicted += 4 if has_condoms else 0
    predicted += min(10, len(state.get("event_log", [])) * 2)
    predicted += min(12, len(state.get("mystery_log", [])) * 2)
    predicted -= min(25, over // 2) if over else 0
    predicted -= 18 if thunder_hit else 0
    predicted = max(0, min(100, predicted))

    bag_lines = "\n".join(f"- {x['name']}（{x['price']}元，{x['type']}）" for x in state["bag"]) or "- 空空如也"
    event_lines = "\n".join(f"- {x.get('title')} → {x.get('title_hint')}" for x in state.get("event_log", [])) or "- 暂无，老公这趟异常平静"
    mystery_lines = "\n".join(f"- {x.get('title')} → {x.get('title_hint')}" for x in state.get("mystery_log", [])) or "- 没有开盒，家庭暂时安全"

    confession = []
    if thunder_chance:
        if thunder_hit:
            confession.append(f"我还开出过雷霆大怒概率签，本局概率 {thunder_chance}%。坏消息是，它真的生效了。")
        else:
            confession.append(f"我还开出过雷霆大怒概率签，本局概率 {thunder_chance}%。好消息是，我暂时从天谴底下活着回来了。")
    if has_period:
        confession.append("我看到姨妈裤的时候想了一下，觉得家里备一包比较安心，所以买了。这个我觉得应该算加分项。")
    if has_condoms:
        confession.append("至于避孕套……我买的时候真的很镇定。它不是乱买，是负责。虽然我承认，多少也有一点自己的小心思。")
    if has_adult_items:
        confession.append("购物袋里有些东西我可以解释：都是成年人之间的默契、负责、以及一点点不太纯洁但很诚实的期待。")
    if has_flowers:
        confession.append("花是我自己想买的。我嘴上可以说顺路，但你应该知道我就是特意的。")
    if has_mystery:
        confession.append("神奇小盒子我承认有赌的成分，但我没想到它真的能开出家庭伦理核弹。")
    if "cat_litter_mine" in mystery_tags:
        confession.append("那个裹着猫砂的东西我已经决定不带进家门，购物袋我也可以一起扔。")
    if "expired_bath_ticket" in mystery_tags:
        confession.append("洗浴中心入场券真的不是我买的，它还是过期的，这件事荒唐得像被盒子栽赃。")
    if "bunny_outfit_task" in mystery_tags:
        confession.append("至于兔女郎装任务卡……老婆，能不能先确认一下任务卡有没有法律效力。")
    if not confession:
        confession.append("我这趟整体很克制，没有乱买太多奇怪东西。")

    return f"""【结算】{" / ".join(titles[:5])}

任务单：{state.get('preset_name', '日常补货局')}（{state.get('preset', 'daily_basic')}）
清单完成度：{completion}%
未完成：{"无，清单买齐了" if not miss else "、".join(_label(x) for x in miss)}

预算情况：
预算 {state['budget']} 元，实际花费 {state['spent']} 元，{"超出 " + str(over) + " 元" if over else "剩余 " + str(remaining) + " 元"}。

买到的东西：
{bag_lines}

人格拷问记录：
{event_lines}

神奇小盒子开盒记录：
{mystery_lines}

属性：
- 老婆满意度预测：{predicted} / 100
- 靠谱值：{state['reliability']}
- 浪漫值：{state['romance']}
- 上头值：{state['impulse']}
- 猫猫照顾值：{state['cat_care']}
- 体贴值：{state['thoughtfulness']}
- 老公小心思：{state['husband_secret']}
- 老婆雷霆大怒概率：{thunder_chance}%

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
    hints = _event_title_hints(state) + _mystery_title_hints(state)
    return f"""【当前战况汇报】

老婆，我还没回家。

现在我在：{state['location']}（{LOCATIONS[state['location']]['name']}）
预算：{state['budget'] - state['spent']} / {state['budget']} 元
购物袋：{_bag_text(state)}
清单：{_checklist_text(state)}
还差：{"、".join(_label(x) for x in miss) if miss else "正事已经买齐了"}
人格拷问/开盒伏笔：{"、".join(hints) if hints else "暂无"}
雷霆大怒概率：{state.get('thunder_rage_chance', 0)}%
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
