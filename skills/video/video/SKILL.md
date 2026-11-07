---
name: video
description: Hace un video animado completo (MP4) con HyperFrames a partir de un tema, guion o brief, de punta a punta y sin preguntar. Úsala cuando el usuario escriba /video seguido de lo que quiere que diga o trate el video, o pida 'hazme un video de...', 'quiero un video sobre...', 'genera un video que hable de...', 'un reel de...', 'un mono/mascota hablando'. Los argumentos son el contexto/tema/guion y opcionalmente formato, duración, voz, colores, mascota o 'sin voz'.
model: claude-opus-5-5
argument-hint: "<de qué quieres que hable el video o el brief completo> [horizontal|cuadrado] [N segundos] [voz X] [sin voz] [mascota] [colores/letra]"
---

# /video: video animado con HyperFrames + Opus 5.5

El usuario escribe `/video <contexto>` y espera un MP4 terminado. Esta skill corre
siempre con Opus 5.5 (`claude-opus-5-5`, fijado en el frontmatter). Se trabaja en
**modo autónomo**: sin entrevista, sin ronda de propuestas y sin pedir confirmación
del guion. Decidir, construir, revisarse uno mismo y entregar. Todo lo que se le
escriba al usuario va en español.

Contexto del usuario: **$ARGUMENTS**

Si `$ARGUMENTS` viene vacío, pregunta solo una cosa: "¿De qué quieres que hable el video?" y sigue.

## 1. Defaults (aplican salvo que el contexto diga otra cosa)

| Campo | Default | Cómo lo cambia el usuario |
|---|---|---|
| Formato | Vertical 1080x1920 (`--resolution portrait`, Reels/TikTok) | "horizontal"/"16:9" → `landscape`; "cuadrado" → `square` |
| Duración | 30–45 s; si el brief da segundos, respetarlos (±2 s) | "N segundos" |
| Idioma | Español (México) | otro idioma explícito; si pide "narración en inglés con subtítulos en español", así |
| Voz en off | **`es-MX-DaliaNeural`** (Microsoft, natural), velocidad `+22%` | "voz X" (ver tabla de voces); "sin voz" |
| Estilo | Fondo oscuro, letra gruesa, mucho movimiento, ningún segundo quieto | colores, letra o estilo que pida |
| Subtítulos | Siempre: frases sincronizadas con la voz, abajo, con placa oscura | — |
| Audio final | Normalizado a **-14 LUFS** (estándar de Instagram/TikTok) | — |

### Voces disponibles (ya instaladas)

| Voz | Motor | Notas |
|---|---|---|
| `es-MX-DaliaNeural` | edge-tts (Microsoft, en línea) | **Default.** Mujer, México. Elegida por el usuario. |
| `es-MX-JorgeNeural` | edge-tts | Hombre, México |
| `es-US-AlonsoNeural` / `es-US-PalomaNeural` | edge-tts | Latino neutro, hombre / mujer |
| `es-CO-GonzaloNeural` / `es-CO-SalomeNeural` | edge-tts | Colombia |
| `es-AR-TomasNeural`, `es-ES-AlvaroNeural`, `es-ES-XimenaNeural` | edge-tts | Argentina / España |
| `en-US-AndrewNeural`, `en-US-AvaNeural` y demás `en-*` | edge-tts | Inglés natural |
| `em_santa` | Kokoro (local) | Hombre, voz de personaje. **Úsala para mascotas** (ej. el mono de Mongli). |
| `ef_dora`, `em_alex` | Kokoro (local) | Español, suenan robóticas: solo para borradores sin internet |
| `am_michael`, `af_heart` | Kokoro (local) | Inglés |

Lista completa de Microsoft: `python -m edge_tts --list-voices`. Si el usuario quiere
comparar, genera la misma frase con varias voces en `videos/muestras-voces/` y mándalas.
La voz de edge-tts manda el texto a Microsoft: no usarla para contenido confidencial
(en ese caso, Kokoro).

## 2. Carpeta del proyecto

Todos los videos viven en `~/videos/` (o la carpeta que el usuario prefiera).
Nombre: `AAAA-MM-DD-<slug-corto-del-tema>` (si existe, agregar `-2`, `-es`, `-mono`…).
Scripts de apoyo de esta skill: `~/.claude/skills/video/scripts/`.

## 3. Flujo

