#!/usr/bin/env python3
# 追加事件（NPC 相遇 / 地点细节 / 每日）
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "LastEmber", "Resources", "Content")

def load(n):
    with open(os.path.join(OUT, n + ".json"), encoding="utf-8") as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{name}: {len(data)}")

def C(text, log, effect=None, items=None, req=None, fight=None,
      chance=100, fail_effect=None, fail_log="", ending=None):
    return {"text": text, "req": req or [], "effect": effect or {}, "items": items or {},
            "fight": fight, "next": None, "chance": chance,
            "effectFail": fail_effect or {}, "log": log, "logFail": fail_log,
            "ending": ending}

def E(id, title, text, choices, tag="encounter", places=None, weight=10, once=True, min_day=1):
    return {"id": id, "title": title, "text": text, "tag": tag, "weight": weight,
            "once": once, "minDay": min_day, "places": places or [], "choices": choices}

new = []
add = new.append

# ---------------- NPC 相遇 ----------------
add(E("ev_meet_doctor", "顾医生", """她把护目镜推到额头上，露出一双熬红的眼睛。
「你有抗体吗？」她问。没等你回答，又低头去看显微镜，「没有也没关系。坐下，我看看你的手。」""", [
    C("伸出手让她检查", "她处理伤口很快，一句话都没多说。结束时她递给你一张纸条，上面是一串坐标。",
      {"flag_met_doctor": 1, "whitecrow": 2, "sanity": 6, "xp": 14}, {"bandage": 2, "antibiotics": 1}),
    C("问她研究什么", "她说她在找一种能让感染停下、又不杀死宿主的东西。「听起来像奇迹，」她说，「但奇迹只是概率问题。」",
      {"xp": 16, "whitecrow": 2, "flag_whitecrow_warning": 1}, {"lab_sample": 1}),
    C("拒绝，保持距离", "她点点头，把护目镜拉回眼睛上。「理解。你这样的人通常活得久一点。」",
      {"sanity": 2}),
], places=["lab_whitecrow", "field_hospital", "clinic"], weight=13, min_day=4))

add(E("ev_meet_cook", "胖婶", """营地后面支着一口大锅，一个女人正往里扔东西。
「来得正好，」她头也不抬，「尝尝。」""", [
    C("喝一口", "味道很奇怪，但你的胃没有抗议。她又给你添了一勺。",
      {"flag_met_cook": 1, "hunger": 24, "sanity": 8, "xp": 8}, {}),
    C("问她从哪弄来的食材", "她笑了笑，「有些问题别问，吃了就行。」",
      {"flag_met_cook": 1, "hunger": 16, "xp": 10}),
    C("帮她把锅端下来", "锅比想象中沉。她看着你，点了点头，「留下吧，我缺个打下手的。」",
      {"flag_met_cook": 1, "sanity": 10, "xp": 12, "fatigue": 6}),
], places=["safehouse", "apartment", "rest_stop", "campsite"], weight=11, min_day=3))

add(E("ev_meet_singer", "阿音", """你顺着歌声找到她。她坐在通讯塔下的折叠椅上，膝盖上放着一支坏掉的麦克风。
「我在练习，」她说，「等电台修好，我要让全城都听见。」""", [
    C("帮她校频率", "你们在杂音里待了一个小时。突然，一个清晰的声音传出来——是她自己的回声。",
      {"flag_met_singer": 1, "sanity": 12, "xp": 16, "flag_lighthouse_known": 1}, {"radio_part": 1}),
    C("告诉她广播会引来东西", "她说，「我知道。但如果没有人出声，活人和死人有什么区别。」",
      {"flag_met_singer": 1, "sanity": 6, "xp": 10}),
    C("坐下来听她唱完", "她唱了一首很老的歌。唱到第二段时，你发现自己在跟着哼。",
      {"flag_met_singer": 1, "sanity": 16, "xp": 8}),
], places=["comm_tower", "tv_tower", "subway_station"], weight=10, min_day=4))

add(E("ev_meet_prisoner", "4207", """拘留室的门锁着，里面的人隔着铁栏看你。
「你有撬棍吗？」他问，「没有也没关系，我可以等。我已经等了很久。」""", [
    C("撬开门", "他走出来，活动了一下手腕，说了声谢谢。他手腕上的编号被烟头烫花了。",
      {"flag_met_prisoner": 1, "sanity": 4, "xp": 14}, {"lockpick": -1}),
    C("问他为什么被关", "他说他炸了一栋楼，楼里有东西。「你可以说我是罪犯，」他说，「也可以说我是清道夫。」",
      {"flag_met_prisoner": 1, "xp": 16, "flag_prisoner_story": 1}),
    C("去别处找工具", "你回来的时候，铁栏后面只剩一具刚死不久的尸体。你分不清他是怎么死的。",
      {"sanity": -6, "xp": 8}),
], places=["police_box", "subway_station", "armory"], weight=10, min_day=4))

add(E("ev_meet_gravedigger", "老掘", """他在教堂后面的空地上挖坑，一个接一个，尺寸都一样。
「你也要一个吗？」他问，语气很客气。""", [
    C("帮他挖", "你们挖到天黑，埋了七个人。他一直没说话，最后说了句：「谢谢。他们不喜欢一个人。」",
      {"flag_met_gravedigger": 1, "sanity": 8, "xp": 16, "fatigue": 12}, {"shovel": 1}),
    C("问他有没有见过核心", "他用铁锹指了指教堂的钟楼，「那上面有一枚。但上面还有人守着。」",
      {"flag_met_gravedigger": 1, "xp": 14, "flag_cathedral_core": 1}),
    C("离开", "他在你身后继续挖。铲子入土的声音很有节奏。",
      {"sanity": -3}),
], places=["church", "field_hospital", "cathedral"], weight=10, min_day=3))

