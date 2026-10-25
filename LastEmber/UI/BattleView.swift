import SwiftUI

struct BattleView: View {
    @EnvironmentObject var store: GameStore
    @State private var flash = false

    var body: some View {
        ZStack {
            Theme.bgDeep.ignoresSafeArea()

            if let b = store.state.battle, let enemy = store.content.enemy(b.enemy) {
                SceneArt(seed: UInt64(abs(enemy.id.unicodeScalars.reduce(0) { $0 &+ Int($1.value) })) &* 17,
                         danger: enemy.tier)
                    .ignoresSafeArea()
                    .opacity(0.5)

                LinearGradient(colors: [Color.black.opacity(0.7), Theme.bgDeep.opacity(0.93), Theme.bgDeep],
                               startPoint: .top, endPoint: .bottom)
                    .ignoresSafeArea()

                VStack(spacing: 12) {
                    topBar(enemy)
                    enemyPanel(enemy, b)
                    battleLog(b)
                    Spacer(minLength: 0)
                    actionPanel(enemy, b)
                }
                .padding(.horizontal, 16)
                .padding(.top, 8)
                .padding(.bottom, 12)

                if b.ended {
                    resultOverlay(b)
                }
            }
        }
    }

    private func topBar(_ enemy: Enemy) -> some View {
        HStack {
            Text("遭遇 / \(enemy.tagName.uppercased())")
                .font(Theme.mono(10, .semibold))
                .kerning(1.6)
                .foregroundColor(Theme.blood)
            Spacer()
            Text("回合 \(store.state.battle?.round ?? 1)")
                .font(Theme.mono(10))
                .foregroundColor(Theme.faint)
            Button {
                store.panel = .inventory
            } label: {
                Image(systemName: "bag")
                    .font(.system(size: 12))
                    .foregroundColor(Theme.dim)
                    .padding(8)
            }
            .buttonStyle(PlainButtonStyle())
        }
    }

