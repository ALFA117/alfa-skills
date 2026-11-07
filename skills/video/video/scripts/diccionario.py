"""Generador de videos "Diccionario Web3" (@tu_usuario) sobre serie_v2.page().

Cada video: intro (índice de 4 palabras) + 4 entradas de diccionario (término, pronunciación, categoría,
definición palabra por palabra, ejemplo, ícono animado) + cierre (rejilla con las 4 palabras).
Uso desde build.py:  from diccionario import build; build(HERE, VIDEO_SPEC)
El spec viene de videos/diccionario-web3/specs.py (VIDEOS[i]). Tiempos: voz.json del proyecto.
"""
import json
import os
import re

from serie_v2 import THEMES, _hex, _mix, _h, install_fonts, page, scene

# ---------------------------------------------------------------- temas (uno distinto por video)
def _t(name, bg, ink, acc, fd, fb, fm, fonts, light=False, upper=False, hsize=96, hls="-0.02em", lh=1.0, ul="bar", cue="pill", esize=110, efd=None):
    d = dict(name=name, bg=bg, ink=ink, acc=acc, glyph="•", fd=fd, fb=fb, fm=fm, upper=upper, hsize=hsize, hls=hls, lh=lh, ul=ul, cue=cue, esize=esize, fonts=fonts)
    if light:
        d["light"] = True
    if efd:
        d["efd"] = efd
    return d

INTER = [("Inter", "100 550", "inter-latin-500-normal.woff2"), ("Inter", "551 900", "inter-latin-700-normal.woff2")]
WORK = [("Work Sans", "100 550", "WorkSans-Regular.ttf"), ("Work Sans", "551 900", "WorkSans-Bold.ttf")]
INSTR = [("Instrument Sans", "100 550", "InstrumentSans-Regular.ttf"), ("Instrument Sans", "551 900", "InstrumentSans-Bold.ttf")]
JB = [("JetBrains Mono", "100 550", "JetBrainsMono-400.woff2"), ("JetBrains Mono", "551 900", "JetBrainsMono-700.woff2")]
DM = [("DM Mono", "100 900", "DMMono-Regular.ttf")]
PLEX = [("IBM Plex Mono", "100 550", "IBMPlexMono-Regular.ttf"), ("IBM Plex Mono", "551 900", "IBMPlexMono-Bold.ttf")]
GEIST = [("Geist Mono", "100 550", "GeistMono-Regular.ttf"), ("Geist Mono", "551 900", "GeistMono-Bold.ttf")]
RHM = [("Red Hat Mono", "100 550", "RedHatMono-Regular.ttf"), ("Red Hat Mono", "551 900", "RedHatMono-Bold.ttf")]

THEMES.update({
    "d01": _t("Hielo magenta", "#F2F4F8", "#101828", "#D61F69", "Gloock", "Inter", "JetBrains Mono", [("Gloock", "100 900", "Gloock-Regular.ttf")] + INTER + JB, light=True, hsize=104),
    "d02": _t("Espresso espuma", "#17130F", "#F3EDE4", "#8FD3C1", "Lora", "Work Sans", "DM Mono", [("Lora", "100 900", "Lora-Bold.ttf")] + WORK + DM, hsize=96),
    "d03": _t("Máquina de escribir", "#ECE5D3", "#22201C", "#2B59C3", "Special Elite", "Inter", "IBM Plex Mono", [("Special Elite", "100 900", "special-elite-latin-400-normal.woff2")] + INTER + PLEX, light=True, hsize=92),
    "d04": _t("Marcador", "#111111", "#F5F5F5", "#FFE14D", "Permanent Marker", "Inter", "Geist Mono", [("Permanent Marker", "100 900", "permanent-marker-latin-400-normal.woff2")] + INTER + GEIST, hsize=100, ul="mark", efd="Inter"),
    "d05": _t("Pixel rosa", "#0E1726", "#E2F3FF", "#F472B6", "Pixelify Sans", "Inter", "JetBrains Mono", [("Pixelify Sans", "100 900", "PixelifySans-Medium.ttf")] + INTER + JB, hsize=100, ul="mark"),
    "d06": _t("Papel financiero", "#E6ECF0", "#14202B", "#B45309", "Libre Baskerville", "Work Sans", "DM Mono", [("Libre Baskerville", "100 900", "LibreBaskerville-Regular.ttf")] + WORK + DM, light=True, hsize=84),
    "d07": _t("Acero salmón", "#1E2320", "#ECEFE9", "#FCA5A5", "Saira Stencil One", "Inter", "Red Hat Mono", [("Saira Stencil One", "100 900", "saira-stencil-one-latin-400-normal.woff2")] + INTER + RHM, upper=True, hsize=88, efd="Inter"),
    "d08": _t("Marfil vino", "#FAF6F0", "#1A1414", "#9F1239", "Italiana", "Instrument Sans", "IBM Plex Mono", [("Italiana", "100 900", "Italiana-Regular.ttf")] + INSTR + PLEX, light=True, hsize=112),
    "d09": _t("Alarma", "#0B0B0C", "#F1F1F1", "#F43F5E", "Crimson Pro", "Inter", "Geist Mono", [("Crimson Pro", "100 900", "CrimsonPro-Bold.ttf")] + INTER + GEIST, hsize=104),
    "d10": _t("Mantequilla", "#FFF3CF", "#2B2118", "#15803D", "Caveat", "Work Sans", "DM Mono", [("Caveat", "100 900", "caveat-latin-700-normal.woff2")] + WORK + DM, light=True, hsize=130, efd="Work Sans"),
})

