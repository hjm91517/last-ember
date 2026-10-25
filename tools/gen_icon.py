#!/usr/bin/env python3
"""生成 AppIcon（1024）与资源目录 JSON。"""
import json, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "LastEmber", "Resources", "Assets.xcassets")
os.makedirs(os.path.join(ASSETS, "AppIcon.appiconset"), exist_ok=True)
os.makedirs(os.path.join(ASSETS, "AccentColor.colorset"), exist_ok=True)
os.makedirs(os.path.join(ASSETS, "LaunchBackground.colorset"), exist_ok=True)

W = H = 1024
CX = 512
TOP_Y, BASE_Y = 356, 904
TOP_W, BASE_W = 104, 212

def half_width(y):
    t = (BASE_Y - y) / (BASE_Y - TOP_Y)
    t = max(0.0, min(1.0, t))
    return (BASE_W + (TOP_W - BASE_W) * t) / 2

img = Image.new("RGB", (W, H), (8, 11, 9))
d = ImageDraw.Draw(img, "RGBA")

# 夜空渐变
for y in range(H):
    t = y / (H - 1)
    c = (int(8 + 16 * t), int(11 + 14 * t), int(9 + 10 * t))
    d.line([(0, y), (W, y)], fill=c)

# 星星 / 灰烬
random.seed(23)
for _ in range(110):
    x, y = random.randint(0, W), random.randint(0, 700)
    r = random.uniform(0.7, 1.9)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(242, 168, 104, random.randint(20, 80)))

# 远景废墟
sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sil)
x = -30
random.seed(5)
while x < W + 30:
    bw = random.randint(36, 92)
    bh = random.randint(24, 118)
    sd.rectangle([x, 872 - bh, x + bw, 890], fill=(5, 7, 6, 235))
    if random.random() < 0.4:
        ax = x + bw // 2
        sd.line([(ax, 872 - bh), (ax, 850 - bh - random.randint(4, 22))], fill=(5, 7, 6, 235), width=3)
    x += bw + random.randint(3, 16)
sil = sil.filter(ImageFilter.GaussianBlur(1.2))
img = Image.alpha_composite(img.convert("RGBA"), sil)

# 光束
beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon([(CX, 338), (W + 60, 196), (W + 60, 372)], fill=(255, 198, 132, 74))
bd.polygon([(CX, 338), (W + 60, 372), (W + 60, 470)], fill=(255, 176, 104, 30))
bd.polygon([(CX, 338), (-60, 214), (-60, 356)], fill=(255, 198, 132, 30))
beam = beam.filter(ImageFilter.GaussianBlur(11))
img = Image.alpha_composite(img, beam)

d = ImageDraw.Draw(img, "RGBA")

# 水面
d.rectangle([0, 888, W, H], fill=(9, 12, 10, 255))
random.seed(88)
for i in range(90):
    yy = 894 + int((i * 43) % 126)
    xx = random.randint(-20, W)
    ln = random.randint(16, 110)
    d.line([(xx, yy), (xx + ln, yy)], fill=(200, 170, 120, random.randint(3, 12)), width=1)

# 塔身（带三圈锈红）
tower_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
td = ImageDraw.Draw(tower_layer)
td.polygon([(CX - half_width(BASE_Y), BASE_Y), (CX - half_width(TOP_Y), TOP_Y),
            (CX + half_width(TOP_Y), TOP_Y), (CX + half_width(BASE_Y), BASE_Y)],
           fill=(208, 201, 185, 255))
# 右侧阴影
td.polygon([(CX + 18, TOP_Y), (CX + half_width(TOP_Y), TOP_Y),
            (CX + half_width(BASE_Y), BASE_Y), (CX + 36, BASE_Y)],
           fill=(178, 170, 155, 255))
for (y0, y1) in [(452, 514), (584, 646), (716, 778)]:
    td.polygon([(CX - half_width(y0), y0), (CX - half_width(y1), y1),
                (CX, y1), (CX, y0)], fill=(160, 74, 56, 235))
    td.polygon([(CX, y0), (CX, y1), (CX + half_width(y1), y1),
                (CX + half_width(y0), y0)], fill=(132, 60, 47, 225))