add(E("ev_meet_deserter", "李默", """他缩在防爆门后面，枪口对着你，手在抖。
「你不是他们的人吧？」他问，「你说句话，随便什么，让我听听像不像人。」""", [
    C("说：我不是", "他放下枪，靠着墙坐下，很久才说：「谢谢。我已经三天没听过人说话了。」",
      {"flag_met_deserter": 1, "sanity": 8, "xp": 16, "military": -2}, {"ammo_556": 6}),
    C("告诉他军方在找他", "他笑了一下，「他们早就不找了。他们连自己都找不到。」",
      {"flag_met_deserter": 1, "xp": 12, "flag_deserter_trust": 1}),
    C("把枪口对准他", "他闭上眼睛，「动手吧。别打肚子，打头。」你最后没有开枪。",
      {"sanity": -8, "xp": 8, "hp": -2}),
], places=["bunker", "airstrip", "checkpoint"], weight=11, min_day=5))

add(E("ev_meet_engineer", "老吴", """他蹲在变电站的柜子前，嘴里叼着手电，手里一团电线。
「别踩那根红的，」他含混地说，「也别踩那根蓝的。」""", [
    C("帮他打手电", "两个小时后，一排指示灯亮了起来。他站起来，拍了拍你的肩，「你救了我一双手。」",
      {"flag_met_engineer": 1, "sanity": 8, "xp": 18}, {"wire": 3, "battery": 2}),
    C("问他要不要加入", "他看了看自己的工具箱，「管饭吗？管饭我就去。」",
      {"flag_met_engineer": 1, "xp": 14, "flag_engineer_join": 1}),
    C("只搜刮，不打扰", "他头也没抬。你在门口找到一卷电线和几节电池。",
      {"xp": 6}, {"wire": 2, "battery": 1}),
], places=["substation", "factory", "armory"], weight=10, min_day=4))

add(E("ev_meet_teacher", "苏老师", """她站在教室前面，对着空椅子念名字。
「王小雨。」她停顿两秒，「到。」然后念下一个。""", [
    C("等她念完", "她念了三十七个名字。最后一个是她自己。她合上本子，看向你，「你是新来的吗？」",
      {"flag_met_teacher": 1, "sanity": -4, "xp": 16}, {"child_drawing": 2}),
    C("告诉她学校已经不安全了", "她点点头，「我知道。但孩子们还没回来，我不能走。」",
      {"flag_met_teacher": 1, "sanity": 6, "xp": 12}),
    C("替她念完剩下的名字", "你念到第十个时，声音开始发抖。她把手放在你肩上，说：「慢一点，他们不着急。」",
      {"flag_met_teacher": 1, "sanity": 10, "xp": 20}),
], places=["school", "apartment", "stadium"], weight=10, min_day=4))

add(E("ev_meet_warden", "铁门", """他坐在一扇铁门前，背挺得很直，膝盖上横着一根铁棍。
「这扇门不能开，」他说，「原因不重要。」""", [
    C("陪他坐一会儿", "你们坐了两个小时。他讲了这扇门后面原本是什么，讲完就不再说话。",
      {"flag_met_warden": 1, "sanity": 6, "xp": 14}),
    C("问门后面有什么", "他看了你很久，「你猜对了会害怕，猜错了会好奇。都不是好事。」",
      {"flag_met_warden": 1, "xp": 10, "flag_warden_door": 1}),
    C("试图开门", "铁棍横在你面前，没有落下。「我说了不能开。」",
      {"hp": -4, "sanity": -3, "flag_met_warden": 1}),
], places=["bunker", "armory", "police_box"], weight=9, min_day=5))

add(E("ev_meet_trader2", "老周", """他把摊子支在加油站遮阳棚下面，货不多，摆得很整齐。
「今天只换不卖，」他说，「你有什么？」""", [
    C("用废铁换水", "他挑了两块，推过来三瓶水。「下次多带点，」他说，「这东西越来越少了。」",
      {"flag_met_trader": 1, "xp": 8}, {"scrap": -2, "water_bottle": 3}, req=["item:scrap>=2"]),
    C("用情报换药", "他听完，从箱子底下摸出两盒抗生素。「这消息值这个价。」",
      {"flag_met_trader": 1, "xp": 14, "vulture": 1}, {"antibiotics": 2}, req=["item:map_fragment>=1"]),
    C("陪他聊一会儿", "他说他以前是会计，最擅长把亏的说成赚的。现在他只想公平一次。",
      {"flag_met_trader": 1, "sanity": 8, "xp": 12}),
], places=["rest_stop", "checkpoint", "central_station", "auto_shop"], weight=10, min_day=2))

