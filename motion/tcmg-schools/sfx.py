# Sound design on the same clock as the picture: every cue time matches a spring start in index.html.
import numpy as np, wave
SR, DUR = 48000, 38.5
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

add(0.15, thud(70, .2), 0.35); add(0.55, thud(65, .2), 0.35); add(1.25, thud(55, .32), 0.55)   # hook lines
add(2.85, whoosh(.45), 0.08)
for i in range(4): add(3.05 + i * .22, pop(700 + i * 120), 0.2)                                  # four boards
add(5.75, thud(90, .18), 0.4)                                                                   # address drops
for i in range(4): add(6.85 + i * .25, tick(1500 + i * 200), 0.12)                              # lines land
add(8.9, whoosh(.5), 0.09); add(9.0, thud(60, .28), 0.4)                                        # half the story
add(11.45, whoosh(.45), 0.08); add(11.55, thud(75, .25), 0.4)                                   # school rises
for i in range(28): add(12.0 + i * 1.9 / 28, tick(1100 + i * 25, .01), 0.05)                     # counter
add(14.9, whoosh(.6), 0.08)                                                                     # over capacity
for i in range(17): add(15.0 + i * .11, tick(1300 + (i % 4) * 150, .02), 0.1)                   # portables
add(17.0, thud(55, .35), 0.55)                                                                  # 17 PORTABLES slam
add(18.15, whoosh(.5), 0.09); add(19.8, thud(70, .3), 0.45)                                     # outline becomes school
add(20.35, thud(120, .08), 0.35); add(20.36, tick(900, .01), 0.2)                               # stamp
add(21.55, whoosh(.45), 0.08); add(21.65, thud(65, .25), 0.4)                                   # kitchen line
add(24.75, whoosh(.45), 0.09); add(26.9, whoosh(.45), 0.09)                                     # question cards
add(29.4, pop(1100), 0.18); add(30.0, pop(1300), 0.18)                                          # checks
add(31.8, thud(60, .3), 0.5); add(33.05, thud(50, .35), 0.6)                                    # the line
add(34.7, whoosh(.5), 0.09)
for i in range(19): add(35.55 + i * 0.9 / 19, tick(2600 + (i % 3) * 300, .008), 0.06)           # url typing

out = out / max(1e-9, np.abs(out).max()) * 0.6
w = wave.open('sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('sfx ok')
