"""Base 3D para /videoV2 (Blender 4.3 sin ventana, GPU OptiX en Cycles o EEVEE Next).

Uso:
  blender -b -P blender_base.py -- --out <carpeta_frames> --fmt vertical|horizontal --fps 60 --dur 21.2
                                   [--engine eevee|cycles] [--frames a-b] [--scale 1.0] [--samples 64]

Construye un mundo de ejemplo y renderiza una secuencia PNG de 16 bits:
- fondo oscuro con bruma volumétrica;
- botón PBR biselado con base más oscura;
- línea de energía emisiva con volumen real;
- cámara en spline con aceleración y profundidad de campo;
- luces key, fill y rim.

Para un proyecto, copia este archivo y reemplaza construir_mundo() por la escena real. Las utilidades se reutilizan
tal cual: material_pbr, boton, linea_luz, camara_spline, luces, mundo_fondo y render_cfg.
"""
import argparse
import math
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--fmt", default="vertical")
ap.add_argument("--fps", type=int, default=60)
ap.add_argument("--dur", type=float, default=21.2)
ap.add_argument("--engine", default="eevee")
ap.add_argument("--frames", default=None)
ap.add_argument("--scale", type=float, default=1.0)
ap.add_argument("--samples", type=int, default=64)
A = ap.parse_args(argv)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)) + (1,)