# ---------------- 地点细节 ----------------
add(E("ev_conv_hotpot", "关东煮", """收银台旁边的锅还在冒热气。电磁炉接的是电瓶。
锅里浮着几串东西，汤汁已经熬成了深褐色。""", [
    C("捞一串吃", "是萝卜和鱼丸。你已经很久没吃过热的东西了，烫到舌头也舍不得吐。",
      {"hunger": 22, "sanity": 12, "warmth": 8}),
    C("看看谁在供电", "电瓶接着一根线，通向后面的储物间。储物间里有人在睡觉，呼吸很轻。",
      {"xp": 10, "sanity": -2}),
    C("把锅端走", "锅很沉，汤洒了一路。至少接下来两天有热的喝。",
      {"fatigue": 6}, {"cooking_pot": 1, "soup_can": 1, "salt": 1}),
], places=["convenience"], weight=9))

add(E("ev_pharmacy_cold", "冷藏柜", """疫苗冷藏柜的灯灭了，温度记录仪停在 8.7℃。
柜子里还有几盒东西，包装上印着你没见过的东西。""", [
    C("打开柜子", "里面是疫苗和两盒试剂。你把能拿的都拿了，手上的温度很低。",
      {"xp": 12, "infection": -3}, {"lab_sample": 1, "serum": 1, "chemical": 1}),
    C("检查记录仪", "最后一条记录是爆发前三天。上面写着：断电后请立即转移。没有人转移。",
      {"xp": 14, "sanity": -4}, {"hard_drive": 1}),
    C("关上柜门", "有些东西还是留在原处比较好。",
      {"sanity": 2}),
], places=["pharmacy", "clinic", "field_hospital"], weight=8))

add(E("ev_school_music", "音乐教室", """钢琴盖是开的，琴键上有灰。
墙上的节拍器还在摆，一下，一下。""", [
    C("弹几个音", "你弹了一首小时候学过的曲子，错了很多音。弹完之后，走廊里非常安静。",
      {"sanity": 18, "fatigue": -4}),
    C("关掉节拍器", "摆锤停下的时候，你听见隔壁教室有椅子被拖动的声音。",
      {"sanity": -5, "xp": 8}),
    C("把钢琴拆了", "木板和钢丝都是好东西。你花了很久，手上全是木屑。",
      {"fatigue": 10}, {"wood": 5, "wire": 3, "spring": 2}),
], places=["school"], weight=8))

add(E("ev_gas_wash", "洗车房", """卷帘门半开，里面传来水声。
水还在流，说明水泵有电。""", [
    C("接水", "水是经过滤的，比雨水干净。你装满了所有容器。",
      {"fatigue": 6}, {"water_boiled": 3, "water_bottle": 2}),
    C("检查水泵", "水泵还能用，但被固定在墙上。你拆下了阀门和铜管。",
      {"xp": 8}, {"valve": 1, "copper": 2, "pump_part": 1}),
    C("顺着水声走进去", "洗车位的尽头站着一个人，手里拿着喷枪，正在冲洗自己的手臂。洗了很久。",
      {"sanity": -8, "xp": 10}),
], places=["gas_station", "auto_shop"], weight=8))

add(E("ev_metro_ticket", "售票机", """售票机的屏幕还亮着，界面停在「请选择目的地」。
按钮上有血手印，从 A 出口一直延伸到闸机。""", [
    C("按下一个站名", "机器吐出一张票，日期是今天。你捏着票站了很久。",
      {"sanity": -2, "xp": 10}, {"paper": 2}),
    C("翻找退币口", "里面有一把硬币和一片钥匙。",
      {}, {"scrap": 2, "lockpick": 1}),
    C("查看监控", "屏幕上是三天前的录像。有人在站台上跑，后面跟着很多人。录像到这里就断了。",
      {"xp": 14, "sanity": -6}, {"map_fragment": 1}),
], places=["subway_station"], weight=9))

add(E("ev_police_cell", "拘留室", """铁栏后面有三个人形，都站着，都朝着同一个方向。
地上有一副手铐，钥匙还插着。""", [
    C("用钥匙打开手铐", "手铐是空的。你把钥匙拔下来，放进兜里。",
      {}, {"scrap": 1, "photo": 1}),
    C("隔着栏子看", "其中一个穿着警服，胸牌还在。你念出上面的名字，它没有反应。",
      {"sanity": -3, "xp": 8}),
    C("锁好门离开", "你确认门锁上了，才转身。",
      {"sanity": 4}),
], places=["police_box"], weight=7))

add(E("ev_clinic_birth", "产房", """产房的灯还亮着，保温箱是空的。
墙上贴着一张手写的值班表，最后一行写着：母子平安。""", [
    C("在保温箱里放一罐奶粉", "你不知道为什么。放好之后，你在门口站了一会儿。",
      {"sanity": 12, "xp": 10}, {"baby_formula": -1}, req=["item:baby_formula>=1"]),
    C("搜药柜", "产房的药柜没有被翻过，里面还有不少东西。",
      {}, {"saline": 3, "medical_tape": 2, "pills_pain": 2}),
    C("关掉灯", "房间暗下来。你在黑暗里听见很轻的呼吸声，但没有回头。",
      {"sanity": -8, "xp": 6}),
], places=["clinic", "field_hospital"], weight=8))

add(E("ev_church_bell", "钟绳", """钟绳垂在楼梯中间，末端磨得很光滑。
你握住它的时候，整栋楼好像都在等。""", [
    C("敲一下", "钟声传得很远。你数到十七秒才听见回声。楼下开始有东西移动。",
      {"xp": 14, "sanity": -6}, fight="screamer_wail"),
    C("把绳子割断", "钟绳落在地上，像一条死蛇。",
      {"sanity": 4, "xp": 8}, {"rope": 2}),
    C("顺着绳子爬上钟楼", "钟楼里有一枚核心，还有一具坐在钟边的尸体，手里攥着钟锤。",
      {"fatigue": 12, "sanity": -4, "xp": 16}, {"light_core": 1, "rope": 1}),
], places=["church", "cathedral"], weight=9))

