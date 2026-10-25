import Foundation
import SwiftUI

enum Screen { case home, game, ending }
enum Panel: String, Identifiable {
    case inventory, craft, base, map, squad, quests, codex, character, journal, scenarios, achievements
    var id: String { rawValue }
}

enum BattleAction { case attack, heavy, aim, dodge, item, throwable, flee }

@MainActor
final class GameStore: ObservableObject {
    @Published var state: GameState
    @Published var meta: MetaState
    @Published var screen: Screen = .home
    @Published var panel: Panel?
    @Published var pendingEvent: EventCard?
    @Published var endingCard: Ending?
    @Published var toast: String?
    @Published var eventResult: String?
    @Published var lastBattleSummary: String?

    let content = ContentStore.shared

    init() {
        let loaded = SaveStore.loadState()
        state = loaded ?? GameStore.blankState()
        meta = SaveStore.loadMeta() ?? MetaState()
        if loaded != nil && state.ending == nil {
            screen = state.battle != nil ? .game : .home
        }
    }

    static func blankState() -> GameState {
        let seed = UInt64(Date().timeIntervalSince1970 * 1000) ^ UInt64(UUID().uuidString.hashValue.magnitude)
        var s = GameState(seed: seed, rng: SeededRNG(seed: seed), scenario: "survivor")
        s.log = []
        return s
    }

    // MARK: - 生命周期

    func newGame(_ scenarioID: String) {
        let sc = ContentStore.scenario(scenarioID)
        var s = GameStore.blankState()
        s.scenario = sc.id
        s.hpMax = 100 + sc.hpBonus
        s.hp = s.hpMax
        s.apMax = 3 + sc.apBonus
        s.ap = s.apMax
        for (k, v) in sc.items { s.inventory[k, default: 0] += v }
        for (k, v) in sc.perks { s.perks[k] = v }
        if let w = sc.weapon, let wp = content.weapon(w) {
            let g = GearInstance(id: UUID().uuidString, item: w, dur: wp.dur)
            s.weapons = [g]
            s.equippedWeapon = g.id
        } else {
            let g = GearInstance(id: UUID().uuidString, item: "fist", dur: 999)
            s.weapons = [g]
            s.equippedWeapon = g.id
        }
        for a in sc.armor {
            if let ar = content.armor(a) {
                let g = GearInstance(id: UUID().uuidString, item: a, dur: 100)
                s.armors.append(g)
                s.equippedArmor[ar.slot] = g.id
            }
        }
        s.place = "safehouse"
        s.region = "旧城区"
        s.visited = ["safehouse", "convenience"]
        state = s
        state.log = []
        log("第 47 天。无线电里最后一段录音重复了三遍：『灯塔仍在运行。』", kind: "story")
        log("你检查了一遍据点：窗户漏风，水桶见底，铁管就靠在门边。", kind: "info")
        log("活下去，然后走到灯塔。", kind: "story")
        acceptQuest("m01")
        pendingEvent = content.events.first { $0.id == "ev_intro" }
        endingCard = nil
        screen = .game
        meta.runs += 1
        save()
    }

    func continueGame() {
        if state.ending != nil { return }
        screen = .game
    }

    func returnHome() {
        panel = nil
        pendingEvent = nil
        endingCard = nil
        screen = .home
        save()
    }

    func save() {
        SaveStore.save(state: state, meta: meta)
    }

    func resetEverything() {
        state = GameStore.blankState()
        meta = MetaState()
        SaveStore.clear()
        screen = .home
    }

    // MARK: - 派生属性

    var currentPlace: Place? { content.place(state.place) }
    var currentEnemy: Enemy? { state.battle.flatMap { content.enemy($0.enemy) } }

    var weaponGear: GearInstance? {
        guard let id = state.equippedWeapon else { return nil }
        return state.weapons.first { $0.id == id }
    }
    var weapon: Weapon? {
        guard let g = weaponGear else { return content.weapon("fist") }
        return content.weapon(g.item)
    }
    func armorGear(_ slot: String) -> GearInstance? {
        guard let id = state.equippedArmor[slot] else { return nil }
        return state.armors.first { $0.id == id }
    }
    func armor(_ slot: String) -> Armor? {
        guard let g = armorGear(slot) else { return nil }
        return content.armor(g.item)
    }

    var armorValue: Int {
        var total = 0
        for slot in ["head", "body", "hands", "back"] {
            total += armor(slot)?.armor ?? 0
        }
        return total
    }
    var evadeValue: Int {
        var total = 4
        for slot in ["head", "body", "hands", "back"] {
            total += armor(slot)?.evade ?? 0
        }
        return total
    }
    var warmthValue: Int {
        var total = 20
        for slot in ["head", "body", "hands", "back"] {
            total += armor(slot)?.warmth ?? 0
        }
        return total
    }

    func perkValue(_ key: String) -> Int {
        var total = 0
        for (id, rank) in state.perks {
            if let p = content.perk(id), let v = p.effect[key] {
                total += v * rank
            }
        }
        return total
    }

    var carryCapacity: Int {
        var cap = 45 + perkValue("carry") * 5 + buildingLevel("storage") * 4
        for a in state.armors where state.equippedArmor.values.contains(a.id) {
            for t in content.armor(a.item)?.traits ?? [] where t.hasPrefix("pack") {
                cap += Int(t.dropFirst(4)) ?? 0
            }
        }
        return cap
    }

    var currentWeight: Double {
        var w = 0.0
        for (id, n) in state.inventory {
            w += (content.item(id)?.weight ?? 0.1) * Double(n)
        }
        for g in state.weapons {
            w += content.weapon(g.item)?.weight ?? 1
        }
        for g in state.armors {
            w += content.armor(g.item)?.weight ?? 1
        }
        return w
    }

    var infectionRisk: Int { 100 - min(80, perkValue("infectResist")) }

    var apCap: Int {
        var cap = 3 + perkValue("ap")
        if state.fatigue >= 70 { cap -= 1 }
        if state.buildings["bed", default: 0] >= 2 { cap += 1 }
        if currentWeight > Double(carryCapacity) { cap -= 1 }
        return max(1, cap)
    }

