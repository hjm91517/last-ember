#!/usr/bin/env python3
# 交叉引用校验：任何悬空 id 都必须为 0
import json, os, sys, collections

C = os.path.join(os.path.dirname(__file__), "..", "LastEmber", "Resources", "Content")
def load(n):
    with open(os.path.join(C, n + ".json"), encoding="utf-8") as f:
        return json.load(f)

items = {x["id"] for x in load("items")}
weapons = {x["id"] for x in load("weapons")}
armors = {x["id"] for x in load("armor")}
enemies = {x["id"] for x in load("enemies")}
abilities = {x["id"] for x in load("abilities")}
places = {x["id"]: x for x in load("places")}
perks = {x["id"] for x in load("perks")}
buildings = {x["id"] for x in load("buildings")}
endings = {x["id"] for x in load("endings")}
npcs = {x["id"]: x for x in load("npcs")}
quests = {x["id"]: x for x in load("quests")}
events = load("events")
recipes = load("recipes")
achievements = load("achievements")

problems = []
def bad(msg):
    problems.append(msg)

all_ref = items | weapons | armors
regions = {"旧城区", "工业区", "近郊农野", "军事管制区", "城市核心"}
tags = set()
for p in places.values():
    tags |= set(p["tags"])
place_tokens = set(places) | regions | tags | {"any"}

# 地点
for pid, p in places.items():
    for e in p["enemies"]:
        if e not in enemies: bad(f"place {pid}: enemy {e}")
    for l in p["loot"]:
        if l["item"] not in all_ref: bad(f"place {pid}: loot {l['item']}")
    for t in p["tags"]:
        if t.startswith("unlock:") and t.split(":", 1)[1] not in places:
            bad(f"place {pid}: unlock target {t}")
    if p["stages"] < 1 or p["danger"] > 5: bad(f"place {pid}: stages/danger")

# 敌人
for eid, e in [(x["id"], x) for x in load("enemies")]:
    for a in e["abilities"]:
        if a not in abilities: bad(f"enemy {eid}: ability {a}")
    for l in e["loot"]:
        if l["item"] not in all_ref: bad(f"enemy {eid}: loot {l['item']}")

# 配方
for r in recipes:
    if r["station"] not in buildings: bad(f"recipe {r['id']}: station {r['station']}")
    for k in r["cost"]:
        if k not in all_ref: bad(f"recipe {r['id']}: cost {k}")
    for k in r["out"]:
        if k not in all_ref: bad(f"recipe {r['id']}: out {k}")
    if r["outWeapon"] and r["outWeapon"] not in weapons: bad(f"recipe {r['id']}: weapon {r['outWeapon']}")
    if r["outArmor"] and r["outArmor"] not in armors: bad(f"recipe {r['id']}: armor {r['outArmor']}")

# 任务
for qid, q in quests.items():
    for k in q["rewardItems"]:
        if k not in all_ref and k != "shards": bad(f"quest {qid}: reward {k}")
    if q["kind"] == "collect" and q["target"] not in all_ref:
        bad(f"quest {qid}: collect target {q['target']}")
    if q["kind"] == "visit" and q["target"] not in places:
        bad(f"quest {qid}: visit target {q['target']}")
    if q["next"] and q["next"] not in quests: bad(f"quest {qid}: next {q['next']}")
    if q["giver"] != "board" and q["giver"] != "light" and q["giver"] not in npcs:
        bad(f"quest {qid}: giver {q['giver']}")

# NPC
for nid, n in npcs.items():
    if n["perkID"] not in perks: bad(f"npc {nid}: perk {n['perkID']}")
    if n["questID"] and n["questID"] not in quests: bad(f"npc {nid}: quest {n['questID']}")

# 事件
for e in events:
    if e["tag"] not in {"daily", "encounter", "story", "trade"}:
        bad(f"event {e['id']}: tag {e['tag']}")
    for t in e["places"]:
        if t not in place_tokens: bad(f"event {e['id']}: place token {t}")
    for c in e["choices"]:
        if c["fight"] and c["fight"] not in enemies: bad(f"event {e['id']}: fight {c['fight']}")
        if c["ending"] and c["ending"] not in endings: bad(f"event {e['id']}: ending {c['ending']}")
        if c["next"] and c["next"] not in {x["id"] for x in events}: bad(f"event {e['id']}: next {c['next']}")
        for k in c["items"]:
            if k not in all_ref: bad(f"event {e['id']}: item {k}")
        for req in c["req"]:
            if req.startswith("item:"):
                rid = req[5:].split(">=")[0]
                if rid not in all_ref: bad(f"event {e['id']}: req item {rid}")
            elif req.startswith("perk:"):
                pid = req[5:]
                if pid not in perks: bad(f"event {e['id']}: req perk {pid}")
        for k in c["effect"]:
            if k not in {"hp","hunger","thirst","infection","sanity","fatigue","warmth","xp","ap",
                         "perk","hpMax","shards","military","vulture","order","whitecrow"} and not k.startswith("flag_"):
                if k not in {"mercy", "infection_survived", "night_battles", "near_death"}:
                    bad(f"event {e['id']}: effect key {k}")

# 成就
stat_keys = {"kills","searches","crafts","builds","places_visited","items_found","battles",
             "damage_dealt","days","boss_kills","recruited","quests_done","runs","shards","endings",
             "heals","melee_kills","gun_kills","night_battles","infection_survived","near_death",
             "weapons_crafted","armors_crafted","battles_won","overweight","enemy_types","cores_held",
             "valuables","damage_dealt"}
for a in achievements:
    k = a["key"]
    ok = (k in stat_keys or k.startswith("kill_") or k.startswith("ending_") or k.startswith("flag_"))
    if not ok: bad(f"achievement {a['id']}: key {k}")

# 剧本引用
scen_items = {"canned_food":1,"water_bottle":1,"bandage":1,"cloth":1,"ammo_9mm":1,"scrap":1,
              "duct_tape":1,"wire":1,"antibiotics":1,"pills_pain":1,"backpack_small":1,"arrow":1,
              "dried_meat":1,"herbs_tea":1,"mre":1,"ammo_556":1,"candy":1,"smoke_grenade":1,"lockpick":1}
for k in scen_items:
    if k not in all_ref: bad(f"scenario item {k}")
for w in ["pipe","pistol_9mm","wrench","knife_scalpel","crowbar","bow_compound","machete","rifle_ar","knife_folding","pistol_silenced"]:
    if w not in weapons: bad(f"scenario weapon {w}")
for a in ["jacket_old","gloves_work","robe_gray","vest_kevlar","hood_cloth"]:
    if a not in armors: bad(f"scenario armor {a}")
for p in ["marksman","handy","field_medic","scrounger","deadeye","zeal","tough","light_step","ghost"]:
    if p not in perks: bad(f"scenario perk {p}")

# 统计
print("items", len(items), "weapons", len(weapons), "armor", len(armors),
      "enemies", len(enemies), "places", len(places), "events", len(events),
      "recipes", len(recipes), "quests", len(quests), "achievements", len(achievements),
      "endings", len(endings), "perks", len(perks), "npcs", len(npcs))
if problems:
    print("\n".join("!! " + p for p in problems[:80]))
    print("TOTAL PROBLEMS", len(problems))
    sys.exit(1)
print("ALL REFERENCES OK")
