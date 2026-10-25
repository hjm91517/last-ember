import SwiftUI

// MARK: - 场景插画（程序化绘制的废墟剪影）

struct SceneArt: View {
    var seed: UInt64 = 7
    var danger: Int = 2
    var body: some View {
        GeometryReader { geo in
            let size = geo.size
            ZStack {
                LinearGradient(
                    colors: [Color(hex: 0x0B1311), Color(hex: 0x131A13), Color(hex: 0x231A10)],
                    startPoint: .top, endPoint: .bottom)

                // 月晕
                RadialGradient(
                    colors: [Theme.bone.opacity(0.18), Theme.bone.opacity(0.02), Color.clear],
                    center: UnitPoint(x: 0.72, y: 0.22),
                    startRadius: 0, endRadius: size.width * 0.55)
                    .blendMode(.screen)

                Canvas { ctx, canvasSize in
                    var rng = SeededRNG(seed: seed &* 2_654_435_761 &+ 17)
                    let w = canvasSize.width
                    let h = canvasSize.height

                    // 月亮
                    let moon = CGRect(x: w * 0.68, y: h * 0.10, width: w * 0.13, height: w * 0.13)
                    ctx.fill(Path(ellipseIn: moon), with: .color(Theme.bone.opacity(0.55)))
                    ctx.fill(Path(ellipseIn: moon.insetBy(dx: -10, dy: -10)), with: .color(Theme.bone.opacity(0.04)))

                    // 三层楼群，越远越淡
                    for layer in 0..<3 {
                        let depth = Double(layer)
                        let baseline = h * (0.60 + depth * 0.075)
                        let tint = Color(hex: 0x0D1411).opacity(0.55 + depth * 0.25)
                        var x = -CGFloat(rng.int(4...30))
                        while x < w + 30 {
                            let bw = CGFloat(rng.int(16...54)) + CGFloat(depth) * 6
                            let bh = CGFloat(rng.int(18...74)) * (1.0 - depth * 0.18) + h * 0.06
                            let rect = CGRect(x: x, y: baseline - bh, width: bw, height: bh + h * 0.5)
                            ctx.fill(Path(rect), with: .color(tint))

                            // 屋顶水塔 / 天线
                            if rng.chance(22) && depth < 2 {
                                let ax = x + bw * 0.5
                                var antenna = Path()
                                antenna.move(to: CGPoint(x: ax, y: baseline - bh))
                                antenna.addLine(to: CGPoint(x: ax, y: baseline - bh - CGFloat(rng.int(8...26))))
                                ctx.stroke(antenna, with: .color(tint.opacity(0.9)), lineWidth: 1)
                            }

                            // 亮着的窗
                            if depth < 2 {
                                let cols = max(1, Int(bw / 11))
                                let rows = max(1, Int(bh / 13))
                                for c in 0..<cols {
                                    for r in 0..<rows where rng.chance(13) {
                                        let rw: CGFloat = 3
                                        let rh: CGFloat = 4
                                        let wr = CGRect(
                                            x: x + CGFloat(c) * 9 + 4,
                                            y: baseline - bh + CGFloat(r) * 10 + 5,
                                            width: rw, height: rh)
                                        let lit = rng.chance(35)
                                        let color = lit ? Theme.ember.opacity(Double(rng.int(20...55)) / 100.0)
                                                        : Theme.steel.opacity(0.12)
                                        ctx.fill(Path(wr), with: .color(color))
                                    }
                                }
                            }
                            x += bw + CGFloat(rng.int(3...14))
                        }
                    }

                    // 地面 / 雾
                    let groundY = h * 0.80
                    ctx.fill(Path(CGRect(x: 0, y: groundY, width: w, height: h - groundY)),
                             with: .linearGradient(Gradient(colors: [Color(hex: 0x0A0E0B), Color(hex: 0x050706)]),
                                                   startPoint: CGPoint(x: 0, y: groundY), endPoint: CGPoint(x: 0, y: h)))
                    ctx.fill(Path(CGRect(x: 0, y: groundY - h * 0.09, width: w, height: h * 0.18)),
                             with: .linearGradient(Gradient(colors: [Color.clear, Theme.bone.opacity(0.05), Color.clear]),
                                                   startPoint: CGPoint(x: 0, y: groundY - h * 0.09),
                                                   endPoint: CGPoint(x: 0, y: groundY + h * 0.09)))

                    // 前景栅栏
                    var fence = Path()
                    let fy = h * 0.855
                    var fx: CGFloat = 0
                    while fx < w {
                        fence.move(to: CGPoint(x: fx, y: fy))
                        fence.addLine(to: CGPoint(x: fx + CGFloat(rng.int(-3...3)), y: h))
                        fx += CGFloat(rng.int(14...30))
                    }
                    ctx.stroke(fence, with: .color(Color.black.opacity(0.45)), lineWidth: 1.2)
                }

                EmberField(count: max(8, danger * 5 + 6), seed: seed)
                    .opacity(0.75)
            }
            .clipped()
        }
    }
}

struct EmberField: View {
    var count: Int = 20
    var seed: UInt64 = 3

