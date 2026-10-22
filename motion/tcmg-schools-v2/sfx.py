# Sound design on the same clock as the picture: every cue time matches a spring start in index.html.
import numpy as np, wave
SR, DUR = 48000, 39.5
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

add(0.15, thud(70, .2), 0.35); add(1.15, thud(65, .2), 0.35); add(2.1, thud(55, .32), 0.55)   # hook lines
add(3.05, whoosh(.45), 0.08)
for i in range(4): add(3.75 + i * .2, pop(700 + i * 120), 0.2)                                   # four boards
add(5.35, thud(90, .18), 0.4)                                                                   # address drops
for i in range(4): add(6.45 + i * .25, tick(1500 + i * 200), 0.12)                              # lines land, tiles light
add(8.1, whoosh(.5), 0.09); add(8.2, thud(60, .28), 0.4)                                        # half the story
add(11.1, whoosh(.45), 0.08); add(11.25, thud(75, .25), 0.4)                                    # school rises
for i in range(26): add(13.4 + i * 1.5 / 26, tick(1100 + i * 25, .01), 0.05)                     # counter to 674
add(16.0, whoosh(.6), 0.08)                                                                     # over capacity
for i in range(17): add(17.25 + i * .07, tick(1300 + (i % 4) * 150, .02), 0.1)                  # portables
add(18.0, thud(55, .35), 0.5)                                                                   # 17 PORTABLES
add(19.7, whoosh(.5), 0.09); add(22.65, thud(70, .3), 0.45)                                     # outline becomes school
add(23.2, thud(120, .08), 0.35); add(23.21, tick(900, .01), 0.2)                                # stamp
add(24.35, whoosh(.45), 0.08); add(24.45, thud(65, .25), 0.4)                                   # kitchen line
add(28.53, whoosh(.45), 0.09); add(30.79, whoosh(.45), 0.09)                                    # question cards
add(30.3, pop(1100), 0.18); add(33.2, pop(1300), 0.18)                                          # checks
add(34.0, thud(60, .3), 0.5); add(35.06, thud(50, .35), 0.55)                                   # the line
add(36.0, whoosh(.55), 0.1)                                                                     # end card wipe
for i in range(19): add(36.55 + i * 1.5 / 19, tick(2600 + (i % 3) * 300, .008), 0.06)           # url typing
add(38.3, pop(900), 0.12)                                                                       # phone

out = out / max(1e-9, np.abs(out).max()) * 0.6
w = wave.open('sfx.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close(); print('sfx ok')
