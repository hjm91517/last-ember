#!/usr/bin/env python3
# 生成 perks / buildings / endings / npcs / quests / achievements / journal
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "LastEmber", "Resources", "Content")

def save(name, data):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{name}: {len(data)}")

def P(i, n, branch, tier, maxr, desc, eff):
    return {"id": i, "name": n, "branch": branch, "tier": tier, "maxRank": maxr,
            "desc": desc, "effect": eff}

perks = [
    # 战斗
    P("brawler", "街头斗殴", "combat", 1, 3, "在巷子里学会的，比训练场管用。", {"dmg": 2}),
    P("marksman", "枪法", "combat", 1, 3, "呼吸、准星、扣扳机。顺序不能乱。", {"acc": 4}),
    P("shield_wall", "铁壁", "combat", 2, 2, "挨打也是一种本事。", {"hpMax": 8}),
    P("brutal", "野蛮", "combat", 2, 2, "用最省事的方式结束战斗。", {"dmg": 3, "crit": 2}),
    P("quick_draw", "快拔", "combat", 2, 2, "先出手的人活下来。", {"acc": 3, "flee": 5}),
    P("steady_aim", "稳定瞄准", "combat", 2, 2, "手不抖，是因为你不再害怕。", {"acc": 5}),
    P("iron_fist", "铁拳", "combat", 3, 2, "关节上全是老茧。", {"dmg": 4, "hpMax": 4}),
    P("executioner", "处决者", "combat", 3, 2, "你知道该往哪里下手。", {"crit": 6}),
    P("deadeye", "鹰眼", "combat", 3, 2, "一百米外，风偏三指。", {"crit": 8, "acc": 3}),
    P("butcher", "屠夫", "combat", 2, 2, "分解过太多东西，知道骨头在哪里。", {"dmg": 3, "crit": 2}),
    P("berserk", "狂怒", "combat", 4, 1, "当恐惧用完之后，剩下的是怒火。", {"dmg": 7, "flee": -5}),
    # 生存
    P("scrounger", "拾荒眼", "survival", 1, 3, "垃圾堆里也有活路。", {"scavenge": 6}),
    P("pack_mule", "负重", "survival", 1, 3, "背得动，才走得远。", {"carry": 8}),
    P("light_step", "轻步", "survival", 1, 3, "踩下去之前先想好落点。", {"stealth": 6, "flee": 4}),
    P("field_medic", "战地医疗", "survival", 2, 3, "止血、固定、抗感染。", {"heal": 5, "infectResist": 8}),
    P("iron_stomach", "铁胃", "survival", 2, 2, "什么都吃得下，什么都扛得住。", {"hpMax": 5, "infectResist": 6}),
    P("camper", "露营者", "survival", 2, 2, "任何地方都能睡一觉。", {"heal": 3, "sanity": 2}),
    P("water_finder", "找水人", "survival", 2, 2, "水比子弹重要。", {"scavenge": 4, "sanity": 1}),
    P("silent", "静默", "survival", 3, 2, "你走过的地方，连灰都不动。", {"stealth": 8}),
    P("tough", "硬汉", "survival", 3, 2, "疼归疼，路还是要走。", {"hpMax": 10}),
    P("survivor", "老手", "survival", 3, 2, "你已经活过了大多数人。", {"hpMax": 6, "infectResist": 6}),
    P("lucky", "幸运", "survival", 4, 1, "有些人就是运气好。", {"sanity": 3, "scavenge": 3}),
    # 技术
    P("handy", "巧手", "tech", 1, 3, "给你一堆垃圾，你能造出点什么。", {"craft": 1}),
    P("tinker", "修补匠", "tech", 1, 3, "坏了就修，修不好就拆。", {"craft": 1, "heal": 2}),
    P("salvager", "拆解师", "tech", 2, 2, "一架废车能拆出三十种零件。", {"scavenge": 4, "carry": 4}),
    P("locksmith", "锁匠", "tech", 2, 2, "锁只是耐心的问题。", {"scavenge": 5}),
    P("grease_monkey", "机修工", "tech", 2, 2, "手上永远洗不干净的油。", {"craft": 1, "carry": 4}),
    P("demolisher", "爆破手", "tech", 2, 2, "炸药是万能钥匙。", {"craft": 1, "dmg": 2}),
    P("medic_tech", "器械医", "tech", 3, 2, "会用缝合包，也会修输液泵。", {"heal": 6}),
    P("night_owl", "夜猫子", "tech", 3, 2, "黑暗里反而看得更清楚。", {"stealth": 4, "sanity": 2}),
    P("gunsmith", "枪匠", "tech", 3, 2, "枪是工具，工具需要保养。", {"craft": 1, "acc": 2}),
    P("quartermaster", "军需官", "tech", 4, 1, "你知道每样东西该放在哪。", {"carry": 12}),
    P("engineer", "总工程师", "tech", 4, 1, "给你一座废墟，你能让它亮起来。", {"craft": 2, "scavenge": 3}),
    # 意志
    P("zeal", "狂热", "will", 1, 3, "信念能挡住一些东西。", {"sanity": 4, "hpMax": 4}),
    P("stubborn", "固执", "will", 1, 3, "别人都倒下了，你还站着。", {"hpMax": 8}),
    P("calm", "冷静", "will", 1, 3, "数到十，再做决定。", {"sanity": 5, "crit": 1}),
    P("faith", "信仰", "will", 2, 2, "灰烬之后，总得信点什么。", {"sanity": 6, "infectResist": 4}),
    P("pain_tolerance", "忍痛", "will", 2, 2, "痛是信号，不是命令。", {"heal": 4, "hpMax": 4}),
    P("clear_mind", "清醒", "will", 2, 2, "你能分清哪个声音是自己的。", {"sanity": 4, "acc": 2}),
    P("field_surgery", "战地手术", "will", 3, 2, "没有麻醉，也要把子弹取出来。", {"heal": 8}),
    P("ghost", "幽灵", "will", 3, 2, "他们已经不记得你的样子了。", {"stealth": 10, "flee": 6}),
    P("priest_faith", "布道", "will", 3, 2, "你说话时，别人会安静下来。", {"sanity": 5}),
    P("singer", "歌者", "will", 2, 1, "你唱歌的时候，营地会安静。", {"sanity": 6}),
    P("dog_bond", "伙伴", "will", 1, 1, "它会在你睡着的时候守着门。", {"sanity": 4, "scavenge": 2}),
    P("nurse_hands", "护理", "will", 2, 2, "手很稳，心很软。", {"heal": 5, "infectResist": 6}),
    P("sharp_eye", "锐眼", "combat", 2, 1, "你总能先看见对方。", {"crit": 5}),
]