# ---------------------------------------------------------------- íconos (A = acento, K = tinta, B = fondo, C = tarjeta)
ICONS = {
    "parachute": '<path d="M10 46 C10 10 90 10 90 46 Z" fill="A"/><path d="M10 46 L50 80 L90 46 M36 46 L50 80 L64 46" fill="none" stroke="K" stroke-width="4"/><rect x="40" y="78" width="20" height="16" rx="3" fill="K"/>',
    "coins": '<circle cx="36" cy="58" r="26" fill="A"/><circle cx="64" cy="42" r="26" fill="none" stroke="K" stroke-width="6"/><circle cx="64" cy="42" r="12" fill="K"/>',
    "peak": '<polyline points="6,86 30,60 48,70 74,22 94,40" fill="none" stroke="K" stroke-width="7" stroke-linejoin="round"/><circle cx="74" cy="22" r="10" fill="A"/><path d="M66 8 L74 0 L82 8" fill="none" stroke="A" stroke-width="5"/>',
    "percent": '<circle cx="28" cy="28" r="16" fill="none" stroke="K" stroke-width="7"/><circle cx="72" cy="72" r="16" fill="A"/><line x1="80" y1="14" x2="20" y2="86" stroke="K" stroke-width="8" stroke-linecap="round"/>',
    "bull": '<path d="M14 26 Q20 46 34 44 M86 26 Q80 46 66 44" fill="none" stroke="K" stroke-width="7" stroke-linecap="round"/><path d="M30 40 H70 L64 84 H36 Z" fill="A"/><circle cx="42" cy="58" r="4" fill="K"/><circle cx="58" cy="58" r="4" fill="K"/><path d="M20 20 L50 4 L80 20" fill="none" stroke="A" stroke-width="6"/>',
    "bear": '<circle cx="28" cy="26" r="11" fill="A"/><circle cx="72" cy="26" r="11" fill="A"/><circle cx="50" cy="54" r="32" fill="A"/><circle cx="40" cy="50" r="4" fill="K"/><circle cx="60" cy="50" r="4" fill="K"/><path d="M20 92 L50 78 L80 92" fill="none" stroke="K" stroke-width="6"/>',
    "flame": '<path d="M50 6 C66 30 82 42 82 64 C82 82 68 96 50 96 C32 96 18 82 18 64 C18 46 34 40 36 22 C44 32 48 36 50 6 Z" fill="A"/><path d="M50 50 C58 62 64 68 64 76 C64 86 58 92 50 92 C42 92 36 86 36 78 C36 70 46 66 50 50 Z" fill="K"/>',
    "block": '<polygon points="50,6 92,28 50,50 8,28" fill="A"/><polygon points="8,28 50,50 50,96 8,74" fill="none" stroke="K" stroke-width="5"/><polygon points="92,28 50,50 50,96 92,74" fill="K"/><text x="50" y="34" text-anchor="middle" font-size="16" font-family="monospace" fill="B">#0</text>',
    "phone": '<rect x="26" y="6" width="48" height="88" rx="10" fill="none" stroke="K" stroke-width="6"/><rect x="34" y="20" width="32" height="50" rx="4" fill="A"/><path d="M60 82 Q50 74 40 82" fill="none" stroke="K" stroke-width="4"/><path d="M80 18 Q90 28 80 38 M86 10 Q100 28 86 46" fill="none" stroke="A" stroke-width="4"/>',
    "safe": '<rect x="8" y="12" width="84" height="78" rx="10" fill="none" stroke="K" stroke-width="6"/><circle cx="50" cy="51" r="20" fill="A"/><circle cx="50" cy="51" r="6" fill="K"/><rect x="16" y="88" width="14" height="8" fill="K"/><rect x="70" y="88" width="14" height="8" fill="K"/>',
    "faucet": '<rect x="14" y="20" width="56" height="18" rx="6" fill="K"/><rect x="36" y="8" width="12" height="14" fill="K"/><path d="M70 26 H82 Q90 26 90 36 V44" fill="none" stroke="K" stroke-width="8"/><circle cx="90" cy="62" r="7" fill="A"/><circle cx="90" cy="84" r="5" fill="A"/>',
    "fork": '<line x1="50" y1="96" x2="50" y2="54" stroke="K" stroke-width="8" stroke-linecap="round"/><path d="M50 54 Q50 30 22 14 M50 54 Q50 30 78 14" fill="none" stroke="K" stroke-width="8" stroke-linecap="round"/><circle cx="22" cy="14" r="9" fill="A"/><circle cx="78" cy="14" r="9" fill="A"/>',
    "eye": '<path d="M4 50 C26 16 74 16 96 50 C74 84 26 84 4 50 Z" fill="none" stroke="K" stroke-width="7"/><circle cx="50" cy="50" r="16" fill="A"/><circle cx="50" cy="50" r="6" fill="K"/>',
    "cloud": '<path d="M24 70 C8 70 6 48 22 46 C22 28 46 24 54 38 C62 26 86 30 84 50 C98 52 96 72 80 72 Z" fill="A"/><path d="M34 82 L28 96 M52 82 L46 96 M70 82 L64 96" stroke="K" stroke-width="6" stroke-linecap="round"/>',
    "hand": '<path d="M24 54 V28 Q24 20 32 20 Q40 20 40 28 V46 V14 Q40 6 48 6 Q56 6 56 14 V46 V20 Q56 12 64 12 Q72 12 72 20 V58 Q72 92 46 92 Q30 92 22 76 L10 56 Q6 48 14 46 Q20 44 24 54 Z" fill="A" stroke="K" stroke-width="4"/>',
    "magnifier": '<circle cx="42" cy="42" r="28" fill="none" stroke="K" stroke-width="8"/><circle cx="42" cy="42" r="14" fill="A"/><line x1="64" y1="64" x2="92" y2="92" stroke="K" stroke-width="12" stroke-linecap="round"/>',
    "drop": '<path d="M50 6 C66 32 80 48 80 64 C80 82 66 94 50 94 C34 94 20 82 20 64 C20 48 34 32 50 6 Z" fill="A"/><text x="50" y="76" text-anchor="middle" font-size="26" font-family="monospace" font-weight="700" fill="B">gw</text>',
    "fingerprint": '<path d="M50 14 C28 14 16 30 16 50 M50 26 C36 26 28 36 28 50 C28 68 34 80 42 90 M50 38 C44 38 40 44 40 50 C40 66 46 78 56 88 M50 50 C50 66 56 76 68 84 M84 50 C84 30 72 14 50 14 M72 50 C72 36 64 26 50 26 M62 52 C62 44 58 38 50 38" fill="none" stroke="K" stroke-width="5" stroke-linecap="round"/><circle cx="50" cy="50" r="6" fill="A"/>',
    "nodes": '<line x1="50" y1="18" x2="18" y2="70" stroke="K" stroke-width="4"/><line x1="50" y1="18" x2="82" y2="70" stroke="K" stroke-width="4"/><line x1="18" y1="70" x2="82" y2="70" stroke="K" stroke-width="4"/><line x1="50" y1="18" x2="50" y2="50" stroke="K" stroke-width="4"/><circle cx="50" cy="18" r="12" fill="A"/><circle cx="18" cy="70" r="12" fill="A"/><circle cx="82" cy="70" r="12" fill="A"/><circle cx="50" cy="50" r="9" fill="K"/>',
    "queue": '<rect x="6" y="40" width="22" height="22" rx="5" fill="none" stroke="K" stroke-width="4"/><rect x="34" y="40" width="22" height="22" rx="5" fill="none" stroke="K" stroke-width="4"/><rect x="62" y="40" width="22" height="22" rx="5" fill="A"/><path d="M88 51 H98 M92 45 L98 51 L92 57" fill="none" stroke="K" stroke-width="4"/><rect x="20" y="74" width="60" height="16" rx="4" fill="K"/>',
    "idcard": '<rect x="6" y="18" width="88" height="64" rx="10" fill="none" stroke="K" stroke-width="6"/><circle cx="32" cy="44" r="11" fill="A"/><path d="M16 70 Q32 54 48 70" fill="A"/><line x1="58" y1="38" x2="84" y2="38" stroke="K" stroke-width="5"/><line x1="58" y1="54" x2="78" y2="54" stroke="K" stroke-width="5"/>',
    "pie": '<circle cx="50" cy="50" r="40" fill="none" stroke="K" stroke-width="7"/><path d="M50 50 L50 10 A40 40 0 0 1 88 62 Z" fill="A"/>',
    "water": '<path d="M4 40 Q16 30 28 40 T52 40 T76 40 T100 40" fill="none" stroke="A" stroke-width="7"/><path d="M4 62 Q16 52 28 62 T52 62 T76 62 T100 62" fill="none" stroke="K" stroke-width="7"/><path d="M4 84 Q16 74 28 84 T52 84 T76 84 T100 84" fill="none" stroke="A" stroke-width="7"/>',
    "zigzag": '<polyline points="4,70 18,30 32,78 46,18 60,84 74,26 88,64 96,44" fill="none" stroke="A" stroke-width="7" stroke-linejoin="round"/><line x1="4" y1="94" x2="96" y2="94" stroke="K" stroke-width="5"/>',
    "globe": '<circle cx="50" cy="50" r="40" fill="none" stroke="K" stroke-width="6"/><ellipse cx="50" cy="50" rx="18" ry="40" fill="none" stroke="K" stroke-width="5"/><line x1="10" y1="50" x2="90" y2="50" stroke="K" stroke-width="5"/><circle cx="76" cy="24" r="10" fill="A"/>',
    "flask": '<path d="M38 6 H62 M42 6 V36 L16 84 Q12 94 24 94 H76 Q88 94 84 84 L58 36 V6" fill="none" stroke="K" stroke-width="6" stroke-linejoin="round"/><path d="M28 66 H72 L82 86 Q84 90 78 90 H22 Q16 90 18 86 Z" fill="A"/>',
    "layer1": '<polygon points="50,46 94,66 50,86 6,66" fill="A"/><polygon points="50,26 94,46 50,66 6,46" fill="none" stroke="K" stroke-width="4" stroke-dasharray="6 6"/>',
    "layer2": '<polygon points="50,52 94,72 50,92 6,72" fill="none" stroke="K" stroke-width="5"/><polygon points="50,16 94,36 50,56 6,36" fill="A"/>',
    "sparkle": '<path d="M50 4 L58 40 L94 50 L58 60 L50 96 L42 60 L6 50 L42 40 Z" fill="A"/><circle cx="82" cy="18" r="7" fill="K"/><circle cx="18" cy="84" r="5" fill="K"/>',
    "floor": '<rect x="10" y="56" width="18" height="34" fill="A"/><rect x="34" y="40" width="18" height="50" fill="none" stroke="K" stroke-width="5"/><rect x="58" y="24" width="18" height="66" fill="none" stroke="K" stroke-width="5"/><line x1="4" y1="56" x2="96" y2="56" stroke="A" stroke-width="4" stroke-dasharray="6 5"/>',
    "crown": '<path d="M10 76 L6 24 L32 46 L50 14 L68 46 L94 24 L90 76 Z" fill="A"/><rect x="10" y="80" width="80" height="12" rx="4" fill="K"/><text x="50" y="66" text-anchor="middle" font-size="22" font-family="monospace" font-weight="700" fill="K">%</text>',
    "list": '<rect x="10" y="8" width="80" height="84" rx="8" fill="none" stroke="K" stroke-width="5"/>' + "".join(f'<path d="M22 {28 + k * 22} l6 6 l12 -12" fill="none" stroke="A" stroke-width="5"/><line x1="48" y1="{30 + k * 22}" x2="78" y2="{30 + k * 22}" stroke="K" stroke-width="5"/>' for k in range(3)),
    "rug": '<path d="M8 30 H72 Q92 30 92 50 Q92 70 72 70 H8 Z" fill="A"/><path d="M8 30 V70 M18 30 V70 M28 30 V70" stroke="K" stroke-width="3"/><path d="M60 84 L92 92" stroke="K" stroke-width="6" stroke-linecap="round"/><circle cx="96" cy="50" r="4" fill="K"/>',
    "hook": '<path d="M50 6 V60 Q50 84 30 84 Q12 84 12 66" fill="none" stroke="K" stroke-width="8" stroke-linecap="round"/><path d="M6 72 L12 60 L20 70" fill="none" stroke="K" stroke-width="6"/><rect x="60" y="20" width="34" height="24" rx="4" fill="A"/><path d="M60 22 L77 34 L94 22" fill="none" stroke="K" stroke-width="3"/>',
    "jar": '<rect x="26" y="8" width="48" height="12" rx="4" fill="K"/><path d="M22 24 H78 Q86 24 86 34 V82 Q86 94 74 94 H26 Q14 94 14 82 V34 Q14 24 22 24 Z" fill="none" stroke="K" stroke-width="6"/><path d="M18 54 Q34 46 50 54 T82 54 V80 Q82 90 72 90 H28 Q18 90 18 80 Z" fill="A"/>',
    "dust": "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in [(20, 22, 4, "A"), (46, 14, 3, "K"), (74, 26, 5, "A"), (30, 48, 3, "K"), (60, 50, 6, "A"), (86, 56, 3, "K"), (16, 76, 5, "A"), (44, 82, 3, "K"), (70, 84, 4, "A")]),
    "whale": '<path d="M8 56 Q12 26 52 28 Q84 30 88 52 Q92 76 60 80 Q28 84 8 56 Z" fill="A"/><path d="M84 52 Q96 36 94 22 Q86 34 78 40" fill="A"/><circle cx="30" cy="50" r="4" fill="K"/><path d="M46 20 Q44 8 36 6 M46 20 Q50 8 58 6" fill="none" stroke="K" stroke-width="4" stroke-linecap="round"/>',
    "dice": '<rect x="10" y="10" width="80" height="80" rx="16" fill="A"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="K"/>' for x, y in [(30, 30), (70, 30), (50, 50), (30, 70), (70, 70)]),
    "rocket": '<path d="M50 4 Q74 24 72 62 H28 Q26 24 50 4 Z" fill="A"/><circle cx="50" cy="36" r="9" fill="K"/><path d="M28 50 L12 70 L28 66 Z M72 50 L88 70 L72 66 Z" fill="K"/><path d="M40 66 Q50 98 60 66" fill="none" stroke="A" stroke-width="5"/>',
    "sun": '<circle cx="50" cy="56" r="20" fill="A"/>' + "".join(f'<line x1="50" y1="56" x2="{50 + 40 * __import__("math").cos(a * 0.785):.0f}" y2="{56 - 40 * __import__("math").sin(a * 0.785):.0f}" stroke="K" stroke-width="5" stroke-linecap="round" stroke-dasharray="0 26 14 0"/>' for a in range(5)) + '<line x1="6" y1="80" x2="94" y2="80" stroke="K" stroke-width="5"/>',
}


