"""Serie "Web3 desde cero" v2 para @tu_usuario — sistema de temas por video (HyperFrames, 1080x1920).

Diferencias con alfa_brand.py (v1):
- SIN logotipo α ni identidad del portafolio: cada video tiene su PROPIO tema (paleta, tipografías, glifo, subrayado).
  La firma final es tipográfica: "@tu_usuario" + índice de la serie con el capítulo actual resaltado.
- Titulares letra por letra (máscara + rotationX + blur), capítulo con barra de progreso segmentada,
  grano animado, viñeta, barrido de luz en cada corte, ráfagas (bursts) en momentos clave.
- retheme(): recolorea automáticamente el HTML/CSS/JS de las escenas escritas con la paleta v1
  (rojo #FF2A4D / negro #0A0708 / hueso #f3eeef) al tema elegido, y cambia Syne/Plex/Public Sans/AlfaSerif por las fuentes del tema.

Uso (build.py):
    from serie_v2 import page, scene, THEMES, install_fonts
    TH = THEMES["tokens"]; install_fonts(HERE, TH)
    html = page(TH, dur, sc, eyes, heads, cues, scenes_html, scene_css, scene_js, bg_html, bg_js, tx_html, tx_js,
                end_at, part=4, cta="SÍGUEME PARA LA PARTE 5", bursts=[(t, x, y), ...])
Retícula: capítulo 252, titular 330-560, escenario 600-1360, subtítulos 1486+.
NOMBRES RESERVADOS (no usarlos en las escenas, chocan con el chrome): ids e0-e9, h0-h9, cue*, bu*, k0-k3, s1-s6, cam*,
sweep, grain, vig, endbg, endc, etake, cta, ghostc; clases .ch .w .wm .ul .seg .enum .esep .head .display .eyebrow .cue
.burst .corner .erow .ering .ename .eseries. Videos nuevos: pasar recolor=False y escribir los colores del tema directo.
"""
import os as _os
FIRMA = _os.environ.get("FIRMA_REDES", "@tu_usuario")

import json
import os
import re
import shutil

SERIES = ["De Web1 a Web3", "Blockchain", "Wallets y llaves", "Tokens, NFTs y contratos", "DAOs"]

