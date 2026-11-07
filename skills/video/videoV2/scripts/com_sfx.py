"""Efectos de comedia sintetizados (deterministas): rimshot, applause, scratch, boing, más whoosh/impact/ding/pop/riser/type.
Uso: python com_sfx.py salida.wav DURACION eventos.json   (eventos = [[t, tipo], ...])"""
import json
import sys

import numpy as np
import soundfile as sf

SR = 48000
out_path, DUR, ev = sys.argv[1], float(sys.argv[2]), json.load(open(sys.argv[3]))
N = int(DUR * SR)
mix = np.zeros((N, 2))
rng = np.random.default_rng(5)


def T(d):
    return np.arange(int(d * SR)) / SR


def place(x, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i < 0:
        x, i = x[-i:], 0
    if i >= N:
        return
    x = x[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    mix[i:i + len(x), 0] += x * g * l
    mix[i:i + len(x), 1] += x * g * r


def onepole(x, a):
    y = np.empty_like(x)
    acc = 0.0
    for k in range(len(x)):
        acc = a * acc + (1 - a) * x[k]
        y[k] = acc
    return y


def hp(x, a):
    return x - onepole(x, a)


def snare(d=0.25):
    t = T(d)
    n = rng.standard_normal(len(t)) * np.exp(-t * 22)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.6
    return hp(n, 0.6) * 0.7 + body


def cymbal(d=1.4):
    t = T(d)
    n = hp(rng.standard_normal(len(t)), 0.15) * np.exp(-t * 3.2)
    return n * 0.5


def rimshot():
    out = np.zeros(int(1.8 * SR))
    for k, (t0, g) in enumerate([(0.0, 0.8), (0.16, 1.0)]):
        s = snare()
        i = int(t0 * SR)
        out[i:i + len(s)] += s * g
    c = cymbal()
    i = int(0.42 * SR)
    out[i:i + len(c)] += c[: len(out) - i]
    k = np.sin(2 * np.pi * 55 * T(0.3)) * np.exp(-T(0.3) * 14)
    out[i:i + len(k)] += k * 0.8
    return out


def applause(d=2.6):
    t = T(d)
    env = np.minimum(1, t / 0.25) * np.exp(-np.maximum(0, t - 1.4) * 2.2)
    out = np.zeros(len(t))
    for _ in range(420):
        c = rng.uniform(0, d - 0.05)
        i = int(c * SR)
        L = int(0.012 * SR)
        clap = rng.standard_normal(L) * np.exp(-np.arange(L) / SR * 400)
        out[i:i + L] += clap * rng.uniform(0.3, 1)
    out = hp(out, 0.5) * env
    return out / np.max(np.abs(out)) * 0.8


def scratch():
    t = T(0.55)
    f = 300 + 900 * np.abs(np.sin(2 * np.pi * 3.2 * t))
    ph = np.cumsum(f) / SR
    n = rng.standard_normal(len(t))
    tone = np.sign(np.sin(2 * np.pi * ph)) * 0.3 + onepole(n, 0.7) * 0.8
    env = np.minimum(1, t / 0.02) * np.exp(-t * 2)
    return hp(tone, 0.4) * env


def boing():
    t = T(0.9)
    f = 140 + 260 * np.exp(-t * 5) + 25 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 2)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2) * 0.9


def whoosh():
    t = T(0.6)
    n = rng.standard_normal(len(t))
    env = np.sin(np.pi * t / 0.6) ** 2
    a = 0.97 - 0.5 * env
    y = np.zeros_like(n)
    acc = 0.0
    for k in range(len(n)):
        acc = a[k] * acc + (1 - a[k]) * n[k]
        y[k] = acc
    return y * env * 1.4


def impact():
    t = T(1.4)
    f = 40 + 80 * np.exp(-t * 8)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3) + rng.standard_normal(len(t)) * np.exp(-t * 25) * 0.25


def ding():
    t = T(1.2)
    return (np.sin(2 * np.pi * 1320 * t) + 0.5 * np.sin(2 * np.pi * 2640 * t) + 0.25 * np.sin(2 * np.pi * 3960 * t)) * np.exp(-t * 4) * 0.35


def pop():
    t = T(0.12)
    f = 900 - 500 * t / 0.12
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35) * 0.6


def riser():
    t = T(1.4)
    n = hp(rng.standard_normal(len(t)), 0.3) * (t / 1.4) ** 2 * 0.25
    s = np.sin(2 * np.pi * np.cumsum(300 + 1500 * (t / 1.4) ** 2) / SR) * (t / 1.4) ** 3 * 0.15
    return n + s


def typ():
    t = T(0.04)
    return hp(rng.standard_normal(len(t)), 0.3) * np.exp(-t * 160) * 0.5


FX = dict(rimshot=(rimshot, 0.75), applause=(applause, 0.6), scratch=(scratch, 0.6), boing=(boing, 0.6), whoosh=(whoosh, 0.35),
          impact=(impact, 0.7), ding=(ding, 0.5), pop=(pop, 0.35), riser=(riser, 0.5), type=(typ, 0.25))
cache = {}
for t, kind in ev:
    fn, g = FX[kind]
    if kind not in cache or kind in ("applause", "scratch", "whoosh"):
        cache[kind] = fn()
    x = cache[kind]
    if kind == "riser":
        t = t - len(x) / SR
    if kind == "whoosh":
        t = t - 0.3
    place(x, t, g, pan=(0.15 if kind in ("pop", "type") else 0.0))
pk = np.max(np.abs(mix))
if pk > 0:
    mix = mix / pk * 0.9
sf.write(out_path, mix.astype(np.float32), SR)
print("ok", len(ev), "eventos")
