import SwiftUI

struct ItemStack: Identifiable {
    let id: String
    let item: Item
    let count: Int
}

// MARK: - 面板骨架

struct Tabs: View {
    let titles: [String]
    @Binding var selection: Int
    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 6) {
                ForEach(titles.indices, id: \.self) { idx in
                    Button {
                        withAnimation(.easeOut(duration: 0.18)) { selection = idx }
                    } label: {
                        Text(titles[idx])
                            .font(Theme.mono(10, .medium))
                            .kerning(0.6)
                            .foregroundColor(selection == idx ? Theme.bgDeep : Theme.dim)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 7)
                            .background(
                                Capsule().fill(selection == idx ? Theme.ember : Theme.surfaceHi)
                            )
                    }
                    .buttonStyle(PlainButtonStyle())
                }
            }
        }
    }
}

struct PanelShell<Content: View>: View {
    @EnvironmentObject var store: GameStore
    let title: String
    let subtitle: String?
    let content: Content

    init(_ title: String, subtitle: String? = nil, @ViewBuilder content: () -> Content) {
        self.title = title
        self.subtitle = subtitle
        self.content = content()
    }

    var body: some View {
        ZStack {
            Theme.bg.ignoresSafeArea()
            VStack(spacing: 0) {
                PanelHeader(title: title, subtitle: subtitle) {
                    store.panel = nil
                }
                .padding(.horizontal, 16)
                .padding(.top, 14)
                .padding(.bottom, 12)

                DividerLine()

                ScrollView(showsIndicators: false) {
                    content
                        .padding(16)
                }
            }
        }
        .preferredColorScheme(.dark)
    }
}

struct CostLine: View {
    let cost: [String: Int]
    let inventory: [String: Int]

    private var enough: Bool {
        cost.allSatisfy { inventory[$0.key, default: 0] >= $0.value }
    }

    var body: some View {
        Text(cost.map { "\(ContentStore.shared.itemName($0.key))×\($0.value)" }.joined(separator: "  ·  "))
            .font(Theme.mono(9))
            .foregroundColor(enough ? Theme.faint : Theme.blood)
            .lineLimit(2)
            .minimumScaleFactor(0.8)
    }
}

// MARK: - 面板路由

struct PanelHost: View {
    @EnvironmentObject var store: GameStore
    let panel: Panel

    @ViewBuilder
    var body: some View {
        switch panel {
        case .inventory: InventoryPanel()
        case .craft: CraftPanel()
        case .base: BasePanel()
        case .map: MapPanel()
        case .squad: SquadPanel()
        case .quests: QuestPanel()
        case .codex: CodexPanel()
        case .character: CharacterPanel()
        case .journal: JournalPanel()
        case .achievements: AchievementPanel()
        case .scenarios: ScenarioPanel()
        }
    }
}

// MARK: - 背包

struct InventoryPanel: View {
    @EnvironmentObject var store: GameStore
    @State private var tab = 0

    private var consumables: [ItemStack] {
        store.state.inventory
            .compactMap { id, n -> ItemStack? in
                guard let it = store.content.item(id) else { return nil }
                return ItemStack(id: it.id, item: it, count: n)
            }
            .sorted { ($0.item.cat, $0.item.tier) < ($1.item.cat, $1.item.tier) }
    }

    private var filtered: [ItemStack] {
        switch tab {
        case 1: return consumables.filter { $0.item.isUsable }
        case 2: return consumables.filter { $0.item.cat == "material" }
        case 3: return consumables.filter { $0.item.cat == "quest" || $0.item.cat == "valuable" }
        default: return consumables
        }
    }

    var body: some View {
        PanelShell("背包", subtitle: "负重 \(Int(store.currentWeight)) / \(store.carryCapacity)") {
            VStack(alignment: .leading, spacing: 14) {
                gearSection
                weaponsSection
                armorSection
                inventorySection
            }
        }
    }

