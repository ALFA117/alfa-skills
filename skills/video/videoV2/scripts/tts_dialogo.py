"""Voz con varios personajes (edge-tts): genera cada réplica, recorta silencios y arma <proyecto>/assets/voz.wav + lineas.json.
Uso: python tts_dialogo.py <carpeta_proyecto> [--start 3.4] [--outro 7.5]
El proyecto debe tener guion.py con VOCES = {clave: dict(voice, rate, pitch, name)} y
ESCENAS = [dict(id, lines=[(clave, texto_hablado, subtitulo, sfx_o_None), ...]), ...].
Las tomas se guardan en <proyecto>/_tts y solo se regeneran las que cambian."""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

sys.stdout.reconfigure(encoding="utf-8")
import argparse  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("proyecto")
ap.add_argument("--start", type=float, default=3.4)
ap.add_argument("--outro", type=float, default=7.5)
ARGS = ap.parse_args()
HERE = os.path.abspath(ARGS.proyecto)
sys.path.insert(0, HERE)
from guion import ESCENAS, VOCES  # noqa: E402

TMP = os.path.join(HERE, "_tts")
os.makedirs(TMP, exist_ok=True)
SR = 48000
START = ARGS.start   # el gancho visual corre antes de la primera voz
GAP = 0.14           # entre réplicas
GAP_SFX = 0.6        # después de un remate con efecto
GAP_SCENE = 0.35     # extra al cambiar de escena


def tts(i, who, text):
    v = VOCES[who]
    mp3, wav = os.path.join(TMP, f"l{i:02d}.mp3"), os.path.join(TMP, f"l{i:02d}.wav")
    key = os.path.join(TMP, f"l{i:02d}.txt")
    sig = f'{v["voice"]}|{v["rate"]}|{v["pitch"]}|{text}'
    if not (os.path.exists(wav) and os.path.exists(key) and open(key, encoding="utf-8").read() == sig):
        subprocess.run([sys.executable, "-m", "edge_tts", "--voice", v["voice"], f"--rate={v['rate']}", f"--pitch={v['pitch']}",
                        "--text", text, "--write-media", mp3], check=True, capture_output=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", str(SR), wav], check=True)
        open(key, "w", encoding="utf-8").write(sig)
    x, _ = sf.read(wav)
    th = 0.012
    idx = np.where(np.abs(x) > th)[0]
    a, b = max(0, idx[0] - int(0.03 * SR)), min(len(x), idx[-1] + int(0.06 * SR))
    return x[a:b]


lines, clips, t = [], [], START
i = 0
for si, sc in enumerate(ESCENAS):
    if si:
        t += GAP_SCENE
    for who, text, en, fx in sc["lines"]:
        x = tts(i, who, text)
        d = len(x) / SR
        lines.append(dict(i=i, scene=sc["id"], si=si, who=who, start=round(t, 2), end=round(t + d, 2), es=text, en=en, fx=fx))
        clips.append((t, x))
        t += d + (GAP_SFX if fx else GAP)
        i += 1
end = lines[-1]["end"]
total = end + ARGS.outro
out = np.zeros(int(total * SR))
for t0, x in clips:
    k = int(t0 * SR)
    out[k:k + len(x)] += x
out = out / max(1e-6, np.max(np.abs(out))) * 0.89
sf.write(os.path.join(HERE, "assets", "voz.wav"), out, SR)
json.dump(dict(lines=lines, speech_end=end, total=round(total, 2)), open(os.path.join(HERE, "lineas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("líneas", len(lines), "voz termina", round(end, 2), "total", round(total, 2))
