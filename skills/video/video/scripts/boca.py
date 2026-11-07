"""Envolvente de apertura de boca (0..1, 30 fps) a partir de la voz, para lip-sync de mascotas.

Uso: python -I boca.py voz.wav salida.json [duracion_seg]
En la composición: const MOUTH = <json>; apertura en t = interpolar MOUTH[t*30].
Aplicarla en el onUpdate de un tween proxy {t:0}->{t:DUR} (determinista y seekable):
scaleY del grupo de boca abierta = o, opacidad de la sonrisa cerrada = 1 - 4*o.
"""
import json
import sys

import numpy as np
import soundfile as sf

src, dst = sys.argv[1], sys.argv[2]
x, sr = sf.read(src)
if x.ndim > 1:
    x = x.mean(1)
dur = float(sys.argv[3]) if len(sys.argv) > 3 else len(x) / sr
hop = sr // 30
n = int(dur * 30)
rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(x) else 0 for i in range(n)])
ref = np.percentile(rms[rms > 1e-4], 97)
o = np.clip(rms / ref, 0, 1) ** 1.6
o[rms < 0.015] = 0
slow = np.convolve(o, np.ones(9) / 9, mode="same")
o = np.clip(o * 0.55 + np.clip(o - slow * 0.6, 0, 1) * 1.1, 0, 1)  # resalta sílabas
env, a = np.zeros_like(o), 0.0
for i, v in enumerate(o):
    a = v if v > a else a * 0.4 + v * 0.6  # abre rápido, cierra suave
    env[i] = a
json.dump([round(float(v), 2) for v in env], open(dst, "w"))
print(f"{n} frames, boca abierta {float((env > 0.15).mean()):.0%} del tiempo (ideal 50-65%)")
