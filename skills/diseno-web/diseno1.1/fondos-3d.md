# Recetas de fondo 3D para /diseno

Tira el dado (`node -e "console.log(1 + Math.floor(Math.random() * 6))"`) y usa la receta que salga.
Todas comparten el **esqueleto común** de abajo: capa fija, dos variantes (completa en la landing,
tranquila en el resto), parallax por puntero y scroll, pausa con la pestaña oculta, menos elementos
en móvil y escena estática con prefers-reduced-motion. Los colores salen SIEMPRE de los tokens CSS
del proyecto (`getComputedStyle(document.documentElement).getPropertyValue("--accent")`), nunca hex
sueltos, para que el modo claro funcione solo.

Proyecto sin React (HTML/Vue/Svelte): el canvas y el CSS 3D son iguales; cambia los hooks por un
`<script type="module">` o el ciclo de vida del framework.

---

## Esqueleto común (React / Next.js con framer-motion)

```tsx
"use client";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { useMotionValue, useReducedMotion, useScroll, useSpring, type MotionValue } from "framer-motion";

export function AmbientBackground() {
  const full = usePathname() === "/";                 // completa en la landing, tranquila en el resto
  const reduce = useReducedMotion() ?? false;
  const [mobile, setMobile] = useState(true);
  useEffect(() => {
    const mq = window.matchMedia("(max-width: 767px)");
    const u = () => setMobile(mq.matches); u();
    mq.addEventListener("change", u); return () => mq.removeEventListener("change", u);
  }, []);

  // Parallax: puntero (solo pointer fino) + scroll, suavizados con spring.
  const rx = useMotionValue(0), ry = useMotionValue(0);
  const px = useSpring(rx, { stiffness: 40, damping: 18 }), py = useSpring(ry, { stiffness: 40, damping: 18 });
  useEffect(() => {
    if (reduce || !matchMedia("(pointer: fine)").matches) return;
    const on = (e: PointerEvent) => { rx.set((e.clientX / innerWidth - 0.5) * 2); ry.set((e.clientY / innerHeight - 0.5) * 2); };
    addEventListener("pointermove", on, { passive: true }); return () => removeEventListener("pointermove", on);
  }, [reduce, rx, ry]);
  const { scrollYProgress } = useScroll();
  const scroll = useSpring(scrollYProgress, { stiffness: 60, damping: 20 });

  return (
    <div aria-hidden className={`amb-root ${full ? "amb-full" : "amb-calm"}`}>
      {/* capa lejana: aurora o degradado que deriva lento */}
      {/* capa media: la receta (canvas o CSS 3D) */}
      {/* capa cercana: 2–4 objetos con más parallax */}
      <div className="amb-vignette" />
    </div>
  );
}
```

CSS mínimo del contenedor (el resto está en `plantillas/ambient.css`):

```css
body { isolation: isolate; }
.amb-root { position: fixed; inset: 0; z-index: -10; overflow: hidden; pointer-events: none; background: var(--bg); }
.amb-calm .amb-layer { opacity: .5; }
.amb-vignette { position: absolute; inset: 0;
  background: radial-gradient(ellipse 120% 90% at 50% 40%, transparent 45%, color-mix(in srgb, var(--bg) 85%, transparent)); }
```

Hook de canvas reutilizable (recetas 2, 3 y 4):

```tsx
function useCanvasLoop(
  el: HTMLCanvasElement | null, reduce: boolean,
  draw: (ctx: CanvasRenderingContext2D, w: number, h: number, t: number) => void,
) {
  useEffect(() => {
    if (!el) return;
    const ctx = el.getContext("2d"); if (!ctx) return;
    const dpr = Math.min(devicePixelRatio || 1, 2);
    let w = 0, h = 0, raf = 0;
    const resize = () => { w = el.clientWidth; h = el.clientHeight; el.width = w * dpr; el.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    resize(); addEventListener("resize", resize);
    if (reduce) { draw(ctx, w, h, 0); return () => removeEventListener("resize", resize); }
    const loop = (t: number) => { draw(ctx, w, h, t / 1000); raf = requestAnimationFrame(loop); };
    const vis = () => { cancelAnimationFrame(raf); if (!document.hidden) raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop); document.addEventListener("visibilitychange", vis);
    return () => { cancelAnimationFrame(raf); removeEventListener("resize", resize); document.removeEventListener("visibilitychange", vis); };
  }, [el, reduce, draw]);
}
```