# 窗
for y in [392, 540, 672, 804]:
    wdt = 30 - int((y - 392) / 20)
    td.rounded_rectangle([CX - wdt // 2, y, CX + wdt // 2, y + 30], radius=5, fill=(16, 20, 16, 255))
    lit = y < 700
    td.rounded_rectangle([CX - wdt // 2 + 3, y + 3, CX + wdt // 2 - 3, y + 27], radius=3,
                         fill=(250, 190, 120, 240) if lit else (74, 82, 70, 255))
img = Image.alpha_composite(img, tower_layer)

# 灯室
d = ImageDraw.Draw(img, "RGBA")
d.rectangle([CX - 58, 306, CX + 58, 360], fill=(26, 30, 24, 255))
d.rectangle([CX - 48, 312, CX + 48, 354], fill=(255, 214, 152, 255))
d.rectangle([CX - 48, 312, CX + 48, 354], outline=(255, 246, 224, 255), width=3)
for gx in range(CX - 48, CX + 49, 24):
    d.line([(gx, 312), (gx, 354)], fill=(120, 96, 66, 150), width=2)
# 顶盖与栏杆
d.polygon([(CX - 66, 306), (CX, 258), (CX + 66, 306)], fill=(186, 179, 164, 255))
d.rectangle([CX - 6, 228, CX + 6, 262], fill=(150, 143, 130, 255))
d.rectangle([CX - 70, 296, CX + 70, 304], fill=(118, 112, 100, 255))

# 灯光光晕
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(22, 0, -1):
    rr = i * 16
    gd.ellipse([CX - rr, 332 - rr, CX + rr, 332 + rr], fill=(255, 190, 120, int(3.4 * (22 - i))))
glow = glow.filter(ImageFilter.GaussianBlur(20))
img = Image.alpha_composite(img, glow)

# 水面倒影
ref = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(ref)
random.seed(77)
for i in range(16):
    yy = 900 + i * 8
    ww = int(46 * (1 - i / 22))
    if ww <= 0:
        break
    rd.rectangle([CX - ww, yy, CX + ww, yy + 3], fill=(250, 178, 110, max(10, 62 - i * 4)))
ref = ref.filter(ImageFilter.GaussianBlur(5))
img = Image.alpha_composite(img, ref)

# 前景碎石与栏杆
d = ImageDraw.Draw(img, "RGBA")
random.seed(41)
for _ in range(40):
    px, py = random.randint(0, W), random.randint(936, 1014)
    r = random.randint(2, 8)
    d.ellipse([px, py, px + r * 2, py + r], fill=(17, 21, 18, 200))

# 暗角与颗粒
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-int(W * 0.26), -int(H * 0.24), int(W * 1.26), int(H * 1.24)], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(150))
black = Image.new("RGB", (W, H), (4, 6, 5))
img = Image.composite(img.convert("RGB"), black, vig)
noise = Image.effect_noise((W, H), 14).convert("L")
noise_rgb = Image.merge("RGB", (noise, noise, noise))
img = Image.blend(img, ImageChops.multiply(img, noise_rgb), 0.045)

img.save(os.path.join(ASSETS, "AppIcon.appiconset", "icon-1024.png"), "PNG")
print("icon saved")

def wjson(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

wjson(os.path.join(ASSETS, "Contents.json"), {"info": {"author": "xcode", "version": 1}})
wjson(os.path.join(ASSETS, "AppIcon.appiconset", "Contents.json"), {
    "images": [{"filename": "icon-1024.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"}],
    "info": {"author": "xcode", "version": 1}
})
wjson(os.path.join(ASSETS, "AccentColor.colorset", "Contents.json"), {
    "colors": [{"color": {"color-space": "srgb", "components": {"alpha": "1.000", "blue": "0.212", "green": "0.471", "red": "0.851"}},
                "idiom": "universal"}],
    "info": {"author": "xcode", "version": 1}
})
wjson(os.path.join(ASSETS, "LaunchBackground.colorset", "Contents.json"), {
    "colors": [{"color": {"color-space": "srgb", "components": {"alpha": "1.000", "blue": "0.043", "green": "0.051", "red": "0.039"}},
                "idiom": "universal"}],
    "info": {"author": "xcode", "version": 1}
})
print("assets json saved")
