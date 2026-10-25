#!/usr/bin/env python3
# 生成事件事件卡
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "LastEmber", "Resources", "Content")

def save(name, data):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{name}: {len(data)}")

def C(text, log, effect=None, items=None, req=None, fight=None,
      chance=100, fail_effect=None, fail_log="", ending=None, next=None):
    return {"text": text, "req": req or [], "effect": effect or {}, "items": items or {},
            "fight": fight, "next": next, "chance": chance,
            "effectFail": fail_effect or {}, "log": log, "logFail": fail_log,
            "ending": ending}

def E(id, title, text, choices, tag="encounter", places=None, weight=10, once=False, min_day=1):
    return {"id": id, "title": title, "text": text, "tag": tag, "weight": weight,
            "once": once, "minDay": min_day, "places": places or [], "choices": choices}

events = []

# ============ 开场 ============
events.append(E("ev_intro", "第 47 天", """无线电在凌晨三点自己响了。
一段录音，女声，背景里有海浪："这里是白塔灯塔。如果你能听见，说明中继站还活着。带上核心，带上你还信得过的人。我们还有电，还有热水。"
录音重复了三遍，然后是一段很长的电流声。
你坐在床沿，听见外面有东西在挠铁门。""", [
    C("把铁门顶死，天亮再说", "你搬来货架顶住门。抓挠声持续到天亮，然后停了。",
      {"fatigue": 6, "sanity": 2}, {"scrap": 1}),
    C("从窗口看一眼", "你掀开窗帘一角。三个影子站在雨里，都低着头。你数了两遍，确认它们没有抬头。",
      {"sanity": -4, "xp": 6}, {"cloth": 1}),
    C("现在就出门，去灯塔", "你背上包，推开门。雨很冷，但你还活着，这就够了。",
      {"xp": 10, "fatigue": 3}, {"water_bottle": 1}),
], tag="story", weight=100, once=True))

# ============ 营地 / 每日 ============
events.append(E("ev_night_knock", "夜里的敲门声", """三下，停顿，两下。然后又三下。
不像是丧尸——它们不会数拍子。""", [
    C("开门", "门外是个浑身湿透的女人，抱着一卷地图。她说她叫阿岚，从南边走过来，走了十一天。",
      {"sanity": 4, "flag_met_scout": 1}, {"map_fragment": 1}, req=["day>=3"]),
    C("不出声，握紧武器", "敲门声持续了二十分钟，然后变成抓挠，最后消失。你在门后坐到天亮。",
      {"fatigue": 8, "sanity": -3}),
    C("朝门外开一枪", "枪声在楼宇间弹了很久。门外安静了。你希望那真的是丧尸。",
      {"sanity": -5, "xp": 4, "vulture": -1}, {"ammo_9mm": -1}, req=["item:ammo_9mm>=1"]),
], tag="daily", weight=14, min_day=2))

events.append(E("ev_dog", "一条狗", """一条瘦得脱形的狗蹲在门口，脖子上挂着半截皮带。
它没有叫，只是看着你，尾巴动了一下。""", [
    C("给它一点吃的", "它吃得很小心，吃完之后就趴在门口不走了。你决定叫它「铁钉」。",
      {"sanity": 8, "flag_dog": 1}, {"canned_food": -1, "water_bottle": -1}, req=["item:canned_food>=1"]),
    C("赶走它", "你跺了跺脚。它退了两步，又停下，最后还是走了。",
      {"sanity": -4}),
    C("杀了它", "你不敢看它的眼睛。肉很柴，但你今晚不用挨饿。",
      {"hunger": 20, "sanity": -10}, {"rat_meat": 2, "dog_tag": 1}),
], tag="daily", weight=8, once=True, min_day=2))

events.append(E("ev_radio_voice", "每隔四小时的坐标", """收音机里那个女声准时出现。她念一串坐标，然后停顿很久，像是在等谁回答。
今天她多说了一句："如果你在路上，别走桥。桥下有东西。"。""", [
    C("记下坐标", "你把数字抄在手背上。手背已经写满了。",
      {"xp": 10, "flag_lighthouse_known": 1}, {"map_fragment": 1}),
    C("试着回话", "你按下通话键，说「收到」。对面沉默了十几秒，然后传来一声很轻的「谢谢」。你握着对讲机，手心在出汗。",
      {"sanity": 10, "xp": 14, "flag_lighthouse_known": 1}, {}),
    C("关掉它", "安静之后，你反而睡不着了。",
      {"sanity": 3}),
], tag="daily", weight=10, min_day=2))

events.append(E("ev_rain", "酸雨", """雨点打在铁皮上，声音不对。你伸手接了一点，指尖发麻。""", [
    C("收集雨水", "你摆了三个桶，接了大半。烧开之后大概能喝。",
      {"fatigue": 5}, {"water_dirty": 3}),
    C("躲进屋里", "你把所有缝隙堵上，但空气里还是有股金属味。",
      {"warmth": -4, "hp": -2}),
    C("趁机洗个澡", "冷水冲下来的时候你差点叫出声。干净的感觉很奢侈。",
      {"sanity": 12, "hp": -5, "fatigue": -6}),
], tag="daily", weight=8))

events.append(E("ev_thief", "物资失踪", """一罐午餐肉不见了。你昨天数过，还剩两罐。""", [
    C("搜查所有人", "你把每个人的包都翻了一遍，什么也没找到。晚上没人跟你说话。",
      {"sanity": -4, "flag_suspect": 1}),
    C("算了", "也许是你记错了。你开始怀疑自己的记性。",
      {"sanity": -2}),
    C("设个陷阱", "你在一罐水上做了记号。第二天，记号出现在老赵的桌上。他没有解释。",
      {"sanity": -5, "xp": 6}),
], tag="daily", weight=7))

events.append(E("ev_child_cry", "孩子的哭声", """哭声隔着两条街传过来，断断续续。
这附近不应该有孩子。""", [
    C("过去看看", "你在一辆翻倒的校车里找到一个小女孩，六岁，鞋掉了一只。她看见你的时候，先举起了双手。",
      {"sanity": -2, "flag_child": 1, "flag_met_kid": 1}, {"child_drawing": 1}),
    C("捂住耳朵走开", "哭声跟了你三个街区，然后突然停了。你不敢回头。",
      {"sanity": -8}),
    C("鸣枪示警", "哭声停了，换来的是别的东西的嚎叫。",
      {"xp": 4, "sanity": -2}, {"ammo_9mm": -1}, req=["item:ammo_9mm>=1"]),
], tag="daily", weight=6, once=True, min_day=3))

events.append(E("ev_mailman", "邮差", """一个背着邮袋的老人坐在路边的邮筒上，脚边摆着一排罐头和一叠信。
"明码标价，"他说，"我这儿不收钱，只收还能用的东西。"。""", [
    C("用废铁换罐头", "他挑了两块最沉的废铁，递给你三罐没有标签的东西。",
      {}, {"scrap": -3, "canned_food": 3}, req=["item:scrap>=3"]),
    C("用电池换药", "他把一小盒抗生素推过来，动作很快，像怕自己反悔。",
      {}, {"battery": -1, "antibiotics": 2}, req=["item:battery>=1"]),
    C("问他灯塔的事", "他抬头看了你很久。“那座塔没救了，”他说，“但塔上的人还值得救。”",
      {"xp": 12, "sanity": 2, "flag_lighthouse_known": 1}, {}),
    C("抢他", "你刚伸手，老人的刀已经到了你喉咙前。他叹了口气，把刀收回去，收拾东西走了。",
      {"hp": -12, "sanity": -8, "vulture": 1}, {"canned_food": 1}),
], tag="daily", weight=10, min_day=4))

events.append(E("ev_cult_offer", "灰袍传教", """两个灰袍人站在门口，没带武器。其中一个递给你一袋豆子。
"灰烬之后有新生，"她说，"跟我们来，你不用再一个人扛。"。""", [
    C("收下东西，拒绝邀请", "她把豆子塞进你手里，笑了一下。“门一直开着。”",
      {"sanity": 2}, {"beans_can": 2}),
    C("听他们讲完", "他们讲了一个小时，讲火，讲重生，讲被选中的人。你发现自己的手抖得没那么厉害了。",
      {"sanity": 10, "order": 2, "xp": 8}),
    C("拔枪赶走他们", "他们不慌，只是转身走了。走出很远之后，其中一个回头看了你一眼。",
      {"order": -4, "vulture": 2}, {}),
], tag="daily", weight=8, min_day=5))

events.append(E("ev_soldier_broadcast", "军方广播", """频道里一段沙哑的男声："检查站仍在接收幸存者。携带武器者请放在地上。重复，携带武器者请放在地上。"。""", [
    C("前往检查站", "你在门口被搜了身，登记了名字。他们给了你一瓶水和一张通行条。",
      {"military": 3, "sanity": 4, "flag_checkpoint_pass": 1}, {"water_bottle": 2, "military_biscuit": 2}),
    C("记下频率", "你调好频率，关掉收音机。多一个知道的地方，多一条路。",
      {"xp": 8, "flag_checkpoint_known": 1}),
    C("保持沉默", "广播重复到第七遍时停了。",
      {}),
], tag="daily", weight=8, min_day=4))

