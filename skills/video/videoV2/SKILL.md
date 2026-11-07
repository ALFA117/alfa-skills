---
name: videoV2
description: Producción audiovisual de nivel cine (estándar «US$1M») para cualquier idea. Primero pregunta el contexto completo del video, el formato (reel de Instagram/TikTok, video demostración/presentación, anuncio cinematográfico 3D), la duración, las voces y los subtítulos. Luego produce el video con gancho inicial, animación con peso, diseño sonoro, portada final y pie de Instagram. Úsala cuando el usuario escriba /videoV2 o /video2, o pida «video pro», «video nivel cine», «anuncio tipo Apple/Duolingo», «video 3D», «video demostración de mi app», «reel producido de…».
model: claude-opus-5-5
argument-hint: "[contexto del video de principio a fin] [reel|demo|anuncio 3D] [duración] [voces] [ruta de fotos/assets]"
---

# /videoV2: producción de nivel cine para cualquier idea

Versión 2 de /video. Está construida a partir del brief maestro que pasó el usuario el 26-oct-2026 (anuncio conceptual
«Duolingo — The Path»), generalizado para cualquier tema.

**Lee `references/estandar-produccion.md` completo antes de diseñar.** Ese archivo es la vara de calidad:
- cinco cualidades;
- iluminación, cámara y animación;
- guion de 10 escenas;
- mezcla a −14 LUFS;
- QC con calificación del 1 al 10 y reglas absolutas.

A diferencia de /video, **esta skill sí pregunta primero** (paso 0) y después trabaja sola hasta entregar.

Todo lo que se le escribe al usuario va en español. Los textos internos del código pueden ir en inglés.

## Paso 0. Entrevista (una sola ronda; luego ya no se pregunta)

1. **Contexto.** Si los argumentos no traen el contexto, pídelo en texto y **detente hasta que conteste**. Pide:
   - de qué habla el video de principio a fin, el mensaje principal y cómo debe cerrar;
   - la marca o protagonista, si hay;
   - la ruta de fotos o assets que se pueden usar (pregúntale al usuario dónde están sus fotos);
   - el título que quiere en la **portada** (si no lo da, lo propones tú).

2. Con el contexto en mano, llama **AskUserQuestion** con estas 4 preguntas juntas, en este orden y con la opción
   recomendada primero:

   - **Formato** («¿Para qué es el video?»):
     - *Reel Instagram/TikTok (Recomendado):* vertical 1080×1920, gancho en 0.5 s, portada final y pie de IG.
     - *Video demostración / presentación:* horizontal 1920×1080, para mostrar una app, producto o pitch con mockups;
       ritmo más contemplativo.
     - *Anuncio cinematográfico 3D:* 15–30 s, mundo 3D real en Blender, versión vertical y horizontal recompuestas.
   - **Duración:** 30 s · 60 s · 2 min (Otro = lo que diga).
   - **Voces:**
     - *Dos voces, hombre y mujer, en diálogo (Recomendado):* un guía y una contraparte con humor.
     - *Una voz de hombre.*
     - *Una voz de mujer.*
     - *Sin voz:* música + SFX + texto.
   - **Subtítulos:** inglés (lo habitual en sus reels) · español · sin subtítulos.

3. Respeta lo que elija. Si escoge «Otro», adapta: cuadrado 1080×1080, 4:5 1080×1350, etc.

## Paso 1. Brief → guion + storyboard

Crea la carpeta del proyecto: `~/videos/AAAA-MM-DD-<slug>`. Copia ahí
`hyperframes.json`, `package.json` y `meta.json` de cualquier proyecto reciente y corrige el id y el nombre.

**`guion.py`** sigue el formato de `scripts/tts_dialogo.py`:
- `VOCES = {clave: dict(voice, rate, pitch, name)}`;
- `ESCENAS = [dict(id, lines=[(clave, texto_hablado, subtitulo, sfx|None)])]`.

**El texto hablado va con ortografía fonética** cuando haga falta (tabla abajo). El subtítulo va bien escrito.

**`storyboard.md`** define:
- el **hilo visual** (el elemento que conecta todo);
- las estaciones o escenas con su porcentaje de tiempo (plantilla de 10 escenas del estándar);
- qué componente o acción física pasa en cada una;
- la energía de cada escena: explosiva, fluida o contemplativa;
- las anclas palabra→segundo.

Para reels con voz, el guion se recorta hasta que la voz dure **la duración pedida menos unos 7 s** (gancho y portada).