buildings = [
    {"id": "bench", "name": "工作台", "desc": "木桌、台钳、一盏灯。大部分东西都从这里造出来。",
     "maxLevel": 4, "baseCost": {"scrap": 8, "wood": 6, "nail": 8}, "scale": 1.7,
     "effectKey": "none", "perLevel": 0, "icon": "hammer.fill"},
    {"id": "kitchen", "name": "厨房", "desc": "能烧水、能煮东西，能把生的变成能吃的。",
     "maxLevel": 3, "baseCost": {"scrap": 5, "wood": 8, "cooking_pot": 1}, "scale": 1.8,
     "effectKey": "none", "perLevel": 0, "icon": "fork.knife"},
    {"id": "medbay", "name": "医疗台", "desc": "一张干净的床，一盏头灯，一套缝合工具。",
     "maxLevel": 3, "baseCost": {"bandage": 4, "cloth": 6, "scrap": 6}, "scale": 1.9,
     "effectKey": "none", "perLevel": 0, "icon": "cross.case.fill"},
    {"id": "armory", "name": "军械台", "desc": "压弹、修枪、把废铁变成能打响的东西。",
     "maxLevel": 3, "baseCost": {"steel_plate": 2, "scrap": 10, "toolbox": 1}, "scale": 2.0,
     "effectKey": "none", "perLevel": 0, "icon": "shield.fill"},
    {"id": "radio", "name": "电台", "desc": "天线架在屋顶，能听见很远的地方。",
     "maxLevel": 2, "baseCost": {"radio_part": 2, "wire": 6, "battery": 4}, "scale": 2.0,
     "effectKey": "none", "perLevel": 0, "icon": "antenna.radiowaves.left.and.right"},
    {"id": "garden", "name": "菜园", "desc": "翻过的土，插着几根标尺。每天能收一点菜。",
     "maxLevel": 4, "baseCost": {"wood": 6, "seed_pack": 1, "fertilizer": 2}, "scale": 1.6,
     "effectKey": "none", "perLevel": 0, "icon": "leaf.fill"},
    {"id": "collector", "name": "雨水收集器", "desc": "帆布和塑料布搭的斜面，每天能接一点浑水。",
     "maxLevel": 4, "baseCost": {"plastic": 6, "fabric": 2, "rope": 3}, "scale": 1.5,
     "effectKey": "none", "perLevel": 0, "icon": "drop.fill"},
    {"id": "wall", "name": "围墙", "desc": "钢板、沙袋、铁丝网。夜袭时能多挡一会儿。",
     "maxLevel": 4, "baseCost": {"steel_plate": 2, "cement": 4, "scrap": 8}, "scale": 1.8,
     "effectKey": "none", "perLevel": 0, "icon": "shield.lefthalf.filled"},
    {"id": "tower", "name": "瞭望塔", "desc": "三米高，能看见两条街以外。守夜的人喜欢它。",
     "maxLevel": 3, "baseCost": {"wood": 10, "scrap": 8, "rope": 4}, "scale": 1.9,
     "effectKey": "none", "perLevel": 0, "icon": "binoculars.fill"},
    {"id": "bed", "name": "床铺", "desc": "干净的床垫和一床被子。睡得好，第二天才走得动。",
     "maxLevel": 3, "baseCost": {"cloth": 6, "wood": 4, "sleeping_bag": 1}, "scale": 1.8,
     "effectKey": "none", "perLevel": 0, "icon": "bed.double.fill"},
    {"id": "storage", "name": "储物架", "desc": "钉在墙上的架子，能多放不少东西。",
     "maxLevel": 4, "baseCost": {"wood": 8, "nail": 10, "scrap": 4}, "scale": 1.5,
     "effectKey": "none", "perLevel": 4, "icon": "shippingbox.fill"},
    {"id": "still", "name": "蒸馏器", "desc": "铜管、密封罐、小火。能把菜变成酒，也能消毒。",
     "maxLevel": 3, "baseCost": {"copper": 3, "valve": 1, "empty_bottle": 4}, "scale": 1.8,
     "effectKey": "none", "perLevel": 0, "icon": "flame.fill"},
    {"id": "trap_line", "name": "陷阱阵", "desc": "铁丝、铃铛、兽夹。夜里会有东西替你站岗。",
     "maxLevel": 3, "baseCost": {"wire": 6, "trap": 1, "scrap": 6}, "scale": 1.7,
     "effectKey": "none", "perLevel": 0, "icon": "circle.hexagongrid.fill"},
    {"id": "infirmary", "name": "病房", "desc": "几张床，一条帘子，一个能安静躺着的地方。",
     "maxLevel": 3, "baseCost": {"bandage": 3, "cloth": 8, "wood": 5}, "scale": 1.8,
     "effectKey": "none", "perLevel": 0, "icon": "bed.double.fill"},
    {"id": "training", "name": "训练桩", "desc": "绑着草绳的木桩。每天挥几百下，肌肉会记住。",
     "maxLevel": 3, "baseCost": {"wood": 8, "cloth": 4, "rope": 3}, "scale": 1.9,
     "effectKey": "hpMax", "perLevel": 5, "icon": "figure.strengthtraining.traditional"},
    {"id": "doghouse", "name": "犬舍", "desc": "门口的小木屋和一只旧饭盆。有它在，夜里踏实些。",
     "maxLevel": 2, "baseCost": {"wood": 6, "fabric": 2, "canned_food": 2}, "scale": 2.0,
     "effectKey": "none", "perLevel": 0, "icon": "dog.fill"},
]

