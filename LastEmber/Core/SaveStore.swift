import Foundation

enum SaveStore {
    private static var dir: URL {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }

    private static func url(_ name: String) -> URL { dir.appendingPathComponent(name) }

    static func loadState() -> GameState? {
        decode(GameState.self, url("save.json"))
    }

    static func loadMeta() -> MetaState? {
        decode(MetaState.self, url("meta.json"))
    }

    static func save(state: GameState, meta: MetaState) {
        encode(state, url("save.json"))
        encode(meta, url("meta.json"))
    }

    static func clear() {
        try? FileManager.default.removeItem(at: url("save.json"))
        try? FileManager.default.removeItem(at: url("meta.json"))
    }

    private static func decode<T: Decodable>(_ type: T.Type, _ file: URL) -> T? {
        guard let data = try? Data(contentsOf: file) else { return nil }
        return try? JSONDecoder().decode(T.self, from: data)
    }

    private static func encode<T: Encodable>(_ value: T, _ file: URL) {
        guard let data = try? JSONEncoder().encode(value) else { return }
        try? data.write(to: file, options: .atomic)
    }
}