**Guion entretenido:**
- un gancho que pare el scroll en el primer medio segundo;
- remates con efecto de sonido (rimshot, boing, scratch);
- un running gag (en la guía MVP fue el contador «COSTO TOTAL $0»);
- un cierre que pide guardar, compartir o seguir.

Ningún dato inventado. Si hay planes gratis, precios o fechas, verifícalos o dilos con prudencia.

## Paso 2. Audio

**Voces nativas en español (edge-tts):**

| Voz | Uso recomendado | Ajustes |
|---|---|---|
| `es-MX-JorgeNeural` | hombre: narrador o tráiler | rate +2 %, pitch −9 Hz para el tono de tráiler |
| `es-US-AlonsoNeural` | hombre: guía o «Alfa» | rate +6 % |
| `es-MX-DaliaNeural` | mujer: contraparte cómica | rate +12 % |
| `es-US-PalomaNeural` | mujer: alternativa | — |

- **Nunca** uses voces multilingües en inglés (Andrew, Ava…) para español: al usuario le sonaron «muy inglés».
- Las muestras están en `videos/voces-prueba`.

**Comandos:**
- Voz: `python scripts/tts_dialogo.py <proyecto> --start 3.4 --outro 7.5`. Genera `assets/voz.wav` y `lineas.json`; solo
  regenera las réplicas que cambian.
- Verificación: `npx hyperframes transcribe assets/voz.wav -l es`, copia `assets/transcript.json` a `transcript.json` y
  léelo completo. Si una palabra sale mal, cámbiala por su versión fonética y repite.

**Ortografía fonética probada:**

| Palabra | Escribir así |
|---|---|
| MVP | eme ve pe |
| React | Riáct |
| GitHub | GuitJab |
| Supabase | Súpabeis |
| Vercel | Bérsel |
| Cloudflare Pages | Claud fler Peiyes |
| full stack | ful stak |
| blockchain | blokchéin |
| hackathons | jákatons |
| Ethereum | Etérium |
| Lizzie | Lisi |
| wifi | wai fai |
| ETH Global | Ez Global |
| MagicBlock | Máyic Blok |
| DCA / ETF / CBDC | de ce a / e te efe / ce be de ce |

**Música y efectos:**
- Música: `python -I ~/.claude/skills/video/scripts/musica.py assets/musica.wav DUR "<cortes>" suave`. El modo `suave`
  deja un solo golpe, al final.
- Efectos: `python scripts/com_sfx.py assets/sfx.wav DUR sfx.json`. Tipos disponibles: rimshot, applause, scratch, boing,
  whoosh, impact, ding, pop, riser, type.
- **Pocos golpes:** un pop por componente, un whoosh por corte y un remate por chiste. Lo secundario se queda discreto.

## Paso 3. Construcción (según el formato)

### A) Reel o demo: HyperFrames «producido» (2.5D)

> **Feedback del usuario (27-oct):** «se ven completamente iguales, aburridos, se nota que es IA». La plantilla de abajo
> (encabezado con número + tablero + etiquetas de presentadores + subtítulos en caja + stickers + flyer) **ya está
> gastada**. Cada video nuevo cambia la ESTRUCTURA, no solo los colores.
>
> Modelo que sí gustó: `videos/2026-10-27-componentes-v2/build.py`.
> - Una sola cámara continua (proxy `cam {x,y,s,r}` → transform de `#world`) que vuela entre «estaciones» de un tablero
>   gigante, con zoom y giro en cada traslado.
> - Componentes reales dentro de un iPhone, con toques de dedo, ondas y resortes.
> - Las selfies verticales van completas a pantalla completa.
> - Subtítulos palabra por palabra sin caja.
> - Sin etiquetas de presentadores ni stickers.
> - Portada sobre la vista general del tablero.
>
> Otras estructuras para variar: documental con zoom sobre fotos, «pantalla del celular» tipo screen recording,
> collage editorial de revista, 3D en Blender.

La plantilla anterior (solo si encaja y sin repetirla seguido):
Parte del `build.py` más parecido:
- `videos/2026-10-16-guia-mvp/build.py`: guía con pasos, contador, editor de código, base de datos, terminal y gráfica;
- `videos/2026-10-15-presentacion-alfa/build.py`: gala cómica con telón, expediente, ficha RPG, polaroids y portada de revista.

