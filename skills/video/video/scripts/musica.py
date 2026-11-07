"""Cama musical electrónica cinematográfica sintetizada (determinista).

Uso: python -I musica.py salida.wav DURACION "0,6.5,15,27,42,52"
- DURACION: segundos totales del video.
- Lista: inicios de escena; cada uno recibe un golpe grave y el último es el clímax.
La batería entra en la escena 3, hay un respiro al inicio de la penúltima escena y un riser hacia el clímax.
"""
import sys
import numpy as np
import soundfile as sf

SR = 48000
DUR = float(sys.argv[2])
N = int(SR * DUR)
t = np.arange(N) / SR
rng = np.random.default_rng(7)
out = np.zeros((N, 2))

BPM = 110
BEAT = 60 / BPM
SCENES = [float(v) for v in sys.argv[3].split(",")]
BRK0, BRK1 = SCENES[-2], SCENES[-2] + 3.5  # respiro (sin bombo) al entrar a la penúltima escena
RIS0 = max(BRK1, SCENES[-1] - 7.5)

def midi(m):
    return 440 * 2 ** ((m - 69) / 12)

def env_seg(n, a, r):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return e

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    out[i:i + len(sig), 0] += sig * gain * l
    out[i:i + len(sig), 1] += sig * gain * r

# Global intensity curve per section
def intensity(x):
    S = SCENES + [DUR] * (6 - len(SCENES))
    pts = [(0, .35), (S[1], .5), (S[2], .65), (S[3], .8), (S[-2], .75), (S[-1] - .65, .95), (S[-1], 1.0), (DUR - 2, .8), (DUR, 0)]
    xs, ys = zip(*pts)
    return np.interp(x, xs, ys)

# 1) Pad: progression Am  F  C  G (2 bars each), detuned sines + soft fifth
prog = [[57, 60, 64, 69], [53, 57, 60, 65], [55, 60, 64, 67], [55, 59, 62, 67]]
bar = BEAT * 4
seg = bar * 2
k = 0; s = 0.0
while s < DUR:
    chord = prog[k % 4]; n = int(seg * SR); tt = np.arange(n) / SR
    sig = np.zeros(n)
    for m in chord:
        for d in (-0.08, 0.0, 0.08):
            sig += np.sin(2 * np.pi * midi(m) * (1 + d / 100) * tt + rng.uniform(0, 6))
    sig *= env_seg(n, 1.2, 1.2) / 12
    add(sig, s, 0.55); s += seg; k += 1

# 2) Sub drone on A1
drone = np.sin(2 * np.pi * 55 * t) * 0.18 + np.sin(2 * np.pi * 110 * t) * 0.05
out[:, 0] += drone; out[:, 1] += drone

# 3) Arp (from scene 2): sixteenth plucks over chord tones
step = BEAT / 2
s = SCENES[1]; i = 0
while s < DUR - 1:
    chord = prog[int(s // seg) % 4]
    m = chord[[0, 2, 1, 3, 2, 1][i % 6]] + 12
    n = int(0.22 * SR); tt = np.arange(n) / SR
    pl = (np.sin(2 * np.pi * midi(m) * tt) + 0.3 * np.sin(4 * np.pi * midi(m) * tt)) * np.exp(-tt * 14)
    add(pl, s, 0.09 * (0.6 + 0.4 * intensity(s)), pan=0.5 if i % 2 else -0.5)
    s += step; i += 1

# 4) Kick from scene 3, hats from scene 4
def kick():
    n = int(0.45 * SR); tt = np.arange(n) / SR
    f = 45 + 110 * np.exp(-tt * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
def hat():
    n = int(0.06 * SR); tt = np.arange(n) / SR
    return np.diff(rng.standard_normal(n + 1)) * np.exp(-tt * 70)
K, H = kick(), hat()
s = SCENES[min(2, len(SCENES) - 1)]
while s < DUR - 0.9:
    if not (BRK0 <= s < BRK1):  # breakdown at scene 5 start
        add(K, s, 0.42 * intensity(s))
    s += BEAT
s = SCENES[min(3, len(SCENES) - 1)] + BEAT / 2
while s < DUR - 0.9:
    if not (BRK0 <= s < BRK1):
        add(H, s, 0.05)
    s += BEAT

# 5) Riser into the climax (46 → 53.65)
r0, r1 = RIS0, SCENES[-1]
n = int((r1 - r0) * SR); tt = np.arange(n) / SR
noise = rng.standard_normal(n) * (tt / tt[-1]) ** 2 * 0.06
sweep = np.sin(2 * np.pi * np.cumsum(200 + 1400 * (tt / tt[-1]) ** 2) / SR) * (tt / tt[-1]) ** 3 * 0.05
add(noise + sweep, r0)

# 6) Impacts on scene changes (deep boom + noise burst)
def impact(big):
    n = int(2.5 * SR); tt = np.arange(n) / SR
    f = 32 + 70 * np.exp(-tt * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (1.6 if big else 3))
    burst = rng.standard_normal(n) * np.exp(-tt * 18) * 0.25
    return boom + burst
SUAVE = len(sys.argv) > 4 and sys.argv[4] == "suave"  # suave: solo el golpe del clímax, sin golpes por escena
for i, sc in enumerate(SCENES):
    big = i in (0, len(SCENES) - 1)
    if SUAVE and i != len(SCENES) - 1:
        continue
    add(impact(big), sc, (0.35 if SUAVE else 0.55) if big else 0.32)

# Master: intensity envelope, fade out, normalize to about -16 LUFS-ish peak
out *= intensity(t)[:, None]
fo = int(2.0 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None]
out /= np.max(np.abs(out)) / 0.7
sf.write(sys.argv[1], out.astype(np.float32), SR)
print("ok", sys.argv[1])
