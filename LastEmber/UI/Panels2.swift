import SwiftUI

// MARK: - 同伴

struct SquadPanel: View {
    @EnvironmentObject var store: GameStore

    private var recruitable: [NPC] {
        store.content.npcList.filter { npc in
            store.state.flags["met_\(npc.id)", default: 0] == 1 &&
            !store.state.companions.contains(where: { $0.id == npc.id })
        }
    }

    var body: some View {
        PanelShell("同伴", subtitle: "最多 4 人 · 每晚执行任务") {
            VStack(alignment: .leading, spacing: 14) {
                SectionLabel(text: "营地成员", trail: "\(store.state.companions.count)/4")
                if store.state.companions.isEmpty {
                    EmptyState(icon: "person.2", title: "还没有同伴", note: "事件与任务中会遇见幸存者")
                }
                ForEach(store.state.companions) { c in
                    if let npc = store.content.npc(c.id) {
                        companionRow(npc, c)
                    }
                }

                SectionLabel(text: "可招募", trail: "\(recruitable.count) 人")
                if recruitable.isEmpty {
                    EmptyState(icon: "binoculars", title: "没有新的面孔", note: "继续探索，遇到更多人")
                }
                ForEach(recruitable) { npc in
                    npcRow(npc)
                }
            }
        }
    }

    private func companionRow(_ npc: NPC, _ c: CompanionState) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(spacing: 12) {
                ZStack {
                    Circle().fill(Theme.surfaceHi).frame(width: 44, height: 44)
                    Image(systemName: npc.icon)
                        .font(.system(size: 16))
                        .foregroundColor(Theme.ember)
                }
                VStack(alignment: .leading, spacing: 3) {
                    Text(npc.name)
                        .font(Theme.sans(14, .semibold))
                        .foregroundColor(Theme.text)
                    Text(npc.role)
                        .font(Theme.mono(9))
                        .foregroundColor(Theme.faint)
                    Text(npc.traits.joined(separator: " · "))
                        .font(Theme.mono(8))
                        .foregroundColor(Theme.dim)
                }
                Spacer()
                VStack(alignment: .trailing, spacing: 4) {
                    Menu {
                        Button("待命") { store.assign(c.id, task: "idle") }
                        Button("外出搜刮") { store.assign(c.id, task: "scavenge") }
                        Button("守夜") { store.assign(c.id, task: "guard") }
                        Button("做饭") { store.assign(c.id, task: "cook") }
                        Button("制作零件") { store.assign(c.id, task: "craft") }
                    } label: {
                        Text(taskName(c.task))
                            .font(Theme.mono(9, .semibold))
                            .foregroundColor(Theme.bgDeep)
                            .padding(.horizontal, 10)
                            .padding(.vertical, 6)
                            .background(Capsule().fill(Theme.ember))
                    }
                    Text("信任 \(c.trust)")
                        .font(Theme.mono(8))
                        .foregroundColor(Theme.faint)
                }
            }
            Text(npc.desc)
                .font(Theme.serif(11))
                .foregroundColor(Theme.dim)
                .lineSpacing(3)
        }
        .cardStyle(padding: 12)
    }

    private func npcRow(_ npc: NPC) -> some View {
        HStack(spacing: 12) {
            Image(systemName: npc.icon)
                .font(.system(size: 15))
                .foregroundColor(Theme.dim)
                .frame(width: 30)
            VStack(alignment: .leading, spacing: 3) {
                Text(npc.name)
                    .font(Theme.sans(13, .medium))
                    .foregroundColor(Theme.text)
                Text("\(npc.role) · \(npc.joinReq)")
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.faint)
                    .lineLimit(2)
            }
            Spacer()
            Button {
                store.recruit(npc)
            } label: {
                Text("招募")
                    .font(Theme.mono(9, .semibold))
                    .foregroundColor(Theme.ember)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(Capsule().fill(Theme.ember.opacity(0.13)))
            }
            .buttonStyle(PlainButtonStyle())
            .disabled(!store.canRecruit(npc))
            .opacity(store.canRecruit(npc) ? 1 : 0.45)
        }
        .padding(.vertical, 6)
    }

    private func taskName(_ task: String) -> String {
        switch task {
        case "scavenge": return "搜刮"
        case "guard": return "守夜"
        case "cook": return "做饭"
        case "craft": return "制作"
        default: return "待命"
        }
    }
}