Conserva las capas que ya funcionan:
1. **Cold open, 0–1.9 s:** cuatro a seis fotos a golpe de 0.3–0.4 s, una palabra encima de cada una y un destello.
2. **Golpe de título:** escala 2.2→1 con brillo que lo cruza y sacudida corta; la voz entra hacia 3.4 s.
3. **Fondo por escena:** la foto del usuario difuminada y oscurecida
   (`ffmpeg … boxblur=24:3,eq=brightness=-0.18` → `bNN.jpg`) con zoom lento.
4. **Acabado:** light leaks en `screen`, viñeta, grano SVG y **barrido de luz** en cada corte.
5. **Presentadores:** etiquetas con color propio y onda de audio real (envolvente de `voz.wav` a 30 Hz en canvas). El
   activo se ilumina y escala 1.06.
6. **Componentes animados por escena**, sincronizados a palabras de la transcripción con `W(palabra, línea)`.
7. **Subtítulos:** una frase a la vez, con borde del color de quien habla.
8. **Flyer-portada final:** quieto ≥3 s y dentro del área central 4:5. Lleva título, subtítulo, 4 puntos, foto,
   @tu_usuario con ícono de IG y CTA.

Cada video lleva **su propia identidad**: paleta y tipografías nuevas. No repitas la del anterior.

### B) Anuncio cinematográfico 3D: Blender + HyperFrames
- **Blender 4.3** está en `C:\Program Files\Blender Foundation\Blender 4.3\blender.exe`. La GPU es una RTX 3050 Ti con
  OptiX.
- Parte de `scripts/blender_base.py`. Sus utilidades: `material_pbr`, `boton` biselado con base, `linea_luz` (curva con
  volumen y emisión, crece con `bevel_factor_end`), `camara_spline` (una sola cámara con easing, DOF y Track-To), `luces`
  (key/fill/rim), `mundo_fondo` (bruma volumétrica) y `render_cfg` (AgX, motion blur, PNG de 16 bits, EEVEE Next o Cycles).
- Render:
  `blender -b -P mundo.py -- --out frames --fmt vertical --fps 60 --dur 21.2 --engine eevee|cycles [--frames a-b] [--scale 0.5]`.
- **Antes de lanzar todo, mide:** renderiza 2 frames, calcula el tiempo total y díselo al usuario.
  - Referencia a media resolución: EEVEE ~36 s y Cycles 64 spp ~18 s, contando el arranque.
  - A 60 fps, 21 s son ~1270 frames; en Cycles a resolución completa pueden ser horas.
  - EEVEE Next sirve para casi todo. Cycles se reserva para planos héroe.
- Codifica: `ffmpeg -framerate 60 -i frames/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 14 -preset slow fondo3d.mp4`.
- **Tipografía, subtítulos, logo y portada van encima en HyperFrames:** `fondo3d.mp4` entra como `<video muted>`. Así el
  texto queda nítido y legible.
- **Vertical y horizontal se recomponen.** Cámara y posiciones van distintas en cada uno. Nunca es un recorte.
- **Emisión de la línea:** ~6–10. Más alto se vuelve blanca con AgX y pierde el color.
- **Marcas ajenas** (Duolingo, Apple…) en piezas conceptuales para portafolio:
  - no se recrean logos de memoria ni se publica como si fuera oficial;
  - usa tipografía propia o assets con permiso;
  - aclara «concepto / spec ad» en el pie.

## Paso 4. QC (obligatorio, con inspección real)

1. `npx hyperframes check`. Errores de overlap o contraste a mitad de una animación se toleran; los que se ven quietos
   se corrigen.
2. `npx hyperframes snapshot --at <lista de tiempos clave> --no-end -o snaps`. Lee las hojas de contacto: impactos, cada
   escena y la portada.
3. Escribe `qc.md` con la calificación de 1 a 10 por escena en composición, movimiento, luz, narrativa y satisfacción, con
   **defectos vistos y correcciones**. Menos de 9 en algo importante obliga a corregir y volver a mirar.
4. Revisa la privacidad: `grep` de apellidos y datos personales en `index.html` y en la transcripción.

## Paso 5. Render final

- `npx hyperframes render -f 60 --video-bitrate=16M -o video-raw.mp4`. Para 2 min son ~9–10 min de render.
- Mezcla: `ffmpeg -i video-raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-2.0:LRA=11,alimiter=limit=0.74:level=false,aresample=48000" -c:a aac -b:a 192k video.mp4`. Queda en
  −14 LUFS con pico ≤ −1.25 dBTP. Sin el alimiter, el pico salía en −0.9 dB por el AAC.
