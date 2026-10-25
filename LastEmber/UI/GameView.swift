import SwiftUI

struct GameView: View {
    @EnvironmentObject var store: GameStore

    var body: some View {
        ScrollView(showsIndicators: false) {
            VStack(alignment: .leading, spacing: 14) {
                header
                sceneCard
                vitals
                objectiveStrip
                actions
                logPanel
                Color.clear.frame(height: 20)
            }
            .padding(.horizontal, 16)
            .padding(.top, 6)
        }
    }

    // MARK: - 顶部

    private var header: some View {
        HStack(alignment: .center, spacing: 10) {
            Button {
                store.returnHome()
            } label: {
                Image(systemName: "chevron.left")
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundColor(Theme.dim)
                    .frame(width: 34, height: 34)
                    .background(Circle().fill(Theme.surface))
                    .overlay(Circle().strokeBorder(Theme.text.opacity(0.08), lineWidth: 1))
            }
            .buttonStyle(PlainButtonStyle())

            VStack(alignment: .leading, spacing: 2) {
                Text(store.dayLabel)
                    .font(Theme.mono(12, .semibold))
                    .kerning(0.8)
                    .foregroundColor(Theme.text)
                Text("\(store.state.region) · \(store.currentPlace?.name ?? "未知地带")")
                    .font(Theme.mono(9))
                    .foregroundColor(Theme.faint)
            }

            Spacer()

            VStack(alignment: .trailing, spacing: 5) {
                APRow(current: store.state.ap, total: store.apCap)
                Text("行动点 \(store.state.ap)/\(store.apCap)")
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.faint)
            }

            Button {
                store.panel = .character
            } label: {
                ZStack {
                    Circle().fill(Theme.surface).frame(width: 34, height: 34)
                    Text("Lv\(store.state.level)")
                        .font(Theme.mono(9, .bold))
                        .foregroundColor(Theme.ember)
                }
                .overlay(Circle().strokeBorder(Theme.text.opacity(0.08), lineWidth: 1))
            }
            .buttonStyle(PlainButtonStyle())
        }
        .padding(.top, 8)
    }

    // MARK: - 场景卡

    private var sceneCard: some View {
        ZStack(alignment: .bottomLeading) {
            SceneArt(seed: seedForPlace, danger: store.currentPlace?.danger ?? 2)
                .frame(height: 188)
                .clipShape(RoundedRectangle(cornerRadius: Theme.r, style: .continuous))

            LinearGradient(colors: [Color.clear, Color.black.opacity(0.35), Color.black.opacity(0.85)],
                           startPoint: .center, endPoint: .bottom)
                .clipShape(RoundedRectangle(cornerRadius: Theme.r, style: .continuous))

            VStack(alignment: .leading, spacing: 8) {
                HStack(spacing: 8) {
                    Chip(text: store.currentPlace?.region ?? "未知", tint: Theme.steel)
                    Chip(text: store.currentPlace?.tags.first.map { tagName($0) } ?? "废墟", tint: Theme.dim)
                    Spacer()
                    HStack(spacing: 5) {
                        Text("危险")
                            .font(Theme.mono(8))
                            .foregroundColor(Theme.faint)
                        DangerMark(level: store.currentPlace?.danger ?? 1)
                    }
                }
                Text(store.currentPlace?.name ?? "未知")
                    .font(Theme.display(28))
                    .foregroundColor(Theme.bone)
                Text(store.currentPlace?.desc ?? "")
                    .font(Theme.serif(12))
                    .foregroundColor(Theme.text.opacity(0.72))
                    .lineSpacing(4)
                    .lineLimit(2)
                HStack(spacing: 16) {
                    HStack(spacing: 6) {
                        Text("资源")
                            .font(Theme.mono(8))
                            .foregroundColor(Theme.faint)
                        StagePips(used: store.state.stage[store.state.place, default: 0],
                                  total: store.currentPlace?.stages ?? 3)
                    }
                    if store.currentPlace?.id == "safehouse" {
                        Text("安全区 · 可作为据点")
                            .font(Theme.mono(8))
                            .foregroundColor(Theme.toxic)
                    }
                }
            }
            .padding(14)
        }
        .overlay(
            RoundedRectangle(cornerRadius: Theme.r, style: .continuous)
                .strokeBorder(Theme.text.opacity(0.08), lineWidth: 1)
        )
        .shadow(color: Color.black.opacity(0.5), radius: 16, y: 8)
    }

    private var seedForPlace: UInt64 {
        UInt64(abs(store.state.place.unicodeScalars.reduce(0) { $0 &+ Int($1.value) })) &* 31 &+ UInt64(store.state.day)
    }

    private func tagName(_ tag: String) -> String {
        switch tag {
        case "urban": return "城区"
        case "indoor": return "室内"
        case "market": return "商铺"
        case "medical": return "医疗"
        case "military": return "军用"
        case "rural": return "郊野"
        case "industrial": return "工业"
        case "lab": return "实验"
        case "start": return "据点"
        case "water": return "水域"
        case "dark": return "昏暗"
        case "boss": return "首领"
        default: return tag
        }
    }

    // MARK: - 体征

    private var vitals: some View {
        VStack(spacing: 12) {
            StatBar(label: "生命", value: store.state.hp, maxValue: store.state.hpMax,
                    tint: Theme.blood, icon: "heart.fill")
            HStack(spacing: 16) {
                StatBar(label: "饥饿", value: store.state.hunger, maxValue: 100,
                        tint: Theme.ember, icon: "fork.knife", mini: true)
                StatBar(label: "口渴", value: store.state.thirst, maxValue: 100,
                        tint: Theme.steel, icon: "drop.fill", mini: true)
            }
            HStack(spacing: 16) {
                StatBar(label: "感染", value: store.state.infection, maxValue: 100,
                        tint: Theme.toxic, icon: "allergens", mini: true)
                StatBar(label: "理智", value: store.state.sanity, maxValue: 100,
                        tint: Theme.dim, icon: "brain.head.profile", mini: true)
            }
            HStack(spacing: 8) {
                Chip(text: "疲劳 \(store.state.fatigue)", tint: store.state.fatigue > 65 ? Theme.blood : Theme.dim)
                Chip(text: "体温 \(store.state.warmth)", tint: store.state.warmth < 35 ? Theme.steel : Theme.dim)
                Chip(text: "负重 \(Int(store.currentWeight))/\(store.carryCapacity)",
                     tint: store.currentWeight > Double(store.carryCapacity) ? Theme.blood : Theme.dim)
                Spacer()
            }
        }
        .cardStyle(padding: 14)
    }

    // MARK: - 目标

    private var objectiveStrip: some View {
        HStack(spacing: 10) {
            Rectangle().fill(Theme.ember).frame(width: 2, height: 26)
            VStack(alignment: .leading, spacing: 2) {
                Text("当前目标")
                    .font(Theme.mono(8))
                    .kerning(1.4)
                    .foregroundColor(Theme.faint)
                Text(objectiveText)
                    .font(Theme.sans(12, .medium))
                    .foregroundColor(Theme.text.opacity(0.9))
                    .lineLimit(1)
                    .minimumScaleFactor(0.85)
            }
            Spacer()
            Button {
                store.panel = .quests
            } label: {
                Text("任务")
                    .font(Theme.mono(9, .medium))
                    .foregroundColor(Theme.ember)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(Capsule().fill(Theme.ember.opacity(0.12)))
            }
            .buttonStyle(PlainButtonStyle())
        }
        .padding(.vertical, 2)
    }

    private var objectiveText: String {
        if let q = store.state.activeQuests.first,
           let def = store.content.quest(q.id) {
            let p = min(store.questProgress(def), def.count)
            return "\(def.title)  ·  \(p)/\(def.count)"
        }
        if store.state.flags["lighthouse_known", default: 0] == 1 {
            let cores = store.state.inventory["light_core", default: 0]
            return "前往灯塔，交付核心（\(cores)/6）"
        }
        return "搜刮物资，撑过下一个夜晚"
    }

    // MARK: - 行动

    private var actions: some View {
        VStack(spacing: 10) {
            SectionLabel(text: "行动", trail: "每次行动消耗 1 点")
            LazyVGrid(columns: [GridItem(.flexible(), spacing: 10), GridItem(.flexible(), spacing: 10)], spacing: 10) {
                ActionTile(title: "搜刮", note: stageNote, icon: "magnifyingglass", tint: Theme.ember) {
                    store.search()
                }
                ActionTile(title: "移动", note: "\(store.content.placeList.count) 个地点", icon: "map", tint: Theme.steel) {
                    store.panel = .map
                }
                ActionTile(title: "休息", note: "回血 · 降疲劳", icon: "moon.zzz", tint: Theme.dim) {
                    store.rest()
                }
                ActionTile(title: "制作", note: "\(store.content.recipes.count) 个配方", icon: "hammer", tint: Theme.toxic) {
                    store.panel = .craft
                }
                ActionTile(title: "背包", note: "\(store.state.inventory.count) 种物品", icon: "bag", tint: Theme.bone) {
                    store.panel = .inventory
                }
                ActionTile(title: "据点", note: "\(store.state.buildings.count) 座设施", icon: "house", tint: Theme.ember) {
                    store.panel = .base
                }
            }

            Button {
                store.endDay()
            } label: {
                HStack {
                    Image(systemName: "moon.stars")
                        .font(.system(size: 12, weight: .semibold))
                    Text("结束第 \(store.state.day) 天")
                    Spacer()
                    Text("进入夜晚")
                        .font(Theme.mono(10))
                        .opacity(0.6)
                }
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(EmberButtonStyle())

            HStack(spacing: 8) {
                miniAction("同伴", "person.2", .squad)
                miniAction("任务", "list.bullet.rectangle", .quests)
                miniAction("角色", "figure.stand", .character)
                miniAction("图鉴", "book.closed", .codex)
            }
        }
    }

    private func miniAction(_ title: String, _ icon: String, _ panel: Panel) -> some View {
        Button {
            store.panel = panel
        } label: {
            HStack(spacing: 5) {
                Image(systemName: icon)
                    .font(.system(size: 10, weight: .medium))
                Text(title)
                    .font(Theme.mono(9, .medium))
            }
            .foregroundColor(Theme.dim)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 9)
            .background(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(Theme.surface)
                    .overlay(RoundedRectangle(cornerRadius: 8, style: .continuous)
                        .strokeBorder(Theme.text.opacity(0.06), lineWidth: 1))
            )
        }
        .buttonStyle(PlainButtonStyle())
        .pressable()
    }

    private var stageNote: String {
        guard let p = store.currentPlace else { return "未知" }
        let used = store.state.stage[p.id, default: 0]
        if used >= p.stages { return "已被搬空" }
        return "剩余 \(p.stages - used) 处 · 危险 \(p.danger)"
    }

    // MARK: - 日志

    private var logPanel: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                SectionLabel(text: "日志", trail: "第 \(store.state.day) 天")
                Button {
                    store.panel = .journal
                } label: {
                    Text("全部")
                        .font(Theme.mono(9, .medium))
                        .foregroundColor(Theme.ember)
                }
                .buttonStyle(PlainButtonStyle())
            }

            VStack(alignment: .leading, spacing: 2) {
                ForEach(Array(store.state.log.suffix(12))) { line in
                    LogLineView(line: line)
                }
            }
            .padding(12)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(
                RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .fill(Theme.bgDeep.opacity(0.7))
                    .overlay(
                        RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                            .strokeBorder(Theme.text.opacity(0.06), lineWidth: 1)
                    )
            )
        }
    }
}
