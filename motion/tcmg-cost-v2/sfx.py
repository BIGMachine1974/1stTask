# Sound design on the same clock as the picture: every cue time matches a spring start in index.html.
import numpy as np, wave
SR, DUR = 48000, 42.0
out = np.zeros(int(SR * DUR))
rng = np.random.default_rng(7)

def add(t, sig, gain):
    i = int(t * SR); n = min(len(sig), len(out) - i); out[i:i + n] += sig[:n] * gain

def env(n, a=0.003, d=0.08):
    tt = np.arange(n) / SR; return np.minimum(1, tt / a) * np.exp(-tt / d)

def tick(f=1800, d=0.03):   # small UI snap
    n = int(SR * 0.12); tt = np.arange(n) / SR; return np.sin(2 * np.pi * f * tt) * env(n, .001, d)

def thud(f=70, d=0.18):     # weight landing
    n = int(SR * 0.6); tt = np.arange(n) / SR; fr = f * (1 + 1.5 * np.exp(-tt / 0.03))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, .002, d)

def whoosh(d=0.45):
    n = int(SR * d); w = rng.standard_normal(n); k = np.linspace(0, 1, n)
    return np.convolve(w, np.ones(24) / 24, 'same') * np.sin(np.pi * k) ** 2

def pop(f=900):
    n = int(SR * 0.15); tt = np.arange(n) / SR; fr = f * (1 + 0.8 * np.exp(-tt / 0.02))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, .001, .04)

add(0.1, thud(70, .2), 0.35); add(0.75, thud(65, .2), 0.35); add(1.35, thud(55, .32), 0.5)   # question lands
add(2.8, whoosh(.45), 0.08); add(2.95, thud(80, .25), 0.4)                                      # tag lands
for i in range(30): add(5.6 + i * 3.0 / 30, tick(1100 + i * 20, .01), 0.05)                      # count to 623,500
add(9.3, thud(120, .08), 0.35); add(9.31, tick(900, .01), 0.2)                                  # 2.2% chip
add(11.8, whoosh(.5), 0.09); add(12.1, pop(800), 0.18)                                          # second tag
for i in range(26): add(13.0 + i * 2.6 / 26, tick(1300 + i * 20, .01), 0.05)                     # count to 685,640
add(16.15, pop(1100), 0.18)                                                                     # gap bracket
for k, t0 in enumerate([17.35, 17.6, 17.85]): add(t0, thud(90 - k * 15, .18), 0.35)              # big sales drop
add(19.75, tick(2200, .02), 0.15)                                                               # benchmark lights
add(23.5, whoosh(.5), 0.09); add(23.6, thud(65, .25), 0.4); add(24.0, whoosh(.4), 0.06)          # map
for t0 in [26.13, 28.96, 32.36]: add(t0, thud(110, .12), 0.35); add(t0 + .2, tick(1700), 0.1)   # pins
add(35.45, thud(60, .3), 0.45); add(35.75, thud(55, .3), 0.45); add(36.97, thud(50, .35), 0.5)  # the line
add(38.24, whoosh(.55), 0.1)
for i in range(19): add(38.75 + i * 1.6 / 19, tick(2600 + (i % 3) * 300, .008), 0.06)           # url typing
add(40.5, pop(900), 0.12)                                                                       # phone

out = out / max(1e-9, np.abs(out).max()) * 0.6
w = wave.open('sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('sfx ok')