events.append(E("ev_fever", "发烧", """你半夜被冷汗浸醒，额头烫得吓人。""", [
    C("吃药硬扛", "药片卡在喉咙里，你灌了半壶水才咽下去。天亮时烧退了一点。",
      {"hp": -6, "infection": -4}, {"pills_fever": -1}, req=["item:pills_fever>=1"]),
    C("用湿布降温", "你裹着毯子发抖，一直抖到天亮。至少还活着。",
      {"hp": -14, "sanity": -4, "fatigue": -6}),
    C("让同伴照顾你", "有人守了你一夜，每半小时换一次湿布。你醒来时，她在椅子上睡着了。",
      {"hp": -4, "sanity": 10}, req=["companions>=1"]),
], tag="daily", weight=7, min_day=4))

events.append(E("ev_letters", "前任屋主的信", """铁皮盒里有一叠信，最上面一封写着："如果你读到这个，请帮我把冰箱上的照片带走。"。""", [
    C("带走照片", "照片上是一家人，背景里有海。你把它塞进内袋。",
      {"sanity": 6}, {"photo": 1}),
    C("读完全部信件", "信里讲了一次失败的逃亡，讲了一个叫白塔的地方，最后一张只有一句话：”别相信穿白大褂的人。“。",
      {"xp": 12, "sanity": -2, "flag_whitecrow_warning": 1}, {"map_fragment": 1}),
    C("放回去", "你把盒子盖好，摆回原位。",
      {"sanity": 2}),
], tag="daily", weight=6, once=True))

events.append(E("ev_music", "唱片", """你在一堆杂物里翻出一台手摇留声机，还有一张唱片。
放上去之后，是一个女人在唱一首很老的歌。""", [
    C("听完", "你坐在地上，听完了一整面。外面天黑了，你忘了点灯。",
      {"sanity": 18, "fatigue": -8}),
    C("带到营地和所有人一起听", "没人说话。老赵在最后偷偷擦了眼睛。",
      {"sanity": 14, "flag_music": 1}, req=["companions>=1"]),
    C("砸了它", "你不想知道自己为什么会这么做。",
      {"sanity": -6}, {"vinyl": 1, "scrap": 2}),
], tag="daily", weight=5, once=True))

events.append(E("ev_smoke", "远处的烟", """地平线上有三股烟，间隔很均匀。
不像是火灾。更像是信号。""", [
    C("朝烟走", "你走了两个小时，找到一处被烧毁的营地。灰里有骨头，还有一枚烧变形的婚戒。",
      {"fatigue": 10, "sanity": -5}, {"wedding_ring": 1, "charcoal": 2}),
    C("记下方位", "你在墙上用炭画了个箭头。也许以后用得上。",
      {"xp": 6, "flag_smoke_seen": 1}),
    C("绕开", "你选择不惹麻烦。这个选择通常是对的。",
      {"sanity": 2}),
], tag="daily", weight=6, min_day=3))

events.append(E("ev_beggar", "乞讨者", """一个瘦到脱相的男人跪在路边，手里捧着一个空罐头。
他没说话，只是把罐头往前递了递。""", [
    C("给他一罐食物", "他接过去的时候手抖得厉害，说了声谢谢，然后哭了。",
      {"sanity": 10, "order": 1}, {"canned_food": -1}, req=["item:canned_food>=1"]),
    C("给他水", "他喝得很慢，像在喝什么很贵的东西。",
      {"sanity": 6}, {"water_bottle": -1}, req=["item:water_bottle>=1"]),
    C("绕过去", "你听见他在背后说了句什么，但没听清。",
      {"sanity": -3}),
    C("搜他的身", "他身上的东西比你想象的还少。",
      {"sanity": -8, "vulture": 1}, {"scrap": 2}),
], tag="daily", weight=7, min_day=2))

events.append(E("ev_wounded", "受伤的陌生人", """他靠墙坐着，小腿上一道很深的伤口，已经发黑。
"别过来，"他说，"我被咬了。"。""", [
    C("给他包扎", "你蹲下的时候，他一直盯着你的手。包扎完，他告诉你一个地方，说那里有很多药。",
      {"sanity": 8, "xp": 10, "flag_wounded_help": 1}, {"bandage": -2, "antiseptic": -1}, req=["item:bandage>=2"]),
    C("问他从哪来", "他说了个名字，然后开始发抖。你退后两步，握紧了刀。",
      {"sanity": -3, "xp": 4}),
    C("结束他的痛苦", "你下手很快。他没有反抗。你在他口袋里找到一张全家福。",
      {"sanity": -12, "xp": 6}, {"photo": 1, "bandage": 2}),
], tag="daily", weight=8, min_day=3))

events.append(E("ev_cold", "寒潮", """温度一夜之间掉了十几度。你呼出的气在窗上结了霜。""", [
    C("烧掉旧家具取暖", "屋子里终于暖了，但浓烟让你咳了一整夜。",
      {"warmth": 20, "hp": -3}, {"wood": -3}, req=["item:wood>=3"]),
    C("把所有衣服穿上", "你裹成一只球，还是冷。",
      {"warmth": 6, "fatigue": -8}),
    C("抱在一起睡", "同伴们的体温让你想起很久以前的事。",
      {"warmth": 18, "sanity": 8}, req=["companions>=1"]),
], tag="daily", weight=7, min_day=6))

events.append(E("ev_horde", "尸潮经过", """它们从街口涌过来，像一条没有尽头的河。你听见几百双脚同时摩擦地面。
你们躲在二楼，没人敢呼吸。""", [
    C("等它们过去", "三个小时。你数着自己的心跳，数到忘了数。",
      {"fatigue": 14, "sanity": -6, "xp": 12}),
    C("从后窗撤走", "你们从消防梯下去，绕了两条街。回头时，那栋楼已经被淹没了。",
      {"fatigue": 10, "sanity": -2, "xp": 14}),
    C("开枪引开它们", "枪声把整条河引向了另一个方向。你们活了下来，但别的地方会死人。",
      {"sanity": -8, "xp": 16, "military": 1}, {"ammo_556": -2}, req=["item:ammo_556>=2"]),
], tag="daily", weight=5, min_day=8))

events.append(E("ev_gunshot_night", "夜里的枪声", """两枪，间隔很久，然后是一声很长的惨叫。
枪声在你据点北边，大概三条街。""", [
    C("过去看看", "你在一家洗衣店里找到两具尸体，一具是人的，一具曾经是人的。柜台上有一把没子弹的手枪。",
      {"sanity": -6, "xp": 12}, {"pistol_9mm": 1, "ammo_9mm": 3}),
    C("守住据点", "你把所有人叫起来，守到天亮。什么也没发生，但没人睡得着。",
      {"fatigue": 8, "sanity": -2}),
    C("趁乱去搜刮", "你摸黑进了隔壁的药店，手一直在抖，但收获不错。",
      {"sanity": -4}, {"bandage": 2, "pills_pain": 1}),
], tag="daily", weight=6, min_day=5))

events.append(E("ev_winter", "第一场雪", """雪落下来的时候，所有人都停下了手里的活。
它很干净，盖住了血、灰和尸体。半小时后，雪下面开始动。""", [
    C("加固据点，准备过冬", "你们把窗户钉死，把食物重新分配。冬天会很长。",
      {"warmth": 10, "sanity": 4, "xp": 20}, req=["day>=40"]),
    C("出去找燃料", "你在雪里走了半天，回来时鞋湿透了，但背上多了一捆木头。",
      {"fatigue": 14, "warmth": -6}, {"wood": 4, "fuel": 1}),
    C("坐在雪里，什么都不做", "你看着雪，想起某个冬天，有人在厨房里喊你吃饭。你决定再活一天。",
      {"sanity": -4, "warmth": -10, "xp": 8}),
], tag="daily", weight=6, min_day=30))

events.append(E("ev_starving", "饥饿", """你已经两天没吃东西了。眼前偶尔会闪过一些不存在的光点。""", [
    C("吃光最后的存粮", "你撕开最后一包压缩饼干，吃得很慢。",
      {"hunger": 40, "sanity": 4}, {"crackers": -1}, req=["item:crackers>=1"]),
    C("煮皮带", "汤是黑的，味道像橡胶。你还是喝了。",
      {"hunger": 16, "sanity": -4, "fatigue": -4}),
    C("去翻垃圾桶", "你翻到了半盒发霉的麦片，挑出了还能吃的部分。",
      {"hunger": 18, "sanity": -8}, {"cereal": 1}),
], tag="daily", weight=8, min_day=4))

# ============ 旧城区 ============
events.append(E("ev_conv_clerk", "收银台后面", """收银台后面坐着一具尸体，工牌上写着「小林」，手里还攥着一把零钱。
收银机是开的，里面没有钱，只有一张便条：「对不起，我先走了。」""", [
    C("合上他的眼睛", "你伸手的时候发现他的眼睑已经僵了。你试了两次才合上。",
      {"sanity": 4, "xp": 6}, {}),
    C("拿走工牌和零钱", "零钱在口袋里响了一路。你不知道自己为什么要拿。",
      {"sanity": -3}, {"scrap": 1, "photo": 1}),
    C("翻收银台下面", "你在下面摸到一个铁盒，里面是三罐罐头和一把钥匙。",
      {"xp": 8}, {"canned_food": 3, "lockpick": 1}),
], places=["convenience"], weight=12, once=True))

