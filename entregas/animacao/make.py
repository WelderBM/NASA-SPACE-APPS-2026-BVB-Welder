"""30-second motion piece for Field Shift Roraima. Draws frames with PIL, one mp4 per scene."""
import subprocess, sys, os, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
F = '/usr/share/fonts/opentype/inter/'
def font(name, size): return ImageFont.truetype(F + name, size)
DISP = lambda s: font('InterDisplay-Bold.otf', s)
XB = lambda s: font('InterDisplay-ExtraBold.otf', s)
SB = lambda s: font('Inter-SemiBold.otf', s)
RG = lambda s: font('Inter-Regular.otf', s)

SOIL = (28, 38, 32); PAPER = (245, 240, 230); PAPER2 = (234, 227, 211)
OCHRE = (217, 144, 47); LEAF = (46, 106, 76); INK2 = (74, 81, 72); MIST = (201, 211, 198)
BUB = (37, 52, 43); LIGHTOCHRE = (233, 182, 106); RED = (176, 72, 48)

def ease(t):  # easeOutCubic clipped
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def mix(c1, c2, a): return tuple(int(c1[i] + (c2[i] - c1[i]) * a) for i in range(3))

class Canvas:
    def __init__(self, bg):
        self.bg = bg; self.im = Image.new('RGB', (W, H), bg); self.d = ImageDraw.Draw(self.im)
    def text(self, xy, s, f, col, a=1.0, dy=0, anchor='la', spacing=10):
        if a <= 0: return
        x, y = xy
        self.d.multiline_text((x, y + dy), s, font=f, fill=mix(self.bg, col, a), anchor=anchor, spacing=spacing)
    def rrect(self, box, r, fill, a=1.0, outline=None, width=0):
        if a <= 0: return
        self.d.rounded_rectangle(box, r, fill=mix(self.bg, fill, a) if fill else None,
                                 outline=mix(self.bg, outline, a) if outline else None, width=width)

def fade_in(t, start, dur=0.5): return ease((t - start) / dur)
def fade_io(t, start, end, dur=0.4): return min(ease((t - start) / dur), ease((end - t) / dur))

def watermark(c, light):
    col = MIST if light else INK2
    c.text((W - 64, H - 48), 'AI-generated with Claude (Anthropic)', SB(22), col, anchor='rs')

# ---------------- scenes ----------------
def s1(t):  # 2.0 s team
    c = Canvas(SOIL)
    a = fade_in(t, 0.0, 0.5); dy = int((1 - a) * 30)
    c.text((160, 380), 'NASA SPACE APPS 2026', SB(30), OCHRE, a, dy)
    b = fade_in(t, 0.25, 0.5); dy2 = int((1 - b) * 30)
    c.text((160, 440), 'Welder Barroso', XB(110), PAPER, b, dy2)
    c.text((160, 590), 'Boa Vista, Roraima, Brazil', RG(48), MIST, fade_in(t, 0.5, 0.5))
    watermark(c, True); return c.im

def s2(t):  # 3.0 s challenge
    c = Canvas(SOIL)
    c.text((160, 200), 'CHALLENGE: FIELD SHIFT, ADAPTING FARMS WITH NASA DATA', SB(30), OCHRE, fade_in(t, 0.0))
    a = fade_in(t, 0.3, 0.6)
    # count-up of -62%
    v = int(round(62 * ease((t - 0.3) / 1.2)))
    c.text((160, 300), f'−{v}%', XB(260), LIGHTOCHRE, a)
    c.text((160, 620), 'June to September rain in Cantá, Roraima, 2026.\nThe worst in 45 years of NASA POWER data.',
           RG(52), PAPER, fade_in(t, 0.9, 0.6), spacing=16)
    c.text((160, 820), 'Then the soil went into the dry season five months early.', SB(40), MIST, fade_in(t, 1.6, 0.6))
    watermark(c, True); return c.im

def s3(t):  # 5.0 s slogan
    c = Canvas(PAPER)
    a = fade_in(t, 0.0, 0.6)
    c.text((160, 300), 'You just harvested.', XB(130), SOIL, a, int((1 - a) * 30))
    b = fade_in(t, 0.8, 0.6)
    c.text((160, 460), 'What do you plant next?', XB(130), LEAF, b, int((1 - b) * 30))
    c.text((160, 680), 'A conversation, by voice or text, that compares what to plant\nafter the harvest a small farmer just made.',
           RG(46), INK2, fade_in(t, 1.8, 0.7), spacing=14)
    watermark(c, False); return c.im

CHIPS = ['Better soil', 'Low risk', 'Food at home', 'Pasture']
def chip_row(c, x, y, active, a):
    for name in CHIPS:
        f = SB(34); w = int(c.d.textlength(name, font=f)) + 56
        on = (name == active)
        c.rrect((x, y, x + w, y + 70), 35, LEAF if on else PAPER, a, outline=None if on else INK2, width=0 if on else 3)
        c.text((x + 28, y + 14), name, f, PAPER if on else INK2, a)
        x += w + 18
    f = SB(34); name = 'Income: it says it doesn’t know'
    w = int(c.d.textlength(name, font=f)) + 56
    c.rrect((x, y, x + w, y + 70), 35, PAPER2, a, outline=MIST, width=3)
    c.text((x + 28, y + 14), name, f, INK2, a)