    var scenarioName: String { ContentStore.scenario(state.scenario).name }

    var dayLabel: String {
        let phases = ["凌晨", "清晨", "上午", "正午", "下午", "黄昏", "夜晚", "深夜"]
        let idx = min(phases.count - 1, max(0, (state.apMax - state.ap) % phases.count))
        return "第 \(state.day) 天 · \(phases[idx])"
    }

    // MARK: - 日志与数值

    func log(_ text: String, kind: String = "info") {
        state.log.append(LogLine(day: state.day, text: text, kind: kind))
        if state.log.count > 260 {
            state.log.removeFirst(state.log.count - 260)
        }
    }

    func toast(_ text: String) {
        toast = text
    }

    func apply(effect: [String: Int]) {
        for (k, v) in effect {
            switch k {
            case "hp": state.hp += v
            case "hunger": state.hunger += v
            case "thirst": state.thirst += v
            case "infection": state.infection += v
            case "sanity": state.sanity += v
            case "fatigue": state.fatigue += v
            case "warmth": state.warmth += v
            case "xp": addXP(v)
            case "ap": state.ap += v
            case "perk": state.perkPoints += v
            case "hpMax": state.hpMax += v; state.hp += v
            case "shards": meta.shards += v
            case "military": bumpFaction("military", v)
            case "vulture": bumpFaction("vulture", v)
            case "order": bumpFaction("order", v)
            case "whitecrow": bumpFaction("whitecrow", v)
            default:
                if k.hasPrefix("flag_") {
                    state.flags[String(k.dropFirst(5)), default: 0] += v
                } else {
                    state.stats[k, default: 0] += v
                }
            }
        }
        normalize()
    }

    func bumpFaction(_ key: String, _ v: Int) {
        state.faction[key] = max(-100, min(100, (state.faction[key] ?? 0) + v))
    }

    func normalize() {
        state.hp = max(0, min(state.hpMax, state.hp))
        state.hunger = max(0, min(100, state.hunger))
        state.thirst = max(0, min(100, state.thirst))
        state.infection = max(0, min(100, state.infection))
        state.sanity = max(0, min(100, state.sanity))
        state.fatigue = max(0, min(100, state.fatigue))
        state.warmth = max(0, min(100, state.warmth))
        state.ap = max(0, min(apCap, state.ap))
        if state.hp > 0 && state.hp <= 10 { state.stats["near_death", default: 0] = 1 }
        checkDeath()
    }

    func checkDeath() {
        guard state.ending == nil else { return }
        if state.hp <= 0 { triggerEnding("death_torn"); return }
        if state.infection >= 100 { triggerEnding("death_turn"); return }
        if state.sanity <= 0 { triggerEnding("death_mind"); return }
    }

    func addXP(_ v: Int) {
        state.xp += v
        while state.xp >= state.level * 90 && state.level < 30 {
            state.xp -= state.level * 90
            state.level += 1
            state.perkPoints += 1
            state.hpMax += 6
            state.hp = min(state.hpMax, state.hp + 18)
            log("经验累积成直觉：升到 Lv.\(state.level)，获得 1 点属性点。", kind: "good")
        }
    }

    class func xpNeed(_ level: Int) -> Int { level * 90 }

    func addItem(_ id: String, _ count: Int = 1) {
        guard count != 0 else { return }
        let n = (state.inventory[id] ?? 0) + count
        if n <= 0 {
            state.inventory.removeValue(forKey: id)
        } else {
            state.inventory[id] = min(n, content.item(id)?.stack ?? 99)
        }
    }

    func grantAny(_ id: String, _ count: Int = 1) {
        if count <= 0 {
            if let w = content.weapon(id), id != "fist" {
                if let idx = state.weapons.firstIndex(where: { $0.item == id }) {
                    state.weapons.remove(at: idx)
                    if state.equippedWeapon == nil || state.weapons.isEmpty { state.equippedWeapon = state.weapons.first?.id }
                }
                return
            }
            if content.armor(id) != nil {
                if let idx = state.armors.firstIndex(where: { $0.item == id }) {
                    let gid = state.armors[idx].id
                    state.armors.remove(at: idx)
                    for (slot, v) in state.equippedArmor where v == gid { state.equippedArmor.removeValue(forKey: slot) }
                }
                return
            }
            addItem(id, count)
            return
        }
        if let w = content.weapon(id), id != "fist" {
            for _ in 0..<count {
                let g = GearInstance(id: UUID().uuidString, item: id, dur: w.dur)
                state.weapons.append(g)
                if state.equippedWeapon == nil { state.equippedWeapon = g.id }
            }
            log("获得 \(w.name) ×\(count)", kind: "good")
            return
        }
        if let a = content.armor(id) {
            for _ in 0..<count {
                let g = GearInstance(id: UUID().uuidString, item: id, dur: 100)
                state.armors.append(g)
                if state.equippedArmor[a.slot] == nil { state.equippedArmor[a.slot] = g.id }
            }
            log("获得 \(a.name) ×\(count)", kind: "good")
            return
        }
        addItem(id, count)
        log("获得 \(content.itemName(id)) ×\(count)", kind: "good")
    }

    func hasItem(_ id: String, _ count: Int = 1) -> Bool {
        (state.inventory[id] ?? 0) >= count
    }

    func rollLoot(_ entries: [LootEntry], bonus: Int = 0) -> [String: Int] {
        var out: [String: Int] = [:]
        var rng = state.rng
        for e in entries {
            if rng.chance(min(100, e.chance + bonus)) {
                let n = rng.int(max(1, e.min)...max(1, e.max))
                out[e.item, default: 0] += n
            }
        }
        state.rng = rng
        return out
    }

    func grant(_ loot: [String: Int]) {
        for (id, n) in loot {
            grantAny(id, n)
        }
    }

    // MARK: - 行动点判定