1. **Plan.** Antes de construir, escribe en `BRIEF.md`: duración, formato, guion por
   escena con segundos, texto en pantalla exacto por escena, marca (fuentes, hex,
   descripción del logo), mascota si la hay y música. Si el usuario pegó un brief largo,
   úsalo tal cual y no re-preguntes lo que ya dice ni las "preguntas pendientes" que trae
   el propio brief: decide con defaults y menciónalo en la entrega.
2. **Guion por escena.** Un archivo por escena en `<proyecto>/voz-por-escena/s1.txt, s2.txt…`
   con solo el texto hablado. Cuenta ~2.5 palabras/s en español para cuadrar la duración.
   - Nombres propios: prueba cómo los pronuncia la voz (genera la frase y transcríbela).
     Ejemplo real: "Mongli DAO" en mayúsculas sonaba "Mon Ideo"; escrito **"Mongli Dao"** se
     pronuncia bien. Los subtítulos y el texto en pantalla sí van con la grafía correcta.
3. **Voz.** Un solo comando genera, recorta pausas y mezcla todas las escenas:
   ```bash
   python -I ~/.claude/skills/video/scripts/voz.py <proyecto>/voz-por-escena es-MX-DaliaNeural <proyecto>/assets/voz.wav --rate +22% --total <duración>
   ```
   Devuelve JSON con el inicio de cada escena: esos son los cortes de escena del video.
   Si se pasa de la duración, sube `--rate` (hasta +30%) o recorta el guion; nunca dejes
   que la voz pise el corte de la siguiente escena. Kokoro: `--rate 1.1` en vez de %.
4. **Proyecto y transcripción.**
   ```bash
   hyperframes init <carpeta> --resolution portrait --non-interactive   # HYPERFRAMES_SKIP_SKILLS=1 para que no re-instale skills
   hyperframes transcribe assets/voz.wav -l es --json                   # deja transcript.json (si cae en assets/, muévelo a la raíz)
   ```
   Los tiempos por palabra de `transcript.json` mandan: cada texto en pantalla y cada
   subtítulo entran en la palabra que les corresponde.
5. **Música.** Si el usuario no da pista, sintetiza una cama electrónica cinematográfica
   con golpes en cada corte de escena y clímax al final:
   ```bash
   python -I ~/.claude/skills/video/scripts/musica.py <proyecto>/assets/musica.wav <duración> "0,<inicio esc2>,<esc3>,..."
   ```
   Volumen en la composición 0.3–0.42 bajo la voz. Si el usuario da una pista: recórtala para
   que el primer golpe caiga en el momento clave, bájala bajo la voz y súbela en el cierre.
   Para publicar, recomiéndale cambiarla por una pista con licencia.
6. **Autoría con HyperFrames.** Carga `/hyperframes` antes de escribir HTML: trae el
   contrato técnico y la tabla de referencias. Para animación, lee su `references/motion.md`;
   para el formato vertical, `references/types/vertical.md`. Constrúyelo sin preguntar.
   (Desde el 30-oct-2026 ya no existen `/hyperframes-core` ni `/hyperframes-animation`;
   su contenido vive dentro de `/hyperframes`.) Reglas que ya nos mordieron:
   - No animar `letterSpacing` (lint error): usa `scale`/`opacity`.
   - Un elemento con varios `fromTo` → `immediateRender: false` en todos menos el primero.
   - Texto con degradado (`background-clip: text`) en un padre cuyos hijos se animan sale
     borroso: pon la clase de degradado en cada letra/span.
   - Fuentes locales con `@font-face` (`assets/fonts/*.woff2`, de `npm pack @fontsource/<fuente>`).
   - Subtítulos y titulares como `div.clip` estáticos en el HTML (no generados con JS).
   - Fondo animado en `<canvas>` dibujado desde un tween proxy `{t:0}→{t:DUR}` con
     `onUpdate`, con PRNG con semilla (mulberry32): determinista y seekable.
   - **Retícula fija en vertical 1080x1920 (obligatoria; el usuario rechazó un video "amontonado, sin orden"):**
     0–240 vacío (interfaz de IG) · 250–560 zona de título: etiqueta de capítulo fija (mono) + UN solo
     titular, que cambia en su lugar, nunca se apila · 600–1360 escenario: personaje/objeto principal,
     siempre del mismo tamaño y en ranuras fijas (centro, o tercio izquierdo con su objeto a la derecha)
     · 1480–1640 subtítulos · 1640–1920 vacío (pie de foto de IG). Ningún objeto de escena entra en la
     zona de título ni en la de subtítulos.
   - Una sola cosa protagonista a la vez: nada de burbujas, letreros o íconos extra encima del
     personaje; los grupos (multitudes, ayudantes) van a los lados, nunca detrás del cuerpo del
     personaje. Sin logo fijo arriba: la marca va en su escena y en el cierre.
   - Revisa las contact sheets buscando específicamente encimados: si dos cosas se tocan, quita una.