add(E("ev_market_tasting", "试吃台", """微波炉还在转，里面是一份没有拆封的便当。
试吃台上摆着一排小纸杯，杯底有一层干掉的东西。""", [
    C("打开微波炉", "便当还是热的，塑料盖鼓起来。你闻了一下，是咖喱味。",
      {}, {"canned_food": 2, "soup_can": 1}),
    C("检查试吃台下方", "下面有个纸箱，装着没开封的调料和罐头。",
      {"xp": 6}, {"salt": 2, "sugar": 2, "beans_can": 2}),
    C("先看看周围", "你绕着货架走了一圈。有东西在冷柜后面，但没动。你决定不惊动它。",
      {"xp": 8}),
], places=["supermarket", "convenience"], weight=8))

add(E("ev_warehouse_freezer", "冷藏箱", """集装箱改的冷库，门缝里冒白气。
压缩机还在响，说明有人维护过它。""", [
    C("拉开门", "冷气扑面而来。里面挂着六扇肉，摆得很整齐。你不想分辨是什么肉。",
      {"hunger": 20, "sanity": -10, "xp": 12}, {"cooked_meat": 3, "fat": 2}),
    C("检查压缩机", "机器保养得很好。你拆下几个零件，还在旁边找到一桶燃料。",
      {"fatigue": 8, "xp": 10}, {"generator_part": 1, "fuel": 2, "oil": 1}),
    C("在门口留下记号", "你用粉笔画了个叉，然后离开。",
      {"sanity": 2, "xp": 6}),
], places=["warehouse", "freight_yard", "slaughterhouse"], weight=10))

add(E("ev_factory_locker", "更衣柜", """一排铁皮柜，只有 37 号是锁着的。
柜门上贴着一张小孩画的太阳。""", [
    C("撬开 37 号", "里面是换洗衣物、一张照片和一封没寄出的信。信里说：等爸爸回来，我们去海边。",
      {"sanity": -6, "xp": 12}, {"photo": 1, "child_drawing": 1, "work_boots": 1}),
    C("找没锁的柜子", "工具、手套、半包烟。都是能用的东西。",
      {}, {"wrench": 1, "gloves_work": 1, "cigarettes": 1}),
    C("不碰", "你走出更衣室。37 号柜门上的太阳画得很用力。",
      {"sanity": 2}),
], places=["factory", "warehouse", "substation"], weight=8))

add(E("ev_chem_valve", "阀门", """压力表的指针在红区边缘抖动。
旁边贴着一张纸：超压时请打开 3 号阀。字迹很潦草。""", [
    C("打开 3 号阀", "管道里传来一阵闷响，压力慢慢降下来。空气里的甜味淡了。",
      {"xp": 18, "sanity": 6}, {"sulfur": 2, "chemical": 1}),
    C("关掉总阀", "整个厂房安静了。你听见更深处有液体滴落的声音。",
      {"xp": 12}, {"valve": 1}),
    C("撤出去", "你不想在这里赌运气。",
      {}),
], places=["chem_plant", "water_plant"], weight=8))

add(E("ev_water_pump", "泵房", """手动泵的把手在缓慢地自己动。
一下，一下，很有规律。""", [
    C("按住把手", "你按下把手，水流出来，很清。你灌满水壶，手还在抖。",
      {"thirst": 24, "xp": 10}, {"water_boiled": 2, "purify_tablet": 1}),
    C("顺着管道往上找", "管道通向一个检修口。里面很窄，但能通到地面。",
      {"fatigue": 8, "xp": 12}, {"pump_part": 1, "wire": 2}),
    C("不管它", "你退出去，把手还在动。",
      {"sanity": -4}),
], places=["water_plant", "bunker"], weight=7))

add(E("ev_auto_lift", "举升机", """举升机升到一半停了，车底悬在你头顶。
车底有一摊油，还有一只手垂下来。""", [
    C("降下举升机", "你按下按钮，机器嘎吱响了两声，车慢慢落回地面。手也缩了回去。",
      {"sanity": 4, "xp": 12}, {"jack": 1, "oil": 2}),
    C("检查车底", "车底绑着一个防水袋，里面是工具和几发子弹。",
      {"fatigue": 8}, {"toolbox": 1, "ammo_45": 5}),
    C("离开", "你绕过那摊油。手还在轻轻晃。",
      {}),
], places=["auto_shop"], weight=7))

add(E("ev_slaughter_hooks", "挂肉钩", """一排钩子从天花板垂下来，空着，轻轻摇晃。
轨道尽头有一扇冷库门，门缝里塞着布。""", [
    C("打开冷库", "里面没有肉，只有一张行军床和一箱罐头。有人在这里住过。",
      {"sanity": -4, "xp": 12}, {"canned_food": 3, "sleeping_bag": 1}),
    C("把钩子拆下来", "钢钩很重，能做武器，也能做陷阱。",
      {"fatigue": 6}, {"steel_plate": 1, "spring": 2}),
    C("离开", "钩子还在晃。你没有回头。",
      {}),
], places=["slaughterhouse"], weight=7))