    func spendAP(_ n: Int = 1) -> Bool {
        guard state.ap >= n else {
            toast("行动点不足，先结束今天。")
            return false
        }
        guard state.ending == nil else { return false }
        state.ap -= n
        return true
    }

    // MARK: - 搜刮

    func search() {
        guard let place = currentPlace else { return }
        guard spendAP() else { return }
        var rng = state.rng
        let stage = state.stage[place.id, default: 0]
        var found: [String: Int] = [:]
        let bonus = perkValue("scavenge") + (state.scenario == "scavenger" ? 8 : 0)
        if stage < place.stages {
            found = rollLoot(place.loot, bonus: bonus)
            state.stage[place.id] = stage + 1
            state.stats["searches", default: 0] += 1
            if found.isEmpty {
                log("你翻遍 \(place.name)，只找到灰和碎玻璃。", kind: "info")
            } else {
                for (id, n) in found {
                    if content.weapon(id) != nil || content.armor(id) != nil {
                        log("在 \(place.name) 找到 \(content.itemName(id))", kind: "good")
                        grantAny(id, n)
                    } else {
                        addItem(id, n)
                        log("在 \(place.name) 找到 \(content.itemName(id)) ×\(n)", kind: "good")
                    }
                    state.stats["items_found", default: 0] += n
                }
            }
            if state.stage[place.id, default: 0] >= place.stages {
                log("这里已经被你搬空了。再待下去只剩危险。", kind: "info")
            }
        } else {
            log("\(place.name) 已经被搜空，你只听见自己的脚步。", kind: "info")
        }
        state.fatigue += 4
        state.hunger = max(0, state.hunger - 2)
        state.thirst = max(0, state.thirst - 3)
        state.visited.append(place.id)
        checkQuests()

        // 遭遇
        let night = rng.chance(30)
        let hostile = min(85, 18 + place.danger * 11 + (night ? 8 : 0) - perkValue("stealth") * 3)
        if rng.chance(hostile), let eid = pickEnemy(from: place) {
            state.rng = rng
            log("有什么东西从阴影里站了起来。", kind: "bad")
            startBattle(eid)
            save()
            return
        }
        if rng.chance(24) {
            state.rng = rng
            if let ev = pickEvent(place: place) {
                pendingEvent = ev
                save()
                return
            }
        }
        state.rng = rng
        normalize()
        save()
    }

    func pickEnemy(from place: Place) -> String? {
        var rng = state.rng
        var pool: [String] = []
        for id in place.enemies {
            if let e = content.enemy(id) {
                if e.night && !rng.chance(45) { continue }
                let weight = max(1, 6 - e.tier)
                for _ in 0..<weight { pool.append(id) }
            }
        }
        if pool.isEmpty { pool = place.enemies }
        let picked = rng.pick(pool)
        state.rng = rng
        return picked
    }

    func pickEvent(place: Place?) -> EventCard? {
        var rng = state.rng
        var pool: [EventCard] = []
        for e in content.events {
            if e.once && state.seenEvents.contains(e.id) { continue }
            if e.minDay > state.day { continue }
            if !e.places.isEmpty {
                var ok = false
                if let p = place {
                    for token in e.places {
                        if token == p.id || token == p.region || token == "any" || p.tags.contains(token) {
                            ok = true
                            break
                        }
                    }
                }
                if !ok { continue }
            }
            let w = max(1, e.weight)
            for _ in 0..<w { pool.append(e) }
        }
        let picked = rng.pick(pool)
        state.rng = rng
        return picked
    }

    func openEvent(_ id: String) {
        pendingEvent = content.events.first { $0.id == id }
    }

    // MARK: - 移动

    func travel(to placeID: String) {
        guard let p = content.place(placeID) else { return }
        if p.id == state.place { return }
        let crossRegion = p.region != state.region
        guard spendAP(crossRegion ? 2 : 1) else { return }
        state.place = p.id
        state.region = p.region
        if !state.visited.contains(p.id) {
            state.visited.append(p.id)
            state.stats["places_visited", default: 0] += 1
        }
        log("你抵达 \(p.name)。\(p.desc)", kind: "story")
        state.fatigue += crossRegion ? 8 : 4
        var rng = state.rng
        if rng.chance(crossRegion ? 22 : 10), let eid = pickEnemy(from: p) {
            state.rng = rng
            log("路上被截住了。", kind: "bad")
            startBattle(eid)
            save()
            return
        }
        if rng.chance(18) {
            state.rng = rng
            if let ev = pickEvent(place: p) {
                pendingEvent = ev
                checkQuests()
                save()
                return
            }
        }
        state.rng = rng
        checkQuests()
        normalize()
        save()
    }

    // MARK: - 休息

    func rest() {
        guard spendAP() else { return }
        var rng = state.rng
        let safe = state.place == "safehouse"
        state.hp = min(state.hpMax, state.hp + 10 + perkValue("heal") * 2 + buildingLevel("infirmary") * 3)
        state.fatigue = max(0, state.fatigue - 26)
        state.sanity = min(100, state.sanity + 5)
        state.infection = max(0, state.infection - 2)
        log("你缩在角落睡了一会儿，醒来时手指还在发抖，但还活着。", kind: "good")
        if !safe && rng.chance(16) {
            state.rng = rng
            if let p = currentPlace, let eid = pickEnemy(from: p) {
                log("你被惊醒——有东西正在靠近。", kind: "bad")
                startBattle(eid)
                save()
                return
            }
        }
        state.rng = rng
        normalize()
        save()
    }

    // MARK: - 使用物品

    func useItem(_ id: String) {
        guard let item = content.item(id) else { return }
        guard hasItem(id) else { return }
        if item.cat == "throwable" { toast("投掷物只能在战斗中使用。"); return }
        var eff = item.effect
        if item.cat == "med" {
            var healBonus = perkValue("heal")
            if state.scenario == "medic" { healBonus += 10 }
            if let hp = eff["hp"], hp > 0 { eff["hp"] = hp + healBonus }
            if let inf = eff["infection"], inf < 0 { eff["infection"] = inf - perkValue("infectResist") / 5 }
        }
        addItem(id, -1)
        if item.cat == "med" { state.stats["heals", default: 0] += 1 }
        apply(effect: eff)
        log("你使用了 \(item.name)。", kind: "good")
        normalize()
        save()
    }