// MARK: - 任务

struct QuestPanel: View {
    @EnvironmentObject var store: GameStore

    var body: some View {
        PanelShell("任务", subtitle: "主线通往灯塔，支线换来资源") {
            VStack(alignment: .leading, spacing: 16) {
                SectionLabel(text: "进行中", trail: "\(store.state.activeQuests.count)")
                if store.state.activeQuests.isEmpty {
                    EmptyState(icon: "list.bullet", title: "没有进行中的任务", note: "从下方接一个，或继续搜刮")
                }
                ForEach(store.state.activeQuests) { qs in
                    if let q = store.content.quest(qs.id) {
                        activeRow(q)
                    }
                }

                SectionLabel(text: "可接取", trail: "\(store.availableQuests().count)")
                ForEach(store.availableQuests()) { q in
                    offerRow(q)
                }
            }
        }
    }

    private func activeRow(_ q: QuestDef) -> some View {
        let p = min(store.questProgress(q), q.count)
        return VStack(alignment: .leading, spacing: 7) {
            HStack {
                Text(q.title)
                    .font(Theme.sans(14, .semibold))
                    .foregroundColor(Theme.text)
                Spacer()
                Text("\(p)/\(q.count)")
                    .font(Theme.mono(10, .semibold))
                    .foregroundColor(Theme.ember)
            }
            Text(q.desc)
                .font(Theme.mono(9))
                .foregroundColor(Theme.faint)
                .lineLimit(2)
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule().fill(Theme.text.opacity(0.07))
                    Capsule().fill(Theme.ember)
                        .frame(width: geo.size.width * CGFloat(p) / CGFloat(max(1, q.count)))
                }
            }
            .frame(height: 4)
        }
        .cardStyle(padding: 12)
    }

    private func offerRow(_ q: QuestDef) -> some View {
        HStack(alignment: .top, spacing: 10) {
            VStack(alignment: .leading, spacing: 3) {
                Text(q.title)
                    .font(Theme.sans(13, .medium))
                    .foregroundColor(Theme.text)
                Text("\(q.giver) · \(q.desc)")
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.faint)
                    .lineLimit(2)
                Text("奖励 \(q.rewardXP) XP" + (q.rewardItems.isEmpty ? "" : " · " + q.rewardItems.map { "\(store.content.itemName($0.key))×\($0.value)" }.joined(separator: " ")))
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.dim)
            }
            Spacer()
            Button {
                store.acceptQuest(q.id)
            } label: {
                Text("接取")
                    .font(Theme.mono(9, .semibold))
                    .foregroundColor(Theme.ember)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(Capsule().fill(Theme.ember.opacity(0.13)))
            }
            .buttonStyle(PlainButtonStyle())
        }
        .padding(.vertical, 6)
    }
}

// MARK: - 图鉴

struct CodexPanel: View {
    @EnvironmentObject var store: GameStore
    @State private var tab = 0
    @State private var query = ""

    private let tabs = ["物品", "武器", "护甲", "敌人", "地点", "结局"]

    var body: some View {
        PanelShell("图鉴", subtitle: "\(store.content.itemList.count) 物品 · \(store.content.enemyList.count) 敌人 · \(store.content.placeList.count) 地点") {
            VStack(alignment: .leading, spacing: 14) {
                Tabs(titles: tabs, selection: $tab)
                HStack(spacing: 8) {
                    Image(systemName: "magnifyingglass")
                        .font(.system(size: 11))
                        .foregroundColor(Theme.faint)
                    TextField("搜索", text: $query)
                        .font(Theme.mono(11))
                        .foregroundColor(Theme.text)
                        .textInputAutocapitalization(.never)
                        .autocorrectionDisabled(true)
                }
                .padding(.horizontal, 10)
                .padding(.vertical, 8)
                .background(RoundedRectangle(cornerRadius: 8, style: .continuous).fill(Theme.surfaceHi))

                LazyVStack(alignment: .leading, spacing: 4) {
                    switch tab {
                    case 1: weaponList
                    case 2: armorList
                    case 3: enemyList
                    case 4: placeList
                    case 5: endingList
                    default: itemList
                    }
                }
            }
        }
    }

