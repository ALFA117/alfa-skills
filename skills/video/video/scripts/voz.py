"""Voz en off por escena -> una sola pista con los inicios de escena.

Uso:
  python -I voz.py <carpeta_con_s1.txt..sN.txt> <voz> <salida.wav> [--rate +22%] [--gap 0.35] [--start 0.4] [--total 61.5]

<voz>:
  - Microsoft (edge-tts, natural, requiere internet): es-MX-DaliaNeural, es-MX-JorgeNeural,
    es-US-AlonsoNeural, es-US-PalomaNeural, en-US-AndrewNeural, ...
  - Kokoro local (sin internet, más robótica): ef_dora, em_alex, em_santa, am_michael, af_heart, ...
--rate: velocidad. Edge-tts: porcentaje ("+22%"). Kokoro: multiplicador ("1.1").

Recorta silencio al inicio y al final de cada escena y deja las pausas internas en
~0.24 s como máximo. Imprime JSON con duración e inicio de cada escena y el total.
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("voice")
ap.add_argument("out")
ap.add_argument("--rate", default=None)
ap.add_argument("--gap", type=float, default=0.35)
ap.add_argument("--start", type=float, default=0.4)
ap.add_argument("--total", type=float, default=None)
a = ap.parse_args()

files = sorted(glob.glob(os.path.join(a.dir, "s*.txt")), key=lambda p: int(re.findall(r"\d+", os.path.basename(p))[0]))
if not files:
    sys.exit("No hay s1.txt, s2.txt... en " + a.dir)
edge = "-" in a.voice
work = os.path.join(a.dir, "_tts")
os.makedirs(work, exist_ok=True)


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=(os.name == "nt" and cmd[0] == "hyperframes"))


def dur(p):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(out.stdout.strip())


clips = []
for i, f in enumerate(files, 1):
    raw = os.path.join(work, f"raw{i}" + (".mp3" if edge else ".wav"))
    if edge:
        cmd = [sys.executable, "-m", "edge_tts", "--voice", a.voice, "--file", f, "--write-media", raw]
        if a.rate:
            cmd.insert(5, f"--rate={a.rate}")
        run(cmd)
    else:
        cmd = ["hyperframes", "tts", f, "-v", a.voice, "-o", raw]
        lang = {"e": "es", "a": "en-us", "b": "en-gb", "f": "fr-fr", "p": "pt-br", "i": "it"}.get(a.voice[0])
        if lang:
            cmd += ["-l", lang]
        if a.rate:
            cmd += ["-s", a.rate]
        run(cmd)
    clean = os.path.join(work, f"s{i}.wav")
    af = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
          "silenceremove=stop_periods=-1:stop_duration=0.28:stop_threshold=-45dB:stop_silence=0.24")
    run(["ffmpeg", "-y", "-i", raw, "-af", af, "-ar", "48000", "-ac", "1", clean])
    clips.append((clean, dur(clean)))

starts, t = [], a.start
for _, d in clips:
    starts.append(round(t, 2))
    t += d + a.gap
total = a.total or round(t - a.gap + 1.6, 2)
inputs, chains, labels = [], [], []
for k, ((p, _), s) in enumerate(zip(clips, starts)):
    inputs += ["-i", p]
    chains.append(f"[{k}]adelay={int(s * 1000)}:all=1[a{k}]")
    labels.append(f"[a{k}]")
fc = ";".join(chains) + ";" + "".join(labels) + f"amix=inputs={len(clips)}:normalize=0,apad=whole_dur={total},atrim=0:{total}"
run(["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-ar", "48000", a.out])
print(json.dumps({"voice": a.voice, "scenes": [{"start": s, "dur": round(d, 2), "end": round(s + d, 2)} for (_, d), s in zip(clips, starts)],
                  "speech_end": round(starts[-1] + clips[-1][1], 2), "total": total}, indent=1))