    func dropItem(_ id: String) {
        addItem(id, -1)
        save()
    }

    func equipWeapon(_ gearID: String) {
        guard state.weapons.contains(where: { $0.id == gearID }) else { return }
        state.equippedWeapon = gearID
        save()
    }

    func equipArmor(_ gearID: String) {
        guard let g = state.armors.first(where: { $0.id == gearID }), let a = content.armor(g.item) else { return }
        state.equippedArmor[a.slot] = gearID
        save()
    }

    func unequipArmor(_ slot: String) {
        state.equippedArmor.removeValue(forKey: slot)
        save()
    }

    func scrapWeapon(_ gearID: String) {
        guard let idx = state.weapons.firstIndex(where: { $0.id == gearID }) else { return }
        let g = state.weapons[idx]
        if let w = content.weapon(g.item) {
            addItem("scrap", max(1, w.rarity + 1))
            log("你把 \(w.name) 拆成了零件。", kind: "info")
        }
        state.weapons.remove(at: idx)
        if state.equippedWeapon == gearID { state.equippedWeapon = state.weapons.first?.id }
        save()
    }

    // MARK: - 制作 / 建设

    func stationLevel(_ station: String) -> Int {
        state.buildings[station, default: 0]
    }

    func canCraft(_ r: Recipe) -> Bool {
        if stationLevel(r.station) < r.stationLevel { return false }
        if state.ap < r.ap { return false }
        for (id, n) in r.cost where !hasItem(id, n) { return false }
        return true
    }

    func craft(_ r: Recipe) {
        guard canCraft(r) else { toast("材料或行动点不足。"); return }
        state.ap -= r.ap
        for (id, n) in r.cost { addItem(id, -n) }
        for (id, n) in r.out { addItem(id, n) }
        if let wid = r.outWeapon, let w = content.weapon(wid) {
            let g = GearInstance(id: UUID().uuidString, item: wid, dur: w.dur)
            state.weapons.append(g)
            if state.equippedWeapon == nil { state.equippedWeapon = g.id }
        }
        if let aid = r.outArmor, let a = content.armor(aid) {
            let g = GearInstance(id: UUID().uuidString, item: aid, dur: 100)
            state.armors.append(g)
            if state.equippedArmor[a.slot] == nil { state.equippedArmor[a.slot] = g.id }
        }
        state.stats["crafts", default: 0] += 1
        if r.outWeapon != nil { state.stats["weapons_crafted", default: 0] += 1 }
        if r.outArmor != nil { state.stats["armors_crafted", default: 0] += 1 }
        if perkValue("craft") > 0 && state.rng.chance(min(60, perkValue("craft") * 5)) {
            if let bonus = r.out.first {
                addItem(bonus.key, bonus.value)
                log("手艺熟练，多做出了 \(content.itemName(bonus.key))。", kind: "good")
            }
        }
        log("你制作了 \(r.name)。", kind: "good")
        checkAchievements()
        normalize()
        save()
    }

    func buildingLevel(_ id: String) -> Int { state.buildings[id, default: 0] }

    func upgrade(_ b: Building) {
        let level = buildingLevel(b.id)
        guard level < b.maxLevel else { toast("已经升到顶了。"); return }
        let cost = b.cost(level: level + 1)
        for (id, n) in cost where !hasItem(id, n) {
            toast("缺少 \(content.itemName(id)) ×\(n)")
            return
        }
        for (id, n) in cost { addItem(id, -n) }
        state.buildings[b.id] = level + 1
        if b.effectKey == "hpMax" { state.hpMax += b.perLevel; state.hp += b.perLevel }
        if b.effectKey == "ap" { state.apMax += b.perLevel; state.ap += b.perLevel }
        state.stats["builds", default: 0] += 1
        log("\(b.name) 升级至 Lv.\(level + 1)。", kind: "good")
        toast("\(b.name) Lv.\(level + 1)")
        normalize()
        save()
    }

    // MARK: - 战斗

    func startBattle(_ enemyID: String, eventID: String? = nil) {
        guard let e = content.enemy(enemyID) else { return }
        var s = BattleState(enemy: e.id, hp: e.hp, maxHP: e.hp, round: 1, log: [],
                            cd: [:], aim: 0, dodge: 0, escaped: false, ended: false,
                            victory: false, loot: [:], eventID: eventID, enemyMaxHP: e.hp)
        s.log = ["\(e.name) 挡在你面前。"]
        state.battle = s
        state.stats["battles", default: 0] += 1
        save()
    }

