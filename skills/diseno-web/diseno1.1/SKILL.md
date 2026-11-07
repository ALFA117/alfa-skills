---
name: diseno1.1
description: "Versión 1.1 del prompt de diseño del usuario: frontend y animaciones con UI/UX Pro Max (buscador local de estilos, paletas, tipografías, guías UX y stacks) + Motion v13 (API verificada contra el repo oficial) + fondo 3D animado, sistema de diseño, móvil primero, estados, honestidad, accesibilidad, SEO y verificación con capturas. Úsala cuando el usuario escriba /diseno1.1, /diseño1.1 o 'diseño 1.1', o pida 'rediseña con pro max y motion', 'haz el front con animaciones', 'diseño completo con animaciones'. Los argumentos son los cambios que quiere en este proyecto."
argument-hint: "cambios que quieres en este proyecto (vacío = rediseño completo)"
---

Vas a rediseñar y mejorar el frontend de este proyecto. En este proyecto quiero que hagas los siguientes cambios: $ARGUMENTS

Si no escribí cambios, haz un rediseño completo con todo lo de abajo. Todo lo que me escribas va en español. Trabajo solo contigo: decide y avanza sin pedirme validación; pregúntame únicamente si algo es irreversible o si falta un dato que solo yo tengo (llaves, cuentas, textos legales).

## Herramientas de esta skill (todo vive junto a este archivo)

