"""Efectos de sonido sintetizados (deterministas) para videos de marca.

Uso: python -I sfx.py salida.wav DURACION 'JSON'   con JSON = lista de [tiempo, tipo]
Tipos: whoosh (barrido de transición, centrado en el corte), impact (golpe grave),
stamp (sello), pop (aparición), tick (contador/clic), riser (subida de 1.2 s que termina en t),
ding (campana corta).
"""
import json
import sys

import numpy as np
import soundfile as sf

SR = 48000
out_path, DUR, events = sys.argv[1], float(sys.argv[2]), json.loads(sys.argv[3])
N = int(DUR * SR)
mix = np.zeros((N, 2))
rng = np.random.default_rng(11)


def place(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i < 0:
        sig, i = sig[-i:], 0
    if i >= N or len(sig) == 0:
        return
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(sig), 0] += sig * gain * l
    mix[i:i + len(sig), 1] += sig * gain * r


def lp(x, a):
    y = np.zeros_like(x)
    acc = 0.0
    for k in range(len(x)):
        acc = a * acc + (1 - a) * x[k]
        y[k] = acc
    return y


def whoosh():
    n = int(0.7 * SR)
    tt = np.linspace(0, 1, n)
    noise = rng.standard_normal(n)
    env = np.sin(np.pi * tt) ** 2
    # sweep a simple low-pass up then down
    a = 0.985 - 0.12 * np.sin(np.pi * tt)
    y = np.zeros(n)
    acc = 0.0
    for k in range(n):
        acc = a[k] * acc + (1 - a[k]) * noise[k]
        y[k] = acc
    return y / (np.max(np.abs(y)) + 1e-9) * env * 0.8


def impact():
    n = int(1.2 * SR)
    tt = np.arange(n) / SR
    f = 40 + 90 * np.exp(-tt * 18)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 4.5) + rng.standard_normal(n) * np.exp(-tt * 40) * 0.25


def stamp():
    n = int(0.45 * SR)
    tt = np.arange(n) / SR
    thud = np.sin(2 * np.pi * np.cumsum(70 + 160 * np.exp(-tt * 40)) / SR) * np.exp(-tt * 14)
    click = rng.standard_normal(n) * np.exp(-tt * 90) * 0.6
    return thud + click


def pop():
    n = int(0.18 * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(500 + 900 * np.exp(-tt * 60)) / SR) * np.exp(-tt * 30) * 0.6


def tick():
    n = int(0.05 * SR)
    tt = np.arange(n) / SR
    return np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 160) * 0.35


def riser():
    n = int(1.2 * SR)
    tt = np.linspace(0, 1, n)
    sweep = np.sin(2 * np.pi * np.cumsum(220 + 1600 * tt ** 2) / SR) * tt ** 2 * 0.35
    return sweep + lp(rng.standard_normal(n), 0.9) * tt ** 3 * 0.5


def ding():
    n = int(1.0 * SR)
    tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1320 * tt) + 0.5 * np.sin(2 * np.pi * 1980 * tt)) * np.exp(-tt * 5) * 0.35


GEN = {"whoosh": (whoosh, -0.35), "impact": (impact, 0.0), "stamp": (stamp, 0.0), "pop": (pop, 0.0),
       "tick": (tick, 0.0), "riser": (riser, -1.2), "ding": (ding, 0.0)}
cache = {}
for t, kind in events:
    fn, off = GEN[kind]
    if kind not in ("whoosh", "pop", "tick") and kind in cache:
        sig = cache[kind]
    else:
        sig = fn()
        cache[kind] = sig
    place(sig, float(t) + off, 1.0, pan=(0.3 if kind == "whoosh" else 0.0))
peak = np.max(np.abs(mix)) or 1.0
mix = mix / peak * 0.85
sf.write(out_path, mix.astype(np.float32), SR)
print("ok", out_path, len(events), "eventos")
