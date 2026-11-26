#!/usr/bin/env python3
"""og.png 1200x630 — Namit Filipino Barbecue hero art. Charcoal ground, grill-grate lines
top, ember radial glow bottom-right, big serif wordmark, ember rule, address line.
Drawn backdrop first, text on top = guaranteed legibility. Machine guards: every text
bbox inside margins; the pixel band behind each text line stays dark. Copy = verified facts only.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'public', 'og.png')
W, H = 1200, 630
CHAR, CHAR_DEEP = (22, 18, 16), (14, 10, 8)
EMBER, EMBER_HI = (232, 87, 31), (255, 122, 60)
CREAM, MUTED, LEAF = (245, 237, 226), (199, 180, 159), (143, 174, 107)

def F(size, serif=False, italic=False, bold=False):
    cands = []
    if serif:
        cands = [f"/System/Library/Fonts/Supplemental/Times New Roman{' Italic' if italic else (' Bold' if bold else '')}.ttf",
                 "/System/Library/Fonts/Times.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
    else:
        cands = [f"/usr/local/share/fonts/Inter-{('Bold' if bold else 'Medium')}.ttf",
                 f"/System/Library/Fonts/Supplemental/Arial{' Bold' if bold else ''}.ttf",
                 "/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for c in cands:
        if os.path.exists(c):
            try: return ImageFont.truetype(c, size)
            except Exception: pass
    return ImageFont.load_default()

img = Image.new('RGB', (W, H), CHAR)
d = ImageDraw.Draw(img)

# backdrop: deeper floor + grate lines + ember glow bottom-right
d.rectangle([0, 430, W, H], fill=CHAR_DEEP)
for y in range(0, 430, 26):
    d.line([0, y, W, y], fill=(36, 29, 25), width=2)
for step, col in [(9, (28, 20, 15)), (7, (33, 23, 17)), (5, (44, 28, 18))]:
    cx, cy, r = 1080, 560, step * 60
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
for x0, x1, y0 in [(0, W, 430)]:
    for yy in range(y0, H, 26):
        d.line([0, yy, W, yy], fill=(26, 18, 13), width=2)

# ember bar top
d.rectangle([0, 0, W, 8], fill=EMBER)

texts = []  # (text, font, xy, fill, anchor) for guard checks
errs = []
MARGIN = 60
def put(t, font, xy, fill, anchor='la'):
    box = d.textbbox(xy, t, font=font, anchor=anchor)
    x0, y0, x1, y1 = box
    if x0 < MARGIN - 6 or x1 > W - MARGIN:
        errs.append(f"TEXT WIDTH OUT OF MARGIN: {t[:30]!r} bbox=({x0},{y1})")
    if y1 > H - 20 or y0 < 20:
        errs.append(f"TEXT OUT OF CANVAS: {t[:30]!r}")
    # sample the GROUND (before drawing) behind the text band: must stay dark for legibility
    band = img.crop((max(0, x0), max(0, y0 - 6), min(W, x1), min(H, y1 + 6)))
    small = band.resize((min(60, band.width), min(8, band.height)))
    lum = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b, *_ in small.getdata()]
    if lum and max(lum) > 120:
        errs.append(f"GROUND TOO BRIGHT BEHIND: {t[:30]!r} max_luma={max(lum):.0f}")
    texts.append((t, font, xy, fill, anchor))
    d.text(xy, t, font=font, fill=fill, anchor=anchor)

put("HALIN SA BACOLOD!  ·  NOW GRILLING IN COLUMBIA, MD", F(21, bold=True), (90, 96), LEAF)
put("NAMIT", F(168, serif=True, bold=True), (88, 140), CREAM)
put("Filipino Barbecue", F(64, serif=True, italic=True), (92, 330), EMBER_HI)
d.line([92, 428, 720, 428], fill=EMBER, width=4)
put("Inasal  ·  Sisig  ·  Lumpia  ·  Pancit  ·  Lechon", F(26), (92, 448), CREAM)
put("9200 Old Annapolis Road, Columbia, MD 21045   ·   (443) 774-8969", F(22), (92, 540), MUTED)

img.save(OUT, 'PNG', optimize=True)

# ---- guard verdict (errors collected inline in put()) ----
if errs:
    print("OG GUARD FAIL:")
    [print(' ', e) for e in errs]
    raise SystemExit(1)
print(f"OG OK {OUT} {os.path.getsize(OUT)} B, {len(texts)} guarded text lines")