events.append(E("ev_apartment_family", "402 室", """门没锁。客厅里摆着三副碗筷，饭菜早就烂成了黑色的壳。
卧室门关着，门缝里塞着毛巾。""", [
    C("打开卧室门", "床上有两具抱在一起的尸体，一大一小。床头放着一瓶安眠药，已经空了。",
      {"sanity": -14, "xp": 8}, {"pills_pain": 2, "child_drawing": 1}),
    C("不打开，退出去", "你带上门，在门口站了一会儿。楼道里的声控灯亮了又灭。",
      {"sanity": -4}),
    C("搜客厅", "你在电视柜里找到一盒子弹和半条香烟。",
      {}, {"ammo_9mm": 4, "cigarettes": 1}),
], places=["apartment"], weight=14, once=True))

events.append(E("ev_school_class", "三年二班", """黑板上还留着作业：写一封信给二十年后的自己。
课桌上摆着三十七封信，都用铅笔画了装饰。""", [
    C("读几封", "大部分孩子想当宇航员、老师、开面馆的。有一封只写了一句话：”我希望妈妈不要死。“。",
      {"sanity": -6, "xp": 10}, {"child_drawing": 1}),
    C("把信收好", "你找了根绳子把信捆起来，放进背包最底层。",
      {"sanity": 8}, {"paper": 3}),
    C("在黑板背面留下自己的字", "你写：「我还在。」粉笔断了两次。",
      {"sanity": 6, "xp": 8}),
], places=["school"], weight=12, once=True))

events.append(E("ev_pharmacy_back", "药房后间", """后间的门虚掩着，里面有人在哼歌。
调子很轻，像是怕吵醒谁。""", [
    C("推门进去", "一个穿白大褂的年轻女人正在分装药片。她抬头看你，眼睛很红。”你是来抢药的？“她问。”你要什么，我给你。别动手。“。",
      {"flag_met_nurse": 1, "sanity": 4, "whitecrow": 1}, {"bandage": 2, "antibiotics": 1}),
    C("在门口退走", "你退出去的时候踩到了一块玻璃。歌声停了。你快步离开。",
      {"sanity": -2}),
    C("等她离开再进去", "半小时后她背着包走了。你进去搜了一圈，找到不少东西。",
      {"sanity": -4}, {"bandage": 3, "pills_pain": 2, "antibiotics": 1}),
], places=["pharmacy", "clinic"], weight=14, once=True, min_day=2))

events.append(E("ev_police_gun", "证物室", """铁柜里锁着几把证物枪，柜门被撬开了一半。""", [
    C("用撬棍撬开", "柜门吱呀一声开了。里面只剩一把手枪和两个弹匣。",
      {"xp": 10}, {"pistol_9mm": 1, "ammo_9mm": 6}, req=["item:toolbox>=1"]),
    C("用手掰", "你的手在流血，柜门纹丝不动。",
      {"hp": -6}),
    C("放弃，去别处找", "你听见楼上有动静，决定不在这里耗。",
      {}),
], places=["police_box"], weight=10))

events.append(E("ev_church_candle", "告解室", """告解室的帘子后面有人。你看见一只手垂下来，指甲全黑了。
但另一个隔间里，还有呼吸声。""", [
    C("先看呼吸的那个", "隔间里缩着一个瘦弱的男人，怀里抱着一本圣经。他抬头看见你，第一句话是：”你也是来躲的？“",
      {"flag_met_priest": 1, "sanity": 4}, {"book": 1}),
    C("拉开帘子", "那只手动了。你后退两步，铃铛在门框上响了一声。",
      {"sanity": -5, "xp": 6}),
    C("点燃蜡烛", "火光让整个教堂亮起来。你看见长椅上摆着一排排鞋子，都是小孩子的。",
      {"sanity": -8, "xp": 10}, {"cigar": 1, "whiskey": 1}),
], places=["church"], weight=12, once=True))

events.append(E("ev_supermarket_freezer", "冷库", """冷库门被从里面顶住了。门把手上结着霜，还有几道抓痕。""", [
    C("打开门", "一股白雾涌出来。里面站着四个人，冻得像雕塑，姿势却都是站着的。你关上门，锁好。",
      {"sanity": -8, "xp": 10}, {"canned_food": 3, "spam": 1}),
    C("从通风口爬进去", "你在里面找到一箱罐头，还有一具蜷成一团的尸体，身上穿着写着别人名字的工服。",
      {"fatigue": 12, "sanity": -6}, {"canned_food": 4, "jerky": 1, "work_boots": 1}),
    C("不碰它", "你绕开冷库。这个决定让你活得更久。",
      {"sanity": 2}),
], places=["supermarket"], weight=12, once=True))

events.append(E("ev_metro_dark", "地铁隧道", """隧道深处有光，一闪一闪，像有人在换灯泡。
这里离地面三十米，空气是暖的。""", [
    C("朝光走", "你走了二十分钟，找到一处用应急灯照明的避难室。桌上摆着六罐水，一张纸条：”祝你比我走运。“。",
      {"sanity": 6, "xp": 12}, {"water_bottle": 4, "canned_food": 2, "light_core": 1}),
    C("留在原地听", "你听见光的方向传来金属敲击声，三短一长，重复。是有人在发信号。",
      {"xp": 10, "flag_metro_signal": 1}),
    C("返回地面", "你不想在地底遇到任何东西。",
      {}),
], places=["subway_station", "subway_hub"], weight=12, once=True))

events.append(E("ev_gas_pump", "没有油的加油站", """油枪全被拔了，地上有柴油的痕迹。
办公室的灯还亮着，里面有人在翻抽屉。""", [
    C("悄悄退走", "你退回车里，听见抽屉被拉开又合上的声音。",
      {}),
    C("敲门", "里面的人骂了一句，然后门开了一条缝。是个戴着脏围裙的中年人，手里握着扳手。”要油？五罐水换一桶。“。",
      {"flag_met_mechanic": 1, "xp": 8}, {"water_bottle": -5, "fuel": 2}, req=["item:water_bottle>=5"]),
    C("等他走", "他在里面待了很久，最后从后窗走了。你进去找到半桶柴油。",
      {"sanity": -2}, {"fuel": 2}),
], places=["gas_station", "rest_stop"], weight=10))

events.append(E("ev_apartment_stair", "楼梯间的涂鸦", """从一楼到六楼，墙上写满了同一句话："不要开 602。"。
字迹从工整变得潦草，最后几层几乎是划出来的。""", [
    C("打开 602", "门里是空的。墙上有血，地上有拖痕，一直延伸到阳台。你听见头顶有呼吸声。",
      {"sanity": -7, "xp": 8}, {"light_core": 1}),
    C("听话，不打开", "你从 601 的阳台翻了下去。脚落地的时候，你听见 602 的门开了。",
      {"sanity": -2, "fatigue": 6}),
    C("在楼下等", "你等了半小时，什么也没发生。你选择相信那行字。",
      {"xp": 4}),
], places=["apartment"], weight=8))

# ============ 工业区 ============
events.append(E("ev_warehouse_container", "集装箱", """一整排集装箱，只有中间那扇门是开的。
里面有光，还有人说话，声音很小，像在开会。""", [
    C("靠近听", "他们在讨论怎么攻下附近的避难所。你记下了他们的数量：七个。",
      {"xp": 12, "flag_raider_plan": 1}),
    C("从背后绕过去", "你从集装箱缝隙里穿过去，在另一边找到一个没锁的箱子，里面是军用口粮。",
      {"fatigue": 8}, {"mre": 2, "military_biscuit": 2}),
    C("扔个燃烧瓶进去", "火光冲起来的时候你已经在跑了。身后传来惨叫，有人类的声音。",
      {"sanity": -12, "xp": 20, "vulture": -6}, {"molotov": -1}, req=["item:molotov>=1"]),
], places=["warehouse", "freight_yard"], weight=11))

events.append(E("ev_factory_machine", "还在运转的机器", """一台冲压机还在工作，每四秒砸一下，砸了大概四十天。""", [
    C("关掉它", "你拉下电闸，世界突然安静得让你耳鸣。你在机器下面找到半截袖子。",
      {"sanity": 4, "xp": 10}, {"scrap": 3, "steel_plate": 1}),
    C("利用它做陷阱", "你花了两个小时调整行程，让冲压机对着门口。今晚能睡个好觉。",
      {"xp": 14, "fatigue": 8, "flag_factory_trap": 1}, {"steel_plate": 1}),
    C("拆零件", "你拆下电机和铜线，手上全是油。",
      {"fatigue": 10}, {"copper": 3, "wire": 3, "spring": 2}),
], places=["factory"], weight=10, once=True))

events.append(E("ev_chem_leak", "泄漏", """绿色气体从破裂的管道里慢慢渗出来，贴着地面流动。""", [
    C("戴上面具进去", "面具里全是自己的呼吸声。你摸到一排试剂瓶，塞进包里就走。",
      {"infection": 5, "fatigue": 8}, {"chemical": 3, "filter_core": 1}, req=["item:gas_mask>=1"]),
    C("用湿布捂住口鼻冲进去", "你憋了四十秒，出来的时候咳得跪在地上。",
      {"hp": -12, "infection": 6}, {"chemical": 2}),
    C("绕开", "你从围墙外面绕了一大圈。",
      {"fatigue": 4}),
], places=["chem_plant"], weight=12))

