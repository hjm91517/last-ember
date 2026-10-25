#!/usr/bin/env python3
# 严格检查 JSON 结构是否与 Swift Codable 模型一致
import json, os, sys

C = os.path.join(os.path.dirname(__file__), "..", "LastEmber", "Resources", "Content")
def load(n):
    with open(os.path.join(C, n + ".json"), encoding="utf-8") as f:
        return json.load(f)

errors = []
def req(obj, keys, ctx):
    for k in keys:
        if k not in obj:
            errors.append(f"{ctx}: missing key {k}")

def typ(obj, key, py, ctx, optional=False):
    if key not in obj:
        return
    v = obj[key]
    if v is None:
        if not optional: errors.append(f"{ctx}: {key} is null")
        return
    if not isinstance(v, py):
        errors.append(f"{ctx}: {key} expected {py.__name__}, got {type(v).__name__}")

# items
for x in load("items"):
    ctx = "item " + str(x.get("id"))
    req(x, ["id","name","cat","tier","weight","value","stack","desc","effect","tags","icon"], ctx)
    for k in ["tier","value","stack"]: typ(x, k, int, ctx)
    for k in ["weight"]: typ(x, k, (int, float), ctx)
    typ(x, "effect", dict, ctx); typ(x, "tags", list, ctx)

for x in load("weapons"):
    ctx = "weapon " + str(x.get("id"))
    req(x, ["id","name","kind","desc","dmg","dmgVar","crit","acc","apCost","dur","value","rarity","weight","ammo","traits","icon"], ctx)
    for k in ["dmg","dmgVar","crit","acc","apCost","dur","value","rarity"]: typ(x, k, int, ctx)
    typ(x, "weight", (int, float), ctx); typ(x, "traits", list, ctx)
    typ(x, "ammo", str, ctx, optional=True)

for x in load("armor"):
    ctx = "armor " + str(x.get("id"))
    req(x, ["id","name","slot","desc","armor","evade","warmth","value","rarity","weight","traits","icon"], ctx)
    for k in ["armor","evade","warmth","value","rarity"]: typ(x, k, int, ctx)
    typ(x, "weight", (int, float), ctx); typ(x, "traits", list, ctx)

for x in load("enemies"):
    ctx = "enemy " + str(x.get("id"))
    req(x, ["id","name","tag","tier","desc","hp","dmg","armor","acc","evade","xp","night","abilities","loot","icon"], ctx)
    for k in ["tier","hp","dmg","armor","acc","evade","xp"]: typ(x, k, int, ctx)
    typ(x, "night", bool, ctx)
    typ(x, "abilities", list, ctx); typ(x, "loot", list, ctx)
    for l in x["loot"]:
        req(l, ["item","chance","min","max"], ctx + " loot")

for x in load("places"):
    ctx = "place " + str(x.get("id"))
    req(x, ["id","name","region","desc","danger","stages","x","y","tags","loot","enemies","events"], ctx)
    for k in ["danger","stages"]: typ(x, k, int, ctx)
    for k in ["x","y"]: typ(x, k, (int, float), ctx)

for x in load("events"):
    ctx = "event " + str(x.get("id"))
    req(x, ["id","title","text","tag","weight","once","minDay","places","choices"], ctx)
    typ(x, "weight", int, ctx); typ(x, "once", bool, ctx); typ(x, "minDay", int, ctx)
    typ(x, "choices", list, ctx)
    if not x["choices"]: errors.append(ctx + ": no choices")
    for c in x["choices"]:
        req(c, ["text","req","effect","items","fight","next","chance","effectFail","log","logFail","ending"], ctx + " choice")
        typ(c, "req", list, ctx); typ(c, "effect", dict, ctx); typ(c, "items", dict, ctx)
        typ(c, "chance", int, ctx)
        typ(c, "fight", str, ctx, optional=True)
        typ(c, "ending", str, ctx, optional=True)
        typ(c, "next", str, ctx, optional=True)

for x in load("recipes"):
    ctx = "recipe " + str(x.get("id"))
    req(x, ["id","name","desc","station","stationLevel","ap","cost","out","outWeapon","outArmor"], ctx)
    for k in ["stationLevel","ap"]: typ(x, k, int, ctx)
    for k in ["cost","out"]: typ(x, k, dict, ctx)
    typ(x, "outWeapon", str, ctx, optional=True)
    typ(x, "outArmor", str, ctx, optional=True)

for x in load("perks"):
    ctx = "perk " + str(x.get("id"))
    req(x, ["id","name","branch","tier","maxRank","desc","effect"], ctx)
    for k in ["tier","maxRank"]: typ(x, k, int, ctx)
    typ(x, "effect", dict, ctx)

for x in load("buildings"):
    ctx = "building " + str(x.get("id"))
    req(x, ["id","name","desc","maxLevel","baseCost","scale","effectKey","perLevel","icon"], ctx)
    typ(x, "baseCost", dict, ctx); typ(x, "scale", (int, float), ctx)

for x in load("achievements"):
    ctx = "achievement " + str(x.get("id"))
    req(x, ["id","name","desc","hidden","key","goal"], ctx)
    typ(x, "goal", int, ctx); typ(x, "hidden", bool, ctx)

for x in load("endings"):
    req(x, ["id","title","kind","text","cond"], "ending " + str(x.get("id")))

for x in load("npcs"):
    ctx = "npc " + str(x.get("id"))
    req(x, ["id","name","role","desc","traits","perkID","trust","joinReq","questID","icon"], ctx)
    typ(x, "trust", int, ctx); typ(x, "questID", str, ctx, optional=True)

for x in load("quests"):
    ctx = "quest " + str(x.get("id"))
    req(x, ["id","title","giver","desc","kind","target","count","rewardXP","rewardItems","next"], ctx)
    for k in ["count","rewardXP"]: typ(x, k, int, ctx)
    typ(x, "next", str, ctx, optional=True)

for x in load("journal"):
    req(x, ["id","text","src"], "journal " + str(x.get("id")))

for x in load("abilities"):
    ctx = "ability " + str(x.get("id"))
    req(x, ["id","name","desc","dmg","kind"], ctx)
    typ(x, "dmg", int, ctx)

# id 唯一性
for name in ["items","weapons","armor","enemies","places","events","recipes","perks","buildings",
             "achievements","endings","npcs","quests","journal","abilities"]:
    ids = [x["id"] for x in load(name)]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        errors.append(f"{name}: duplicate ids {sorted(dup)[:5]}")

if errors:
    print("\n".join("!! " + e for e in errors[:60]))
    print("SCHEMA PROBLEMS", len(errors))
    sys.exit(1)
print("SCHEMA OK")