    func battleAction(_ action: BattleAction) {
        guard var b = state.battle, !b.ended, let e = content.enemy(b.enemy) else { return }
        var rng = state.rng
        var extra: [String] = []
        var skipEnemy = false

        switch action {
        case .attack, .heavy:
            guard let gIndex = state.weapons.firstIndex(where: { $0.id == state.equippedWeapon }) else {
                extra.append("你没有可用的武器，只能用拳头。")
                break
            }
            let gear = state.weapons[gIndex]
            let w = content.weapon(gear.item) ?? ContentStore.fist
            if let ammo = w.ammo {
                if hasItem(ammo) {
                    addItem(ammo, -1)
                } else {
                    extra.append("没有 \(content.itemName(ammo)) 了，你只能近身。")
                }
            }
            let heavy = action == .heavy
            var noAmmo = false
            if let ammo = w.ammo, !hasItem(ammo) {
                noAmmo = true
                extra.append("没有弹药，你只能把枪当棍子挥。")
            }
            var dmg = w.dmg + rng.int(0...max(0, w.dmgVar))
            if noAmmo { dmg = max(4, w.dmg / 3) }
            dmg += perkValue("dmg")
            if state.scenario == "veteran" { dmg = dmg * 12 / 10 }
            if heavy { dmg = dmg * 3 / 2 }
            let hitChance = w.acc + perkValue("acc") + b.aim - e.evade - (heavy ? 18 : 0) + (state.fatigue > 60 ? -8 : 0) - (noAmmo ? 20 : 0)
            if rng.chance(max(12, min(97, hitChance))) {
                var crit = rng.chance(min(70, w.crit + perkValue("crit") + b.aim / 2))
                if heavy && rng.chance(12) { crit = true }
                var final = dmg
                if crit { final = final * 2 }
                final = max(1, final - e.armor)
                b.hp -= final
                extra.append(crit ? "暴击！你对 \(e.name) 造成 \(final) 点伤害。" : "你击中 \(e.name)，造成 \(final) 点伤害。")
                if w.traits.contains("bleed") && rng.chance(35) {
                    b.hp -= 4
                    extra.append("伤口撕开，\(e.name) 在流血（+4）。")
                }
                if w.traits.contains("stun") && rng.chance(25) {
                    skipEnemy = true
                    extra.append("\(e.name) 被打得踉跄，失去一次行动。")
                }
            } else {
                extra.append("你挥空了。\(e.name) 嗅到了你的恐惧。")
            }
            state.weapons[gIndex].dur -= heavy ? 2 : 1
            if state.weapons[gIndex].dur <= 0 {
                let broken = w.name
                state.weapons.remove(at: gIndex)
                state.equippedWeapon = state.weapons.first?.id
                extra.append("\(broken) 断在了手里。")
            }
            b.aim = 0
            state.stats["damage_dealt", default: 0] += max(0, finalDamage(dmg: dmg, enemy: e))

        case .aim:
            b.aim = min(40, b.aim + 20)
            extra.append("你稳住呼吸，瞄准了 \(e.name) 的要害。")
        case .dodge:
            b.dodge = 30
            extra.append("你压低身子，准备闪避。")
        case .item:
            if let heal = bestHealItem() {
                useItem(heal)
                extra.append("你用了 \(content.itemName(heal))。")
            } else {
                extra.append("你摸遍口袋，什么药都没有。")
            }
        case .throwable:
            if let t = bestThrowable() {
                addItem(t, -1)
                let dmg = 18 + rng.int(0...14) + perkValue("dmg")
                b.hp -= dmg
                extra.append("你扔出 \(content.itemName(t))，造成 \(dmg) 点伤害。")
            } else {
                extra.append("没有可以扔的东西。")
            }
        case .flee:
            let chance = 42 + evadeValue - e.tier * 4 + perkValue("flee")
            if rng.chance(max(10, chance)) {
                b.ended = true
                b.escaped = true
                b.log.append("你逃开了。")
                state.battle = b
                state.rng = rng
                log("你从 \(e.name) 手里逃了出来，代价是丢下了些尊严。", kind: "info")
                save()
                return
            }
            extra.append("逃跑失败，\(e.name) 扑了上来。")
        }

        for line in extra { b.log.append(line) }

        if b.hp <= 0 {
            finishVictory(&b, enemy: e)
            state.rng = rng
            state.battle = b
            save()
            return
        }

        if !skipEnemy && b.hp > 0 {
            enemyTurn(&b, enemy: e, rng: &rng)
        }
        b.dodge = max(0, b.dodge - 12)
        b.round += 1
        for (k, v) in b.cd { b.cd[k] = max(0, v - 1) }
        state.rng = rng
        if state.ending != nil {
            b.ended = true
            b.victory = false
            b.escaped = false
            b.log.append("视野边缘开始发黑。")
        } else {
            checkDeath()
            if state.ending != nil {
                b.ended = true
                b.victory = false
                b.escaped = false
                b.log.append("视野边缘开始发黑。")
            }
        }
        state.battle = b
        normalize()
        save()
    }

    private func finalDamage(dmg: Int, enemy: Enemy) -> Int {
        max(1, dmg - enemy.armor)
    }

    private func enemyTurn(_ b: inout BattleState, enemy e: Enemy, rng: inout SeededRNG) {
        var ability: EnemyAbility? = nil
        if !e.abilities.isEmpty && rng.chance(35) {
            let ready = e.abilities.filter { b.cd[$0, default: 0] <= 0 }
            if let id = rng.pick(ready), let ab = content.ability(id) {
                ability = ab
                b.cd[id] = 3
            }
        }
        let dodge = b.dodge
        let hit = e.acc + (ability != nil ? 5 : 0) - evadeValue - dodge
        if !rng.chance(max(10, min(95, hit))) {
            b.log.append("\(e.name) 扑空，撞在墙上。")
            return
        }
        var dmg = (ability?.dmg ?? e.dmg) + rng.int(0...4) - armorValue / 3
        dmg = max(1, dmg)
        state.hp -= dmg
        b.log.append(ability != nil ? "\(e.name) 使用『\(ability!.name)』，你受到 \(dmg) 点伤害。" : "\(e.name) 抓伤了你，\(dmg) 点伤害。")

        if let ab = ability {
            switch ab.kind {
            case "infect":
                state.infection = min(100, state.infection + 6 + e.tier * 2)
                b.log.append("伤口发烫，感染值上升。")
            case "bleed":
                state.stats["bleeding", default: 0] += 1
                state.hp -= 3
                b.log.append("你开始流血（-3）。")
            case "drain":
                state.fatigue = min(100, state.fatigue + 12)
                b.log.append("你感到力气被抽走。")
            case "fear":
                state.sanity = max(0, state.sanity - 8)
                b.log.append("那声音钻进脑子里，理智下降。")
            case "rage":
                b.log.append("它愈发狂躁。")
            default:
                if rng.chance(30) { state.infection = min(100, state.infection + 3) }
            }
        } else {
            if rng.chance(20 + e.tier * 4) {
                state.infection = min(100, state.infection + 3 + e.tier)
                b.log.append("它的指甲划破了你的皮肤，感染值上升。")
            }
        }
        if state.hp <= 0 { triggerEnding("death_torn") }
    }