    private var itemList: some View {
        ForEach(store.content.itemList.filter { query.isEmpty || $0.name.contains(query) }) { it in
            GridRowContent(icon: it.icon, title: it.name,
                           meta: "\(it.categoryName) · T\(it.tier) · \(it.desc)",
                           stat: "×\(store.state.inventory[it.id, default: 0])",
                           tint: Theme.dim)
        }
    }

    private var weaponList: some View {
        ForEach(store.content.weaponList.filter { query.isEmpty || $0.name.contains(query) }) { w in
            GridRowContent(icon: w.icon, title: w.name,
                           meta: "\(w.kindName) · 伤害 \(w.dmg)-\(w.dmg + w.dmgVar) · \(w.desc)",
                           stat: "\(w.crit)% 暴击",
                           tint: Theme.ember)
        }
    }

    private var armorList: some View {
        ForEach(store.content.armorList.filter { query.isEmpty || $0.name.contains(query) }) { a in
            GridRowContent(icon: a.icon, title: a.name,
                           meta: "\(a.slotName) · 护甲 \(a.armor) · \(a.desc)",
                           stat: "闪避 \(a.evade)%",
                           tint: Theme.steel)
        }
    }

    private var enemyList: some View {
        ForEach(store.content.enemyList.filter { query.isEmpty || $0.name.contains(query) }) { e in
            let known = store.state.stats["kill_\(e.id)", default: 0] > 0
            GridRowContent(icon: e.icon, title: known ? e.name : "未记录的威胁",
                           meta: "\(e.tagName) · T\(e.tier) · 生命 \(e.hp) · 伤害 \(e.dmg)",
                           stat: known ? "已记录" : "未遭遇",
                           tint: known ? Theme.blood : Theme.faint)
        }
    }

    private var placeList: some View {
        ForEach(store.content.placeList.filter { query.isEmpty || $0.name.contains(query) }) { p in
            GridRowContent(icon: "building.2", title: p.name,
                           meta: "\(p.region) · \(p.desc)",
                           stat: store.state.visited.contains(p.id) ? "已到访" : "危险 \(p.danger)",
                           tint: store.state.visited.contains(p.id) ? Theme.toxic : Theme.faint)
        }
    }

    private var endingList: some View {
        ForEach(store.content.endings.values.sorted { $0.kind < $1.kind }) { e in
            let got = store.meta.endings.contains(e.id)
            VStack(alignment: .leading, spacing: 5) {
                HStack {
                    Text(got ? e.title : "？？？")
                        .font(Theme.sans(14, .semibold))
                        .foregroundColor(got ? Theme.text : Theme.faint)
                    Spacer()
                    Chip(text: e.kindName, tint: e.kind == "win" ? Theme.toxic : (e.kind == "death" ? Theme.blood : Theme.dim))
                }
                Text(got ? e.text : "条件：\(e.cond)")
                    .font(Theme.serif(11))
                    .foregroundColor(Theme.faint)
                    .lineSpacing(3)
                    .lineLimit(got ? 4 : 1)
            }
            .padding(.vertical, 8)
            .hairline()
        }
    }
}

struct GridRowContent: View {
    let icon: String
    let title: String
    let meta: String
    let stat: String
    var tint: Color = Theme.dim

    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 12))
                .foregroundColor(tint)
                .frame(width: 22)
            VStack(alignment: .leading, spacing: 3) {
                Text(title)
                    .font(Theme.sans(13, .medium))
                    .foregroundColor(Theme.text)
                Text(meta)
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.faint)
                    .lineLimit(2)
            }
            Spacer(minLength: 4)
            Text(stat)
                .font(Theme.mono(8))
                .foregroundColor(tint.opacity(0.9))
        }
        .padding(.vertical, 6)
        .hairline()
    }
}

// MARK: - 角色

struct BranchTab: Identifiable {
    let id: String
    let name: String
}

struct CharacterPanel: View {
    @EnvironmentObject var store: GameStore
    @State private var branch = "combat"

