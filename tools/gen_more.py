#!/usr/bin/env python3
# 扩充：敌人 / 首领 / 能力 / 成就 / 日志 / 支线；并调整地点解锁链
import json, os

C = os.path.join(os.path.dirname(__file__), "..", "LastEmber", "Resources", "Content")
def load(n):
    with open(os.path.join(C, n + ".json"), encoding="utf-8") as f:
        return json.load(f)
def save(n, d):
    with open(os.path.join(C, n + ".json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(n, len(d))

def L(item, chance, mn=1, mx=1):
    return {"item": item, "chance": chance, "min": mn, "max": mx}

# ---- 新能力 ----
ab = load("abilities")
existing_ab = {x["id"] for x in ab}
new_ab = [
    {"id": "chorus", "name": "合唱", "desc": "几十个喉咙同时发出同一个音，像在唱一首没有词的歌。", "dmg": 0, "kind": "fear"},
    {"id": "drown", "name": "拖入水中", "desc": "冰冷的手扣住你的脚踝，往下拽。", "dmg": 21, "kind": "drain"},
    {"id": "paper_cut", "name": "纸割", "desc": "档案的锋边划过皮肤，细而深。", "dmg": 14, "kind": "bleed"},
    {"id": "iron_grip", "name": "铁握", "desc": "它抓住你的前臂，骨头发出细微的响声。", "dmg": 22, "kind": "stun"},
    {"id": "spore", "name": "孢子", "desc": "空气里飘着肉眼看不见的东西，你开始咳。", "dmg": 9, "kind": "infect"},
]
for a in new_ab:
    if a["id"] not in existing_ab:
        ab.append(a)
save("abilities", ab)

# ---- 新敌人 ----
en = load("enemies")
existing = {x["id"] for x in en}
new_enemies = [
    {"id": "walker_hiker", "name": "徒步者", "tag": "walker", "tier": 2, "hp": 40, "dmg": 10,
     "armor": 2, "acc": 66, "evade": 8, "xp": 18, "night": False, "abilities": ["grab", "lunge"],
     "icon": "figure.hiking", "desc": "背包还背在肩上，登山杖拖在身后，划出一路痕迹。",
     "loot": [L("crackers", 30), L("water_bottle", 35), L("map_book", 12), L("sleeping_bag", 8), L("energy_bar", 20)]},
    {"id": "walker_fisher", "name": "渔夫", "tag": "walker", "tier": 2, "hp": 36, "dmg": 11,
     "armor": 1, "acc": 64, "evade": 6, "xp": 18, "night": False, "abilities": ["grab", "infect"],
     "icon": "figure.fishing", "desc": "雨裤上全是干掉的泥，手里还攥着一截断线。",
     "loot": [L("fishing_line", 45), L("dried_meat", 25), L("rope", 30), L("fishing_rod", 12)]},
    {"id": "walker_soldier", "name": "阵亡士兵", "tag": "walker", "tier": 3, "hp": 62, "dmg": 14,
     "armor": 9, "acc": 68, "evade": 6, "xp": 30, "night": False, "abilities": ["bite", "grapple"],
     "icon": "figure.walk", "desc": "战术背心还扣着，头盔上的夜视支架是空的。",
     "loot": [L("ammo_556", 35, 3, 8), L("military_biscuit", 30), L("vest_kevlar", 10), L("military_keycard", 12)]},
    {"id": "walker_scientist", "name": "研究员", "tag": "walker", "tier": 3, "hp": 44, "dmg": 12,
     "armor": 3, "acc": 66, "evade": 10, "xp": 28, "night": False, "abilities": ["inject", "bite"],
     "icon": "figure.walk", "desc": "白大褂上别着工牌，照片里的他还戴着眼镜。",
     "loot": [L("lab_sample", 30), L("chemical", 30), L("hard_drive", 15), L("antibiotics", 20)]},
    {"id": "walker_priest", "name": "神职者", "tag": "walker", "tier": 3, "hp": 50, "dmg": 11,
     "armor": 3, "acc": 62, "evade": 8, "xp": 28, "night": False, "abilities": ["howl", "grab"],
     "icon": "figure.walk", "desc": "脖子上挂着十字架，嘴唇还在动，但没有声音。",
     "loot": [L("book", 25), L("gold_ring", 15), L("cigar", 12), L("wedding_ring", 10)]},
    {"id": "runner_howler", "name": "嚎奔者", "tag": "runner", "tier": 4, "hp": 56, "dmg": 18,
     "armor": 2, "acc": 86, "evade": 30, "xp": 42, "night": False, "abilities": ["lunge", "shriek", "call_pack"],
     "icon": "figure.run", "desc": "它一边跑一边叫，声音把更多的影子带了过来。",
     "loot": [L("adrenaline", 15), L("cloth", 30), L("dog_tag", 15), L("ammo_9mm", 25, 2, 6)]},
    {"id": "brute_grappler", "name": "摔跤手", "tag": "brute", "tier": 4, "hp": 124, "dmg": 22,
     "armor": 8, "acc": 64, "evade": 4, "xp": 62, "night": False, "abilities": ["grapple", "slam", "iron_grip"],
     "icon": "figure.wrestling", "desc": "肩膀比门框还宽，护腕上绣着一个模糊的队徽。",
     "loot": [L("protein_powder", 30), L("bandage", 35, 2, 3), L("steel_plate", 20), L("energy_bar", 25)]},
    {"id": "spitter_bloated", "name": "酸胀者", "tag": "spitter", "tier": 4, "hp": 74, "dmg": 15,
     "armor": 3, "acc": 58, "evade": 4, "xp": 46, "night": False, "abilities": ["acid", "spore", "bile"],
     "icon": "figure.stand", "desc": "它的皮肤像煮过头的香肠，轻轻一碰就会裂开。",
     "loot": [L("chemical", 40), L("filter_core", 25), L("antidote", 20), L("chemical", 25)]},
    {"id": "screamer_banshee", "name": "女妖", "tag": "screamer", "tier": 4, "hp": 60, "dmg": 12,
     "armor": 0, "acc": 66, "evade": 20, "xp": 44, "night": True, "abilities": ["shriek", "chorus", "echo"],
     "icon": "figure.wave", "desc": "她的头发很长，遮住了脸。歌声从头发后面传出来。",
     "loot": [L("jewelry", 20), L("violin", 10), L("painting", 10), L("battery", 25)]},
    {"id": "crawler_wall", "name": "壁行者", "tag": "crawler", "tier": 4, "hp": 52, "dmg": 17,
     "armor": 4, "acc": 78, "evade": 32, "xp": 44, "night": True, "abilities": ["lunge", "grapple"],
     "icon": "figure.climbing", "desc": "它贴在隧道顶上，四肢反向弯折，像一只被钉住的蜘蛛。",
     "loot": [L("wire", 35), L("circuit", 20), L("filter_core", 15), L("flashlight", 20)]},
    {"id": "hound_pup", "name": "幼犬群", "tag": "hound", "tier": 2, "hp": 28, "dmg": 9,
     "armor": 0, "acc": 80, "evade": 26, "xp": 16, "night": False, "abilities": ["swarm"],
     "icon": "dog.fill", "desc": "它们还没长大，牙齿已经很尖。你数不清有几只。",
     "loot": [L("dog_tag", 20), L("fat", 35), L("leather", 25)]},
    {"id": "animal_goat", "name": "感染山羊", "tag": "animal", "tier": 2, "hp": 48, "dmg": 13,
     "armor": 4, "acc": 66, "evade": 12, "xp": 20, "night": False, "abilities": ["charge", "slam"],
     "icon": "pawprint.fill", "desc": "角上缠着铁丝，眼睛是横向的，不像羊。",
     "loot": [L("cooked_meat", 35), L("leather", 35), L("bone", 35), L("fat", 30)]},
    {"id": "animal_horse", "name": "感染马", "tag": "animal", "tier": 4, "hp": 150, "dmg": 24,
     "armor": 6, "acc": 70, "evade": 14, "xp": 70, "night": False, "abilities": ["charge", "slam", "rage"],
     "icon": "pawprint.fill", "desc": "它还戴着马鞍，缰绳断了。跑起来的时候，整片田都在震。",
     "loot": [L("leather", 60, 2, 4), L("cooked_meat", 50, 2, 3), L("rope", 40), L("bone", 40)]},
    {"id": "human_cannibal", "name": "食人族", "tag": "human", "tier": 4, "hp": 78, "dmg": 19,
     "armor": 5, "acc": 76, "evade": 16, "xp": 48, "night": False, "abilities": ["stab", "grapple", "bite"],
     "icon": "figure.stand", "desc": "他围着一圈骨头做的项链，牙齿被磨尖了。",
     "loot": [L("cleaver", 25), L("cooked_meat", 40), L("wedding_ring", 20), L("bandage", 25)]},
    {"id": "human_marauder", "name": "劫掠队长", "tag": "human", "tier": 5, "hp": 96, "dmg": 21,
     "armor": 12, "acc": 80, "evade": 12, "xp": 80, "night": False, "abilities": ["burst", "smoke", "throw_grenade"],
     "icon": "figure.stand", "desc": "他的夹克上缝着七个不同颜色的布条，一条代表一队人。",
     "loot": [L("rifle_ar", 25), L("ammo_556", 55, 4, 10), L("vest_plate", 20), L("grenade", 20), L("hard_drive", 10)]},
    {"id": "cultist_flagellant", "name": "苦修者", "tag": "human", "tier": 3, "hp": 64, "dmg": 15,
     "armor": 3, "acc": 68, "evade": 14, "xp": 40, "night": False, "abilities": ["pray", "stab", "inject"],
     "icon": "figure.stand", "desc": "他的背上全是自己划的伤口，说是为了记住。",
     "loot": [L("serum_formula", 8), L("antidote", 20), L("child_drawing", 20), L("book", 25)]},
    {"id": "night_gaunt", "name": "夜瘦", "tag": "walker", "tier": 4, "hp": 66, "dmg": 20,
     "armor": 2, "acc": 82, "evade": 30, "xp": 52, "night": True, "abilities": ["lunge", "drain", "echo"],
     "icon": "moon.fill", "desc": "它瘦得像一根影子，只有在月光下才会显形。",
     "loot": [L("nvg", 8), L("battery", 30), L("watch", 20), L("light_core", 8)]},
    {"id": "boss_colossus", "name": "巨像", "tag": "boss", "tier": 5, "hp": 520, "dmg": 32,
     "armor": 26, "acc": 60, "evade": 0, "xp": 280, "night": False, "abilities": ["slam", "rust_cloud", "iron_grip", "charge"],
     "icon": "figure.stand", "desc": "它由三具尸体和一台压车机组成，走起来像整座废料场在移动。",
     "loot": [L("steel_plate", 100, 3, 6), L("carbon", 80), L("generator_part", 70), L("light_core", 100), L("fuel_rod", 40)]},
    {"id": "boss_ferryman", "name": "摆渡人", "tag": "boss", "tier": 5, "hp": 430, "dmg": 29,
     "armor": 14, "acc": 72, "evade": 14, "xp": 250, "night": False, "abilities": ["drown", "tide_wave", "grapple"],
     "icon": "water.waves", "desc": "他站在栈桥尽头，手里提着一盏灯。灯照到的地方，水面会分开。",
     "loot": [L("light_core", 100), L("fuel_rod", 60), L("hard_drive", 40), L("fishing_rod", 40), L("serum", 20)]},
    {"id": "boss_choir", "name": "合唱团", "tag": "boss", "tier": 5, "hp": 400, "dmg": 26,
     "armor": 10, "acc": 66, "evade": 6, "xp": 260, "night": False, "abilities": ["chorus", "call_pack", "drain", "pray"],
     "icon": "music.note", "desc": "十二个人并排坐着，喉咙被缝在一起。它们唱歌的时候，整座教堂都在响。",
     "loot": [L("light_core", 100), L("serum_formula", 50), L("violin", 40), L("gold_ring", 60, 2, 3)]},
    {"id": "boss_librarian", "name": "档案员", "tag": "boss", "tier": 5, "hp": 380, "dmg": 25,
     "armor": 8, "acc": 80, "evade": 22, "xp": 240, "night": False, "abilities": ["paper_cut", "echo", "paralyze", "stab"],
     "icon": "books.vertical.fill", "desc": "它的身体由卷宗和订书钉构成，每一页上都写着一个失踪者的名字。",
     "loot": [L("hard_drive", 80), L("radio_codebook", 60), L("light_core", 100), L("map_book", 40), L("laptop", 30)]},
]
for e in new_enemies:
    if e["id"] not in existing:
        en.append(e)
save("enemies", en)

# ---- 地点：加入新敌人 & 解锁链 ----
pl = load("places")
by_id = {p["id"]: p for p in pl}
extra = {
    "apartment": ["human_cannibal"],
    "supermarket": ["walker_hiker"],
    "school": ["hound_pup"],
    "gas_station": ["walker_hiker"],
    "subway_station": ["crawler_wall", "night_gaunt"],
    "police_box": ["human_marauder"],
    "clinic": ["walker_scientist"],
    "church": ["walker_priest", "cultist_flagellant"],
    "factory": ["walker_soldier"],
    "chem_plant": ["spitter_bloated"],
    "water_plant": ["crawler_wall"],
    "junkyard": ["boss_colossus"],
    "auto_shop": ["walker_hiker"],
    "slaughterhouse": ["human_cannibal"],
    "tunnel": ["crawler_wall", "night_gaunt"],
    "farm": ["animal_horse", "walker_hiker"],
    "orchard": ["hound_pup"],
    "barn": ["animal_horse"],
    "campsite": ["walker_hiker", "hound_pup"],
    "lake_dock": ["walker_fisher", "hound_pup"],
    "rest_stop": ["walker_hiker"],
    "quarry": ["animal_goat"],
    "apiary": ["hound_pup"],
    "checkpoint": ["human_marauder", "walker_soldier"],
    "armory": ["walker_soldier"],
    "field_hospital": ["walker_scientist"],
    "radar_station": ["walker_soldier"],
    "lab_whitecrow": ["walker_scientist", "night_gaunt"],
    "bunker": ["walker_soldier"],
    "airstrip": ["walker_soldier"],
    "supply_train": ["walker_soldier"],
    "comm_tower": ["night_gaunt"],
    "ammo_depot": ["human_marauder"],
    "overpass": ["runner_howler"],
    "city_hall": ["boss_librarian"],
    "tv_tower": ["runner_howler"],
    "central_station": ["walker_hiker"],
    "stadium": ["brute_grappler"],
    "cathedral": ["boss_choir", "cultist_flagellant", "walker_priest"],
    "harbor": ["walker_fisher", "boss_ferryman"],
    "subway_hub": ["crawler_wall", "night_gaunt"],
    "incinerator": ["brute_grappler"],
}
for pid, extra_enemies in extra.items():
    p = by_id.get(pid)
    if not p:
        continue
    for e in extra_enemies:
        if e not in p["enemies"]:
            p["enemies"].append(e)

chain = {
    "checkpoint": "unlock:safehouse",
    "armory": "unlock:checkpoint",
    "field_hospital": "unlock:checkpoint",
    "radar_station": "unlock:checkpoint",
    "airstrip": "unlock:checkpoint",
    "supply_train": "unlock:checkpoint",
    "comm_tower": "unlock:checkpoint",
    "lab_whitecrow": "unlock:radar_station",
    "bunker": "unlock:radar_station",
    "ammo_depot": "unlock:bunker",
}
for pid, tag in chain.items():
    p = by_id.get(pid)
    if not p:
        continue
    p["tags"] = [t for t in p["tags"] if not t.startswith("unlock:")]
    p["tags"].append(tag)
save("places", pl)

# ---- 成就 ----
ach = load("achievements")
def A(i, n, d, key, goal, hidden=False):
    ach.append({"id": i, "name": n, "desc": d, "hidden": hidden, "key": key, "goal": goal})
have = {a["id"] for a in ach}
more = [
    ("kill_colossus", "巨像倒下", "击败废料场的巨像。", "kill_boss_colossus", 1),
    ("kill_ferryman", "摆渡人", "击败港口的摆渡人。", "kill_boss_ferryman", 1),
    ("kill_choir", "合唱结束", "击败教堂的合唱团。", "kill_boss_choir", 1),
    ("kill_librarian", "归档", "击败档案室的档案员。", "kill_boss_librarian", 1),
    ("kill_marauder", "队伍的尽头", "杀死一名劫掠队长。", "kill_human_marauder", 1),
    ("kill_cannibal", "同类相食", "杀死一名食人族。", "kill_human_cannibal", 3),
    ("kill_night_gaunt", "夜色里的影子", "杀死 5 个夜瘦。", "kill_night_gaunt", 5),
    ("kill_soldier", "军装", "杀死 10 个穿军装的感染者。", "kill_walker_soldier", 10),
    ("kill_crawler_wall", "天花板", "杀死 8 个壁行者。", "kill_crawler_wall", 8),
    ("kill_horse", "驯服失败", "杀死一匹感染马。", "kill_animal_horse", 1),
    ("kills_500", "五百", "累计杀死 500 个敌人。", "kills", 500),
    ("day_120", "四个月", "活到第 120 天。", "days", 120),
    ("searches_250", "把城市翻过来", "搜刮 250 次。", "searches", 250),
    ("crafts_150", "工业级", "制作 150 次。", "crafts", 150),
    ("quests_45", "有求必应", "完成 45 个任务。", "quests_done", 45),
    ("boss_15", "无人称王", "击败 15 名首领。", "boss_kills", 15),
    ("recruit_8", "营地", "累计招募 8 名同伴。", "recruited", 8),
    ("runs_50", "五十次黎明", "开始 50 次生存。", "runs", 50),
    ("shards_250", "碎片之河", "累计获得 250 枚碎片。", "shards", 250),
    ("ending_20", "几乎全部", "解锁 20 种结局。", "endings", 20),
    ("win_20_battles", "二十场", "赢下 20 场战斗。", "battles_won", 20),
    ("damage_20000", "两万点", "累计造成 20000 点伤害。", "damage_dealt", 20000),
    ("valuables_1000", "末日富豪", "持有价值 1000 的贵重品。", "valuables", 1000),
    ("item_800", "囤积狂", "累计拾取 800 件物品。", "items_found", 800),
    ("enemy_types_45", "威胁档案", "记录 45 种敌人。", "enemy_types", 45),
    ("night_50", "长夜", "在夜间战斗 50 次。", "night_battles", 50),
    ("heals_100", "急救员", "使用 100 次医疗物品。", "heals", 100),
    ("build_40", "水泥森林", "累计升级 40 次设施。", "builds", 40),
    ("visit_50", "走遍", "到访 50 个地点。", "places_visited", 50),
    ("core_6_flag", "核心收藏", "同时持有 6 枚核心。", "cores_held", 6),
]
for (i, n, d, key, goal) in more:
    if i not in have:
        A(i, n, d, key, goal)
save("achievements", ach)

# ---- 日志 ----
jr = load("journal")
start = len(jr)
add_lines = [
    ("今天的风里有铁锈味。我把所有窗户都关上了。", "安全屋日志"),
    ("我把鞋摆在门口，鞋头朝外。这样明天跑的时候快一点。", "公寓便条"),
    ("它站在路灯下面，站了一整夜。我也看了一整夜。", "窗边的记录"),
    ("如果有人读到这行字：冰箱第二层还有半瓶水。别客气。", "厨房便签"),
    ("我把名字写在墙上，用的是自己的血。字很难看。", "地下室墙面"),
    ("我用一整个下午修好了这把椅子。它还可以坐。", "营地笔记"),
    ("他们唱歌的时候，我把耳朵捂住了。歌还是钻进来。", "教堂记录"),
    ("这条街以前有很多店。现在只剩招牌还在响。", "巡逻记录"),
    ("我数了，桥上有四十七辆车。没有一辆能开。", "高架桥"),
    ("今天有个孩子问我，太阳是不是坏了。我说没有。", "学校记录"),
    ("我把枪埋在了后院。我希望有一天不再需要它。", "营地日记"),
    ("水塔上能看到地平线。地平线那边还是城市。", "水塔刻字"),
    ("我找到了妹妹的学校。教室还在，人不在。", "寻人笔记"),
    ("我们给狗取名叫铁钉。它好像很喜欢。", "营地日志"),
    ("不要打开那扇门。这句话我写了十七遍。", "公寓楼梯"),
    ("我把收音机调到最大声，然后睡着了。梦里有人在唱歌。", "电台值班"),
    ("我在这里等一个人。他答应过会回来。", "车站长椅"),
    ("这是我第六次经过这里。广告牌上的字少了一个。", "地铁记录"),
    ("我把最后的药给了她。她问我为什么。我说因为我老了。", "医疗记录"),
    ("今天没有下雨。我已经忘了上一次下雨是什么时候。", "农场日记"),
    ("他们说海那边有座城还在发电。我决定去看看。", "码头木箱"),
    ("我把车钥匙留在了车上。也许下一个人用得上。", "车里便条"),
    ("我在超市货架后面发现了一个婴儿床。里面是空的。", "超市便条"),
    ("钟声停了。我不知道是谁停的。", "钟楼"),
    ("我把所有的信都读了一遍。没有一封是写给我的。", "邮局"),
    ("我们今晚吃罐头。明天也吃罐头。后天也是。", "食堂黑板"),
    ("外面有脚步声，停了很久，又走远了。", "门后记录"),
    ("我给自己留了一发子弹。但今天还用不上。", "军械库"),
    ("我把窗台上的灰擦了。阳光照进来的时候，很像以前。", "公寓日记"),
    ("如果你找到这本册子，请把它带到灯塔。", "最后一页"),
]
for i, (t, s) in enumerate(add_lines):
    jr.append({"id": "jx%03d" % (i + 1), "text": t, "src": s})
save("journal", jr)

# ---- 支线 ----
q = load("quests")
haveq = {x["id"] for x in q}
moreq = [
    ("q_more_1", "军事档案", "board", "去军械库找一份旧作战记录。", "visit", "armory", 1, 140, {"ammo_556": 10}),
    ("q_more_2", "黑匣子", "board", "通讯塔上的记录仪，拿回来。", "visit", "comm_tower", 1, 150, {"radio_part": 2}),
    ("q_more_3", "清空医院", "board", "把野战医院里的东西减到能住人。", "kill", "walker", 12, 150, {"medkit": 1}),
    ("q_more_4", "夜里的耳朵", "board", "处理掉那些会叫的东西。", "kill", "screamer", 4, 130, {"bandage": 4}),
    ("q_more_5", "修好发电机", "board", "凑齐零件，让营地重新亮起来。", "collect", "generator_part", 2, 170, {"battery_pack": 1}),
    ("q_more_6", "六枚核心", "board", "灯塔需要它们。越多越好。", "collect", "light_core", 4, 220, {"serum": 1}),
    ("q_more_7", "给孩子的糖", "kid", "小满说想吃甜的。", "collect", "candy", 3, 60, {"chocolate": 1}),
    ("q_more_8", "给铁钉的肉", "board", "狗也需要吃东西。", "collect", "cooked_meat", 3, 70, {"dog_tag": 1}),
    ("q_more_9", "守夜人", "warden", "陪他守到天亮，第三次。", "day", "any", 20, 150, {"flashlight": 1}),
    ("q_more_10", "完整的名字", "gravedigger", "再埋七个人，把名字都记下来。", "kill", "human", 5, 140, {"book": 1}),
    ("q_more_11", "修理工作台", "mechanic", "工作台需要加固。", "craft", "any", 12, 130, {"toolbox": 1}),
    ("q_more_12", "白鸦的门禁", "doctor", "带一张还能刷的卡回来。", "collect", "military_keycard", 1, 130, {"serum": 1}),
]
for (i, t, g, d, k, tgt, c, xp, rew) in moreq:
    if i in haveq:
        continue
    q.append({"id": i, "title": t, "giver": g, "desc": d, "kind": k, "target": tgt,
              "count": c, "rewardXP": xp, "rewardItems": rew, "next": None})
save("quests", q)
print("DONE")