Proyección 3D simple para canvas: `const k = FOV / (FOV + z); sx = cx + x * k; sy = cy + y * k;` con `FOV ≈ 500`.
Rotación en Y: `x' = x*cos(a) - z*sin(a); z' = x*sin(a) + z*cos(a)`.

---

## 1. Galería de figuras CSS 3D + constelación

**Qué se ve:** cubos, prismas y un giroscopio de anillos girando en 3D real a distintas profundidades,
con brillo del color del acento, estrellas que vuelan hacia la cámara y se unen en constelaciones,
aurora y haces de luz.
**Encaja con:** casi todo; ideal para producto cripto, educación o seguridad.
**Implementación:** copia `plantillas/AmbientBackground.tsx` y `plantillas/ambient.css`, renombra
los tokens (`--navy`, `--gold`, `--info`, `--violet`) a los del proyecto y ajusta la lista `FULL` /
`CALM` (posición, tamaño, profundidad 0–1, velocidad, tono, `mobile: true` para las que se quedan en
celular). Cambia las figuras por objetos del tema si aplica (por ejemplo, un anillo = moneda).
**Probada en producción** (FYV Box).

## 2. Terreno de ondas (wireframe)

**Qué se ve:** una malla de puntos o líneas en perspectiva, como un terreno o un océano digital,
que ondula lento hacia el horizonte; el puntero inclina la cámara.
**Encaja con:** datos, finanzas, pagos, infraestructura.

```tsx
function WaveTerrain({ reduce, dense, px }: { reduce: boolean; dense: boolean; px: MotionValue<number> }) {
  const [el, setEl] = useState<HTMLCanvasElement | null>(null);
  const draw = useCallback((ctx: CanvasRenderingContext2D, w: number, h: number, t: number) => {
    const color = getComputedStyle(document.documentElement).getPropertyValue("--accent").trim();
    const COLS = w < 768 ? 28 : dense ? 56 : 40, ROWS = w < 768 ? 16 : 26, FOV = 500;
    ctx.clearRect(0, 0, w, h); ctx.strokeStyle = color; ctx.lineWidth = 1;
    const tilt = px.get() * 0.15;
    for (let r = 0; r < ROWS; r++) {
      ctx.beginPath();
      for (let c = 0; c <= COLS; c++) {
        const x = (c / COLS - 0.5) * w * 2.2;
        const z = r * 60 + 40;
        const y = Math.sin(c * 0.35 + t * 0.8) * 22 + Math.cos(r * 0.45 + t * 0.6) * 18 + 160;
        const xr = x * Math.cos(tilt) - z * Math.sin(tilt), zr = x * Math.sin(tilt) + z * Math.cos(tilt);
        const k = FOV / (FOV + zr), sx = w / 2 + xr * k, sy = h * 0.55 + y * k;
        c ? ctx.lineTo(sx, sy) : ctx.moveTo(sx, sy);
      }
      ctx.globalAlpha = 0.5 * (1 - r / ROWS); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }, [dense, px]);
  useCanvasLoop(el, reduce, draw);
  return <canvas ref={setEl} className="amb-layer" style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }} />;
}
```

Añade encima una aurora suave y 2–3 objetos CSS 3D cercanos (de la receta 1) para la capa frontal.

## 3. Globo de puntos con arcos

**Qué se ve:** una esfera hecha de cientos de puntos (distribución de Fibonacci) que gira despacio;
cada pocos segundos aparece un arco luminoso entre dos puntos, como una transferencia.
**Encaja con:** remesas, pagos internacionales, comunidades, redes.

```tsx
// Puntos de la esfera (una vez): N = móvil ? 350 : 700
const pts = Array.from({ length: N }, (_, i) => {
  const y = 1 - (i / (N - 1)) * 2, r = Math.sqrt(1 - y * y), th = Math.PI * (3 - Math.sqrt(5)) * i;
  return [Math.cos(th) * r, y, Math.sin(th) * r];
});
// En draw: a = t * 0.12 + px.get() * 0.4; R = Math.min(w, h) * 0.38; centro a la derecha del hero en escritorio.
// Para cada punto: rota en Y por a, proyecta, alpha = 0.25 + 0.75 * (z > 0 ? z : 0) (los de atrás tenues), radio 1–1.8.
// Arcos: guarda {from, to, born}; dibuja una curva cuadrática elevada (punto medio * 1.35) con
// ctx.setLineDash y un "cometa" que recorre la curva durante 1.6 s; crea uno nuevo cada 1.2 s (máx. 4).
```