    private var gearSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionLabel(text: "已装备")
            if let w = store.weapon, let g = store.weaponGear {
                GearRow(title: w.name, subtitle: "\(w.kindName) · 伤害 \(w.dmg)-\(w.dmg + w.dmgVar) · 耐久 \(max(0, g.dur))",
                        icon: w.icon, stat: "\(w.crit)% 暴击", tint: Theme.ember)
            }
            ForEach(["head", "body", "hands", "back"], id: \.self) { slot in
                if let a = store.armor(slot), let g = store.armorGear(slot) {
                    HStack {
                        GearRow(title: a.name, subtitle: "\(a.slotName) · 护甲 \(a.armor) · 保暖 \(a.warmth)",
                                icon: a.icon, stat: "+\(a.evade)% 闪避", tint: Theme.steel)
                        Button {
                            store.unequipArmor(slot)
                        } label: {
                            Text("卸下")
                                .font(Theme.mono(9))
                                .foregroundColor(Theme.faint)
                        }
                        .buttonStyle(PlainButtonStyle())
                        .opacity(g.dur > 0 ? 1 : 0.5)
                    }
                }
            }
        }
        .cardStyle(padding: 14)
    }

    private var weaponsSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            SectionLabel(text: "武器库", trail: "\(store.state.weapons.count) 件")
            if store.state.weapons.isEmpty {
                EmptyState(icon: "hand.raised", title: "没有武器", note: "你只能靠拳头了")
            }
            ForEach(store.state.weapons) { g in
                if let w = store.content.weapon(g.item) {
                    HStack(spacing: 10) {
                        GearRow(title: w.name, subtitle: "\(w.kindName) · 伤害 \(w.dmg)-\(w.dmg + w.dmgVar) · 耐久 \(max(0, g.dur))/\(w.dur)",
                                icon: w.icon, stat: w.traits.joined(separator: " "), tint: g.id == store.state.equippedWeapon ? Theme.ember : Theme.dim)
                        Button {
                            store.equipWeapon(g.id)
                        } label: {
                            Text(g.id == store.state.equippedWeapon ? "使用中" : "装备")
                                .font(Theme.mono(9, .medium))
                                .foregroundColor(g.id == store.state.equippedWeapon ? Theme.faint : Theme.ember)
                        }
                        .buttonStyle(PlainButtonStyle())
                        .disabled(g.id == store.state.equippedWeapon)
                    }
                    .contextMenu {
                        Button("拆解为零件", role: .destructive) { store.scrapWeapon(g.id) }
                    }
                }
            }
        }
        .cardStyle(padding: 14)
    }

    private var armorSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            SectionLabel(text: "护甲库", trail: "\(store.state.armors.count) 件")
            if store.state.armors.isEmpty {
                EmptyState(icon: "shield", title: "没有护甲", note: "一件旧夹克也比皮肤强")
            }
            ForEach(store.state.armors) { g in
                if let a = store.content.armor(g.item) {
                    HStack(spacing: 10) {
                        GearRow(title: a.name, subtitle: "\(a.slotName) · 护甲 \(a.armor) · 闪避 +\(a.evade)%",
                                icon: a.icon, stat: a.traits.joined(separator: " "), tint: Theme.steel)
                        Button {
                            store.equipArmor(g.id)
                        } label: {
                            Text(store.state.equippedArmor[a.slot] == g.id ? "使用中" : "穿上")
                                .font(Theme.mono(9, .medium))
                                .foregroundColor(store.state.equippedArmor[a.slot] == g.id ? Theme.faint : Theme.ember)
                        }
                        .buttonStyle(PlainButtonStyle())
                        .disabled(store.state.equippedArmor[a.slot] == g.id)
                    }
                }
            }
        }
        .cardStyle(padding: 14)
    }

    private var inventorySection: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionLabel(text: "物品", trail: "\(filtered.count) 种")
            Tabs(titles: ["全部", "可用", "材料", "关键"], selection: $tab)
            if filtered.isEmpty {
                EmptyState(icon: "tray", title: "空的", note: "出去搜刮一圈")
            }
            ForEach(filtered) { pair in
                HStack(spacing: 8) {
                    ItemRow(item: pair.item, count: pair.count)
                    if pair.item.isUsable && pair.item.cat != "throwable" {
                        Button {
                            store.useItem(pair.item.id)
                        } label: {
                            Text("使用")
                                .font(Theme.mono(9, .semibold))
                                .foregroundColor(Theme.ember)
                                .padding(.horizontal, 9)
                                .padding(.vertical, 6)
                                .background(Capsule().fill(Theme.ember.opacity(0.13)))
                        }
                        .buttonStyle(PlainButtonStyle())
                    }
                }
                .contextMenu {
                    Button("丢弃 1 个", role: .destructive) { store.dropItem(pair.item.id) }
                }
                DividerLine()
            }
        }
        .cardStyle(padding: 14)
    }
}

// MARK: - 制作

