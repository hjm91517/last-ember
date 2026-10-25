import SwiftUI

enum Theme {
    // 底色：冷绿偏的炭黑，避免纯黑死板
    static let bg = Color(hex: 0x0A0D0B)
    static let bgDeep = Color(hex: 0x060807)
    static let surface = Color(hex: 0x111613)
    static let surfaceHi = Color(hex: 0x18211B)
    static let surfaceLine = Color(hex: 0x232D26)

    static let text = Color(hex: 0xE6E1D3)
    static let dim = Color(hex: 0x9AA096)
    static let faint = Color(hex: 0x68716A)

    static let ember = Color(hex: 0xD97836)
    static let emberHi = Color(hex: 0xF2A45F)
    static let blood = Color(hex: 0xA5483E)
    static let toxic = Color(hex: 0x8C9B45)
    static let steel = Color(hex: 0x6E8781)
    static let bone = Color(hex: 0xD9D2C0)

    static let r: CGFloat = 16
    static let rSmall: CGFloat = 10
    static let rTiny: CGFloat = 6
    static let pad: CGFloat = 16

    static func display(_ size: CGFloat) -> Font {
        .system(size: size, weight: .semibold, design: .serif)
    }
    static func serif(_ size: CGFloat, _ weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight, design: .serif)
    }
    static func sans(_ size: CGFloat, _ weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight)
    }
    static func mono(_ size: CGFloat, _ weight: Font.Weight = .regular) -> Font {
        .system(size: size, weight: weight, design: .monospaced)
    }

    static let cardShadow = Color.black.opacity(0.45)

    static let emberGradient = LinearGradient(
        colors: [Color(hex: 0xE98B45), Color(hex: 0xC4602A)],
        startPoint: .topLeading, endPoint: .bottomTrailing)

    static let fade = LinearGradient(
        colors: [Color.clear, Color.black.opacity(0.35), Color.black.opacity(0.82)],
        startPoint: .top, endPoint: .bottom)
}

extension Color {
    init(hex: UInt32) {
        let r = Double((hex >> 16) & 0xFF) / 255.0
        let g = Double((hex >> 8) & 0xFF) / 255.0
        let b = Double(hex & 0xFF) / 255.0
        self.init(.sRGB, red: r, green: g, blue: b, opacity: 1)
    }
}

extension View {
    func cardStyle(padding: CGFloat = 16, radius: CGFloat = Theme.r) -> some View {
        self
            .padding(padding)
            .background(
                RoundedRectangle(cornerRadius: radius, style: .continuous)
                    .fill(Theme.surface)
                    .overlay(
                        RoundedRectangle(cornerRadius: radius, style: .continuous)
                            .strokeBorder(Theme.text.opacity(0.07), lineWidth: 1)
                    )
            )
            .shadow(color: Color(hex: 0x1A0F08).opacity(0.55), radius: 18, x: 0, y: 10)
            .shadow(color: Color.black.opacity(0.35), radius: 3, x: 0, y: 1)
    }

    func hairline() -> some View {
        overlay(alignment: .bottom) {
            Rectangle().fill(Theme.text.opacity(0.07)).frame(height: 1)
        }
    }

    func pressable() -> some View {
        modifier(PressableModifier())
    }
}

struct PressableModifier: ViewModifier {
    @State private var pressed = false
    func body(content: Content) -> some View {
        content
            .scaleEffect(pressed ? 0.975 : 1)
            .opacity(pressed ? 0.9 : 1)
            .animation(.easeOut(duration: 0.12), value: pressed)
            .simultaneousGesture(
                DragGesture(minimumDistance: 0)
                    .onChanged { _ in if !pressed { pressed = true } }
                    .onEnded { _ in pressed = false }
            )
    }
}

struct SectionLabel: View {
    let text: String
    var trail: String? = nil
    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 8) {
            Text(text)
                .font(Theme.mono(11, .semibold))
                .kerning(1.8)
                .foregroundColor(Theme.dim)
            Rectangle().fill(Theme.text.opacity(0.08)).frame(height: 1)
            if let t = trail {
                Text(t)
                    .font(Theme.mono(11))
                    .foregroundColor(Theme.faint)
            }
        }
    }
}

struct Chip: View {
    let text: String
    var tint: Color = Theme.dim
    var filled: Bool = false
    var body: some View {
        Text(text)
            .font(Theme.mono(10, .semibold))
            .kerning(0.6)
            .foregroundColor(filled ? Theme.bgDeep : tint)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(
                Capsule().fill(filled ? tint : tint.opacity(0.10))
                    .overlay(Capsule().strokeBorder(tint.opacity(filled ? 0 : 0.28), lineWidth: 1))
            )
    }
}

struct StatBar: View {
    let label: String
    let value: Int
    let maxValue: Int
    var tint: Color = Theme.ember
    var icon: String? = nil
    var mini: Bool = false

    private var ratio: CGFloat {
        guard maxValue > 0 else { return 0 }
        return min(1, max(0, CGFloat(value) / CGFloat(maxValue)))
    }