def s4(t):  # 10.0 s how it works
    c = Canvas(PAPER)
    c.text((160, 110), 'HOW IT WORKS', SB(30), LEAF, fade_in(t, 0))
    c.text((160, 160), 'Harvested cassava in Cantá. What comes next?', DISP(68), SOIL, fade_in(t, 0.1))
    c.text((160, 270), 'The farmer chooses what to optimize:', RG(38), INK2, fade_in(t, 0.4))
    active = 'Low risk' if t < 5.0 else 'Better soil'
    chip_row(c, 160, 340, active, fade_in(t, 0.6))
    # answer bubble
    if t < 5.0:
        a = fade_io(t, 1.4, 5.0); who = 'Priority: low risk'
        say = '“Cowpea. It’s quick, out of the ground in 60 days.”'
    else:
        a = fade_io(t, 5.2, 10.4); who = 'Same harvest, same place. Priority: better soil'
        say = '“It leaves the soil stronger for what comes next.”'
    c.rrect((160, 470, 1760, 680), 28, SOIL, a)
    c.text((210, 505), who, SB(32), OCHRE, a)
    c.text((210, 565), say, DISP(56), PAPER, a)
    # NASA data ribbon
    r = fade_in(t, 2.4, 0.6)
    c.rrect((160, 740, 1760, 900), 24, PAPER2, r)
    c.text((210, 765), 'Computed from NASA POWER for that coordinate:', SB(32), LEAF, r)
    c.text((210, 820), 'rain  ·  root-zone soil moisture  ·  this year against 45 years', RG(40), SOIL, r)
    watermark(c, False); return c.im

def s5(t):  # 9.5 s validity + future
    if t < 4.6:
        c = Canvas(PAPER2)
        c.text((160, 120), 'SAME CODE, OPPOSITE ANSWERS', SB(30), LEAF, fade_in(t, 0))
        c.text((160, 170), 'Maize, same 500 mm need, two places', DISP(68), SOIL, fade_in(t, 0.1))
        cols = [(160, 'Cantá, Roraima', 'April planting', 1.24, 'Water risk: LOW', LEAF),
                (1000, 'Rio Verde, Goiás', 'September planting', 0.66, 'Water risk: HIGH', RED)]
        for i, (x, place, when, ratio, verdict, col) in enumerate(cols):
            a = fade_in(t, 0.5 + i * 0.4)
            c.text((x, 320), place, DISP(56), SOIL, a)
            c.text((x, 395), when, RG(36), INK2, a)
            full = 700; bw = int(full * min(ratio / 1.4, 1.0) * ease((t - 0.8 - i * 0.4) / 1.2))
            c.rrect((x, 470, x + full, 540), 14, PAPER, a)
            if bw > 20: c.rrect((x, 470, x + bw, 540), 14, col, a)
            c.text((x, 560), f'{ratio:.2f}× the water it needs, this year', RG(34), INK2, a)
            c.text((x, 630), verdict, XB(60), col, fade_in(t, 1.8 + i * 0.4))
        c.text((160, 800), 'No location-specific code. The NASA data decides.', SB(40), SOIL, fade_in(t, 2.8))
        out = 1 - ease((t - 4.2) / 0.4)
        if out < 1:
            ov = Image.new('RGB', (W, H), SOIL); c.im = Image.blend(ov, c.im, out)
        watermark(Canvas(PAPER2), False)
        im = c.im; d = ImageDraw.Draw(im)
        d.text((W - 64, H - 48), 'AI-generated with Claude (Anthropic)', font=SB(22), fill=INK2, anchor='rs')
        return im
    u = t - 4.6
    c = Canvas(SOIL)
    c.text((160, 170), 'It won’t tell a farmer what to do.', XB(84), PAPER, fade_in(u, 0.0))
    c.text((160, 290), 'It shows what each choice does to the soil, this year.\nAnd it says what it doesn’t know.',
           DISP(64), LIGHTOCHRE, fade_in(u, 0.5), spacing=18)
    c.text((160, 560), 'NEXT', SB(30), OCHRE, fade_in(u, 1.4))
    c.text((160, 610), 'Official ZARC planting windows  ·  FAO ECOCROP crop traits\nWhatsApp on the same engine  ·  field tests with Roraima extension agents',
           RG(42), MIST, fade_in(u, 1.6), spacing=16)
    c.text((160, 860), 'github.com/WelderBM/NASA-SPACE-APPS-2026-BVB-Welder', SB(36), PAPER, fade_in(u, 2.4))
    watermark(c, True); return c.im

SCENES = [('s1', s1, 2.0), ('s2', s2, 3.0), ('s3', s3, 5.0), ('s4', s4, 10.0), ('s5', s5, 9.5)]

def render(name, fn, dur):
    n = int(round(dur * FPS)); tmp = f'{name}.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                          '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(fn(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, f'{name}.mp4')
    else: sys.exit(f'{name} failed')

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if mode == 'stills':
        for name, fn, t in [('s2', s2, 2.5), ('s3', s3, 4.5), ('s4', s4, 4.0), ('s4b', s4, 8.0), ('s5', s5, 3.5), ('s5b', s5, 8.5)]:
            fn(t).save(f'still_{name}.png')
    else:
        for name, fn, dur in SCENES: render(name, fn, dur)
        open('list.txt', 'w').write(''.join(f"file '{n}.mp4'\n" for n, _, _ in SCENES))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy',
                        'field-shift-roraima-30s.mp4'], check=True)