struct CraftPanel: View {
    @EnvironmentObject var store: GameStore
    @State private var tab = 0

    private var stations: [String] {
        Array(Set(store.content.recipes.map { $0.station })).sorted()
    }

    private var list: [Recipe] {
        if tab == 0 { return store.content.recipes.sorted { $0.stationLevel < $1.stationLevel } }
        let station = stations[tab - 1]
        return store.content.recipes.filter { $0.station == station }.sorted { $0.stationLevel < $1.stationLevel }
    }

    var body: some View {
        PanelShell("制作", subtitle: "工作台等级决定你能做什么") {
            VStack(alignment: .leading, spacing: 14) {
                Tabs(titles: ["全部"] + stations, selection: $tab)
                ForEach(list) { r in
                    recipeRow(r)
                    DividerLine()
                }
            }
        }
    }

    private func recipeRow(_ r: Recipe) -> some View {
        VStack(alignment: .leading, spacing: 7) {
            HStack(alignment: .firstTextBaseline) {
                VStack(alignment: .leading, spacing: 2) {
                    Text(r.name)
                        .font(Theme.sans(14, .semibold))
                        .foregroundColor(Theme.text)
                    Text(r.desc)
                        .font(Theme.mono(9))
                        .foregroundColor(Theme.faint)
                        .lineLimit(2)
                }
                Spacer()
                Text("\(r.station) Lv.\(r.stationLevel)")
                    .font(Theme.mono(8))
                    .foregroundColor(store.stationLevel(r.station) >= r.stationLevel ? Theme.toxic : Theme.blood)
            }
            CostLine(cost: r.cost, inventory: store.state.inventory)
            HStack(spacing: 8) {
                Text("耗时 \(r.ap) AP")
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.faint)
                Spacer()
                Button {
                    store.craft(r)
                } label: {
                    Text(store.canCraft(r) ? "制作" : "缺材料")
                        .font(Theme.mono(9, .semibold))
                        .foregroundColor(store.canCraft(r) ? Theme.bgDeep : Theme.faint)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(Capsule().fill(store.canCraft(r) ? Theme.ember : Theme.surfaceHi))
                }
                .buttonStyle(PlainButtonStyle())
                .disabled(!store.canCraft(r))
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - 据点

struct BasePanel: View {
    @EnvironmentObject var store: GameStore

    var body: some View {
        PanelShell("据点", subtitle: "灯塔营地 · 升级设施改变生存曲线") {
            VStack(alignment: .leading, spacing: 14) {
                factionBlock
                SectionLabel(text: "设施", trail: "材料来自搜刮与拆解")
                ForEach(store.content.buildings) { b in
                    buildingRow(b)
                    DividerLine()
                }
            }
        }
    }

    private var factionBlock: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionLabel(text: "势力关系")
            ForEach(ContentStore.factions) { f in
                HStack(spacing: 10) {
                    Image(systemName: f.icon)
                        .font(.system(size: 12))
                        .foregroundColor(Theme.dim)
                        .frame(width: 18)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(f.name)
                            .font(Theme.sans(12, .medium))
                            .foregroundColor(Theme.text)
                        Text(f.desc)
                            .font(Theme.mono(8))
                            .foregroundColor(Theme.faint)
                            .lineLimit(1)
                    }
                    Spacer()
                    let v = store.state.faction[f.id] ?? 0
                    Text(v >= 0 ? "+\(v)" : "\(v)")
                        .font(Theme.mono(11, .semibold))
                        .foregroundColor(v >= 0 ? Theme.toxic : Theme.blood)
                }
            }
        }
        .cardStyle(padding: 14)
    }

