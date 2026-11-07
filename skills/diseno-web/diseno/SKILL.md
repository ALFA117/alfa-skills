---
name: diseno
description: "Prompt de diseño del usuario para frontends web: rediseño visual completo con fondo 3D animado, sistema de diseño, móvil primero, animación, estados, honestidad, accesibilidad, SEO y verificación con capturas. Úsala cuando el usuario escriba /diseno o /diseño, o pida 'mejora el diseño', 'rediseña', 'que se vea mejor', 'se ve muy básico', 'aplica el diseño', 'haz el front', 'ponle fondo 3d', o pegue feedback de testers sobre cómo se ve una app. Los argumentos son los cambios que quiere en este proyecto."
argument-hint: "cambios que quieres en este proyecto (vacío = rediseño completo)"
---

Vas a rediseñar y mejorar el frontend de este proyecto. En este proyecto quiero que hagas los siguientes cambios: $ARGUMENTS

Si no escribí cambios, haz un rediseño completo con todo lo de abajo.

## Regla principal: siempre entregas cambios visibles

Esta skill **nunca** termina solo con un inventario, un plan o recomendaciones. El entregable es código implementado, compilando y visible en el navegador, con capturas de **antes y después**. Si terminas y la app se ve igual que al empezar, no terminaste. El inventario sirve para no romper nada, no es el trabajo. No me preguntes "¿quieres que lo haga?": hazlo.

Como mínimo, cada ejecución entrega:
1. Un **fondo 3D animado** nuevo (sección "Fondo 3D", obligatorio salvo que yo diga lo contrario o el proyecto ya tenga uno igual de completo; en ese caso, súbele el nivel).
2. Un **hero** con más impacto: jerarquía tipográfica fuerte, un elemento visual propio del tema del proyecto (no una imagen genérica) y una entrada animada.
3. **Microinteracciones** en botones, tarjetas y navegación (hover, press con spring, foco visible).
4. Los cambios que pedí en los argumentos, completos.
5. La verificación de la sección "Verificación" con capturas.

## Skills y actitud

Antes de empezar carga y usa las skills /ui-ux-pro-max:ui-ux-pro-max y /motion, y aplica sus reglas en todo el trabajo: la primera para las decisiones de estilo, color, tipografía, layout, accesibilidad y experiencia de usuario, y la segunda para todas las animaciones e interacciones. Trabajo solo contigo, así que decide y avanza sin pedirme validación; pregúntame únicamente si algo es irreversible o si falta un dato que solo yo tengo, como llaves, cuentas o textos legales. Todo lo que me escribas va en español.

## Contexto (sácalo del repo, no me lo preguntes)

Qué es el proyecto y para quién (README, landing, textos), cuál es su acción principal, su stack y las versiones reales de cada librería (package.json y la documentación de la versión instalada; no asumas APIs de memoria), su paleta, tipografías y marca si ya existen (tokens, CSS global, logos). Si ya hay sistema de diseño, respétalo y complétalo; si no, propón uno a partir del tema del proyecto que no sea genérico. Revisa git log, git status y el sitio en vivo antes de tocar nada, porque otras IAs pueden haber roto algo. Toma las capturas de "antes" en este momento.

## Fondo 3D (obligatorio)

Elige la receta **al azar** para que cada proyecto se vea distinto. Corre esto y usa el número que salga:

```bash
node -e "console.log(1 + Math.floor(Math.random() * 6))"
```

Las recetas y su código base están en `fondos-3d.md`, junto a este archivo. Léelo antes de implementar. Adapta colores y formas al tema del proyecto: si es de pagos, que las figuras evoquen monedas o puentes; si es de seguridad, escudos o candados; si es de educación, caminos o constelaciones. Si la receta que salió choca con el proyecto, tira el dado otra vez, una sola vez, y dime por qué.

Reglas del fondo, sin excepción:
- Un solo componente (por ejemplo `AmbientBackground`) montado una vez en el layout raíz, en una capa `position: fixed; inset: 0; z-index: -10; pointer-events: none`, con `isolation: isolate` en `body` para que se pinte encima del fondo del body.
- Profundidad real: al menos dos capas (lejana y cercana) que se muevan distinto con el puntero en escritorio y con el scroll en todos lados (parallax por profundidad).
- Variante **completa** en la landing y variante **tranquila** (menos elementos, menos opacidad) en las pantallas de trabajo, para que no distraiga.
- Móvil: menos elementos (más o menos la mitad), sin `filter: blur` animado, `devicePixelRatio` limitado a 2.
- Rendimiento: solo `transform` y `opacity`; canvas con `requestAnimationFrame` que se pausa con `document.hidden`; nada de librerías pesadas si CSS 3D o canvas alcanzan. Three.js solo si la receta lo pide y el proyecto ya usa bundler.
- `prefers-reduced-motion`: se dibuja una sola escena estática, sin parallax.
- Modo claro: los tokens del fondo cambian con el tema y las figuras se atenúan para no competir con el texto.
- Legibilidad: viñeta o degradado sutil detrás del contenido; el texto debe seguir cumpliendo 4.5:1.

## Identidad visual