    private func finishVictory(_ b: inout BattleState, enemy e: Enemy) {
        b.ended = true
        b.victory = true
        b.hp = 0
        state.stats["kills", default: 0] += 1
        state.stats["kill_\(e.tag)", default: 0] += 1
        state.stats["kill_\(e.id)", default: 0] += 1
        meta.totalKills += 1
        if e.tag == "boss" { state.stats["boss_kills", default: 0] += 1 }
        state.flags["seen_\(e.id)"] = 1
        state.stats["battles_won", default: 0] += 1
        if e.night { state.stats["night_battles", default: 0] += 1 }
        if let k = weapon?.kind {
            if k == "gun" || k == "bow" { state.stats["gun_kills", default: 0] += 1 }
            else { state.stats["melee_kills", default: 0] += 1 }
        }
        addXP(e.xp)
        let loot = rollLoot(e.loot)
        for (id, n) in loot {
            grantAny(id, n)
            b.loot[id, default: 0] += n
        }
        b.log.append("\(e.name) 倒下了。")
        log("你杀死了 \(e.name)。", kind: "good")
        state.fatigue = min(100, state.fatigue + 6)
        state.sanity = max(0, state.sanity - (e.tag == "human" ? 3 : 0))
        checkAchievements()
        checkQuests()
        save()
    }

    func closeBattle() {
        guard let b = state.battle, b.ended else { return }
        state.battle = nil
        if b.victory && !b.loot.isEmpty {
            lastBattleSummary = "战利品：" + b.loot.map { "\(content.itemName($0.key))×\($0.value)" }.joined(separator: "、")
        } else {
            lastBattleSummary = b.escaped ? "你逃走了。" : nil
        }
        normalize()
        save()
    }

    func bestHealItem() -> String? {
        let order = ["medkit", "serum", "antibiotics", "bandage", "pills_pain", "herbs_poultice", "energy_bar", "water_bottle"]
        for id in order where hasItem(id) {
            if let it = content.item(id), !it.effect.isEmpty { return id }
        }
        return state.inventory.keys.first { id in
            guard let it = content.item(id) else { return false }
            return it.cat == "med" && !it.effect.isEmpty && (it.effect["hp"] ?? 0) > 0
        }
    }

    func bestThrowable() -> String? {
        let order = ["pipe_bomb", "grenade", "molotov", "smoke_grenade", "flashbang", "throwing_knife", "brick"]
        for id in order where hasItem(id) { return id }
        return nil
    }

    // MARK: - 事件

    func canChoose(_ c: EventChoice) -> Bool {
        for req in c.req {
            if !checkRequirement(req) { return false }
        }
        return true
    }

    func checkRequirement(_ req: String) -> Bool {
        if req.isEmpty || req == "none" { return true }
        if req.hasPrefix("item:") {
            var s = String(req.dropFirst(5))
            var need = 1
            if let range = s.range(of: ">=") {
                need = Int(s[range.upperBound...]) ?? 1
                s = String(s[..<range.lowerBound])
            }
            return hasItem(s, need)
        }
        if req.hasPrefix("perk:") { return state.perks[String(req.dropFirst(5))] != nil }
        if req.hasPrefix("faction:") {
            var s = String(req.dropFirst(8))
            var need = 1
            if let range = s.range(of: ">=") {
                need = Int(s[range.upperBound...]) ?? 1
                s = String(s[..<range.lowerBound])
            }
            return (state.faction[s] ?? 0) >= need
        }
        if req.hasPrefix("flag:") {
            var s = String(req.dropFirst(5))
            var need = 1
            if let range = s.range(of: ">=") {
                need = Int(s[range.upperBound...]) ?? 1
                s = String(s[..<range.lowerBound])
            }
            return (state.flags[s] ?? 0) >= need
        }
        if req.hasPrefix("hp>=") { return state.hp >= (Int(req.dropFirst(4)) ?? 0) }
        if req.hasPrefix("thirst>=") { return state.thirst >= (Int(req.dropFirst(8)) ?? 0) }
        if req.hasPrefix("sanity>=") { return state.sanity >= (Int(req.dropFirst(8)) ?? 0) }
        if req.hasPrefix("day>=") { return state.day >= (Int(req.dropFirst(5)) ?? 0) }
        if req.hasPrefix("companions>=") { return state.companions.filter { $0.alive }.count >= (Int(req.dropFirst(12)) ?? 0) }
        if req.hasPrefix("weapon:") { return weapon?.kind == String(req.dropFirst(7)) }
        if req.hasPrefix("hasweapon") { return weapon != nil }
        return false
    }

    func choose(_ choice: EventChoice, from event: EventCard) {
        guard canChoose(choice) else { toast("条件不满足。"); return }
        state.seenEvents.append(event.id)
        var rng = state.rng
        let success = rng.chance(max(1, min(100, choice.chance)))
        state.rng = rng
        let eff = success ? choice.effect : choice.effectFail
        apply(effect: eff)
        apply(items: success ? choice.items : [:])
        if success {
            if !choice.log.isEmpty { log(choice.log, kind: "story") }
        } else {
            if !choice.logFail.isEmpty { log(choice.logFail, kind: "bad") }
        }
        pendingEvent = nil
        eventResult = success ? choice.log : choice.logFail
        save()
        if let fight = choice.fight, state.ending == nil {
            startBattle(fight, eventID: event.id)
            return
        }
        if let endID = choice.ending, state.ending == nil {
            triggerEnding(endID)
            return
        }
        if success, let next = choice.next, let ev = content.events.first(where: { $0.id == next }) {
            pendingEvent = ev
            return
        }
        checkAchievements()
        checkQuests()
        normalize()
    }

    func apply(items: [String: Int]) {
        for (id, n) in items {
            if n < 0 {
                if content.weapon(id) != nil || content.armor(id) != nil {
                    grantAny(id, n)
                    log("失去 \(content.itemName(id))", kind: "bad")
                } else {
                    if !hasItem(id, -n) { continue }
                    addItem(id, n)
                    log("失去 \(content.itemName(id)) ×\(-n)", kind: "bad")
                }
            } else if n > 0 {
                grantAny(id, n)
            }
        }
    }

