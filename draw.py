#!/usr/bin/env python3
"""news-23 b113 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories: 3 hero scenes + 10 cards + 18 ALSO + map pins + DATE CHECK.
Output: entry.png 1024x1024, < 1 MiB."""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (192, 0, 0)
DARKRED = (150, 0, 0)
GOLD = (176, 134, 11)
NAVY = (30, 58, 95)
GREEN = (20, 83, 45)
GRAY = (90, 90, 90)
LGRAY = (238, 238, 238)
CREAM = (255, 247, 224)
LGREEN = (200, 230, 160)
MGREEN = (143, 191, 111)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trunc(text, font, max_w):
    if font.getlength(text) <= max_w:
        return text
    while len(text) > 1 and font.getlength(text + "\u2026") > max_w:
        text = text[:-1]
    return text + "\u2026"

# ---------- masthead ----------
d.rectangle([0, 0, W, 56], fill=BLACK)
d.text((16, 7), "THE WORLD TODAY", font=F(SERIF_B, 38), fill=WHITE)
d.text((1008, 22), "MONDAY 23 NOVEMBER 2026", font=F(SANS_B, 14),
       fill=(212, 175, 55), anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 56, W, 76], fill=RED)
d.text((512, 61), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  "
       "US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
       font=F(SANS_B, 12), fill=WHITE, anchor="ma")

# ---------- number strip (10 numbers, 5 cols x 2 rows) ----------
nums = [
    ("-3.3%", "KOSPI"), ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"), ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"), ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"), ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
for i, (v, lab) in enumerate(nums):
    col, row = i % 5, i // 5
    x0 = 8 + col * 202
    y0 = 80 + row * 24
    d.text((x0, y0), v, font=F(SANS_B, 15), fill=RED if i == 0 else BLACK)
    d.text((x0, y0 + 15), lab, font=F(SANS, 8), fill=GRAY)
    if col < 4:
        d.line([x0 + 196, y0 + 2, x0 + 196, y0 + 22], fill=(220, 220, 220))

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", 227, NAVY), ("AMERICAS 8", 260, RED),
           ("MIDDLE EAST 6", 195, (0, 120, 120)), ("EUROPE 5", 163, (90, 60, 140)),
           ("AFRICA 3", 98, (40, 120, 40)), ("WORLD 2", 65, (60, 60, 60))]
x = 8
for label, wdt, col in regions:
    d.rectangle([x, 128, x + wdt - 1, 146], fill=col)
    d.text((x + wdt / 2, 132), label, font=F(SANS_B, 10), fill=WHITE, anchor="ma")
    x += wdt

# ---------- UTC strip ----------
d.rectangle([0, 148, W, 162], fill=LGRAY)
d.text((8, 151), "THE DAY IN UTC   ~00:00 Kospi dives  \u00b7  ~05:30 Guterres opens  "
       "\u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles",
       font=F(SANS, 9), fill=GRAY)
d.text((1016, 151), "~ APPROX", font=F(SANS, 9), fill=GRAY, anchor="ra")

# ---------- heroes ----------
HERO_X = [8, 347, 686]
HERO_W = 330
CHIP_FONT = F(SANS_B, 8)

def chip(xr, y, label, col):
    tw = CHIP_FONT.getlength(label) + 10
    d.rectangle([xr - tw, y, xr, y + 13], fill=col)
    d.text((xr - tw / 2, y + 2), label, font=CHIP_FONT, fill=WHITE, anchor="ma")

def hero_text(col_i, headline, body, source, chip_label, chip_col):
    x0 = HERO_X[col_i]
    hl = wrap(headline, F(SANS_B, 15), HERO_W)
    y = 292
    for ln in hl[:2]:
        d.text((x0, y), ln, font=F(SANS_B, 15), fill=BLACK)
        y += 17
    bl = wrap(body, F(SANS, 10), HERO_W)
    y = 332
    for ln in bl[:2]:
        d.text((x0, y), ln, font=F(SANS, 10), fill=BLACK)
        y += 12
    d.text((x0, 368), source, font=F(SANS, 8), fill=GRAY)
    chip(x0 + HERO_W, 366, chip_label, chip_col)

# hero 1 — Kospi chart scene
x0 = HERO_X[0]
d.rectangle([x0, 162, x0 + HERO_W, 288], fill=(11, 30, 58))
rng = random.Random(42)
for _ in range(50):
    wx = x0 + rng.randint(160, 312)
    wy = 170 + rng.randint(0, 92)
    d.rectangle([wx, wy, wx + 7, wy + 9], fill=(255, 214, 90))
d.text((x0 + 10, 166), "-3.3%", font=F(SANS_B, 32), fill=WHITE)
pts = [(x0 + 170, 202), (x0 + 200, 212), (x0 + 228, 208),
       (x0 + 255, 226), (x0 + 282, 236), (x0 + 310, 250)]
d.line(pts, fill=(255, 140, 40), width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE,
              outline=(255, 140, 40))
