import Foundation

// MARK: - 基础内容模型

struct LootEntry: Codable, Hashable {
    var item: String
    var chance: Int
    var min: Int
    var max: Int
}

struct Item: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var cat: String
    var tier: Int
    var weight: Double
    var value: Int
    var stack: Int
    var desc: String
    var effect: [String: Int]
    var tags: [String]
    var icon: String

    var isUsable: Bool { !effect.isEmpty }
    var categoryName: String {
        switch cat {
        case "food": return "食物"
        case "drink": return "饮水"
        case "med": return "医疗"
        case "ammo": return "弹药"
        case "material": return "材料"
        case "tool": return "工具"
        case "valuable": return "贵重"
        case "quest": return "关键"
        case "throwable": return "投掷"
        default: return "杂物"
        }
    }
}

struct Weapon: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var kind: String
    var desc: String
    var dmg: Int
    var dmgVar: Int
    var crit: Int
    var acc: Int
    var apCost: Int
    var dur: Int
    var value: Int
    var rarity: Int
    var weight: Double
    var ammo: String?
    var traits: [String]
    var icon: String

    var kindName: String {
        switch kind {
        case "blunt": return "钝器"
        case "blade": return "利器"
        case "pole": return "长柄"
        case "axe": return "斧类"
        case "gun": return "枪械"
        case "bow": return "弓弩"
        case "exotic": return "特殊"
        default: return "徒手"
        }
    }
    var ammoName: String? {
        guard let a = ammo else { return nil }
        return ContentStore.shared.items[a]?.name ?? a
    }
}

struct Armor: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var slot: String
    var desc: String
    var armor: Int
    var evade: Int
    var warmth: Int
    var value: Int
    var rarity: Int
    var weight: Double
    var traits: [String]
    var icon: String

    var slotName: String {
        switch slot {
        case "head": return "头部"
        case "body": return "躯干"
        case "hands": return "手部"
        case "back": return "背负"
        default: return "配件"
        }
    }
}

struct EnemyAbility: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var desc: String
    var dmg: Int
    var kind: String
}

struct Enemy: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var tag: String
    var tier: Int
    var desc: String
    var hp: Int
    var dmg: Int
    var armor: Int
    var acc: Int
    var evade: Int
    var xp: Int
    var night: Bool
    var abilities: [String]
    var loot: [LootEntry]
    var icon: String

    var tagName: String {
        switch tag {
        case "walker": return "行尸"
        case "runner": return "奔行"
        case "brute": return "重装"
        case "spitter": return "喷吐"
        case "screamer": return "尖啸"
        case "crawler": return "爬行"
        case "hound": return "感染兽"
        case "human": return "人类"
        case "boss": return "首领"
        default: return "异变"
        }
    }
}

struct Place: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var region: String
    var desc: String
    var danger: Int
    var stages: Int
    var x: Double
    var y: Double
    var tags: [String]
    var loot: [LootEntry]
    var enemies: [String]
    var events: [String]
}

struct EventChoice: Codable, Hashable {
    var text: String
    var req: [String]
    var effect: [String: Int]
    var items: [String: Int]
    var fight: String?
    var next: String?
    var chance: Int
    var effectFail: [String: Int]
    var log: String
    var logFail: String
    var ending: String?
}

struct EventCard: Codable, Identifiable, Hashable {
    var id: String
    var title: String
    var text: String
    var tag: String
    var weight: Int
    var once: Bool
    var minDay: Int
    var places: [String]
    var choices: [EventChoice]
}

struct Recipe: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var desc: String
    var station: String
    var stationLevel: Int
    var ap: Int
    var cost: [String: Int]
    var out: [String: Int]
    var outWeapon: String?
    var outArmor: String?
}

struct Perk: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var branch: String
    var tier: Int
    var maxRank: Int
    var desc: String
    var effect: [String: Int]

    var branchName: String {
        switch branch {
        case "combat": return "战斗"
        case "survival": return "生存"
        case "tech": return "技术"
        default: return "意志"
        }
    }
    var branchIcon: String {
        switch branch {
        case "combat": return "bolt.fill"
        case "survival": return "leaf.fill"
        case "tech": return "wrench.and.screwdriver.fill"
        default: return "brain.head.profile"
        }
    }
}

struct Building: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var desc: String
    var maxLevel: Int
    var baseCost: [String: Int]
    var scale: Double
    var effectKey: String
    var perLevel: Int
    var icon: String

    func cost(level: Int) -> [String: Int] {
        var out: [String: Int] = [:]
        for (k, v) in baseCost {
            out[k] = Int(Double(v) * pow(scale, Double(level - 1)))
        }
        return out
    }
}

struct Achievement: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var desc: String
    var hidden: Bool
    var key: String
    var goal: Int
}

struct Ending: Codable, Identifiable, Hashable {
    var id: String
    var title: String
    var kind: String
    var text: String
    var cond: String

    var kindName: String {
        switch kind {
        case "win": return "生还"
        case "death": return "终结"
        default: return "余波"
        }
    }
}

