"""Sistema v3 «Web3 en 60 segundos» (@tu_usuario): producción con gancho, malla de gradiente, vidrio,
13 componentes animados sincronizados a palabras de la voz (transcript.json) y flyer-portada final.

Uso (build.py):  from produccion import build; build(HERE, VIDEO_SPEC)
Spec: ver videos/web3-en-60/specs.py. Voz recomendada: en-US-AndrewMultilingualNeural (lee siglas en inglés nativo).
Reglas: nada de texto con fill transparente (el linter lo marca); ids de componentes = c{escena}_{n}.
"""
import os as _os
FIRMA = _os.environ.get("FIRMA_REDES", "@tu_usuario")

import json
import math
import os
import re
import unicodedata

from serie_v2 import _hex, _mix, _h, install_fonts
from diccionario import ICONS

INTER = [("Inter", "100 550", "inter-latin-500-normal.woff2"), ("Inter", "551 900", "inter-latin-700-normal.woff2")]
WORK = [("Work Sans", "100 550", "WorkSans-Regular.ttf"), ("Work Sans", "551 900", "WorkSans-Bold.ttf")]
JB = [("JetBrains Mono", "100 550", "JetBrainsMono-400.woff2"), ("JetBrains Mono", "551 900", "JetBrainsMono-700.woff2")]
GEIST = [("Geist Mono", "100 550", "GeistMono-Regular.ttf"), ("Geist Mono", "551 900", "GeistMono-Bold.ttf")]
DM = [("DM Mono", "100 900", "DMMono-Regular.ttf")]


def _t(bg, ink, acc, acc2, fd, ffile, fb, fbfiles, fm, fmfiles, tsize=104, light=False, upper=False, ls="-0.03em", bigsize=170, lh=1.04, wf=0.62):
    return dict(wf=wf, bg=bg, ink=ink, acc=acc, acc2=acc2, fd=fd, fb=fb, fm=fm, tsize=tsize, light=light, upper=upper, ls=ls, bigsize=bigsize, lh=lh,
                fonts=[(fd, "100 900", ffile)] + fbfiles + fmfiles + ([] if fbfiles is INTER else INTER))


THEMES3 = {
    "p1": _t("#0B1020", "#EEF0FF", "#7C5CFF", "#00D1B2", "Inter Black", "inter-latin-900-normal.woff2", "Inter", INTER, "JetBrains Mono", JB, tsize=100),
    "p2": _t("#FFF4E6", "#21160E", "#E8590C", "#F59F00", "National Park", "NationalPark-Bold.ttf", "Work Sans", WORK, "DM Mono", DM, tsize=98, light=True),
    "p3": _t("#08090A", "#F7F7F7", "#22C55E", "#EF4444", "Erica One", "EricaOne-Regular.ttf", "Inter", INTER, "Geist Mono", GEIST, tsize=92, ls="0em", wf=0.9),
    "p4": _t("#EEF3F8", "#0F172A", "#0284C7", "#6366F1", "Smooch Sans", "SmoochSans-Medium.ttf", "Inter", INTER, "JetBrains Mono", JB, tsize=128, light=True, upper=True, ls="0em", bigsize=210),
    "p5": _t("#13061F", "#F6EEFF", "#E879F9", "#FACC15", "Boldonse", "Boldonse-Regular.ttf", "Work Sans", WORK, "DM Mono", DM, tsize=64, ls="-0.01em", bigsize=110, lh=1.35, wf=0.95),
    "p6": _t("#0D1310", "#F1F5F2", "#E0A93B", "#34D399", "Shippori Mincho", "shippori-mincho-latin-700-normal.woff2", "Inter", INTER, "Geist Mono", GEIST, tsize=96),
    "p7": _t("#0E0E14", "#F2F2F7", "#F43F5E", "#3B82F6", "Audiowide", "audiowide-latin-400-normal.woff2", "Inter", INTER, "JetBrains Mono", JB, tsize=80, ls="0em", bigsize=140, wf=0.8),
    "p8": _t("#050816", "#E8F0FF", "#FDE047", "#F97316", "Space Grotesk", "space-grotesk-latin-700-normal.woff2", "Inter", INTER, "Geist Mono", GEIST, tsize=100),
    "p9": _t("#F1EFFF", "#17123A", "#6D28D9", "#0891B2", "Sora", "sora-latin-700-normal.woff2", "Work Sans", WORK, "DM Mono", DM, tsize=94, light=True),
}