    private func enemyPanel(_ enemy: Enemy, _ b: BattleState) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .top, spacing: 14) {
                ZStack {
                    Circle().fill(Theme.blood.opacity(0.10)).frame(width: 66, height: 66)
                    Circle().strokeBorder(Theme.blood.opacity(0.28), lineWidth: 1).frame(width: 66, height: 66)
                    Image(systemName: enemy.icon)
                        .font(.system(size: 27, weight: .light))
                        .foregroundColor(Theme.blood.opacity(0.92))
                }
                VStack(alignment: .leading, spacing: 6) {
                    Text(enemy.name)
                        .font(Theme.display(24))
                        .foregroundColor(Theme.bone)
                        .lineLimit(1)
                        .minimumScaleFactor(0.7)
                    HStack(spacing: 6) {
                        Chip(text: "T\(enemy.tier)", tint: Theme.ember)
                        Chip(text: "护甲 \(enemy.armor)", tint: Theme.steel)
                        Chip(text: "闪避 \(enemy.evade)%", tint: Theme.dim)
                    }
                }
                Spacer(minLength: 0)
            }

            VStack(spacing: 6) {
                GeometryReader { geo in
                    ZStack(alignment: .leading) {
                        Capsule().fill(Theme.text.opacity(0.08))
                        Capsule()
                            .fill(LinearGradient(colors: [Theme.blood.opacity(0.7), Theme.blood],
                                                 startPoint: .leading, endPoint: .trailing))
                            .frame(width: max(3, geo.size.width * CGFloat(max(0, b.hp)) / CGFloat(max(1, b.maxHP))))
                    }
                }
                .frame(height: 7)
                HStack {
                    Text("敌方生命")
                        .font(Theme.mono(9))
                        .foregroundColor(Theme.faint)
                    Spacer()
                    Text("\(max(0, b.hp)) / \(b.maxHP)")
                        .font(Theme.mono(10, .semibold))
                        .foregroundColor(Theme.blood)
                }
            }

            HStack(spacing: 6) {
                ForEach(Array(enemy.abilities.prefix(3)), id: \.self) { aid in
                    if let ab = store.content.ability(aid) {
                        Chip(text: ab.name, tint: Theme.toxic)
                    }
                }
                Spacer()
                Text(enemy.desc)
                    .font(Theme.serif(10))
                    .foregroundColor(Theme.faint)
                    .lineLimit(1)
                    .frame(maxWidth: 150, alignment: .trailing)
            }
        }
        .cardStyle(padding: 14)
    }

    private func battleLog(_ b: BattleState) -> some View {
        ScrollViewReader { proxy in
            ScrollView(showsIndicators: false) {
                VStack(alignment: .leading, spacing: 6) {
                    ForEach(b.log.indices, id: \.self) { idx in
                        HStack(alignment: .top, spacing: 8) {
                            Text(String(format: "%02d", idx + 1))
                                .font(Theme.mono(8))
                                .foregroundColor(Theme.faint)
                                .padding(.top, 2)
                            Text(b.log[idx])
                                .font(Theme.sans(12))
                                .foregroundColor(lineColor(b.log[idx]))
                                .lineSpacing(3)
                                .fixedSize(horizontal: false, vertical: true)
                            Spacer(minLength: 0)
                        }
                        .id(idx)
                    }
                }
                .padding(12)
            }
            .frame(maxHeight: 190)
            .background(
                RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .fill(Color.black.opacity(0.35))
                    .overlay(RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                        .strokeBorder(Theme.text.opacity(0.06), lineWidth: 1))
            )
            .onAppear {
                proxy.scrollTo(max(0, b.log.count - 1), anchor: .bottom)
            }
            .onChange(of: b.log.count) { count in
                withAnimation(.easeOut(duration: 0.2)) {
                    proxy.scrollTo(max(0, count - 1), anchor: .bottom)
                }
            }
        }
    }

    private func lineColor(_ text: String) -> Color {
        if text.contains("伤害") || text.contains("暴击") { return Theme.ember }
        if text.contains("逃") { return Theme.dim }
        if text.contains("倒下") { return Theme.toxic }
        return Theme.text.opacity(0.86)
    }

    private func actionPanel(_ enemy: Enemy, _ b: BattleState) -> some View {
        VStack(spacing: 8) {
            HStack(spacing: 10) {
                StatBar(label: "生命", value: store.state.hp, maxValue: store.state.hpMax,
                        tint: Theme.blood, icon: "heart.fill", mini: true)
                StatBar(label: "感染", value: store.state.infection, maxValue: 100,
                        tint: Theme.toxic, icon: "allergens", mini: true)
            }
            .padding(.horizontal, 2)

            HStack(spacing: 8) {
                Button {
                    store.battleAction(.attack)
                } label: {
                    battleButton("攻击", note: weaponNote, icon: "bolt.fill", tint: Theme.ember, primary: true)
                }
                .buttonStyle(PlainButtonStyle())
                .disabled(b.ended)

                Button {
                    store.battleAction(.heavy)
                } label: {
                    battleButton("重击", note: "伤害+50% · 命中-18", icon: "hammer.fill", tint: Theme.blood)
                }
                .buttonStyle(PlainButtonStyle())
                .disabled(b.ended)
            }

            HStack(spacing: 8) {
                smallBattleButton("瞄准", "scope", Theme.steel) { store.battleAction(.aim) }
                smallBattleButton("闪避", "figure.run", Theme.dim) { store.battleAction(.dodge) }
                smallBattleButton("用药", "bandage.fill", Theme.blood) { store.battleAction(.item) }
                smallBattleButton("投掷", "flame.fill", Theme.ember) { store.battleAction(.throwable) }
            }
            .disabled(b.ended)

            Button {
                store.battleAction(.flee)
            } label: {
                Text("试图逃跑")
                    .font(Theme.mono(11, .medium))
                    .foregroundColor(Theme.faint)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 9)
            }
            .buttonStyle(PlainButtonStyle())
            .disabled(b.ended)
        }
    }

    private var weaponNote: String {
        guard let w = store.weapon, let g = store.weaponGear else { return "徒手" }
        return "\(w.name) · 耐久 \(max(0, g.dur))"
    }

    private func battleButton(_ title: String, note: String, icon: String, tint: Color, primary: Bool = false) -> some View {
        VStack(alignment: .leading, spacing: 5) {
            HStack {
                Image(systemName: icon)
                    .font(.system(size: 12, weight: .semibold))
                    .foregroundColor(primary ? Theme.bgDeep : tint)
                Spacer()
            }
            Text(title)
                .font(Theme.sans(15, .semibold))
                .foregroundColor(primary ? Theme.bgDeep : Theme.text)
            Text(note)
                .font(Theme.mono(8))
                .foregroundColor(primary ? Theme.bgDeep.opacity(0.65) : Theme.faint)
                .lineLimit(1)
                .minimumScaleFactor(0.75)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(12)
        .background(
            RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                .fill(primary ? AnyShapeStyle(Theme.emberGradient) : AnyShapeStyle(Theme.surfaceHi))
                .overlay(RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .strokeBorder(Theme.text.opacity(primary ? 0 : 0.07), lineWidth: 1))
        )
    }

    private func smallBattleButton(_ title: String, _ icon: String, _ tint: Color, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            VStack(spacing: 5) {
                Image(systemName: icon)
                    .font(.system(size: 13, weight: .medium))
                    .foregroundColor(tint)
                Text(title)
                    .font(Theme.mono(9, .medium))
                    .foregroundColor(Theme.dim)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 9)
            .background(
                RoundedRectangle(cornerRadius: 9, style: .continuous)
                    .fill(Theme.surface)
                    .overlay(RoundedRectangle(cornerRadius: 9, style: .continuous)
                        .strokeBorder(Theme.text.opacity(0.07), lineWidth: 1))
            )
        }
        .buttonStyle(PlainButtonStyle())
    }

    private func resultOverlay(_ b: BattleState) -> some View {
        ZStack {
            Color.black.opacity(0.72).ignoresSafeArea()
            VStack(alignment: .leading, spacing: 14) {
                Text(b.victory ? "威胁解除" : "你逃开了")
                    .font(Theme.display(26))
                    .foregroundColor(b.victory ? Theme.toxic : Theme.dim)
                Text(b.victory ? "呼吸还很急促，但你还站着。" : "你跑出很远，才敢回头看。")
                    .font(Theme.serif(12))
                    .foregroundColor(Theme.dim)

                if !b.loot.isEmpty {
                    DividerLine()
                    Text("战利品")
                        .font(Theme.mono(9, .semibold))
                        .kerning(1.4)
                        .foregroundColor(Theme.faint)
                    ForEach(b.loot.keys.sorted(), id: \.self) { key in
                        HStack {
                            Text(store.content.itemName(key))
                                .font(Theme.sans(13))
                                .foregroundColor(Theme.text)
                            Spacer()
                            Text("×\(b.loot[key, default: 0])")
                                .font(Theme.mono(11, .semibold))
                                .foregroundColor(Theme.ember)
                        }
                    }
                }

                Button {
                    store.closeBattle()
                } label: {
                    Text("继续")
                }
                .buttonStyle(EmberButtonStyle())
                .padding(.top, 4)
            }
            .padding(20)
            .frame(maxWidth: 340)
            .background(
                RoundedRectangle(cornerRadius: Theme.r, style: .continuous)
                    .fill(Theme.surface)
                    .overlay(RoundedRectangle(cornerRadius: Theme.r, style: .continuous)
                        .strokeBorder(Theme.text.opacity(0.09), lineWidth: 1))
            )
            .shadow(color: Color.black.opacity(0.6), radius: 30, y: 14)
        }
        .transition(.opacity)
    }
}
