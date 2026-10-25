import Foundation

final class ContentStore {
    static let shared = ContentStore()

    private(set) var items: [String: Item] = [:]
    private(set) var weapons: [String: Weapon] = [:]
    private(set) var armors: [String: Armor] = [:]
    private(set) var enemies: [String: Enemy] = [:]
    private(set) var abilities: [String: EnemyAbility] = [:]
    private(set) var places: [String: Place] = [:]
    private(set) var events: [EventCard] = []
    private(set) var recipes: [Recipe] = []
    private(set) var perks: [String: Perk] = [:]
    private(set) var buildings: [Building] = []
    private(set) var achievements: [Achievement] = []
    private(set) var endings: [String: Ending] = [:]
    private(set) var npcs: [String: NPC] = [:]
    private(set) var quests: [String: QuestDef] = [:]
    private(set) var journal: [JournalEntry] = []

    private(set) var itemList: [Item] = []
    private(set) var weaponList: [Weapon] = []
    private(set) var armorList: [Armor] = []
    private(set) var enemyList: [Enemy] = []
    private(set) var placeList: [Place] = []
    private(set) var perkList: [Perk] = []
    private(set) var npcList: [NPC] = []
    private(set) var questList: [QuestDef] = []

    private init() {
        items = Self.index(loadArray("items", Item.self))
        weapons = Self.index(loadArray("weapons", Weapon.self))
        armors = Self.index(loadArray("armor", Armor.self))
        enemies = Self.index(loadArray("enemies", Enemy.self))
        abilities = Self.index(loadArray("abilities", EnemyAbility.self))
        places = Self.index(loadArray("places", Place.self))
        events = loadArray("events", EventCard.self)
        recipes = loadArray("recipes", Recipe.self)
        perks = Self.index(loadArray("perks", Perk.self))
        buildings = loadArray("buildings", Building.self)
        achievements = loadArray("achievements", Achievement.self)
        endings = Self.index(loadArray("endings", Ending.self))
        npcs = Self.index(loadArray("npcs", NPC.self))
        quests = Self.index(loadArray("quests", QuestDef.self))
        journal = loadArray("journal", JournalEntry.self)

        itemList = items.values.sorted { ($0.tier, $0.cat, $0.name) < ($1.tier, $1.cat, $1.name) }
        weaponList = weapons.values.sorted { ($0.rarity, $0.name) < ($1.rarity, $1.name) }
        armorList = armors.values.sorted { ($0.rarity, $0.name) < ($1.rarity, $1.name) }
        enemyList = enemies.values.sorted { ($0.tier, $0.name) < ($1.tier, $1.name) }
        placeList = places.values.sorted { ($0.region, $0.name) < ($1.region, $1.name) }
        perkList = perks.values.sorted { ($0.branch, $0.tier, $0.name) < ($1.branch, $1.tier, $1.name) }
        npcList = npcs.values.sorted { $0.name < $1.name }
        questList = quests.values.sorted { $0.giver < $1.giver }
    }

    private static func index<T>(_ arr: [T]) -> [String: T] where T: ContentIdentifiable {
        var out: [String: T] = [:]
        for v in arr { out[v.contentID] = v }
        return out
    }

    private func loadArray<T: Decodable>(_ name: String, _ type: T.Type) -> [T] {
        var url = Bundle.main.url(forResource: name, withExtension: "json")
        if url == nil {
            url = Bundle.main.url(forResource: name, withExtension: "json", subdirectory: "Content")
        }
        guard let file = url else {
            print("⚠️ missing content: \(name).json")
            return []
        }
        do {
            return try JSONDecoder().decode([T].self, from: try Data(contentsOf: file))
        } catch {
            print("⚠️ content decode failed \(name): \(error)")
            return []
        }
    }

    // MARK: - 查询

    func item(_ id: String) -> Item? { items[id] }
    func itemName(_ id: String) -> String { items[id]?.name ?? weapons[id]?.name ?? armors[id]?.name ?? id }
    func weapon(_ id: String) -> Weapon? { weapons[id] }
    func armor(_ id: String) -> Armor? { armors[id] }
    func enemy(_ id: String) -> Enemy? { enemies[id] }
    func place(_ id: String) -> Place? { places[id] }
    func perk(_ id: String) -> Perk? { perks[id] }
    func quest(_ id: String) -> QuestDef? { quests[id] }
    func npc(_ id: String) -> NPC? { npcs[id] }
    func ending(_ id: String) -> Ending? { endings[id] }
    func ability(_ id: String) -> EnemyAbility? { abilities[id] }

