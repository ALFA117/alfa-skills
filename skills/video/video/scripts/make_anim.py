"""Genera anim_template.html: la misma plantilla (zonas, capítulos, titulares, globo, cortinas, subtítulos,
mapa de tiempos) SIN mascota. El escenario de cada escena lo ocupa una animación propia:
globo + órbitas, torre de bloques, emblema hexagonal, foco/personas/red, túnel warp y emblema final.
Uso: python -I make_anim.py"""
import os
import re

D = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(D, "mono_template.html"), encoding="utf-8").read()


def R(a, b, cnt=1):
    global s
    assert a in s, "FALTA: " + a[:100]
    s = s.replace(a, b) if cnt == 0 else s.replace(a, b, cnt)


def cut(a_marker, b_marker, keep_b=True):
    global s
    a = s.index(a_marker)
    b = s.index(b_marker, a)
    s = s[:a] + (s[b:] if keep_b else s[b + len(b_marker):])


def emblem(eid):
    return (f'<svg id="{eid}" class="emb" viewBox="-200 -200 400 400">'
            '<polygon class="hex" points="0,-180 156,-90 156,90 0,180 -156,90 -156,-90" fill="rgba(8,14,40,0.82)" stroke="url(#embG)" stroke-width="10" stroke-linejoin="round" />'
            '<g class="inner"><polygon points="0,-138 120,-69 120,69 0,138 -120,69 -120,-69" fill="none" stroke="#22e6ff" stroke-opacity="0.4" stroke-width="3" stroke-dasharray="14 10" /></g>'
            '<text class="mm" x="0" y="52" text-anchor="middle" font-family="Unbounded, sans-serif" font-weight="800" font-size="150" fill="url(#embG)">M</text>'
            '</svg>')


# ---------- remove the mascot ----------
cut("      <!-- HERO (persistent) -->", "      <!-- chrome -->")
cut("        const face = { lookX: 0, lookY: 0, brow: 0, fly: 0 };", "        const tl = gsap.timeline({ paused: true });")
R("rig(0); drawGlobe(0);", "drawGlobe(0);")
R("onUpdate: () => { rig(st.t); drawGlobe(st.t); } }, 0);", "onUpdate: () => drawGlobe(st.t) }, 0);")
cut("        // ---------- hero placement per scene ----------", "        // ---------- scene 1 ----------")
s = re.sub(r'\n\s*tl\.to\("#hero", \{ \.\.\.place\(540, 990, 0\.66\).*?\n', "\n", s)

# "people" are abstract avatars, not monkeys
s = re.sub(r'<symbol id="mini" viewBox="0 0 200 230">.*?</symbol>', '''<symbol id="mini" viewBox="0 0 200 230">
          <circle cx="100" cy="118" r="92" fill="rgba(8,14,40,0.88)" stroke="currentColor" stroke-width="6" />
          <circle cx="100" cy="92" r="32" fill="currentColor" />
          <path d="M42 182 Q46 130 100 128 Q154 130 158 182 Q100 204 42 182 Z" fill="currentColor" />
        </symbol>
        <linearGradient id="embG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22e6ff" /><stop offset="0.55" stop-color="#7dd3fc" /><stop offset="1" stop-color="#ffc83d" /></linearGradient>''', s, count=1, flags=re.S)

# ---------- S1: globe centred on the stage + orbits ----------
R('const GL = { cx: 540, cy: 2140, R: 820, a: 1, tilt: 1.05 };', 'const GL = { cx: 540, cy: 990, R: 330, a: 1, tilt: 0.38 };')
R('tl.set(GL, { cx: 540, cy: 2140, R: 820, a: 1 }, 0);', 'tl.fromTo(GL, { cx: 540, cy: 990, R: 40, a: 0 }, { R: 330, a: 1, duration: 1.8, ease: "expo.out" }, 0.1);')
R('<div id="shoot"></div>', '''<div id="shoot"></div>
          <svg id="orbit" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px">
            <g id="orbG"><ellipse cx="540" cy="990" rx="440" ry="120" fill="none" stroke="#22e6ff" stroke-opacity="0.55" stroke-width="3" stroke-dasharray="8 14" /><circle cx="980" cy="990" r="13" fill="#ffc83d" /><circle cx="100" cy="990" r="8" fill="#22e6ff" /></g>
            <g id="orbG2"><ellipse cx="540" cy="990" rx="400" ry="210" fill="none" stroke="#8b5cf6" stroke-opacity="0.45" stroke-width="2" /><circle cx="540" cy="780" r="9" fill="#ff5d8f" /></g>
          </svg>''')