7. **Revisión propia (obligatoria antes de mostrar).**
   `npx hyperframes check` con 0 errores, luego `npx hyperframes snapshot --at <momentos clave>`
   y **lee las contact sheets**: corrige textos que se salen o se enciman, escenas vacías
   o quietas, y palabras que no caben. Repite hasta que esté limpio.
8. **Render.**
   ```bash
   npx hyperframes render -f 30 -q high -o video-raw.mp4
   ffmpeg -y -i video-raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 video.mp4
   ```
   60 s tardan de 3 a 11 min: córrelo en segundo plano y avanza con otra cosa. Para borradores,
   `-q draft` o sin `-q`.
9. **Entrega.** `SendUserFile` con `video.mp4` (display `render`) y un resumen corto:
   duración, formato, voz, qué decidiste por tu cuenta y qué falta del cliente (logo
   oficial, música con licencia, enlaces). Recuérdale que puede pedir cambios en palabras
   normales y que `npx hyperframes preview` en la carpeta abre el editor.

## 4. Variantes frecuentes

- **Versión en otro idioma del mismo video:** copia el proyecto (`<slug>-es`), traduce el
  texto en pantalla, genera la nueva voz y **retemporiza** todo. Si el texto es el mismo con
  otra voz, alinea los dos `transcript.json` palabra por palabra y aplica el mapa de tiempos a
  cada posición del timeline (así se hizo con Dora → Dalia; los 171 anclajes coincidieron).
- **Solo animaciones, sin mascota (lo que el usuario terminó eligiendo para Mongli DAO):**
  `scripts/anim_template.html`, generada con `scripts/make_anim.py` desde `mono_template.html`.
  Misma retícula, capítulos, titulares, cortinas, subtítulos y mapa de tiempos; el escenario lo
  ocupa una pieza por escena (globo + órbitas, torre de bloques, emblema hexagonal "M", foco →
  dos personas conectadas → red, túnel warp con viajero que aterriza en "TÚ", emblema final).
  Las personas son íconos abstractos (símbolo `#mini`). Ejemplo: `videos/2026-10-09-mongli-dao-anim`
  (`build.py` con `anim_template.html`). Ojo: todo lo que dibuja un canvas debe calcular su estado
  como función pura del tiempo (como `glAt(t)`); si lo tweeneas con GSAP, el proxy `onUpdate`
  de t=0 lo pinta un cuadro tarde y las capturas/seek salen mal.
- **Mascota con ilustración real (cuando existe arte del personaje):** el usuario rechazó
  dos versiones del mono dibujadas a mano en SVG por verse "básicas"; lo que sí funcionó fue animar
  la ilustración original como marioneta recortada:
  1. `hyperframes remove-background arte.jpg -o recorte.png` (quita el fondo, local).
  2. Recorta el busto (sin manos ni objetos), difumina el borde inferior y los bordes con artefactos
     (alfa en gradiente) y mide con una cuadrícula la línea de la boca, el polígono de la mandíbula,
     el visor/ojos y la parte superior de la cabeza.
  3. Plantilla: `scripts/mono_template_ilustrado.html` (se genera con `scripts/make_ilustrado.py`
     desde `mono_template.html`). Usa la misma imagen dos veces: base con la mandíbula recortada
     (`clip-path: path(evenodd, ...)`) y mandíbula sola (`clip-path: polygon(...)`) que baja con la
     envolvente de la voz; detrás, el interior oscuro de la boca y la lengua. Ojos LED dibujados sobre
     el visor (normal, feliz, guiño, estrellas, corazones), respiración, cabeceo y "pops" en los
     momentos clave en lugar de gestos con los brazos. La multitud y los amigos son copias chicas de
     la misma ilustración con halo de color (y algunas en espejo), así todo combina.
  4. En `build.py`: `MONO_TEMPLATE=mono_template_ilustrado.html` (es el valor por defecto en
     `videos/2026-10-08-mongli-mono-dalia`). Assets en `assets/mono/busto.png`.