    static let branches = [
        BranchTab(id: "combat", name: "战斗"),
        BranchTab(id: "survival", name: "生存"),
        BranchTab(id: "tech", name: "技术"),
        BranchTab(id: "will", name: "意志")
    ]

    private var need: Int { GameStore.xpNeed(store.state.level) }

    var body: some View {
        PanelShell("角色", subtitle: "Lv.\(store.state.level) · \(store.state.perkPoints) 点可分配") {
            VStack(alignment: .leading, spacing: 16) {
                levelCard
                statGrid
                perkSection
                factionSection
            }
        }
    }

    private var levelCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .firstTextBaseline) {
                Text(store.state.scenarioName)
                    .font(Theme.display(20))
                    .foregroundColor(Theme.bone)
                Spacer()
                Text("\(store.state.xp)/\(need) XP")
                    .font(Theme.mono(9))
                    .foregroundColor(Theme.ember)
            }
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule().fill(Theme.text.opacity(0.08))
                    Capsule().fill(Theme.emberGradient)
                        .frame(width: geo.size.width * min(1, CGFloat(store.state.xp) / CGFloat(max(1, need))))
                }
            }
            .frame(height: 5)
            HStack(spacing: 6) {
                Chip(text: "属性点 \(store.state.perkPoints)", tint: Theme.ember)
                Chip(text: "击杀 \(store.state.stats["kills", default: 0])", tint: Theme.blood)
                Chip(text: "最远 \(store.meta.bestDay) 天", tint: Theme.dim)
            }
        }
        .cardStyle(padding: 14)
    }

    private var statGrid: some View {
        let cols = [GridItem(.flexible(), spacing: 10), GridItem(.flexible(), spacing: 10)]
        return LazyVGrid(columns: cols, spacing: 10) {
            statCell("近战伤害", "+\(store.perkValue("dmg"))")
            statCell("暴击", "+\(store.perkValue("crit"))%")
            statCell("搜刮", "+\(store.perkValue("scavenge"))%")
            statCell("治疗", "+\(store.perkValue("heal"))")
            statCell("抗感染", "+\(store.perkValue("infectResist"))%")
            statCell("负重", "\(store.carryCapacity)")
            statCell("护甲", "\(store.armorValue)")
            statCell("闪避", "\(store.evadeValue)%")
        }
    }

    private func statCell(_ label: String, _ value: String) -> some View {
        HStack {
            Text(label)
                .font(Theme.mono(9))
                .foregroundColor(Theme.faint)
            Spacer()
            Text(value)
                .font(Theme.mono(11, .semibold))
                .foregroundColor(Theme.text)
        }
        .padding(10)
        .background(RoundedRectangle(cornerRadius: 8, style: .continuous).fill(Theme.surface))
    }

    private var perkSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            SectionLabel(text: "技能", trail: "前置需先点出")
            HStack(spacing: 6) {
                ForEach(CharacterPanel.branches) { item in
                    Button {
                        withAnimation(.easeOut(duration: 0.18)) { branch = item.id }
                    } label: {
                        Text(item.name)
                            .font(Theme.mono(10, .medium))
                            .foregroundColor(branch == item.id ? Theme.bgDeep : Theme.dim)
                            .padding(.horizontal, 12)
                            .padding(.vertical, 7)
                            .background(Capsule().fill(branch == item.id ? Theme.ember : Theme.surfaceHi))
                    }
                    .buttonStyle(PlainButtonStyle())
                }
            }
            ForEach(store.content.perkList.filter { $0.branch == branch }) { p in
                perkRow(p)
            }
        }
        .cardStyle(padding: 14)
    }

    private func perkRow(_ p: Perk) -> some View {
        let rank = store.perkRank(p.id)
        let can = store.canLearn(p)
        return HStack(alignment: .top, spacing: 10) {
            Image(systemName: p.branchIcon)
                .font(.system(size: 11))
                .foregroundColor(rank > 0 ? Theme.ember : Theme.faint)
                .frame(width: 20)
            VStack(alignment: .leading, spacing: 3) {
                HStack(spacing: 6) {
                    Text(p.name)
                        .font(Theme.sans(13, .semibold))
                        .foregroundColor(rank > 0 ? Theme.text : Theme.dim)
                    Text("T\(p.tier)")
                        .font(Theme.mono(7))
                        .foregroundColor(Theme.faint)
                    Text("\(rank)/\(p.maxRank)")
                        .font(Theme.mono(8, .medium))
                        .foregroundColor(rank > 0 ? Theme.ember : Theme.faint)
                }
                Text(p.desc)
                    .font(Theme.mono(9))
                    .foregroundColor(Theme.faint)
                    .lineLimit(2)
            }
            Spacer(minLength: 4)
            Button {
                store.learn(p)
            } label: {
                Text(can ? "学习" : (rank >= p.maxRank ? "满级" : "锁定"))
                    .font(Theme.mono(9, .medium))
                    .foregroundColor(can ? Theme.ember : Theme.faint)
                    .padding(.horizontal, 9)
                    .padding(.vertical, 5)
                    .background(Capsule().fill(Theme.surfaceHi))
            }
            .buttonStyle(PlainButtonStyle())
            .disabled(!can)
            .opacity(can ? 1 : 0.5)
        }
        .padding(.vertical, 7)
        .hairline()
    }

    private var factionSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            SectionLabel(text: "势力")
            ForEach(ContentStore.factions) { f in
                HStack {
                    Text(f.name)
                        .font(Theme.sans(12, .medium))
                        .foregroundColor(Theme.dim)
                    Spacer()
                    let v = store.state.faction[f.id] ?? 0
                    Text(v >= 0 ? "+\(v)" : "\(v)")
                        .font(Theme.mono(10, .semibold))
                        .foregroundColor(v >= 0 ? Theme.toxic : Theme.blood)
                }
                .padding(.vertical, 3)
            }
        }
        .cardStyle(padding: 14)
    }
}