endings = [
    {"id": "death_torn", "title": "被撕碎", "kind": "death",
     "text": "你没有听见自己的最后一句话。\n疼痛只持续了几秒，然后是一种奇怪的轻松。你看见天花板上的水渍，像一张地图。\n它们还在吃。你已经不在了。",
     "cond": "生命值降到 0"},
    {"id": "death_turn", "title": "转化", "kind": "death",
     "text": "你最后记得的是自己的手。\n指甲变黑，关节发硬，视野边缘开始泛白。你想说点什么，但喉咙里只有风。\n你站起来了。城市里又少了一个人，多了一个影子。",
     "cond": "感染值达到 100"},
    {"id": "death_mind", "title": "崩溃", "kind": "death",
     "text": "你听见有人在叫你的名字，很近，就在耳边。\n你跟着那个声音走了很久，走到一栋没有门的房子里。里面很暖。\n你坐下来，决定不再起来了。",
     "cond": "理智值降到 0"},
    {"id": "win_light", "title": "灯塔仍在运行", "kind": "win",
     "text": "六枚核心嵌入控制台，灯塔的光从白变成很淡的蓝。\n林晚把血清推进离心机，机器开始转动。她说需要三个小时，也可能更久。\n你走到塔外，海风很咸。远处的地平线上，第一次有船朝这边开来。\n你没有拯救世界。你只是让某一部分的它，晚一点结束。",
     "cond": "在灯塔交付 6 枚核心"},
    {"id": "win_stay", "title": "留下的人", "kind": "win",
     "text": "你没有走。\n灯泡换了三次，发电机修了两次，菜园里的番茄第一次结果。\n有人从南边来，带着伤和孩子。你给他们开门，告诉他们水在哪里。\n灯塔每天亮一次。不是为了求救，是为了让还活着的人知道，这里有人在。",
     "cond": "在灯塔选择留下"},
    {"id": "win_burn", "title": "烧塔", "kind": "win",
     "text": "火从塔顶烧到塔底，烧了整整一夜。\n海面被照成橘红色，像很多年前的日落。你站在沙滩上，看着那束光最后闪了一下，然后灭了。\n没有人再能利用它。也没有人再能被它指引。\n你说不清这是慈悲还是残忍。",
     "cond": "在灯塔选择纵火"},
    {"id": "win_boat", "title": "向海", "kind": "win",
     "text": "渔船驶出港口的时候，天还没亮。\n你不敢回头看，怕看见有人在岸上挥手。海浪拍在船壳上，声音大得像心跳。\n第三天，你看见了一座岛。岛上有炊烟。\n你把船靠过去，手心全是汗。",
     "cond": "在港口驾船离开"},
    {"id": "win_signal", "title": "有人听见了", "kind": "win",
     "text": "你把灯塔的坐标发出去，覆盖了所有还能工作的频段。\n之后的十二个小时里，电台收到了十四个回应。有一个人说他在海上，有一个人说他有一箱药，还有一个孩子，只是问了一句：还有人吗？\n你说：有。\n你重复了十四遍。",
     "cond": "在通讯塔广播坐标"},
    {"id": "win_bunker", "title": "门后", "kind": "win",
     "text": "你按下红色按钮，防爆门缓缓合上，把敲击声关在了外面。\n你一个人坐在控制室里，听见通风系统在呼吸。库存够吃两年，水够喝三年。\n你有了一间绝对安全的房间。\n只是每天夜里，你都会听见有人在敲门。你知道他们没有死。你只是没有开门。",
     "cond": "在掩体封锁大门"},
    {"id": "win_whitecrow", "title": "样本编号 47", "kind": "win",
     "text": "他们抽了你的血，抽了六管，然后把针头拔掉，给了你一张床。\n白大褂说你的抗体浓度高得不正常。他们说，也许三年，也许五年。\n你透过观察窗看着城市，玻璃上有一层淡淡的雾。\n你活下来了。以另一种方式。",
     "cond": "接受白鸦的条件"},
    {"id": "win_train", "title": "铁轨尽头", "kind": "win",
     "text": "列车开了两天两夜。\n窗外的风景从废墟变成田野，又从田野变成森林，最后是海。\n你关掉引擎，坐在铁轨上吃掉了最后一份军用口粮。远处有牛在叫。\n你不知道这里有没有人。但至少这里的空气是干净的。",
     "cond": "发动补给列车"},
    {"id": "win_serum", "title": "第一支", "kind": "win",
     "text": "液体从浑浊变得清澈。你给自己注射的时候，手一点都没抖。\n第二天早上，伤口开始结痂。第三天，你把配方抄了十份，贴在每个还能看见的墙上。\n你不知道有没有人会用。但你把门留开了。\n这大概就是希望的样子：不体面，不宏大，只是一支用过的针管。",
     "cond": "完成血清并注射"},
    {"id": "end_mother", "title": "母亲", "kind": "neutral",
     "text": "你坐上那把椅子。几万个人同时站起来，转向你。\n它们没有扑上来。它们只是看着，像在等一个拥抱。\n你听见很多声音在叫你，用你认识的和不认识的口音。\n你闭上眼睛。你终于不用再做选择了。",
     "cond": "在体育场坐上那张椅子"},
    {"id": "end_cult", "title": "新生", "kind": "neutral",
     "text": "针头刺入颈侧的时候，你听见自己的心跳慢下来。\n然后你听见了别的声音：几千个人同时呼吸，像潮水。\n牧师在你身边跪下，说：欢迎回家。\n你张开嘴，想说点什么，但发出来的不是你自己的声音。",
     "cond": "在教堂接受注射"},
    {"id": "end_king", "title": "铁锈王", "kind": "neutral",
     "text": "王冠有点大，滑下来遮住了一只眼睛。\n废料场里的人一个一个跪下去，包括昨天还想杀你的那个。\n你拥有了这座城最坚固的城堡，和所有还能用的废铁。\n你坐在椅子上，看着太阳落下。没有人敢上来打扰你。",
     "cond": "戴上废料场的王冠"},
    {"id": "end_ash", "title": "灰", "kind": "neutral",
     "text": "你又往炉子里添了一铲煤。\n火很亮，映在墙上的影子很慢地动。你想起第一次点火的那个晚上，所有人都在笑。\n现在只剩你，和一个不需要燃料也能烧下去的炉子。\n你坐下来，准备等它烧完。它不会烧完。",
     "cond": "在焚化厂继续添燃料"},
    {"id": "end_loop", "title": "第七盏灯", "kind": "neutral",
     "text": "你数到第七盏灯的时候，听见自己的声音在背后叫你。\n你回头。是一个和你一模一样的人，穿着同样的衣服，脸上同样的疲惫。\n他说：别往上走。\n你问：为什么。\n他说：因为你已经走过一百次了。",
     "cond": "在地铁隧道继续前行"},
    {"id": "end_winter", "title": "冬天", "kind": "neutral",
     "text": "雪下了三天。\n你把最后一块木板钉在窗上，把最后半罐水放在床头。\n无线电里只剩下电流声。灯塔的光在雪里变成一团模糊的白色。\n你钻进睡袋，想着春天。你知道它不会来了。但想一想不花钱。",
     "cond": "在塔顶关掉控制台"},
    {"id": "end_silence", "title": "安静", "kind": "death",
     "text": "你坐在马路中间，看着天。\n没有枪声，没有嚎叫，没有风。只有耳朵里那根很细的线，在轻轻地响。\n你想起有人叫过你的名字。你想不起那是谁了。\n天黑了。你还坐着。",
     "cond": "理智耗尽后选择独坐"},
    {"id": "end_mercy", "title": "放过", "kind": "neutral",
     "text": "你放下刀，转身走出教堂。\n身后没有脚步声，只有歌声，一直在唱，唱到你听不见为止。\n你走了很远，才发现自己在哭。你哭的不是他，是所有本来可以不必死的人。\n你继续走。这次你没有回头。",
     "cond": "在教堂放下刀"},
    {"id": "end_exile", "title": "被赶走的人", "kind": "death",
     "text": "门在你身后关上。\n你听见有人在里面哭，也听见有人把门闩插上。\n你背着包站在雪里，不知道往哪走。这座城市很大，但每一扇门都关着。\n第三天，你不再觉得冷了。",
     "cond": "被营地驱逐并动手"},
    {"id": "end_witness", "title": "记录者", "kind": "neutral",
     "text": "你写完了最后一页，把本子塞进背包。\n你不知道谁会读到它。也许没有人。但你写下了每一个名字，每一个日期，每一件不该被忘记的事。\n你合上笔帽，走出门。外面阳光很好。\n你决定再活一天，只是为了看看后面会发生什么。",
     "cond": "写下这一切"},
    {"id": "end_dog", "title": "铁钉", "kind": "death",
     "text": "你抱着它，一直到它不再动。\n你把它埋在门口的树下，用木板做了个牌子，写上它的名字。\n那天晚上，你没有关门。你希望有什么东西进来。\n什么也没有来。",
     "cond": "铁钉死去"},
    {"id": "end_sacrifice", "title": "最后一次注射", "kind": "win",
     "text": "你把针管塞进她手里。她不知道那是什么，但你说要保管好，她就点头了。\n你坐在门口，感觉伤口越来越热。\n她蹲在你旁边，问你疼不疼。你说不疼。\n你最后看见的，是她抱着那支针管，跑向营地的背影。",
     "cond": "把最后的血清留给孩子"},
]