- **Mascota que habla en vector (solo si NO hay arte del personaje), ej. el mono de Mongli v1–v5:** personaje en SVG con grupos `head`, `body`,
  `mouthOpen`, `smile` y el visor/ojos, y lip-sync por envolvente de audio:
  ```bash
  python -I ~/.claude/skills/video/scripts/boca.py assets/voz.wav assets/mouth.json <duración>
  ```
  En el `onUpdate`: scaleY de la boca = apertura, sonrisa = 1 − 4·apertura, cabeceo con
  seno + un poco de movimiento al hablar, parpadeo determinista cada ~3.7 s y un salto en
  cada corte de escena. Los ojos actúan (parpadean, miran a un lado, guiñan) y el personaje
  se aplasta y se estira al aterrizar.
  **Plantilla v2 (la mejorada tras "se ve muy feo y básico"): `scripts/mono_template.html`.** Mono de
  cuerpo completo (sudadera, cola, tenis, antena, visor con ojos LED: normal, feliz, guiño,
  estrellas, corazones), brazos con poses (`pose()`, `wave()`), props que se encienden por
  escena (casco, foco, jetpack con flamas) y 6 escenarios: espacio con planeta-red, taller
  con cubos que caen, ciudad neón con letrero, ideas + amigo + multitud + fuegos
  artificiales, viaje por túnel warp hasta "TÚ", final con confeti, logo y CTA.
  Se ensambla con un `build.py` en el proyecto (ver `videos/2026-10-08-mongli-mono/build.py`)
  que mete boca, subtítulos y titulares. Para otro guion: cambia en la plantilla los tiempos
  de `SC`, las poses, las expresiones y los props según el `transcript.json`.
  **Cambiar de voz con el mismo guion (ej. em_santa → Dalia):** copia el proyecto, guarda el
  transcript viejo como `transcript-santa.json`, genera la voz nueva con `voz.py` en
  `assets/voz-mono.wav`, transcribe y corre `build.py`. `scripts/timemap.py` alinea las dos
  transcripciones palabra por palabra y la plantilla recoloca TODA la coreografía (`__TIMEMAP__`
  envuelve `tl.to/fromTo/set`); `build.py` mapea los `data-start` de escenas, titulares,
  `data-at` y subtítulos. Regenera la música con los nuevos cortes de escena (el `build.py` los
  imprime en los `data-start` de `#s1..#s6`). Ejemplo: `videos/2026-10-08-mongli-mono-dalia`.
  Reglas aprendidas: los brazos levantados no pasan de ±140° (si no, tapan el visor); los
  props que pasan volando van arriba (y≈560) para no quedar detrás del personaje; las
  burbujas y los textos no van encima de la cabeza. `scripts/ejemplo_mascota.py` es la
  v1 básica: no usarla.
  La ilustración original del mono de Mongli está en
  la carpeta de assets del proyecto (referencia de estilo: visor azul, sudadera).
- **Anuncio de producto/app:** burbujas de chat que entran con puntos de "escribiendo",
  marcos de teléfono realistas, notificaciones de pantalla de bloqueo, la cámara hace zoom
  a través de la UI y el cierre gira hacia el logo + lema.
- **Serie educativa vertical (ej. "Web3 desde cero" de @tu_usuario):** usar
  `scripts/serie_v2.py` (NO `alfa_brand.py`, que es la v1 rechazada). Cada video lleva su
  propio tema en `THEMES` (paleta + tipografía display/cuerpo/mono + glifo + estilo de acento
  "mark" o "bar"); `install_fonts()` copia las fuentes desde las carpetas de skills. El módulo
  aporta: titulares letra por letra (máscara + rotationX + blur), capítulo con barra
  segmentada, palabra fantasma en canvas por escena, esquinas de encuadre, barrido de luz en
  cada corte, ráfagas (`bursts=[(t, x, y)]`), grano y viñeta, y un cierre tipográfico con el
  @usuario + índice de la serie (capítulo actual resaltado). `retheme()` recolorea las escenas
  escritas con la paleta v1 al tema. Reglas aprendidas: nada de logotipo personal repetido en
  todos los videos; `stage` (escala del escenario) en 1.0 si hay filas anchas que llegan a
  los bordes; el texto en contorno debe ir en canvas (el linter marca como error el texto
  transparente o tapado). Ejemplos: `videos/2026-10-12-web3-alfa` (parte 1) a
  `videos/2026-10-13-daos-alfa` (parte 5); `build_v1.py` guarda la versión anterior.
  Videos únicos (sin «parte X»): `page(..., part=None, takeaway="Frase *clave.", recolor=False)`
  y colores del tema escritos directo en el build; NO usar ids/clases reservados (lista en el
  docstring de serie_v2.py). Si una fuente display solo tiene mayúsculas (Bangers), poner
  `efd=` en el tema para la firma @usuario. Siglas o anglicismos en la voz: escribirlos
  fonéticos solo en `voz-por-escena` («jálving», «érdrop», «jódel»).
