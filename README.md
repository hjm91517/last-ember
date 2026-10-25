# 余烬 · Last Ember

> 一款单机丧尸末日生存 Roguelike，纯 SwiftUI 编写，无第三方依赖。
> 你从第 47 天醒来，带着一根铁管和三天口粮，目标是走到还在运转的白塔灯塔。

## 这是什么

- **类型**：回合制生存 / 资源管理 / 事件抉择 / 战斗 Roguelike
- **平台**：iPhone（iOS 16+），竖屏，离线运行，自动存档
- **体量**（由 `tools/` 下的生成器产出，全部为原创内容）：
  - 203 种物品 · 53 件武器 · 44 件护甲 · 55 个配方
  - 78 种敌人（含 14 名首领）· 40 个敌人技能 · 53 个地点 · 5 个区域
  - 141 张事件卡 · 61 条任务（10 章主线 + 51 条支线）
  - 46 个技能 · 16 座据点设施 · 16 名可招募 NPC · 137 段拾得文本
  - 138 个成就 · 24 种结局 · 11 个可选剧本

## 玩法

- 每天 3 点行动点：搜刮、移动、休息、制作、结束今日。
- 六项生存压力：生命、饥饿、口渴、感染、理智、疲劳；感染到 100 会转化。
- 回合制战斗：攻击 / 重击 / 瞄准 / 闪避 / 用药 / 投掷 / 逃跑，武器有耐久，会断。
- 资源循环：搜刮 → 拆解 / 制作 → 升级据点 → 支撑更远的探索。
- 同伴系统：4 个岗位，每晚结算产出与风险。
- 任务与剧本：主线通向灯塔，结局取决于你带去了什么、又留下了什么。
- 周目继承：记忆碎片、成就、结局图鉴、剧本解锁。

## 从源码构建

需要 macOS + Xcode 15 或以上，以及 [XcodeGen](https://github.com/yonaskolb/XcodeGen)。

```bash
brew install xcodegen
xcodegen generate
open LastEmber.xcodeproj
```

或直接命令行：

```bash
xcodebuild -project LastEmber.xcodeproj -scheme LastEmber \
  -sdk iphoneos -configuration Release CODE_SIGNING_ALLOWED=NO build
```

## 下载

最新构建产物在 **[Releases](https://github.com/hjm91517/last-ember/releases)**：
`LastEmber-unsigned.ipa`（约 1.5 MB，未签名，iOS 16+，iPhone / iPad）。

## 安装 IPA

GitHub Actions 会在每次推送到 `main` 或打 `v*` 标签时构建 **未签名** IPA，并发布到 Releases。

未签名 IPA 不能直接双击安装，需要自行签名：

- **Sideloadly / AltStore / SideStore**：用你自己的 Apple ID 签名（免费账号 7 天有效）。
- **TrollStore**：支持的设备可直接安装（iOS 14–17.x 特定版本）。
- 有开发者账号也可用 Xcode 直接跑真机。

安装后首次启动即为完整游戏：没有账号、没有联网请求、没有内购。

## 工程结构

```
LastEmber/
  App/            入口与根视图
  Core/           模型、内容加载、引擎、存档
  UI/             主题、组件、主界面、战斗、面板
  Resources/
    Content/*.json  全部游戏内容（运行时加载）
    Assets.xcassets AppIcon 与配色
tools/            Python 内容生成器与交叉引用校验
.github/          GitHub Actions：构建 + 发布 IPA
```

### 内容生成与校验

```bash
python3 tools/gen_items.py     # 物品 / 武器 / 护甲 / 配方
python3 tools/gen_world.py     # 敌人 / 技能 / 地点
python3 tools/gen_events.py    # 事件卡
python3 tools/gen_meta.py      # 技能 / 设施 / 结局 / NPC / 任务 / 成就 / 日志
python3 tools/validate.py      # 交叉引用检查（必须输出 ALL REFERENCES OK）
python3 tools/gen_icon.py      # 重新生成 AppIcon
```

内容全部为 JSON，改完不需要重新编译 Swift；但 id 之间互相引用，改动后请跑一遍 `validate.py`。

## 已验证 / 未验证

已验证：

- `xcodebuild` Release 构建通过（GitHub Actions macOS runner，`CODE_SIGNING_ALLOWED=NO`）。
- 15 个内容 JSON 的交叉引用与结构校验通过（`tools/validate.py`、`tools/check_schema.py`）。
- IPA 结构检查：`Payload/LastEmber.app` 内含全部 15 个内容 JSON、Assets.car 与可执行文件；
  `CFBundleDisplayName=余烬`、`MinimumOSVersion=16.0`。

未验证：

- 真机/模拟器上的运行时表现（本环境无 Xcode 与 iOS 设备），包括布局、触控、长时间游玩与存档读档。
- 签名与安装（IPA 未签名，需要你自己签）。

## 说明

- 本作为原创虚构作品，人物、组织、事件均与现实无关。
- 无内购、无广告、无联网请求、不收集任何数据。
- 代码以 MIT 许可发布，内容为原创虚构作品。
- 存档位于 App 沙盒 `Documents/save.json` 与 `meta.json`。
