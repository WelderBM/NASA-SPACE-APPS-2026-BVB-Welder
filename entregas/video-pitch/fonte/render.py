"""Render scene.html frame by frame with headless Chrome, encode, add narration + light music."""
import json, subprocess, sys, os
from playwright.sync_api import sync_playwright

FPS = 30
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 29.9
mode = sys.argv[1] if len(sys.argv) > 1 else 'video'
timing = json.load(open('/home/claude/tts/timing_af_heart.json'))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--force-device-scale-factor=1'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto('file:///home/claude/film/scene.html')
    pg.evaluate('t => setSubs(t.phrases, t)', timing)
    if mode == 'stills':
        for t in [float(x) for x in sys.argv[3].split(',')]:
            pg.evaluate(f'render({t})')
            pg.screenshot(path=f'still_{t:05.2f}.jpg', type='jpeg', quality=90)
    else:
        n = int(round(DUR * FPS)); tmp = 'video.tmp.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-r', str(FPS), '-i', '-',
                               '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
        for i in range(n):
            pg.evaluate(f'render({i / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
        ff.stdin.close()
        if ff.wait() == 0: os.replace(tmp, 'video.mp4')
        else: sys.exit('encode failed')
    b.close()