npcs = [
    {"id": "nurse", "name": "林晚", "role": "急诊科护士 · 白鸦前成员", "desc": "手很稳，话很少。她记得每一个死在她手上的病人的名字。",
     "traits": ["医疗专精", "抗感染", "夜班"], "perkID": "nurse_hands", "trust": 25,
     "joinReq": "带她见过一次真正的伤员", "questID": "q_nurse_1", "icon": "cross.case.fill"},
    {"id": "mechanic", "name": "陈铁", "role": "汽修工 · 改装师", "desc": "手上永远有机油，笑起来很大声。她说修不好的东西只是还没找到对的扳手。",
     "traits": ["制作加速", "武器改装", "烟瘾"], "perkID": "grease_monkey", "trust": 20,
     "joinReq": "帮她修好一台发动机", "questID": "q_mech_1", "icon": "wrench.fill"},
    {"id": "scout", "name": "阿岚", "role": "斥候 · 前快递员", "desc": "走过这条城市所有的巷子。她记得哪条路有狗，哪扇门后有人。",
     "traits": ["潜行", "地图记忆", "跑得快"], "perkID": "light_step", "trust": 30,
     "joinReq": "在她需要的时候开一次门", "questID": "q_scout_1", "icon": "figure.walk"},
    {"id": "sergeant", "name": "何中士", "role": "残军 · 检查站指挥官", "desc": "制服永远扣到最上面一颗。他说命令还没解除，所以他还在守。",
     "traits": ["枪械", "战术", "固执"], "perkID": "marksman", "trust": 15,
     "joinReq": "证明你值得信任", "questID": "q_sergeant_1", "icon": "shield.fill"},
    {"id": "kid", "name": "小满", "role": "十四岁 · 前小学生", "desc": "她只肯吃一半，说另一半留给「以后」。她画画很好，画的都是白天。",
     "traits": ["灵巧", "幸运", "需要保护"], "perkID": "lucky", "trust": 40,
     "joinReq": "给她一个不会被丢下的承诺", "questID": "q_kid_1", "icon": "figure.child"},
    {"id": "trader", "name": "老周", "role": "行商 · 前会计", "desc": "他什么都卖，也什么都收。他说价格是这个世界最后的秩序。",
     "traits": ["交易", "情报", "算得清"], "perkID": "pack_mule", "trust": 10,
     "joinReq": "让他相信你不是来抢东西的", "questID": "q_trader_1", "icon": "shippingbox.fill"},
    {"id": "hunter", "name": "秦", "role": "猎人 · 前护林员", "desc": "他能从一片折断的草看出三小时前经过的东西。他不喜欢城市。",
     "traits": ["远程", "追踪", "沉默"], "perkID": "sharp_eye", "trust": 20,
     "joinReq": "和他一起打一次猎", "questID": "q_hunter_1", "icon": "figure.archery"},
    {"id": "priest", "name": "牧者", "role": "灰袍教团 · 叛逃牧师", "desc": "他仍在祷告，但不再相信。他说他留下来是为了给死人念名字。",
     "traits": ["安抚", "仪式", "知道太多"], "perkID": "priest_faith", "trust": 25,
     "joinReq": "听他把话说完", "questID": "q_priest_1", "icon": "flame.fill"},
    {"id": "doctor", "name": "顾医生", "role": "白鸦 · 病毒学家", "desc": "她的白大褂很干净，眼睛很累。她说她只是想知道答案。",
     "traits": ["科研", "血清", "危险"], "perkID": "field_surgery", "trust": 5,
     "joinReq": "带给她一份抗体血样", "questID": "q_doctor_1", "icon": "testtube.2"},
    {"id": "cook", "name": "胖婶", "role": "食堂厨师 · 营地后勤", "desc": "她能把任何东西煮成能吃的样子，并且坚持每个人都要吃完。",
     "traits": ["烹饪", "士气", "囤积"], "perkID": "iron_stomach", "trust": 30,
     "joinReq": "带来一口能用的锅", "questID": "q_cook_1", "icon": "fork.knife"},
    {"id": "singer", "name": "阿音", "role": "酒吧歌手 · 电台主播", "desc": "她的声音就是灯塔录音里的那个声音。她说她只是想让外面的人知道还有人。",
     "traits": ["鼓舞", "广播", "失眠"], "perkID": "singer", "trust": 35,
     "joinReq": "修好一台收音机", "questID": "q_singer_1", "icon": "music.note"},
    {"id": "prisoner", "name": "4207", "role": "囚犯 · 前爆破手", "desc": "他不说自己的名字，只说编号。他手上有一道很长的疤，是自己划的。",
     "traits": ["爆破", "开锁", "不可信"], "perkID": "demolisher", "trust": 0,
     "joinReq": "给他一把能用的撬棍", "questID": "q_prisoner_1", "icon": "lock.fill"},
    {"id": "gravedigger", "name": "老掘", "role": "掘墓人 · 前殡仪馆工人", "desc": "他给每一个找到的尸体挖坑，不管认不认识。他说这是他唯一还会做的事。",
     "traits": ["冷静", "体力", "知道埋了什么"], "perkID": "survivor", "trust": 20,
     "joinReq": "帮他埋完这一批", "questID": "q_grave_1", "icon": "figure.stand"},
    {"id": "deserter", "name": "李默", "role": "逃兵 · 前工兵", "desc": "他睡觉时总是背靠着墙。他说他不是怕死，是怕被抓回去。",
     "traits": ["工事", "爆破", "警惕"], "perkID": "tough", "trust": 10,
     "joinReq": "保证不会把他交给军方", "questID": "q_deserter_1", "icon": "figure.stand"},
    {"id": "engineer", "name": "老吴", "role": "工程师 · 前电网维修", "desc": "他随身带着一卷电线和一块万用表。他说电比人可靠。",
     "traits": ["电力", "机械", "怕黑"], "perkID": "engineer", "trust": 15,
     "joinReq": "提供一台还能转的发电机", "questID": "q_engineer_1", "icon": "bolt.fill"},
    {"id": "teacher", "name": "苏老师", "role": "小学老师 · 临时看守", "desc": "她还留着点名册。每天早读，她会念一遍名字，然后替没来的人答到。",
     "traits": ["教育", "安抚", "固执"], "perkID": "calm", "trust": 30,
     "joinReq": "帮她把孩子们的名字念完", "questID": "q_teacher_1", "icon": "book.fill"},
    {"id": "warden", "name": "铁门", "role": "前狱警 · 守门人", "desc": "他守着一扇不属于任何人的门。他说门后面是什么，不重要，重要的是门还关着。",
     "traits": ["守夜", "格挡", "沉默"], "perkID": "shield_wall", "trust": 15,
     "joinReq": "和他一起守一整夜", "questID": "q_warden_1", "icon": "shield.lefthalf.filled"},
]