# ---------- S2: tower centred ----------
R('const CUBES = [[628, 1180, 8.08], [754, 1180, 8.55], [565, 1075, 8.96], [691, 1075, 10.8], [817, 1075, 10.95], [628, 970, 12.24], [754, 970, 13.84], [691, 865, 14.0]];',
  'const CUBES = [[414, 1180, 8.08], [540, 1180, 8.55], [351, 1075, 8.96], [477, 1075, 10.8], [603, 1075, 10.95], [414, 970, 12.24], [540, 970, 13.84], [477, 865, 14.0]];')
R('"left:950px;top:1180px;width:116px;height:134px", "#ff4fd8"', '"left:800px;top:1170px;width:130px;height:150px", "#ff4fd8"')
R('"left:14px;top:1180px;width:116px;height:134px", "#ffc83d"', '"left:150px;top:1170px;width:130px;height:150px", "#ffc83d"')

# ---------- S3: emblem under the spotlight ----------
R('<div id="stage"></div>', '<div id="stage"></div>\n          ' + emblem("emb3"))

# ---------- S4: bulb, two people + link, then the network ----------
s = re.sub(r'\s*<div class="say" id="sayA".*?</div>\s*<div class="say" id="sayB".*?</div>', '', s, flags=re.S)
R('<svg id="friend" viewBox="0 0 200 230">', '''<svg id="bulb4" viewBox="-130 -150 260 300">
          <circle cx="0" cy="-10" r="110" fill="#fff4a8" opacity="0.35" filter="url(#bulbGlow)" />
          <circle cx="0" cy="-20" r="70" fill="#fff6b8" stroke="#0a1030" stroke-width="6" />
          <path d="M-22 -30 Q0 -60 22 -30 M0 -40 L0 30" fill="none" stroke="#ffb300" stroke-width="6" stroke-linecap="round" />
          <rect x="-30" y="44" width="60" height="22" rx="6" fill="#cfd8ff" stroke="#0a1030" stroke-width="5" /><rect x="-24" y="66" width="48" height="18" rx="6" fill="#9aa7d6" stroke="#0a1030" stroke-width="5" />
          <g stroke="#ffe680" stroke-width="9" stroke-linecap="round"><line x1="0" y1="-112" x2="0" y2="-140" /><line x1="-80" y1="-82" x2="-100" y2="-102" /><line x1="80" y1="-82" x2="100" y2="-102" /><line x1="-104" y1="-20" x2="-128" y2="-20" /><line x1="104" y1="-20" x2="128" y2="-20" /></g>
          <defs><filter id="bulbGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18" /></filter></defs>
        </svg>
        <svg id="me" viewBox="0 0 200 230"><use href="#mini" width="200" height="230" style="color: #22e6ff" /></svg>
        <svg id="friend" viewBox="0 0 200 230">''')
R("#friend { position: absolute; left: 640px; top: 900px; width: 360px; height: 414px; }",
  "#friend { position: absolute; left: 640px; top: 880px; width: 330px; height: 380px; }\n"
  "      #me { position: absolute; left: 110px; top: 880px; width: 330px; height: 380px; }\n"
  "      #bulb4 { position: absolute; left: 410px; top: 780px; width: 260px; height: 300px; }\n"
  "      .emb { position: absolute; left: 330px; top: 790px; width: 420px; height: 420px; filter: drop-shadow(0 0 30px rgba(34, 230, 255, 0.45)); }")