def icon(name, th, size):
    bg, ink = _hex(th["bg"]), _hex(th["ink"])
    svg = ICONS[name].replace('"A"', '"' + th["acc"] + '"').replace('"K"', '"' + th["ink"] + '"').replace('"B"', '"' + th["bg"] + '"')
    return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">{svg}</svg>'


# ---------------------------------------------------------------- fondos (canvas, función pura del tiempo)
def bg_js(kind, th):
    a, k = "%d,%d,%d" % _hex(th["acc"]), "%d,%d,%d" % _hex(th["ink"])
    body = {
        "dots": f'for (let y = 30; y < 1920; y += 54) for (let x = 30; x < 1080; x += 54) {{ const p = Math.sin(t * 0.9 + x * 0.012 + y * 0.008); g.fillStyle = "rgba({k}," + (0.05 + 0.06 * Math.max(0, p)).toFixed(3) + ")"; g.beginPath(); g.arc(x, y, 2.4 + Math.max(0, p) * 1.6, 0, 6.283); g.fill(); }}',
        "lines": f'for (let k = 0; k < 40; k++) {{ const y = ((k * 52 + t * 18) % 2080) - 80; g.fillStyle = k % 6 === 0 ? "rgba({a},0.10)" : "rgba({k},0.035)"; g.fillRect(0, y, 1080, k % 6 === 0 ? 3 : 2); }}',
        "grid": f'const o = (t * 10) % 72; g.strokeStyle = "rgba({k},0.06)"; g.lineWidth = 1.5; for (let x = -72 + o; x < 1080; x += 72) {{ g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 1920); g.stroke(); }} for (let y = -72 + o; y < 1920; y += 72) {{ g.beginPath(); g.moveTo(0, y); g.lineTo(1080, y); g.stroke(); }} g.fillStyle = "rgba({a},0.12)"; for (let i = 0; i < 6; i++) {{ const x = 72 * ((i * 5 + Math.floor(t / 2)) % 15) + o, y = 72 * ((i * 11 + Math.floor(t / 3)) % 26) + o; g.fillRect(x, y, 72, 72); }}',
        "scribble": f'g.lineWidth = 4; g.lineCap = "round"; for (let i = 0; i < 14; i++) {{ const x0 = (i * 173) % 1080, y0 = ((i * 397 + t * 22) % 2100) - 90; g.strokeStyle = i % 3 === 0 ? "rgba({a},0.16)" : "rgba({k},0.06)"; g.beginPath(); g.moveTo(x0, y0); for (let s = 1; s < 8; s++) g.lineTo(x0 + Math.sin(s * 1.7 + i) * 40 + s * 12, y0 + Math.cos(s * 2.1 + i) * 30 + s * 8); g.stroke(); }}',
        "pixels": f'for (let y = 0; y < 1920; y += 40) for (let x = 0; x < 1080; x += 40) {{ const v = Math.sin(x * 0.05 + t * 1.3) * Math.cos(y * 0.03 - t * 0.7); if (v > 0.6) {{ g.fillStyle = "rgba({a}," + ((v - 0.6) * 0.35).toFixed(3) + ")"; g.fillRect(x + 4, y + 4, 32, 32); }} }}',
        "ticker": f'g.font = "600 22px monospace"; for (let c = 0; c < 9; c++) {{ const x = 40 + c * 120; for (let r = 0; r < 34; r++) {{ const y = ((r * 60 + t * (20 + c * 4)) % 2040) - 60, v = ((c * 37 + r * 13) % 97) / 10; g.fillStyle = (c + r) % 5 === 0 ? "rgba({a},0.20)" : "rgba({k},0.07)"; g.fillText((v > 5 ? "+" : "-") + v.toFixed(1) + "%", x, y); }} }}',
        "hexes": f'g.lineWidth = 2; for (let r = 0; r < 26; r++) for (let c = 0; c < 10; c++) {{ const x = c * 112 + (r % 2) * 56, y = r * 80 - 40, p = Math.sin(t * 0.8 + c * 0.7 + r * 0.4); g.strokeStyle = p > 0.85 ? "rgba({a},0.30)" : "rgba({k},0.05)"; g.beginPath(); for (let i = 0; i < 6; i++) {{ const an = Math.PI / 3 * i + Math.PI / 6; g.lineTo(x + 50 * Math.cos(an), y + 50 * Math.sin(an)); }} g.closePath(); g.stroke(); }}',
        "frames": f'g.lineWidth = 3; for (let i = 0; i < 10; i++) {{ const x = (i * 211) % 960 + 20, y = ((i * 331 + t * 14) % 2200) - 140, w = 120 + (i % 3) * 40, h = 160 + (i % 2) * 50; g.strokeStyle = i % 4 === 0 ? "rgba({a},0.20)" : "rgba({k},0.07)"; g.strokeRect(x, y, w, h); g.strokeRect(x + 12, y + 12, w - 24, h - 24); }}',
        "scan": f'for (let y = 0; y < 1920; y += 5) {{ g.fillStyle = "rgba({k},0.03)"; g.fillRect(0, y, 1080, 2); }} for (let i = 0; i < 5; i++) {{ const y = ((i * 431 + t * 260) % 2200) - 140; g.fillStyle = "rgba({a},0.07)"; g.fillRect(0, y, 1080, 6 + (i % 3) * 8); }}',
        "confetti": f'for (let i = 0; i < 46; i++) {{ const x = (i * 97) % 1080 + Math.sin(t + i) * 20, y = ((i * 211 + t * (40 + (i % 5) * 12)) % 2040) - 60; g.save(); g.translate(x, y); g.rotate(t * (i % 2 ? 1 : -1) + i); g.fillStyle = i % 3 === 0 ? "rgba({a},0.35)" : "rgba({k},0.09)"; g.fillRect(-8, -4, 16, 8); g.restore(); }}',
    }[kind]
    return ('        const cv = document.getElementById("dbg"), g = cv.getContext("2d");\n'
            f'        function bg(t) {{ g.clearRect(0, 0, 1080, 1920); {body} }}\n'
            '        const st = { t: 0 }; bg(0); tl.to(st, { t: DUR, duration: DUR, ease: "none", onUpdate: () => bg(st.t) }, 0);\n')