def _lum(c):
    def ch(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = _hex(c)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _on(th):
    """Color de texto sobre el degradado acc→acc2: el que mejor contraste dé con el peor extremo."""
    cands = [th["bg"], th["ink"], "#FFFFFF", "#0A0A0A"]
    def cr(a, b):
        la, lb = _lum(a), _lum(b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
    return max(cands, key=lambda c: min(cr(c, th["acc"]), cr(c, th["acc2"])))


def _rgb(c):
    return "%d,%d,%d" % _hex(c)


def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def _marked(txt, cls="hl"):
    out = []
    for w in txt.split():
        if w.startswith("*"):
            out.append(f'<span class="{cls}">{w[1:]}</span>')
        else:
            out.append(w)
    return " ".join(out)


def _title_words(txt):
    out = []
    for w in txt.split():
        acc = w.startswith("*")
        w = w.lstrip("*")
        out.append(f'<span class="tm"><span class="tw{" ta" if acc else ""}">{w}</span></span>')
    return " ".join(out)


CHK = '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M5 12.5 L10 17 L19 7" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def _icon(name, th, size):
    svg = ICONS[name].replace('"A"', '"' + th["acc"] + '"').replace('"K"', '"' + th["ink"] + '"').replace('"B"', '"' + th["bg"] + '"')
    return f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">{svg}</svg>'


# =========================================================================== voz
# Pronunciación para voces nativas en español (es-MX-JorgeNeural): solo cambia lo que se lee, no lo que se ve.
PRON = [(r"\bexchanges?\b", "exchéinch"), (r"\bExchanges?\b", "Exchéinch"), (r"\bwallets?\b", "wálet"), (r"\bDCA\b", "de ce a"),
        (r"\bETFs?\b", "e te efe"), (r"\bCBDCs?\b", "ce be de ce"), (r"\bLightning\b", "Láitning"), (r"\btokenomics\b", "tokenómics"),
        (r"\btokenómics\b", "tokenómics"), (r"\bblockchain\b", "blokchéin"), (r"\bBlockchain\b", "Blokchéin")]


def voz_texto(txt):
    for a, b in PRON:
        txt = re.sub(a, b, txt)
    return txt


# =========================================================================== componentes
class Ctx:
    def __init__(self, th, words, scn, SC, END):
        self.th, self.words, self.scn, self.SC, self.END = th, words, scn, SC, END

    def kw(self, si, kw, text):
        a, b = self.scn[si]["start"], self.scn[si]["end"]
        t = None
        for k in dict.fromkeys([_norm(kw), _norm(voz_texto(kw))]):
            for w in self.words:
                if a - 0.4 <= w["start"] <= b + 0.4 and _norm(w["text"]).startswith(k[: max(3, len(k))]):
                    t = w["start"] - 0.15
                    break
            if t is not None:
                break
        k = _norm(kw)
        if t is None:
            pos = _norm(text).find(k)
            frac = pos / max(1, len(_norm(text))) if pos >= 0 else 0.3
            t = a + (b - a) * frac
        # nunca antes de que el título se acomode, y siempre con ≥2.6 s en pantalla antes del corte
        return round(min(max(t, self.floor(si)), self.limit(si)), 2)

    def floor(self, si):
        return (self.SC[0] + 4.7) if si == 0 else self.SC[si] + 1.7

    def limit(self, si):
        end = self.SC[si + 1] if si + 1 < len(self.SC) else self.END
        return max(self.floor(si), min(end - 3.0, self.floor(si) + 2.2))


def comp(c, cid, si, ctx, text):
    th, t = ctx.th, c["t"]
    T = lambda kw: ctx.kw(si, kw, text)  # noqa: E731
    last = [-9.0]

    def TS(kw):
        t = max(T(kw), last[0] + 0.45)
        last[0] = t
        return round(t, 2)
    H, J = "", ""
    if t == "bigword":
        tk = T(c["kw"])
        fs = min(th["bigsize"], int(860 / (0.66 * max(1, len(c["text"])))))
        H = f'<div class="x-big" id="{cid}"><span class="x-bigbg"></span><b style="font-size:{fs}px">{c["text"]}</b></div>'
        J = (f'tl.fromTo("#{cid}", {{ opacity: 0, scale: 1.5, rotation: -10 }}, {{ opacity: 1, scale: 1, rotation: -3, duration: 0.8, ease: "expo.out" }}, {tk:.2f});\n'
             f'tl.fromTo("#{cid} .x-bigbg", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, {tk:.2f});\n'
             f'tl.fromTo("#{cid}", {{ y: 0 }}, {{ y: -12, duration: 1.6, ease: "sine.inOut", yoyo: true, repeat: 1, immediateRender: false }}, {tk + 0.8:.2f});\n')
        return H, J, [(tk, "impact")]
    if t == "stat":
        tk = T(c["kw"])
        v = c["value"]
        fmt = f'(v) => "{c.get("prefix", "")}" + Math.round(v).toLocaleString("en-US") + "{c.get("suffix", "")}"'
        H = (f'<div class="x-glass x-stat" id="{cid}"><svg viewBox="0 0 120 120" width="190" height="190"><circle cx="60" cy="60" r="50" fill="none" stroke="rgba({_rgb(th["ink"])},0.12)" stroke-width="12"/>'
             f'<circle class="x-ring" cx="60" cy="60" r="50" fill="none" stroke="{th["acc"]}" stroke-width="12" stroke-linecap="round" transform="rotate(-90 60 60)"/></svg>'
             f'<div><b class="x-num" id="{cid}n">{c.get("prefix", "")}0{c.get("suffix", "")}</b><span>{c["label"]}</span></div></div>')
        J = (f'tl.fromTo("#{cid}", {{ opacity: 0, y: 70, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power3.out" }}, {tk:.2f});\n'
             f'tl.fromTo("#{cid} .x-ring", {{ strokeDasharray: 315, strokeDashoffset: 315 }}, {{ strokeDashoffset: 40, duration: 1.6, ease: "power2.inOut" }}, {tk + 0.2:.2f});\n'
             f'count("#{cid}n", {v}, 1.6, {tk + 0.2:.2f}, {fmt});\n')
        return H, J, [(tk, "pop"), (tk + 1.2, "ding")]
    if t == "checklist":
        rows, sf = "", []
        for k, (txt, ok, kw) in enumerate(c["items"]):
            tk = TS(kw)
            mark = ('<svg viewBox="0 0 40 40" width="44" height="44"><circle cx="20" cy="20" r="19" fill="' + (th["acc2"] if ok else "#E5484D") + '"/><path class="x-mk" d="'
                    + ("M11 21 L17 27 L29 14" if ok else "M13 13 L27 27 M27 13 L13 27") + '" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/></svg>')
            rows += f'<div class="x-glass x-row" id="{cid}r{k}">{mark}<span>{txt}</span></div>'
            J += (f'tl.fromTo("#{cid}r{k}", {{ opacity: 0, x: -90 }}, {{ opacity: 1, x: 0, duration: 0.7, ease: "power3.out" }}, {tk:.2f});\n'
                  f'tl.fromTo("#{cid}r{k} .x-mk", {{ strokeDasharray: 40, strokeDashoffset: 40 }}, {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }}, {tk + 0.35:.2f});\n')
            sf.append((tk, "tick" if ok else "stamp"))
        return f'<div class="x-col" id="{cid}">{rows}</div>', J, sf
    if t == "phone":
        rows, sf = "", []
        last[0] = ctx.floor(si) + 0.5
        for k, (a, b, kw) in enumerate(c["rows"]):
            tk = TS(kw)
            ok = "✓" in b
            b = b.replace("✓", "").strip()
            rows += f'<div class="x-noti" id="{cid}r{k}"><i></i><div><b>{a}</b><span>{b}</span></div>' + (f'<em class="x-ok">{CHK}</em>' if ok else "") + '</div>'
            J += f'tl.fromTo("#{cid}r{k}", {{ opacity: 0, y: -40, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "power3.out" }}, {tk:.2f});\n'
            sf.append((tk, "pop"))
        t0 = ctx.floor(si)
        H = f'<div class="x-phone" id="{cid}"><div class="x-notch"></div><div class="x-app mono">{c["app"]}</div>{rows}</div>'
        J = f'tl.fromTo("#{cid}", {{ opacity: 0, y: 140, rotationX: 25, transformPerspective: 1200 }}, {{ opacity: 1, y: 0, rotationX: 0, duration: 1.0, ease: "power3.out" }}, {t0:.2f});\n' + J
        return H, J, [(t0, "whoosh")] + sf
    if t == "chart":
        tk = T(c["kw"])
        pts = c["pts"]
        mx, mn = max(pts), min(pts)
        W, Hh = 820, 300
        xy = [(20 + i * (W - 40) / (len(pts) - 1), Hh - 20 - (p - mn) / max(1, mx - mn) * (Hh - 60)) for i, p in enumerate(pts)]
        d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in xy)
        area = d + f" L{xy[-1][0]:.0f} {Hh} L{xy[0][0]:.0f} {Hh} Z"
        col = "#E5484D" if c.get("down") else th["acc"]
        avg = ""
        if c.get("avg"):
            ay = sum(y for _, y in xy) / len(xy)
            avg = f'<line class="x-avg" x1="20" y1="{ay:.0f}" x2="{W - 20}" y2="{ay:.0f}" stroke="{th["acc2"]}" stroke-width="5" stroke-dasharray="14 10"/>'
        gid = cid + "g"
        H = (f'<div class="x-glass x-chart" id="{cid}"><svg viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}"><defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0.35"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>'
             f'<path class="x-area" d="{area}" fill="url(#{gid})"/><path class="x-line" d="{d}" fill="none" stroke="{col}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>{avg}'
             f'<circle class="x-dot" cx="{xy[-1][0]:.0f}" cy="{xy[-1][1]:.0f}" r="13" fill="{col}"/></svg><span class="x-tag" style="background:{col}">{c["label"]}</span></div>')
        J = (f'tl.fromTo("#{cid}", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, {tk - 0.3:.2f});\n'
             f'tl.fromTo("#{cid} .x-line", {{ strokeDasharray: 2000, strokeDashoffset: 2000 }}, {{ strokeDashoffset: 0, duration: 1.8, ease: "power1.inOut" }}, {tk:.2f});\n'
             f'tl.fromTo("#{cid} .x-area", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0 }}, {tk + 0.8:.2f});\n'
             f'tl.fromTo("#{cid} .x-dot", {{ scale: 0, svgOrigin: "{xy[-1][0]:.0f} {xy[-1][1]:.0f}" }}, {{ scale: 1, duration: 0.35, ease: "back.out(2)", svgOrigin: "{xy[-1][0]:.0f} {xy[-1][1]:.0f}" }}, {tk + 1.7:.2f});\n'
             f'tl.fromTo("#{cid} .x-tag", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "back.out(1.6)" }}, {tk + 1.8:.2f});\n')
        if avg:
            J += f'tl.fromTo("#{cid} .x-avg", {{ strokeDashoffset: 0, opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {tk + 1.6:.2f});\n'
        return H, J, [(tk, "riser"), (tk + 1.4, "pop")]
    if t == "compare":
        tk = T(c["kw"])
        win = c.get("win", "none")

        def card(side, data):
            ttl, lines = data
            w = " x-win" if win == side else ""
            return f'<div class="x-glass x-cmp{w}" id="{cid}{side[0]}"><b>{ttl}</b>' + "".join(f'<span>{ln}</span>' for ln in lines) + '</div>'
        H = f'<div class="x-pair" id="{cid}">{card("left", c["left"])}<div class="x-vs">VS</div>{card("right", c["right"])}</div>'
        J = (f'tl.fromTo("#{cid}l", {{ opacity: 0, x: -200, rotationY: 30, transformPerspective: 1000 }}, {{ opacity: 1, x: 0, rotationY: 0, duration: 0.85, ease: "power3.out" }}, {tk:.2f});\n'
             f'tl.fromTo("#{cid}r", {{ opacity: 0, x: 200, rotationY: -30, transformPerspective: 1000 }}, {{ opacity: 1, x: 0, rotationY: 0, duration: 0.85, ease: "power3.out" }}, {tk + 0.45:.2f});\n'
             f'tl.fromTo("#{cid} .x-vs", {{ opacity: 0, scale: 0.2, rotation: -90 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.7)" }}, {tk + 0.8:.2f});\n'
             f'tl.fromTo("#{cid} .x-cmp span", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.5, stagger: 0.18, ease: "power2.out" }}, {tk + 1.0:.2f});\n')
        if win in ("left", "right"):
            J += f'tl.fromTo("#{cid}{win[0]}", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.7, ease: "power2.out", immediateRender: false }}, {tk + 1.9:.2f});\n'
        return H, J, [(tk, "whoosh"), (tk + 0.45, "impact")]
    if t == "chips":
        H, sf = '<div class="x-chips" id="' + cid + '">', []
        for k, (txt, kw) in enumerate(c["items"]):
            tk = TS(kw)
            H += f'<span class="x-chip" id="{cid}k{k}">{txt}</span>'
            J += f'tl.fromTo("#{cid}k{k}", {{ opacity: 0, scale: 0.6, y: 30, rotation: {(-6 if k % 2 else 6)} }}, {{ opacity: 1, scale: 1, y: 0, rotation: 0, duration: 0.7, ease: "back.out(1.5)" }}, {tk:.2f});\n'
            sf.append((tk, "pop"))
        return H + "</div>", J, sf
    if t == "icons":
        H, sf = '<div class="x-icons" id="' + cid + '">', []
        for k, (ic, lab, kw) in enumerate(c["items"]):
            tk = TS(kw)
            H += f'<div class="x-glass x-ic" id="{cid}i{k}"><div class="x-icg">{_icon(ic, th, 120)}</div><b>{lab}</b></div>'
            J += (f'tl.fromTo("#{cid}i{k}", {{ opacity: 0, y: 80, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power3.out" }}, {tk:.2f});\n'
                  f'tl.fromTo("#{cid}i{k} .x-icg", {{ rotation: -20 }}, {{ rotation: 0, duration: 1.0, ease: "back.out(1.6)" }}, {tk + 0.1:.2f});\n')
            sf.append((tk, "pop"))
        return H + "</div>", J, sf
    if t == "timeline":
        n = len(c["items"])
        H, sf = f'<div class="x-glass x-tl" id="{cid}"><div class="x-tlbar"><i></i></div><div class="x-tln" style="grid-template-columns:repeat({n},1fr)">', []
        t0 = None
        for k, (a, b, kw) in enumerate(c["items"]):
            tk = TS(kw)
            t0 = tk if t0 is None else min(t0, tk)
            H += f'<div class="x-tlx" id="{cid}t{k}"><i></i><b>{a}</b><span>{b}</span></div>'
            J += f'tl.fromTo("#{cid}t{k}", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {tk:.2f});\n'
            sf.append((tk, "tick"))
        J = (f'tl.fromTo("#{cid}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {t0 - 0.5:.2f});\n'
             f'tl.fromTo("#{cid} .x-tlbar i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {max(0.8, sf[-1][0] - t0 + 0.4):.2f}, ease: "none" }}, {t0 - 0.2:.2f});\n') + J
        return H + "</div></div>", J, sf
    if t == "steps":
        H, sf = '<div class="x-steps" id="' + cid + '">', []
        for k, (txt, kw) in enumerate(c["items"]):
            tk = TS(kw)
            H += f'<div class="x-st" id="{cid}s{k}"><i>{k + 1}</i><b>{txt}</b></div>'
            J += (f'tl.fromTo("#{cid}s{k}", {{ opacity: 0, x: -70 }}, {{ opacity: 1, x: 0, duration: 0.7, ease: "power3.out" }}, {tk:.2f});\n'
                  f'tl.fromTo("#{cid}s{k} i", {{ backgroundColor: "rgba({_rgb(th["ink"])},0.08)", color: "{th["ink"]}" }}, {{ backgroundColor: "{th["acc"]}", color: "{th["on"]}", duration: 0.45, immediateRender: false }}, {tk + 0.3:.2f});\n')
            sf.append((tk, "tick"))
        return H + "</div>", J, sf
    if t == "quote":
        tk = T(c["kw"])
        H = f'<div class="x-quote" id="{cid}"><span class="x-qm">“</span><p>{_marked(c["text"], "x-qh")}</p></div>'
        J = (f'tl.fromTo("#{cid}", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.9, ease: "power3.out" }}, {tk:.2f});\n'
             f'tl.fromTo("#{cid} .x-qm", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.8, ease: "back.out(1.6)" }}, {tk + 0.1:.2f});\n'
             f'tl.fromTo("#{cid} .x-qh", {{ backgroundSize: "0% 40%" }}, {{ backgroundSize: "100% 40%", duration: 0.7, stagger: 0.2, ease: "power2.out" }}, {tk + 0.9:.2f});\n')
        return H, J, [(tk, "whoosh")]
    if t == "pie":
        tk = T(c["kw"])
        cols = [th["acc"], th["acc2"], _h(_mix(_hex(th["ink"]), _hex(th["bg"]), 0.45))]
        r, C = 80, 2 * math.pi * 80
        segs, leg, off = "", "", 0
        for k, (lab, v) in enumerate(c["parts"]):
            L = C * v / 100
            segs += f'<circle class="x-seg" id="{cid}p{k}" cx="110" cy="110" r="{r}" fill="none" stroke="{cols[k % 3]}" stroke-width="44" stroke-dasharray="{L:.1f} {C:.1f}" stroke-dashoffset="{-off:.1f}" transform="rotate(-90 110 110)"/>'
            leg += f'<div class="x-leg" id="{cid}l{k}"><i style="background:{cols[k % 3]}"></i><b>{v}%</b><span>{lab}</span></div>'
            off += L
            J += (f'tl.fromTo("#{cid}p{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, {tk + 0.45 * k:.2f});\n'
                  f'tl.fromTo("#{cid}l{k}", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {tk + 0.45 * k + 0.15:.2f});\n')
        H = f'<div class="x-glass x-pie" id="{cid}"><svg viewBox="0 0 220 220" width="300" height="300">{segs}</svg><div class="x-legs">{leg}</div></div>'
        J = f'tl.fromTo("#{cid}", {{ opacity: 0, scale: 0.85, rotation: -8 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.8, ease: "power3.out" }}, {tk - 0.3:.2f});\n' + J
        return H, J, [(tk, "pop"), (tk + 0.25, "tick"), (tk + 0.5, "tick")]
    if t == "channel":
        tk = T(c["kw"])
        H = (f'<div class="x-glass x-chan" id="{cid}"><div class="x-node">{c["a"]}</div><div class="x-pipe"><i></i>'
             + "".join(f'<u class="x-pk" id="{cid}k{k}">{c["pkt"]}</u>' for k in range(6))
             + f'</div><div class="x-node">{c["b"]}</div><div class="x-cnt mono">pagos: <b id="{cid}n">0</b></div></div>')
        J = (f'tl.fromTo("#{cid}", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }}, {tk - 0.4:.2f});\n'
             f'tl.fromTo("#{cid} .x-pipe i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.out" }}, {tk:.2f});\n')
        for k in range(6):
            fwd = k % 2 == 0
            J += f'tl.fromTo("#{cid}k{k}", {{ x: {0 if fwd else 420}, opacity: 0 }}, {{ keyframes: {{ x: [{0 if fwd else 420}, {420 if fwd else 0}], opacity: [1, 1, 0] }}, duration: 1.1, ease: "power1.inOut" }}, {tk + 0.6 + k * 0.6:.2f});\n'
        J += f'count("#{cid}n", 1000, 4.0, {tk + 0.6:.2f}, (v) => Math.round(v).toLocaleString("en-US"));\n'
        return H, J, [(tk, "whoosh")] + [(tk + 0.5 + k * 0.45, "tick") for k in range(6)]
    raise ValueError(t)


# =========================================================================== página
def _faces(th):
    return "\n".join(f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{fn}") format("{"woff2" if fn.endswith("woff2") else "truetype"}"); }}' for f, w, fn in th["fonts"])


def _split(txt):
    return [p for p in re.split(r"(?<=[.!?:])\s+", txt.strip()) if p]


def build(here, v):
    th = THEMES3[v["theme"]]
    th = dict(th, on=_on(th))
    install_fonts(here, dict(fonts=th["fonts"]))
    vz = json.load(open(os.path.join(here, "voz.json")))
    scn = vz["scenes"]
    words = json.load(open(os.path.join(here, "transcript.json"), encoding="utf-8")) if os.path.exists(os.path.join(here, "transcript.json")) else []
    SC = [0] + [round(s["start"] - 0.55, 2) for s in scn[1:]]
    END = round(vz["speech_end"] + 0.7, 2)
    DUR = round(max(56.0, END + 6.5), 2)
    ctx = Ctx(th, words, scn, SC, END)
    bg, ink, acc, acc2 = th["bg"], th["ink"], th["acc"], th["acc2"]
    B, I = _hex(bg), _hex(ink)
    card = "rgba(255,255,255,0.62)" if th["light"] else f"rgba({_rgb(_h(_mix(B, I, 0.10)))},0.55)"
    line = f"rgba({_rgb(ink)},{0.12 if th['light'] else 0.14})"
    muted = _h(_mix(B, I, 0.62))
    up = "uppercase" if th["upper"] else "none"
    labc = _h(_mix(_hex(acc), I, 0.35)) if th["light"] else acc
    scenes_h, js, sfx = "", "", [[0.0, "riser"]]
    n = len(v["scenes"])
    HK = 3.2  # fin del gancho
    # ---------------- escenas
    for si, sc in enumerate(v["scenes"]):
        a = SC[si]
        b = SC[si + 1] if si + 1 < n else END
        comps_h, comps_j = "", ""
        for ci, c in enumerate(sc["comps"]):
            h, j, s = comp(c, f"c{si}_{ci}", si, ctx, sc["v"])
            comps_h += h
            comps_j += j
            if s:  # un solo golpe suave por componente
                sfx.append([round(min(x for x, _ in s), 2), "pop"])
        tin = (HK - 0.2) if si == 0 else (a + 0.25)
        tdock = (HK + 0.7) if si == 0 else (a + 1.05)
        scenes_h += (f'      <div id="s{si + 1}" class="clip scene" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="1"><div class="cam" id="cam{si + 1}">\n'
                     f'        <div class="x-lab mono" id="lb{si}"><i></i>{si + 1:02d} — {sc["label"].upper()}</div>\n'
                     f'        <div class="x-ttl" id="tt{si}" data-layout-allow-overflow data-layout-allow-overlap><div class="x-tin">{_title_words(sc["title"])}</div></div>\n'
                     f'        <div class="x-stage">{comps_h}</div>\n      </div></div>\n')
        if si == 0:
            js += f'        tl.fromTo("#tt0", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {tin - 0.05:.2f});\n'
        js += (f'        tl.fromTo("#tt{si} .x-tin", {{ y: 520, scale: 1.1 }}, {{ y: 0, scale: 1, duration: 0.9, ease: "power3.inOut" }}, {tdock:.2f});\n'
               f'        tl.fromTo("#tt{si} .tw", {{ yPercent: 115, rotation: 4 }}, {{ yPercent: 0, rotation: 0, duration: 0.7, stagger: 0.07, ease: "power3.out" }}, {tin:.2f});\n'
               f'        tl.fromTo("#tt{si} .ta", {{ backgroundSize: "0% 100%", color: "{ink}" }}, {{ backgroundSize: "100% 100%", color: "{th["on"]}", duration: 0.6, stagger: 0.1, ease: "power2.out", immediateRender: false }}, {tin + 0.55:.2f});\n'
               f'        tl.fromTo("#lb{si}", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, {tdock + 0.3:.2f});\n'
               + "".join("        " + l + "\n" for l in comps_j.strip().split("\n") if l))
        if si > 0:
            js += f'        tl.fromTo("#cam{si + 1}", {{ opacity: 0, y: 90, scale: 0.97 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.75, ease: "power3.out" }}, {a:.2f});\n'
            sfx.append([round(a - 0.1, 2), "whoosh"])
        js += f'        tl.to("#cam{si + 1}", {{ opacity: 0, y: -70, scale: 0.98, duration: 0.45, ease: "power2.in" }}, {b - 0.45:.2f});\n'
        js += f'        tl.fromTo("#cam{si + 1} .x-stage", {{ scale: 1.0 }}, {{ scale: 1.03, duration: {max(1.0, b - a - 0.4):.2f}, ease: "none", immediateRender: false }}, {a + 0.2:.2f});\n'
    # ---------------- gancho (0 → HK): anillo que se dibuja, órbita, etiqueta, 3 palabras con entradas distintas, partículas
    hook = v["hook"]
    hfs = min(int(th["bigsize"] * 1.12), int(960 / (th["wf"] * max(len(w) for w in hook))))
    w2 = "".join(f'<span class="hc">{ch}</span>' for ch in hook[2])
    hook_h = (f'<div class="x-hw" id="hw0"><b style="font-size:{hfs}px">{hook[0]}</b></div>'
              f'<div class="x-hw" id="hw1"><span class="hbox"></span><b style="font-size:{hfs}px">{hook[1]}</b></div>'
              f'<div class="x-hw" id="hw2"><b style="font-size:{hfs}px">{w2}</b></div><div id="hbar"></div>')
    import random as _r
    rg = _r.Random(v["n"] * 101)
    parts, pj = "", ""
    for k in range(18):
        ang = k / 18 * 6.283 + rg.uniform(-0.15, 0.15)
        dist = rg.uniform(330, 520)
        dx, dy = math.cos(ang) * dist, math.sin(ang) * dist
        sz = rg.choice([12, 16, 22])
        col = acc if k % 2 == 0 else acc2
        shape = "50%" if k % 3 else "4px"
        parts += f'<i id="hp{k}" style="width:{sz}px;height:{sz}px;margin:-{sz // 2}px 0 0 -{sz // 2}px;border-radius:{shape};background:{col}"></i>'
        pj += (f'        tl.fromTo("#hp{k}", {{ x: 0, y: 0, scale: 0.3, rotation: 0 }}, {{ x: {dx:.0f}, y: {dy:.0f}, scale: 1, rotation: {rg.randint(-180, 180)}, duration: 1.6, ease: "power3.out" }}, 0.6);\n'
               f'        tl.fromTo("#hp{k}", {{ opacity: 0 }}, {{ keyframes: {{ opacity: [0, 1, 1, 0] }}, duration: 1.9, ease: "none" }}, 0.6);\n')
    orbit = "".join(f'<i style="transform:rotate({k * 30}deg) translateX(380px)"></i>' for k in range(12))
    js += ('        tl.fromTo("#hook", { opacity: 1 }, { opacity: 1, duration: 0.01 }, 0);\n'
           '        tl.fromTo("#hring .r1", { strokeDashoffset: 2400 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.out" }, 0.0);\n'
           '        tl.fromTo("#hring .r2", { strokeDashoffset: 1900 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.out" }, 0.2);\n'
           '        tl.fromTo("#hring", { rotation: -40, scale: 0.9 }, { rotation: 80, scale: 1.05, duration: HKD, ease: "none" }, 0);\n'
           '        tl.fromTo("#horbit", { rotation: 0, opacity: 0 }, { rotation: -90, opacity: 1, duration: HKD, ease: "none" }, 0.1);\n'
           '        tl.fromTo("#htag", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }, 0.1);\n'
           '        tl.fromTo("#hw0", { opacity: 0, x: -700, rotation: -6 }, { opacity: 1, x: 0, rotation: 0, duration: 0.7, ease: "power4.out" }, 0.15);\n'
           '        tl.fromTo("#hw1", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.6)" }, 0.55);\n'
           f'        tl.fromTo("#hw1 .hbox", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "power3.out" }}, 0.8);\n'
           f'        tl.fromTo("#hw1 b", {{ color: "{acc}" }}, {{ color: "{th["on"]}", duration: 0.4, ease: "none" }}, 0.9);\n'
           '        tl.fromTo("#hw2 .hc", { opacity: 0, yPercent: 110 }, { opacity: 1, yPercent: 0, duration: 0.6, stagger: 0.04, ease: "power3.out" }, 0.95);\n'
           '        tl.fromTo("#hbar", { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.inOut" }, 1.35);\n'
           '        tl.fromTo("#hookbox", { scale: 1 }, { scale: 1.05, duration: 1.4, ease: "sine.inOut", immediateRender: false }, 1.2);\n'
           '        tl.fromTo("#hw0", { x: 0, opacity: 1 }, { x: -900, opacity: 0, immediateRender: false, duration: 0.55, ease: "power3.in" }, 2.55);\n'
           '        tl.fromTo("#hw1", { scale: 1, opacity: 1 }, { scale: 1.5, opacity: 0, immediateRender: false, duration: 0.55, ease: "power3.in" }, 2.6);\n'
           '        tl.fromTo("#hw2", { x: 0, opacity: 1 }, { x: 900, opacity: 0, immediateRender: false, duration: 0.55, ease: "power3.in" }, 2.65);\n'
           '        tl.fromTo("#hbar", { scaleX: 1 }, { scaleX: 0, immediateRender: false, duration: 0.4, ease: "power2.in" }, 2.55);\n'
           '        tl.fromTo("#hring", { opacity: 1 }, { scale: 2.0, opacity: 0, immediateRender: false, duration: 0.6, ease: "power2.in" }, 2.6);\n'
           '        tl.fromTo("#horbit", { opacity: 1 }, { opacity: 0, immediateRender: false, duration: 0.4 }, 2.6);\n'
           '        tl.fromTo("#htag", { opacity: 1, y: 0 }, { opacity: 0, y: -30, immediateRender: false, duration: 0.4, ease: "power2.in" }, 2.6);\n'
           f'        tl.set("#hook", {{ opacity: 0 }}, {HK:.2f});\n').replace("HKD", f"{HK:.2f}") + pj
    sfx += [[0.6, "impact"], [2.55, "whoosh"]]
    hook_html = (f'<div id="hook" data-layout-allow-overlap data-layout-allow-overflow class="clip" data-start="0" data-duration="{HK:.2f}" data-track-index="4">'
                 f'<svg id="hring" viewBox="0 0 900 900" width="900" height="900"><circle class="r1" cx="450" cy="450" r="380" fill="none" stroke="{acc}" stroke-opacity="0.55" stroke-width="4" stroke-dasharray="2400" stroke-linecap="round"/>'
                 f'<circle class="r2" cx="450" cy="450" r="300" fill="none" stroke="{acc2}" stroke-opacity="0.45" stroke-width="3" stroke-dasharray="10 16"/></svg>'
                 f'<div id="horbit">{orbit}</div><div id="hparts">{parts}</div>'
                 f'<div id="htag" class="mono">WEB3 EN 60 SEGUNDOS · N.º {v["n"]:02d}</div><div id="hookbox">{hook_h}</div></div>')
    # ---------------- HUD
    rail = "".join(f'<i id="rl{k}"></i>' for k in range(n))
    for k in range(n):
        a = SC[k]
        js += f'        tl.fromTo("#rl{k}", {{ height: 14, backgroundColor: "rgba({_rgb(ink)},0.25)" }}, {{ height: 54, backgroundColor: "{acc}", duration: 0.6, ease: "power3.out" }}, {(HK if k == 0 else a + 0.2):.2f});\n'
        js += f'        tl.to("#rl{k}", {{ height: 14, backgroundColor: "rgba({_rgb(ink)},0.25)", duration: 0.4 }}, {(SC[k + 1] if k + 1 < n else END):.2f});\n'
        js += f'        tl.set("#hudn", {{ textContent: "{k + 1:02d} / {n:02d}" }}, {a + 0.05:.2f});\n'
    js += f'        tl.fromTo("#hud", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, {HK:.2f});\n'
    js += f'        tl.to("#hud", {{ opacity: 0, duration: 0.4 }}, {END - 0.3:.2f});\n'
    # ---------------- subtítulos
    cues = []
    for si, sc in enumerate(v["scenes"]):
        a0, b0 = scn[si]["start"] - 0.2, scn[si]["end"] + 0.15
        sents = _split(sc["en"])
        tot = sum(len(s) for s in sents)
        t = a0
        for s in sents:
            d = (b0 - a0) * len(s) / tot
            cues.append((round(t, 2), round(t + d, 2), s))
            t += d
    cues_h = "\n".join(f'      <div class="x-cue clip" id="cue{i}" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="9"><span>{s}</span></div>' for i, (a, b, s) in enumerate(cues))
    for i, (a, b, s) in enumerate(cues):
        js += f'        tl.fromTo("#cue{i} span", {{ opacity: 0, y: 12 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {a:.2f});\n'
    # ---------------- flyer final
    ttl = v["title"]
    tlen = len(ttl.replace("*", ""))
    fsize = max(60, min(140, int(th["tsize"] * 1.5), int(th["tsize"] * 1.5 * 24 / max(24, tlen))))
    pts = "".join(f'<div class="x-fp" id="fp{k}"><i>{CHK}</i>{p}</div>' for k, p in enumerate(v["points"]))
    flyer = (f'      <div id="flyer" class="clip" data-start="{END}" data-duration="{DUR - END:.2f}" data-track-index="8">\n'
             f'        <div id="fbg"></div><div class="fblob" id="fb1" data-layout-allow-overflow></div><div class="fblob" id="fb2" data-layout-allow-overflow></div>\n'
             f'        <div id="fcard"><div id="fser" class="mono">WEB3 EN 60 SEGUNDOS · N.º {v["n"]:02d}</div>\n'
             f'          <div id="ftitle" style="font-size:{fsize}px">{_marked(ttl, "fhl")}</div>\n'
             f'          <div id="fsub">{v["sub"]}</div><div id="fpts">{pts}</div>\n'
             f'          <div id="fhandle"><span class="ig"><i></i><u></u></span><b>{FIRMA}</b></div>\n'
             f'          <div id="fcta">SÍGUEME PARA MÁS</div></div>\n      </div>\n')
    js += (f'        tl.fromTo("#fbg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {END:.2f});\n'
           f'        tl.fromTo(".fblob", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 1.2, stagger: 0.15, ease: "expo.out" }}, {END:.2f});\n'
           f'        tl.fromTo("#fser", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {END + 0.2:.2f});\n'
           f'        tl.fromTo("#ftitle", {{ opacity: 0, y: 80, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "expo.out" }}, {END + 0.35:.2f});\n'
           f'        tl.fromTo("#ftitle .fhl", {{ backgroundSize: "0% 34%" }}, {{ backgroundSize: "100% 34%", duration: 0.5, stagger: 0.1, ease: "power3.out" }}, {END + 0.9:.2f});\n'
           f'        tl.fromTo("#fsub", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, {END + 0.8:.2f});\n'
           f'        tl.fromTo(".x-fp", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, stagger: 0.1, ease: "back.out(2)" }}, {END + 1.1:.2f});\n'
           f'        tl.fromTo("#fhandle", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.8)" }}, {END + 1.6:.2f});\n'
           f'        tl.fromTo("#fcta", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.4)" }}, {END + 1.9:.2f});\n'
           f'        tl.fromTo("#fcta", {{ boxShadow: "0 0 0px rgba({_rgb(acc)},0)" }}, {{ boxShadow: "0 0 70px rgba({_rgb(acc)},0.75)", duration: 0.8, yoyo: true, repeat: 1, ease: "sine.inOut", immediateRender: false }}, {END + 2.4:.2f});\n')
    sfx += [[END - 0.6, "riser"], [END, "impact"]]
    # ---------------- CSS
    css = f'''
{_faces(th)}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {bg}; }}
      body {{ font-family: "{th["fb"]}", sans-serif; color: {ink}; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: {bg}; }}
      .scene, .cam {{ position: absolute; inset: 0; }}
      .mono {{ font-family: "{th["fm"]}", monospace; font-weight: 700; }}
      #mesh {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      #grainc {{ position: absolute; inset: 0; pointer-events: none; opacity: {0.07 if th["light"] else 0.1}; mix-blend-mode: overlay; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='220' height='220' filter='url(%23n)'/></svg>"); }}
      /* HUD */
      #hud {{ position: absolute; left: 60px; right: 60px; top: 250px; display: flex; justify-content: space-between; align-items: center; }}
      #hudp {{ display: flex; align-items: center; gap: 12px; padding: 10px 18px; border-radius: 999px; background: {card}; border: 1px solid {line}; font-size: 20px; letter-spacing: 0.18em; }}
      #hudp i {{ width: 12px; height: 12px; border-radius: 50%; background: {acc}; box-shadow: 0 0 14px {acc}; }}
      #hudn {{ font-size: 22px; letter-spacing: 0.2em; color: {muted}; }}
      #rail {{ position: absolute; left: 26px; top: 760px; display: flex; flex-direction: column; gap: 10px; }}
      #rail i {{ display: block; width: 6px; height: 14px; border-radius: 3px; background: rgba({_rgb(ink)},0.25); }}
      /* títulos */
      .x-lab {{ position: absolute; left: 70px; top: 330px; display: flex; align-items: center; gap: 12px; font-size: 22px; letter-spacing: 0.22em; color: {labc}; }}
      .x-lab i {{ width: 30px; height: 3px; background: {acc}; }}
      .x-ttl {{ position: absolute; left: 60px; right: 60px; top: 376px; height: 230px; }}
      .x-tin {{ font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: {th["tsize"]}px; line-height: {th.get("lh", 1.04)}; letter-spacing: {th["ls"]}; text-transform: {up}; color: {ink}; transform-origin: 50% 0%; }}
      .tm {{ display: inline-block; overflow: hidden; vertical-align: top; padding: 0.1em 0.04em 0.06em; margin-top: -0.1em; }}
      .tw {{ display: inline-block; }}
      .ta {{ color: {th["on"]}; padding: 0 0.12em; border-radius: 0.12em; background-image: linear-gradient(100deg, {acc}, {acc2}); background-repeat: no-repeat; background-size: 100% 100%; }}
      /* escenario */
      .x-orb {{ position: absolute; left: 140px; top: 620px; }}
      .x-stage {{ position: absolute; left: 70px; right: 70px; top: 640px; height: 760px; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 26px; transform-origin: 50% 50%; }}
      .x-glass {{ background: {card}; border: 1px solid {line}; border-radius: 30px; box-shadow: 0 30px 70px rgba(0,0,0,{0.10 if th["light"] else 0.35}), inset 0 1px 0 rgba(255,255,255,{0.6 if th["light"] else 0.08}); backdrop-filter: blur(18px); }}
      .x-big {{ position: relative; padding: 10px 40px; }}
      .x-big b {{ position: relative; z-index: 1; font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: {th["bigsize"]}px; line-height: 1; letter-spacing: {th["ls"]}; color: {th["on"]}; white-space: nowrap; }}
      .x-bigbg {{ position: absolute; inset: 0; border-radius: 26px; background: linear-gradient(110deg, {acc}, {acc2}); transform-origin: left center; box-shadow: 0 20px 60px rgba({_rgb(acc)},0.45); }}
      .x-stat {{ display: flex; align-items: center; gap: 40px; padding: 40px 56px; min-width: 860px; }}
      .x-num {{ display: block; font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 120px; line-height: 1; color: {ink}; letter-spacing: {th["ls"]}; white-space: nowrap; }}
      .x-stat span {{ display: block; margin-top: 8px; font-size: 30px; font-weight: 700; color: {muted}; }}
      .x-col {{ width: 100%; display: flex; flex-direction: column; gap: 18px; }}
      .x-row {{ display: flex; align-items: center; gap: 26px; padding: 32px 34px; font-size: 44px; font-weight: 700; }}
      .x-phone {{ position: relative; width: 540px; height: 740px; border-radius: 64px; border: 10px solid {ink}; background: {card}; padding: 110px 26px 26px; display: flex; flex-direction: column; gap: 18px; box-shadow: 0 40px 90px rgba(0,0,0,{0.15 if th["light"] else 0.5}); }}
      .x-notch {{ position: absolute; left: 195px; top: 20px; width: 130px; height: 32px; border-radius: 16px; background: {ink}; }}
      .x-app {{ position: absolute; left: 34px; top: 66px; font-size: 22px; letter-spacing: 0.15em; color: {acc}; }}
      .x-noti {{ display: flex; align-items: center; gap: 16px; padding: 18px 20px; border-radius: 22px; background: rgba({_rgb(ink)},0.06); border: 1px solid {line}; }}
      .x-noti i {{ flex: none; width: 48px; height: 48px; border-radius: 14px; background: linear-gradient(135deg, {acc}, {acc2}); }}
      .x-ok {{ margin-left: auto; flex: none; width: 40px; height: 40px; border-radius: 50%; background: {acc2}; color: {bg}; display: flex; align-items: center; justify-content: center; }}
      .x-noti b {{ display: block; font-size: 32px; }} .x-noti span {{ font-size: 27px; color: {muted}; }}
      .x-chart {{ position: relative; padding: 30px; }}
      .x-tag {{ position: absolute; right: 30px; top: 22px; padding: 10px 18px; border-radius: 999px; color: #fff; font-weight: 800; font-size: 26px; }}
      .x-pair {{ width: 100%; display: flex; align-items: stretch; gap: 0; position: relative; }}
      .x-cmp {{ flex: 1; padding: 50px 30px; display: flex; flex-direction: column; gap: 12px; text-align: center; }}
      .x-cmp b {{ font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 54px; line-height: 1.05; letter-spacing: {th["ls"]}; text-transform: {up}; }}
      .x-cmp span {{ font-size: 36px; font-weight: 700; color: {muted}; }}
      .x-win {{ border: 3px solid {acc}; box-shadow: 0 0 60px rgba({_rgb(acc)},0.35); }} .x-win b {{ color: {labc}; }}
      .x-vs {{ position: relative; z-index: 2; flex: none; align-self: center; width: 96px; height: 96px; margin: 0 -26px; border-radius: 50%; background: linear-gradient(135deg, {acc}, {acc2}); color: {th["on"]}; display: flex; align-items: center; justify-content: center; font-family: "{th["fm"]}", monospace; font-weight: 700; font-size: 30px; }}
      .x-chips {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 16px; }}
      .x-chip {{ padding: 22px 34px; border-radius: 999px; background: linear-gradient(110deg, {acc}, {acc2}); color: {th["on"]}; font-weight: 800; font-size: 38px; }}
      .x-icons {{ width: 100%; display: flex; gap: 20px; }}
      .x-ic {{ flex: 1; padding: 30px 16px; display: flex; flex-direction: column; align-items: center; gap: 16px; text-align: center; }} .x-ic b {{ font-size: 32px; line-height: 1.15; }}
      .x-tl {{ width: 100%; padding: 36px 30px 30px; position: relative; }}
      .x-tlbar {{ position: absolute; left: 50px; right: 50px; top: 58px; height: 6px; border-radius: 3px; background: rgba({_rgb(ink)},0.12); }}
      .x-tlbar i {{ position: absolute; inset: 0; border-radius: 3px; background: linear-gradient(90deg, {acc}, {acc2}); transform-origin: left center; }}
      .x-tln {{ display: grid; gap: 10px; }} .x-tlx {{ display: flex; flex-direction: column; align-items: center; gap: 10px; text-align: center; }}
      .x-tlx i {{ width: 30px; height: 30px; border-radius: 50%; background: {acc}; border: 6px solid {bg}; box-shadow: 0 0 0 3px {acc}; }}
      .x-tlx b {{ font-family: "{th["fm"]}", monospace; font-size: 28px; }} .x-tlx span {{ font-size: 24px; font-weight: 700; color: {muted}; line-height: 1.2; }}
      .x-steps {{ width: 100%; display: flex; flex-direction: column; gap: 16px; }}
      .x-st {{ display: flex; align-items: center; gap: 26px; padding: 26px 30px; border-radius: 26px; background: {card}; border: 1px solid {line}; }}
      .x-st i {{ flex: none; width: 64px; height: 64px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-style: normal; font-family: "{th["fm"]}", monospace; font-size: 30px; background: rgba({_rgb(ink)},0.08); }}
      .x-st b {{ font-size: 48px; }}
      .x-quote {{ position: relative; padding: 20px 30px; text-align: center; }}
      .x-qm {{ display: block; font-family: "{th["fd"]}", serif; font-size: 200px; line-height: 0.7; color: {acc}; }}
      .x-quote p {{ font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 74px; line-height: 1.12; letter-spacing: {th["ls"]}; text-transform: {up}; }}
      .x-qh {{ background-image: linear-gradient({acc}, {acc}); background-repeat: no-repeat; background-position: 0 88%; background-size: 0% 40%; }}
      .x-pie {{ display: flex; align-items: center; gap: 36px; padding: 30px 40px; }} .x-legs {{ display: flex; flex-direction: column; gap: 16px; }}
      .x-leg {{ display: flex; align-items: center; gap: 14px; font-size: 32px; }} .x-leg i {{ width: 26px; height: 26px; border-radius: 8px; }} .x-leg b {{ min-width: 80px; }} .x-leg span {{ color: {muted}; font-weight: 700; }}
      .x-chan {{ width: 100%; padding: 40px 30px 30px; display: flex; align-items: center; justify-content: space-between; position: relative; flex-wrap: wrap; }}
      .x-node {{ width: 170px; height: 170px; border-radius: 50%; background: linear-gradient(135deg, {acc}, {acc2}); color: {th["on"]}; display: flex; align-items: center; justify-content: center; text-align: center; font-weight: 800; font-size: 30px; padding: 12px; }}
      .x-pipe {{ position: relative; flex: 1; height: 120px; margin: 0 10px; }}
      .x-pipe i {{ position: absolute; left: 0; right: 0; top: 54px; height: 12px; border-radius: 6px; background: rgba({_rgb(ink)},0.15); transform-origin: left center; }}
      .x-pk {{ position: absolute; left: 0; top: 34px; padding: 8px 14px; border-radius: 999px; background: {ink}; color: {bg}; font-weight: 800; font-size: 24px; text-decoration: none; white-space: nowrap; }}
      .x-cnt {{ width: 100%; margin-top: 18px; text-align: center; font-size: 28px; color: {muted}; }} .x-cnt b {{ color: {acc}; }}
      /* gancho */
      #hook {{ position: absolute; inset: 0; }}
      #hookbox {{ position: absolute; left: 0; right: 0; top: 560px; height: 680px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; }}
      .x-hw b {{ display: block; font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: {int(th["bigsize"] * 1.12)}px; line-height: 1.02; letter-spacing: {th["ls"]}; color: {ink}; white-space: nowrap; text-transform: uppercase; }}
      #hw1 {{ position: relative; padding: 0 30px; }} #hw1 b {{ position: relative; color: {acc}; }}
      .hbox {{ position: absolute; inset: 6px 0; border-radius: 22px; background: linear-gradient(110deg, {acc}, {acc2}); transform-origin: left center; box-shadow: 0 20px 60px rgba({_rgb(acc)},0.4); }}
      .hc {{ display: inline-block; }}
      #hw2 b {{ overflow: hidden; padding: 0.05em 0; }}
      #hbar {{ width: 520px; height: 12px; margin-top: 18px; border-radius: 6px; background: linear-gradient(90deg, {acc}, {acc2}); transform-origin: center; }}
      #hring {{ position: absolute; left: 90px; top: 450px; }}
      #horbit {{ position: absolute; left: 540px; top: 900px; width: 0; height: 0; }}
      #horbit i {{ position: absolute; left: -6px; top: -6px; width: 12px; height: 12px; border-radius: 50%; background: {acc2}; opacity: 0.8; }}
      #hparts {{ position: absolute; left: 540px; top: 900px; width: 0; height: 0; }}
      #hparts i {{ position: absolute; left: 0; top: 0; opacity: 0; }}
      #htag {{ position: absolute; left: 0; right: 0; top: 380px; margin: 0 auto; width: max-content; padding: 12px 22px; border-radius: 999px; border: 2px solid {acc}; color: {ink}; font-size: 24px; letter-spacing: 0.2em; background: {card}; }}
      #rays {{ position: absolute; left: 540px; top: 900px; width: 0; height: 0; }}
      #rays i {{ position: absolute; left: 0; top: -4px; width: 900px; height: 8px; transform-origin: 0 50%; }}
      #rays u {{ position: absolute; left: 160px; top: 0; width: 740px; height: 8px; border-radius: 4px; background: linear-gradient(90deg, rgba({_rgb(acc)},0.9), rgba({_rgb(acc2)},0)); transform-origin: 0 50%; }}
      #flash {{ position: absolute; inset: 0; background: {"#ffffff" if not th["light"] else acc}; opacity: 0; }}
      #streak {{ position: absolute; left: 0; top: -200px; width: 260px; height: 2400px; transform: rotate(14deg); background: linear-gradient(90deg, transparent, rgba({_rgb(acc)},0.55), rgba(255,255,255,0.6), rgba({_rgb(acc2)},0.55), transparent); }}
      /* subtítulos */
      .x-cue {{ position: absolute; left: 70px; right: 70px; top: 1488px; display: flex; justify-content: center; }}
      .x-cue span {{ display: block; max-width: 940px; text-align: center; font-family: "Inter", sans-serif; font-weight: 700; font-size: 38px; line-height: 1.3; color: #fff; padding: 14px 26px; border-radius: 20px; background: rgba(10,10,14,0.62); }}
      /* flyer */
      #fbg {{ position: absolute; inset: 0; background: radial-gradient(ellipse 90% 60% at 50% 40%, rgba({_rgb(acc)},{0.18 if th["light"] else 0.28}), {bg} 70%); }}
      .fblob {{ position: absolute; border-radius: 50%; filter: blur(60px); }}
      #fb1 {{ left: -120px; top: 260px; width: 560px; height: 560px; background: rgba({_rgb(acc)},0.45); }}
      #fb2 {{ right: -140px; top: 980px; width: 600px; height: 600px; background: rgba({_rgb(acc2)},0.40); }}
      #fcard {{ position: absolute; left: 70px; right: 70px; top: 300px; height: 1200px; padding: 60px 54px; border-radius: 48px; background: {card}; border: 1px solid {line}; backdrop-filter: blur(24px);
        box-shadow: 0 40px 100px rgba(0,0,0,{0.12 if th["light"] else 0.45}); display: flex; flex-direction: column; align-items: flex-start; gap: 28px; }}
      #fser {{ padding: 10px 18px; border-radius: 999px; background: rgba({_rgb(acc)},0.15); border: 2px solid {acc}; color: {ink}; font-size: 22px; letter-spacing: 0.18em; }}
      #ftitle {{ font-family: "{th["fd"]}", sans-serif; font-weight: 800; line-height: {max(1.05, th["lh"])}; letter-spacing: {th["ls"]}; text-transform: {up}; color: {ink}; }}
      .fhl {{ background-image: linear-gradient(100deg, rgba({_rgb(acc)},0.85), rgba({_rgb(acc2)},0.85)); background-repeat: no-repeat; background-position: 0 85%; background-size: 100% 34%; }}
      #fsub {{ font-size: 40px; font-weight: 700; color: {muted}; }}
      #fpts {{ width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 10px; }}
      .x-fp {{ display: flex; align-items: center; gap: 14px; padding: 26px 22px; border-radius: 22px; background: rgba({_rgb(ink)},0.06); border: 1px solid {line}; font-size: 32px; font-weight: 700; }}
      .x-fp i {{ flex: none; width: 36px; height: 36px; border-radius: 50%; background: {acc}; color: {bg}; display: flex; align-items: center; justify-content: center; font-style: normal; font-size: 22px; }}
      #fhandle {{ margin-top: auto; display: flex; align-items: center; gap: 20px; }}
      #fhandle b {{ font-family: "Inter", sans-serif; font-weight: 800; font-size: 60px; letter-spacing: -0.02em; color: {ink}; }}
      .ig {{ position: relative; flex: none; width: 84px; height: 84px; border-radius: 24px; background: linear-gradient(45deg, #F58529, #DD2A7B 45%, #8134AF 75%, #515BD4); }}
      .ig i {{ position: absolute; left: 21px; top: 21px; width: 42px; height: 42px; border-radius: 50%; border: 6px solid #fff; }}
      .ig u {{ position: absolute; right: 15px; top: 13px; width: 10px; height: 10px; border-radius: 50%; background: #fff; }}
      #fcta {{ align-self: stretch; padding: 30px; text-align: center; border-radius: 26px; background: linear-gradient(110deg, {acc}, {acc2}); color: {th["on"]}; font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 44px; letter-spacing: {th["ls"]}; text-transform: uppercase; }}
'''
    # ---------------- fondo malla
    blobs = [(acc, 0.22 if th["light"] else 0.30, 220, 520, 640), (acc2, 0.20 if th["light"] else 0.26, 880, 1300, 660), (acc, 0.16, 760, 300, 480), (acc2, 0.14, 180, 1620, 560)]
    bl_js = "[" + ", ".join(f'["{_rgb(c)}", {a}, {x}, {y}, {r}]' for c, a, x, y, r in blobs) + "]"
    sh_col = f"rgba({_rgb(ink)},{0.10 if th['light'] else 0.12})"
    bg_js = """
        const mc = document.getElementById("mesh"), mg = mc.getContext("2d");
        const BL = BLJS;
        const SH = []; for (let i = 0; i < 14; i++) SH.push({ x: R() * 1080, y: R() * 1920, s: 14 + R() * 30, k: i % 3, sp: 8 + R() * 18, r: R() * 6 });
        function bg(t) {
          mg.fillStyle = "BGC"; mg.fillRect(0, 0, 1080, 1920);
          BL.forEach((b, i) => { const x = b[2] + Math.sin(t * 0.21 + i * 1.7) * 160, y = b[3] + Math.cos(t * 0.17 + i) * 200;
            const gr = mg.createRadialGradient(x, y, 0, x, y, b[4]); gr.addColorStop(0, "rgba(" + b[0] + "," + b[1] + ")"); gr.addColorStop(1, "rgba(" + b[0] + ",0)");
            mg.fillStyle = gr; mg.fillRect(0, 0, 1080, 1920); });
          mg.lineWidth = 3; mg.strokeStyle = "SHC";
          for (const s of SH) { const y = ((s.y - t * s.sp) % 2040 + 2040) % 2040 - 60, x = s.x + Math.sin(t * 0.5 + s.r) * 30;
            mg.save(); mg.translate(x, y); mg.rotate(t * 0.4 + s.r);
            if (s.k === 0) { mg.strokeRect(-s.s / 2, -s.s / 2, s.s, s.s); } else if (s.k === 1) { mg.beginPath(); mg.arc(0, 0, s.s / 2, 0, 6.283); mg.stroke(); } else { mg.beginPath(); mg.moveTo(0, -s.s / 2); mg.lineTo(s.s / 2, s.s / 2); mg.lineTo(-s.s / 2, s.s / 2); mg.closePath(); mg.stroke(); }
            mg.restore(); }
        }
        const st = { t: 0 }; bg(0); tl.to(st, { t: DUR, duration: DUR, ease: "none", onUpdate: () => bg(st.t) }, 0);
""".replace("BLJS", bl_js).replace("BGC", bg).replace("SHC", sh_col)
    top = r'''
        function mulberry32(a) { return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
        const R = mulberry32(31);
        const tl = gsap.timeline({ paused: true });
        const count = (sel, to, dur, at, fmt) => { const o = { v: 0 }; const el = document.querySelector(sel);
          tl.fromTo(o, { v: 0 }, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v); } }, at); };
'''
    js_all = top + f"        const DUR = {DUR};\n" + bg_js + js + '        \n        window.__timelines = window.__timelines || {};\n        window.__timelines["main"] = tl;\n'
    html = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{css}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="bgClip" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0"><canvas id="mesh" width="1080" height="1920"></canvas></div>
{scenes_h}
      <div id="hudClip" class="clip" data-start="0" data-duration="{END:.2f}" data-track-index="3"><div id="hud"><div id="hudp" class="mono"><i></i>WEB3 EN 60s</div><div id="hudn" class="mono">01 / {n:02d}</div></div><div id="rail">{rail}</div></div>
      {hook_html}
{flyer}
      <div id="grainClip" class="clip" data-start="0" data-duration="{DUR}" data-track-index="7"><div id="grainc"></div></div>
{cues_h}
      <audio id="vo" src="assets/voz.wav" data-start="0" data-duration="{DUR}" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/musica.wav" data-start="0" data-duration="{DUR}" data-track-index="11" data-volume="0.24"></audio>
      <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="{DUR}" data-track-index="12" data-volume="0.35"></audio>
    </div>
    <script>
      (function () {{{js_all}      }})();
    </script>
  </body>
</html>
'''
    open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"dur": DUR, "cuts": SC + [END, DUR], "sfx": sorted(sfx)}, open(os.path.join(here, "timing.json"), "w"))
    print("index.html listo", DUR, SC, END)