add(E("ev_tunnel_vent", "通风井", """风从井口吹上来，带着一股暖意。
井壁上有攀爬用的钢筋，一直通向下面。""", [
    C("爬下去", "井底是一间机房，有电，有灯，还有一台还在录制的摄像机。",
      {"fatigue": 14, "sanity": -6, "xp": 20}, {"light_core": 1, "hard_drive": 1}),
    C("往下扔一个燃烧瓶", "火光掉下去，很久才触底。你听见一片细密的移动声。",
      {"sanity": -6, "xp": 10}, {"molotov": -1}),
    C("在井口做个记号", "你不想下去。至少今天不想。",
      {"xp": 6}),
], places=["tunnel", "subway_hub"], weight=9))

add(E("ev_barn_root", "地窖", """谷仓地板下面有一扇暗门，锁是新的。
里面的东西被整整齐齐码着，像是有人准备长期住下去。""", [
    C("搬走一部分", "你尽量只拿自己需要的，把剩下的放回原位。",
      {"xp": 10}, {"canned_food": 3, "water_bottle": 2, "ammo_9mm": 8}),
    C("等主人回来", "你在地窖里坐了两个小时。没有人回来。你留下了一罐食物，走了。",
      {"sanity": 6, "xp": 8}),
    C("全部搬走", "你跑了三趟。最后一趟时，远处的路上出现了一个人影。",
      {"vulture": 2, "xp": 12}, {"canned_food": 5, "water_bottle": 4}),
], places=["farm", "barn", "orchard"], weight=8))

add(E("ev_lake_wreck", "沉船", """一条渔船半沉在岸边，船头朝天。
船舱里有灯，一闪一闪，像有人在里面。""", [
    C("蹚水过去", "船舱里是一台无线电，接着汽车电瓶。屏幕上跳着：灯塔，还在。",
      {"xp": 18, "flag_lighthouse_known": 1}, {"radio_part": 1, "fuel": 1}),
    C("检查船尾", "船尾挂着渔网，兜里有几条已经风干的鱼。",
      {}, {"dried_meat": 2, "rope": 2}),
    C("留在岸上", "灯还在闪。你坐在岸边，看它闪了很久。",
      {"sanity": 2}),
], places=["lake_dock", "harbor"], weight=9))

add(E("ev_rest_store", "收银台", """收银台后面挂着一串钥匙，标着 1 到 12。
货架是空的，但库房的门锁着。""", [
    C("试到第 7 把", "门开了。库房里堆着没上架的货，还有一只猫。猫看了你一眼，走了。",
      {"xp": 14, "sanity": 8}, {"canned_food": 3, "energy_bar": 2, "milk": 2}),
    C("把钥匙全拿走", "有了这些钥匙，你以后能回来慢慢翻。",
      {}, {"lockpick": 1, "scrap": 2}),
    C("先找点吃的", "你在收银台下面找到半箱过期的巧克力和一瓶酒。",
      {"hunger": 8, "sanity": 6}, {"chocolate": 2, "liquor": 1}),
], places=["rest_stop", "convenience", "supermarket"], weight=8))

add(E("ev_checkpoint_tower", "哨塔", """沙袋后面的机枪还架着，弹链垂到地上。
瞭望口外面，公路一直延伸到雾里。""", [
    C("拆下机枪", "枪机锈死了，你只能拆下弹链和瞄准镜。",
      {"fatigue": 8}, {"ammo_762": 12, "binoculars": 1}),
    C("用望远镜看", "雾里有车队，三辆，往检查站方向。你数了数人，至少九个。",
      {"xp": 16, "flag_convoy_seen": 1}),
    C("在哨塔上休息", "这里视野好，风也大。你睡了一会儿，梦见自己在站岗。",
      {"fatigue": -18, "sanity": 6}),
], places=["checkpoint", "armory"], weight=8))

add(E("ev_radar_screen", "屏幕", """雷达屏幕上的光点比昨天多了一个。
它们排成一条线，正在缓慢移动。""", [
    C("记录轨迹", "你抄下坐标，发现它们正沿着铁路移动。",
      {"xp": 16, "flag_convoy_seen": 1}, {"map_fragment": 1}),
    C("关掉雷达", "屏幕暗下去。你希望那些光点只是飞鸟。",
      {"sanity": 2}),
    C("用无线电呼叫", "对面沉默了很久，然后传来一句：「别挡路。」",
      {"xp": 14, "sanity": -4, "military": -1}),
], places=["radar_station", "comm_tower"], weight=8))

add(E("ev_bunker_kids", "儿童房", """上下铺，墙上贴着卡通贴纸，被子叠得很整齐。
桌上摆着六份没吃完的军用口粮。""", [
    C("吹响哨子", "三短一长。十分钟后，通风管里传来回应：两短。",
      {"sanity": 12, "xp": 18, "flag_bunker_kids": 1}, {}),
    C("留下补给", "你把罐头摆在桌上，摆成一条直线。",
      {"sanity": 10, "xp": 10}, {"canned_food": -2}, req=["item:canned_food>=2"]),
    C("搜柜子", "柜子里有衣服、玩具和一张全家福。你把照片放回原处。",
      {"sanity": -2}, {"cloth": 3, "child_drawing": 1}),
], places=["bunker", "field_hospital"], weight=7))

