"""Genera index.html del borrador: mono parlante de Mongli DAO con lip-sync por envolvente."""
import json
import sys

import numpy as np
import soundfile as sf

proj = sys.argv[1]
DUR = 62.5

# ---------- mouth envelope (30 fps) ----------
x, sr = sf.read(f"{proj}/assets/voz-mono.wav")
if x.ndim > 1:
    x = x.mean(1)
hop = sr // 30
n = int(DUR * 30)
rms = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) if i * hop < len(x) else 0 for i in range(n)])
ref = np.percentile(rms[rms > 1e-4], 97)
o = np.clip(rms / ref, 0, 1) ** 1.6
o[rms < 0.015] = 0
# emphasise syllable motion: subtract a slow average
slow = np.convolve(o, np.ones(9) / 9, mode="same")
o = np.clip(o * 0.55 + np.clip(o - slow * 0.6, 0, 1) * 1.1, 0, 1)
env = np.zeros_like(o)
a = 0.0
for i, v in enumerate(o):
    a = v if v > a else a * 0.4 + v * 0.6
    env[i] = a
mouth = [round(float(v), 2) for v in env]
print("open ratio", round(float((env > 0.15).mean()), 2))

# ---------- headlines (start, end, html) ----------
A = '<span class="accent">'
H = [
    (2.6, 5.8, "La nueva era"),
    (5.8, 7.1, f"empieza con {A}nosotros.</span>"),
    (7.1, 10.75, f"{A}Web3</span>"),
    (10.75, 12.2, "Construir."),
    (12.2, 13.8, f"{A}Colaborar.</span>"),
    (13.8, 15.15, f"Crear {A}juntos.</span>"),
    (15.15, 18.5, f"Conoce {A}Mongli DAO</span>"),
    (18.5, 20.6, "Personas · Ideas · Web3"),
    (20.6, 24.3, "No entre unos pocos."),
    (24.3, 28.45, f"Lo construimos {A}juntos.</span>"),
    (28.45, 31.15, f"Una {A}idea.</span>"),
    (31.15, 32.1, "Una pregunta."),
    (32.1, 33.15, "Una conversación."),
    (33.15, 34.5, f"Una {A}conexión.</span>"),
    (34.5, 37.0, f"Una {A}comunidad.</span>"),
    (37.0, 40.85, f"Posibilidades {A}infinitas.</span>"),
    (40.85, 43.15, f"Lo que {A}viene.</span>"),
    (43.15, 45.4, "Explora."),
    (45.4, 47.1, f"{A}Crea.</span>"),
    (47.1, 49.6, "Conecta."),
    (49.6, 52.0, f"Hay un lugar {A}para ti.</span>"),
    (52.0, 55.0, f"Tu camino en {A}Web3</span> empieza aquí."),
    (55.0, 59.1, f"El futuro se construye {A}juntos.</span>"),
]
# ---------- subtitles ----------
C = [
    (0.4, 1.92, "Internet cambió el mundo."),
    (1.92, 5.84, "Pero, ¿y si el siguiente capítulo no se trata solamente de tecnología…"),
    (5.84, 7.12, "…sino de nosotros?"),
    (7.12, 9.84, "Web3 está abriendo nuevas posibilidades."),
    (9.84, 11.44, "Nuevas formas de construir."),
    (11.44, 12.88, "Nuevas formas de colaborar."),
    (12.88, 15.2, "Y nuevas formas de crear valor juntos."),
    (15.2, 16.88, "Conoce Mongli DAO."),
    (16.88, 20.64, "Una comunidad en la intersección de las personas, las ideas y Web3."),
    (20.64, 24.32, "Porque el futuro de internet no debería construirse entre unos pocos…"),
    (24.32, 28.48, "…sino tomar forma gracias a quienes participan y construyen juntos."),
    (28.48, 30.8, "Toda gran idea comienza en algún lugar."),
    (30.8, 31.92, "Con una pregunta."),
    (31.92, 32.96, "Una conversación."),
    (32.96, 33.92, "Una conexión."),
    (33.92, 38.96, "Y cuando las personas se unen con una visión compartida, las posibilidades comienzan a crecer."),
    (38.96, 40.88, "Esto es más que estar conectados."),
    (40.88, 43.2, "Se trata de formar parte de lo que viene."),
    (43.2, 46.88, "Ya sea que estés explorando Web3, desarrollando nuevas ideas"),
    (46.88, 49.68, "o buscando personas que compartan tu visión…"),
    (49.68, 52.08, "…hay un lugar para ti en esta conversación."),
    (52.08, 55.05, "Tu siguiente capítulo comienza con una conexión."),
    (55.05, 57.45, "El futuro no es algo que debamos esperar."),
    (57.45, 59.13, "Es algo que construimos. Juntos."),
    (59.13, 60.09, "Mongli DAO."),
    (60.09, 62.3, "Únete a la comunidad."),
]
SCENES = [7.12, 15.2, 28.48, 43.2, 55.05, 59.13]