    // MARK: - 一天结束

    func endDay() {
        guard state.ending == nil else { return }
        var rng = state.rng
        state.day += 1
        state.stats["days", default: 0] = state.day

        // 生存消耗
        var hungerLoss = 15
        var thirstLoss = 20
        if state.scenario == "deserter" || state.scenario == "child" { hungerLoss += 3; thirstLoss += 4 }
        state.hunger = max(0, state.hunger - hungerLoss)
        state.thirst = max(0, state.thirst - thirstLoss)
        state.fatigue = min(100, state.fatigue + 10)
        state.sanity = max(0, state.sanity - max(0, (state.companions.filter { $0.alive }.isEmpty ? 3 : 1) - perkValue("sanity") / 3))
        if state.infection >= 80 { state.stats["infection_survived", default: 0] += 1 }
        if currentWeight > Double(carryCapacity) { state.stats["overweight", default: 0] = 1 }
        if state.hunger == 0 {
            state.hp -= 6
            log("饥饿在啃你的胃。你开始发晕。", kind: "bad")
        }
        if state.thirst == 0 {
            state.hp -= 9
            log("嘴唇裂开，喉咙像塞了沙子。", kind: "bad")
        }
        if state.thirst == 0 && state.hunger == 0 { state.hp -= 5 }

        // 温度
        let cold = 60 - state.warmth
        if cold > 0 {
            state.warmth = max(0, state.warmth - 6)
            if state.warmth < 25 { state.hp -= 3; log("夜里太冷，你发抖到天亮。", kind: "bad") }
        }

        // 感染
        if state.infection > 0 {
            if state.infection >= 60 {
                state.infection = min(100, state.infection + 3)
                log("血管里有东西在爬。", kind: "bad")
            } else if rng.chance(50) {
                state.infection = max(0, state.infection - 2)
            }
        }

        // 据点产出
        let water = buildingLevel("collector")
        let garden = buildingLevel("garden")
        if water > 0 { addItem("water_dirty", water) }
        if garden > 0 { addItem("vegetable", garden / 2 + 1) }
        if buildingLevel("still") > 0 && garden > 1 { addItem("moonshine", 1) }

        // 同伴任务
        companionDaily()

        // 夜袭
        let guardPower = buildingLevel("wall") * 6 + buildingLevel("tower") * 5 + buildingLevel("trap_line") * 3 + state.companions.filter { $0.task == "guard" }.count * 8
        let raidChance = max(4, 20 - guardPower / 2)
        if rng.chance(raidChance) {
            let raiders = ["walker_shambler", "walker_shambler", "human_looter", "hound_stray", "walker_runner"]
            if let eid = rng.pick(raiders) {
                state.rng = rng
                log("夜里，围墙外传来抓挠声。", kind: "bad")
                state.ap = max(1, apCap)
                startBattle(eid, eventID: "raid")
                save()
                return
            }
        }

        state.ap = apCap
        state.rng = rng

        if let j = content.journal.randomElement() {
            log("〔\(j.src)〕\(j.text)", kind: "story")
        }

        checkAchievements()
        checkQuests()
        normalize()
        save()
        if state.ending != nil { return }

        // 每日事件
        if rng.chance(38) {
            if let ev = pickDailyEvent() {
                pendingEvent = ev
                save()
                return
            }
        }
        if state.day >= 75 && state.flags["lighthouse_known", default: 0] == 0 {
            state.flags["lighthouse_known"] = 1
            log("收音机里忽然有人说话：『灯塔还在运转，带上核心来。』", kind: "story")
        }
    }

    private func pickDailyEvent() -> EventCard? {
        var rng = state.rng
        var pool: [EventCard] = []
        for e in content.events where e.tag == "daily" {
            if e.once && state.seenEvents.contains(e.id) { continue }
            if e.minDay > state.day { continue }
            for _ in 0..<max(1, e.weight) { pool.append(e) }
        }
        let picked = rng.pick(pool)
        state.rng = rng
        return picked
    }

    private func companionDaily() {
        for i in state.companions.indices where state.companions[i].alive {
            let c = state.companions[i]
            guard let npc = content.npc(c.id) else { continue }
            switch c.task {
            case "scavenge":
                if state.rng.chance(65) {
                    let pool = ["scrap", "cloth", "canned_food", "water_bottle", "wire", "wood", "ammo_9mm"]
                    if let id = state.rng.pick(pool) {
                        let n = state.rng.int(1...2)
                        addItem(id, n)
                        log("\(npc.name) 带回 \(content.itemName(id)) ×\(n)。", kind: "good")
                        state.companions[i].trust = min(100, c.trust + 1)
                    }
                } else {
                    state.companions[i].trust = max(0, c.trust - 2)
                    state.hp = max(1, state.hp - 0)
                    log("\(npc.name) 空着手回来，衣服上有新的血。", kind: "info")
                }
            case "guard":
                state.companions[i].trust = min(100, c.trust + 1)
            case "cook":
                state.hunger = min(100, state.hunger + 10)
                log("\(npc.name) 煮了一锅勉强能喝的东西。", kind: "good")
            case "craft":
                addItem("scrap", 1)
                if state.rng.chance(30) { addItem("duct_tape", 1) }
                log("\(npc.name) 在工作台前敲了一晚上。", kind: "info")
            default:
                if state.rng.chance(25) { state.sanity = min(100, state.sanity + 3) }
            }
        }
    }

    // MARK: - 同伴

    func meetNPC(_ id: String) {
        state.flags["met_\(id)"] = 1
        if let npc = content.npc(id) {
            log("你遇见了 \(npc.name)——\(npc.role)。", kind: "story")
        }
    }