# (familia, rango de peso, archivo)
THEMES = {
    "web": dict(name="Cobalto editorial", bg="#060A1C", ink="#EEF1FF", acc="#5B8CFF", glyph="3",
                fd="Anton", fb="Inter", fm="JetBrains Mono", upper=True, hsize=112, hls="0.01em", lh=1.0, ul="mark", cue="bar", esize=128,
                fonts=[("Anton", "100 900", "anton-latin-400-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                       ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("JetBrains Mono", "100 550", "JetBrainsMono-400.woff2"),
                       ("JetBrains Mono", "551 900", "JetBrainsMono-700.woff2")]),
    "blockchain": dict(name="Terminal lima", bg="#050805", ink="#ECF7E8", acc="#B6FF3B", glyph="#",
                       fd="Space Grotesk", fb="Inter", fm="Geist Mono", upper=False, hsize=88, hls="-0.035em", lh=1.0, ul="bar", cue="pill", esize=104,
                       fonts=[("Space Grotesk", "100 900", "space-grotesk-latin-700-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                              ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("Geist Mono", "100 550", "GeistMono-Regular.ttf"),
                              ("Geist Mono", "551 900", "GeistMono-Bold.ttf")]),
    "wallets": dict(name="Bóveda dorada", bg="#0D0920", ink="#F4F0FF", acc="#FFC53D", glyph="✓",
                    fd="Bricolage Grotesque", fb="Instrument Sans", fm="Red Hat Mono", upper=False, hsize=90, hls="-0.03em", lh=1.0, ul="mark", cue="bar", esize=108,
                    fonts=[("Bricolage Grotesque", "100 900", "BricolageGrotesque-Bold.ttf"), ("Instrument Sans", "100 550", "InstrumentSans-Regular.ttf"),
                           ("Instrument Sans", "551 900", "InstrumentSans-Bold.ttf"), ("Red Hat Mono", "100 550", "RedHatMono-Regular.ttf"),
                           ("Red Hat Mono", "551 900", "RedHatMono-Bold.ttf")]),
    "tokens": dict(name="Menta profunda", bg="#031417", ink="#E8FFF8", acc="#2EF2B4", glyph="T",
                   fd="Outfit", fb="Sora", fm="DM Mono", upper=False, hsize=104, hls="-0.03em", lh=1.0, ul="bar", cue="pill", esize=110,
                   fonts=[("Outfit", "100 900", "Outfit-Bold.ttf"), ("Sora", "100 550", "sora-latin-400-normal.woff2"),
                          ("Sora", "551 900", "sora-latin-700-normal.woff2"), ("DM Mono", "100 900", "DMMono-Regular.ttf")]),
    "daos": dict(name="Naranja cívico", bg="#120B07", ink="#FFF4EC", acc="#FF6A2B", glyph="✓",
                 fd="Big Shoulders", fb="Work Sans", fm="IBM Plex Mono", upper=True, hsize=120, hls="0.0em", lh=0.98, ul="mark", cue="bar", esize=136,
                 fonts=[("Big Shoulders", "100 900", "BigShoulders-Bold.ttf"), ("Work Sans", "100 550", "WorkSans-Regular.ttf"),
                        ("Work Sans", "551 900", "WorkSans-Bold.ttf"), ("IBM Plex Mono", "100 550", "IBMPlexMono-Regular.ttf"),
                        ("IBM Plex Mono", "551 900", "IBMPlexMono-Bold.ttf")]),
    # --- temas minimalistas para videos únicos (13-oct) ---
    "estafas": dict(name="Papel y alerta", bg="#F3EFE6", ink="#151413", acc="#D3263A", glyph="!", light=True,
                    fd="Instrument Serif", fb="Inter", fm="JetBrains Mono", upper=False, hsize=118, hls="-0.02em", lh=0.98, ul="bar", cue="bar", esize=120,
                    fonts=[("Instrument Serif", "100 900", "InstrumentSerif-Regular.ttf"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                           ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("JetBrains Mono", "100 550", "JetBrainsMono-400.woff2"),
                           ("JetBrains Mono", "551 900", "JetBrainsMono-700.woff2")]),
    "autocustodia": dict(name="Grafito lila", bg="#111113", ink="#F1F0F4", acc="#C3B3FF", glyph="◆",
                         fd="Sora", fb="Inter", fm="Geist Mono", upper=False, hsize=84, hls="-0.04em", lh=1.02, ul="mark", cue="pill", esize=100,
                         fonts=[("Sora", "100 900", "sora-latin-700-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                                ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("Geist Mono", "100 550", "GeistMono-Regular.ttf"),
                                ("Geist Mono", "551 900", "GeistMono-Bold.ttf")]),
    "stablecoins": dict(name="Salvia", bg="#E6EDE7", ink="#13231B", acc="#2C7A55", glyph="$", light=True,
                        fd="Fraunces", fb="Work Sans", fm="DM Mono", upper=False, hsize=96, hls="-0.03em", lh=1.0, ul="bar", cue="pill", esize=108,
                        fonts=[("Fraunces", "100 900", "fraunces-latin-600-normal.woff2"), ("Work Sans", "100 550", "WorkSans-Regular.ttf"),
                               ("Work Sans", "551 900", "WorkSans-Bold.ttf"), ("DM Mono", "100 900", "DMMono-Regular.ttf")]),
    "gas": dict(name="Asfalto ámbar", bg="#131416", ink="#F4F2EC", acc="#FFB238", glyph="⛽",
                fd="Chakra Petch", fb="Inter", fm="Red Hat Mono", upper=True, hsize=88, hls="-0.01em", lh=1.0, ul="mark", cue="bar", esize=104,
                fonts=[("Chakra Petch", "100 900", "chakra-petch-latin-700-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                       ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("Red Hat Mono", "100 550", "RedHatMono-Regular.ttf"),
                       ("Red Hat Mono", "551 900", "RedHatMono-Bold.ttf")]),
    "staking": dict(name="Lavanda", bg="#ECE9F5", ink="#1B1730", acc="#5A3DD8", glyph="◆", light=True,
                    fd="Teko", fb="Instrument Sans", fm="IBM Plex Mono", upper=True, hsize=136, hls="0.0em", lh=0.9, ul="bar", cue="pill", esize=150,
                    fonts=[("Teko", "100 900", "teko-latin-700-normal.woff2"), ("Instrument Sans", "100 550", "InstrumentSans-Regular.ttf"),
                           ("Instrument Sans", "551 900", "InstrumentSans-Bold.ttf"), ("IBM Plex Mono", "100 550", "IBMPlexMono-Regular.ttf"),
                           ("IBM Plex Mono", "551 900", "IBMPlexMono-Bold.ttf")]),
    # --- 14-oct ---
    "defi": dict(name="Glaciar", bg="#EBF1F8", ink="#0E1A2B", acc="#2563EB", glyph="$", light=True,
                 fd="Rajdhani", fb="Inter", fm="DM Mono", upper=True, hsize=124, hls="-0.01em", lh=0.92, ul="mark", cue="pill", esize=128,
                 fonts=[("Rajdhani", "100 900", "rajdhani-latin-700-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                        ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("DM Mono", "100 900", "DMMono-Regular.ttf")]),
    "btceth": dict(name="Noche dual", bg="#0F0F10", ink="#F2F1EE", acc="#F7931A", glyph="₿",
                   fd="Tektur", fb="Work Sans", fm="Geist Mono", upper=True, hsize=92, hls="-0.01em", lh=1.0, ul="bar", cue="bar", esize=104,
                   fonts=[("Tektur", "100 900", "Tektur-Medium.ttf"), ("Work Sans", "100 550", "WorkSans-Regular.ttf"),
                          ("Work Sans", "551 900", "WorkSans-Bold.ttf"), ("Geist Mono", "100 550", "GeistMono-Regular.ttf"), ("Geist Mono", "551 900", "GeistMono-Bold.ttf")]),
    "oraculos": dict(name="Arena y petróleo", bg="#F1EADC", ink="#2A2118", acc="#0F766E", glyph="◎", light=True,
                     fd="Bodoni Moda", fb="Instrument Sans", fm="Red Hat Mono", upper=False, hsize=100, hls="-0.02em", lh=1.0, ul="bar", cue="bar", esize=110,
                     fonts=[("Bodoni Moda", "100 900", "bodoni-moda-latin-700-normal.woff2"), ("Instrument Sans", "100 550", "InstrumentSans-Regular.ttf"),
                            ("Instrument Sans", "551 900", "InstrumentSans-Bold.ttf"), ("Red Hat Mono", "100 550", "RedHatMono-Regular.ttf"), ("Red Hat Mono", "551 900", "RedHatMono-Bold.ttf")]),
    "tokenizacion": dict(name="Bosque y latón", bg="#0E1513", ink="#EEF2EE", acc="#D4B26A", glyph="▣",
                         fd="Cormorant Garamond", fb="Inter", fm="IBM Plex Mono", upper=False, hsize=112, hls="-0.02em", lh=0.98, ul="bar", cue="pill", esize=120,
                         fonts=[("Cormorant Garamond", "100 900", "cormorant-garamond-latin-700-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                                ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("IBM Plex Mono", "100 550", "IBMPlexMono-Regular.ttf"), ("IBM Plex Mono", "551 900", "IBMPlexMono-Bold.ttf")]),
    "login": dict(name="Rubor frambuesa", bg="#F7ECEE", ink="#25181E", acc="#D6336C", glyph="@", light=True,
                  fd="Fredoka", fb="Inter", fm="DM Mono", upper=False, hsize=96, hls="-0.02em", lh=1.0, ul="mark", cue="pill", esize=110,
                  fonts=[("Fredoka", "100 900", "fredoka-latin-700-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                         ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("DM Mono", "100 900", "DMMono-Regular.ttf")]),
    # --- 14-oct (tanda 2) ---
    "halving": dict(name="Medianoche cian", bg="#0B0D12", ink="#EAF0FF", acc="#6EE7F9", glyph="½",
                    fd="Orbitron", fb="Inter", fm="JetBrains Mono", upper=True, hsize=74, hls="0.0em", lh=1.08, ul="mark", cue="bar", esize=84,
                    fonts=[("Orbitron", "100 900", "orbitron-latin-700-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                           ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("JetBrains Mono", "100 550", "JetBrainsMono-400.woff2"), ("JetBrains Mono", "551 900", "JetBrainsMono-700.woff2")]),
    "dex": dict(name="Pistache y oliva", bg="#EEF1E4", ink="#1C2112", acc="#5B6E12", glyph="⇄", light=True,
                fd="Baloo 2", fb="Work Sans", fm="DM Mono", upper=False, hsize=104, hls="-0.02em", lh=0.98, ul="bar", cue="pill", esize=116,
                fonts=[("Baloo 2", "100 900", "baloo-2-latin-700-normal.woff2"), ("Work Sans", "100 550", "WorkSans-Regular.ttf"),
                       ("Work Sans", "551 900", "WorkSans-Bold.ttf"), ("DM Mono", "100 900", "DMMono-Regular.ttf")]),
    "puentes": dict(name="Marino y coral", bg="#0A1428", ink="#E8EEF8", acc="#FF7A59", glyph="⌒",
                    fd="Young Serif", fb="Instrument Sans", fm="Geist Mono", upper=False, hsize=94, hls="-0.02em", lh=1.02, ul="bar", cue="bar", esize=104,
                    fonts=[("Young Serif", "100 900", "YoungSerif-Regular.ttf"), ("Instrument Sans", "100 550", "InstrumentSans-Regular.ttf"),
                           ("Instrument Sans", "551 900", "InstrumentSans-Bold.ttf"), ("Geist Mono", "100 550", "GeistMono-Regular.ttf"), ("Geist Mono", "551 900", "GeistMono-Bold.ttf")]),
    "memecoins": dict(name="Crema bermellón", bg="#FFF6E5", ink="#1B1712", acc="#E2401C", glyph="!", light=True, efd="Inter",
                      fd="Bangers", fb="Inter", fm="Red Hat Mono", upper=True, hsize=128, hls="0.02em", lh=0.95, ul="mark", cue="pill", esize=140,
                      fonts=[("Bangers", "100 900", "bangers-latin-400-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                             ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("Red Hat Mono", "100 550", "RedHatMono-Regular.ttf"), ("Red Hat Mono", "551 900", "RedHatMono-Bold.ttf")]),
    "privacidad": dict(name="Monocromo", bg="#EFEFEC", ink="#121212", acc="#121212", glyph="#", light=True,
                       fd="VT323", fb="Inter", fm="IBM Plex Mono", upper=True, hsize=132, hls="0.0em", lh=0.88, ul="mark", cue="bar", esize=150,
                       fonts=[("VT323", "100 900", "vt323-latin-400-normal.woff2"), ("Inter", "100 550", "inter-latin-500-normal.woff2"),
                              ("Inter", "551 900", "inter-latin-700-normal.woff2"), ("IBM Plex Mono", "100 550", "IBMPlexMono-Regular.ttf"), ("IBM Plex Mono", "551 900", "IBMPlexMono-Bold.ttf")]),
}

FONT_DIRS = [os.path.expanduser("~/.claude/skills"), os.path.expanduser("~/.claude/skills-src")]


def install_fonts(here, th):
    """Copia a <here>/assets/fonts los archivos del tema (los busca en las carpetas de skills)."""
    dst = os.path.join(here, "assets", "fonts")
    os.makedirs(dst, exist_ok=True)
    need = {f for _, _, f in th["fonts"]}
    for f in list(need):
        if os.path.exists(os.path.join(dst, f)):
            need.discard(f)
    for base in FONT_DIRS:
        for root, _, files in os.walk(base):
            for f in files:
                if f in need:
                    shutil.copy(os.path.join(root, f), os.path.join(dst, f))
                    need.discard(f)
            if not need:
                return
    if need:
        raise SystemExit(f"faltan fuentes: {need}")


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _h(c):
    return "#%02x%02x%02x" % c


def _lum(c):
    return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255


OLD_ACC = (255, 42, 77)


def _map(rgb, th):
    bg, ink, acc = _hex(th["bg"]), _hex(th["ink"]), _hex(th["acc"])
    r, g, b = rgb
    if rgb in ((0, 0, 0), (255, 255, 255)):
        return rgb
    if r > g + 40 and r > b + 40:  # familia del rojo de marca v1 -> acento del tema
        lo, la = _lum(rgb), _lum(OLD_ACC)
        if lo > la + 0.03:
            return _mix(acc, (255, 255, 255), min(0.75, (lo - la) / (1 - la)))
        if lo < la - 0.03:
            return _mix(acc, bg, min(0.92, (la - lo) / la))
        return acc
    if max(rgb) - min(rgb) < 50:  # neutros -> rampa fondo..tinta del tema
        t = min(1.0, max(0.0, ((r + g + b) / 3 - 8) / (240 - 8)))
        return _mix(bg, ink, t)
    return rgb


def retheme(s, th):
    s = re.sub(r"#([0-9a-fA-F]{6})\b", lambda m: _h(_map(_hex(m.group(1)), th)), s)
    s = re.sub(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,", lambda m: "rgba(%d,%d,%d," % _map(tuple(int(m.group(k)) for k in (1, 2, 3)), th), s)
    for old, new in (("IBM Plex Mono", "__FM__"), ("Public Sans", "__FB__"), ("AlfaSerif", "__FD__"), ("Georgia", "__FD__")):
        s = s.replace(old, new)
    s = re.sub(r"\bSyne\b", "__FD__", s)
    s = s.replace("__FM__", th["fm"]).replace("__FB__", th["fb"]).replace("__FD__", th["fd"])
    return s.replace("α", th["glyph"])


def _rgb(c):
    return "%d,%d,%d" % _hex(c)


def base_css(th):
    bg, ink, acc = _hex(th["bg"]), _hex(th["ink"]), _hex(th["acc"])
    card, line, muted, dim = _h(_mix(bg, ink, 0.06)), _h(_mix(bg, ink, 0.2)), _h(_mix(bg, ink, 0.62)), _h(_mix(bg, ink, 0.12))
    faces = "\n".join(f'      @font-face {{ font-family: "{f}"; font-weight: {w}; src: url("assets/fonts/{fn}") format("{"woff2" if fn.endswith("woff2") else "truetype"}"); }}' for f, w, fn in th["fonts"])
    up = "uppercase" if th["upper"] else "none"
    ul = (".wm .ul { position: absolute; left: 0; right: 0; top: 10%; bottom: 2%; background: var(--acc); transform-origin: left center; z-index: 0; border-radius: 6px; }\n"
          "      .wm.a .w { position: relative; z-index: 1; color: var(--bg); padding: 0 0.06em; }") if th["ul"] == "mark" else \
         (".wm .ul { position: absolute; left: 0.04em; right: 0.04em; bottom: 0.06em; height: 0.09em; background: var(--acc); transform-origin: left center; border-radius: 99px; }\n"
          "      .wm.a .w { color: var(--acc); }")
    cue = ("padding: 14px 30px; border-radius: 999px; background: rgba(%s,0.86); border: 2px solid rgba(%s,0.55);" % (_rgb(th["bg"]), _rgb(th["acc"]))) if th["cue"] == "pill" else \
          ("padding: 12px 26px; border-radius: 10px; background: rgba(%s,0.86); border-left: 7px solid var(--acc);" % _rgb(th["bg"]))
    return f'''
{faces}
      :root {{ --bg: {th["bg"]}; --ink: {th["ink"]}; --acc: {th["acc"]}; --card: {card}; --line: {line}; --muted: {muted}; --dim: {dim};
        --void: var(--bg); --signal: var(--acc); --bone: var(--ink); --circuit: var(--line); --ash: var(--muted); --ink2: var(--card); --accrgb: {_rgb(th["acc"])}; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }}
      body {{ font-family: "{th["fb"]}", sans-serif; font-weight: 500; color: var(--ink); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--bg); }}
      .scene, .layer, .tint, .cam {{ position: absolute; inset: 0; }}
      svg.layer {{ width: 1080px; height: 1920px; }}
      .eyeclip {{ position: absolute; left: 0; right: 0; top: 250px; display: flex; justify-content: center; }}
      .eyebrow {{ display: flex; align-items: center; gap: 18px; font-family: "{th["fm"]}", monospace; font-weight: 700; font-size: 25px; letter-spacing: 0.2em; text-transform: uppercase; color: var(--ink); }}
      .segs {{ display: flex; gap: 6px; }} .seg {{ position: relative; width: 30px; height: 6px; border-radius: 3px; background: var(--line); overflow: hidden; }}
      .seg.done {{ background: var(--acc); }} .seg i {{ position: absolute; inset: 0; background: var(--acc); transform-origin: left center; }}
      .enum {{ color: var(--acc); }} .esep {{ width: 26px; height: 2px; background: var(--line); }}
      .head {{ position: absolute; left: 50px; right: 50px; top: 322px; height: 250px; display: flex; justify-content: center; align-items: flex-start; text-align: center; }}
      .display {{ font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: {th["hsize"]}px; line-height: {th["lh"]}; letter-spacing: {th["hls"]}; text-transform: {up}; color: var(--ink); }}
      .wm {{ position: relative; display: inline-block; overflow: hidden; vertical-align: top; padding: 0.16em 0.03em 0.1em; margin-top: -0.14em; margin-bottom: -0.08em; }}
      .wm .w {{ display: inline-block; position: relative; }} .ch {{ display: inline-block; transform-origin: 50% 100%; }}
      {ul}
      .chip {{ position: absolute; display: inline-flex; align-items: center; gap: 12px; padding: 12px 24px; border-radius: 999px; border: 2px solid var(--line); background: rgba({_rgb(card)},0.95);
        font-family: "{th["fm"]}", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; color: var(--ink); white-space: nowrap; box-shadow: 0 14px 30px rgba(0,0,0,{0.08 if th.get('light') else 0.35}); }}
      .chip.red {{ background: var(--acc); border-color: var(--acc); color: var(--bg); box-shadow: 0 0 40px rgba(var(--accrgb),0.35); }} .chip b {{ color: var(--acc); font-weight: 700; }}
      .stamp {{ position: absolute; padding: 8px 22px; border: 7px solid var(--acc); border-radius: 12px; font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 40px; color: var(--acc); background: rgba({_rgb(th["bg"])},0.9); white-space: nowrap; text-transform: uppercase; }}
      .card {{ position: absolute; border-radius: 24px; background: linear-gradient(160deg, {_h(_mix(bg, ink, 0.09))}, {card}); border: 2px solid var(--line); box-shadow: 0 30px 60px rgba(0,0,0,{0.10 if th.get('light') else 0.45}), inset 0 1px 0 rgba(255,255,255,0.06); }}
      .ab {{ display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 10px; background: var(--acc); color: var(--bg); font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 26px; flex: none; text-transform: none; }}
      .mono {{ font-family: "{th["fm"]}", monospace; font-weight: 700; }}
      .syne {{ font-family: "{th["fd"]}", sans-serif; font-weight: 800; }}
      .ghost {{ position: absolute; left: -400px; right: -400px; top: 0; height: 1920px; display: flex; align-items: center; justify-content: center; }}
      .ghost b {{ display: block; }} .ghost text {{ font-family: "{th["fd"]}", sans-serif; font-weight: 800; letter-spacing: -0.02em; }}
      .corner {{ position: absolute; width: 46px; height: 46px; border-color: rgba(var(--accrgb),0.55); border-style: solid; border-width: 0; }}
      #k0 {{ left: 46px; top: 600px; border-left-width: 4px; border-top-width: 4px; }} #k1 {{ right: 46px; top: 600px; border-right-width: 4px; border-top-width: 4px; }}
      #k2 {{ left: 46px; top: 1410px; border-left-width: 4px; border-bottom-width: 4px; }} #k3 {{ right: 46px; top: 1410px; border-right-width: 4px; border-bottom-width: 4px; }}
      /* fx */
      #ghostc {{ position: absolute; inset: 0; width: 1080px; height: 1920px; }}
      #fxClip, #grainClip {{ position: absolute; inset: 0; pointer-events: none; }}
      #sweep {{ position: absolute; left: 0; top: -200px; width: 420px; height: 2400px; background: linear-gradient(90deg, transparent, rgba(var(--accrgb),0.09), rgba(255,255,255,0.06), transparent); }}
      .burst {{ position: absolute; width: 0; height: 0; }}
      .burst .br {{ position: absolute; left: -90px; top: -90px; width: 180px; height: 180px; border-radius: 50%; border: 5px solid var(--acc); }}
      .burst b {{ position: absolute; left: 0; top: -3px; width: 150px; height: 6px; transform-origin: 0 50%; }}
      .burst b u {{ position: absolute; left: 60px; top: 0; width: 70px; height: 6px; border-radius: 3px; background: var(--acc); transform-origin: 0 50%; }}
      #grain {{ position: absolute; inset: 0; opacity: 0.09; mix-blend-mode: overlay; background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='256' height='256' filter='url(%23n)'/></svg>"); }}
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 48%, transparent 55%, rgba(0,0,0,{0.10 if th.get('light') else 0.55}) 100%); }}
      /* end card */
      #endbg {{ position: absolute; inset: 0; background: radial-gradient(ellipse 85% 55% at 50% 42%, rgba(var(--accrgb),0.20), rgba({_rgb(th["bg"])},0.97) 70%); }}
      .ering {{ position: absolute; left: 140px; top: 330px; width: 800px; height: 800px; border-radius: 50%; border: 3px solid rgba(var(--accrgb),0.5); }}
      #endc {{ position: absolute; left: 0; right: 0; top: 430px; display: flex; flex-direction: column; align-items: center; gap: 22px; }}
      .eseries {{ font-family: "{th["fm"]}", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.3em; color: var(--acc); }}
      .ename {{ font-family: "{th.get("efd", th["fd"])}", sans-serif; font-weight: 800; font-size: {th["esize"]}px; line-height: 1.05; letter-spacing: {th["hls"]}; color: var(--ink); white-space: nowrap; }}
      .ename .wm {{ padding-bottom: 0.06em; }}
      #elist {{ width: 820px; margin-top: 18px; display: flex; flex-direction: column; border-top: 2px solid var(--line); }}
      .erow {{ position: relative; display: flex; align-items: center; gap: 26px; height: 74px; padding: 0 22px; border-bottom: 2px solid var(--line); font-family: "{th["fb"]}", sans-serif; font-weight: 700; font-size: 32px; color: var(--muted); overflow: hidden; }}
      .erow i {{ position: relative; z-index: 1; font-style: normal; font-family: "{th["fm"]}", monospace; font-size: 24px; letter-spacing: 0.1em; }}
      .erow span {{ position: relative; z-index: 1; flex: 1; }}
      #etake {{ max-width: 880px; margin-top: 26px; padding: 34px 40px; border-top: 3px solid var(--acc); border-bottom: 3px solid var(--acc); text-align: center; font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 60px; line-height: 1.1; letter-spacing: {th["hls"]}; text-transform: {up}; color: var(--ink); }}
      #etake .wm {{ margin-top: 0; padding-top: 0.06em; }}
      .erow.cur {{ color: var(--ink); }} .erow .hl {{ position: absolute; inset: 0; background: var(--acc); transform-origin: left center; }}
      .erow b {{ position: relative; z-index: 1; font-family: "{th["fm"]}", monospace; font-size: 20px; letter-spacing: 0.2em; }}
      #cta {{ margin-top: 26px; padding: 26px 52px; border-radius: 999px; background: var(--ink); color: var(--bg); font-family: "{th["fd"]}", sans-serif; font-weight: 800; font-size: 38px; text-transform: uppercase; white-space: nowrap; }}
      .cue {{ position: absolute; left: 70px; right: 70px; top: 1486px; display: flex; justify-content: center; }}
      .cue span {{ display: block; max-width: 940px; text-align: center; font-family: "{th["fb"]}", sans-serif; font-weight: 700; font-size: 39px; line-height: 1.28; color: var(--ink); {cue} }}
'''


JS_TOP = r'''
        function mulberry32(a) { return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
        const R = mulberry32(117);
        const $ = (s) => document.querySelector(s);
        const tl = gsap.timeline({ paused: true });
        const count = (sel, to, dur, at, fmt) => { const o = { v: 0 }; const el = document.querySelector(sel);
          tl.fromTo(o, { v: 0 }, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { const n = Math.round(o.v); el.textContent = fmt ? fmt(n) : n.toLocaleString("es-MX"); } }, at); };
        const typeText = (sel, text, at, cps) => { const el = document.querySelector(sel); const from = el.dataset.tt !== undefined ? el.dataset.tt : el.textContent; el.dataset.tt = text; const o = { n: 0 };
          tl.fromTo(o, { n: 0 }, { n: text.length, duration: text.length / (cps || 28), ease: "none", immediateRender: false, onUpdate: () => { const k = Math.round(o.n); el.textContent = k === 0 ? from : text.slice(0, k); } }, at); };
'''

JS_CHROME = r'''
        // camera: slow push-in with a slight alternating tilt
        SC.forEach((s, i) => { const e = i < SC.length - 1 ? SC[i + 1] : END; const c = document.getElementById("cam" + (i + 1));
          if (c) tl.fromTo(c, { scale: STAGE * 1.08, y: 36, rotation: i % 2 ? 0.7 : -0.7, transformOrigin: "540px 980px" }, { scale: STAGE, y: 0, rotation: 0, transformOrigin: "540px 980px", duration: e - s, ease: "power2.out" }, s); });
        if (GHOSTS.length) { const gc = document.getElementById("ghostc"), gg = gc.getContext("2d");
          const ghost = (t) => { gg.clearRect(0, 0, 1080, 1920); let i = 0; while (i < SC.length - 1 && t >= SC[i + 1]) i++; if (t >= END || !GHOSTS[i]) return;
            const s0 = SC[i], e0 = i < SC.length - 1 ? SC[i + 1] : END, u = (t - s0) / (e0 - s0), w = GHOSTS[i];
            const fs = Math.min(520, Math.floor(1900 / Math.max(1, w.length) * 1.05)); gg.font = "800 " + fs + "px \"" + FD + "\"";
            gg.textAlign = "center"; gg.textBaseline = "middle"; gg.lineWidth = 3; gg.strokeStyle = "rgba(" + ACCRGB + "," + (0.16 * Math.min(1, (t - s0) / 0.6)).toFixed(3) + ")";
            gg.strokeText(w, 540 + (i % 2 ? -1 : 1) * (120 - 240 * u), 990); };
          const gp = { t: 0 }; ghost(0); tl.to(gp, { t: DUR, duration: DUR, ease: "none", onUpdate: () => ghost(gp.t) }, 0); }
        tl.fromTo(".corner", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.5, stagger: 0.06, ease: "expo.out" }, 0.2);
        SC.slice(1).forEach((c) => tl.fromTo(".corner", { scale: 1 }, { keyframes: { scale: [1.35, 1] }, duration: 0.5, ease: "power2.out", immediateRender: false }, c + 0.1));
        tl.to(".corner", { opacity: 0, duration: 0.3 }, END);
        // chapter bar: current segment fills across the scene
        document.querySelectorAll(".eyeclip").forEach((ec) => { const s0 = +ec.getAttribute("data-start"), d0 = +ec.getAttribute("data-duration");
          tl.fromTo(ec.querySelector(".eyebrow"), { opacity: 0, y: -18 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, s0 + 0.12);
          tl.fromTo(ec.querySelector(".seg i"), { scaleX: 0 }, { scaleX: 1, duration: d0, ease: "none" }, s0); });
        // headlines: letter-by-letter rise with 3D tilt + blur, accent mark/underline, staggered exit
        document.querySelectorAll(".head").forEach((h) => {
          const s0 = +h.getAttribute("data-start"), e0 = s0 + +h.getAttribute("data-duration");
          const chars = h.querySelectorAll(".ch");
          tl.fromTo(chars, { yPercent: 115, rotationX: -85, opacity: 0, filter: "blur(10px)", transformPerspective: 700 },
            { yPercent: 0, rotationX: 0, opacity: 1, filter: "blur(0px)", duration: 0.6, stagger: 0.018, ease: "expo.out" }, s0 + 0.14);
          h.querySelectorAll(".ul").forEach((ul) => tl.fromTo(ul, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power4.out" }, s0 + 0.02));
          tl.to(chars, { yPercent: -115, opacity: 0, duration: 0.26, stagger: 0.008, ease: "power2.in" }, e0 - 0.3);
          h.querySelectorAll(".ul").forEach((ul) => tl.to(ul, { scaleX: 0, transformOrigin: "right center", duration: 0.14, ease: "power2.in" }, e0 - 0.15));
        });
        // light sweep on each cut
        SC.slice(1).forEach((c) => tl.fromTo("#sweep", { x: -700, opacity: 1 }, { x: 1400, opacity: 1, duration: 0.9, ease: "power2.inOut", immediateRender: false }, c + 0.25));
        tl.set("#sweep", { x: -700 }, 0);
        // bursts
        BURSTS.forEach((t, k) => { const b = "#bu" + k;
          tl.fromTo(b + " .br", { scale: 0.2, opacity: 1 }, { scale: 2.1, opacity: 0, duration: 0.7, ease: "power2.out" }, t);
          tl.fromTo(b + " b u", { x: -50, scaleX: 0, opacity: 1 }, { keyframes: { x: [-50, 0, 70], scaleX: [0, 1, 0] }, duration: 0.55, ease: "power2.out" }, t); });
        tl.set(".burst .br, .burst b u", { opacity: 0 }, 0);
        // grain flicker (stepped, deterministic)
        tl.fromTo("#grain", { backgroundPosition: "0px 0px" }, { backgroundPosition: "2560px 1792px", duration: DUR, ease: "steps(" + Math.round(DUR * 12) + ")" }, 0);
        // end card
        tl.fromTo("#endbg", { opacity: 0 }, { opacity: 1, duration: 0.45 }, END);
        document.querySelectorAll(".ering").forEach((r, k) => tl.fromTo(r, { scale: 0.2, opacity: 0.9 }, { scale: 1.5, opacity: 0, duration: 2.4, repeat: Math.max(0, Math.floor((DUR - END - 0.3 - k * 0.8) / 2.4)), ease: "power1.out" }, END + 0.3 + k * 0.8));
        tl.fromTo("#endc .eseries", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, END + 0.25);
        tl.fromTo("#endc .ename .ch", { yPercent: 115, rotationX: -85, opacity: 0, transformPerspective: 700 }, { yPercent: 0, rotationX: 0, opacity: 1, duration: 0.6, stagger: 0.03, ease: "expo.out" }, END + 0.35);
        if (document.querySelector(".erow")) {
        tl.fromTo(".erow", { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: 0.45, stagger: 0.08, ease: "expo.out" }, END + 0.9);
        tl.fromTo(".erow .hl", { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power4.out" }, END + 1.5);
        tl.fromTo(".erow.cur b", { opacity: 0 }, { opacity: 1, duration: 0.2 }, END + 2.0);
        tl.fromTo(".erow.cur", { color: getComputedStyle(document.documentElement).getPropertyValue("--ink").trim() }, { color: getComputedStyle(document.documentElement).getPropertyValue("--bg").trim(), duration: 0.25 }, END + 1.65);
        }
        if (document.querySelector("#etake")) {
          tl.fromTo("#etake", { opacity: 0, scaleX: 0.6 }, { opacity: 1, scaleX: 1, duration: 0.5, ease: "expo.out" }, END + 0.9);
          tl.fromTo("#etake .ch", { yPercent: 110, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.5, stagger: 0.012, ease: "expo.out" }, END + 1.05); }
        tl.fromTo("#cta", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(2.4)" }, END + 1.8);
        tl.fromTo("#cta", { boxShadow: "0 0 0px rgba(" + ACCRGB + ",0)" }, { boxShadow: "0 0 90px rgba(" + ACCRGB + ",0.9)", duration: 0.7, yoyo: true, repeat: 3, ease: "sine.inOut", immediateRender: false }, END + 2.3);
        // subtitles
        CUES.forEach((s, i) => tl.fromTo(`#cue${i} span`, { opacity: 0, y: 16, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.22, ease: "power3.out" }, s));
        window.__timelines["main"] = tl;
'''


def _chars(word):
    return "".join(f'<span class="ch">{c}</span>' for c in word)


def words(txt):
    """'Texto con *acento' -> palabras con letras separadas; * = palabra de acento (marca o subrayado según tema)."""
    out = []
    for w in txt.split():
        acc = w.startswith("*")
        w = w.lstrip("*")
        out.append(f'<span class="wm{" a" if acc else ""}">' + ('<span class="ul"></span>' if acc else "") + f'<span class="w">{_chars(w)}</span></span>')
    return " ".join(out)


def scene(i, sc, end, inner, tint):
    a, b = sc[i - 1], (sc[i] if i < len(sc) else end)
    return (f'      <div id="s{i}" class="clip scene" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="1">\n'
            f'        <div class="tint" style="background:{tint}"></div>\n        <div class="cam" id="cam{i}">\n{inner}\n        </div>\n      </div>')


def _eyebrow(i, n, txt):
    num, _, lab = txt.partition("·")
    segs = "".join(f'<div class="seg{" done" if k < i else ""}">{"<i></i>" if k == i else ""}</div>' for k in range(n))
    return f'<div class="eyebrow"><div class="segs">{segs}</div><span class="enum">{num.strip()}/{n:02d}</span><i class="esep"></i><span>{lab.strip()}</span></div>'


def page(th, dur, sc, eyes, heads, cues, scenes_html, scene_css, scene_js, bg_html, bg_js, tx_html, tx_js, end_at, part, cta,
         takeaway=None, kicker="WEB3 EXPLICADO FÁCIL", recolor=True, bursts=(), ghosts=(), stage=1.0, music_vol=0.26, sfx_vol=0.55, lang="es"):
    rt = (lambda s: retheme(s, th)) if recolor else (lambda s: s)  # noqa: E731
    n = len(eyes)
    eyes_h = "\n".join(f'      <div class="eyeclip clip" id="e{i}" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="5">{_eyebrow(i, n, t)}</div>' for i, (a, b, t) in enumerate(eyes))
    heads_h = "\n".join(f'      <div class="head clip" id="h{i}" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="6"><div class="display">{words(t)}</div></div>' for i, (a, b, t) in enumerate(heads))
    cues_h = "\n".join(f'      <div class="cue clip" id="cue{i}" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="9"><span>{t}</span></div>' for i, (a, b, t) in enumerate(cues))
    rows = "".join(f'<div class="erow{" cur" if k + 1 == part else ""}">' + ('<u class="hl"></u>' if k + 1 == part else "") + f'<i>0{k + 1}</i><span>{t}</span>' + ("<b>AHORA</b>" if k + 1 == part else "") + "</div>" for k, t in enumerate(SERIES))
    series_lab = f"WEB3 DESDE CERO · {part}/5" if part else kicker
    middle = f'<div id="elist">{rows}</div>' if part else (f'<div id="etake">{words(takeaway)}</div>' if takeaway else "")
    end_h = f'''      <div id="endClip" class="clip" data-start="{end_at}" data-duration="{dur - end_at:.2f}" data-track-index="5">
        <div id="endbg"></div><div class="ering"></div><div class="ering"></div><div class="ering"></div>
        <div id="endc"><div class="eseries">{series_lab}</div><div class="ename"><span class="wm"><span class="w">{_chars(FIRMA)}</span></span></div>
          {middle}<div id="cta">{cta}</div></div>
      </div>'''
    rays = "".join(f'<b style="transform:rotate({k * 36}deg)"><u></u></b>' for k in range(10))
    bursts_h = "".join(f'<div class="burst" id="bu{k}" style="left:{x}px;top:{y}px"><i class="br"></i>{rays}</div>' for k, (_, x, y) in enumerate(bursts))
    ends = list(sc[1:]) + [end_at]
    ghosts_h = f'      <div id="ghostClip" class="clip" data-start="0" data-duration="{dur}" data-track-index="2"><canvas id="ghostc" width="1080" height="1920"></canvas></div>' if ghosts else ""
    js = (JS_TOP + f"\n        const DUR = {dur}, SC = {json.dumps(sc)}, END = {end_at}, CUES = {json.dumps([a for a, _, _ in cues])}, BURSTS = {json.dumps([t for t, _, _ in bursts])}, ACCRGB = \"{_rgb(th['acc'])}\", STAGE = {stage}, GHOSTS = {json.dumps([w.upper() for w in ghosts], ensure_ascii=False)}, FD = \"{th['fd']}\";\n"
          + rt(bg_js) + rt(scene_js) + rt(tx_js) + JS_CHROME)
    return f'''<!doctype html>
<html lang="{lang}" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{base_css(th)}{rt(scene_css)}    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
      <div id="bgClip" class="clip" data-start="0" data-duration="{dur}" data-track-index="0">
{rt(bg_html)}
      </div>
{ghosts_h}
{rt(scenes_html)}
      <div id="fxClip" class="clip" data-start="0" data-duration="{dur}" data-track-index="4"><div id="sweep" data-layout-allow-overflow></div><div class="corner" id="k0"></div><div class="corner" id="k1"></div><div class="corner" id="k2"></div><div class="corner" id="k3"></div>{bursts_h}</div>
{eyes_h}
{heads_h}
{end_h}
      <div id="txClip" class="clip" data-start="0" data-duration="{dur}" data-track-index="8">
{rt(tx_html)}
      </div>
      <div id="grainClip" class="clip" data-start="0" data-duration="{dur}" data-track-index="7"><div id="vig"></div><div id="grain"></div></div>
{cues_h}
      <audio id="vo" src="assets/voz.wav" data-start="0" data-duration="{dur}" data-track-index="10" data-volume="1"></audio>
      <audio id="music" src="assets/musica.wav" data-start="0" data-duration="{dur}" data-track-index="11" data-volume="{music_vol}"></audio>
      <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="{dur}" data-track-index="12" data-volume="{sfx_vol}"></audio>
    </div>
    <script>
      (function () {{{js}      }})();
    </script>
  </body>
</html>
'''