heads = "\n".join(
    f'      <div class="head clip" id="h{i}" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="4"><div class="display">{t}</div></div>'
    for i, (a, b, t) in enumerate(H)
)
cues = "\n".join(
    f'      <div class="cue clip" id="cue{i}" data-start="{a}" data-duration="{b - a:.2f}" data-track-index="5"><span>{t}</span></div>'
    for i, (a, b, t) in enumerate(C)
)

MONKEY = """
<svg id="monkey" viewBox="0 0 900 1000" width="900" height="1000" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="visorG" x1="0" x2="1"><stop offset="0" stop-color="#22e6ff"/><stop offset="0.55" stop-color="#3b82f6"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
    <radialGradient id="furG" cx="0.5" cy="0.35" r="0.7"><stop offset="0" stop-color="#6b4330"/><stop offset="1" stop-color="#3a2219"/></radialGradient>
    <radialGradient id="faceG" cx="0.5" cy="0.4" r="0.7"><stop offset="0" stop-color="#e8b48c"/><stop offset="1" stop-color="#c88a60"/></radialGradient>
    <linearGradient id="hoodG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16214a"/><stop offset="1" stop-color="#090e22"/></linearGradient>
    <filter id="glow" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="14" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="visorClip"><rect x="222" y="332" width="456" height="116" rx="58"/></clipPath>
  </defs>
  <g id="body">
    <path d="M70 1000 C 90 770, 250 690, 450 690 C 650 690, 810 770, 830 1000 Z" fill="url(#hoodG)" stroke="#22e6ff" stroke-opacity="0.55" stroke-width="5"/>
    <path d="M300 705 Q450 800 600 705" fill="none" stroke="#22e6ff" stroke-opacity="0.6" stroke-width="6"/>
    <line x1="450" y1="770" x2="450" y2="1000" stroke="#22e6ff" stroke-opacity="0.7" stroke-width="5"/>
    <rect x="330" y="860" width="240" height="70" rx="35" fill="none" stroke="#8b5cf6" stroke-width="4"/>
    <text x="450" y="907" text-anchor="middle" font-family="Space Grotesk" font-weight="700" font-size="34" fill="#f4f7ff" letter-spacing="4">MONGLI</text>
  </g>
  <g id="head">
    <circle cx="170" cy="430" r="95" fill="url(#furG)"/>
    <circle cx="170" cy="430" r="56" fill="#c98a63"/>
    <circle cx="730" cy="430" r="95" fill="url(#furG)"/>
    <circle cx="730" cy="430" r="56" fill="#c98a63"/>
    <ellipse cx="450" cy="420" rx="275" ry="265" fill="url(#furG)"/>
    <path d="M400 170 Q430 120 455 165 Q480 115 505 172" fill="#3a2219"/>
    <ellipse cx="450" cy="415" rx="215" ry="150" fill="url(#faceG)"/>
    <ellipse cx="450" cy="555" rx="170" ry="125" fill="url(#faceG)"/>
    <!-- visor -->
    <rect x="150" y="370" width="80" height="44" rx="10" fill="#1b2547"/>
    <rect x="670" y="370" width="80" height="44" rx="10" fill="#1b2547"/>
    <rect x="212" y="322" width="476" height="136" rx="68" fill="#0b1430"/>
    <g filter="url(#glow)"><rect id="visor" x="222" y="332" width="456" height="116" rx="58" fill="url(#visorG)"/></g>
    <g clip-path="url(#visorClip)">
      <rect x="222" y="352" width="456" height="16" fill="#ffffff" opacity="0.35"/>
      <rect id="scan" x="222" y="332" width="40" height="116" fill="#ffffff" opacity="0.35"/>
      <ellipse id="eyeL" cx="355" cy="392" rx="34" ry="20" fill="#eaffff" opacity="0.9"/>
      <ellipse id="eyeR" cx="545" cy="392" rx="34" ry="20" fill="#eaffff" opacity="0.9"/>
    </g>
    <!-- nose -->
    <ellipse cx="428" cy="502" rx="13" ry="9" fill="#5a3020"/>
    <ellipse cx="472" cy="502" rx="13" ry="9" fill="#5a3020"/>
    <!-- mouth -->
    <path id="smile" d="M375 585 Q450 615 525 585" fill="none" stroke="#3a1f15" stroke-width="9" stroke-linecap="round"/>
    <g id="mouthOpen">
      <ellipse cx="450" cy="600" rx="78" ry="52" fill="#2a0f0a"/>
      <rect x="400" y="560" width="100" height="16" rx="6" fill="#fff6ee"/>
      <ellipse cx="450" cy="630" rx="44" ry="18" fill="#e0607a"/>
    </g>
  </g>
</svg>"""