// MARK: - 日志 / 档案

struct JournalPanel: View {
    @EnvironmentObject var store: GameStore

    var body: some View {
        PanelShell("档案", subtitle: "第 \(store.state.day) 天 · 记录 \(store.state.log.count) 条") {
            VStack(alignment: .leading, spacing: 14) {
                SectionLabel(text: "日志")
                ForEach(Array(store.state.log.reversed())) { line in
                    LogLineView(line: line)
                }

                SectionLabel(text: "拾到的纸片", trail: "\(store.content.journal.count) 段")
                ForEach(store.content.journal) { j in
                    VStack(alignment: .leading, spacing: 4) {
                        Text("「\(j.text)」")
                            .font(Theme.serif(12))
                            .foregroundColor(Theme.text.opacity(0.85))
                            .lineSpacing(4)
                        Text("—— \(j.src)")
                            .font(Theme.mono(8))
                            .foregroundColor(Theme.faint)
                    }
                    .padding(.vertical, 8)
                    .hairline()
                }
            }
        }
    }
}

// MARK: - 成就

struct AchievementPanel: View {
    @EnvironmentObject var store: GameStore

    private var unlocked: Int { store.meta.achievements.count }

    var body: some View {
        PanelShell("成就", subtitle: "\(unlocked)/\(store.content.achievements.count) 已解锁") {
            VStack(alignment: .leading, spacing: 6) {
                ForEach(store.content.achievements) { a in
                    let got = store.meta.achievements[a.id] != nil
                    let value = min(store.statValue(a.key), a.goal)
                    HStack(spacing: 10) {
                        Image(systemName: got ? "rosette" : "circle.dashed")
                            .font(.system(size: 13))
                            .foregroundColor(got ? Theme.ember : Theme.faint)
                            .frame(width: 22)
                        VStack(alignment: .leading, spacing: 4) {
                            HStack(spacing: 6) {
                                Text(a.name)
                                    .font(Theme.sans(12.5, .medium))
                                    .foregroundColor(got ? Theme.text : Theme.dim)
                                if a.hidden && !got {
                                    Chip(text: "隐藏", tint: Theme.faint)
                                }
                            }
                            Text(got ? a.desc : (a.hidden ? "达成条件未知" : a.desc))
                                .font(Theme.mono(8))
                                .foregroundColor(Theme.faint)
                                .lineLimit(2)
                            if !got {
                                GeometryReader { geo in
                                    ZStack(alignment: .leading) {
                                        Capsule().fill(Theme.text.opacity(0.06))
                                        Capsule().fill(Theme.ember.opacity(0.7))
                                            .frame(width: geo.size.width * CGFloat(value) / CGFloat(max(1, a.goal)))
                                    }
                                }
                                .frame(height: 3)
                            }
                        }
                        Spacer(minLength: 4)
                        Text("\(value)/\(a.goal)")
                            .font(Theme.mono(8))
                            .foregroundColor(Theme.faint)
                    }
                    .padding(.vertical, 8)
                    .hairline()
                }
            }
        }
    }
}

