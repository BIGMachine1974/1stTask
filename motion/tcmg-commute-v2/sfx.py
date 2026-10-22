# Sound design on the same clock as the picture: every cue time matches a spring start in index.html.
import numpy as np, wave
SR, DUR = 48000, 41.5
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

add(0.1, thud(75, .25), 0.4); add(1.95, tick(2000, .02), 0.15)                              # listing card, chip
add(3.42, whoosh(.5), 0.08); add(3.6, thud(80, .22), 0.35)                                      # clock lands
for i in range(8): add(3.8 + i * .125, tick(1500, .01), 0.06)                                   # hands sweep to 8
add(4.65, tick(1800, .02), 0.14); add(5.15, pop(700), 0.2)                                      # chip, question
add(6.1, whoosh(.5), 0.09); add(6.25, thud(65, .25), 0.4)                                       # since July 6
for i in range(5): add(6.9 + i * .12, tick(1200 + i * 100, .02), 0.08)                          # weekday tiles
for i in range(4): add(9.0 + i * .22, pop(700 + i * 120), 0.2)                                  # four days light
add(9.95, thud(90, .15), 0.35)                                                                  # 4 days chip
add(10.75, whoosh(.4), 0.07); add(11.4, whoosh(.45), 0.08)                                      # weekend, strike
add(13.1, whoosh(.45), 0.08); add(13.25, thud(80, .2), 0.3); add(13.9, pop(1100), 0.16)          # distance card, check
add(14.85, thud(80, .2), 0.3)
for i in range(10): add(14.9 + i * .12, tick(1600, .01), 0.05)                                  # clock spins
add(15.35, thud(120, .08), 0.3)                                                                 # x mark
add(16.35, whoosh(.45), 0.08); add(16.45, thud(65, .25), 0.4)                                   # do one test
for t0, c0 in [(19.17, 19.75), (20.31, 21.5), (22.31, 25.7)]: add(t0, whoosh(.4), 0.08); add(c0, pop(1100), 0.16)
add(26.55, whoosh(.5), 0.09); add(26.7, thud(70, .2), 0.35)                                     # route scene
for t0 in [28.6, 29.4, 30.3]: add(t0, whoosh(.5), 0.07); add(t0 + .3, tick(1700), 0.1)          # alternates
add(31.55, thud(60, .3), 0.45); add(32.45, thud(55, .25), 0.4); add(33.4, thud(55, .25), 0.4)   # one honest drive
add(35.25, thud(60, .3), 0.5); add(36.39, thud(50, .35), 0.55)                                  # the line
add(37.65, whoosh(.55), 0.1)
for i in range(19): add(38.15 + i * 1.5 / 19, tick(2600 + (i % 3) * 300, .008), 0.06)           # url typing
add(39.8, pop(900), 0.12)                                                                       # phone

out = out / max(1e-9, np.abs(out).max()) * 0.6
w = wave.open('sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('sfx ok')