    var body: some View {
        TimelineView(.animation(minimumInterval: 1.0 / 20.0)) { timeline in
            Canvas { ctx, size in
                let t = timeline.date.timeIntervalSinceReferenceDate
                var rng = SeededRNG(seed: seed &+ 99)
                for _ in 0..<count {
                    let baseX = CGFloat(rng.double()) * size.width
                    let speed = 5.0 + rng.double() * 16.0
                    let phase = rng.double() * 10.0
                    let span = Double(size.height) + 40
                    let y = size.height + 20 - CGFloat((t * speed + phase * 37).truncatingRemainder(dividingBy: span))
                    let drift = CGFloat(sin(t * 0.6 + phase)) * 7
                    let radius = CGFloat(0.6 + rng.double() * 1.7)
                    let alpha = 0.18 + rng.double() * 0.55
                    let rect = CGRect(x: baseX + drift, y: y, width: radius * 2, height: radius * 2)
                    ctx.fill(Path(ellipseIn: rect), with: .color(Theme.ember.opacity(alpha)))
                }
            }
        }
        .allowsHitTesting(false)
    }
}

// MARK: - 小部件

struct DangerMark: View {
    let level: Int
    var body: some View {
        HStack(spacing: 3) {
            ForEach(0..<5, id: \.self) { i in
                RoundedRectangle(cornerRadius: 1, style: .continuous)
                    .fill(i < level ? Theme.blood : Theme.text.opacity(0.10))
                    .frame(width: 4, height: i < level ? 9 : 6)
            }
        }
    }
}

struct StagePips: View {
    let used: Int
    let total: Int
    var body: some View {
        HStack(spacing: 3) {
            ForEach(0..<max(1, total), id: \.self) { i in
                Circle()
                    .fill(i < used ? Theme.faint.opacity(0.35) : Theme.ember.opacity(0.75))
                    .frame(width: 5, height: 5)
            }
        }
    }
}

struct APRow: View {
    let current: Int
    let total: Int
    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<max(total, 1), id: \.self) { i in
                RoundedRectangle(cornerRadius: 2, style: .continuous)
                    .fill(i < current ? Theme.ember : Theme.text.opacity(0.12))
                    .frame(width: 12, height: 5)
            }
        }
    }
}

struct ItemRow: View {
    let item: Item
    let count: Int
    var trailing: String? = nil
    var body: some View {
        HStack(spacing: 12) {
            ZStack {
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(Theme.surfaceHi)
                    .frame(width: 38, height: 38)
                Image(systemName: item.icon)
                    .font(.system(size: 15, weight: .regular))
                    .foregroundColor(tint)
            }
            VStack(alignment: .leading, spacing: 3) {
                HStack(spacing: 6) {
                    Text(item.name)
                        .font(Theme.sans(14, .medium))
                        .foregroundColor(Theme.text)
                    Text("×\(count)")
                        .font(Theme.mono(11, .semibold))
                        .foregroundColor(Theme.dim)
                }
                Text(item.desc)
                    .font(Theme.mono(9))
                    .foregroundColor(Theme.faint)
                    .lineLimit(2)
            }
            Spacer(minLength: 6)
            VStack(alignment: .trailing, spacing: 3) {
                Text(item.categoryName)
                    .font(Theme.mono(9))
                    .foregroundColor(Theme.faint)
                if let t = trailing {
                    Text(t)
                        .font(Theme.mono(9, .medium))
                        .foregroundColor(Theme.ember.opacity(0.8))
                }
            }
        }
        .padding(.vertical, 7)
    }

    private var tint: Color {
        switch item.cat {
        case "med": return Theme.blood
        case "food": return Theme.ember
        case "drink": return Theme.steel
        case "ammo": return Theme.toxic
        case "quest": return Theme.emberHi
        case "valuable": return Theme.bone
        default: return Theme.dim
        }
    }
}

struct GearRow: View {
    let title: String
    let subtitle: String
    let icon: String
    let stat: String
    var tint: Color = Theme.ember
    var body: some View {
        HStack(spacing: 12) {
            ZStack {
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(Theme.surfaceHi)
                    .frame(width: 38, height: 38)
                Image(systemName: icon)
                    .font(.system(size: 15))
                    .foregroundColor(tint)
            }
            VStack(alignment: .leading, spacing: 3) {
                Text(title)
                    .font(Theme.sans(14, .medium))
                    .foregroundColor(Theme.text)
                Text(subtitle)
                    .font(Theme.mono(9))
                    .foregroundColor(Theme.faint)
                    .lineLimit(1)
            }
            Spacer(minLength: 6)
            Text(stat)
                .font(Theme.mono(11, .semibold))
                .foregroundColor(tint)
        }
        .padding(.vertical, 7)
    }
}

struct LogLineView: View {
    let line: LogLine
    var body: some View {
        HStack(alignment: .top, spacing: 9) {
            Text("D\(line.day)")
                .font(Theme.mono(9, .medium))
                .foregroundColor(Theme.faint)
                .frame(width: 26, alignment: .leading)
            Rectangle()
                .fill(color.opacity(0.7))
                .frame(width: 2)
                .clipShape(Capsule())
            Text(line.text)
                .font(Theme.sans(12.5))
                .foregroundColor(line.kind == "info" ? Theme.dim : Theme.text.opacity(0.92))
                .lineSpacing(3)
                .fixedSize(horizontal: false, vertical: true)
            Spacer(minLength: 0)
        }
        .padding(.vertical, 3)
    }

    private var color: Color {
        switch line.kind {
        case "good": return Theme.toxic
        case "bad": return Theme.blood
        case "combat": return Theme.steel
        case "story": return Theme.ember
        default: return Theme.dim
        }
    }
}

struct DividerLine: View {
    var body: some View {
        Rectangle().fill(Theme.text.opacity(0.07)).frame(height: 1)
    }
}