struct NPC: Codable, Identifiable, Hashable {
    var id: String
    var name: String
    var role: String
    var desc: String
    var traits: [String]
    var perkID: String
    var trust: Int
    var joinReq: String
    var questID: String?
    var icon: String
}

struct QuestDef: Codable, Identifiable, Hashable {
    var id: String
    var title: String
    var giver: String
    var desc: String
    var kind: String
    var target: String
    var count: Int
    var rewardXP: Int
    var rewardItems: [String: Int]
    var next: String?
}

struct JournalEntry: Codable, Identifiable, Hashable {
    var id: String
    var text: String
    var src: String
}

// MARK: - 运行时状态

struct SeededRNG: Codable, Hashable {
    var state: UInt64

    init(seed: UInt64) {
        state = seed == 0 ? 0x9E3779B97F4A7C15 : seed
    }

    mutating func next() -> UInt64 {
        state = state &+ 0x9E3779B97F4A7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58476D1CE4E5B9
        z = (z ^ (z >> 27)) &* 0x94D049BB133111EB
        return z ^ (z >> 31)
    }

    mutating func int(_ range: ClosedRange<Int>) -> Int {
        guard range.upperBound >= range.lowerBound else { return range.lowerBound }
        let span = UInt64(range.upperBound - range.lowerBound + 1)
        return range.lowerBound + Int(next() % span)
    }

    mutating func chance(_ percent: Int) -> Bool {
        guard percent > 0 else { return false }
        if percent >= 100 { return true }
        return int(0...99) < percent
    }

    mutating func pick<T>(_ items: [T]) -> T? {
        guard !items.isEmpty else { return nil }
        return items[int(0...(items.count - 1))]
    }

    mutating func shuffled<T>(_ items: [T]) -> [T] {
        var arr = items
        guard arr.count > 1 else { return arr }
        for i in stride(from: arr.count - 1, to: 0, by: -1) {
            let j = int(0...i)
            arr.swapAt(i, j)
        }
        return arr
    }

    mutating func double() -> Double {
        Double(next() % 100_000) / 100_000.0
    }
}

struct GearInstance: Codable, Hashable, Identifiable {
    var id: String
    var item: String
    var dur: Int
}

struct LogLine: Codable, Hashable, Identifiable {
    var id: String = UUID().uuidString
    var day: Int
    var text: String
    var kind: String
}

struct QuestState: Codable, Hashable, Identifiable {
    var id: String
    var progress: Int
    var done: Bool
}

struct CompanionState: Codable, Hashable, Identifiable {
    var id: String
    var trust: Int
    var task: String   // idle / scavenge / guard / cook / craft
    var alive: Bool
}

struct BattleState: Codable, Hashable {
    var enemy: String
    var hp: Int
    var maxHP: Int
    var round: Int
    var log: [String]
    var cd: [String: Int]
    var aim: Int
    var dodge: Int
    var escaped: Bool
    var ended: Bool
    var victory: Bool
    var loot: [String: Int]
    var eventID: String?
    var enemyMaxHP: Int
}

struct GameState: Codable {
    var ver: Int = 1
    var seed: UInt64
    var rng: SeededRNG
    var scenario: String
    var day: Int = 1
    var ap: Int = 3
    var apMax: Int = 3
    var hp: Int = 100
    var hpMax: Int = 100
    var hunger: Int = 80
    var thirst: Int = 80
    var infection: Int = 0
    var sanity: Int = 75
    var fatigue: Int = 5
    var warmth: Int = 70
    var place: String = "safehouse"
    var region: String = "旧城区"
    var inventory: [String: Int] = [:]
    var weapons: [GearInstance] = []
    var armors: [GearInstance] = []
    var equippedWeapon: String?
    var equippedArmor: [String: String] = [:]
    var perks: [String: Int] = [:]
    var xp: Int = 0
    var level: Int = 1
    var perkPoints: Int = 1
    var faction: [String: Int] = ["military": 0, "vulture": 0, "order": 0, "whitecrow": 0]
    var buildings: [String: Int] = [:]
    var visited: [String] = []
    var stage: [String: Int] = [:]
    var log: [LogLine] = []
    var seenEvents: [String] = []
    var stats: [String: Int] = [:]
    var activeQuests: [QuestState] = []
    var doneQuests: [String] = []
    var companions: [CompanionState] = []
    var battle: BattleState?
    var ending: String?
    var flags: [String: Int] = [:]
}

struct MetaState: Codable {
    var runs: Int = 0
    var bestDay: Int = 1
    var totalKills: Int = 0
    var shards: Int = 0
    var unlocked: [String] = ["survivor"]
    var achievements: [String: Int] = [:]
    var endings: [String] = []
}

struct Scenario: Identifiable, Hashable {
    var id: String
    var name: String
    var tagline: String
    var desc: String
    var unlock: String?
    var perks: [String: Int]
    var items: [String: Int]
    var weapon: String?
    var armor: [String]
    var hpBonus: Int
    var apBonus: Int
}
