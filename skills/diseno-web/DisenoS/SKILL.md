---
name: DisenoS
description: "Rediseño de interfaz en estilo BENTO + BRUTALISMO: retícula bento, bordes gruesos, sombras duras sin desenfoque, colores de alto contraste, íconos e ilustraciones solo en SVG, minimalista y con un flujo de usuario más corto y simple. Úsala cuando el usuario escriba /DisenoS, /disenos o /diseños, o pida 'estilo bento', 'brutalista', 'neo-brutalismo', 'bento con brutalismo', 'no me gusta la interfaz, rediséñala', 'colores contrastantes', 'flujo más sencillo', 'hazlo minimalista con SVG'. Los argumentos son los cambios que quiere en este proyecto."
argument-hint: "cambios que quieres en este proyecto (vacío = rediseño completo bento brutalista)"
---

Vas a rediseñar la interfaz de usuario de este proyecto porque la actual no me gusta. El estilo es **bento con brutalismo**, con **colores contrastantes**, **íconos e ilustraciones en SVG** y **minimalista**, y el objetivo de fondo es que el **flujo sea más sencillo**. En este proyecto quiero además: $ARGUMENTS

Si no escribí cambios, haz el rediseño completo con todo lo de abajo.

## Regla principal: siempre entregas cambios visibles

Esta skill **nunca** termina solo con un inventario, un plan o recomendaciones. El entregable es código implementado, compilando y visible en el navegador, con capturas de **antes y después**. Si terminas y la app se ve igual que al empezar, no terminaste. No me preguntes "¿quieres que lo haga?": hazlo.

Como mínimo, cada ejecución entrega:
1. La **dirección visual bento + brutalista** aplicada a todas las pantallas (sección "Estilo").
2. Un **flujo simplificado**: menos pasos, menos clics y una sola acción principal por pantalla (sección "Flujo").
3. **Íconos e ilustraciones en SVG** propios o de Lucide, sin imágenes rasterizadas decorativas ni emojis como íconos.
4. **Microinteracciones brutalistas** en botones, tarjetas y navegación (sección "Interacción").
5. Los cambios que pedí en los argumentos, completos.
6. La verificación con capturas.

## Skills y actitud

Antes de empezar carga y usa /ui-ux-pro-max:ui-ux-pro-max (pide el estilo con `--domain style "neubrutalism bento"` y una paleta de alto contraste) y /motion para las interacciones si el proyecto es React. Trabajo solo contigo: decide y avanza sin pedirme validación; pregúntame únicamente si algo es irreversible o si falta un dato que solo yo tengo (llaves, cuentas, textos legales). Todo lo que me escribas va en español.

## Contexto (sácalo del repo, no me lo preguntes)

Qué es el proyecto y para quién, cuál es su acción principal, su stack y las versiones reales de cada librería (package.json; no asumas APIs de memoria), y la marca si existe (logo, nombre, color principal). El color de marca se conserva como uno de los acentos; todo lo demás se rehace. Revisa git log, git status y el sitio en vivo antes de tocar nada, porque otras IAs pueden haber roto algo. Toma las capturas de "antes" en este momento.

## Estilo: bento + brutalismo minimalista

**Retícula bento**
- El contenido se organiza en una cuadrícula de bloques de tamaños distintos (1×1, 2×1, 1×2, 2×2) con `display: grid`, `grid-template-columns` de 4 a 6 columnas en escritorio, 2 en tableta y 1 en móvil, y separación fija (16 o 24 px).
- Cada bloque cuenta **una sola cosa**: un dato, una acción, una lista corta o una ilustración. Nunca dos ideas en el mismo bloque.
- El bloque más grande es siempre la acción principal o el dato más importante. La jerarquía la da el tamaño del bloque, no la decoración.
- Nada de tarjetas idénticas en fila: varía tamaño, color de fondo y contenido.