    var body: some View {
        VStack(alignment: .leading, spacing: mini ? 4 : 6) {
            HStack(spacing: 5) {
                if let i = icon {
                    Image(systemName: i)
                        .font(.system(size: mini ? 9 : 10, weight: .semibold))
                        .foregroundColor(tint.opacity(0.9))
                }
                Text(label)
                    .font(Theme.mono(mini ? 9 : 10, .medium))
                    .kerning(0.8)
                    .foregroundColor(Theme.dim)
                Spacer(minLength: 4)
                Text("\(value)")
                    .font(Theme.mono(mini ? 10 : 11, .semibold))
                    .foregroundColor(tint)
            }
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule().fill(Theme.text.opacity(0.07))
                    Capsule()
                        .fill(LinearGradient(colors: [tint.opacity(0.75), tint], startPoint: .leading, endPoint: .trailing))
                        .frame(width: max(2, geo.size.width * ratio))
                }
            }
            .frame(height: mini ? 3 : 5)
        }
    }
}

struct ActionTile: View {
    let title: String
    let note: String
    let icon: String
    var tint: Color = Theme.ember
    var disabled: Bool = false
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Image(systemName: icon)
                        .font(.system(size: 14, weight: .medium))
                        .foregroundColor(disabled ? Theme.faint : tint)
                    Spacer()
                    Image(systemName: "arrow.up.right")
                        .font(.system(size: 9, weight: .bold))
                        .foregroundColor(Theme.faint)
                }
                Text(title)
                    .font(Theme.sans(14, .semibold))
                    .foregroundColor(disabled ? Theme.faint : Theme.text)
                Text(note)
                    .font(Theme.mono(9))
                    .foregroundColor(Theme.faint)
                    .lineLimit(1)
                    .minimumScaleFactor(0.8)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(12)
            .background(
                RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                    .fill(Theme.surfaceHi.opacity(disabled ? 0.35 : 1))
                    .overlay(
                        RoundedRectangle(cornerRadius: Theme.rSmall, style: .continuous)
                            .strokeBorder(Theme.text.opacity(0.06), lineWidth: 1)
                    )
            )
        }
        .buttonStyle(PlainButtonStyle())
        .disabled(disabled)
        .pressable()
    }
}

struct EmberButtonStyle: ButtonStyle {
    var tint: Color = Theme.ember
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(Theme.mono(13, .semibold))
            .kerning(1.2)
            .foregroundColor(Theme.bgDeep)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 15)
            .background(
                LinearGradient(colors: [tint.opacity(configuration.isPressed ? 0.8 : 1), tint.opacity(0.82)],
                               startPoint: .top, endPoint: .bottom)
            )
            .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
            .shadow(color: tint.opacity(0.25), radius: 14, x: 0, y: 8)
            .scaleEffect(configuration.isPressed ? 0.985 : 1)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}

struct GhostButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(Theme.mono(12, .medium))
            .kerning(1.2)
            .foregroundColor(configuration.isPressed ? Theme.emberHi : Theme.text)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 13)
            .background(
                RoundedRectangle(cornerRadius: 12, style: .continuous)
                    .fill(Theme.surfaceHi.opacity(configuration.isPressed ? 1 : 0.6))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12, style: .continuous)
                            .strokeBorder(Theme.text.opacity(0.12), lineWidth: 1)
                    )
            )
    }
}

struct PanelHeader: View {
    let title: String
    var subtitle: String? = nil
    let onClose: () -> Void
    var body: some View {
        HStack(alignment: .center) {
            VStack(alignment: .leading, spacing: 3) {
                Text(title)
                    .font(Theme.display(22))
                    .foregroundColor(Theme.text)
                if let s = subtitle {
                    Text(s)
                        .font(Theme.mono(10))
                        .kerning(1)
                        .foregroundColor(Theme.faint)
                }
            }
            Spacer()
            Button(action: onClose) {
                Image(systemName: "xmark")
                    .font(.system(size: 12, weight: .bold))
                    .foregroundColor(Theme.dim)
                    .frame(width: 34, height: 34)
                    .background(Circle().fill(Theme.surfaceHi))
                    .overlay(Circle().strokeBorder(Theme.text.opacity(0.08), lineWidth: 1))
            }
            .buttonStyle(PlainButtonStyle())
        }
    }
}

struct EmptyState: View {
    let icon: String
    let title: String
    let note: String
    var body: some View {
        VStack(spacing: 10) {
            Image(systemName: icon)
                .font(.system(size: 26, weight: .light))
                .foregroundColor(Theme.faint)
            Text(title)
                .font(Theme.sans(14, .medium))
                .foregroundColor(Theme.dim)
            Text(note)
                .font(Theme.mono(10))
                .foregroundColor(Theme.faint)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 34)
    }
}

struct ToastView: View {
    let text: String
    var body: some View {
        Text(text)
            .font(Theme.mono(11, .medium))
            .foregroundColor(Theme.bone)
            .padding(.horizontal, 14)
            .padding(.vertical, 10)
            .background(
                Capsule().fill(Theme.surfaceHi)
                    .overlay(Capsule().strokeBorder(Theme.ember.opacity(0.35), lineWidth: 1))
            )
            .shadow(color: Color.black.opacity(0.5), radius: 12, y: 6)
    }
}