add(E("ev_airstrip_plane", "货舱", """运输机的后舱门开着，里面固定着几个托盘。
机身侧面有一个弹孔，补过，又裂开了。""", [
    C("清点托盘", "医疗物资、口粮、弹药。都还在。你只拿了能背走的。",
      {"fatigue": 10, "xp": 18}, {"medkit": 1, "mre": 2, "ammo_556": 10}),
    C("检查驾驶舱", "仪表盘上放着一顶飞行帽和一张航线图。终点标着一个岛。",
      {"xp": 20, "sanity": 6}, {"map_fragment": 1, "map_book": 1}),
    C("修舱门", "舱门卡住了，你用撬棍别了半天。至少今晚能在这里过夜。",
      {"fatigue": 8, "warmth": 10, "sanity": 4}),
], places=["airstrip"], weight=8))

add(E("ev_train_dining", "餐车", """餐桌上摆着六副餐具，食物早就成了黑色的壳。
桌上的花瓶里插着假花，颜色还很鲜艳。""", [
    C("在餐车过一夜", "座椅很软，暖气虽然停了，但车厢挡住了风。你睡得很沉。",
      {"fatigue": -24, "sanity": 8, "warmth": 12}),
    C("搜厨房", "后厨的柜子锁着，但锁已经锈了。里面有罐头和一把好刀。",
      {}, {"canned_food": 3, "kitchen_knife": 1, "salt": 1}),
    C("看窗外", "铁轨旁的雪地上有一串脚印，跟着列车走了很久，然后消失。",
      {"sanity": -4, "xp": 8}),
], places=["supply_train", "central_station"], weight=8))

add(E("ev_overpass_below", "桥下", """高架桥的接缝处垂着一辆车，只剩一根钢筋挂着。
桥下堆着的东西，看起来不像垃圾。""", [
    C("爬下去", "桥下是一个用防水布搭的窝。里面有睡袋、水桶和一本日记。",
      {"fatigue": 12, "sanity": -2, "xp": 12}, {"sleeping_bag": 1, "water_bottle": 2, "book": 1}),
    C("用绳子把车拉上来", "你试了三次。第三次，钢筋断了，车掉下去，砸出一片回声。",
      {"fatigue": 16, "sanity": -5, "xp": 10}, {"scrap": 4, "fuel": 1}),
    C("绕开", "你从另一侧下桥。桥下很暗，你没有看清那些东西。",
      {}),
], places=["overpass"], weight=8))

add(E("ev_cityhall_file", "档案室", """铁柜里的卷宗按年份排好，最后一个抽屉被拉开了一半。
里面是一份名单，你的名字在第七页。""", [
    C("带走名单", "你把名单卷起来，塞进背包。你不知道它意味着什么，但你不能把它留在这里。",
      {"sanity": -6, "xp": 20, "flag_list_found": 1}, {"radio_codebook": 1}),
    C("查自己的档案", "档案上写着：健康状况良好，无家属，建议编入 B 组。日期是爆发前一周。",
      {"sanity": -10, "xp": 22, "flag_whitecrow_warning": 1}, {"hard_drive": 1}),
    C("关掉抽屉", "你把它推回去。有些问题不问，日子会好过一点。",
      {"sanity": 2}),
], places=["city_hall", "police_box"], weight=9))

add(E("ev_tv_studio", "演播室", """提词器还开着，滚动着一行字：请不要离开你的座位。
摄像机上的红灯亮着。""", [
    C("对着镜头说话", "你说：如果有人看见，往北走，找灯塔。说完之后，红灯灭了。",
      {"sanity": 12, "xp": 20, "flag_tv_message": 1}, {}),
    C("查看录像", "存储卡里是三天的素材。最后一段，主持人还在念稿子，念到一半，稿子掉了。",
      {"sanity": -8, "xp": 14}, {"hard_drive": 1}),
    C("拆摄像机", "镜头和电池都是好东西。红灯灭了。",
      {"xp": 10}, {"circuit": 2, "battery": 3, "camera": 1}),
], places=["tv_tower"], weight=8))

add(E("ev_station_lost", "失物招领", """货架上摆着几十件行李，标签上写着日期和姓名。
最上面一层有一件很小的外套。""", [
    C("找一件能穿的", "你挑了一件厚外套，口袋里有一张车票和半包烟。",
      {}, {"jacket_puffer": 1, "cigarettes": 1}),
    C("翻箱子", "行李箱里有衣服、照片和一点钱。钱在这里已经没有用了。",
      {"fatigue": 8}, {"suitcase": 1, "gold_ring": 1, "watch": 1}),
    C("把小外套带走", "你说不清为什么。你把它叠好，放进背包最里面。",
      {"sanity": -4, "xp": 10}, {"cloth": 2}),
], places=["central_station", "subway_station"], weight=8))

add(E("ev_stadium_locker", "更衣室", """一排水龙头，一个冰浴池，柜门上的名字被撕掉了。
其中一扇柜门内侧贴满了照片。""", [
    C("看照片", "一支球队的合影，每个人都笑得很高兴。照片背面写着：赛季结束，一起吃饭。",
      {"sanity": 8, "xp": 12}, {"photo": 1}),
    C("搜柜子", "绷带、止痛喷雾、几块能量胶，还有一个急救箱。",
      {}, {"bandage": 3, "pills_pain": 2, "medkit": 1}),
    C("打开冰浴池的盖子", "水面上浮着一层白雾。你没有往下看。",
      {"sanity": -6}), 
], places=["stadium"], weight=8))