- Verifica duración, fps (60/1), bitrate (~15 Mbps) y LUFS con `ffprobe` y `ebur128`. Borra `video-raw.mp4`.
- Corre el render en segundo plano y avisa al usuario que está en proceso.

## Paso 6. Entrega: video + portada + pie

1. **Portada:** `ffmpeg -sseof -0.5 -i video.mp4 -frames:v 1 -q:v 2 portada.jpg`. Es el flyer final; el usuario la elige como
   portada del reel.
2. **SendUserFile** del video, con el **pie de Instagram en el caption**, y aparte la portada. Formato que le gusta
   (video / pie, nada de listas largas):

   ```
   <Título> <emoji>

   <emoji> <gancho de una línea>

   <emoji> punto 1
   <emoji> punto 2
   … (4–7 puntos)

   <remate o pregunta para comentarios> 👇
   📌 <CTA: guárdalo / sígueme>

   #tema #tema … #alfa_edg.mou
   ```

3. En el chat, cuenta qué hiciste en pocas líneas: gancho, estilo, voces, duración y calidad. Recuérdale activar en IG
   «Subir con la máxima calidad».

## Reglas aprendidas (no repetir errores)

- **Privacidad:** en contenido público usa solo el nombre o @ que el usuario autorice. Nunca apellidos ni datos completos.
- **Zonas del vertical:**
  - 0–240 vacío (interfaz de IG);
  - título 250–560;
  - escenario 580–1340;
  - presentadores 1360;
  - subtítulos 1490;
  - el fondo de abajo queda libre.
- **Legibilidad:**
  - cada componente aparece ≥3 s antes del corte;
  - entradas de 0.6–1 s con `power3.out`, sin blur ni skew;
  - nada «trabado» ni tan rápido que no se alcance a leer.
- **GSAP:**
  - no pongas `transform` CSS en elementos animados (la rotación va dentro de `fromTo`);
  - las salidas son `fromTo` con `immediateRender: false`;
  - `className` no se anima;
  - no mezcles keyframes con otras propiedades en el mismo tween.
- **Emojis y glifos raros:** como SVG, nunca en texto (el linter marca la falta de fuente).
- **Bash:** heredocs con comillas o backticks se rompen en esta terminal. Escribe scripts y parches con la herramienta
  Write y ejecútalos.
- **Contraste:** el texto sobre degradados usa el color que mejor contraste dé. Revisa el linter.
- **Encuadre de fotos (regla del usuario, 26-oct):** nunca dejes el recorte al azar de `object-fit` + `object-position`.
  1. Haz una hoja con cuadrícula de porcentajes de cada foto.
  2. Mide dónde están la cara y el cuerpo.
  3. Define cada uso en `scripts/recortes.py` (copiarlo al proyecto). Se indica por uso: foto, centro x, arriba, alto
     y proporción exacta de su caja.
  4. Genera `c_<uso>.jpg` y revisa `_grid/recortes.jpg` antes de construir.

  Reglas del encuadre:
  - cara en el tercio superior, con aire arriba de la cabeza;
  - cortes en la cintura, o cuerpo completo; **nunca en rodillas o tobillos**;
  - los avatares redondos llevan el rostro completo con el cabello;
  - para cajas horizontales usa fotos de busto o horizontales, no fotos de cuerpo completo vertical.

  OpenCV 5 ya no trae `CascadeClassifier`; para detectar caras se mide a ojo con la cuadrícula.
- **Duraciones:** reels de 1 a 2 min funcionaron; un gancho de 3.4 s antes de la voz y una portada de ~7 s al final.

## Referencias
- `references/estandar-produccion.md`: el brief maestro generalizado. Es obligatorio leerlo.
- `scripts/tts_dialogo.py`: voz con varios personajes.
- `scripts/com_sfx.py`: efectos de comedia y de movimiento.
- `scripts/blender_base.py`: mundo 3D base.
- `scripts/recortes.py`: encuadres manuales por uso (cara y cuerpo bien puestos) + hoja de revisión.
- `~/.claude/skills/video/`: musica.py, sfx.py, produccion.py (serie «Web3 en 60»), diccionario.py y voz.py.
- Proyectos modelo: `videos/2026-10-15-presentacion-alfa` (gala cómica) y `videos/2026-10-16-guia-mvp` (guía en 7 pasos).