// MARK: - 剧本选择

struct ScenarioPanel: View {
    @EnvironmentObject var store: GameStore
    @State private var confirm: Scenario?

    var body: some View {
        PanelShell("选择剧本", subtitle: "解锁条件跨周目保留 · 记忆碎片 \(store.meta.shards)") {
            VStack(alignment: .leading, spacing: 12) {
                ForEach(ContentStore.scenarios) { s in
                    let unlocked = ContentStore.isUnlocked(s, meta: store.meta)
                    Button {
                        if unlocked { confirm = s }
                    } label: {
                        VStack(alignment: .leading, spacing: 7) {
                            HStack {
                                Text(s.name)
                                    .font(Theme.display(19))
                                    .foregroundColor(unlocked ? Theme.bone : Theme.faint)
                                Spacer()
                                if unlocked {
                                    Chip(text: "可开始", tint: Theme.toxic)
                                } else {
                                    Chip(text: unlockText(s), tint: Theme.faint)
                                }
                            }
                            Text(s.tagline)
                                .font(Theme.serif(11))
                                .foregroundColor(Theme.ember.opacity(unlocked ? 0.9 : 0.4))
                            Text(s.desc)
                                .font(Theme.mono(9))
                                .foregroundColor(unlocked ? Theme.dim : Theme.faint)
                                .lineSpacing(2)
                            HStack(spacing: 6) {
                                Chip(text: "HP \(100 + s.hpBonus)", tint: Theme.blood)
                                if s.apBonus != 0 { Chip(text: "AP +\(s.apBonus)", tint: Theme.ember) }
                                if let w = s.weapon, let wp = store.content.weapon(w) {
                                    Chip(text: wp.name, tint: Theme.steel)
                                }
                            }
                        }
                        .padding(14)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(
                            RoundedRectangle(cornerRadius: Theme.r, style: .continuous)
                                .fill(Theme.surface)
                                .overlay(RoundedRectangle(cornerRadius: Theme.r, style: .continuous)
                                    .strokeBorder(unlocked ? Theme.ember.opacity(0.18) : Theme.text.opacity(0.06), lineWidth: 1))
                        )
                        .opacity(unlocked ? 1 : 0.6)
                    }
                    .buttonStyle(PlainButtonStyle())
                }
            }
        }
        .confirmationDialog("以「\(confirm?.name ?? "")」开始新的生存？", isPresented: Binding(get: { confirm != nil }, set: { if !$0 { confirm = nil } })) {
            Button("开始", role: .destructive) {
                if let s = confirm {
                    store.panel = nil
                    store.newGame(s.id)
                }
                confirm = nil
            }
            Button("取消", role: .cancel) { confirm = nil }
        }
    }

    private func unlockText(_ s: Scenario) -> String {
        guard let rule = s.unlock else { return "已解锁" }
        let parts = rule.split(separator: ":")
        guard parts.count == 2 else { return "未解锁" }
        switch String(parts[0]) {
        case "bestDay": return "生存 \(parts[1]) 天解锁"
        case "kills": return "累计击杀 \(parts[1]) 解锁"
        case "shards": return "碎片 \(parts[1]) 解锁"
        case "endings": return "结局 \(parts[1]) 种解锁"
        case "ach": return "成就解锁"
        default: return "未解锁"
        }
    }
}

// MARK: - 结局

struct EndingView: View {
    @EnvironmentObject var store: GameStore

    private var ending: Ending? { store.endingCard ?? store.content.ending(store.state.ending ?? "") }

