"""Genera mono_template_ilustrado.html: la plantilla del mono con la ilustración real recortada
(assets/mono/busto.png, 800x800) animada como marioneta: mandíbula con lip-sync, ojos LED en el
visor, respiración, cabeceo y pulsos en los momentos clave. Uso: python -I make_ilustrado.py"""
import os
import re

D = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(D, "mono_template.html"), encoding="utf-8").read()

# Jaw polygon (bust image coords) and the base image with that hole cut out
JAW = [(238, 486), (312, 489), (374, 494), (434, 486), (446, 522), (420, 564), (300, 570), (234, 542)]
jaw_poly = ", ".join(f"{x}px {y}px" for x, y in JAW)
jaw_path = "M" + " L".join(f"{x} {y}" for x, y in JAW) + " Z"

HERO = f'''<div id="hero"><div id="heroHop"><div id="bustPop">
          <div id="bust">
            <svg class="bustLayer" viewBox="0 0 800 800"><ellipse cx="420" cy="770" rx="250" ry="40" fill="#000" opacity="0.35" /></svg>
            <img id="bustBase" class="bustLayer" src="assets/mono/busto.png" alt="" />
            <svg class="bustLayer" viewBox="0 0 800 800">
              <ellipse id="mouthIn" cx="314" cy="490" rx="62" ry="0.1" fill="#2a0a08" />
              <ellipse id="tongue" cx="314" cy="496" rx="30" ry="0.1" fill="#c45a6a" />
            </svg>
            <img id="bustJaw" class="bustLayer" src="assets/mono/busto.png" alt="" />
            <svg id="faceSvg" viewBox="0 -220 800 1020" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <clipPath id="glassClip"><rect x="190" y="258" width="266" height="88" rx="38" /></clipPath>
                <filter id="ledGlow" x="-50%" y="-80%" width="200%" height="260%"><feGaussianBlur stdDeviation="5" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
                <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" /></filter>
              </defs>
              <rect x="190" y="258" width="266" height="88" rx="38" fill="#04163f" opacity="0.62" />
              <rect id="visorGlow" x="190" y="258" width="266" height="88" rx="38" fill="#22e6ff" opacity="0.15" />
              <g clip-path="url(#glassClip)">
                <g id="eyes" fill="#e6feff" stroke="#e6feff" filter="url(#ledGlow)">
                  <g id="eN" stroke="none"><rect x="236" y="287" width="64" height="28" rx="14" /><rect x="364" y="289" width="56" height="26" rx="13" /></g>
                  <g id="eH" fill="none" stroke-width="10" stroke-linecap="round" opacity="0"><path d="M240 312 Q268 280 296 312" /><path d="M366 312 Q392 282 418 312" /></g>
                  <g id="eW" opacity="0"><rect x="236" y="287" width="64" height="28" rx="14" stroke="none" /><path d="M366 306 Q392 292 418 306" fill="none" stroke-width="10" stroke-linecap="round" /></g>
                  <g id="eS" stroke="none" opacity="0"><polygon points="268,274 275,292 294,293 279,305 284,324 268,313 252,324 257,305 242,293 261,292" /><polygon points="392,276 398,292 416,293 402,304 406,322 392,312 378,322 382,304 368,293 386,292" /></g>
                  <g id="eL" stroke="none" opacity="0" fill="#ff7ad9"><path d="M268 322 C 238 302, 251 278, 268 293 C 285 278, 298 302, 268 322 Z" /><path d="M392 322 C 364 302, 376 280, 392 294 C 408 280, 420 302, 392 322 Z" /></g>
                </g>
                <rect id="scan" x="170" y="258" width="34" height="88" fill="#ffffff" opacity="0.22" />
              </g>
              <path d="M210 270 L300 266" stroke="#ffffff" stroke-opacity="0.6" stroke-width="6" stroke-linecap="round" />
              <g id="helmet" opacity="0">
                <path d="M196 196 Q392 -78 606 176 Z" fill="#ffc83d" stroke="#0a1030" stroke-width="8" stroke-linejoin="round" />
                <path d="M236 176 Q290 70 380 34" fill="none" stroke="#fff3c4" stroke-width="9" stroke-linecap="round" opacity="0.7" />
                <path d="M372 30 Q392 24 412 30 L420 186 L364 190 Z" fill="#ffd76a" stroke="#0a1030" stroke-width="6" />
                <path d="M170 204 Q400 150 636 178 L640 206 Q400 182 174 234 Z" fill="#ffb300" stroke="#0a1030" stroke-width="7" stroke-linejoin="round" />
              </g>
              <g id="bulb" opacity="0">
                <circle cx="420" cy="-90" r="84" fill="#fff4a8" opacity="0.5" filter="url(#softGlow)" />
                <circle cx="420" cy="-95" r="50" fill="#fff6b8" stroke="#0a1030" stroke-width="5" />
                <rect x="401" y="-48" width="38" height="30" rx="6" fill="#cfd8ff" stroke="#0a1030" stroke-width="4" />
                <g stroke="#ffe680" stroke-width="7" stroke-linecap="round"><line x1="420" y1="-168" x2="420" y2="-190" /><line x1="358" y1="-142" x2="342" y2="-158" /><line x1="482" y1="-142" x2="498" y2="-158" /><line x1="344" y1="-95" x2="322" y2="-95" /><line x1="496" y1="-95" x2="518" y2="-95" /></g>
              </g>
            </svg>
          </div>
        </div></div>
        <div style="display: none"><i id="armR"></i><i id="armL"></i><i id="handR"></i><i id="thumbR"></i><i id="jetpack"></i></div>
        </div>'''