## 4. Túnel warp de anillos

**Qué se ve:** anillos o polígonos que vienen desde el fondo hacia la cámara, girando, como un
túnel de datos; el centro del túnel sigue al puntero.
**Encaja con:** velocidad, gaming, transacciones instantáneas, IA.

```tsx
// Estado: rings = Array.from({ length: móvil ? 14 : 24 }, (_, i) => ({ z: i * 80, rot: i * 0.3 }))
// En draw: para cada anillo z -= (dense ? 2.4 : 1.2); si z < 1 → z += rings.length * 80.
// k = 500 / z; radio = 260 * k; centro = (w/2 + px*80, h/2 + py*60);
// Dibuja un polígono de 6 lados rotado por rot + t*0.2, lineWidth = 1 + k, alpha = min(1, k*0.8) * 0.6.
// Alterna dos tokens de color por índice. Con reduce: dibuja una sola vez con z fijos.
```

## 5. Objetos del tema flotando (CSS 3D)

**Qué se ve:** 5–8 objetos propios del proyecto en CSS 3D real: monedas con canto (dos caras + un
cilindro de 12 segmentos), tarjetas con frente y reverso, escudos, candados o bloques apilados; flotan,
giran lento y a veces voltean mostrando el reverso.
**Encaja con:** cuando el proyecto tiene un objeto claro (moneda, tarjeta, ticket, credencial).

```tsx
// Moneda: contenedor preserve-3d; cara frontal y trasera (círculos con el símbolo/ícono del proyecto,
// translateZ(±grosor/2)); canto: 12 <span> de ancho 2πr/12 y alto = grosor, cada uno
// rotateY(i*30deg) translateZ(r). Animación: rotateY 360deg en 8–14 s, más flotación translateY ±12px.
// Tarjeta: dos caras (frente con el wordmark, reverso con un patrón) y backface-visibility: hidden;
// cada 6–10 s un flip de 180° con spring (framer-motion animate rotateY).
// Reutiliza Float/profundidad/parallax de plantillas/AmbientBackground.tsx.
```

## 6. Malla low-poly con Three.js

**Qué se ve:** un icosaedro o nudo toroidal en wireframe que respira y gira, con una nube de
partículas alrededor y luz del color del acento. Es la más "3D de verdad".
**Encaja con:** producto tech/IA/infra, landing que necesite un momento wow.
**Solo si** el proyecto usa bundler (Next, Vite). Instala `three` (y si ya hay React, opcionalmente
`@react-three/fiber`). Carga el componente con `next/dynamic` y `ssr: false` para no afectar el
primer render.

```tsx
// Vanilla three dentro de useEffect:
// renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: !móvil });
// renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
// mesh = new THREE.Mesh(new THREE.IcosahedronGeometry(1.6, móvil ? 1 : 2),
//   new THREE.MeshBasicMaterial({ color: accent, wireframe: true, transparent: true, opacity: .35 }));
// points = new THREE.Points(geometría con 600–1500 posiciones aleatorias en una esfera, PointsMaterial size .02);
// Loop: mesh.rotation.y += .0015; mesh.rotation.x = py * .3; escala 1 + sin(t) * .03; cámara.position.x = px * .4.
// Pausa con document.hidden; con reduce, renderiza un frame y detente; en cleanup: renderer.dispose(),
// geometry.dispose(), material.dispose().
```

---

## Checklist del fondo antes de entregar

- [ ] Se ve en la landing (completa) y en otra pantalla (tranquila), en oscuro y claro.
- [ ] A 380 px: menos elementos, sin scroll horizontal, el texto se lee (4.5:1).
- [ ] `document.getAnimations().length > 0` o el canvas cambia entre dos frames (si el navegador
      integrado congela, confirma con Chrome headless `--virtual-time-budget`).
- [ ] Con prefers-reduced-motion: escena quieta.
- [ ] Pestaña oculta: el requestAnimationFrame se detiene.
- [ ] DESIGN_NOTES dice qué receta salió en el dado y cómo se adaptó al tema.