    var body: some View {
        ScrollView(showsIndicators: false) {
            VStack(alignment: .leading, spacing: 18) {
                HStack {
                    Text(ending?.kindName ?? "终结")
                        .font(Theme.mono(10, .semibold))
                        .kerning(2)
                        .foregroundColor(Theme.ember)
                    Spacer()
                    Text("第 \(store.state.day) 天")
                        .font(Theme.mono(10))
                        .foregroundColor(Theme.faint)
                }
                .padding(.top, 26)

                Text(ending?.title ?? "你倒下了")
                    .font(.system(size: 42, weight: .semibold, design: .serif))
                    .foregroundColor(Theme.bone)
                    .lineSpacing(2)

                DividerLine()

                Text(ending?.text ?? "")
                    .font(Theme.serif(14))
                    .foregroundColor(Theme.dim)
                    .lineSpacing(8)

                statsBlock

                Button {
                    store.newRunFromEnding()
                } label: {
                    Text("回到灰烬")
                }
                .buttonStyle(EmberButtonStyle())

                Button {
                    store.screen = .home
                    store.panel = .scenarios
                    store.endingCard = nil
                } label: {
                    Text("换个剧本")
                }
                .buttonStyle(GhostButtonStyle())
            }
            .padding(.horizontal, 24)
            .padding(.bottom, 30)
        }
        .background(
            ZStack {
                Theme.bgDeep.ignoresSafeArea()
                SceneArt(seed: 991, danger: 5)
                    .opacity(0.28)
                    .ignoresSafeArea()
                LinearGradient(colors: [Color.black.opacity(0.4), Theme.bgDeep], startPoint: .top, endPoint: .bottom)
                    .ignoresSafeArea()
            }
        )
    }

    private var statsBlock: some View {
        VStack(spacing: 10) {
            HStack(spacing: 0) {
                endStat("生存", "\(store.state.day)", "天")
                endStat("击杀", "\(store.state.stats["kills", default: 0])", "只")
                endStat("等级", "\(store.state.level)", "级")
            }
            HStack(spacing: 0) {
                endStat("地点", "\(store.state.visited.count)", "处")
                endStat("制作", "\(store.state.stats["crafts", default: 0])", "次")
                endStat("碎片", "\(store.meta.shards)", "枚")
            }
        }
        .padding(.vertical, 12)
        .background(RoundedRectangle(cornerRadius: Theme.r, style: .continuous).fill(Theme.surface.opacity(0.7)))
    }

    private func endStat(_ label: String, _ value: String, _ unit: String) -> some View {
        VStack(spacing: 4) {
            HStack(alignment: .firstTextBaseline, spacing: 2) {
                Text(value).font(Theme.mono(18, .semibold)).foregroundColor(Theme.text)
                Text(unit).font(Theme.mono(8)).foregroundColor(Theme.faint)
            }
            Text(label).font(Theme.mono(8)).kerning(1).foregroundColor(Theme.faint)
        }
        .frame(maxWidth: .infinity)
    }
}

struct EndingOverlay: View {
    @EnvironmentObject var store: GameStore
    let ending: Ending

    var body: some View {
        VStack {
            Spacer()
            VStack(alignment: .leading, spacing: 10) {
                Text(ending.kindName)
                    .font(Theme.mono(9, .semibold))
                    .kerning(1.6)
                    .foregroundColor(Theme.ember)
                Text(ending.title)
                    .font(Theme.display(22))
                    .foregroundColor(Theme.bone)
                Button {
                    store.screen = .ending
                } label: {
                    Text("查看结局")
                }
                .buttonStyle(EmberButtonStyle())
            }
            .padding(18)
            .background(RoundedRectangle(cornerRadius: Theme.r, style: .continuous).fill(Theme.surface))
            .padding(20)
        }
    }
}

// MARK: - 事件

struct EventView: View {
    @EnvironmentObject var store: GameStore
    @Environment(\.dismiss) private var dismiss
    @State private var current: EventCard

    init(event: EventCard) {
        _current = State(initialValue: event)
    }