La carpeta de esta skill es `~/.claude/skills/diseno1.1/` (en Windows `%USERPROFILE%\.claude\skills\diseno1.1\`). Úsala con ruta completa, no asumas el directorio actual.

1. **UI/UX Pro Max** (`uipro/`): buscador local, sin dependencias, Python 3.
   - Sistema de diseño completo (obligatorio en rediseños y páginas nuevas):
     ```bash
     python "~/.claude/skills/diseno1.1/uipro/scripts/search.py" "<tipo de producto> <industria> <2-3 palabras de estilo>" --design-system -p "<Proyecto>" --motion 6
     ```
     Diales opcionales 1–10: `--variance` (minimal ↔ audaz), `--motion` (sutil ↔ coreografía), `--density` (aireado ↔ dashboard).
   - Guardar el sistema en el repo: añade `--persist --output-dir "<raíz del proyecto>"` → crea `design-system/<slug>/MASTER.md`. Si ya existe, léelo y respétalo; nunca uses `--force` sin que yo lo diga.
   - Búsquedas puntuales: `--domain <product|style|color|typography|google-fonts|ux|landing|icons|chart|gsap|react|web>` y `--stack <react|nextjs|vue|svelte|astro|html-tailwind|shadcn|threejs|...>` (el stack real del package.json, nunca uno inventado).
   - Consultas de 2–5 términos con una sola intención. Si sale vacío o fuera de tema, reintenta una vez más acotado; si sigue vacío, dilo y usa las reglas generales marcándolas como respaldo. No inventes resultados.
   - Reglas completas cuando las necesites: `uipro/references/quick-reference.md` (119 guías UX por prioridad) y `uipro/references/pro-rules.md` (pulido y checklist previo a entregar).
   - Orden de prioridad: 1 accesibilidad → 2 táctil/interacción → 3 rendimiento → 4 estilo → 5 layout/responsive → 6 tipografía y color → 7 animación → 8 formularios → 9 navegación → 10 gráficas.
2. **Motion** (`motion.md`): referencia de implementación + la lista de API verificada contra el repo oficial clonado (v13.4.6). Léela antes de escribir cualquier animación. Si dudas de una API, busca en el código fuente clonado en `~/.claude/skills-src/motion/packages/` (si no existe, en `node_modules/motion` del proyecto o en motion.dev) en vez de fiarte de memoria, y confirma la versión instalada en el `package.json` del proyecto.
3. **Fondos 3D** (`fondos-3d.md` y `plantillas/`): recetas y componente base del fondo animado.

## Regla principal: siempre entregas cambios visibles

Esta skill **nunca** termina solo con un inventario, un plan o recomendaciones. El entregable es código implementado, compilando y visible en el navegador, con capturas de **antes y después**. Si la app se ve igual que al empezar, no terminaste. No me preguntes "¿quieres que lo haga?": hazlo.

Como mínimo, cada ejecución entrega:
1. Un **sistema de diseño** salido de `--design-system` (adaptado al tema, no copiado a ciegas), guardado en `design-system/<slug>/MASTER.md`.
2. Un **fondo 3D animado** nuevo (sección "Fondo 3D"), salvo que yo diga lo contrario o ya haya uno igual de completo; en ese caso súbele el nivel.
3. Un **hero** con más impacto: jerarquía tipográfica fuerte, un elemento visual propio del tema (no una imagen genérica) y entrada animada con Motion.
4. **Microinteracciones** con Motion en botones, tarjetas y navegación (hover, press con spring, foco visible) y transiciones entre estados.
5. Los cambios que pedí en los argumentos, completos.
6. La verificación con capturas.

## Contexto (sácalo del repo, no me lo preguntes)

Qué es el proyecto y para quién (README, landing, textos), su acción principal, su stack y las versiones reales de cada librería (package.json; no asumas APIs de memoria), su paleta, tipografías y marca si ya existen (tokens, CSS global, logos). Si ya hay sistema de diseño, respétalo y complétalo. Revisa `git log`, `git status` y el sitio en vivo antes de tocar nada, porque otras IAs pueden haber roto algo. Toma las capturas de "antes" en este momento.

## Fondo 3D (obligatorio)

Elige la receta **al azar**:

```bash
node -e "console.log(1 + Math.floor(Math.random() * 6))"
```

Las recetas están en `fondos-3d.md`. Adapta colores y formas al tema (pagos → monedas o puentes; seguridad → escudos; educación → caminos o constelaciones). Si choca con el proyecto, tira otra vez, una sola vez, y dime por qué.

- Un solo componente (`AmbientBackground`) montado una vez en el layout raíz, capa `position: fixed; inset: 0; z-index: -10; pointer-events: none`, con `isolation: isolate` en `body`.
- Profundidad real: al menos dos capas con parallax distinto (puntero en escritorio, scroll en todos lados). Para el scroll usa `useScroll` + `useTransform` de Motion si el proyecto es React.
- Variante **completa** en la landing y **tranquila** en pantallas de trabajo.
- Móvil: la mitad de elementos, sin `filter: blur` animado, `devicePixelRatio` máximo 2.
- Solo `transform` y `opacity`; canvas con `requestAnimationFrame` pausado con `document.hidden`. Three.js solo si la receta lo pide y hay bundler (consulta `--stack threejs`).
- `prefers-reduced-motion`: escena estática, sin parallax. Modo claro: tokens propios y figuras atenuadas. Texto siempre a 4.5:1.

## Identidad visual

Parte de lo que devolvió `--design-system` (patrón, estilo, paleta, tipografías, efectos y anti-patrones) y ajústalo al tema. Tipografía: display con carácter para títulos, sans legible para cuerpo y mono para direcciones, montos y códigos (direcciones largas truncadas en medio). Nada de logos oficiales de terceros sin permiso. Evita el look "hecho con IA": sin cuadrículas genéricas, gradientes morados por defecto, tarjetas idénticas ni emojis como íconos (Lucide o SVG propios; consulta `--domain icons`). Cada pantalla tiene al menos un detalle que solo este proyecto tendría.

## Sistema de diseño

Tokens CSS de color, radios, sombras, espaciado en múltiplos de 4 y 8 y escala tipográfica, para modo oscuro y claro, sin colores sueltos en componentes; utilidades de texto (display, títulos, cuerpo, etiqueta, eyebrow); componentes base: botón con variantes y estado de carga, input con label visible y error debajo, tarjeta, toast, skeleton, estado vacío y estado de error con reintentar.

## Móvil primero

Revisa a 380 y 320 px: cero scroll horizontal, áreas táctiles ≥44 px con 8 de separación, cuerpo ≥16 px y nada <12, safe areas en barras fijas, `dvh` en vez de `100vh`, barras fijas fuera de elementos con transform, y navegación que oculta textos antes de romper la fila.

## Animación (Motion)

- Envuelve la app en `<MotionConfig reducedMotion="user">`. Si el bundle importa, usa `LazyMotion` + `m`.
- El contenido siempre es visible sin JavaScript; nunca `opacity: 0` desde el servidor esperando un scroll. Las entradas por scroll (`whileInView` con `viewport={{ once: true }}`) solo afectan lo que está bajo el pliegue y tras hidratar.
- Springs para interacción (`whileTap` 0.96–0.98, `whileHover` 1.02–1.03, `type: "spring"`), tweens de 150–300 ms para entradas, stagger de 30–50 ms en listas (variants con `staggerChildren` o `stagger()`).
- Hero: entrada escalonada eyebrow → título → texto → botones; un elemento con movimiento sutil continuo.
- Cambios de estado (cargando → listo, pregunta → resultado) con `AnimatePresence mode="wait"` o `popLayout`, nunca corte seco. Indicadores de tabs/nav con `layoutId`.
- Solo `transform` y `opacity`; máximo una o dos cosas llamando la atención a la vez (sin contar el fondo). Si el proyecto no es React, usa `animate()` de `motion` en vanilla o CSS, y consulta `--domain gsap` solo si el proyecto ya usa GSAP.

## Estados y honestidad

Cada pantalla con datos tiene skeleton con la forma real, estado vacío que diga qué hacer, error con causa, solución y botón de reintentar, y estado de éxito. Nada falso se presenta como real: lo simulado, testnet o demo se etiqueta; no se inventan hashes, contadores ni testimonios; las estadísticas dicen su muestra. En quizzes, la respuesta correcta no siempre en la misma posición ni siempre la más larga. Ninguna llave secreta llega al navegador y todo lo del cliente se valida en el servidor.

## Accesibilidad y SEO

Contraste 4.5:1, foco visible, skip link, encabezados sin saltos, `aria-label` en botones de solo ícono, errores con `role="alert"`, el color nunca como única señal. Metadatos completos por página (título, descripción, canonical, Open Graph e imagen para WhatsApp y X), robots, sitemap, manifest, ícono, apple-icon y `noindex` en páginas privadas.

## Orden de trabajo

1. Contexto y capturas de "antes".
2. `--design-system` (+ `--persist`) y búsquedas puntuales del stack.
3. Tokens y componentes base.
4. Fondo 3D.
5. Hero y pantallas en orden de importancia, con los cambios que pedí.
6. Estados.
7. Microinteracciones y animación fina con Motion.
8. Checklist de `uipro/references/pro-rules.md`, verificación y capturas de "después".

Si los cambios son puntuales, aplica solo lo necesario sin rehacer lo que funciona, pero el fondo 3D y la verificación van siempre salvo que diga lo contrario.

## Verificación (tú, no yo)

- Capturas antes/después a 380 px y escritorio, modo oscuro y claro. Si el navegador integrado congela animaciones, usa Chrome headless con `--virtual-time-budget` y revisa `document.getAnimations()` antes de concluir que algo no anima.
- Consola sin errores; `document.documentElement.scrollWidth > innerWidth` debe ser falso; texto ≥12 px; áreas táctiles ≥44 px.
- Build de producción limpio.
- Si el proyecto se despliega con push, haz commit, push y revisa producción consultando el estado del deploy en la plataforma, no el sitio en bucle.

## Entrega

No inventes funciones que no pedí; si ves algo que falta, dímelo en una línea al final. Deja en el README una sección FIX_NOTES (qué arreglaste y por qué), una DESIGN_NOTES (decisiones de diseño, qué salió de `--design-system`, receta de fondo y por qué la adaptaste así) y un checklist de dos minutos para probar en el celular. Commits pequeños con mensajes claros y al final dime en español qué cambió (con capturas), qué verificaste y qué queda pendiente o depende de mí.

## Feedback de testers

Cuando te pegue conversaciones o capturas de testers, confirma cada observación en el código o en el sitio, arréglala en la raíz y dime en una línea qué hiciste; si algo no se puede tal cual, aplica la alternativa más cercana y explica por qué.