def material_pbr(nombre, color, rough=0.35, metal=0.0, emit=None, emit_str=0.0, coat=0.0):
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexrgb(color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if emit:
        b.inputs["Emission Color"].default_value = hexrgb(emit)
        b.inputs["Emission Strength"].default_value = emit_str
    return m


def bisel(ob, ancho=0.12, seg=6):
    mod = ob.modifiers.new("bev", "BEVEL")
    mod.width, mod.segments = ancho, seg
    return mod


def boton(nombre, loc, size=(2.4, 0.9, 0.35), color="#58CC02", base="#46A302"):
    """Botón físico: tapa satinada biselada + base más oscura. Animar la tapa en Z para «presionarlo»."""
    bpy.ops.mesh.primitive_cube_add(location=(loc[0], loc[1], loc[2] - 0.12))
    bas = bpy.context.object
    bas.name, bas.scale = nombre + "_base", (size[0] / 2, size[1] / 2, size[2] / 2)
    bisel(bas)
    bas.data.materials.append(material_pbr(nombre + "_mb", base, 0.5))
    bpy.ops.mesh.primitive_cube_add(location=loc)
    top = bpy.context.object
    top.name, top.scale = nombre, (size[0] / 2, size[1] / 2, size[2] / 2)
    bisel(top)
    top.data.materials.append(material_pbr(nombre + "_m", color, 0.28, coat=0.3))
    bpy.ops.object.shade_smooth()
    return top, bas


def curva(nombre, puntos):
    cd = bpy.data.curves.new(nombre, "CURVE")
    cd.dimensions = "3D"
    sp = cd.splines.new("NURBS")
    sp.points.add(len(puntos) - 1)
    for p, c in zip(sp.points, puntos):
        p.co = (*c, 1)
    sp.use_endpoint_u, sp.order_u = True, 4
    ob = bpy.data.objects.new(nombre, cd)
    bpy.context.collection.objects.link(ob)
    return ob


def linea_luz(puntos, color="#58FF6A", grosor=0.03, fuerza=8, crecer=None):
    """Línea de energía con volumen (bevel) y emisión. crecer=(f0, f1) anima bevel_factor_end de 0 a 1."""
    ob = curva("linea", puntos)
    ob.data.bevel_depth, ob.data.bevel_resolution = grosor, 6
    ob.data.materials.append(material_pbr("linea_m", color, 0.2, emit=color, emit_str=fuerza))
    if crecer:
        ob.data.bevel_factor_end = 0.0
        ob.data.keyframe_insert("bevel_factor_end", frame=crecer[0])
        ob.data.bevel_factor_end = 1.0
        ob.data.keyframe_insert("bevel_factor_end", frame=crecer[1])
    return ob


def camara_spline(puntos, objetivo, fps, dur, lente=35, f_stop=2.8):
    """Una sola cámara que recorre una spline con aceleración/desaceleración (Bezier AUTO), mirando y enfocando al objetivo."""
    ruta = curva("ruta_cam", puntos)
    cam_d = bpy.data.cameras.new("cam")
    cam_d.lens = lente
    cam_d.dof.use_dof, cam_d.dof.aperture_fstop = True, f_stop
    cam = bpy.data.objects.new("cam", cam_d)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    fp = cam.constraints.new("FOLLOW_PATH")
    fp.target, fp.use_fixed_location = ruta, True
    fp.offset_factor = 0.0
    cam.keyframe_insert('constraints["Follow Path"].offset_factor', frame=1)
    fp.offset_factor = 1.0
    cam.keyframe_insert('constraints["Follow Path"].offset_factor', frame=int(fps * dur))
    for fc in cam.animation_data.action.fcurves:
        for k in fc.keyframe_points:
            k.interpolation, k.easing = "BEZIER", "AUTO"
    tr = cam.constraints.new("TRACK_TO")
    tr.target, tr.track_axis, tr.up_axis = objetivo, "TRACK_NEGATIVE_Z", "UP_Y"
    cam_d.dof.focus_object = objetivo
    return cam


def luces():
    """Key amplia y suave, fill muy controlada (fría), rim de separación."""
    def area(n, loc, rot, energia, size, color=(1, 1, 1)):
        d = bpy.data.lights.new(n, "AREA")
        d.energy, d.size, d.color = energia, size, color
        o = bpy.data.objects.new(n, d)
        o.location, o.rotation_euler = loc, rot
        bpy.context.collection.objects.link(o)
        return o
    return (area("key", (4, -5, 6), (math.radians(50), 0, math.radians(35)), 900, 6),
            area("fill", (-6, -3, 2), (math.radians(70), 0, math.radians(-60)), 120, 8, (0.85, 0.92, 1)),
            area("rim", (0, 6, 4), (math.radians(-60), 0, math.radians(180)), 600, 3))


def mundo_fondo(color="#060A0C", bruma=0.012):
    w = bpy.data.worlds.new("mundo")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes["Background"].inputs["Color"].default_value = hexrgb(color)
    if bruma:
        vol = nt.nodes.new("ShaderNodeVolumePrincipled")
        vol.inputs["Density"].default_value = bruma
        nt.links.new(vol.outputs[0], nt.nodes["World Output"].inputs["Volume"])


def render_cfg(fmt, fps, dur, engine, out, scale, samples):
    s = bpy.context.scene
    s.render.resolution_x, s.render.resolution_y = (1080, 1920) if fmt == "vertical" else (1920, 1080)
    s.render.resolution_percentage = int(100 * scale)
    s.render.fps = fps
    s.frame_start, s.frame_end = 1, int(round(fps * dur))
    s.render.use_motion_blur = True
    s.view_settings.view_transform = "AgX"
    s.view_settings.look = "AgX - Medium High Contrast"
    s.render.image_settings.file_format, s.render.image_settings.color_depth = "PNG", "16"
    s.render.filepath = out.rstrip("/\\") + "/f_"
    if engine == "cycles":
        s.render.engine = "CYCLES"
        pr = bpy.context.preferences.addons["cycles"].preferences
        pr.compute_device_type = "OPTIX"
        pr.get_devices()
        for d in pr.devices:
            d.use = d.type == "OPTIX"
        s.cycles.device, s.cycles.samples, s.cycles.use_denoising = "GPU", samples, True
    else:
        s.render.engine = "BLENDER_EEVEE_NEXT"
        s.eevee.taa_render_samples = samples
        s.eevee.use_raytracing = True


def construir_mundo():
    """Escena de ejemplo: REEMPLAZAR por el mundo del proyecto."""
    top, _ = boton("empezar", (0, 0, 0.3))
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -0.2))
    bpy.context.object.data.materials.append(material_pbr("piso_m", "#0B1114", 0.6))
    linea_luz([(-6, -2, 0.6), (-2, -1, 1.2), (0, 0, 0.8), (2, 1, 1.4), (6, 3, 0.9)], crecer=(1, int(A.fps * 3)))
    camara_spline([(0, -9, 3), (-3, -6, 2.2), (2.5, -4, 1.6), (0, -3.2, 1.2)], top, A.fps, A.dur)
    luces()
    mundo_fondo()


bpy.ops.wm.read_factory_settings(use_empty=True)
construir_mundo()
render_cfg(A.fmt, A.fps, A.dur, A.engine, A.out, A.scale, A.samples)
if A.frames:
    a, b = (int(x) for x in A.frames.split("-"))
    bpy.context.scene.frame_start, bpy.context.scene.frame_end = a, b
bpy.ops.render.render(animation=True)
print("RENDER_OK", bpy.context.scene.frame_start, bpy.context.scene.frame_end)
