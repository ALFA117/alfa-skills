# Instalador de alfa-skills para Windows (PowerShell 5.1 o 7).
#
# Desde internet, sin clonar:
#   irm https://raw.githubusercontent.com/ALFA117/alfa-skills/main/instalar.ps1 | iex
# Desde el repo clonado:
#   powershell -ExecutionPolicy Bypass -File .\instalar.ps1 [-Grupos diseno-web,video] [-Dependencias]
#
# Copia cada skill a %USERPROFILE%\.claude\skills\<nombre>. Si ya tenias una con el mismo
# nombre, la respalda antes en %USERPROFILE%\.claude\skills-respaldo\<fecha>\.

param(
    [string[]]$Grupos = @(),
    [switch]$Dependencias
)

$ErrorActionPreference = 'Stop'
# Con -File los grupos llegan como un solo texto "a,b": se separan aqui.
$Grupos = @($Grupos | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
$Repo = 'ALFA117/alfa-skills'
$Rama = 'main'

function Escribir($texto, $color = 'Gray') { Write-Host $texto -ForegroundColor $color }

# 1. Ubicar las skills: junto al script o descargando el repo.
$origen = $null
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot 'skills'))) {
    $origen = Join-Path $PSScriptRoot 'skills'
} else {
    $tmp = Join-Path ([IO.Path]::GetTempPath()) ("alfa-skills-" + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    $zip = Join-Path $tmp 'repo.zip'
    Escribir "Descargando $Repo ..." 'Cyan'
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/$Repo/archive/refs/heads/$Rama.zip" -OutFile $zip
    Expand-Archive -Path $zip -DestinationPath $tmp
    $origen = Join-Path (Get-ChildItem $tmp -Directory | Select-Object -First 1).FullName 'skills'
}

$destino = Join-Path $env:USERPROFILE '.claude\skills'
$respaldo = Join-Path $env:USERPROFILE ('.claude\skills-respaldo\' + (Get-Date -Format 'yyyy-MM-dd_HHmmss'))
New-Item -ItemType Directory -Force -Path $destino | Out-Null

# 2. Copiar cada skill.
$instaladas = @()
foreach ($grupo in Get-ChildItem $origen -Directory) {
    if ($Grupos.Count -gt 0 -and $Grupos -notcontains $grupo.Name) { continue }
    foreach ($skill in Get-ChildItem $grupo.FullName -Directory) {
        $final = Join-Path $destino $skill.Name
        if (Test-Path $final) {
            New-Item -ItemType Directory -Force -Path $respaldo | Out-Null
            Move-Item $final (Join-Path $respaldo $skill.Name)
        }
        Copy-Item $skill.FullName $final -Recurse
        $instaladas += "$($grupo.Name)/$($skill.Name)"
    }
}

Escribir ""
Escribir "Skills instaladas en $destino :" 'Green'
$instaladas | ForEach-Object { Escribir "  - $_" }
if (Test-Path $respaldo) { Escribir "Las versiones anteriores quedaron respaldadas en $respaldo" 'Yellow' }

# 3. Revisar herramientas que usan las skills de video y diseno.
Escribir ""
Escribir "Revisando herramientas:" 'Cyan'
$faltan = @()
foreach ($h in @(
    @{ cmd = 'node';   para = 'HyperFrames (videos). Necesita Node.js 22 o mayor: https://nodejs.org' },
    @{ cmd = 'python'; para = 'scripts de voz, musica y busqueda de estilos: https://www.python.org' },
    @{ cmd = 'ffmpeg'; para = 'render y audio de los videos: winget install Gyan.FFmpeg' }
)) {
    if (Get-Command $h.cmd -ErrorAction SilentlyContinue) { Escribir "  OK  $($h.cmd)" 'Green' }
    else { Escribir "  FALTA $($h.cmd) -> $($h.para)" 'Yellow'; $faltan += $h.cmd }
}

if ($Dependencias -and (Get-Command python -ErrorAction SilentlyContinue)) {
    Escribir ""
    Escribir "Instalando paquetes de Python para voz y audio (edge-tts, numpy, soundfile, pillow)..." 'Cyan'
    python -m pip install --user --upgrade edge-tts numpy soundfile pillow
}

Escribir ""
Escribir "Listo. Cierra y vuelve a abrir Claude Code y escribe / para ver las skills (ej. /video, /diseno1.1)." 'Green'
if (-not $Dependencias) { Escribir "Tip: corre de nuevo con -Dependencias para instalar los paquetes de Python de voz y audio." }
