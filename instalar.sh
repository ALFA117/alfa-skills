#!/usr/bin/env bash
# Instalador de alfa-skills para macOS y Linux.
#
# Desde internet, sin clonar:
#   curl -fsSL https://raw.githubusercontent.com/ALFA117/alfa-skills/main/instalar.sh | bash
# Desde el repo clonado:
#   bash instalar.sh [--grupos diseno-web,video] [--dependencias]
#
# Copia cada skill a ~/.claude/skills/<nombre>. Si ya tenias una con el mismo nombre,
# la respalda antes en ~/.claude/skills-respaldo/<fecha>/.
set -euo pipefail

REPO="ALFA117/alfa-skills"
RAMA="main"
GRUPOS=""
DEPENDENCIAS=0

while [ $# -gt 0 ]; do
  case "$1" in
    --grupos) GRUPOS="$2"; shift 2 ;;
    --dependencias) DEPENDENCIAS=1; shift ;;
    *) echo "Opcion desconocida: $1"; exit 1 ;;
  esac
done

# 1. Ubicar las skills: junto al script o descargando el repo.
DIR_SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
if [ -n "$DIR_SCRIPT" ] && [ -d "$DIR_SCRIPT/skills" ]; then
  ORIGEN="$DIR_SCRIPT/skills"
else
  TMP="$(mktemp -d)"
  echo "Descargando $REPO ..."
  curl -fsSL "https://github.com/$REPO/archive/refs/heads/$RAMA.tar.gz" | tar -xz -C "$TMP"
  ORIGEN="$(find "$TMP" -mindepth 1 -maxdepth 1 -type d | head -1)/skills"
fi

DESTINO="$HOME/.claude/skills"
RESPALDO="$HOME/.claude/skills-respaldo/$(date +%Y-%m-%d_%H%M%S)"
mkdir -p "$DESTINO"

# 2. Copiar cada skill.
echo
echo "Skills instaladas en $DESTINO:"
for grupo in "$ORIGEN"/*/; do
  g="$(basename "$grupo")"
  if [ -n "$GRUPOS" ] && [[ ",$GRUPOS," != *",$g,"* ]]; then continue; fi
  for skill in "$grupo"*/; do
    s="$(basename "$skill")"
    if [ -e "$DESTINO/$s" ]; then
      mkdir -p "$RESPALDO"
      mv "$DESTINO/$s" "$RESPALDO/$s"
    fi
    cp -R "$skill" "$DESTINO/$s"
    echo "  - $g/$s"
  done
done
[ -d "$RESPALDO" ] && echo "Las versiones anteriores quedaron respaldadas en $RESPALDO"

# 3. Revisar herramientas que usan las skills de video y diseno.
echo
echo "Revisando herramientas:"
revisar() { if command -v "$1" >/dev/null 2>&1; then echo "  OK  $1"; else echo "  FALTA $1 -> $2"; fi; }
revisar node "HyperFrames (videos). Necesita Node.js 22 o mayor: https://nodejs.org"
revisar python3 "scripts de voz, musica y busqueda de estilos: https://www.python.org"
revisar ffmpeg "render y audio de los videos: brew install ffmpeg  /  sudo apt install ffmpeg"

if [ "$DEPENDENCIAS" = 1 ] && command -v python3 >/dev/null 2>&1; then
  echo
  echo "Instalando paquetes de Python para voz y audio (edge-tts, numpy, soundfile, pillow)..."
  python3 -m pip install --user --upgrade edge-tts numpy soundfile pillow
fi

echo
echo "Listo. Cierra y vuelve a abrir Claude Code y escribe / para ver las skills (ej. /video, /diseno1.1)."
[ "$DEPENDENCIAS" = 1 ] || echo "Tip: corre de nuevo con --dependencias para instalar los paquetes de Python de voz y audio."