- **Diccionario Web3 (glosario):** `scripts/diccionario.py` genera un video de 4 términos
  (intro con índice, 4 entradas de diccionario con pronunciación/definición/ejemplo/ícono,
  repaso) a partir de un spec; temas d01–d10, 10 fondos y 10 transiciones. Contenido en
  `videos/diccionario-web3/specs.py`; cada proyecto `2026-10-14-dicc-XX` solo llama `build()`.
  Voces con `--rate=-2% --gap 1.9` (ojo: `--rate=-2%` con `=`, si no argparse falla).

## 5. Cómo pedir (y escribir) un buen video: lecciones de la guía "Motion Graphics with Opus 5.5"

Fuente: https://pdhouse.notion.site/motion-guide (Jason Lee). Aplícalas al planear:

- **Copiar una referencia.** Si el usuario da un video de referencia, copia su estructura,
  ritmo y estilo ("copia los primeros 30 s de este video").
- **Escenas con segundos y texto exacto.** Cada escena lleva su duración ("Cold open (8s)")
  y el texto en pantalla literal. Las escenas con mucho texto van 10% más lentas para que
  se lean.
- **Marca concreta:** fuente de titulares y de UI, hex de cada color con su uso (tinta,
  acento, burbujas), y el logo descrito en palabras ("círculo lavanda con avión de papel
  navy junto al wordmark").
- **Números de la historia consistentes:** los mismos montos, nombres y folios en todas
  las escenas.
- **Estilo con verbos de movimiento:** titulares que entran palabra por palabra con blur,
  la cámara se acerca y se aleja suave, las burbujas aparecen con puntos de escritura, y el
  cierre gira hacia el logo y se sostiene mientras la música se desvanece.
- **Sonido:** sintetiza efectos sutiles de UI (swoosh al enviar, pop, clicks en taps, ding
  en pagos, tinks de monedas). La música entra suave al inicio, baja bajo la voz y se
  desvanece en el cierre. Mezcla final a -14 LUFS.
- **Borrador primero:** renderiza un borrador a media resolución y revísalo tú con contact
  sheets antes de mostrarlo.
- **Sin rayas largas (em dash "—") en el texto en pantalla.**
- **Cinemático con personas reales (avanzado, solo si hay conector de Higgsfield):**
  1) plan + guion + lista de tomas sin generar nada; 2) hoja de personaje (cuerpo completo
  y primer plano en fondo blanco) para fijar cara y ropa; 3) set vacío aprobado; 4) "first
  look" que une personaje y set; 5) las demás tomas a partir de ese first look; 6) animar
  cada toma con su frame inicial y la hoja de personaje como referencia, en borrador 480p y
  luego finalizar a 1080p; 7) editar con la voz cortada en las pausas, los textos encima y
  la música recortada. Modelos y costo aproximado: Soul 2.0 (retratos, ~0.12 créditos),
  Soul Cinema (sets, ~0.12), Seedream 5.0 Pro (hoja de personaje, first look y ángulos,
  2.5 por imagen), Seedance 2.5 (video, 3/s borrador, 10/s final). Hoy **no** está conectado
  Higgsfield: si el usuario lo pide, dile que lo conecte en Settings → Connectors, y mientras
  tanto haz la versión en motion graphics.
- **Motion OS** (herramienta gratuita del autor de la guía, en GitHub) sirve de reproductor/
  editor por escenas. Aquí el equivalente es `npx hyperframes preview` (Studio).

## 6. Cambios después de la entrega

