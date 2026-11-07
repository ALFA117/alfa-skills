# alfa-skills

Las skills que uso todos los días en **Claude Code** para diseñar páginas web, animar interfaces, hacer videos e imágenes y pensar ideas. Están todas juntas en un solo repo, separadas por tema, y se instalan con un comando.

> **¿Qué es una skill?** Es una carpeta con instrucciones (y a veces scripts) que le enseña a Claude a hacer algo de cierta forma. Cuando la instalas, Claude la usa solo cuando tu pedido encaja (por ejemplo «hazme un video de…»), o tú la llamas con `/nombre`.

---

## Instalar (1 minuto)

Necesitas tener [Claude Code](https://claude.com/claude-code) instalado. Elige una de estas tres opciones.

### Opción A: un solo comando

**Windows** (PowerShell):

```powershell
irm https://raw.githubusercontent.com/ALFA117/alfa-skills/main/instalar.ps1 | iex
```

**macOS / Linux** (Terminal):

```bash
curl -fsSL https://raw.githubusercontent.com/ALFA117/alfa-skills/main/instalar.sh | bash
```

### Opción B: pedírselo a Claude

Abre Claude Code y escríbele:

```text
Instala las skills de https://github.com/ALFA117/alfa-skills siguiendo su README
```

### Opción C: clonar el repo

```bash
git clone https://github.com/ALFA117/alfa-skills.git
cd alfa-skills
```

Luego, en **Windows**:

```powershell
powershell -ExecutionPolicy Bypass -File .\instalar.ps1 -Dependencias
```

En **macOS / Linux**:

```bash
bash instalar.sh --dependencias
```

### Qué hace el instalador

- Copia cada skill a `~/.claude/skills/<nombre>` (en Windows es `%USERPROFILE%\.claude\skills\`).
- Si ya tenías una skill con el mismo nombre, la mueve a `~/.claude/skills-respaldo/<fecha>/`. No se pierde nada.
- Revisa que tengas Node.js, Python y ffmpeg, y te dice cómo instalar lo que falte.
- Con `-Dependencias` / `--dependencias` instala además los paquetes de Python para voz y audio: `edge-tts`, `numpy`, `soundfile` y `pillow`.

**Solo algunos grupos:**
- Windows: `.\instalar.ps1 -Grupos diseno-web,ideas`
- macOS / Linux: `bash instalar.sh --grupos diseno-web,ideas`

Al terminar, **cierra y vuelve a abrir Claude Code** y escribe `/` para ver las skills nuevas.

---

## Qué trae

### 🎨 Diseño web: `skills/diseno-web/`

| Skill | Para qué sirve | Cómo se usa |
|---|---|---|
| **diseno** | Rediseño visual completo de un frontend: sistema de diseño, fondo 3D animado, móvil primero, estados, accesibilidad, SEO. Al final se revisa con capturas. | `/diseno` + lo que quieres cambiar |
| **diseno1.1** | Lo mismo que `diseno`, más el buscador de estilos de UI/UX Pro Max y la API de Motion verificada. Es la versión que más uso. | `/diseno1.1` o «rediseña con pro max y motion» |
| **DisenoS** | Rediseño en estilo **bento + brutalismo**: bloques de distintos tamaños, bordes gruesos, sombras duras, colores contrastantes con significado fijo, íconos e ilustraciones en SVG, minimalista y con un flujo más corto (compara los pasos de antes y después). | `/DisenoS` o «estilo bento brutalista» |
| **ui-ux-pro-max** | Base de datos de diseño: más de 50 estilos, 161 paletas, 57 parejas de fuentes y guías UX para React, Next, Vue, Tailwind, shadcn, etc. Trae un buscador en Python. | Se activa sola al pedir UI, o `/ui-ux-pro-max` |
| **motion** | Guía para animar en React con Motion (antes Framer Motion): entradas, salidas, stagger, layout, scroll, drag. | «anima esto», «agrega transiciones» |
| **taste-skill** (`design-taste-frontend`) | Diseño «anti-plantilla» para landings, portafolios y rediseños, para que no se vea hecho por IA. | «haz una landing que no se vea genérica» |

### 🎬 Video e imágenes: `skills/video/`

| Skill | Para qué sirve | Cómo se usa |
|---|---|---|
| **video** | Video animado completo (MP4) de punta a punta y sin preguntas: guion, voz en off en español, música, subtítulos y render. Vertical por default para Reels/TikTok. | `/video de qué es una wallet, 30 segundos` |
| **videoV2** | Producción «nivel cine»: primero pregunta contexto, formato, duración y voces. Entrega video, portada y texto para Instagram. | `/videoV2` |
| **hyperframes** | El motor: convierte HTML animado en video. Las demás skills de video se apoyan en esta. | «haz un video con HyperFrames» |
| **hyperframes-cli** | Comandos del CLI de HyperFrames: crear, revisar, previsualizar y renderizar. | Se usa sola cuando hace falta |
| **hyperframes-registry** | Unos 450 bloques listos: transiciones, títulos, subtítulos, gráficas, mapas, 3D. | «ponle una transición glitch» |
| **media-use** | Conseguir o generar música, efectos de sonido, imágenes, íconos, logos, voz, recortes y corrección de color. | «búscale música», «quítale el fondo» |
| **figma** | Llevar diseños de Figma a un video animado. | Pega un link de figma.com |
| **slideshow** | Presentaciones en vivo con modo presentador y notas. | «hazme una presentación» |
| **remotion-to-hyperframes** | Pasar videos hechos en Remotion, Lottie, Three.js, etc. a HyperFrames. | «convierte este proyecto de Remotion» |
| **reverse-any-video** | Reconstruir cualquier video como proyecto editable. | «recrea este video» + archivo |

### 🧑‍💼 Avatares y presentadores (HeyGen): `skills/heygen/`

| Skill | Para qué sirve |
|---|---|
| **heygen-avatar** | Crear un avatar con cara y voz (tuyo o un personaje). |
| **heygen-video** | Videos con presentador que habla: pitch, tutorial, anuncio. |
| **heygen-translate** | Doblar un video a otro idioma con tu voz clonada y los labios sincronizados. |

> Estas tres necesitan una cuenta de [HeyGen](https://www.heygen.com). Pueden usar el conector de HeyGen en Claude o la variable `HEYGEN_API_KEY`, y el uso cuesta créditos de HeyGen. Las demás skills son gratis.

### 💡 Ideas y decisiones: `skills/ideas/`

| Skill | Para qué sirve | Cómo se usa |
|---|---|---|
| **llm-council** | Pasa una idea o decisión por un «consejo» de 5 asesores que la analizan, se critican entre ellos y dan un veredicto. Basado en el LLM Council de Karpathy. | «tengo esta idea…», «council this» |

---

## Requisitos

| Herramienta | Para qué | Dónde |
|---|---|---|
| Claude Code | Todo | https://claude.com/claude-code |
| Node.js 22+ | Videos (HyperFrames corre con `npx hyperframes`) | https://nodejs.org |
| Python 3.10+ | Voz, música, efectos y buscador de estilos | https://www.python.org |
| ffmpeg | Render y audio | Windows: `winget install Gyan.FFmpeg` · macOS: `brew install ffmpeg` · Linux: `sudo apt install ffmpeg` |

Las skills de diseño web solo necesitan Python (para el buscador de UI/UX Pro Max). Las de ideas no necesitan nada.

---

## Personalizar

- **Tu firma en los videos.** Algunos estilos de `/video` cierran con tu @ de redes. Por default sale `@tu_usuario`. Para poner el tuyo, define una variable de entorno:
  - Windows: `setx FIRMA_REDES "@mi_usuario"`
  - macOS / Linux: agrega `export FIRMA_REDES="@mi_usuario"` a tu `~/.zshrc` o `~/.bashrc`

  También se lo puedes decir a Claude en el pedido: «firma con @mi_usuario».
- **La voz.** El default es `es-MX-DaliaNeural` (gratis, con edge-tts). Pide otra en el mensaje: «voz Jorge», «voz en inglés», «sin voz».
- **La carpeta de videos.** Por default los proyectos van en `~/videos/`. Dile a Claude si los quieres en otro lado.
- **Ejemplos.** Dentro de las skills de video hay referencias a proyectos de ejemplo (`videos/2026-…`). Son de mi máquina y no vienen en el repo; Claude sigue las reglas aunque no los tenga.

---

## Actualizar y desinstalar

- **Actualizar:** vuelve a correr el comando de instalación. Lo que tenías queda respaldado en `~/.claude/skills-respaldo/`.
- **Desinstalar una skill:** borra su carpeta en `~/.claude/skills/`. Por ejemplo, `~/.claude/skills/videoV2`.

---

## Estructura del repo

```text
alfa-skills/
├── instalar.ps1          # instalador para Windows
├── instalar.sh           # instalador para macOS / Linux
├── skills/
│   ├── diseno-web/       # diseno, diseno1.1, DisenoS, ui-ux-pro-max, motion, taste-skill
│   ├── video/            # video, videoV2, hyperframes y compañía
│   ├── heygen/           # avatares, presentadores y doblaje
│   └── ideas/            # llm-council
├── TERCEROS.md           # de dónde viene cada skill y su licencia
├── licencias/            # textos de las licencias de terceros
└── LICENSE
```

Cada carpeta dentro de `skills/<grupo>/` es una skill completa con su `SKILL.md`. Puedes copiar solo la que quieras a `~/.claude/skills/`.

---

## Créditos

Las skills **diseno**, **diseno1.1**, **DisenoS**, **motion**, **video**, **videoV2** y **llm-council** (adaptación) son mías. Las demás son de proyectos abiertos y se incluyen con su licencia: HyperFrames y HeyGen, UI/UX Pro Max y taste-skill. El detalle está en [TERCEROS.md](TERCEROS.md).

Hecho por **Alfa**.