d.rectangle([x0, 272, x0 + HERO_W, 288], fill=BLACK)
d.text((x0 + 6, 275), "KOSPI 4,708.54  \u00b7  -161 PTS", font=F(SANS_B, 9), fill=WHITE)
hero_text(0, "AI ROUT HITS ASIA",
          "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. "
          "Samsung -3.1%, SK Hynix -2.5%.",
          "KOREA EXCHANGE", "REPORTED", NAVY)

# hero 2 — Guterres globe scene
x0 = HERO_X[1]
d.rectangle([x0, 162, x0 + HERO_W, 288], fill=GREEN)
d.text((x0 + 10, 164), "150", font=F(SANS_B, 40), fill=(212, 175, 55))
d.text((x0 + 10, 206), "DELEGATES", font=F(SANS_B, 19), fill=(212, 175, 55))
d.text((x0 + 10, 226), "BACK A RISK", font=F(SANS_B, 19), fill=(212, 175, 55))
d.text((x0 + 10, 246), "FRAMEWORK", font=F(SANS_B, 19), fill=(212, 175, 55))
cx, cy, r = x0 + 272, 222, 38
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(187, 247, 208))
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(20, 83, 45), width=2)
d.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=(20, 83, 45))
d.line([cx - r, cy, cx + r, cy], fill=(20, 83, 45))
d.line([cx, cy - r, cx, cy + r], fill=(20, 83, 45))
d.rectangle([x0, 272, x0 + HERO_W, 288], fill=BLACK)
d.text((x0 + 6, 275), "UN  \u00b7  BRIDGETOWN", font=F(SANS_B, 9), fill=WHITE)
hero_text(1, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
          "UN chief urges global AI safety rules at the Bridgetown summit; "
          "150 back a risk framework.",
          "UNITED NATIONS", "REPORTED", NAVY)

# hero 3 — Power Index bars scene
x0 = HERO_X[2]
d.rectangle([x0, 162, x0 + HERO_W, 288], fill=CREAM)
d.text((x0 + 8, 168), "NARROWEST SINCE 2018", font=F(SANS_B, 10), fill=BLACK)
d.text((x0 + HERO_W - 8, 168), "GAP 5.3", font=F(SANS_B, 12), fill=RED, anchor="ra")
bars = [("78.9", "US", NAVY, 55), ("73.6", "CHINA", RED, 51),
        ("40.5", "INDIA", GOLD, 28)]
base = 256
for i, (val, lab, col, hgt) in enumerate(bars):
    bx = x0 + 30 + i * 110
    d.text((bx + 26, base - hgt - 16), val, font=F(SANS_B, 13), fill=BLACK,
           anchor="ma")
    d.rectangle([bx, base - hgt, bx + 52, base], fill=col)
    d.text((bx + 26, base + 2), lab, font=F(SANS_B, 8), fill=BLACK, anchor="ma")
d.rectangle([x0, 272, x0 + HERO_W, 288], fill=BLACK)
d.text((x0 + 6, 275), "ASIA POWER INDEX 2026", font=F(SANS_B, 9), fill=WHITE)
hero_text(2, "US LEAD OVER CHINA AT RECORD LOW",
          "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest "
          "since 2018. India third at 40.5.",
          "LOWY INSTITUTE", "REPORTED", NAVY)

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 398, W, 416], fill=BLACK)
d.text((8, 402), "MORE OF THE DAY  \u2014  10 STORIES", font=F(SANS_B, 11), fill=WHITE)

# ---------- cards (5 cols x 2 rows) ----------
CAT_COL = {"AMERICAS": RED, "WHITE HOUSE": (120, 60, 0), "MARKETS": NAVY,
           "SPORT": (140, 110, 0), "LEGAL": (90, 60, 140), "TECH": (0, 120, 120),
           "EUROPE": (90, 60, 140), "SPACE": (60, 60, 60)}
cards = [
    ("AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED", NAVY),
    ("AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED", NAVY),
    ("WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED", NAVY),
    ("MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED", NAVY),
    ("SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", NAVY),
    ("SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED", NAVY),
    ("LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED", NAVY),
    ("TECH", "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED", NAVY),
    ("EUROPE", "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM", RED),
    ("SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM", RED),
]
for i, (cat, head, body, src, clab, ccol) in enumerate(cards):
    col, row = i % 5, i // 5
    cx = 8 + col * 202
    cy = 420 + row * 74
    cw, ch = 196, 66
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=(248, 248, 248),
                outline=(220, 220, 220))
    d.text((cx + 6, cy + 4), cat, font=F(SANS_B, 8), fill=CAT_COL[cat])
    d.text((cx + cw - 6, cy + 3), str(i + 1), font=F(SANS_B, 10), fill=RED,
           anchor="ra")
    hl = wrap(head, F(SANS_B, 11), cw - 12)
    y = cy + 15
    for ln in hl[:2]:
        d.text((cx + 6, y), ln, font=F(SANS_B, 11), fill=BLACK)
        y += 12
    d.text((cx + 6, cy + 40), trunc(body, F(SANS, 9), cw - 12),
           font=F(SANS, 9), fill=BLACK)
    d.text((cx + 6, cy + 53), src, font=F(SANS, 8), fill=GRAY)
    chip(cx + cw - 4, cy + 52, clab, ccol)