a = s.index('<div id="hero"><div id="heroHop">')
b = s.index("</svg>\n        </div></div>", a) + len("</svg>\n        </div></div>")
s = s[:a] + HERO + s[b:]

s = s.replace(
    "#hero { position: absolute; left: 0; top: 0; width: 600px; height: 1050px; }",
    "#hero { position: absolute; left: 0; top: 0; width: 800px; height: 800px; }\n"
    "      #bustPop { position: absolute; inset: 0; }\n"
    "      #bust { position: absolute; inset: 0; transform-origin: 420px 640px; }\n"
    "      .bustLayer { position: absolute; left: 0; top: 0; width: 800px; height: 800px; }\n"
    f"      #bustBase {{ clip-path: path(evenodd, \"M0 0 H800 V800 H0 Z {jaw_path}\"); }}\n"
    f"      #bustJaw {{ clip-path: polygon({jaw_poly}); }}\n"
    "      #faceSvg { position: absolute; left: 0; top: -220px; width: 800px; height: 1020px; overflow: visible; }",
)
assert "#bustJaw" in s
s = s.replace("#heroSvg { position: absolute; inset: 0; width: 600px; height: 1050px; overflow: visible; }", "")

# new rig (replaces the vector rig)
a = s.index("        const face = { lookX: 0, lookY: 0, brow: 0, fly: 0 };")
b = s.index("        const tl = gsap.timeline({ paused: true });")
RIG = r'''        const face = { lookX: 0, lookY: 0, brow: 0, fly: 0 };
        const $ = (id) => document.getElementById(id);
        const bust = $("bust"), jaw = $("bustJaw"), mouthIn = $("mouthIn"), tongue = $("tongue"), eyes = $("eyes"), eN = $("eN");
        const scan = $("scan"), visorGlow = $("visorGlow");
        const mouthAt = (t) => { const f = t * 30, i = Math.floor(f), u = f - i; return lerp(MOUTH[i] || 0, MOUTH[i + 1] || 0, u); };
        const blinkAt = (t) => { const c = (t + 1.3) % 3.7; return c < 0.16 ? 0.12 + 0.88 * Math.abs(c - 0.08) / 0.08 : 1; };
        function rig(t) {
          const o = mouthAt(t), talk = (mouthAt(t - 0.12) + o) / 2;
          const breath = Math.sin(t * 2.1) * 0.006;
          const rot = Math.sin(t * 1.4) * 1.2 + Math.sin(t * 4.3) * talk * 1.6;
          const bob = Math.sin(t * 2.1 + 0.4) * 4 - talk * 6;
          bust.style.transform = `translate(0px, ${bob.toFixed(2)}px) rotate(${rot.toFixed(2)}deg) scale(${(1 + breath).toFixed(4)}, ${(1 - breath).toFixed(4)})`;
          const d = o * 30;
          jaw.style.transform = `translate(${(d * 0.12).toFixed(2)}px, ${d.toFixed(2)}px)`;
          mouthIn.setAttribute("cy", (490 + d / 2).toFixed(2)); mouthIn.setAttribute("ry", Math.max(0.1, d / 2 + 1).toFixed(2));
          tongue.setAttribute("cy", (488 + d - 3).toFixed(2)); tongue.setAttribute("ry", Math.max(0.1, Math.min(8, d / 3)).toFixed(2));
          const b = blinkAt(t);
          eyes.setAttribute("transform", `translate(${face.lookX.toFixed(2)} ${face.lookY.toFixed(2)})`);
          eN.setAttribute("transform", `translate(0 301) scale(1 ${b.toFixed(3)}) translate(0 -301)`);
          scan.setAttribute("x", (170 + ((t * 0.5) % 1.4) * 320).toFixed(1));
          visorGlow.setAttribute("opacity", (0.1 + 0.3 * talk).toFixed(3));
        }

'''
s = s[:a] + RIG + s[b:]