add(E("ev_cathedral_crypt", "地下室", """石棺盖被推开了一条缝，里面是空的。
墙上刻满了名字，最后一行还没刻完。""", [
    C("把最后一行刻完", "你找到一把凿子。名字是：牧者。",
      {"sanity": 6, "xp": 16, "flag_crypt_name": 1}, {"light_core": 1}),
    C("搜石棺", "空的石棺底部有一个暗格，里面是核心和一本圣经。",
      {"sanity": -4, "xp": 18}, {"light_core": 1, "book": 1}),
    C("退出去", "楼梯很长。你走上来的时候，天已经黑了。",
      {"sanity": -2}),
], places=["cathedral", "church"], weight=9))

add(E("ev_incinerator_belt", "传送带", """传送带还在转，上面空着，但履带上有烧焦的痕迹。
控制台上有一个绿色的按钮，写着：继续。""", [
    C("按下按钮", "传送带加速，炉膛里的火旺了起来。你听见远处有金属被拖动的声音。",
      {"sanity": -8, "xp": 18}, {"charcoal": 3, "steel_plate": 1}),
    C("拉下总闸", "机器停了。世界安静下来，你听见自己的呼吸。",
      {"sanity": 6, "xp": 12}, {"copper": 3, "wire": 3}),
    C("检查控制台", "抽屉里有一张值班表和一枚核心，编号 06。",
      {"xp": 14}, {"light_core": 1, "paper": 2}),
], places=["incinerator"], weight=8))

add(E("ev_quarry_cave", "矿洞", """洞口架着木支撑，里面吹出凉风。
地上有一串新鲜的脚印，朝着里面。""", [
    C("跟进去", "洞里有爆破留下的空间，堆着工具和几箱炸药。脚印在尽头消失了。",
      {"fatigue": 12, "xp": 16}, {"gunpowder": 3, "pipe_bomb": 1, "light_core": 1}),
    C("在洞口守着", "你等到天黑，没有人出来。你拿走了洞口的工具。",
      {"sanity": -2}, {"toolbox": 1, "steel_plate": 1}),
    C("炸塌洞口", "你不想让里面的东西出来。爆炸声在山谷里滚了很久。",
      {"xp": 14, "sanity": -4}, {"pipe_bomb": -1}),
], places=["quarry"], weight=8))

add(E("ev_apiary_queen", "蜂王", """蜂箱深处传来低沉的嗡鸣，和别处不一样。
养蜂人的面罩挂在墙上，里面还有干枯的花。""", [
    C("取出蜂王巢", "蜂群围着你转，但没有蜇你。你取走了一小块巢脾，甜得发苦。",
      {"sanity": 8}, {"honey": 3, "wax": 2}),
    C("穿上养蜂服", "面罩里的味道很旧。你在蜂群里待了半个小时，它们当你是空气。",
      {"fatigue": 6}, {"hazmat": 1, "honey": 2}),
    C("不打扰它们", "蜜蜂还在工作，像什么都没发生过。你轻轻带上门。",
      {"sanity": 6}),
], places=["apiary", "orchard"], weight=7))

# ---------------- 每日 ----------------
add(E("ev_water_bad", "水有问题", """喝完水之后，你的胃开始绞痛。
桶底有一层细沙，沙里有东西在动。""", [
    C("催吐", "你在墙角吐了很久，直到吐出来的只有水。至少把大部分咽下去的东西弄出来了。",
      {"hp": -8, "thirst": -10, "infection": -2, "sanity": -4}),
    C("吃抗生素硬扛", "药片压住了症状，但你整晚都在发抖。",
      {"hp": -4, "infection": 4}, {"antibiotics": -1}, req=["item:antibiotics>=1"]),
    C("烧一锅开水，重新来", "你把所有水都烧开，倒掉第一锅，重新灌满。",
      {"fatigue": 6, "thirst": 6}, {"water_boiled": 2}),
], tag="daily", weight=8, once=False, min_day=3))

add(E("ev_fire", "营地起火", """半夜，储藏室烧起来了。火不大，但烟很浓。""", [
    C("先救物资", "你冲进去抢出了两箱东西。眉毛烧掉了一半。",
      {"hp": -10, "fatigue": 10, "sanity": -4}, {"canned_food": 2, "bandage": 2}),
    C("先救人", "没有人受伤。火灭之后，你们清点物资，少了三箱。",
      {"sanity": 8, "fatigue": 8}, {"canned_food": -3}),
    C("用湿毯子压火", "火被闷住了。你趴在地上咳了很久。",
      {"hp": -4, "fatigue": 6, "sanity": 2}),
], tag="daily", weight=6, min_day=4))

add(E("ev_medicine_missing", "药少了", """急救箱里的抗生素少了三粒。
箱子没锁，谁都能拿。""", [
    C("召集所有人，当面问", "没有人承认。第二天，一个伤员退烧了。你选择不再追问。",
      {"sanity": -3, "flag_med_mystery": 1}),
    C("把药分给每个人保管", "每个人手里都有一份。这让你放心了一点，也让你更累。",
      {"sanity": 2, "fatigue": 4}),
    C("设一个上锁的柜子", "你花了半天做了一个锁。没人反对。",
      {"sanity": 4, "fatigue": 6}, {"scrap": -2}),
], tag="daily", weight=6, min_day=5))