quests = [
    # 主线
    {"id": "m01", "title": "杂音", "giver": "light", "desc": "灯塔的信号需要中继。找一块还能用的无线电零件。",
     "kind": "collect", "target": "radio_part", "count": 1, "rewardXP": 40, "rewardItems": {"bandage": 2}, "next": "m02"},
    {"id": "m02", "title": "公路检查站", "giver": "light", "desc": "去检查站，看看军方还剩下什么。",
     "kind": "visit", "target": "checkpoint", "count": 1, "rewardXP": 60, "rewardItems": {"ammo_556": 8}, "next": "m03"},
    {"id": "m03", "title": "通行证", "giver": "light", "desc": "没有密钥卡，你连军械库的门都摸不到。",
     "kind": "collect", "target": "military_keycard", "count": 1, "rewardXP": 70, "rewardItems": {"mre": 1}, "next": "m04"},
    {"id": "m04", "title": "白鸦的门", "giver": "light", "desc": "雷达站是通往白鸦实验室的必经之路。",
     "kind": "visit", "target": "radar_station", "count": 1, "rewardXP": 80, "rewardItems": {"battery": 4}, "next": "m05"},
    {"id": "m05", "title": "实验记录", "giver": "light", "desc": "取一份实验样本，看看白鸦到底在研究什么。",
     "kind": "collect", "target": "lab_sample", "count": 1, "rewardXP": 90, "rewardItems": {"antibiotics": 2}, "next": "m06"},
    {"id": "m06", "title": "抗体", "giver": "light", "desc": "一名免疫者的血样。白鸦说这比黄金值钱。",
     "kind": "collect", "target": "blood_sample", "count": 1, "rewardXP": 110, "rewardItems": {"serum": 1}, "next": "m07"},
    {"id": "m07", "title": "配方", "giver": "light", "desc": "血清配方，三页手写笔记。",
     "kind": "collect", "target": "serum_formula", "count": 1, "rewardXP": 130, "rewardItems": {"chemical": 3}, "next": "m08"},
    {"id": "m08", "title": "六枚核心", "giver": "light", "desc": "灯塔需要六枚核心才能全功率运行。它们散在这座城里。",
     "kind": "collect", "target": "light_core", "count": 6, "rewardXP": 200, "rewardItems": {"medkit": 1}, "next": "m09"},
    {"id": "m09", "title": "燃料", "giver": "light", "desc": "发电机需要燃料。越多越好。",
     "kind": "collect", "target": "fuel", "count": 4, "rewardXP": 150, "rewardItems": {"jerky": 2}, "next": "m10"},
    {"id": "m10", "title": "白塔", "giver": "light", "desc": "去灯塔。带上核心，带上你还信得过的人。",
     "kind": "visit", "target": "lighthouse", "count": 1, "rewardXP": 300, "rewardItems": {"serum": 1}, "next": None},
]
# 支线
side = [
    ("q_nurse_1", "第一批绷带", "nurse", "收集干净的布料，伤员需要。", "collect", "cloth", 6, 60, {"bandage": 3}),
    ("q_nurse_2", "抗生素配额", "nurse", "药快用完了。", "collect", "antibiotics", 2, 90, {"medkit": 1}),
    ("q_mech_1", "发动机", "mechanic", "带一桶燃料来，我就能让它转起来。", "collect", "fuel", 2, 80, {"fuel": 1}),
    ("q_mech_2", "零件仓库", "mechanic", "去仓库拆点东西回来。", "collect", "generator_part", 1, 100, {"toolbox": 1}),
    ("q_scout_1", "三条路线", "scout", "去三个不同的地方看看，回来告诉我哪条路能走。", "visit", "overpass", 1, 60, {"map_fragment": 1}),
    ("q_scout_2", "桥下", "scout", "别走桥。但如果你非要走，帮我看看桥下有什么。", "visit", "tunnel", 1, 90, {"light_core": 1}),
    ("q_sergeant_1", "哨兵的补给", "sergeant", "检查站的存粮只够四天。", "collect", "mre", 2, 80, {"ammo_556": 10}),
    ("q_sergeant_2", "清理道路", "sergeant", "把盘踞在军械库门口的东西清掉。", "kill", "brute", 3, 120, {"vest_kevlar": 1}),
    ("q_kid_1", "兔子玩偶", "kid", "小满说她的兔子丢在小学了。", "visit", "school", 1, 50, {"candy": 3}),
    ("q_kid_2", "画里的太阳", "kid", "找到三张画，她想把它们贴起来。", "collect", "child_drawing", 3, 80, {"photo": 1}),
    ("q_trader_1", "三件货", "trader", "给我三块能用的金属，我给你一个消息。", "collect", "steel_plate", 3, 90, {"binoculars": 1, "ammo_45": 12}),
    ("q_hunter_1", "林子里的东西", "hunter", "有东西在咬我的陷阱。去处理一下。", "kill", "hound", 4, 90, {"cooked_meat": 2, "arrow": 8}),
    ("q_hunter_2", "鹿角", "hunter", "我需要一副完整的鹿角做诱饵。", "kill", "animal", 3, 100, {"bow_compound": 0, "arrow": 12}),
    ("q_priest_1", "名字", "priest", "帮我把教堂里那些人的名字记下来。", "visit", "church", 1, 70, {"book": 1, "cigar": 1}),
    ("q_priest_2", "祭坛上的东西", "priest", "去 cathedral，别碰那些核心，只看。", "visit", "cathedral", 1, 120, {"light_core": 1}),
    ("q_doctor_1", "样本", "doctor", "我需要一份新鲜的实验样本。", "collect", "lab_sample", 2, 140, {"serum": 1}),
    ("q_doctor_2", "血", "doctor", "抗体血样。越多越好。", "collect", "blood_sample", 1, 160, {"serum": 2}),
    ("q_cook_1", "一口锅", "cook", "没有锅，我只能给你们吃冷的。", "collect", "cooking_pot", 1, 50, {"soup_can": 2}),
    ("q_cook_2", "五十罐", "cook", "营地要过冬了。", "collect", "canned_food", 6, 100, {"mre": 2}),
    ("q_singer_1", "电台", "singer", "修好它，我就继续播。", "collect", "radio_part", 2, 110, {"radio": 1}),
    ("q_singer_2", "新的频率", "singer", "去通讯塔，把天线转个方向。", "visit", "comm_tower", 1, 120, {"circuit": 2}),
    ("q_prisoner_1", "撬棍", "prisoner", "给我一根撬棍，我帮你开任何门。", "collect", "crowbar", 1, 60, {"lockpick": 2}),
    ("q_grave_1", "埋了他们", "gravedigger", "医院后面还有十七具。", "visit", "field_hospital", 1, 80, {"shovel": 1}),
    ("q_grave_2", "名字牌", "gravedigger", "找些木板来，给他们做个记号。", "collect", "wood", 8, 70, {"bone": 3}),
    ("q_deserter_1", "销毁档案", "deserter", "把雷达站里那份名单烧了。", "visit", "radar_station", 1, 110, {"military_keycard": 1}),
    ("q_engineer_1", "点亮营地", "engineer", "给我一台发电机，还有燃料。", "collect", "generator", 1, 150, {"battery_pack": 1}),
    ("q_engineer_2", "电网", "engineer", "变电站里还有能用的一段线。", "collect", "wire", 10, 100, {"circuit": 3}),
    ("q_teacher_1", "点名册", "teacher", "去学校，把点名册带回来。", "visit", "school", 1, 70, {"paper": 5, "candy": 2}),
    ("q_warden_1", "守夜", "warden", "陪我守着这扇门，到天亮。", "collect", "battery", 3, 80, {"flashlight": 1}),
    ("q_board_1", "补给清单", "board", "营地需要废铁、布料和木板。", "collect", "scrap", 10, 80, {"duct_tape": 2}),
    ("q_board_2", "净水", "board", "水不够了。", "collect", "water_bottle", 6, 80, {"purify_tablet": 3}),
    ("q_board_3", "医药", "board", "伤员在增加。", "collect", "bandage", 5, 90, {"antibiotics": 2}),
    ("q_board_4", "子弹", "board", "围墙外的枪声越来越近。", "collect", "ammo_9mm", 12, 80, {"ammo_9mm": 6}),
    ("q_board_5", "探路", "board", "去商业区看看还能不能走。", "visit", "supermarket", 1, 90, {"water_bottle": 3}),
    ("q_board_6", "清剿", "board", "把附近的感染者压低到能睡觉的程度。", "kill", "walker", 10, 100, {"jerky": 2}),
    ("q_board_7", "猎兽", "board", "肉食短缺。", "kill", "animal", 4, 100, {"cooked_meat": 3}),
    ("q_board_8", "制作者", "board", "营地需要更多手工制品。", "craft", "any", 5, 90, {"toolbox": 1}),
    ("q_board_9", "守住十天", "board", "活过第十天，你会习惯的。", "day", "any", 10, 100, {"mre": 1}),
    ("q_board_10", "军械库", "board", "去军械库，看看还能不能补充弹药。", "visit", "armory", 1, 130, {"ammo_556": 12}),
]
for (i, t, g, d, k, tgt, c, xp, rew) in side:
    quests.append({"id": i, "title": t, "giver": g, "desc": d, "kind": k, "target": tgt,
                   "count": c, "rewardXP": xp, "rewardItems": rew, "next": None})