# ---------------------------------------------------------------- transiciones
def tx(kind, th):
    A = th["acc"]
    if kind == "wipe":
        h = f'<div id="tw" data-layout-allow-overflow style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:{A}"></div>'
        j = 'tl.set("#tw", { xPercent: -101 }, 0); EDGES.forEach((c) => tl.fromTo("#tw", { xPercent: -101 }, { keyframes: { xPercent: [-101, 0, 0, 101] }, duration: 0.9, ease: "power3.inOut", immediateRender: false }, c - 0.45));'
    elif kind == "rise":
        h = f'<div id="tw" data-layout-allow-overflow style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:{A};border-radius:120px 120px 0 0"></div>'
        j = 'tl.set("#tw", { yPercent: 101 }, 0); EDGES.forEach((c) => tl.fromTo("#tw", { yPercent: 101 }, { keyframes: { yPercent: [101, 0, 0, -101] }, duration: 0.9, ease: "power3.inOut", immediateRender: false }, c - 0.45));'
    elif kind in ("iris", "iris2", "bounce"):
        rad = {"iris": "50%", "iris2": "80px", "bounce": "50%"}[kind]
        h = f'<div id="tw" data-layout-allow-overflow style="position:absolute;left:340px;top:760px;width:400px;height:400px;border-radius:{rad};background:{A}"></div>'
        if kind == "bounce":
            j = 'tl.set("#tw", { scale: 0 }, 0); EDGES.forEach((c) => tl.fromTo("#tw", { scale: 0.3, y: -1300, opacity: 1 }, { keyframes: { y: [-1300, 0, 0, 0], scale: [0.3, 0.3, 6.5, 6.5], opacity: [1, 1, 1, 0] }, duration: 0.95, ease: "power2.inOut", immediateRender: false }, c - 0.5));'
        else:
            rot = "45" if kind == "iris2" else "0"
            j = f'tl.set("#tw", {{ scale: 0 }}, 0); EDGES.forEach((c) => tl.fromTo("#tw", {{ scale: 0, rotation: {rot}, opacity: 1 }}, {{ keyframes: {{ scale: [0, 6.5, 6.5, 6.5], rotation: [{rot}, 0, 0, 0], opacity: [1, 1, 1, 0] }}, duration: 0.9, ease: "power2.inOut", immediateRender: false }}, c - 0.45));'
    elif kind == "diag":
        h = f'<div id="tw" data-layout-allow-overflow style="position:absolute;left:-400px;top:-300px;width:1900px;height:2600px;background:{A}"></div>'
        j = 'tl.set("#tw", { x: -2300, rotation: 14 }, 0); EDGES.forEach((c) => tl.fromTo("#tw", { x: -2300, rotation: 14 }, { keyframes: { x: [-2300, 0, 0, 2300] }, duration: 0.85, ease: "power3.inOut", immediateRender: false }, c - 0.42));'
    elif kind == "bars":
        h = "".join(f'<div class="tb" id="tb{i}" data-layout-allow-overflow style="position:absolute;top:0;left:{i * 180}px;width:181px;height:1920px;background:{A}"></div>' for i in range(6))
        j = 'tl.set(".tb", { yPercent: -101 }, 0); EDGES.forEach((c) => { for (let i = 0; i < 6; i++) tl.fromTo("#tb" + i, { yPercent: -101 }, { keyframes: { yPercent: [-101, 0, 0, 101] }, duration: 0.8, ease: "power3.inOut", immediateRender: false }, c - 0.45 + i * 0.03); });'
    elif kind == "slide":
        h = f'<div id="tw" data-layout-allow-overflow style="position:absolute;left:0;top:0;width:1080px;height:1920px;background:{A};border-radius:0 140px 140px 0"></div>'
        j = 'tl.set("#tw", { xPercent: 101 }, 0); EDGES.forEach((c) => tl.fromTo("#tw", { xPercent: 101 }, { keyframes: { xPercent: [101, 0, 0, -101] }, duration: 0.9, ease: "power3.inOut", immediateRender: false }, c - 0.45));'
    elif kind == "split":
        h = f'<div id="twa" data-layout-allow-overflow style="position:absolute;left:0;top:0;width:1080px;height:961px;background:{A}"></div><div id="twb" data-layout-allow-overflow style="position:absolute;left:0;bottom:0;width:1080px;height:961px;background:{A}"></div>'
        j = ('tl.set("#twa", { yPercent: -101 }, 0); tl.set("#twb", { yPercent: 101 }, 0); EDGES.forEach((c) => { '
             'tl.fromTo("#twa", { yPercent: -101 }, { keyframes: { yPercent: [-101, 0, 0, -101] }, duration: 0.9, ease: "power3.inOut", immediateRender: false }, c - 0.45); '
             'tl.fromTo("#twb", { yPercent: 101 }, { keyframes: { yPercent: [101, 0, 0, 101] }, duration: 0.9, ease: "power3.inOut", immediateRender: false }, c - 0.45); });')
    else:  # glitch
        h = "".join(f'<div class="tg" id="tg{i}" data-layout-allow-overflow style="position:absolute;left:0;top:{i * 240}px;width:1080px;height:241px;background:{A if i % 2 else th["ink"]}"></div>' for i in range(8))
        j = 'tl.set(".tg", { xPercent: -101 }, 0); EDGES.forEach((c) => { for (let i = 0; i < 8; i++) tl.fromTo("#tg" + i, { xPercent: i % 2 ? 101 : -101 }, { keyframes: { xPercent: [i % 2 ? 101 : -101, 0, 0, i % 2 ? -101 : 101] }, duration: 0.7, ease: "power4.inOut", immediateRender: false }, c - 0.38 + (i % 3) * 0.03); });'
    return "        " + h, "        " + j + "\n"