events.append(E("ev_water_plant_quiet", "沉淀池", """水面很平静，平静得不对。
池边有一排鞋，摆得很整齐，鞋头朝外。""", [
    C("看看水里", "水底下有很多影子，都保持着站立的姿势。你后退时踩到了什么，水面荡开一圈波纹。",
      {"sanity": -9, "xp": 10}),
    C("把鞋收起来", "你不知道为什么这么做。回去的路上你一直想着那些脚。",
      {"sanity": -3}, {"work_boots": 1}),
    C("取水", "你灌满了所有容器，烧开之后大概能喝。",
      {"infection": 2}, {"water_dirty": 4}, req=["item:canteen>=1"]),
], places=["water_plant"], weight=10, once=True))

events.append(E("ev_junkyard_crown", "铁王冠", """废料堆的顶端坐着一个巨大的人形，头上戴着一顶用轮毂做成的王冠。
它没有动。它身边的废铁在动。""", [
    C("绕开它", "你贴着墙走，脚下每一声响都像雷。它始终没有转头。",
      {"fatigue": 10, "sanity": -4}),
    C("爬上废料堆，从另一侧搜刮", "你在它背后找到一箱工具，还有一枚核心。它一直看着城市的方向。",
      {"xp": 16, "sanity": -6}, {"light_core": 1, "toolbox": 1, "carbon": 1}),
    C("向它开枪", "子弹打在它头上，发出金属的声音。它慢慢站了起来。",
      {"xp": 10, "sanity": -8}, {"ammo_762": -3}, fight="boss_rustking", req=["item:ammo_762>=3"]),
], places=["junkyard"], weight=14, once=True, min_day=8))

events.append(E("ev_tunnel_block", "堵住的隧道", """三辆车撞在一起，把隧道堵死了一半。
中间的缝隙只能侧身过去，里面很黑。""", [
    C("侧身挤过去", "你在黑暗里走了很久，感觉有东西碰到了你的腿，但你没有低头看。",
      {"fatigue": 12, "sanity": -6, "xp": 12}, {"light_core": 1}),
    C("从车顶翻过去", "车顶锈得厉害，你踩穿了一块，小腿被划了一道。",
      {"hp": -10, "fatigue": 6}, {"scrap": 2}),
    C("炸开它", "爆炸声在隧道里滚了很久。路通了，但你的耳朵嗡了一整天。",
      {"hp": -6, "fatigue": -4, "xp": 14}, {"pipe_bomb": -1}, req=["item:pipe_bomb>=1"]),
], places=["tunnel"], weight=10, once=True))

# ============ 近郊农野 ============
events.append(E("ev_farm_well", "井", """井水很清，绳子还在。你打上来一桶，水面上浮着一枚戒指。""", [
    C("喝一口", "水很甜。你已经很久没喝过这么甜的东西了。",
      {"thirst": 34, "sanity": 6}, {"wedding_ring": 1}),
    C("先把水烧开", "你花了半小时生火。喝的时候，天已经黑了。",
      {"thirst": 26, "fatigue": 6}, {"water_boiled": 2}),
    C("下到井里看看", "井壁上有一个洞，洞里塞着铁盒。你打开它，里面是一把钥匙和半张地图。",
      {"fatigue": 14, "sanity": -4, "xp": 12}, {"map_fragment": 1, "lockpick": 1, "light_core": 1}),
], places=["farm"], weight=12, once=True))

events.append(E("ev_barn_loft", "干草堆", """干草堆得比人高。你听见里面有呼吸声，很轻。""", [
    C("用叉子戳一下", "草堆里跳出一个男孩，十三四岁，手里握着一把折叠刀。他看见你，刀掉在了地上。",
      {"flag_met_conor": 1, "sanity": 4, "xp": 8}, {"candy": 2}),
    C("说「我走了」", "你退出去的时候，草堆动了一下。你假装没看见。",
      {"sanity": -2}),
    C("在草堆边上放一罐食物", "第二天你回来，罐头空了，旁边摆着一颗子弹。",
      {"sanity": 8, "xp": 6}, {"canned_food": -1, "ammo_9mm": 1}),
], places=["barn"], weight=10, once=True))

events.append(E("ev_lake_boat", "船", """栈桥尽头拴着一条小船，船里有半桶水和一支鱼竿。
对岸的雾里，有什么东西在移动。""", [
    C("划过去", "雾散开的时候，你看见岸边停着十几条船，全都空着。你划了回去。",
      {"fatigue": 10, "sanity": -4, "xp": 12}, {"fishing_rod": 1, "water_bottle": 2}),
    C("拿了鱼竿就走", "你不想知道对岸有什么。",
      {}, {"fishing_rod": 1}),
    C("在船上钓一会儿", "你钓上来一条你叫不出名字的鱼。它有三只眼睛。",
      {"sanity": -2, "xp": 6}, {"rat_meat": 2}),
], places=["lake_dock"], weight=10, once=True))

events.append(E("ev_campsite_tent", "帐篷里的日记", """帐篷里睡袋还是铺开的，旁边放着一本日记。
最后一页写着："今天听见了狗叫。如果明天还听得见，就说明附近还有活人。"。""", [
    C("带上日记", "你把它塞进背包。也许有一天能读到结尾。",
      {"sanity": 4, "xp": 6}, {"book": 1}),
    C("在附近搜一圈", "你找到一把折叠铲和几个罐头，还有一双晒干的袜子。",
      {}, {"canned_food": 2, "work_boots": 1}),
    C("睡在这里", "你躺进别人的睡袋，闻着陌生的味道，很快就睡着了。",
      {"fatigue": -20, "sanity": 4}, {"sleeping_bag": 1}),
], places=["campsite"], weight=10, once=True))

events.append(E("ev_orchard_ferment", "发酵的果园", """落果发酵的味道飘得很远。你听见有很多东西在果树林里动。""", [
    C("慢慢摘", "你摘了满满一袋，没惊动任何东西。",
      {}, {"wild_berry": 4, "honey": 1}),
    C("摇树", "果子像雨一样落下来。也把七八个影子引了过来。",
      {"xp": 8}, {"wild_berry": 6}, fight="hound_pack"),
    C("不摘了", "你退了出去。",
      {}),
], places=["orchard"], weight=10))

events.append(E("ev_quarry_blast", "采石场", """爆破员的安全日志还挂在墙上，最后一页写着："明天最后一次爆破。"。
下面画了一个箭头，指向工具箱。""", [
    C("打开工具箱", "里面是炸药、雷管和一本手写笔记。",
      {"xp": 12}, {"gunpowder": 3, "pipe_bomb": 2, "book": 1}),
    C("按笔记找爆破点", "你在标记的位置挖出一个铁箱，里面是工程队留下的补给。",
      {"fatigue": 12, "xp": 16}, {"fuel": 2, "steel_plate": 2, "light_core": 1}),
    C("离开", "你听见山壁那边有石头滚落的声音。",
      {}),
], places=["quarry"], weight=10, once=True))

events.append(E("ev_apiary_swarm", "蜂群", """蜂箱还活着。蜜蜂在空气里织出一层黑纱。
其中一只落在你手背上，停了一会儿，没有蜇你。""", [
    C("慢慢取蜜", "你割下一块蜂巢，甜味在嘴里化开。",
      {"sanity": 10}, {"honey": 2, "wax": 1}),
    C("用烟熏", "你点了湿草，烟雾让蜂群安静下来。",
      {"fatigue": 6}, {"honey": 3, "wax": 2}),
    C("烧掉蜂箱", "火光里有密集的爆裂声。你不想在这里遇到别的。",
      {"sanity": -4}, {"honey": 1, "charcoal": 2}),
], places=["apiary"], weight=9))

# ============ 军事区 ============
events.append(E("ev_checkpoint_gate", "检查站", """沙袋后面有人喊话："停下。把武器放在地上，往前走十步。"。
枪口一直对着你。""", [
    C("照做", "他们搜了身，登记了名字，给了你一瓶水和一张过期通行条。”你们现在归我们管了，“中士说。",
      {"military": 4, "sanity": 4, "xp": 10, "flag_checkpoint_pass": 1}, {"water_bottle": 2, "military_biscuit": 2}),
    C("谈判", "中士听完你的话，沉默了很久。”灯塔？我们三个月前就放弃那条线了。“他给了你一些补给，让你走。",
      {"military": 2, "xp": 12, "sanity": 2}, {"mre": 1, "ammo_556": 5}),
    C("掉头就走", "你听见身后有人骂了一句，但没有开枪。",
      {"sanity": -2}),
], places=["checkpoint"], weight=14, once=True, min_day=3))