    private func buildingRow(_ b: Building) -> some View {
        let level = store.buildingLevel(b.id)
        let maxed = level >= b.maxLevel
        let cost = b.cost(level: level + 1)
        let can = cost.allSatisfy { store.state.inventory[$0.key, default: 0] >= $0.value }
        return VStack(alignment: .leading, spacing: 8) {
            HStack(spacing: 10) {
                Image(systemName: b.icon)
                    .font(.system(size: 14))
                    .foregroundColor(level > 0 ? Theme.ember : Theme.faint)
                    .frame(width: 22)
                VStack(alignment: .leading, spacing: 2) {
                    Text(b.name)
                        .font(Theme.sans(14, .semibold))
                        .foregroundColor(Theme.text)
                    Text(b.desc)
                        .font(Theme.mono(9))
                        .foregroundColor(Theme.faint)
                        .lineLimit(2)
                }
                Spacer()
                Text("Lv.\(level)/\(b.maxLevel)")
                    .font(Theme.mono(10, .semibold))
                    .foregroundColor(level > 0 ? Theme.ember : Theme.faint)
            }
            HStack(spacing: 5) {
                ForEach(0..<b.maxLevel, id: \.self) { i in
                    Capsule()
                        .fill(i < level ? Theme.ember : Theme.text.opacity(0.09))
                        .frame(height: 4)
                }
            }
            if !maxed {
                HStack(alignment: .center) {
                    CostLine(cost: cost, inventory: store.state.inventory)
                    Spacer()
                    Button {
                        store.upgrade(b)
                    } label: {
                        Text("升级")
                            .font(Theme.mono(9, .semibold))
                            .foregroundColor(can ? Theme.bgDeep : Theme.faint)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 6)
                            .background(Capsule().fill(can ? Theme.ember : Theme.surfaceHi))
                    }
                    .buttonStyle(PlainButtonStyle())
                    .disabled(!can)
                }
            } else {
                Text("已达到最高等级")
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.toxic)
            }
        }
        .padding(.vertical, 5)
    }
}

// MARK: - 地图

struct MapPanel: View {
    @EnvironmentObject var store: GameStore

    var body: some View {
        PanelShell("地图", subtitle: "跨区域移动消耗 2 AP，同区 1 AP") {
            VStack(alignment: .leading, spacing: 18) {
                ForEach(ContentStore.regionOrder, id: \.self) { region in
                    let places = store.content.places(in: region)
                    if !places.isEmpty {
                        VStack(alignment: .leading, spacing: 8) {
                            SectionLabel(text: region, trail: "危险 \(places.map { $0.danger }.max() ?? 1)")
                            ForEach(places) { p in
                                placeRow(p)
                            }
                        }
                    }
                }
            }
        }
    }

    private func placeRow(_ p: Place) -> some View {
        let current = store.state.place == p.id
        let unlocked = isUnlocked(p)
        let cross = p.region != store.state.region
        return Button {
            if unlocked && !current {
                store.panel = nil
                store.travel(to: p.id)
            }
        } label: {
            HStack(spacing: 12) {
                ZStack {
                    RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .fill(current ? Theme.ember.opacity(0.14) : Theme.surfaceHi)
                        .frame(width: 40, height: 40)
                    Image(systemName: p.tags.contains("medical") ? "cross.case" :
                            p.tags.contains("military") ? "shield" :
                            p.tags.contains("rural") ? "leaf" :
                            p.tags.contains("industrial") ? "gearshape.2" :
                            p.tags.contains("water") ? "drop" : "building.2")
                        .font(.system(size: 14))
                        .foregroundColor(current ? Theme.ember : Theme.dim)
                }
                VStack(alignment: .leading, spacing: 3) {
                    HStack(spacing: 6) {
                        Text(p.name)
                            .font(Theme.sans(14, .medium))
                            .foregroundColor(Theme.text)
                        if current { Chip(text: "当前", tint: Theme.ember, filled: true) }
                        if !unlocked { Chip(text: "未探索", tint: Theme.faint) }
                    }
                    Text(p.desc)
                        .font(Theme.mono(9))
                        .foregroundColor(Theme.faint)
                        .lineLimit(1)
                }
                Spacer(minLength: 4)
                VStack(alignment: .trailing, spacing: 5) {
                    DangerMark(level: p.danger)
                    Text(cross ? "2 AP" : "1 AP")
                        .font(Theme.mono(8))
                        .foregroundColor(unlocked ? Theme.dim : Theme.faint)
                }
            }
            .padding(10)
            .background(
                RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .fill(current ? Theme.surfaceHi : Theme.surface)
                    .overlay(RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                        .strokeBorder(current ? Theme.ember.opacity(0.3) : Theme.text.opacity(0.05), lineWidth: 1))
            )
            .opacity(unlocked ? 1 : 0.5)
        }
        .buttonStyle(PlainButtonStyle())
        .disabled(!unlocked || current)
    }

    private func isUnlocked(_ p: Place) -> Bool {
        if store.state.visited.contains(p.id) { return true }
        guard let tag = p.tags.first(where: { $0.hasPrefix("unlock:") }) else { return true }
        return store.state.visited.contains(String(tag.dropFirst(7)))
    }
}