add(E("ev_cold_snap2", "暴风雪", """雪压塌了半个棚子。风声大到你听不见自己的脚步。""", [
    C("用木板加固", "你在雪里钉了两个小时，手指冻得没有知觉，但棚子撑住了。",
      {"hp": -6, "fatigue": 14, "warmth": 10}, {"wood": -4, "nail": -6}, req=["item:wood>=4"]),
    C("躲进地下室", "你们挤在一起，靠彼此的体温撑过了一夜。",
      {"warmth": -6, "sanity": 6}, req=["companions>=1"]),
    C("烧掉所有能烧的", "火很大，暖了很久。第二天，你们没有椅子坐了。",
      {"warmth": 24}, {"wood": -6, "paper": -5}),
], tag="daily", weight=6, min_day=12))

add(E("ev_heat_wave", "热浪", """空气在中午变得粘稠，柏油路上浮着一层热浪。
水在快速蒸发。""", [
    C("减少活动", "你躲在阴影里，一整天没有出门。水还是少了半桶。",
      {"thirst": -12, "fatigue": -10, "sanity": 2}),
    C("去抢水", "你去了最近的超市，把能找到的水都搬了回来。",
      {"fatigue": 16, "hp": -4}, {"water_bottle": 4, "soda": 2}),
    C("把水留给别人", "你只喝了一小口。傍晚的时候，有人把半瓶水放在你门口。",
      {"sanity": 8, "thirst": -8}, req=["companions>=1"]),
], tag="daily", weight=6, min_day=10))

add(E("ev_radio_silence", "无线电静默", """那个女声今天没有出现。
你调到每个频段，只有电流声。""", [
    C("等", "你守了一整夜。凌晨四点，她出现了，声音很哑：「抱歉，发电机坏了。」",
      {"sanity": 8, "fatigue": -6}),
    C("自己去修中继站", "你带着工具出了门。路很长，但你知道方向。",
      {"fatigue": 12, "xp": 16}, {"wire": 2, "radio_part": 1}),
    C("关掉收音机", "安静也很好。你对自己说。",
      {"sanity": -4}),
], tag="daily", weight=6, min_day=7))

add(E("ev_convoy", "车队", """三辆卡车从公路上驶过，车厢用帆布盖着。
最后一辆车的尾灯坏了，忽明忽暗。""", [
    C("拦车", "车队没有停。第二辆车的后斗里有人朝你挥手。",
      {"sanity": -2, "xp": 8, "flag_convoy_seen": 1}),
    C("尾随", "车队开进了检查站。你在远处看见他们卸货，一箱一箱地搬。",
      {"fatigue": 10, "xp": 14, "flag_convoy_seen": 1}),
    C("避开", "你等车声消失才继续走。",
      {"sanity": 2}),
], tag="daily", weight=5, min_day=6))

add(E("ev_child_sick", "孩子发烧", """小满的额头烫得吓人。她一直说冷，但身上全是汗。""", [
    C("用退烧药", "她喝下去，半夜吐了一次，天亮时烧退了。",
      {"sanity": 10}, {"pills_fever": -1, "water_boiled": -1}, req=["item:pills_fever>=1"]),
    C("物理降温", "你换了整晚的湿毛巾。她一直在说梦话，叫妈妈。",
      {"fatigue": -12, "sanity": 4, "hp": -2}, req=["flag:met_kid>=1"]),
    C("去弄药", "你摸黑出门，天亮时带着药回来。手背上多了一道口子。",
      {"hp": -8, "sanity": 12}, {"pills_fever": 1}, req=["flag:met_kid>=1"]),
], tag="daily", weight=6, min_day=6))

add(E("ev_dog_bark", "铁钉在叫", """狗对着门外的黑暗低吼，毛竖起来。
它不常这样。""", [
    C("相信它，准备战斗", "你刚握紧武器，门就被撞了一下。",
      {"sanity": 4, "xp": 8}, fight="runner_feral", req=["flag:dog>=1"]),
    C("安抚它", "它慢慢安静下来，但整晚都贴在你脚边。",
      {"sanity": 6}, req=["flag:dog>=1"]),
    C("赶它出去", "它站在门外，看着你，然后走进黑暗里。",
      {"sanity": -6}, req=["flag:dog>=1"]),
], tag="daily", weight=6, min_day=5))

add(E("ev_stray_offer", "陌生人的情报", """有人在门上留了一张纸条，压在一块石头下面。
纸条上写着一个地址，和一句话：「那里有你要的东西。别带人去。」""", [
    C("按地址去", "你找到了一个没有被翻过的储藏室。东西不多，但都是你需要。",
      {"fatigue": 8, "sanity": -2}, {"light_core": 1, "medkit": 1}, req=["day>=8"]),
    C("不理会", "你把纸条揉成一团，扔进火里。",
      {"sanity": 2}),
    C("在附近埋伏", "你等了三个小时，看见一个瘸腿的男人在远处观察。他发现你之后，转身走了。",
      {"xp": 12, "flag_watcher_seen": 1}),
], tag="daily", weight=5, min_day=6))

# 追加并校验 id
existing = load("events")
seen = set()
deduped = []
for e in existing:
    if e["id"] in seen:
        continue
    seen.add(e["id"])
    deduped.append(e)
ids = set(seen)
added = 0
for e in new:
    if e["id"] in ids:
        continue
    deduped.append(e)
    ids.add(e["id"])
    added += 1
save("events", deduped)
print("added", added, "total", len(deduped))