events.append(E("ev_armory_door", "第三道门", """门上有一个读卡器，红灯在闪。
门缝里飘出枪油和铁锈的味道。""", [
    C("刷卡", "绿灯亮起。门后面是一排空枪架，只有最里面那层还放着东西。",
      {"xp": 14}, {"rifle_ar": 1, "ammo_556": 12, "light_core": 1}, req=["item:military_keycard>=1"]),
    C("用焊枪切", "火花在昏暗里很亮。门开了，但也把附近的东西引来了。",
      {"fatigue": 14}, {"rifle_ak": 1, "ammo_762": 8}, fight="armored_swat", req=["item:welder>=1"]),
    C("离开", "你没有钥匙，也不想用手去撬。",
      {}),
], places=["armory"], weight=14, once=True, min_day=4))

events.append(E("ev_field_hospital_ward", "7 号病床", """7 号床上躺着一个人，胸口还在起伏。
他的手腕上系着红色标签，上面写着「实验组 B」。""", [
    C("救他", "他醒来后看着你，第一句话是：”别让白鸦找到我。“。",
      {"flag_met_deserter": 1, "sanity": 5, "xp": 14}, {"bandage": -1, "antibiotics": -1}, req=["item:bandage>=1"]),
    C("拔掉他的输液管", "他很快就不动了。你在他枕头下面找到一张门禁卡。",
      {"sanity": -14, "xp": 8}, {"military_keycard": 1, "lab_sample": 1}),
    C("安静地离开", "你退出病房，把门带上。",
      {"sanity": -3}),
], places=["field_hospital"], weight=12, once=True))

events.append(E("ev_radar_console", "雷达控制台", """屏幕上有一个缓慢移动的亮点，每转一圈就靠近一点。
桌上有半杯冷掉的咖啡。""", [
    C("调整天线", "亮点消失了。你希望那是因为它走了。",
      {"xp": 12, "sanity": -2, "flag_radar_clear": 1}, {"radio_part": 1}),
    C("记录坐标", "你把坐标抄下来，发现那个点在灯塔方向。",
      {"xp": 16, "flag_lighthouse_known": 1}, {"map_fragment": 1, "radio_codebook": 1}),
    C("对着屏幕开枪", "玻璃碎了一地。亮点还在，只是不那么清楚了。",
      {"sanity": -5}, {"ammo_9mm": -2}),
], places=["radar_station"], weight=11, once=True))

events.append(E("ev_lab_decon", "消毒间", """你按下按钮，喷头喷出白色的雾，味道像医院。
玻璃窗外，有一个穿白大褂的人正看着你，一动不动。""", [
    C("走出去和他说话", "他开口的第一句话是：”你有抗体吗？“ 你摇头。他点点头，转身走了。",
      {"whitecrow": 3, "xp": 14, "flag_whitecrow_contact": 1}, {"lab_sample": 1}),
    C("等雾气散尽再走", "你等了十分钟。窗外已经没人了。",
      {"sanity": -2}),
    C("从另一扇门离开", "你绕过走廊，在储藏室找到几个冷冻箱。",
      {"xp": 10}, {"blood_sample": 1, "chemical": 2, "antibiotics": 2}),
], places=["lab_whitecrow"], weight=14, once=True))

events.append(E("ev_bunker_generator", "掩体发电机", """柴油机还在响，声音很稳。
控制台上贴着一张纸："燃料耗尽前，请撤离。已停机 46 天。"。""", [
    C("加油，重启主电源", "灯一盏接一盏亮起来，整个掩体都在嗡鸣。通风也恢复了。",
      {"xp": 20, "sanity": 6, "flag_bunker_online": 1}, {"fuel": -2}, req=["item:fuel>=2"]),
    C("拆发电机零件", "你拆下需要的东西。柴油机的声音渐渐慢下来，最后停了。",
      {"sanity": -4, "xp": 14}, {"generator_part": 2, "copper": 3, "wire": 3}),
    C("搜宿舍区", "你在铁柜里找到一封没寄出的家书，和一把钥匙。",
      {"xp": 10}, {"photo": 1, "light_core": 1, "military_keycard": 1}),
], places=["bunker"], weight=14, once=True))

events.append(E("ev_train_choice", "列车长", """列车的最前面，驾驶室门开着。
一个穿铁路制服的男人坐在里面，脖子上挂着一串钥匙，膝盖上放着一把猎枪。
"这列车归我，"他说，"你想去哪，拿东西来换。"。""", [
    C("用手表换一次搭车", "他看了看表，笑了。”成交。“车开了三个小时，把你送到了城市边缘。",
      {"fatigue": -10, "xp": 16, "flag_train_ride": 1}, {"watch": -1}, req=["item:watch>=1"]),
    C("用燃料换车厢物资", "他让你搬了两箱东西下车，还多给了你一个弹匣。",
      {"xp": 12}, {"fuel": -2, "mre": 3, "ammo_762": 8}, req=["item:fuel>=2"]),
    C("拒绝，离开", "他在你身后说：”你会回来的。“。",
      {}),
    C("动手抢列车", "他叹了口气，把猎枪抬起来。”我在这里等了半年，就为了不被人抢。“。",
      {"xp": 10}, {}, fight="boss_trainman", ending=None),
], places=["supply_train"], weight=16, once=True, min_day=6))

events.append(E("ev_comm_tower_climb", "塔顶", """你爬到一半，风大得几乎站不稳。
塔顶的灯还在闪，频率很慢，像心跳。""", [
    C("继续爬", "塔顶有一具穿着安全绳的尸体，怀里抱着一个工具箱。你取下箱子，向他点了点头。",
      {"fatigue": 20, "sanity": -4, "xp": 20}, {"radio_part": 2, "light_core": 1, "binoculars": 1}),
    C("在平台休息", "你坐在铁梯上，看着整座城市。它很安静，安静得像一张照片。",
      {"fatigue": -12, "sanity": 8}),
    C("下塔", "你不想在这么高的地方遇到夜行者。",
      {}),
], places=["comm_tower"], weight=10, once=True))

events.append(E("ev_ammo_tripwire", "绊雷", """你的脚停在半空。
一根鱼线横在门框上，连着墙上的手雷。""", [
    C("剪断它", "你掏出钳子，手很稳。线断了。你在地上坐了很久。",
      {"sanity": -4, "xp": 12}, {"grenade": 2}),
    C("从下面爬过去", "你趴在地上，一点一点挪过去，衣服全湿透了。",
      {"fatigue": 10, "xp": 8}),
    C("退出去", "你退了三步，转身就跑。",
      {}),
], places=["ammo_depot", "bunker", "checkpoint"], weight=10))

# ============ 城市核心 ============
events.append(E("ev_cityhall_vault", "市政厅金库", """地下室的铁门上贴着封条，日期是爆发前三天。
门缝里有钱的味道，还有别的味道。""", [
    C("开门", "里面堆着成捆的现金和三个箱子。箱子是打开的，里面是空的。地上有拖痕。",
      {"sanity": -4, "xp": 14}, {"jewelry": 2, "gold_ring": 2, "light_core": 1}),
    C("找通风管进去", "你在管道里爬了十几米，出来的时候浑身是灰。你找到了一份文件。",
      {"fatigue": 14}, {"radio_codebook": 1, "hard_drive": 1}),
    C("不进去", "你听见里面有人在数钱。",
      {}),
], places=["city_hall"], weight=12, once=True))

events.append(E("ev_stadium_horde", "看台", """看台上坐满了人，几万个人，全都朝着球场中央。
球场中央搭着一个台子，台子上有一张空椅子。""", [
    C("悄悄穿过看台", "你贴着最外圈走，脚下的可乐瓶每一步都在响。没有一张脸转过来。",
      {"sanity": -10, "xp": 20, "fatigue": 10}),
    C("走向球场中央", "你走上台的时候，所有椅子同时响了一声。椅子上的东西都站了起来。",
      {"sanity": -20, "xp": 30}, fight="boss_mother"),
    C("走上台，坐上那张椅子", "木头很凉。几万个人同时站起来，转向你。你听见自己的名字被念了一遍，用很多种声音。",
      {"sanity": -30, "xp": 30}, {}, ending="end_mother"),
    C("离开体育场", "你不想知道那张椅子是给谁准备的。",
      {}),
], places=["stadium"], weight=16, once=True, min_day=8))

events.append(E("ev_cathedral_ritual", "祭坛", """祭坛上摆着十几枚核心，围成一个圈。
灰袍牧师站在中间，手里举着针管。"你来了，"他说，"你是最后一个。"。""", [
    C("听他讲完", "他讲了二十分钟。你听懂了：他要给所有人注射，让灰烬之后的新生开始。",
      {"order": 4, "sanity": -8, "xp": 20}),
    C("打掉他手里的针管", "针管碎了。他笑了。”没关系，“他说，”还有一千支。“。",
      {"xp": 20, "sanity": -6}, fight="boss_preacher"),
    C("拿走核心就走", "你抓了三枚核心，转身跑下台阶。身后传来歌声。",
      {"xp": 25, "sanity": -8}, {"light_core": 3}, fight="cultist_zealot"),
    C("跪下，接受注射", "针头刺入颈侧。你听见自己的心跳慢下来，然后听见了别的东西。",
      {"sanity": -30, "xp": 40}, {}, ending="end_cult"),
    C("放下刀，转身离开", "你走出教堂。身后没有脚步声，只有歌声。你走了很远才发现自己在哭。",
      {"sanity": 6, "xp": 20}, {}, ending="end_mercy"),
], places=["cathedral"], weight=18, once=True, min_day=6))