**Brutalismo**
- Bordes sólidos y gruesos (2 a 4 px) en negro o en el color de texto, en tarjetas, botones, inputs y separadores.
- Sombras **duras**, desplazadas y sin desenfoque: `box-shadow: 4px 4px 0 0 var(--ink)` (6–8 px en bloques grandes). Prohibido `blur` en sombras y glassmorphism.
- Radios pequeños o cero (0 a 8 px), iguales en todo el sistema.
- Tipografía grande y pesada en títulos (800–900, tamaños de 48 a 96 px en escritorio), con mayúsculas o tracking ajustado si queda bien; cuerpo sans muy legible; mono para números, montos, códigos e ids.
- Fondos planos. Sin gradientes, sin fondos 3D ni animados y sin texturas de ruido. Como mucho, un patrón SVG plano y muy sutil (puntos o líneas) en un solo bloque.

**Colores contrastantes**
- Base: fondo claro casi blanco o crema (por ejemplo `#FFFDF5`) y texto/bordes casi negros (`#111`). Si el proyecto necesita modo oscuro, se invierte: fondo `#111`, bordes y texto claros.
- 3 o 4 acentos **saturados y planos** que contrasten entre sí (ejemplos: amarillo `#FFD23F`, rosa `#FF5DA2`, azul `#3A86FF`, verde `#06D6A0`, naranja `#FF7A00`), elegidos a partir del color de marca.
- Cada color tiene **un significado fijo** en toda la app: por ejemplo, amarillo = acción principal, verde = éxito, rojo = error o peligro, azul = información o navegación. Nunca se usa un acento solo para adornar.
- Texto sobre cualquier acento con contraste mínimo de 4.5:1 (normalmente negro sobre acento). Verifícalo con una herramienta o cálculo, no a ojo.
- El color nunca es la única señal: estados y errores llevan también ícono SVG y texto.

**SVG y minimalismo**
- Todos los íconos en SVG inline o con Lucide (`lucide-react` o el SVG copiado), de trazo grueso (2–2.5) a juego con los bordes. Cero emojis como íconos.
- Las ilustraciones son SVG propios simples: formas geométricas planas con el mismo borde grueso y los colores de la paleta, relacionadas con el tema del proyecto (pagos → monedas o tarjetas; seguridad → candados; educación → libros o caminos).
- `aria-hidden="true"` en SVG decorativos y `role="img"` con `<title>` en los que comunican algo.
- Minimalista: quita todo lo que no ayude a completar la tarea. Menos texto, menos secciones, menos opciones visibles. Si dudas si algo sobra, sobra.

**Evita**
- El look genérico "hecho con IA": gradientes morados, glassmorphism, sombras difusas, tarjetas idénticas, emojis.
- Logos oficiales de terceros sin permiso.

## Flujo: más sencillo

Antes de diseñar, escribe en una lista corta el recorrido actual de la acción principal (cada pantalla, clic y campo) y luego el recorrido nuevo. El nuevo debe tener **menos pasos** o, si no se pueden quitar, explica por qué en una línea.

- Una sola acción principal por pantalla, en el bloque más grande y en el color de "acción principal". Las secundarias van como botón de borde sin relleno o como enlace.
- Formularios: solo los campos indispensables, en una columna, con label visible, valores por defecto inteligentes y validación en línea. Divide en pasos solo si son más de 5 o 6 campos, con indicador de progreso.
- Navegación con 5 elementos o menos; en móvil, barra inferior o menú simple.
- Cada pantalla dice en una frase qué es y qué hacer a continuación.
- Nada se esconde detrás de hover: en táctil todo debe verse y funcionar.

## Sistema de diseño

Tokens en CSS: colores con significado (`--ink`, `--paper`, `--accent-action`, `--accent-ok`, `--accent-error`, `--accent-info`…), grosor de borde, sombra dura en 2 o 3 tamaños, radio único, espaciado en múltiplos de 4 y 8 y escala tipográfica. Ningún color suelto en los componentes. Componentes base: botón (principal, secundario, peligro, cargando), input con label y error debajo, bloque bento (tamaños y colores), badge, toast, skeleton con la forma real, estado vacío y estado de error con reintentar.