Tipografía: una display con carácter para títulos, una sans legible para el cuerpo y una mono para direcciones, montos y códigos; las direcciones largas se truncan en medio. No se usan logos oficiales de terceros sin permiso. Evita el look de "hecho con IA": nada de cuadrículas de fondo genéricas, gradientes morados por defecto, tarjetas idénticas con el mismo borde y sombra, ni emojis como íconos (usa Lucide o SVG propios). Cada pantalla tiene al menos un detalle que solo este proyecto tendría (sus unidades, su jerga, sus objetos reales), como contenido y no como adorno.

## Sistema de diseño

Tokens en CSS de color, radios, sombras, espaciado en múltiplos de 4 y 8 y escala tipográfica, pensados juntos para modo oscuro y claro y sin colores sueltos en los componentes; utilidades de texto para display, títulos, cuerpo, etiqueta y eyebrow; y componentes base de botón con variantes y estado de carga, input con label visible y error debajo, tarjeta, toast, skeleton, estado vacío y estado de error con reintentar.

## Móvil primero

Todo se revisa a 380 y a 320 píxeles: cero scroll horizontal, áreas táctiles de al menos 44 píxeles con 8 de separación, texto de cuerpo de al menos 16 píxeles y nada por debajo de 12, safe areas del notch y la barra inferior en las barras fijas, dvh en lugar de 100vh, barras fijas fuera de elementos con transform y una navegación que oculta textos antes de romper la fila.

## Animación (siguiendo /motion)

- El contenido siempre es visible sin JavaScript; nunca `opacity: 0` desde el servidor esperando un scroll. Las entradas por scroll solo ocultan lo que está debajo del pliegue y después de hidratar.
- Springs para la interacción (press 0.96–0.98, hover 1.02–1.03), transiciones de 150 a 300 ms para entradas, stagger de 30 a 50 ms en listas.
- Hero: entrada escalonada de eyebrow, título, texto y botones; un elemento visual del hero con movimiento sutil continuo (flotar, rotar lento o brillo).
- Transiciones entre estados (cargando → listo, pregunta → resultado) con crossfade o slide, nunca un corte seco.
- Solo `transform` y `opacity`; respeta prefers-reduced-motion; máximo una o dos cosas llamando la atención a la vez, sin contar el fondo.

## Estados y honestidad

Cada pantalla con datos tiene estado de carga con un skeleton de la forma real, estado vacío que diga qué hacer, estado de error con la causa, cómo arreglarlo y un botón para reintentar, y estado de éxito. Nada falso se presenta como real: lo simulado, testnet o demo se etiqueta en la interfaz, no se inventan hashes de transacción, contadores ni testimonios, y las estadísticas muestran el tamaño de la muestra y qué significan exactamente. Si hay preguntas o quizzes, la respuesta correcta no puede estar siempre en la misma posición ni ser siempre la más larga, y los distractores deben ser creíbles y de longitud pareja. Ninguna llave secreta llega al navegador, solo las publicables, y todo lo que manda el cliente se valida en el servidor.

## Accesibilidad y SEO

Contraste de 4.5 a 1 en texto, foco visible, skip link, jerarquía de encabezados sin saltos, aria-label en botones de solo ícono, errores con role alert y el color nunca como única señal. Metadatos completos por página con título, descripción, canonical, Open Graph e imagen para WhatsApp y X, además de robots, sitemap, manifest, ícono y apple-icon, y noindex en las páginas privadas.

## Orden de trabajo

1. Contexto y capturas de "antes".
2. Tokens y componentes base (si faltan).
3. Fondo 3D.
4. Hero y pantallas en orden de importancia, con los cambios que pedí.
5. Estados.
6. Microinteracciones y animación fina.
7. Verificación y capturas de "después".

Si los cambios que pedí son puntuales, aplica solo lo necesario sin rehacer lo que ya funciona, pero el fondo 3D y la verificación van siempre salvo que diga lo contrario.

## Verificación (tú, no yo)

- Capturas de antes y después a 380 px y en escritorio, en modo oscuro y claro. Si el navegador integrado congela animaciones en las capturas, usa Chrome headless con `--virtual-time-budget` y revisa `document.getAnimations()` antes de concluir que algo no anima.
- Consola sin errores, auditoría de overflow (`document.documentElement.scrollWidth > innerWidth` debe ser falso), texto mínimo de 12 px y áreas táctiles de 44 px.
- Build de producción limpio.
- Si el proyecto se despliega con push, haz commit, push y revisa en producción (sin martillar el sitio: consulta el estado del deploy en la plataforma, no el sitio en bucle).

## Entrega

No inventes funciones que no pedí; si ves algo que falta, dímelo en una línea al final. Deja en el README una sección FIX_NOTES con qué arreglaste y por qué, una sección DESIGN_NOTES con las decisiones de diseño (incluida la receta de fondo que salió y por qué la adaptaste así) y un checklist de dos minutos para probar en el celular. Haz commits pequeños con mensajes claros y al final dime en español qué cambió (con las capturas), qué verificaste y qué queda pendiente o depende de mí.

## Feedback de testers

Cuando te pegue conversaciones o capturas de testers, confirma cada observación en el código o en el sitio, arréglala en la raíz y no solo el síntoma, y dime en una línea qué hiciste; si algo no se puede hacer tal cual, por ejemplo usar una mascota oficial que no existe, aplica la alternativa más cercana y explica por qué.