events.append(E("ev_lighthouse_arrival", "白塔", """门是开着的。楼梯上亮着应急灯，一圈一圈往上。
塔顶有发电机的声音，还有一个女人在哼歌。
"上来吧，"她说，"我等你很久了。"。""", [
    C("交出 6 枚核心", "她把核心一枚一枚嵌进控制台。灯塔的光变了颜色，从白变成很淡的蓝。”可以了，“她说，”现在我们可以开始做疫苗了。“。",
      {"xp": 100, "sanity": 30, "military": 3}, {"ending": "win_light"}, req=["item:light_core>=6"]),
    C("交出核心，但要求先见所有人", "你见到了塔里的七个人，包括那个每天念坐标的女人。她比你想的年轻，也更累。",
      {"xp": 80, "sanity": 20}, {"ending": "win_stay"}, req=["item:light_core>=6"]),
    C("烧掉灯塔，让所有人无法再利用它", "你把燃料泼在发电机上。火光从塔顶烧到塔底，照亮了整片海。",
      {"sanity": -20, "xp": 60}, {"ending": "win_burn"}, req=["item:fuel>=2"]),
    C("不交核心，离开", "你转身下楼。她在背后说：”你会回来的。“。",
      {"sanity": -4}, {}),
], places=["lighthouse"], weight=100, once=False, min_day=1))

events.append(E("ev_harbor_boat", "港口的船", """一艘渔船还浮在水面上，油箱里有一半油。
海面上有雾，雾里有灯。""", [
    C("发动它，离开这座城市", "引擎响了三下才点着。你驶进雾里，身后的城市慢慢变小。",
      {"xp": 60, "sanity": 20}, {"ending": "win_boat"}, req=["item:fuel>=1"]),
    C("检查船舱", "船舱里有一具尸体，身边放着三箱罐头和一封没写完的信。",
      {"sanity": -4, "xp": 12}, {"canned_food": 3, "fuel": 1, "wedding_ring": 1}),
    C("留在岸上", "你看着那条船，想了很久，最后把油桶放回了仓库。",
      {"sanity": 2}),
], places=["harbor"], weight=20, once=True, min_day=5))

events.append(E("ev_incinerator_furnace", "焚化炉", """炉膛里还有火。传送带在转，上面躺着东西。
控制室的记录本上写着："日处理量：47。"。""", [
    C("关掉传送带", "机器停了。你在传送带上找到一枚核心，还有一件小小的外套。",
      {"sanity": -10, "xp": 20}, {"light_core": 1, "child_drawing": 1}),
    C("爬上炉顶看看", "炉口的热浪让你睁不开眼。你看见里面有一个没有被烧完的人，还在动。",
      {"hp": -10, "sanity": -12, "xp": 24}, fight="boss_ash"),
    C("离开", "你退了出去。身后的传送带还在响。",
      {}),
], places=["incinerator"], weight=14, once=True))

events.append(E("ev_subway_nest", "巢", """隧道尽头是一堵肉做的墙，还在轻轻起伏。
墙上嵌着很多人的东西：眼镜、鞋、钥匙、一枚核心。""", [
    C("取下核心", "你伸手的时候，墙睁开了眼。",
      {"xp": 30, "sanity": -15}, {"light_core": 1}, fight="boss_hive"),
    C("放火烧", "火焰沿着墙爬上去，发出很长的声音。你退到站台，看着隧道被照亮。",
      {"sanity": -10, "xp": 26}, {"molotov": -2}, fight="boss_hive", req=["item:molotov>=2"]),
    C("悄悄退走", "你退出去的时候，墙上的嘴动了一下。",
      {"sanity": -6}),
], places=["subway_hub"], weight=16, once=True, min_day=6))

events.append(E("ev_overpass_jam", "高架上的车流", """车堵得看不到头。有几辆车的后备箱是开的。
风很大，桥在轻轻晃。""", [
    C("翻后备箱", "你找到一只行李箱、一箱水和一个儿童安全座椅。",
      {"fatigue": 8}, {"suitcase": 1, "water_bottle": 2, "child_drawing": 1}),
    C("在车流里睡一觉", "车座比床还舒服。你醒来时，天已经黑了，桥下有东西在看你。",
      {"fatigue": -20, "sanity": -3}),
    C("看看桥下", "桥下密密麻麻，全是站着的影子。它们都仰着头。",
      {"sanity": -10, "xp": 8}),
], places=["overpass"], weight=10))

events.append(E("ev_tv_tower_elevator", "电梯", """电梯停在 17 层和 18 层之间，轿厢里有人。
那个人正在敲电梯门，一下，一下，很有耐心。""", [
    C("撬开电梯门", "轿厢里只有一个对讲机，还在响。你按下通话键，对面说：”有人吗？“",
      {"xp": 16, "sanity": 6, "flag_tower_voice": 1}, {"walkie": 1, "radio_part": 1}),
    C("朝里面喊", "敲门声停了。然后，整栋楼的应急灯同时灭了。",
      {"sanity": -8, "xp": 6}),
    C("爬楼梯上去", "你爬到塔顶，花了很久。城市在脚下，很安静。",
      {"fatigue": 20}, {"binoculars": 1}),
], places=["tv_tower"], weight=12, once=True))

events.append(E("ev_station_announce", "广播仍在继续", """站内广播还在循环："开往北站的 K417 次列车即将进站，请旅客站在黄色安全线内。"。
站台上站着很多人，都站在黄线内。""", [
    C("沿着黄线走", "你贴着墙走完了整个站台。没有人转头，但你能感觉到所有的眼睛。",
      {"sanity": -12, "fatigue": 8, "xp": 16}),
    C("登上列车", "车厢里空无一人，座位上摆着一只行李箱和一个信封。",
      {"sanity": -4, "xp": 14}, {"suitcase": 1, "photo": 1, "light_core": 1}),
    C("拉下紧急制动", "警铃响彻整个车站。所有站着的人同时转过了头。",
      {"sanity": -20, "xp": 24}, fight="walker_fresh"),
], places=["central_station"], weight=14, once=True))

# ============ 剧情 / NPC ============
events.append(E("ev_meet_nurse", "白大褂", """她坐在医院的台阶上，膝盖上摊着一本笔记，正在写字。
听见脚步，她没有抬头，只是说："如果你是来抢药的，左边柜子里还有一点。"。""", [
    C("我不是来抢东西的", "她终于抬头。她说她叫林晚，以前是急诊科护士。她愿意跟你走，但有个条件：别丢下伤员。",
      {"flag_met_nurse": 1, "sanity": 6, "whitecrow": 1, "xp": 14}, {"bandage": 2}),
    C("问她关于白鸦", "她说白鸦在找免疫者，给的报酬很高，但没人回来过。",
      {"xp": 12, "whitecrow": 1, "flag_whitecrow_warning": 1}, {}),
    C("抢走她的药", "她没有反抗，只是在你走远之后说了一句：”你会需要我的。“。",
      {"sanity": -10, "whitecrow": -4}, {"bandage": 3, "antibiotics": 2, "pills_pain": 2}),
], places=["pharmacy", "clinic", "field_hospital"], weight=13, once=True, min_day=3))

events.append(E("ev_meet_mechanic", "柴油味", """一个戴护目镜的女人从车底下滑出来，手里还攥着扳手。
"你踩到我的扳手了，"她说，"不过没关系，反正我也修不好它。"。""", [
    C("帮她修", "你们搞了三个小时，引擎居然点着了。她大笑，声音在厂房里撞来撞去。",
      {"flag_met_mechanic": 1, "sanity": 8, "xp": 16}, {"wrench": 1}),
    C("问她能不能改装武器", "她看了看你的家伙，说：”给我一个工作台，我能把它变得比现在更像样。“。",
      {"xp": 10, "flag_met_mechanic": 1}, {}),
    C("问她要不要一起走", "她考虑了一下，说：”我在这里等个人。如果他不回来，我就去找你。“。",
      {"sanity": 4, "flag_met_mechanic": 1, "xp": 10}),
], places=["auto_shop", "factory", "junkyard"], weight=12, once=True, min_day=3))

events.append(E("ev_meet_sergeant", "中士", """他坐在沙袋上擦枪，脚边放着一壶水和一个相框。
相框里是两个穿军装的人，其中一个是他。""", [
    C("向他敬礼", "他愣了一下，然后站起来回礼。”好久没人这么干了，“他说，”坐下吧。“。",
      {"flag_met_sergeant": 1, "military": 4, "sanity": 6, "xp": 14}, {"mre": 2}),
    C("问他检查站还有多少人", "他把弹匣装回去，说：”算上我，六个。你看到的那些沙袋，大部分是空的。“。",
      {"xp": 10, "flag_checkpoint_weak": 1}),
    C("劝他跟你去灯塔", "他摇头：”我的命令是守住这里。命令还没有解除。“。",
      {"sanity": -2, "xp": 8}),
], places=["checkpoint", "armory", "field_hospital"], weight=12, once=True, min_day=4))