## Móvil primero

Todo se revisa a 380 y 320 px: la bento pasa a una columna en el orden de importancia, cero scroll horizontal, áreas táctiles de al menos 44 px con 8 de separación, cuerpo de al menos 16 px y nada por debajo de 12, safe areas en barras fijas, dvh en lugar de 100vh. Las sombras duras se reducen en móvil (3–4 px) para que no se coman el espacio.

## Interacción

- Botones y bloques clicables: en hover se desplazan `translate(-2px, -2px)` y la sombra crece; al presionar, `translate(4px, 4px)` con sombra en 0 (efecto de "hundirse"). Transición de 100 a 150 ms.
- Foco visible con contorno grueso del color de texto y separación (`outline-offset: 3px`).
- Entradas de bloques con un stagger corto (30–50 ms) solo tras hidratar y solo en lo que está bajo el pliegue; el contenido siempre es visible sin JavaScript.
- Cambios de estado (cargando → listo, pregunta → resultado) con transición corta, nunca un corte seco.
- Solo `transform` y `opacity`; respeta `prefers-reduced-motion` (sin desplazamientos, solo cambio de color).

## Estados y honestidad

Cada pantalla con datos tiene skeleton con la forma real, estado vacío que diga qué hacer, error con causa, solución y botón de reintentar, y estado de éxito. Nada falso se presenta como real: lo simulado o de demo se etiqueta, no se inventan hashes, contadores ni testimonios, y las estadísticas dicen su muestra. En quizzes, la respuesta correcta no siempre en la misma posición ni siempre la más larga. Ninguna llave secreta llega al navegador.

## Accesibilidad y SEO

Contraste 4.5:1 (más estricto aún con colores saturados), foco visible, skip link, encabezados sin saltos, aria-label en botones de solo ícono, errores con role alert y el color nunca como única señal. Metadatos completos (título, descripción, canonical, Open Graph con imagen en el mismo estilo), robots, sitemap, manifest, ícono SVG y apple-icon, y noindex en páginas privadas.

## Orden de trabajo

1. Contexto, recorrido actual y capturas de "antes".
2. Recorrido nuevo simplificado (lista corta).
3. Tokens y componentes base.
4. Retícula bento de cada pantalla en orden de importancia, con los cambios que pedí.
5. SVG: íconos e ilustraciones.
6. Estados.
7. Interacción.
8. Verificación y capturas de "después".

Si los cambios que pedí son puntuales, aplica solo lo necesario sin rehacer lo que funciona, pero el estilo bento brutalista y la verificación van siempre.

## Verificación (tú, no yo)

- Capturas de antes y después a 380 px y en escritorio (y en oscuro si el proyecto lo tiene).
- Consola sin errores; `document.documentElement.scrollWidth > innerWidth` debe ser falso; texto mínimo de 12 px; áreas táctiles de 44 px; contraste de cada combinación de acento comprobado.
- Recorre el flujo principal de punta a punta y cuenta los pasos: deben ser menos que antes o igual con la explicación.
- Build de producción limpio.
- Si el proyecto se despliega con push, haz commit, push y revisa en producción consultando el estado del deploy en la plataforma, no el sitio en bucle.

## Entrega

No inventes funciones que no pedí; si ves algo que falta, dímelo en una línea al final. Deja en el README una sección DESIGN_NOTES (paleta con el significado de cada color, retícula bento, recorrido antes y después) y FIX_NOTES (qué arreglaste y por qué), y un checklist de dos minutos para probar en el celular. Commits pequeños con mensajes claros y al final dime en español qué cambió (con capturas), cuántos pasos tiene ahora el flujo, qué verificaste y qué queda pendiente o depende de mí.

## Feedback de testers

Cuando te pegue conversaciones o capturas de testers, confirma cada observación en el código o en el sitio, arréglala en la raíz y dime en una línea qué hiciste; si algo no se puede hacer tal cual, aplica la alternativa más cercana y explica por qué.