LOGO_ICON = """<svg width="104" height="104" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="48" fill="#0b1430" stroke="#22e6ff" stroke-width="3"/>
  <circle cx="22" cy="50" r="11" fill="#5a3826"/><circle cx="78" cy="50" r="11" fill="#5a3826"/>
  <circle cx="50" cy="50" r="27" fill="#5a3826"/>
  <ellipse cx="50" cy="57" rx="20" ry="16" fill="#d9a27a"/>
  <rect x="28" y="40" width="44" height="12" rx="6" fill="#22e6ff"/>
  <path d="M43 64 Q50 68 57 64" stroke="#3a1f15" stroke-width="2.5" fill="none" stroke-linecap="round"/>
</svg>"""

html = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Space Grotesk"; font-weight: 500; src: url("assets/fonts/space-grotesk-latin-500-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Space Grotesk"; font-weight: 700; src: url("assets/fonts/space-grotesk-latin-700-normal.woff2") format("woff2"); }}
      @font-face {{ font-family: "Inter"; font-weight: 600; src: url("assets/fonts/inter-latin-600-normal.woff2") format("woff2"); }}
      :root {{ --ink: #04050a; --white: #f4f7ff; --cyan: #22e6ff; --violet: #8b5cf6; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: var(--ink); }}
      body {{ font-family: "Inter", sans-serif; color: var(--white); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--ink); }}
      #net {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
      .vignette {{ position: absolute; inset: 0; background: radial-gradient(ellipse 75% 60% at 50% 50%, transparent 40%, rgba(2,3,8,0.85) 100%); }}
      .spot {{ position: absolute; left: 90px; top: 520px; width: 900px; height: 900px; border-radius: 50%;
        background: radial-gradient(circle, rgba(34,230,255,0.22), rgba(139,92,246,0.12) 45%, transparent 70%); }}
      #logo {{ position: absolute; left: 0; right: 0; top: 110px; display: flex; align-items: center; justify-content: center; gap: 24px; }}
      #logo .word {{ font-family: "Space Grotesk", sans-serif; font-weight: 700; font-size: 70px; letter-spacing: -0.01em;
        background: linear-gradient(100deg, var(--white) 10%, var(--cyan) 55%, var(--violet) 95%); -webkit-background-clip: text; background-clip: text; color: transparent; }}
      .head {{ position: absolute; left: 70px; right: 70px; top: 290px; height: 230px; display: flex; align-items: center; justify-content: center; text-align: center; }}
      .display {{ font-family: "Space Grotesk", sans-serif; font-weight: 700; font-size: 86px; line-height: 1.0; text-transform: uppercase; letter-spacing: -0.02em;
        text-shadow: 0 0 30px rgba(34,230,255,0.35); }}
      .accent {{ color: var(--cyan); }}
      #monkeyWrap {{ position: absolute; left: 90px; top: 520px; width: 900px; height: 1000px; }}
      #cta {{ position: absolute; left: 0; right: 0; top: 300px; display: flex; flex-direction: column; align-items: center; gap: 22px; }}
      #cta-btn {{ font-family: "Space Grotesk", sans-serif; font-weight: 700; font-size: 46px; letter-spacing: 0.12em; padding: 28px 64px; border-radius: 999px;
        background: linear-gradient(100deg, var(--cyan), var(--violet)); color: var(--ink); box-shadow: 0 0 60px rgba(34,230,255,0.5); }}
      #handle {{ font-family: "Space Grotesk", sans-serif; font-weight: 700; font-size: 54px; }}
      #flash {{ position: absolute; inset: 0; opacity: 0; background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.8), rgba(34,230,255,0.3) 30%, transparent 65%); }}
      .cue {{ position: absolute; left: 70px; right: 70px; top: 1540px; display: flex; justify-content: center; }}
      .cue span {{ display: block; max-width: 920px; text-align: center; font-family: "Inter", sans-serif; font-weight: 600; font-size: 48px; line-height: 1.22;
        color: #fff; padding: 14px 26px; border-radius: 18px; background: rgba(4,5,10,0.78); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
      <div id="bg" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0">
        <canvas id="net" width="1080" height="1920"></canvas>
        <div class="vignette"></div>
        <div class="spot" id="spot"></div>
      </div>
      <div id="brand" class="clip" data-start="0" data-duration="{DUR}" data-track-index="1">
        <div id="logo">{LOGO_ICON}<div class="word">MONGLI DAO</div></div>
      </div>
      <div id="mono" class="clip" data-start="0" data-duration="{DUR}" data-track-index="2">
        <div id="monkeyWrap">{MONKEY}</div>
      </div>
{heads}
      <div id="end" class="clip" data-start="59.1" data-duration="{DUR - 59.1:.2f}" data-track-index="4">
        <div id="cta"><div id="cta-btn">ÚNETE A LA COMUNIDAD</div><div id="handle">@mongli_dao</div></div>
      </div>
      <div id="flash-clip" class="clip" data-start="0" data-duration="{DUR}" data-track-index="3"><div id="flash"></div></div>
{cues}
      <audio id="vo" src="assets/voz-mono.wav" data-start="0" data-duration="{DUR}" data-track-index="8" data-volume="1"></audio>
      <audio id="music" src="assets/musica.wav" data-start="0" data-duration="{DUR}" data-track-index="9" data-volume="0.32"></audio>
    </div>
    <script>
      (function () {{
        const DUR = {DUR}, W = 1080, H = 1920;
        const MOUTH = {json.dumps(mouth)};
        const HEADS = {len(H)}, CUES = {json.dumps([a for a, _, _ in C])};
        function mulberry32(a) {{ return function () {{ a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }}; }}
        const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
        const smooth = (a, b, t) => {{ const u = clamp((t - a) / (b - a), 0, 1); return u * u * (3 - 2 * u); }};
        const lerp = (a, b, u) => a + (b - a) * u;

        // background network
        const cv = document.getElementById("net"), ctx = cv.getContext("2d");
        const R = mulberry32(117), NP = 170, DEPTH = 12, F = 820, P = [];
        for (let i = 0; i < NP; i++) P.push({{ x: (R() * 2 - 1) * 1.9, y: (R() * 2 - 1) * 3.3, z: R() * DEPTH, hue: R(), appear: 0.1 + R() * 2.5 }});
        const C1 = [34, 230, 255], C2 = [139, 92, 246];
        const col = (h, a) => `rgba(${{Math.round(lerp(C1[0], C2[0], h))}},${{Math.round(lerp(C1[1], C2[1], h))}},${{Math.round(lerp(C1[2], C2[2], h))}},${{a}})`;
        const sx = new Float32Array(NP), sy = new Float32Array(NP), sa = new Float32Array(NP);
        function drawNet(t) {{
          ctx.clearRect(0, 0, W, H);
          const cz = t * 0.6;
          for (let i = 0; i < NP; i++) {{
            const p = P[i]; const z = ((((p.z - cz) % DEPTH) + DEPTH) % DEPTH) + 0.7;
            sx[i] = W / 2 + (p.x * F) / z; sy[i] = H / 2 + (p.y * F) / z;
            sa[i] = smooth(p.appear, p.appear + 0.8, t) * smooth(DEPTH + 0.7, DEPTH * 0.7, z) * smooth(0.7, 1.6, z) * 0.7;
          }}
          ctx.globalCompositeOperation = "lighter"; ctx.lineWidth = 1.2;
          for (let i = 0; i < NP; i++) {{ if (sa[i] < 0.03) continue;
            for (let j = i + 1; j < NP; j++) {{ if (sa[j] < 0.03) continue;
              const dx = sx[i] - sx[j], dy = sy[i] - sy[j], d2 = dx * dx + dy * dy; if (d2 > 22500) continue;
              ctx.strokeStyle = col(P[i].hue, (Math.min(sa[i], sa[j]) * (1 - Math.sqrt(d2) / 150) * 0.5).toFixed(3));
              ctx.beginPath(); ctx.moveTo(sx[i], sy[i]); ctx.lineTo(sx[j], sy[j]); ctx.stroke(); }} }}
          for (let i = 0; i < NP; i++) {{ if (sa[i] < 0.02) continue;
            ctx.fillStyle = `rgba(255,255,255,${{sa[i].toFixed(3)}})`; ctx.beginPath(); ctx.arc(sx[i], sy[i], 2.2, 0, 6.2832); ctx.fill(); }}
          ctx.globalCompositeOperation = "source-over";
        }}

        // monkey rig
        const headG = document.getElementById("head"), bodyG = document.getElementById("body");
        const mouthO = document.getElementById("mouthOpen"), smile = document.getElementById("smile");
        const scan = document.getElementById("scan"), visor = document.getElementById("visor");
        const eyeL = document.getElementById("eyeL"), eyeR = document.getElementById("eyeR");
        function mouthAt(t) {{ const f = t * 30, i = Math.floor(f), u = f - i; return lerp(MOUTH[i] || 0, MOUTH[i + 1] || 0, u); }}
        function blinkAt(t) {{ const c = t % 3.7; return c < 0.14 ? Math.abs(c - 0.07) / 0.07 : 1; }}
        function rig(t) {{
          const o = mouthAt(t);
          const talk = mouthAt(t - 0.1) * 0.5 + o * 0.5;
          const rot = Math.sin(t * 1.6) * 1.6 + Math.sin(t * 4.1) * talk * 1.8;
          const bob = Math.sin(t * 2.0) * 6 - talk * 8;
          headG.setAttribute("transform", `translate(0 ${{bob.toFixed(2)}}) rotate(${{rot.toFixed(2)}} 450 640)`);
          bodyG.setAttribute("transform", `translate(0 ${{(Math.sin(t * 2.0 - 0.6) * 3).toFixed(2)}})`);
          mouthO.setAttribute("transform", `translate(450 562) scale(${{(0.85 + 0.15 * o).toFixed(3)}} ${{Math.max(0.02, o).toFixed(3)}}) translate(-450 -562)`);
          smile.setAttribute("opacity", clamp(1 - o * 4, 0, 1).toFixed(2));
          scan.setAttribute("x", (222 + ((t * 0.45) % 1) * 500 - 40).toFixed(1));
          visor.setAttribute("opacity", (0.82 + 0.18 * talk).toFixed(3));
          const b = blinkAt(t).toFixed(3);
          eyeL.setAttribute("ry", (20 * b).toFixed(2)); eyeR.setAttribute("ry", (20 * b).toFixed(2));
        }}

        const tl = gsap.timeline({{ paused: true }});
        const st = {{ t: 0 }};
        drawNet(0); rig(0);
        tl.to(st, {{ t: DUR, duration: DUR, ease: "none", onUpdate: () => {{ drawNet(st.t); rig(st.t); }} }}, 0);

        // intro
        tl.fromTo("#monkeyWrap", {{ opacity: 0, y: 140, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 1.0, ease: "expo.out" }}, 0.0);
        tl.fromTo("#logo", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.8, ease: "expo.out" }}, 0.3);
        tl.fromTo("#spot", {{ opacity: 0.5, scale: 0.95 }}, {{ opacity: 1, scale: 1.05, duration: 2.4, yoyo: true, repeat: 25, ease: "sine.inOut" }}, 0);

        // scene changes: flash + monkey hop
        {json.dumps(SCENES)}.forEach((s) => {{
          tl.fromTo("#flash", {{ opacity: 0 }}, {{ opacity: 0.5, duration: 0.12, ease: "power2.out", immediateRender: false }}, s - 0.1);
          tl.to("#flash", {{ opacity: 0, duration: 0.5, ease: "power2.in" }}, s + 0.02);
          tl.fromTo("#monkeyWrap", {{ y: 0 }}, {{ y: -36, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }}, s - 0.05);
        }});

        // headlines
        for (let i = 0; i < HEADS; i++) {{
          tl.fromTo(`#h${{i}} .display`, {{ opacity: 0, y: 40, scale: 0.9, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, document.getElementById(`h${{i}}`).getAttribute("data-start") * 1);
        }}
        // subtitles
        CUES.forEach((s, i) => tl.fromTo(`#cue${{i}} span`, {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "power3.out" }}, s));

        // end card
        tl.fromTo("#logo", {{ scale: 1 }}, {{ scale: 1.12, duration: 0.6, ease: "back.out(2)", immediateRender: false }}, 59.1);
        tl.fromTo("#cta-btn", {{ opacity: 0, y: 40, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "back.out(2)" }}, 59.2);
        tl.fromTo("#handle", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out" }}, 59.6);

        window.__timelines["main"] = tl;
      }})();
    </script>
  </body>
</html>
"""
open(f"{proj}/index.html", "w", encoding="utf-8").write(html)
print("ok")