Si el usuario pide ajustes sobre un video ya hecho, trabaja en la misma carpeta, revisa con
snapshots y vuelve a renderizar. Para otra voz: regenera con `voz.py`, transcribe y
retemporiza (sección 4); regenera la música con los nuevos cortes de escena.

## 7. Notas del equipo (Windows)

- Instalado: `hyperframes` global (npm), FFmpeg 9 (winget), Chrome del sistema para el
  render, Kokoro TTS (`kokoro-onnx soundfile`), edge-tts (pip), Parakeet para transcribir.
  Si algo falla: `hyperframes doctor`.
- `hyperframes tts` falla con textos largos: genera por escena (ya lo hace `voz.py`).
- **edge-tts da 403 (`WSServerHandshakeError`) desde el 12-oct-2026:** Microsoft dejó de aceptar
  `speech.platform.bing.com`. Está parcheado en local (`site-packages/edge_tts/constants.py`, respaldo
  `constants.py.orig`) con el arreglo del PR #491 de edge-tts: `WSS_URL` apunta a
  `wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1?Ocp-Apim-Subscription-Key=<token>`.
  Si `pip install -U edge-tts` reinstala una versión sin el arreglo, vuelve a aplicarlo.
- Para texto en pantalla en otro idioma que la voz (ej. audio ES + texto EN): los titulares y subtítulos
  se escriben traducidos con los tiempos de las frases de la voz original. Ejemplo:
  `videos/2026-10-12-web1-a-web3` (video educativo con escenas propias en `build.py`).
- `python -I` ignora `PYTHONIOENCODING`: para imprimir acentos usa `sys.stdout.reconfigure(encoding="utf-8")`.
- Videos hechos (como referencia de código): `videos/2026-10-08-mongli-dao` (inglés),
  `-mongli-dao-es` (Dalia), `-mongli-mono` (mascota con lip-sync).

## 8. Sistema v3 de producción (`scripts/produccion.py`, serie «Web3 en 60 segundos»)

Para videos con aspecto «más producido» (pedido del 15-oct-2026): gancho de 3 palabras con temblor y destello,
título de escena grande que se acomoda arriba, fondo de malla de degradado en canvas con figuras flotantes,
HUD (píldora + contador + riel de puntos), transiciones tipo latigazo, subtítulos EN y **flyer final que sirve de
portada del reel** (título del video, subtítulo, 4 puntos, @tu_usuario con icono de IG, «SÍGUEME PARA MÁS»;
queda quieto ≥3 s dentro del área central 4:5).
- Spec por video en `videos/web3-en-60/specs.py`; cada carpeta tiene `build.py` que llama `build(HERE, spec)`.
- 13 componentes (`bigword stat checklist phone chart compare chips icons timeline steps quote pie channel`),
  cada uno con `kw` = palabra de la voz que lo dispara (busca en `transcript.json`, si no la encuentra usa posición proporcional).
- Temas p1–p9 en `THEMES3`; el color del texto sobre degradados (`on`) se calcula por contraste.
- `build()` escribe `timing.json` (dur, cortes, sfx) → `musica.py` y `sfx.py` con esos valores.
- **Voz v3: `es-MX-JorgeNeural`** (`--rate=+4% --gap 2.2 --start 1.0`). La AndrewMultilingual se descartó el 15-oct:
  al usuario le sonó «muy inglés, no puede pronunciar español». El texto que se lee pasa por `voz_texto()` (mapa `PRON`:
  exchange→exchéinch, wallet→wálet, DCA→de ce a, ETF→e te efe, CBDC→ce be de ce, Lightning→Láitning, blockchain→blokchéin);
  lo que se ve en pantalla no cambia.
- Ritmo y sonido (feedback 15-oct): entradas suaves de 0.6–1 s con `power3.out` (sin blur ni skew), cada componente
  aparece ≥3 s antes del corte, intro de 3.2 s con anillo, órbita, partículas y 3 entradas distintas; **pocos golpes**:
  un solo pop por componente, whoosh por corte, `musica.py ... suave` (sin golpes por escena) y SFX a 0.35.
- **Render final para reels:** `npx hyperframes render -f 60 --video-bitrate=16M -o video-raw.mp4` y luego loudnorm
  (~15 Mbps, ~100 MB por minuto, ~4.5 min de render). A 30 fps y `-q high` salía a ~5 Mbps y se veían bandas en los degradados.
