"""Mapa de tiempos entre dos narraciones del MISMO guion (otra voz, otra velocidad).

Alinea palabra por palabra dos transcript.json de HyperFrames y devuelve pares [viejo, nuevo]
estrictamente crecientes para remapear una coreografía hecha sobre la voz de referencia.

Uso como módulo:
    from timemap import build_map, mapper
    pairs = build_map("transcript-ref.json", "transcript.json", dur)
    M = mapper(pairs); M(10.8) -> segundo equivalente en la voz nueva
Uso CLI: python -I timemap.py ref.json nuevo.json 62.5   (imprime los pares)
"""
import difflib
import json
import re
import sys
import unicodedata


def _norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def build_map(ref_path, new_path, dur):
    old = json.load(open(ref_path, encoding="utf-8"))
    new = json.load(open(new_path, encoding="utf-8"))
    a, b = [_norm(x["text"]) for x in old], [_norm(x["text"]) for x in new]
    pts = [(0.0, 0.0)]
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            pts.append((old[blk.a + k]["start"], new[blk.b + k]["start"]))
    pts.append((dur, dur))
    pts.sort()
    mono = [pts[0]]
    for p in pts[1:]:
        if p[0] > mono[-1][0] + 1e-6 and p[1] > mono[-1][1] + 1e-6:
            mono.append(p)
    return [[round(x, 3), round(y, 3)] for x, y in mono]


def mapper(pairs):
    def M(t):
        t = float(t)
        for (x0, y0), (x1, y1) in zip(pairs, pairs[1:]):
            if t <= x1:
                return y0 + (y1 - y0) * (t - x0) / (x1 - x0)
        return t
    return M


if __name__ == "__main__":
    pr = build_map(sys.argv[1], sys.argv[2], float(sys.argv[3]))
    print(len(pr), "anclas")
    print(json.dumps(pr))
