"""Encuadres manuales por uso: cada foto se recorta a la proporción exacta de su caja.
Las posiciones de cara y cuerpo se midieron con cuadrícula. Reglas del encuadre:
- cara en el tercio superior, con aire arriba de la cabeza;
- cortes en la cintura o cuerpo completo, nunca en rodillas o tobillos.
Genera assets/fotos/c_<uso>.jpg (al doble de la resolución de la caja) y _grid/recortes.jpg para revisión."""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "assets", "fotos")
# uso: (foto, centro_x, arriba, alto (fracción del alto de la foto), proporción ancho/alto de la caja, ancho de salida)
CROPS = {
    "hero": (2, 0.52, 0.107, 0.62, 1.29, 1080),      # «Hola, soy Alfa»: busto en la mesa (gancho y página final)
    "card": (13, 0.50, 0.14, 0.36, 1.286, 1080),     # card: de la cabeza a la cintura
    "avatar": (10, 0.46, 0.13, 0.31, 1.0, 240),     # avatares redondos: rostro centrado
    "tabs": (17, 0.50, 0.07, 0.384, 1.953, 1680),    # pestaña Fotos: sentado, manos arriba completas
    "car0": (7, 0.50, 0.075, 0.461, 1.219, 1560),
    "car1": (10, 0.50, 0.106, 0.461, 1.219, 1560),
    "car2": (11, 0.50, 0.176, 0.461, 1.219, 1560),
    "car3": (16, 0.50, 0.075, 0.461, 1.219, 1560),
    "car4": (18, 0.50, 0.03, 0.461, 1.219, 1560),
    "rav": (14, 0.68, 0.215, 0.37, 1.0, 240),        # avatar del skeleton
    "rim": (21, 0.52, 0.06, 0.39, 1.3, 1144),        # post del skeleton: de la cabeza a la cintura
    "fc0": (12, 0.54, 0.17, 0.30, 1.205, 480),
    "fc1": (21, 0.52, 0.06, 0.36, 1.205, 480),
    "flyer": (13, 0.48, 0.135, 0.385, 0.766, 720),   # portada: busto
}
tiles = []
for name, (n, cx, top, h, asp, ow) in CROPS.items():
    im = Image.open(os.path.join(F, f"f{n:02d}.jpg")).convert("RGB")
    W, H = im.size
    ph = h * H
    pw = ph * asp
    assert pw <= W + 1, (name, pw, W)
    left = min(max(0, cx * W - pw / 2), W - pw)
    box = (round(left), round(top * H), round(left + pw), round(top * H + ph))
    c = im.crop(box).resize((ow, round(ow / asp)), Image.LANCZOS)
    c.save(os.path.join(F, f"c_{name}.jpg"), quality=92)
    t = c.copy()
    t.thumbnail((300, 300))
    can = Image.new("RGB", (310, 330), (40, 40, 40))
    can.paste(t, (5, 5))
    ImageDraw.Draw(can).text((8, 312), f"{name} (f{n:02d})", fill=(255, 255, 0))
    tiles.append(can)
cols = 5
sheet = Image.new("RGB", (310 * cols, 330 * ((len(tiles) + cols - 1) // cols)), (20, 20, 20))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * 310, (i // cols) * 330))
os.makedirs(os.path.join(HERE, "_grid"), exist_ok=True)
sheet.save(os.path.join(HERE, "_grid", "recortes.jpg"), quality=90)
print("ok", len(tiles))