events.append(E("ev_meet_trader", "交易", """一个穿西装的老头在站台边摆了个摊，桌布是国旗，商品只有三样：水、子弹、抗生素。
"价格每天变，"他说，"今天很便宜。"。""", [
    C("用废铁换水", "他称了称废铁，递给你四瓶水。”明天涨价，“他说。",
      {}, {"scrap": -4, "water_bottle": 4}, req=["item:scrap>=4"]),
    C("用金戒指换抗生素", "他把戒指对着光看了看，收进内袋，推过来两盒药。",
      {}, {"gold_ring": -1, "antibiotics": 2}, req=["item:gold_ring>=1"]),
    C("用情报换子弹", "你告诉他检查站的巡逻时间。他很满意，给了你两个弹匣。",
      {"military": -2, "vulture": 1}, {"ammo_9mm": 8}, req=["flag:checkpoint_pass>=1"]),
], places=["central_station", "rest_stop", "checkpoint"], weight=12, once=False, min_day=3))

events.append(E("ev_meet_hunter", "猎人", """他蹲在树杈上，弓半开，箭头对着你。
"别动，"他说，"我在确认你有没有被咬。"。""", [
    C("卷起袖子给他看", "他看了很久，然后从树上跳下来，把弓收好。”上来吧，我烤了肉。“。",
      {"flag_met_hunter": 1, "xp": 14, "sanity": 4}, {"cooked_meat": 2}),
    C("让他别废话", "他笑了一下，松开弓弦，箭擦着你的耳朵钉在树上。”下次我不会偏。“。",
      {"hp": -5, "xp": 6, "sanity": -3}),
    C("问他有没有见过灯塔的人", "他说见过。上个月有一队人往那边走，七个人，最后只剩一个女孩子到塔下。",
      {"xp": 16, "flag_lighthouse_known": 1}, {"map_fragment": 1}),
], places=["orchard", "barn", "lake_dock", "apiary"], weight=12, once=True, min_day=3))

events.append(E("ev_meet_kid", "那孩子", """她躲在货架后面，抱着一只脏兮兮的兔子玩偶。
看见你，她没有跑，只是把玩偶抱得更紧。""", [
    C("蹲下来和她说话", "她问她妈妈在哪。你说不知道，但可以带她去找。她点了点头，牵住了你的手。",
      {"flag_met_kid": 1, "sanity": 10, "xp": 10}, {"candy": 1}),
    C("给她一罐食物就走", "你走出一段路回头看，她还站在原地，抱着那只兔子。",
      {"sanity": -4}, {"canned_food": -1}),
    C("带她回据点", "路上她一直没说话。到门口时，她问：”这里会有怪物吗？“ 你说不会。",
      {"flag_met_kid": 1, "sanity": 12, "xp": 16}, {}, req=["companions>=1"]),
], places=["convenience", "school", "apartment", "stadium"], weight=11, once=True, min_day=4))

events.append(E("ev_meet_priest", "灰袍", """他坐在教堂门口，给每个路过的人递一杯水，不管对方是不是活人。
"喝吧，"他说，"灰烬之后，我们都一样。"。""", [
    C("接过水", "水是温的，有一点苦。喝完你才想起来，他可能给你下了药。但什么也没有发生。",
      {"sanity": 8, "order": 2, "xp": 8}, {}),
    C("问他关于核心", "他指了指教堂里面，”都在祭坛上。你要的话，自己去拿。“。",
      {"xp": 12, "flag_cathedral_core": 1}, {}),
    C("把水泼在他脸上", "他没有生气，只是用袖子擦了擦脸，又倒了一杯。",
      {"order": -4, "sanity": -2}, {}),
], places=["church", "cathedral"], weight=10, once=True))

events.append(E("ev_meet_dog", "铁钉", """那条狗又出现了，嘴里叼着一只死兔子，放在门口，然后退后两步看着你。""", [
    C("收下兔子", "它摇了摇尾巴，趴了下来。兔肉很柴，但你没有一个人吃。",
      {"sanity": 8, "hunger": 12, "flag_dog": 1}, {"rat_meat": 1}),
    C("摸摸它的头", "它很脏，很瘦，但体温是真实的。",
      {"sanity": 10, "flag_dog": 1}),
    C("让它走", "它等了一会儿，叼起兔子走了。",
      {"sanity": -2}),
], places=["safehouse", "apartment", "farm", "barn"], weight=8, once=True, min_day=5))

events.append(E("ev_lighthouse_note", "灯塔明信片", """一张明信片，正面是白塔灯塔，背面用铅笔写着：
"如果你看到这个，说明我还没死。别走桥。别相信穿白大褂的。带够水。——Z"。
邮戳是爆发前两周。""", [
    C("收起来", "你把它放在内袋，和照片、婚戒、孩子的画放在一起。",
      {"sanity": 6, "flag_lighthouse_known": 1, "xp": 10}, {"map_fragment": 1}),
    C("按邮戳地址找过去", "你走了很久，找到一间被烧毁的邮局。灰里有半枚核心。",
      {"fatigue": 14, "sanity": -4, "xp": 16}, {"light_core": 1}),
    C("丢下", "纸片飘进积水里，很快沉了下去。",
      {"sanity": -3}),
], tag="story", places=["apartment", "school", "convenience", "police_box", "rest_stop"], weight=7, once=True, min_day=3))

events.append(E("ev_core_cache", "核心", """一枚灯塔核心卡在排水沟的铁栅上，外壳上有烧焦的痕迹。
编号是 04。""", [
    C("取出来", "铁栅很沉，你用了撬棍。手上全是铁锈。",
      {"xp": 20, "fatigue": 6}, {"light_core": 1}),
    C("先看看周围", "你绕着街区走了一圈，确认没有东西跟着。回来时，核心还在。",
      {"xp": 24, "fatigue": 10}, {"light_core": 1}),
    C("放弃", "太危险了。你继续往前走。",
      {}),
], tag="story", places=["water_plant", "supermarket", "central_station", "city_hall", "armory"], weight=8, once=True, min_day=3))

# ============ 结局事件 ============
events.append(E("ev_mercy", "投降", """一个掠夺者跪在你面前，枪扔在一边，双手举过头顶。
"我女儿在等药，"他说，"我不是故意要杀人的。"。""", [
    C("放他走", "他爬起来，退着走了很远，才转身跑。你希望他说的是真的。",
      {"sanity": 8, "xp": 14, "mercy": 1}),
    C("杀了他", "你在他口袋里找到一张小女孩的照片。你把照片放在他胸口。",
      {"sanity": -14, "xp": 12}, {"photo": 1, "ammo_9mm": 6}),
    C("让他带路去他家", "他住在两公里外的一间车库里。他的女儿确实在发烧。你把药给了他们。",
      {"sanity": 12, "xp": 20}, {"antibiotics": -2}, req=["item:antibiotics>=2"]),
    C("收他当手下", "他愣了一下，然后低下头。”我叫老周，“他说。”以后你说什么，我做什么。“。",
      {"sanity": 4, "xp": 16}),
], tag="encounter", places=["warehouse", "overpass", "checkpoint", "supermarket"], weight=9, once=True, min_day=5))

events.append(E("ev_bunker_seal", "密封门", """防爆门的控制面板还有电。按下红色按钮，门就会永远关上。
门后面还有人在敲门，敲得很规律。""", [
    C("关门", "门合上时，敲门声停了。你在门后站了很久，直到应急灯熄灭。",
      {"sanity": -12, "xp": 30}, {"ending": "win_bunker"}),
    C("打开门", "门后面是三个孩子和一个老人。他们已经在里面待了一个月。",
      {"sanity": 14, "xp": 24, "flag_bunker_kids": 1}, {}),
    C("不碰它", "你离开了控制室。敲门声还在继续。",
      {"sanity": -4}),
], places=["bunker"], weight=8, once=True, min_day=7))

events.append(E("ev_signals_end", "把信号发出去", """通讯塔的控制台还能用。你可以把灯塔的坐标发出去，覆盖所有频道。
也可能把别的东西引来。""", [
    C("发送坐标", "你按下按钮，红灯变绿。整个频段都在重复那段话。你不知道会有多少人听见。",
      {"xp": 60, "sanity": 20}, {"ending": "win_signal"}, req=["item:radio_part>=1"]),
    C("发送假坐标", "你把坐标改到了城市另一头。做完之后，你在塔顶坐了很久。",
      {"sanity": -10, "xp": 24}, {}),
    C("关掉设备", "你拔掉电源。世界安静了。",
      {"sanity": 2}),
], places=["comm_tower", "tv_tower"], weight=10, once=True, min_day=6))

events.append(E("ev_silence_choice", "安静", """你的耳朵里开始出现一种持续的嗡鸣，像有人在你脑子里拉一根很细的线。
你很久没有听见过别人叫你的名字了。""", [
    C("走出去，坐在街上", "你坐在马路中间，看着天。天是灰的，很漂亮。",
      {"sanity": -20, "xp": 20}, {"ending": "end_silence"}, req=["sanity<=30"]),
    C("回到营地，找个人说话", "你说了两个小时，语无伦次。对方一直在听。",
      {"sanity": 20, "xp": 10}, req=["companions>=1"]),
    C("用疼痛把自己拉回来", "你咬破了自己的手。血腥味让你清醒了一点。",
      {"hp": -6, "sanity": 10}),
], tag="daily", weight=6, once=True, min_day=12))

