import SwiftUI

struct HomeView: View {
    @EnvironmentObject var store: GameStore
    @State private var confirmNew = false
    @State private var showScenarios = false

    private var hasRun: Bool {
        !store.state.log.isEmpty && store.state.ending == nil
    }

    var body: some View {
        GeometryReader { geo in
            ZStack {
                SceneArt(seed: UInt64(store.meta.runs &* 97 &+ 13), danger: 3)
                    .frame(width: geo.size.width, height: geo.size.height)
                    .ignoresSafeArea()

                LinearGradient(
                    colors: [Color.black.opacity(0.55), Color.black.opacity(0.15), Color.black.opacity(0.86)],
                    startPoint: .top, endPoint: .bottom)
                    .ignoresSafeArea()

                ScrollView(showsIndicators: false) {
                    VStack(alignment: .leading, spacing: 0) {
                        topBar
                        Spacer(minLength: geo.size.height * 0.16)
                        titleBlock
                        Spacer(minLength: 34)
                        actionBlock
                        Spacer(minLength: 28)
                        metaBlock
                        footer
                    }
                    .padding(.horizontal, 24)
                    .frame(minHeight: geo.size.height, alignment: .top)
                }
            }
        }
        .confirmationDialog("开始新的生存？当前进度会被覆盖。", isPresented: $confirmNew, titleVisibility: .visible) {
            Button("覆盖并重新开始", role: .destructive) { showScenarios = true }
            Button("取消", role: .cancel) {}
        }
        .sheet(isPresented: $showScenarios) {
            PanelHost(panel: .scenarios)
                .environmentObject(store)
        }
    }

    private var topBar: some View {
        HStack(alignment: .center) {
            HStack(spacing: 7) {
                Circle().fill(Theme.ember).frame(width: 6, height: 6)
                Text("ASH EPOCH / 灰烬纪元")
                    .font(Theme.mono(10, .medium))
                    .kerning(1.6)
                    .foregroundColor(Theme.dim)
            }
            Spacer()
            Text("v1.0")
                .font(Theme.mono(10))
                .foregroundColor(Theme.faint)
        }
        .padding(.top, 12)
    }

    private var titleBlock: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("DAY 47")
                .font(Theme.mono(11, .semibold))
                .kerning(3)
                .foregroundColor(Theme.ember)

            Text("余烬")
                .font(.system(size: 76, weight: .semibold, design: .serif))
                .kerning(4)
                .foregroundColor(Theme.bone)
                .shadow(color: Theme.ember.opacity(0.22), radius: 22, x: 0, y: 8)

            HStack(spacing: 10) {
                Rectangle().fill(Theme.ember.opacity(0.7)).frame(width: 28, height: 1)
                Text("LAST EMBER")
                    .font(Theme.mono(12, .medium))
                    .kerning(4.2)
                    .foregroundColor(Theme.dim)
            }

            Text("在灰烬里，活着是一种技术。\n搜刮、搏杀、撑过夜晚，然后走到灯塔。")
                .font(Theme.serif(14))
                .foregroundColor(Theme.dim)
                .lineSpacing(7)
                .padding(.top, 4)
        }
    }

    private var actionBlock: some View {
        VStack(spacing: 12) {
            if hasRun {
                Button {
                    store.continueGame()
                } label: {
                    HStack(spacing: 10) {
                        Text("继续生存")
                        Spacer()
                        Text("第 \(store.state.day) 天 · \(store.currentPlace?.name ?? "未知")")
                            .font(Theme.mono(10))
                            .opacity(0.65)
                    }
                    .frame(maxWidth: .infinity)
                }
                .buttonStyle(EmberButtonStyle())
            }

            Button {
                if hasRun { confirmNew = true } else { showScenarios = true }
            } label: {
                HStack(spacing: 10) {
                    Text(hasRun ? "重新开始" : "进入废墟")
                    Spacer()
                    Image(systemName: "chevron.right")
                        .font(.system(size: 11, weight: .bold))
                }
                .frame(maxWidth: .infinity)
            }
            .buttonStyle(GhostButtonStyle())

            HStack(spacing: 10) {
                smallButton(icon: "book.closed", title: "图鉴") { store.panel = .codex }
                smallButton(icon: "rosette", title: "成就") { store.panel = .achievements }
                smallButton(icon: "questionmark.circle", title: "档案") { store.panel = .journal }
            }
        }
    }

    private func smallButton(icon: String, title: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            VStack(spacing: 7) {
                Image(systemName: icon)
                    .font(.system(size: 15, weight: .light))
                    .foregroundColor(Theme.dim)
                Text(title)
                    .font(Theme.mono(9))
                    .kerning(1)
                    .foregroundColor(Theme.faint)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .fill(Color.black.opacity(0.28))
                    .overlay(
                        RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                            .strokeBorder(Theme.text.opacity(0.08), lineWidth: 1)
                    )
            )
        }
        .buttonStyle(PlainButtonStyle())
        .pressable()
    }

    private var metaBlock: some View {
        VStack(alignment: .leading, spacing: 12) {
            SectionLabel(text: "生存档案", trail: "档案会跨周目保留")
            HStack(spacing: 0) {
                statCell("最远", "\(store.meta.bestDay)", "天")
                divider
                statCell("击杀", "\(store.meta.totalKills)", "只")
                divider
                statCell("结局", "\(store.meta.endings.count)/\(max(1, ContentStore.shared.endings.count))", "种")
                divider
                statCell("碎片", "\(store.meta.shards)", "枚")
            }
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .fill(Color.black.opacity(0.3))
            )
        }
    }

    private var divider: some View {
        Rectangle().fill(Theme.text.opacity(0.07)).frame(width: 1, height: 26)
    }

    private func statCell(_ label: String, _ value: String, _ unit: String) -> some View {
        VStack(spacing: 5) {
            HStack(alignment: .firstTextBaseline, spacing: 3) {
                Text(value)
                    .font(Theme.mono(17, .semibold))
                    .foregroundColor(Theme.text)
                Text(unit)
                    .font(Theme.mono(8))
                    .foregroundColor(Theme.faint)
            }
            Text(label)
                .font(Theme.mono(9))
                .kerning(1)
                .foregroundColor(Theme.faint)
        }
        .frame(maxWidth: .infinity)
    }

    private var footer: some View {
        HStack {
            Text("单机 · 无需联网 · 进度自动保存")
                .font(Theme.mono(9))
                .foregroundColor(Theme.faint)
            Spacer()
            Text("\(ContentStore.shared.itemList.count) 物品 · \(ContentStore.shared.enemyList.count) 敌人 · \(ContentStore.shared.events.count) 事件")
                .font(Theme.mono(9))
                .foregroundColor(Theme.faint.opacity(0.85))
        }
        .padding(.top, 18)
        .padding(.bottom, 22)
    }
}