    func places(in region: String) -> [Place] {
        placeList.filter { $0.region == region }
    }

    static let regionOrder = ["旧城区", "工业区", "近郊农野", "军事管制区", "城市核心"]

    func unlockedPlaces(_ visited: [String]) -> [Place] {
        placeList.filter { p in
            if p.tags.contains("start") { return true }
            if visited.contains(p.id) { return true }
            guard let first = p.tags.first(where: { $0.hasPrefix("unlock:") }) else { return true }
            let need = String(first.dropFirst("unlock:".count))
            return visited.contains(need)
        }
    }
}

struct Faction: Identifiable {
    let id: String
    let name: String
    let desc: String
    let icon: String
}

protocol ContentIdentifiable {
    var contentID: String { get }
}

extension Item: ContentIdentifiable { var contentID: String { id } }
extension Weapon: ContentIdentifiable { var contentID: String { id } }
extension Armor: ContentIdentifiable { var contentID: String { id } }
extension Enemy: ContentIdentifiable { var contentID: String { id } }
extension EnemyAbility: ContentIdentifiable { var contentID: String { id } }
extension Place: ContentIdentifiable { var contentID: String { id } }
extension Perk: ContentIdentifiable { var contentID: String { id } }
extension Ending: ContentIdentifiable { var contentID: String { id } }
extension NPC: ContentIdentifiable { var contentID: String { id } }
extension QuestDef: ContentIdentifiable { var contentID: String { id } }

// MARK: - 剧本

extension ContentStore {
    static let fist = Weapon(id: "fist", name: "空手", kind: "fist",
                             desc: "没有武器的时候，你还有牙齿和指甲。",
                             dmg: 5, dmgVar: 3, crit: 5, acc: 78, apCost: 1, dur: 9999,
                             value: 0, rarity: 0, weight: 0, ammo: nil, traits: [],
                             icon: "hand.raised.fill")