events.append(E("ev_exile", "驱逐", """营地的人围坐成一圈，没有人看你。
"我们商量过了，"老赵说，"你太危险了。你走吧。"。""", [
    C("收拾东西离开", "他们给了你三天的口粮，然后关上了门。",
      {"sanity": -16, "xp": 16}, {"canned_food": 3, "water_bottle": 2}, req=["companions>=1"]),
    C("争论", "你说了一个小时。最后老赵叹了口气，说：”那就再试一次。“。",
      {"sanity": -6, "xp": 10, "flag_exile_reprieved": 1}, req=["companions>=1"]),
    C("动手", "你打倒了两个人。其他人没有还手。你走出门的时候，听见有人在哭。",
      {"sanity": -24, "hp": -12, "xp": 10}, {"ending": "end_exile"}),
], tag="daily", weight=4, once=True, min_day=12))

events.append(E("ev_devil_deal", "白鸦的邀请", """一个穿防护服的人站在门口，手里提着一个铝箱。
"我们需要你的血，"他说，"作为交换，我们可以保证你活到疫苗做出来的那天。"。""", [
    C("跟他走", "实验室很干净。他们抽了你六管血，然后给了你一张床。你睡了一个没有梦的觉。",
      {"hp": -10, "sanity": -6, "whitecrow": 6, "xp": 40}, {"ending": "win_whitecrow"}),
    C("拒绝", "他点了点头，把铝箱放在门口就走了。箱子里是药和一张名片。",
      {"whitecrow": -2}, {"antibiotics": 2, "serum": 1}),
    C("抢他的箱子", "他跑得比你想象的快。你只抢到了箱子，里面是空的。",
      {"whitecrow": -20, "sanity": -6}, {}),
], places=["lab_whitecrow", "field_hospital", "radar_station"], weight=9, once=True, min_day=5))

events.append(E("ev_ash_choice", "灰", """焚化炉的火光照在墙上，影子动得很慢。
你突然觉得，把一切都烧掉，也许是最干净的做法。""", [
    C("往炉里添燃料", "火变得更亮了。你看着它，直到眼睛发痛。",
      {"sanity": -10, "xp": 20}, {"ending": "end_ash"}),
    C("离开", "你转身走出厂房。外面的天开始亮了。",
      {"sanity": 4}),
], places=["incinerator"], weight=6, once=True, min_day=8))

events.append(E("ev_loop", "隧道尽头", """你第三次走过这个站台。第三次看见同一个广告牌，同一只鞋，同一摊血。
你确定自己一直在往前走。""", [
    C("继续走", "第四次。第五次。你开始数墙上的灯。数到第七盏时，你听见了自己的声音在背后叫你。",
      {"sanity": -24, "xp": 20}, {"ending": "end_loop"}),
    C("停下来，坐下", "你坐了很久。然后你站起来，往回走。这一次，广告牌不见了。",
      {"sanity": -6, "xp": 16}),
    C("朝声音开枪", "回声停了。你顺着铁轨跑出去，摔了两次。",
      {"hp": -8, "sanity": -8, "xp": 12}, {"ammo_9mm": -2}),
], places=["subway_hub", "tunnel", "subway_station"], weight=6, once=True, min_day=9))

events.append(E("ev_tower_accept", "塔顶的回答", """你终于站在了灯塔顶上。控制台是全亮的，屏幕上跳着一句话：
"还有人在听吗？"。
你的手停在按钮上。""", [
    C("回复：我在", "屏幕闪了一下，跳出一行字：”坐标已记录。我们会来找你。谢谢你。“。",
      {"xp": 50, "sanity": 26}, {"ending": "win_stay"}),
    C("回复：别来了，这里什么都没有", "过了很久，屏幕上出现：”明白。祝你好运。“。",
      {"xp": 40, "sanity": 10}, {"ending": "end_witness"}),
    C("关掉控制台", "灯一盏一盏熄灭。你站在黑暗里，听着海浪。",
      {"sanity": -4, "xp": 20}, {"ending": "end_winter"}),
], places=["lighthouse"], weight=5, once=True, min_day=10))

events.append(E("ev_sacrifice", "最后一次注射", """血清只剩一支。你被咬了，伤口在发烫。
把血清给自己，还是留给那个孩子？""", [
    C("留给孩子", "你把针管塞进她手里。她不知道那是什么，但你说要保管好，她就点头了。",
      {"sanity": 20, "xp": 30}, {"ending": "end_sacrifice"}, req=["flag:met_kid>=1"]),
    C("给自己", "针头推进去的时候，你听见自己的心跳慢了下来。你还活着。",
      {"infection": -60, "sanity": -6, "xp": 20}, {"serum": -1}, req=["item:serum>=1"]),
    C("扔掉它", "玻璃在水泥地上碎开。你看着药水渗进灰里。",
      {"sanity": -10, "xp": 10}, {"serum": -1}, req=["item:serum>=1"]),
], places=["lab_whitecrow", "bunker", "field_hospital", "safehouse"], weight=5, once=True, min_day=8))

events.append(E("ev_dog_end", "铁钉", """它躺在门口，肚子上有一道很深的口子。
它看见你，尾巴还是动了一下。""", [
    C("抱着它，等到它不动", "天黑了，然后亮了。你把它埋在门口的树下，用木板做了个牌子。",
      {"sanity": -10, "xp": 20}, {"ending": "end_dog"}, req=["flag:dog>=1"]),
    C("给它包扎", "你知道这没用。但你还是蹲下来，给它缠了绷带。它舔了舔你的手。",
      {"sanity": 8, "xp": 12}, {"bandage": -1}, req=["flag:dog>=1"]),
], places=["safehouse"], weight=4, once=True, min_day=14))

events.append(E("ev_king_ending", "坐上去", """废料堆顶端的椅子空着。王冠就放在扶手上。
城市在脚下，风很大。""", [
    C("戴上王冠", "金属很凉。你坐了下来。从这一刻起，这片废墟归你管。",
      {"xp": 40, "sanity": -10}, {"ending": "end_king"}),
    C("把王冠扔下去", "它滚下废料堆，声音一路响到很远的地方。",
      {"sanity": 8, "xp": 16}),
], places=["junkyard"], weight=4, once=True, min_day=10))

events.append(E("ev_witness_ending", "记录", """你在一间完好的公寓里找到一支笔和一个本子。
窗外是城市，安静得像一幅画。你想把这一切写下来。""", [
    C("开始写", "你写了很久，写到手抽筋。你不知道谁会读到它，但你必须写。",
      {"sanity": 16, "xp": 30}, {"ending": "end_witness"}),
    C("放下笔", "你合上本子。有些事不写下来，也不会忘。",
      {"sanity": 4}),
], places=["apartment", "school"], weight=4, once=True, min_day=15))


events.append(E("ev_serum_triumph", "疫苗", """你按配方把三样东西倒进烧杯：抗体血样、实验样本、化学试剂。
液体先是浑浊，然后慢慢变清。""", [
    C("给自己注射", "针头推进去的时候，你什么都没感觉到。第二天早上，伤口开始结痂。",
      {"hp": 40, "infection": -80, "sanity": 20, "xp": 60}, {"ending": "win_serum"}, req=["item:serum_formula>=1", "item:blood_sample>=1"]),
    C("带上它去灯塔", "你把烧杯封好，放进冷藏箱。灯塔的人会知道该怎么做。",
      {"xp": 40, "sanity": 10}, {"serum": 2, "light_core": 1}, req=["item:serum_formula>=1", "item:blood_sample>=1"]),
    C("放弃", "你把液体倒进了下水道。它流下去的时候，你听见自己松了一口气。",
      {"sanity": -10, "xp": 10}),
], places=["lab_whitecrow", "field_hospital"], weight=8, once=True, min_day=8))

events.append(E("ev_train_escape", "发车", """列车长死了。驾驶室里的钥匙还插着，油表显示还有三分之一。
铁轨一直延伸到雾里。""", [
    C("发动列车", "列车缓缓移动，越来越快。你坐在驾驶室里，看着城市从窗边退后。你不知道铁轨通向哪里，但至少不是这里。",
      {"xp": 60, "sanity": 20}, {"ending": "win_train"}, req=["item:military_keycard>=1"]),
    C("搜空车厢", "你在车厢里找到很多补给，然后把列车钥匙扔进了排水沟。",
      {"xp": 30}, {"mre": 3, "ammo_556": 12, "ammo_762": 12, "light_core": 1}),
    C("离开", "你下了车，走进雾里。",
      {}),
], places=["supply_train"], weight=10, once=True, min_day=8))

# 结局参数规范化
for _e in events:
    for _c in _e["choices"]:
        if "ending" in _c["items"] and _c["items"]["ending"]:
            _c["ending"] = _c["items"].pop("ending")
        else:
            _c["items"].pop("ending", None)

save("events", events)

# 自检：espec 引用
ids = {e["id"] for e in events}
endings = set()
for e in events:
    for c in e["choices"]:
        if c["ending"]:
            endings.add(c["ending"])
        if c["next"] and c["next"] not in ids:
            print("!! next missing", e["id"], c["next"])
print("ending refs:", sorted(endings))