achievements = []
def A(i, n, d, key, goal, hidden=False):
    achievements.append({"id": i, "name": n, "desc": d, "hidden": hidden, "key": key, "goal": goal})

# 基础进度
A("first_blood", "第一次", "杀死第一个感染者。", "kills", 1)
A("kills_10", "手感", "累计杀死 10 个敌人。", "kills", 10)
A("kills_25", "街区的清道夫", "累计杀死 25 个敌人。", "kills", 25)
A("kills_60", "老手", "累计杀死 60 个敌人。", "kills", 60)
A("kills_120", "屠夫", "累计杀死 120 个敌人。", "kills", 120)
A("kills_250", "行走的墓地", "累计杀死 250 个敌人。", "kills", 250)
A("first_search", "第一次翻找", "完成一次搜刮。", "searches", 1)
A("search_20", "熟门熟路", "搜刮 20 次。", "searches", 20)
A("search_60", "拾荒者", "搜刮 60 次。", "searches", 60)
A("search_150", "废墟考古学家", "搜刮 150 次。", "searches", 150)
A("first_craft", "第一件作品", "完成一次制作。", "crafts", 1)
A("craft_10", "手艺人", "制作 10 次。", "crafts", 10)
A("craft_40", "工程师", "制作 40 次。", "crafts", 40)
A("craft_100", "流水线", "制作 100 次。", "crafts", 100)
A("first_heal", "止血", "第一次使用医疗物品。", "heals", 1)
A("build_1", "据点雏形", "升级一次设施。", "builds", 1)
A("build_10", "堡垒", "累计升级 10 次设施。", "builds", 10)
A("build_25", "混凝土与铁", "累计升级 25 次设施。", "builds", 25)
A("visit_5", "周边", "到访 5 个地点。", "places_visited", 5)
A("visit_15", "城市地图", "到访 15 个地点。", "places_visited", 15)
A("visit_30", "无处可去", "到访 30 个地点。", "places_visited", 30)
A("visit_40", "走遍废墟", "到访 40 个地点。", "places_visited", 40)
A("item_50", "囤积癖", "累计拾取 50 件物品。", "items_found", 50)
A("item_150", "仓库", "累计拾取 150 件物品。", "items_found", 150)
A("item_400", "蚂蚁", "累计拾取 400 件物品。", "items_found", 400)
A("battle_20", "习惯暴力", "经历 20 场战斗。", "battles", 20)
A("battle_60", "战场常客", "经历 60 场战斗。", "battles", 60)
A("damage_1000", "千点伤害", "累计造成 1000 点伤害。", "damage_dealt", 1000)
A("damage_5000", "暴力美学", "累计造成 5000 点伤害。", "damage_dealt", 5000)
A("day_5", "第五天", "活到第 5 天。", "days", 5)
A("day_10", "第十天", "活到第 10 天。", "days", 10)
A("day_20", "三周", "活到第 20 天。", "days", 20)
A("day_30", "一个月", "活到第 30 天。", "days", 30)
A("day_45", "撑过冬天", "活到第 45 天。", "days", 45)
A("day_60", "第六十天", "活到第 60 天。", "days", 60)
A("day_90", "活成传说", "活到第 90 天。", "days", 90)
A("boss_1", "首领杀手", "击败一名首领。", "boss_kills", 1)
A("boss_5", "名字被记住", "击败 5 名首领。", "boss_kills", 5)
A("boss_10", "没有王", "击败 10 名首领。", "boss_kills", 10)
A("recruit_1", "同伴", "招募第一名同伴。", "recruited", 1)
A("recruit_4", "满编", "招募 4 名同伴。", "recruited", 4)
A("quest_1", "第一份委托", "完成一个任务。", "quests_done", 1)
A("quest_10", "可靠的人", "完成 10 个任务。", "quests_done", 10)
A("quest_30", "所有人都找你", "完成 30 个任务。", "quests_done", 30)
A("runs_5", "反复", "开始 5 次生存。", "runs", 5)
A("runs_20", "轮回", "开始 20 次生存。", "runs", 20)
A("shards_20", "记忆碎片", "累计获得 20 枚碎片。", "shards", 20)
A("shards_100", "记忆之海", "累计获得 100 枚碎片。", "shards", 100)
A("ending_3", "三种结局", "解锁 3 种结局。", "endings", 3)
A("ending_8", "收藏家", "解锁 8 种结局。", "endings", 8)
A("ending_16", "全知", "解锁 16 种结局。", "endings", 16)
A("ending_24", "所有可能", "解锁全部 24 种结局。", "endings", 24)
# 击杀类型
for (i, n, d, tag, goal) in [
    ("tag_walker_30", "行尸收割", "杀死 30 个行尸。", "walker", 30),
    ("tag_runner_20", "追不上", "杀死 20 个奔行者。", "runner", 20),
    ("tag_brute_10", "以硬碰硬", "杀死 10 个重装感染者。", "brute", 10),
    ("tag_spitter_8", "别沾到", "杀死 8 个喷吐者。", "spitter", 8),
    ("tag_crawler_8", "低头看", "杀死 8 个爬行者。", "crawler", 8),
    ("tag_hound_15", "打的什么针", "杀死 15 只感染兽。", "hound", 15),
    ("tag_animal_10", "野味", "杀死 10 只感染动物。", "animal", 10),
    ("tag_human_20", "同类", "杀死 20 个人类敌人。", "human", 20),
    ("tag_screamer_6", "让它们闭嘴", "杀死 6 个尖啸者。", "screamer", 6),
    ("human_mercy", "手下留情", "放走一个掠夺者。", "mercy", 1),
]:
    A(i, n, d, "kill_" + tag, goal)