    static let scenarios: [Scenario] = [
        Scenario(id: "survivor", name: "幸存者", tagline: "你只活到了今天",
                 desc: "标准开局。三天口粮、一根铁管、一件旧夹克，以及一座漏风的据点。",
                 unlock: nil, perks: [:], items: ["canned_food": 2, "water_bottle": 3, "bandage": 2, "cloth": 2],
                 weapon: "pipe", armor: ["jakcet_old"], hpBonus: 0, apBonus: 0),
        Scenario(id: "veteran", name: "退伍老兵", tagline: "枪声比心跳熟悉",
                 desc: "战斗专精。近战伤害 +20%，初始携带手枪与弹药，但精神更脆弱。",
                 unlock: "kills:60", perks: ["marksman": 1], items: ["ammo_9mm": 12, "bandage": 1, "canned_food": 1],
                 weapon: "pistol_9mm", armor: ["jacket_old"], hpBonus: 10, apBonus: 0),
        Scenario(id: "engineer", name: "工程师", tagline: "没有修不好的东西",
                 desc: "制作与据点专精。制作不消耗额外行动点，初始带工具箱与大量零件。",
                 unlock: "ach:first_craft", perks: ["handy": 2], items: ["scrap": 8, "duct_tape": 4, "wire": 3, "canned_food": 2],
                 weapon: "wrench", armor: ["gloves_work"], hpBonus: 0, apBonus: 0),
        Scenario(id: "medic", name: "急诊科医生", tagline: "先止血，再谈以后",
                 desc: "医疗专精。治疗效率 +40%，抗感染 +30%，药品储备充足。",
                 unlock: "ach:first_heal", perks: ["field_medic": 2], items: ["bandage": 4, "antibiotics": 2, "pills_pain": 2, "water_bottle": 2],
                 weapon: "knife_scalpel", armor: [], hpBonus: 5, apBonus: 0),
        Scenario(id: "scavenger", name: "拾荒者", tagline: "垃圾里什么都有",
                 desc: "搜刮专精。搜刮产出 +35%，背包更大，但体质偏弱。",
                 unlock: "ach:first_search", perks: ["scrounger": 2], items: ["backpack_small": 1, "canned_food": 3, "water_bottle": 2],
                 weapon: "crowbar", armor: ["jakcet_old"], hpBonus: -5, apBonus: 0),
        Scenario(id: "hunter", name: "猎人", tagline: "我听见它在林子里",
                 desc: "远程专精。弓弩与潜行加成，自带复合弓，但枪械起步更晚。",
                 unlock: "kills:25", perks: ["deadeye": 2], items: ["arrow": 12, "dried_meat": 2, "water_bottle": 2, "bandage": 1],
                 weapon: "bow_compound", armor: ["jacket_old"], hpBonus: 0, apBonus: 0),
        Scenario(id: "zealot", name: "灰袍信徒", tagline: "灰烬之后有新生",
                 desc: "意志专精。精神抗性大幅提升，可与灰袍教团交好，但被军方通缉。",
                 unlock: "ach:join_order", perks: ["zeal": 2], items: ["canned_food": 2, "water_bottle": 2, "herbs_tea": 2],
                 weapon: "machete", armor: ["robe_gray"], hpBonus: 0, apBonus: 0),
        Scenario(id: "deserter", name: "逃兵", tagline: "别回头，别信口令",
                 desc: "高难度。军方与你敌对，开局带军用装备，饥饿与口渴衰减更快。",
                 unlock: "endings:3", perks: ["tough": 1], items: ["mre": 1, "water_bottle": 2, "ammo_556": 20],
                 weapon: "rifle_ar", armor: ["vest_kevlar"], hpBonus: 5, apBonus: 0),
        Scenario(id: "child", name: "十四岁", tagline: "大人都不在了",
                 desc: "极限难度。体质与负重受限，无法使用重型武器，但更容易被幸存者怜悯。",
                 unlock: "bestDay:20", perks: ["light_step": 2], items: ["canned_food": 1, "water_bottle": 1, "candy": 2],
                 weapon: "knife_folding", armor: [], hpBonus: -20, apBonus: 1),
        Scenario(id: "ghost", name: "无名者", tagline: "档案里没有你",
                 desc: "进阶。潜行极强，敌人更难发现你，初始携带烟雾弹与消音手枪。",
                 unlock: "shards:40", perks: ["ghost": 2], items: ["smoke_grenade": 2, "ammo_9mm": 8, "lockpick": 1],
                 weapon: "pistol_silenced", armor: ["hood_cloth"], hpBonus: 0, apBonus: 0)
    ]

    static func scenario(_ id: String) -> Scenario {
        scenarios.first { $0.id == id } ?? scenarios[0]
    }

    static func isUnlocked(_ s: Scenario, meta: MetaState) -> Bool {
        guard let rule = s.unlock else { return true }
        let parts = rule.split(separator: ":")
        guard parts.count == 2 else { return true }
        let key = String(parts[0])
        let val = String(parts[1])
        switch key {
        case "bestDay": return meta.bestDay >= (Int(val) ?? 0)
        case "kills": return meta.totalKills >= (Int(val) ?? 0)
        case "shards": return meta.shards >= (Int(val) ?? 0)
        case "endings": return meta.endings.count >= (Int(val) ?? 0)
        case "ach": return meta.achievements[val] != nil
        default: return true
        }
    }

    static let factions: [Faction] = [
        Faction(id: "military", name: "残军", desc: "退守检查站的旧军队，讲规矩，也讲代价。", icon: "shield.lefthalf.filled"),
        Faction(id: "vulture", name: "秃鹫帮", desc: "把活人当货物的人。和他们做生意要握紧刀柄。", icon: "bird.fill"),
        Faction(id: "order", name: "灰袍教团", desc: "相信灰烬之后有新生，救济穷人，也收割死者。", icon: "flame.fill"),
        Faction(id: "whitecrow", name: "白鸦", desc: "实验室里最后一批科学家，寻找疫苗，也寻找试验品。", icon: "cross.case.fill")
    ]
}