# ---------- WHERE IT HAPPENED strip ----------
d.rectangle([0, 562, W, 580], fill=BLACK)
d.text((8, 566), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=WHITE)

# ---------- map ----------
d.polygon([(18, 640), (60, 600), (110, 610), (125, 660), (105, 720),
           (80, 800), (55, 860), (25, 830), (15, 720)], fill=LGREEN, outline=MGREEN)
d.polygon([(168, 596), (210, 588), (248, 600), (258, 640), (240, 680),
           (200, 690), (172, 660), (162, 625)], fill=LGREEN, outline=MGREEN)
d.polygon([(185, 700), (230, 695), (252, 730), (245, 790), (215, 825),
           (190, 790), (180, 740)], fill=LGREEN, outline=MGREEN)
d.polygon([(262, 600), (320, 595), (340, 640), (335, 720), (300, 760),
           (268, 720), (258, 660)], fill=LGREEN, outline=MGREEN)
pins = {1: (318, 640), 2: (58, 812), 3: (300, 618), 4: (55, 700),
        5: (78, 668), 6: (232, 628), 7: (196, 622), 8: (182, 600),
        9: (222, 604), 10: (168, 622), 11: (246, 676), 12: (230, 716),
        13: (212, 770)}
for n, (px, py) in pins.items():
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE)
    d.text((px, py - 1), str(n), font=F(SANS_B, 9), fill=WHITE, anchor="mm")
d.text((8, 836), "Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing  \u00b7  "
       "4 Washington  \u00b7  5 New York", font=F(SANS, 8), fill=BLACK)
d.text((8, 848), "6 Kyiv  \u00b7  7 Paris  \u00b7  8 London  \u00b7  9 Warsaw  \u00b7  "
       "10 Manchester  \u00b7  11 Beirut", font=F(SANS, 8), fill=BLACK)
d.text((8, 860), "12 Gaza  \u00b7  13 Khartoum", font=F(SANS, 8), fill=BLACK)

# ---------- ALSO ----------
d.text((352, 584), "ALSO ON MONDAY", font=F(SANS_B, 11), fill=BLACK)
also = [
    (14, "Paris: 100+ back 2% billionaire tax", False),
    (15, "Manchester: 12,000 cleared", False),
    (16, "Zelenskyy: 165 missiles in a week", False),
    (17, "COP31: the day after Antalya pact rejected", False),
    (18, "Israel unity talks resume", False),
    (19, "Gaza: two killed in Israeli strike", False),
    (20, "West Bank settler attacks", False),
    (21, "Iran war: no deal in sight", False),
    (22, "Lebanon seizes 264 kg explosives", False),
    (23, "Bahrain: strike hits plant, 2 hurt", False),
    (24, "Benghazi: UN demands probe", True),
    (25, "Sudan: defences down drones", True),
    (26, "DRC: fighting traps Ebola teams", False),
    (27, "Bangladesh: Hasina jailed if she returns", False),
    (28, "Seoul minister quits in exam row", False),
    (29, "SK Telecom -7.3% as hype cools", False),
    (30, "China eases margin rules", False),
    (31, "Seoul readies 10T-won fund", False),
]
for i, (n, txt, is_claim) in enumerate(also):
    col = 0 if i < 9 else 1
    ax = 352 + col * 336
    ay = 604 + (i % 9) * 30
    d.text((ax, ay), f"{n}. {txt}", font=F(SANS, 9), fill=BLACK)
    if is_claim:
        tw = F(SANS, 9).getlength(f"{n}. {txt}")
        d.text((ax + tw + 4, ay), "[CLAIM]", font=F(SANS_B, 9), fill=RED)

# ---------- DATE CHECK ----------
d.rectangle([8, 876, 1016, 938], outline=RED, width=2)
d.text((16, 882), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u2014  "
       "STORIES DATED 23 NOV ONLY", font=F(SANS_B, 11), fill=RED)
left = ("LEFT OUT \u2014 NOT 23 Nov: Dems reach 258 (22 Nov) \u00b7 Sparta II fire "
        "(22 Nov) \u00b7 El Chapo Isidro captured (22 Nov) \u00b7 EU\u2013Indonesia "
        "pact (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar ruling (19 Nov)")
y = 898
for ln in wrap(left, F(SANS, 9), 984):
    d.text((16, y), ln, font=F(SANS, 9), fill=BLACK)
    y += 11
d.text((16, y + 1), "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 "
       "4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating "
       "trapped Ebola staff", font=F(SANS, 9), fill=BLACK)

# ---------- footer ----------
d.text((8, 944), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 "
       "BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
       font=F(SANS, 9), fill=GRAY)
d.text((8, 958), "CHIPS: REPORTED = confirmed by wires \u00b7 CLAIM = one side's claim, "
       "not independently confirmed \u00b7 ONGOING = still developing.",
       font=F(SANS, 9), fill=GRAY)
d.text((8, 972), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn "
       "illustrations, not photographs.", font=F(SANS, 9), fill=GRAY)
d.text((512, 994), "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  "
       "31 stories  \u00b7  6 regions", font=F(SANS_B, 11), fill=GOLD, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