# ---------------------------------------------------------------- utilidades de texto / tiempo
def _split_sentences(txt):
    parts = re.split(r"(?<=[.!?:])\s+", txt.strip())
    return [p for p in parts if p]


def _cues_for(text, a, b):
    sents = _split_sentences(text)
    tot = sum(len(s) for s in sents)
    out, t = [], a
    for s in sents:
        d = (b - a) * len(s) / tot
        out.append((round(t, 2), round(t + d, 2), s))
        t += d
    return out


def build(here, v, outro_en):
    th = THEMES[v["theme"]]
    install_fonts(here, th)
    vz = json.load(open(os.path.join(here, "voz.json")))
    scn = vz["scenes"]
    SC = [0] + [round(s["start"] - 0.6, 2) for s in scn[1:]]
    END = round(vz["speech_end"] + 0.6, 2)
    DUR = 60.0
    terms = v["terms"]
    ink, acc = th["ink"], th["acc"]
    bg, inkc = _hex(th["bg"]), _hex(th["ink"])
    card, line, muted = _h(_mix(bg, inkc, 0.05 if th.get("light") else 0.07)), _h(_mix(bg, inkc, 0.18)), _h(_mix(bg, inkc, 0.6))
    if th.get("light"):
        card = "#FFFFFF" if sum(bg) > 690 else _h(_mix(bg, (255, 255, 255), 0.6))

    edition = v["edition"]
    EYES = [(SC[0], SC[1], "01 · Hoy")] + [(SC[i], SC[i + 1] if i + 1 < len(SC) else END, f"0{i + 1} · {terms[i - 1]['t']}") for i in range(1, 5)] + [(SC[5], END, "06 · Repaso")]
    HEADS = [(0.3, SC[1] - 0.1, (f"Diccionario Web3: *{edition}." if edition else "Diccionario *Web3."))]
    for i in range(1, 5):
        HEADS.append((SC[i] + 0.3, SC[i + 1] - 0.1, terms[i - 1]["q"]))
    HEADS.append((SC[5] + 0.3, END - 0.1, "Tu diccionario *crece."))
    CUES = _cues_for(v["intro_en"], scn[0]["start"] - 0.3, scn[0]["end"] + 0.2)
    for i in range(1, 5):
        CUES += _cues_for(terms[i - 1]["en"], scn[i]["start"] - 0.3, scn[i]["end"] + 0.2)
    CUES += _cues_for(outro_en, scn[5]["start"] - 0.3, END)

    # ---------------- escenas
    tabs = "".join(f'<div class="tab" id="tab{k}"><b class="syne">{t["t"][0]}</b><span>{t["t"]}</span></div>' for k, t in enumerate(terms))
    S = [scene(1, SC, END, f'''          <div id="cover"><i class="mono">DICCIONARIO</i><b class="syne">Web3</b><span class="mono">{edition.upper() if edition else "VOL. 1"} · 4 PALABRAS</span></div>
          <div id="tabs">{tabs}</div>''', "transparent")]
    for i, t in enumerate(terms, 1):
        tsize = max(64, min(118, int(1500 / max(6, len(t["t"])))))
        defw = " ".join(f'<span class="dw">{w}</span>' for w in t["d"].split())
        S.append(scene(i + 1, SC, END, f'''          <div class="entry" id="en{i}"><div class="eh"><div><b class="syne et" style="font-size:{tsize}px">{t["t"]}</b>
              <div class="ep mono">/ {t["tv"].split(",")[0].lower()} / · <em>{t["cat"]}</em></div></div><div class="ei" id="ei{i}">{icon(t["icon"], th, 190)}</div></div>
            <div class="ed" id="ed{i}"></div><p class="edef" id="df{i}">{defw}</p>
            <div class="ex" id="ex{i}"><i class="mono">EJEMPLO</i><span>{t["ex"]}</span></div>
            <div class="num mono">0{i}<small>/04</small></div></div>''', "transparent"))
    grid = "".join(f'<div class="gt" id="gt{k}">{icon(t["icon"], th, 120)}<b class="syne">{t["t"]}</b></div>' for k, t in enumerate(terms))
    S.append(scene(6, SC, END, f'''          <div id="grid">{grid}</div>
          <div id="next" class="chip red">¿QUÉ PALABRA SIGUE?</div>''', "transparent"))

    css = f'''
      #dbg {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      #cover {{ position: absolute; left: 0; right: 0; top: 660px; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
      #cover i {{ font-style: normal; font-size: 30px; letter-spacing: 0.5em; color: {muted}; }} #cover b {{ font-size: 220px; line-height: 0.95; color: {acc}; }}
      #cover span {{ font-size: 24px; letter-spacing: 0.3em; color: {ink}; }}
      #tabs {{ position: absolute; left: 80px; right: 80px; top: 1080px; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
      .tab {{ display: flex; align-items: center; gap: 18px; padding: 16px 22px; border-radius: 18px; background: {card}; border: 2px solid {line}; }}
      .tab b {{ width: 64px; height: 64px; flex: none; border-radius: 14px; background: {acc}; color: {th["bg"]}; display: flex; align-items: center; justify-content: center; font-size: 40px; line-height: 1; }}
      .tab span {{ font-size: 32px; font-weight: 700; color: {ink}; white-space: nowrap; overflow: hidden; }}
      .entry {{ position: absolute; left: 70px; top: 630px; width: 940px; height: 730px; padding: 40px 46px; border-radius: 30px; background: {card}; border: 2px solid {line}; box-shadow: 0 30px 60px rgba(0,0,0,{0.08 if th.get("light") else 0.4}); }}
      .eh {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; }}
      .et {{ display: block; line-height: 1; color: {ink}; white-space: nowrap; }} .ep {{ margin-top: 14px; font-size: 26px; color: {muted}; }} .ep em {{ font-style: italic; color: {acc}; }}
      .ei {{ flex: none; }}
      .ed {{ height: 4px; margin: 26px 0 22px; background: {acc}; transform-origin: left center; border-radius: 2px; }}
      .edef {{ font-family: "{th["fb"]}", sans-serif; font-weight: 700; font-size: 46px; line-height: 1.3; color: {ink}; }}
      .dw {{ display: inline-block; }}
      .ex {{ position: absolute; left: 46px; right: 46px; bottom: 40px; padding: 22px 26px; border-radius: 18px; background: {_h(_mix(_hex(card), _hex(acc), 0.12))}; border-left: 8px solid {acc}; }}
      .ex i {{ font-style: normal; display: block; font-size: 20px; letter-spacing: 0.3em; color: {acc}; margin-bottom: 6px; }} .ex span {{ font-size: 34px; line-height: 1.3; font-style: italic; color: {ink}; }}
      .num {{ position: absolute; right: 40px; top: -26px; padding: 8px 18px; border-radius: 999px; background: {acc}; color: {th["bg"]}; font-size: 26px; }} .num small {{ font-size: 18px; opacity: 0.8; }}
      #grid {{ position: absolute; left: 80px; right: 80px; top: 650px; display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }}
      .gt {{ height: 270px; border-radius: 26px; background: {card}; border: 2px solid {line}; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; }}
      .gt b {{ font-size: 48px; line-height: 1; color: {ink}; text-align: center; padding: 0 10px; }}
      #next {{ left: 360px; top: 1270px; }}
'''
    js = ""
    # intro
    a0, b0 = scn[0]["start"], scn[0]["end"]
    js += f'        tl.fromTo("#cover", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.8)" }}, {a0:.2f});\n'
    for k in range(4):
        tk = a0 + (b0 - a0) * (0.55 + k * 0.11)
        js += f'        tl.fromTo("#tab{k}", {{ opacity: 0, y: 40, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {tk:.2f});\n'
    bursts = []
    sfx = [[0.3, "whoosh"], [a0, "pop"]]
    for i, t in enumerate(terms, 1):
        a, b = scn[i]["start"], scn[i]["end"]
        full = f'{t["tv"]}: {t["dv"]} {t["exv"]}'
        f_def = len(t["tv"]) / len(full)
        f_ex = (len(t["tv"]) + len(t["dv"])) / len(full)
        tdef, tex = a + (b - a) * f_def + 0.15, a + (b - a) * f_ex + 0.1
        nwords = len(t["d"].split())
        js += (f'        tl.fromTo("#en{i}", {{ opacity: 0, y: 80, rotationX: 18, transformPerspective: 1200 }}, {{ opacity: 1, y: 0, rotationX: 0, duration: 0.6, ease: "expo.out" }}, {SC[i] + 0.25:.2f});\n'
               f'        tl.fromTo("#en{i} .et", {{ opacity: 0, x: -50 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "expo.out" }}, {a - 0.05:.2f});\n'
               f'        tl.fromTo("#ei{i}", {{ opacity: 0, scale: 0.3, rotation: -25 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.55, ease: "back.out(2.2)" }}, {a + 0.15:.2f});\n'
               f'        tl.fromTo("#ei{i}", {{ y: 0 }}, {{ keyframes: {{ y: [-10, 0, -6, 0] }}, duration: 2.4, ease: "sine.inOut", immediateRender: false }}, {a + 0.9:.2f});\n'
               f'        tl.fromTo("#ed{i}", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, {a + 0.2:.2f});\n'
               f'        tl.fromTo("#df{i} .dw", {{ opacity: 0, y: 18 }}, {{ opacity: 1, y: 0, duration: 0.25, stagger: {max(0.05, min(0.16, (tex - tdef - 0.3) / max(1, nwords))):.3f}, ease: "power2.out" }}, {tdef:.2f});\n'
               f'        tl.fromTo("#ex{i}", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "back.out(1.6)" }}, {tex:.2f});\n')
        bursts.append((round(a + 0.15, 2), 830, 760))
        sfx += [[SC[i], "whoosh"], [a, "pop"], [tdef, "tick"], [tex, "pop"]]
    a5 = scn[5]["start"]
    js += f'        tl.fromTo(".gt", {{ opacity: 0, scale: 0.6, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.45, stagger: 0.15, ease: "back.out(2)" }}, {SC[5] + 0.3:.2f});\n'
    js += f'        tl.fromTo("#next", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }}, {a5 + 1.2:.2f});\n'
    sfx += [[SC[5], "whoosh"], [SC[5] + 0.3, "tick"], [SC[5] + 0.45, "tick"], [SC[5] + 0.6, "tick"], [SC[5] + 0.75, "tick"], [END - 0.4, "riser"], [END, "impact"]]
    bursts.append((round(a5 + 1.2, 2), 540, 1300))

    txh, txj = tx(v["tx"], th)
    txj = "        const EDGES = SC.slice(1).concat([END]);\n" + txj
    html = page(th, DUR, SC, EYES, HEADS, CUES, "\n".join(S), css, js, '        <canvas id="dbg" width="1080" height="1920"></canvas>', bg_js(v["bg"], th), txh, txj,
                END, None, "SÍGUEME PARA MÁS", takeaway=" · ".join(t["t"] for t in terms), recolor=False, kicker="DICCIONARIO WEB3",
                ghosts=["Glosario"] + [t["t"] for t in terms] + ["Repaso"], bursts=bursts)
    open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"cuts": SC + [END], "sfx": sfx}, open(os.path.join(here, "timing.json"), "w"))
    print("index.html listo", SC, END)