# 特定敌人 / 首领
for (i, n, d, eid) in [
    ("kill_rustking", "铁锈王", "击败废料场的王。", "boss_rustking"),
    ("kill_mother", "母亲的怀抱", "击败体育场中央的东西。", "boss_mother"),
    ("kill_hive", "拆巢", "摧毁地铁深处的巢。", "boss_hive"),
    ("kill_whitecrow", "白鸦坠落", "击败白鸦实验体。", "boss_whitecrow"),
    ("kill_preacher", "布道结束", "击败灰袍牧师。", "boss_preacher"),
    ("kill_twins", "双子", "击败双子。", "boss_twins"),
    ("kill_trainman", "列车长", "击败守住列车的人。", "boss_trainman"),
    ("kill_tide", "退潮", "击败港口的东西。", "boss_tide"),
    ("kill_ash", "灰烬行者", "击败灰烬行者。", "boss_ash"),
    ("kill_bell", "钟声停止", "击败钟楼暴君。", "boss_bell"),
]:
    A(i, n, d, "kill_" + eid, 1)

# 结局成就
for (i, n, key, desc) in [
    ("end_light", "灯塔", "win_light", "在灯塔交付全部核心。"),
    ("end_stay", "留下", "win_stay", "选择留在灯塔。"),
    ("end_burn", "烧塔", "win_burn", "烧掉灯塔。"),
    ("end_boat", "向海", "win_boat", "从港口离开。"),
    ("end_signal", "有人听见了", "win_signal", "广播坐标。"),
    ("end_bunker", "门后", "win_bunker", "封闭掩体。"),
    ("end_whitecrow", "样本", "win_whitecrow", "接受白鸦的实验。"),
    ("end_train", "铁轨尽头", "win_train", "发动列车。"),
    ("end_serum", "第一支", "win_serum", "完成血清。"),
    ("end_mother", "母亲", "end_mother", "坐上体育场的椅子。"),
    ("end_cult", "新生", "end_cult", "接受灰袍的注射。"),
    ("end_king", "铁锈王", "end_king", "戴上王冠。"),
    ("end_ash", "灰", "end_ash", "在焚化厂添燃料。"),
    ("end_loop", "第七盏灯", "end_loop", "在地铁里继续走。"),
    ("end_winter", "冬天", "end_winter", "关掉灯塔控制台。"),
    ("end_silence", "安静", "end_silence", "在街上坐下来。"),
    ("end_mercy", "放过", "end_mercy", "放下刀。"),
    ("end_exile", "被赶走的人", "end_exile", "被营地驱逐。"),
    ("end_witness", "记录者", "end_witness", "写下这一切。"),
    ("end_dog", "铁钉", "end_dog", "埋葬铁钉。"),
    ("end_sacrifice", "最后一次注射", "end_sacrifice", "把血清留给孩子。"),
]:
    A(i, n, "解锁结局：" + desc, "ending_" + key, 1)

# 特殊行为
A("survive_infection", "带病生存", "感染值超过 80 后活过 5 天。", "infection_survived", 5)
A("near_death", "一线", "生命值低于 10 后活下来。", "near_death", 1)
A("no_ammo", "冷兵器", "在没有弹药的情况下击杀 20 个敌人。", "melee_kills", 20)
A("guns_50", "火力覆盖", "用枪械击杀 50 个敌人。", "gun_kills", 50)
A("craft_weapon", "自制", "制作一把武器。", "weapons_crafted", 1)
A("craft_armor", "缝纫课", "制作一件护甲。", "armors_crafted", 1)
A("win_50", "五十场", "赢下 50 场战斗。", "battles_won", 50)
A("night_owl", "夜行动物", "在夜间战斗 20 次。", "night_battles", 20)
A("looter", "满载", "背包负重达到上限。", "overweight", 1)
A("codex_half", "半个图鉴", "记录 30 种敌人。", "enemy_types", 30)
A("codex_full", "全图鉴", "记录 60 种敌人。", "enemy_types", 60)
A("friend_dog", "铁钉", "和一条狗成为朋友。", "flag_dog", 1)
A("music", "一首歌", "听完一整张唱片。", "flag_music", 1)
A("core_6", "六枚", "同时持有 6 枚核心。", "cores_held", 6)
A("rich", "有钱人", "持有价值 500 的贵重品。", "valuables", 500)