    func canRecruit(_ npc: NPC) -> Bool {
        if state.companions.contains(where: { $0.id == npc.id }) { return false }
        if state.flags["met_\(npc.id)", default: 0] == 0 { return false }
        if state.companions.filter({ $0.alive }).count >= 4 { return false }
        return true
    }

    func recruit(_ npc: NPC) {
        guard canRecruit(npc) else { toast("现在还不能招募他/她。"); return }
        state.companions.append(CompanionState(id: npc.id, trust: npc.trust, task: "idle", alive: true))
        state.stats["recruited", default: 0] += 1
        state.perks[npc.perkID, default: 0] += 1
        state.flags["recruited_\(npc.id)"] = 1
        log("\(npc.name) 加入了据点。", kind: "good")
        if let q = npc.questID, content.quest(q) != nil {
            if !state.activeQuests.contains(where: { $0.id == q }) && !state.doneQuests.contains(q) {
                acceptQuest(q)
            }
        }
        checkAchievements()
        save()
    }

    func assign(_ companionID: String, task: String) {
        guard let idx = state.companions.firstIndex(where: { $0.id == companionID }) else { return }
        state.companions[idx].task = task
        save()
    }

    // MARK: - 任务

    func acceptQuest(_ id: String) {
        guard let q = content.quest(id) else { return }
        guard !state.activeQuests.contains(where: { $0.id == id }), !state.doneQuests.contains(id) else { return }
        state.activeQuests.append(QuestState(id: id, progress: 0, done: false))
        log("接受任务：\(q.title)。", kind: "story")
        save()
    }

    func questProgress(_ q: QuestDef) -> Int {
        switch q.kind {
        case "kill": return state.stats["kill_\(q.target)", default: 0]
        case "collect": return state.inventory[q.target, default: 0]
        case "visit": return state.visited.contains(q.target) ? 1 : 0
        case "day": return state.day
        case "craft": return state.stats["crafts", default: 0]
        default: return 0
        }
    }

    func checkQuests() {
        for qs in state.activeQuests {
            guard let q = content.quest(qs.id) else { continue }
            let p = questProgress(q)
            if p >= q.count {
                state.activeQuests.removeAll { $0.id == q.id }
                if !state.doneQuests.contains(q.id) { state.doneQuests.append(q.id) }
                addXP(q.rewardXP)
                state.stats["quests_done", default: 0] += 1
                for (id, n) in q.rewardItems { grantAny(id, n) }
                for (k, v) in q.rewardItems where k == "shards" { meta.shards += v }
                log("任务完成：\(q.title)。", kind: "good")
                toast("任务完成：\(q.title)")
                if let next = q.next { acceptQuest(next) }
            }
        }
    }

    func availableQuests() -> [QuestDef] {
        content.questList.filter { q in
            guard !state.doneQuests.contains(q.id) else { return false }
            guard !state.activeQuests.contains(where: { $0.id == q.id }) else { return false }
            if q.giver == "light" { return false }
            return true
        }
    }

    // MARK: - 技能

    func perkRank(_ id: String) -> Int { state.perks[id, default: 0] }

    func canLearn(_ p: Perk) -> Bool {
        if perkRank(p.id) >= p.maxRank { return false }
        if state.perkPoints <= 0 { return false }
        if p.tier > 1 && perkRank(p.id) == 0 {
            let prev = content.perkList.contains { other in
                other.branch == p.branch && other.tier == p.tier - 1 && perkRank(other.id) > 0
            }
            if !prev { return false }
        }
        return true
    }

    func learn(_ p: Perk) {
        guard canLearn(p) else { toast("属性点不足或前置未解锁。"); return }
        state.perkPoints -= 1
        state.perks[p.id, default: 0] += 1
        if let hpUp = p.effect["hpMax"], hpUp > 0 {
            state.hpMax += hpUp
            state.hp += hpUp
        }
        log("技能提升：\(p.name) Lv.\(state.perks[p.id] ?? 1)", kind: "good")
        normalize()
        save()
    }

    // MARK: - 结局 / 成就

    func triggerEnding(_ id: String) {
        guard state.ending == nil else { return }
        state.ending = id
        state.stats["run_days", default: 0] = state.day
        state.stats["ending_\(id)", default: 0] = 1
        meta.bestDay = max(meta.bestDay, state.day)
        meta.totalKills = max(meta.totalKills, meta.totalKills + state.stats["kills", default: 0])
        if !meta.endings.contains(id) { meta.endings.append(id) }
        meta.shards += max(3, state.day / 4 + state.stats["kills", default: 0] / 8)
        if let e = content.ending(id) {
            endingCard = e
        }
        checkAchievements()
        screen = .ending
        save()
    }

    func statValue(_ key: String) -> Int {
        if key.hasPrefix("flag_") { return state.flags[String(key.dropFirst(5)), default: 0] }
        if key == "cores_held" { return state.inventory["light_core", default: 0] }
        if key == "valuables" {
            var sum = 0
            for (id, n) in state.inventory where content.item(id)?.cat == "valuable" {
                sum += (content.item(id)?.value ?? 0) * n
            }
            return sum
        }
        if key == "enemy_types" {
            return state.flags.keys.filter { $0.hasPrefix("seen_") }.count
        }
        switch key {
        case "days": return state.day
        case "runs": return meta.runs
        case "endings": return meta.endings.count
        case "kills": return state.stats["kills", default: 0]
        case "shards": return meta.shards
        default: return state.stats[key, default: 0]
        }
    }

    func checkAchievements() {
        for a in content.achievements {
            if meta.achievements[a.id] != nil { continue }
            if statValue(a.key) >= a.goal {
                meta.achievements[a.id] = state.day
                toast("成就解锁：\(a.name)")
                log("成就解锁：\(a.name)", kind: "good")
            }
        }
    }

    func unlockedScenarios() -> [Scenario] {
        ContentStore.scenarios.filter { ContentStore.isUnlocked($0, meta: meta) }
    }

    func newRunFromEnding() {
        endingCard = nil
        state = GameStore.blankState()
        screen = .home
        panel = nil
        save()
    }
}