# placement: the box is now 800x800 (centre 400,400)
s = s.replace("const place = (cx, cy, s) => ({ x: cx - 300, y: cy - 525, scale: s });",
              "const place = (cx, cy, s) => ({ x: cx - 400, y: cy - 400, scale: s });")
# bulb pivot moved
s = s.replace('svgOrigin: "300 -60"', 'svgOrigin: "420 -95"')
# the bust replaces arm gestures with pops on the beats that used to be gestures
s = s.replace("        // ---------- arm poses ----------",
              "        // ---------- beats: the bust pops where the vector rig used to gesture ----------\n"
              "        [6.3, 10.8, 13.84, 15.68, 27.75, 29.0, 34.45, 37.0, 50.0, 58.0, 59.13].forEach((t) =>\n"
              "          tl.fromTo(\"#bustPop\", { scale: 1, transformOrigin: \"52% 80%\" }, { keyframes: { scale: [1.06, 0.98, 1] }, duration: 0.45, ease: \"power2.out\", immediateRender: false }, t));\n"
              "        // ---------- arm poses (no-ops on hidden stubs in the illustrated version) ----------")
# bigger bust: same slots, ~30 % larger
s = s.replace("const place = (cx, cy, s) => ({ x: cx - 400, y: cy - 400, scale: s });",
              "const place = (cx, cy, s) => ({ x: cx - 400, y: cy - 400, scale: s * 1.3 });")
s = s.replace('{ scale: 0.2, opacity: 0 }, { scale: 0.72, opacity: 1,', '{ scale: 0.26, opacity: 0 }, { scale: 0.94, opacity: 1,')
# community members: small copies of the same illustration (consistent style), coloured halo, some mirrored
s = s.replace(
    """        const miniSvg = (parent, cls, style, color) => {""",
    """        let MI = 0;
        const miniSvg = (parent, cls, style, color) => {
          const im = document.createElement("img"); im.src = "assets/mono/busto.png"; im.alt = ""; im.className = cls + " mimg";
          im.setAttribute("style", style + `;filter:drop-shadow(0 0 12px ${color}) drop-shadow(0 6px 0 rgba(0,0,0,0.25));${MI++ % 2 ? "scale:-1 1;" : ""}`);
          parent.appendChild(im); return im;
        };
        const miniSvgOld = (parent, cls, style, color) => {""")
s = s.replace("      .bustLayer {", "      .mimg { object-fit: contain; }\n      .bustLayer {")
s = s.replace('<svg id="friend" viewBox="0 0 200 230"><use href="#mini" width="200" height="230" style="color: #8b5cf6" /></svg>',
              '<img id="friend" class="mimg" src="assets/mono/busto.png" alt="" style="filter: drop-shadow(0 0 18px #8b5cf6)" />')
s = s.replace("#friend { position: absolute; left: 640px; top: 900px; width: 360px; height: 414px; }",
              "#friend { position: absolute; left: 600px; top: 900px; width: 440px; height: 440px; }")
assert "miniSvgOld" in s and 'img id="friend"' in s

open(os.path.join(D, "mono_template_ilustrado.html"), "w", encoding="utf-8").write(s)
print("ok", len(s))