R("#link { position: absolute; left: 470px; top: 1080px; width: 240px;", "#link { position: absolute; left: 430px; top: 1060px; width: 220px;")
R('tl.set(["#friend", "#sayA", "#sayB", "#link", "#hr1", "#hr2"], { opacity: 0 }, 28.48);',
  'tl.set(["#friend", "#me", "#bulb4", "#link", "#hr1", "#hr2"], { opacity: 0 }, 28.48);\n'
  '        tl.fromTo("#bulb4", { opacity: 0, scale: 0.3, transformOrigin: "50% 60%" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(3)", immediateRender: false }, 29.0);\n'
  '        tl.to("#bulb4", { scale: 1.08, duration: 0.4, yoyo: true, repeat: 3, ease: "sine.inOut" }, 29.5);\n'
  '        tl.to("#bulb4", { opacity: 0, scale: 0.6, duration: 0.3, ease: "power2.in" }, 31.55);\n'
  '        tl.fromTo("#me", { opacity: 0, x: -300 }, { opacity: 1, x: 0, duration: 0.5, ease: "expo.out", immediateRender: false }, 31.7);\n'
  '        tl.to("#me", { x: 265, scale: 0.85, duration: 0.5, ease: "power3.inOut" }, 34.45);')
for pat in [r'\n\s*tl\.fromTo\("#sayA".*?\n', r'\n\s*tl\.fromTo\("#sayB".*?\n', r'\n\s*tl\.fromTo\("\.say i".*?\n', r'\n\s*tl\.to\(\["#sayA", "#sayB"\].*?\n']:
    s, n = re.subn(pat, "\n", s, count=1)
    assert n == 1, pat

# ---------- S5: platform centred ----------
R("#plat { position: absolute; left: 400px; top: 760px; width: 640px; height: 640px; }", "#plat { position: absolute; left: 220px; top: 760px; width: 640px; height: 640px; }")

# traveller through the warp that lands on the "TÚ" seat
R('<div id="plat"><div id="plat-floor"></div><div id="you">TÚ</div></div>',
  '<svg id="warpMe" viewBox="0 0 200 230" style="position:absolute;left:410px;top:850px;width:260px;height:300px"><use href="#mini" width="200" height="230" style="color: #22e6ff" /></svg>\n'
  '        <div id="plat"><div id="plat-floor"></div><div id="you">TÚ</div></div>')
R("        // ---------- scene 5 ----------", '''        // ---------- scene 5 ----------
        tl.fromTo("#warpMe", { scale: 0.15, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 1.0, ease: "expo.out" }, 43.3);
        tl.fromTo("#warpMe", { rotation: -6 }, { rotation: 6, duration: 0.6, yoyo: true, repeat: 9, ease: "sine.inOut", immediateRender: false }, 44.2);
        tl.to("#warpMe", { y: 225, scale: 0.42, duration: 0.9, ease: "power3.inOut" }, 49.45);
        tl.to("#warpMe", { opacity: 0, duration: 0.2 }, 50.3);''')

# ---------- S6: big emblem on the stage ----------
R('<div class="layer" id="confetti"></div>', '<div class="layer" id="confetti"></div>\n        ' + emblem("emb6"))