    var body: some View {
        ZStack {
            Theme.bgDeep.ignoresSafeArea()
            SceneArt(seed: UInt64(abs(current.id.unicodeScalars.reduce(0) { $0 &+ Int($1.value) })) &* 43, danger: 3)
                .ignoresSafeArea()
                .opacity(0.22)
            LinearGradient(colors: [Color.black.opacity(0.5), Theme.bgDeep.opacity(0.96)],
                           startPoint: .top, endPoint: .bottom)
                .ignoresSafeArea()

            ScrollView(showsIndicators: false) {
                VStack(alignment: .leading, spacing: 18) {
                    HStack {
                        Chip(text: tagName(current.tag), tint: Theme.ember)
                        Spacer()
                        Button {
                            store.pendingEvent = nil
                            dismiss()
                        } label: {
                            Image(systemName: "xmark")
                                .font(.system(size: 11, weight: .bold))
                                .foregroundColor(Theme.faint)
                                .padding(8)
                        }
                        .buttonStyle(PlainButtonStyle())
                    }

                    Text(current.title)
                        .font(.system(size: 30, weight: .semibold, design: .serif))
                        .foregroundColor(Theme.bone)
                        .lineSpacing(4)

                    Rectangle().fill(Theme.ember.opacity(0.6)).frame(width: 40, height: 1)

                    Text(current.text)
                        .font(Theme.serif(14))
                        .foregroundColor(Theme.text.opacity(0.86))
                        .lineSpacing(8)
                        .fixedSize(horizontal: false, vertical: true)

                    VStack(spacing: 10) {
                        ForEach(current.choices.indices, id: \.self) { i in
                            choiceButton(current.choices[i])
                        }
                    }
                    .padding(.top, 6)
                }
                .padding(.horizontal, 22)
                .padding(.top, 20)
                .padding(.bottom, 30)
            }
        }
    }

    private func choiceButton(_ choice: EventChoice) -> some View {
        let enabled = store.canChoose(choice)
        return Button {
            store.choose(choice, from: current)
            if let next = store.pendingEvent {
                current = next
            } else {
                dismiss()
            }
        } label: {
            VStack(alignment: .leading, spacing: 6) {
                HStack(alignment: .top, spacing: 8) {
                    Image(systemName: enabled ? "chevron.right" : "lock")
                        .font(.system(size: 10, weight: .semibold))
                        .foregroundColor(enabled ? Theme.ember : Theme.faint)
                        .padding(.top, 3)
                    Text(choice.text)
                        .font(Theme.sans(13.5, .medium))
                        .foregroundColor(enabled ? Theme.text : Theme.faint)
                        .multilineTextAlignment(.leading)
                    Spacer(minLength: 0)
                    if choice.chance < 100 && enabled {
                        Text("\(choice.chance)%")
                            .font(Theme.mono(9, .medium))
                            .foregroundColor(Theme.ember.opacity(0.8))
                    }
                }
                if !enabled {
                    Text(requirementText(choice.req))
                        .font(Theme.mono(8))
                        .foregroundColor(Theme.blood.opacity(0.8))
                        .padding(.leading, 18)
                }
            }
            .padding(14)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .fill(Theme.surface.opacity(enabled ? 0.9 : 0.4))
                    .overlay(RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                        .strokeBorder(enabled ? Theme.text.opacity(0.09) : Theme.text.opacity(0.04), lineWidth: 1))
            )
        }
        .buttonStyle(PlainButtonStyle())
        .disabled(!enabled)
    }

    private func tagName(_ tag: String) -> String {
        switch tag {
        case "daily": return "每日 · 营地"
        case "encounter": return "遭遇"
        case "story": return "线索"
        case "trade": return "交易"
        default: return "事件"
        }
    }

    private func requirementText(_ req: [String]) -> String {
        req.map { r -> String in
            if r.hasPrefix("item:") {
                var s = String(r.dropFirst(5))
                var n = 1
                if let range = s.range(of: ">=") {
                    n = Int(s[range.upperBound...]) ?? 1
                    s = String(s[..<range.lowerBound])
                }
                return "需要 \(ContentStore.shared.itemName(s))×\(n)"
            }
            if r.hasPrefix("perk:") {
                let id = String(r.dropFirst(5))
                return "需要技能 \(ContentStore.shared.perk(id)?.name ?? id)"
            }
            if r.hasPrefix("faction:") { return "需要势力关系" }
            if r.hasPrefix("flag:") { return "条件未满足" }
            return "条件未满足"
        }.joined(separator: " · ")
    }
}