journal = [
    ("第 1 天，天气晴。超市的冷柜还会响，像有人在里面敲门。我没敢开。", "无名者的日记"),
    ("他们说水要烧开。我烧了，但水面上还是浮着一层灰。", "便利店便签"),
    ("今天杀了一个人。他先动的手。我一直在想这句话是不是真的。", "撕下的日记页"),
    ("如果你看到这本册子，说明我失败了。请继续往北走。", "地图背面"),
    ("广播说军队在组织撤离。广播说了三个月了。", "收音机旁的纸条"),
    ("爸爸说他去找妈妈。他走的时候带了枪，没有带我。", "小学作业本"),
    ("我把最后一块巧克力留给了妹妹。她没有醒过来。", "公寓墙上的字"),
    ("不要相信穿白大褂的人。他们会给你很好的理由。", "医院告示"),
    ("这里的夜晚很长。我学会了不看窗外。", "营地床板"),
    ("如果你听见钟声，说明你离钟楼很近了。别去。", "涂鸦"),
    ("我数过了，这栋楼里有四十七具。我只埋了三十一具。", "掘墓人的记录"),
    ("今天在收音机里听见一个女人的声音。她说她还在灯塔。", "幸存者笔记"),
    ("我给他取名叫铁钉，因为它总是踩到钉子。", "营地日志"),
    ("我梦见城市还亮着灯。醒来之后，灯是灭的。", "日记"),
    ("不要浪费子弹。每一发都是一条命换来的。", "军械库标语"),
    ("教堂里的人说灰烬之后有新生。我觉得他们只是需要相信点什么。", "无署名纸条"),
    ("我把婚戒留在了井边。她说过喜欢那口井。", "井边石刻"),
    ("孩子问我，怪物会不会疼。我说不会。她哭了。", "营地日志"),
    ("今天我第一次看见了海。海是灰色的，和天一样。", "公路休息站"),
    ("如果有人读到这里：请把冰箱上的照片带走。", "铁皮盒里的信"),
    ("我们本想走到灯塔。我们走了六天。第七天，少了一个人。", "地图残页"),
    ("雨下了一整夜。我把所有桶都摆了出去。水是酸的。", "屋顶水桶"),
    ("我在墙上画正字。今天是第十五个正字的最后一笔。", "安全屋墙面"),
    ("我听见他在门外咳嗽。他咳了整整一夜，我不敢开门。", "公寓门缝纸条"),
    ("抗生素还有四粒。我决定留给最年轻的人。", "医疗包"),
    ("发电机还能转。只要我不停下来想。", "变电站日志"),
    ("我在高架桥上待了三天，看车流。车流的尽头是雾。", "高架桥刻字"),
    ("他们说南边还有一座城没有沦陷。我决定往南走。", "休息站留言"),
    ("别喝河里的水。哪怕是烧开的。", "河湾农场木牌"),
    ("我给自己定了规矩：不杀孩子。今天我的规矩救了我。", "营地笔记"),
    ("我把最后一张照片放进内袋。这样我就不会忘记他们。", "幸存者日记"),
    ("钟声响了十三下。我觉得不对劲，但我说不出来为什么。", "钟楼附近的涂鸦"),
    ("我在这里等了三天，没有等到他。我决定走了。", "码头木箱"),
    ("如果有来生，我想开一家面馆。不用很大，能坐满就好。", "日记最后一页"),
    ("他们把车堵在隧道口，以为能挡住。后面的事我不记得了。", "隧道墙壁"),
    ("我在超市里找到了黄桃罐头。我坐在货架上吃完了两罐。", "超市便条"),
    ("我把药藏在水箱里。只有我知道。这就是我活下来的原因。", "未署名"),
    ("医疗队三天前撤走了。他们没带走伤员。", "医院白板"),
    ("我用粉笔在门上画了一个圈。里面的人还活着。", "学校门框"),
    ("不要往西边走。西边的桥断了。", "路口指示牌"),
    ("我们六个人，现在剩两个。另一个不肯说话。", "露营地日志"),
    ("今天天气很好。我把被子晒了。至少这一点，和以前一样。", "日记"),
    ("水塔上能看见整座城。它比我想象的安静。", "水塔刻字"),
    ("如果核心里有编号，请按顺序放。别问我为什么。", "灯塔控制室"),
    ("我今天朝一个孩子举起了枪。他跑了。我坐在地上吐了。", "撕碎的纸"),
    ("母带只剩这一卷。希望有人能听见。", "电台留言"),
    ("我们把它叫做「潮汐」。它涨起来的时候，整条街都会消失。", "港口记录"),
    ("妈妈说天黑之前要回家。现在没有家了。", "蜡笔背面"),
    ("我在市政厅找到一份名单。上面有我的名字。", "市政厅文件"),
    ("如果有一天你走到灯塔，替我看一眼那束光。", "工地安全帽内衬"),
    ("子弹还剩三发。我决定留一发给自己。", "军械库"),
    ("我听见有人在唱歌。我跟着唱，唱到嗓子哑了。", "体育场看台"),
    ("我们没有食物了。我把皮带煮了。味道不好，但有效。", "公寓账本"),
    ("今天是我戒烟的第三天。我杀了四个感染者。", "营地日志"),
    ("他们说我疯了。我说我只是看得比他们清楚。", "实验室便签"),
    ("别去地铁。下面有东西在数你的脚步。", "站台涂鸦"),
    ("我写这些，不是为了被救。是为了证明我来过。", "记录者"),
    ("今天第一次有人叫我的名字。我差点忘了那是我。", "日记"),
    ("我把所有东西都留给你了。别浪费。", "储物柜"),
    ("有人在敲门。敲了三下，停了，又敲了两下。我没开。", "公寓日志"),
    ("我学会了不用眼睛看路。脚下会告诉你方向。", "盲人幸存者"),
    ("如果还能再吃一次热的东西，我想喝一碗汤。", "食堂黑板"),
    ("他们用铁皮做了一面墙。墙后面，是一个小菜园。", "营地记录"),
    ("我把钟绳割断了。它再也不会响了。", "钟楼"),
    ("这炉子烧了四十天，没有停过。", "焚化厂控制室"),
    ("我数了，隧道里有七盏灯。每次都数到七。", "地铁隧道"),
    ("孩子说她想养一只狗。我说好。我们就去找。", "营地笔记"),
    ("我把她的名字刻在子弹上。最后一发。", "军械库刻痕"),
    ("我们在码头等潮水。潮水带来了很多东西。", "港口日志"),
    ("不要开 602。不要开 602。不要开 602。", "公寓楼梯"),
    ("有人从南边来，走了一百多公里。他说他一直在听广播。", "营地记录"),
    ("我把收音机埋了。它总是在不该响的时候响。", "后院土层"),
    ("我在这里写最后一行字。愿有人记得。", "教堂长椅"),
    ("如果你在读这个，请不要停下来。继续走。", "路边指示牌"),
    ("我想念便利店的热狗。这很荒唐，但我是认真的。", "日记"),
    ("今天我把一整个弹匣打空了。为了一个不值得的理由。", "军械库账本"),
    ("他们给了我一张地图，上面标着灯塔。地图是手画的。", "货箱底部"),
    ("雪化了。下面全是草。它们长得很好。", "农场日记"),
    ("我决定相信一次人。这个决定让我付出了两根手指。", "日记"),
    ("铁门后面有七个人。铁门前面有三个人。门一直没开。", "岗哨记录"),
    ("我在广播里说：还有人吗。有人回了。就一个字：有。", "电台日志"),
    ("我不怕死，我怕死后没人记得我叫什么。", "墓碑背面"),
    ("钟楼的钟被人敲了一夜。第二天，钟楼上什么也没有。", "目击记录"),
    ("今天很安静。安静得让我想把所有的枪都开一遍。", "营地日志"),
    ("我们给菜园围了铁丝网。不是防人，是防它们。", "菜园木牌"),
    ("我梦见了超市。货架是满的，灯是亮的，没有人。", "日记"),
    ("在废墟里，最贵的东西是干净的水。", "交易记录"),
    ("我在这里躲了十五天。今天第一次出门。", "地下室墙面"),
    ("如果我没能回来，请把背包里的东西分给孩子们。", "遗书"),
    ("我把核心藏在冰箱里。没人会翻冰箱。", "公寓便条"),
    ("广场上的旗子换了三次。最后一次，是黑色的。", "市民记录"),
    ("今天是我生日。我给自己煮了一碗面。味道很差。", "日记"),
    ("你问我为什么还活着。因为我已经不知道该去死了。", "无署名纸条"),
    ("我把她的骨灰装进了一个罐头盒。我们结婚时用的那种。", "旧罐头"),
    ("外面的雨停了。我决定出去看看。", "日记最后一页"),
    ("有光从窗户照进来。我坐了很久，才想起来那是太阳。", "幸存者笔记"),
    ("我听见孩子的笑声了。我找了一整栋楼，什么也没有。", "公寓记录"),
    ("如果你听见无线电响，别急着回答。先听三遍。", "电台守则"),
    ("我把门锁了三道。钥匙放在门垫下面。我从不拿。", "安全屋"),
    ("这里是灯塔。如果你能听见，说明中继站还活着。", "无线电录音"),
    ("他们走得很快，没有回头。我在原地站了很久。", "公路记录"),
    ("我从没见过海。现在看到了，也谈不上喜欢。", "港口日记"),
    ("我给自己留了一份口粮。我知道这很自私。但我还不想死。", "储物柜便条"),
    ("墙根下长出了一棵草。我没有拔掉它。", "营地记录"),
    ("最后一个声音是关门声。很轻，像有人走了。", "公寓日志"),
    ("我们数到一百，然后一起跑。只有我跑了出来。", "幸存者口述"),
    ("这是最后一次记录。不是因为没有电，是因为没有话了。", "电台日志"),
]

save("perks", perks)
save("buildings", buildings)
save("endings", endings)
save("npcs", npcs)
save("quests", quests)
save("achievements", achievements)
save("journal", [{"id": "j%03d" % (i + 1), "text": t, "src": s} for i, (t, s) in enumerate(journal)])
