import SwiftUI

@main
struct LastEmberApp: App {
    var body: some Scene {
        WindowGroup {
            RootView()
                .preferredColorScheme(.dark)
        }
    }
}

struct RootView: View {
    @StateObject private var store = GameStore()

    var body: some View {
        ZStack {
            Theme.bg.ignoresSafeArea()

            switch store.screen {
            case .home:
                HomeView()
            case .game:
                GameView()
            case .ending:
                EndingView()
            }

            if store.state.battle != nil && store.state.ending == nil {
                BattleView()
                    .transition(.opacity)
            }

            if let ending = store.endingCard, store.screen != .ending {
                EndingOverlay(ending: ending)
            }

            toastLayer
        }
        .environmentObject(store)
        .sheet(item: $store.panel) { panel in
            PanelHost(panel: panel)
                .environmentObject(store)
        }
        .fullScreenCover(item: $store.pendingEvent) { event in
            EventView(event: event)
                .environmentObject(store)
        }
        .onChange(of: store.toast) { value in
            guard value != nil else { return }
            DispatchQueue.main.asyncAfter(deadline: .now() + 2.2) {
                withAnimation(.easeOut(duration: 0.2)) { store.toast = nil }
            }
        }
        .animation(.easeOut(duration: 0.28), value: store.screen == .game)
        .animation(.easeOut(duration: 0.2), value: store.state.battle != nil)
    }

    private var toastLayer: some View {
        VStack {
            Spacer()
            if let t = store.toast {
                ToastView(text: t)
                    .padding(.bottom, 26)
                    .transition(.opacity.combined(with: .move(edge: .bottom)))
            }
        }
        .animation(.easeOut(duration: 0.2), value: store.toast)
        .allowsHitTesting(false)
    }
}