# ---------- animations for the new stage pieces ----------
R("        // ---------- scene 1 ----------", '''        // ---------- stage pieces (no mascot) ----------
        tl.fromTo("#orbit", { opacity: 0 }, { opacity: 1, duration: 1.2, ease: "power2.out" }, 0.8);
        tl.fromTo("#orbG", { rotation: 0, svgOrigin: "540 990" }, { rotation: 360, duration: 7.2, ease: "none" }, 0);
        tl.fromTo("#orbG2", { rotation: 0, svgOrigin: "540 990" }, { rotation: -220, duration: 7.2, ease: "none" }, 0);
        tl.fromTo("#emb3 .hex", { strokeDasharray: 1200, strokeDashoffset: 1200 }, { strokeDashoffset: 0, duration: 1.3, ease: "power2.inOut" }, 15.3);
        tl.fromTo("#emb3 .mm", { opacity: 0, scale: 0.3, svgOrigin: "0 0" }, { opacity: 1, scale: 1, duration: 0.6, ease: "back.out(2.2)" }, 15.68);
        tl.fromTo("#emb3 .inner", { rotation: 0, svgOrigin: "0 0" }, { rotation: 120, duration: 13.2, ease: "none" }, 15.2);
        tl.fromTo("#emb3", { scale: 1, transformOrigin: "50% 50%" }, { keyframes: { scale: [1.08, 0.98, 1] }, duration: 0.5, ease: "power2.out", immediateRender: false }, 24.35);
        tl.fromTo("#emb6", { opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.8, ease: "back.out(1.6)" }, 55.2);
        tl.fromTo("#emb6 .hex", { strokeDasharray: 1200, strokeDashoffset: 1200 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" }, 55.2);
        tl.fromTo("#emb6 .inner", { rotation: 0, svgOrigin: "0 0" }, { rotation: -90, duration: 7.4, ease: "none" }, 55.05);
        tl.fromTo("#emb6", { scale: 1 }, { keyframes: { scale: [1.1, 0.97, 1] }, duration: 0.5, ease: "power2.out", immediateRender: false }, 58.0);
        tl.fromTo("#emb6", { scale: 1 }, { keyframes: { scale: [1.1, 0.97, 1] }, duration: 0.5, ease: "power2.out", immediateRender: false }, 59.13);

        // ---------- scene 1 ----------''')

# Globe framing as a pure function of time (a proxy onUpdate at t=0 renders BEFORE later tweens,
# so tweening GL lagged one frame and broke seeks). Keyframes are in reference time -> T().
a = s.index("        tl.fromTo(GL, { cx: 540, cy: 990, R: 40, a: 0 }")
b = s.index("\n", s.index("tl.to(GL, { cx: 540, cy: 820, R: 700, a: 0.75", a)) + 1
s = s[:a] + s[b:]
R("        const st = { t: 0 };", '''        const GLK = [[0, 540, 990, 40, 0], [1.9, 540, 990, 330, 1], [6.85, 540, 990, 330, 1], [7.45, 900, 420, 300, 0.55],
          [14.9, 900, 420, 300, 0.55], [15.5, 220, 640, 380, 0.45], [28.2, 220, 640, 380, 0.45], [28.8, 540, 900, 620, 0.5],
          [43.0, 540, 900, 620, 0.5], [43.4, 540, 900, 620, 0], [49.4, 680, 1500, 520, 0], [50.2, 680, 1500, 520, 0.6],
          [54.8, 680, 1500, 520, 0.6], [55.6, 540, 820, 700, 0.75]].map((r) => [T(r[0]), ...r.slice(1)]);
        function glAt(t) {
          let i = 1; while (i < GLK.length - 1 && t > GLK[i][0]) i++;
          const A = GLK[i - 1], B = GLK[i], u = Math.min(1, Math.max(0, (t - A[0]) / (B[0] - A[0] || 1))), e = u * u * (3 - 2 * u);
          GL.cx = A[1] + (B[1] - A[1]) * e; GL.cy = A[2] + (B[2] - A[2]) * e; GL.R = A[3] + (B[3] - A[3]) * e; GL.a = A[4] + (B[4] - A[4]) * e;
        }
        const st = { t: 0 };''')
R("        function drawGlobe(t) {", "        function drawGlobe(t) {\n          glAt(t);")

for sel in ("#hero", "#heroHop", "#heroSvg"):
    s = re.sub(r"\n\s*" + re.escape(sel) + r" \{[^}]*\}", "", s)
assert "heroSvg" not in s
open(os.path.join(D, "anim_template.html"), "w", encoding="utf-8").write(s)
print("ok", len(s))
