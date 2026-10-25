#!/usr/bin/env python3
# 数值平衡：首领血量 / 核心与无线电零件供给（幂等）
import json, os

C = os.path.join(os.path.dirname(__file__), "..", "LastEmber", "Resources", "Content")

def load(n):
    with open(os.path.join(C, n + ".json"), encoding="utf-8") as f:
        return json.load(f)
def save(n, d):
    with open(os.path.join(C, n + ".json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print(n, len(d))

en = load("enemies")
BOSS = {
    "boss_bell": (260, 22), "boss_mother": (240, 20), "boss_whitecrow": (280, 24),
    "boss_rustking": (300, 25), "boss_tide": (320, 26), "boss_preacher": (240, 21),
    "boss_twins": (220, 22), "boss_trainman": (260, 23), "boss_hive": (340, 22),
    "boss_ash": (240, 25), "boss_colossus": (300, 27), "boss_ferryman": (260, 25),
    "boss_choir": (240, 22), "boss_librarian": (220, 21),
}
for e in en:
    if e["id"] in BOSS:
        e["hp"], e["dmg"] = BOSS[e["id"]]
    for l in e["loot"]:
        if l["item"] == "light_core":
            l["chance"] = min(60, l["chance"] + 10)
save("enemies", en)

pl = load("places")
extra_loot = {
    "police_box": [("light_core", 10), ("radio_part", 18)],
    "apartment": [("light_core", 8), ("radio_part", 10)],
    "convenience": [("radio_part", 8)],
    "school": [("radio_part", 8)],
    "church": [("light_core", 10)],
    "supermarket": [("light_core", 8)],
    "factory": [("light_core", 10)],
    "field_hospital": [("light_core", 10), ("radio_part", 12)],
    "stadium": [("light_core", 12)],
    "auto_shop": [("radio_part", 14)],
    "checkpoint": [("radio_part", 10)],
}
for p in pl:
    for l in p["loot"]:
        if l["item"] == "light_core":
            l["chance"] = min(60, l["chance"] + 10)
    for (item, chance) in extra_loot.get(p["id"], []):
        if not any(l["item"] == item for l in p["loot"]):
            p["loot"].append({"item": item, "chance": chance, "min": 1, "max": 1})
save("places", pl)
print("BALANCE DONE")
