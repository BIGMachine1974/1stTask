"""TCMG claymation style test: the "Find your street" scene from the paper test, built in clay.

usage (Blender in background):
  blender -b -P make_clay.py -- stills 0.5,3.0,5.5 [--res 360] [--samples 16]   test stills at those times (s)
  blender -b -P make_clay.py -- poses [--res 720] [--samples 48]                 every pose, 12 a second (on twos)

Poses are written to poses/p###.png; render.sh holds each one for 2 frames at 24 fps and muxes the music.
The look: matte clay (high roughness, a little subsurface), thumb-print bump, soft bevelled edges, small lumps,
a tabletop set under a warm key light, shallow depth of field, and a "boil": every pose nudges every piece a
hair and re-rolls the surface noise, the way hands disturb real clay between photos.
"""
import bpy, math, random, sys
from pathlib import Path
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["stills", "5.5"]
MODE = ARGS[0]
def opt(name, default):
    return type(default)(ARGS[ARGS.index(name) + 1]) if name in ARGS else default
RES, SAMPLES, DUR, PPS = opt("--res", 540), opt("--samples", 16), 6.0, 12
FONT = HERE / "assets" / "Mansfield-Extra-Bold.ttf"

PAL = dict(parch="#f1efe8", paper="#e7e3d8", white="#fffdf8", brass="#c2a56a", brassL="#d8c08f", brassD="#725b2f",
           moss="#59644d", mossL="#7d8770", slate="#4d5560", carbon="#22241f", brick="#a8664a", ink="#171915")

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1]

# ---------- scene ----------
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 3
sc.cycles.use_adaptive_sampling = True
sc.render.use_persistent_data = True
sc.render.resolution_x, sc.render.resolution_y = RES, int(RES * 16 / 9)
sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"
sc.view_settings.look = "AgX - Base Contrast" if "AgX - Base Contrast" in [l.name for l in []] else "None"
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = srgb(PAL["paper"])
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35

NOISES = []  # every clay material's noise node, re-rolled each pose (the boil)

def clay(name, hexcol):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; N, L = nt.nodes, nt.links
    b = N["Principled BSDF"]
    b.inputs["Base Color"].default_value = srgb(hexcol)
    b.inputs["Roughness"].default_value = 0.82
    b.inputs["Subsurface Weight"].default_value = 0.0
    b.inputs["Subsurface Radius"].default_value = (0.08, 0.04, 0.03)
    b.inputs["Subsurface Scale"].default_value = 0.05
    tc = N.new("ShaderNodeTexCoord")
    # thumb prints: stretched voronoi cells, plus fine noise for the clay grain
    vor = N.new("ShaderNodeTexVoronoi"); vor.voronoi_dimensions = "4D"; vor.feature = "SMOOTH_F1"
    vor.inputs["Scale"].default_value = 9.0
    noi = N.new("ShaderNodeTexNoise"); noi.noise_dimensions = "4D"
    noi.inputs["Scale"].default_value = 38.0; noi.inputs["Detail"].default_value = 4
    L.new(tc.outputs["Object"], vor.inputs["Vector"]); L.new(tc.outputs["Object"], noi.inputs["Vector"])
    mix = N.new("ShaderNodeMath"); mix.operation = "MULTIPLY_ADD"
    L.new(noi.outputs["Fac"], mix.inputs[0]); mix.inputs[1].default_value = 0.35
    L.new(vor.outputs["Distance"], mix.inputs[2])
    bump = N.new("ShaderNodeBump"); bump.inputs["Strength"].default_value = 0.6; bump.inputs["Distance"].default_value = 0.02
    L.new(mix.outputs[0], bump.inputs["Height"]); L.new(bump.outputs["Normal"], b.inputs["Normal"])
    NOISES.extend([vor, noi])
    return m

MATS = {k: clay(k, v) for k, v in PAL.items()}
PIECES = []  # (object, rest location, rest rotation, rest scale, appear time, pivot kind)

def soften(o, bevel=0.04, lumps=0.02, sub=1):
    bv = o.modifiers.new("bevel", "BEVEL"); bv.width = bevel; bv.segments = 3; bv.limit_method = "NONE"
    sd = o.modifiers.new("sub", "SUBSURF"); sd.levels = sd.render_levels = sub
    if lumps:
        tex = bpy.data.textures.new(o.name + "_lump", "CLOUDS"); tex.noise_scale = 0.35
        dp = o.modifiers.new("lumps", "DISPLACE"); dp.texture = tex; dp.strength = lumps; dp.texture_coords = "GLOBAL"
    for p in o.data.polygons: p.use_smooth = True

def add(o, mat, appear, kind="pop", **kw):
    o.data.materials.append(MATS[mat]); soften(o, **kw)
    PIECES.append([o, o.location.copy(), o.rotation_euler.copy(), o.scale.copy(), appear, kind])
    return o

def box(name, loc, size, mat, appear, kind="pop", **kw):
    bpy.ops.mesh.primitive_cube_add(location=loc); o = bpy.context.object; o.name = name
    o.scale = (size[0] / 2, size[1] / 2, size[2] / 2); bpy.ops.object.transform_apply(scale=True)
    return add(o, mat, appear, kind, **kw)

def roof(name, x, z, w, d, h, mat, appear):
    """A triangular prism sitting on the wall top at height z."""
    me = bpy.data.meshes.new(name)
    v = [(-w / 2, -d / 2, 0), (w / 2, -d / 2, 0), (0, -d / 2, h), (-w / 2, d / 2, 0), (w / 2, d / 2, 0), (0, d / 2, h)]
    f = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (0, 2, 5, 3)]
    me.from_pydata(v, [], f); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.location = (x, 0, z)
    return add(o, mat, appear, bevel=0.03, lumps=0.008)

def house(name, x, w, h, wall, roofc, doorc, t0, chimney=False):
    box(name + "_wall", (x, 0, h / 2), (w, 0.8, h), wall, t0)
    roof(name + "_roof", x, h - 0.02, w * 1.2, 0.95, 0.5, roofc, t0 + 0.08)
    box(name + "_door", (x, -0.41, 0.26), (w * 0.22, 0.06, 0.5), doorc, t0 + 0.16, bevel=0.02, lumps=0.004)
    for dx in (-w * 0.28, w * 0.28):
        box(name + f"_win{dx:+.2f}", (x + dx, -0.41, h * 0.68), (w * 0.2, 0.06, w * 0.2), "brassL", t0 + 0.2, bevel=0.02, lumps=0.004)
    if chimney:
        box(name + "_chim", (x + w * 0.25, 0, h + 0.38), (0.13, 0.13, 0.4), "brick", t0 + 0.28, bevel=0.02, kind="popbase")

def tree(name, x, y, s, t0):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05 * s, depth=0.4 * s, location=(x, y, 0.2 * s))
    add(bpy.context.object, "brassD", t0, bevel=0.01, lumps=0.004)
    for i, (r, z, c) in enumerate([(0.38, 0.55, "moss"), (0.28, 0.85, "mossL")]):
        bpy.ops.mesh.primitive_cone_add(radius1=r * s, depth=0.55 * s, location=(x, y, z * s))
        add(bpy.context.object, c, t0 + 0.08 * (i + 1), bevel=0.02, lumps=0.02)

def blob(name, loc, scale, mat, appear, kind="pop"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=loc)
    o = bpy.context.object; o.name = name; o.scale = scale; bpy.ops.object.transform_apply(scale=True)
    return add(o, mat, appear, kind, bevel=0.0001, lumps=0.03, sub=1)

def text(name, s, loc, size, mat, appear, depth=0.05):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = s; cu.size = size; cu.extrude = depth; cu.bevel_depth = 0.012
    cu.align_x = "CENTER"; cu.align_y = "CENTER"
    if FONT.exists(): cu.font = bpy.data.fonts.load(str(FONT))
    o = bpy.data.objects.new(name, cu); bpy.context.collection.objects.link(o)
    o.location = loc; o.rotation_euler = (math.radians(90), 0, 0)
    o.data.materials.append(MATS[mat])
    PIECES.append([o, o.location.copy(), o.rotation_euler.copy(), o.scale.copy(), appear, "drop"])
    return o

# set: tabletop, backdrop, hills, sun
box("table", (0, 0, -0.08), (12, 9, 0.12), "paper", -1, kind="static", bevel=0.02, lumps=0)
box("backdrop", (0, 4.2, 4.5), (14, 0.1, 10), "paper", -1, kind="static", bevel=0.02, lumps=0)
box("road", (0, -2.35, -0.0), (9, 1.3, 0.06), "slate", 0.2, kind="slide", bevel=0.02, lumps=0.006)
for i in range(6):
    box(f"dash{i}", (-3.1 + i * 1.25, -2.35, 0.04), (0.6, 0.1, 0.03), "brassL", 0.3 + 0.03 * i, bevel=0.01, lumps=0)
box("sidewalk", (0, -1.5, 0.01), (9, 0.4, 0.06), "white", 0.3, kind="slide", bevel=0.02, lumps=0.004)
box("lawn", (0, -0.35, 0.0), (9, 1.9, 0.07), "mossL", 0.4, kind="slide", bevel=0.03, lumps=0.01)
blob("hill_back", (-1.6, 2.2, 0), (3.2, 1.2, 1.3), "mossL", 0.1, kind="slide")
blob("hill_back2", (2.2, 2.6, 0), (3.4, 1.2, 1.7), "moss", 0.2, kind="slide")
blob("sun", (1.5, 3.9, 3.9), (0.55, 0.15, 0.55), "brass", 1.9, kind="slide")
blob("cloud", (-1.5, 3.8, 3.6), (0.6, 0.15, 0.25), "white", 2.2)

# the street
house("h1", -1.35, 1.0, 0.95, "parch", "slate", "moss", 0.9, chimney=True)
house("h2", 0.0, 1.1, 1.25, "brassL", "carbon", "brick", 1.3)
house("h3", 1.32, 0.95, 0.85, "white", "brick", "slate", 1.7, chimney=True)
tree("t1", -2.35, -0.1, 1.0, 2.1)
tree("t2", 2.3, -0.1, 0.85, 2.5)
for i, x in enumerate((-1.35, 0.0, 1.32)):
    box(f"path{i}", (x, -0.9, 0.05), (0.32, 0.95, 0.03), "paper", 2.7 + 0.06 * i, bevel=0.01, lumps=0.004)

# the SOLD sign hops onto the lawn
bpy.ops.mesh.primitive_cylinder_add(radius=0.025, depth=0.7, location=(0.75, -0.95, 0.35))
post = add(bpy.context.object, "brassD", 3.1, kind="hop", bevel=0.005, lumps=0)
board = box("board", (0.75, -0.97, 0.72), (0.62, 0.05, 0.28), "white", 3.1, kind="hop", bevel=0.02, lumps=0.003)
sold = text("sold", "SOLD", (0.75, -1.0, 0.71), 0.17, "ink", 3.1, depth=0.012)
PIECES[-1][5] = "hop"

# title
text("title1", "Find your street.", (0, 0.6, 3.0), 0.42, "ink", 4.0)

title = [p[0] for p in PIECES if p[0].name == "title1"][0]
title.data.materials.append(MATS["brassD"])
for i in range(5, 9): title.data.body_format[i].material_index = 1

# lights: warm key from the upper left (a window), cool soft fill, a little rim
def area(name, loc, rot, energy, size, col):
    l = bpy.data.lights.new(name, "AREA"); l.energy = energy; l.size = size; l.color = col
    o = bpy.data.objects.new(name, l); o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]
    bpy.context.collection.objects.link(o)
area("key", (-4.5, -4.5, 6.0), (45, 0, -45), 1600, 3.0, (1.0, 0.88, 0.72))
area("fill", (5, -5, 2.5), (70, 0, 45), 380, 6.0, (0.85, 0.9, 1.0))

# camera: close to the tabletop, a little above, shallow focus on the middle house
cam = bpy.data.cameras.new("cam"); cam.lens = 28; cam.sensor_fit = "VERTICAL"
cam.dof.use_dof = True; cam.dof.aperture_fstop = 1.6
co = bpy.data.objects.new("cam", cam); bpy.context.collection.objects.link(co); sc.camera = co
co.location = (0, -7.9, 2.3)
tgt = Vector((0, 0, 1.35)); co.rotation_euler = (tgt - co.location).to_track_quat("-Z", "Y").to_euler()
cam.dof.focus_distance = (Vector((0, 0, 0.6)) - co.location).length

# ---------- animation, on twos ----------
def spring(dt, w=15.0, z=0.42):
    if dt <= 0: return 0.0
    wd = w * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w * dt) * (math.cos(wd * dt) + z * w / wd * math.sin(wd * dt))

def pose(t, p):
    rnd = random.Random(p * 7919)
    for v in NOISES: v.inputs["W"].default_value = rnd.random() * 0.25   # surface re-touched each pose
    for o, loc, rot, scl, t0, kind in PIECES:
        o.location, o.rotation_euler, o.scale = loc.copy(), rot.copy(), scl.copy()
        if kind == "static": continue
        s = spring(t - t0)
        o.hide_render = s <= 0.001
        if o.hide_render: continue
        if kind == "pop":     # grows from its base like a lump being pushed up
            base = Vector((loc.x, loc.y, 0)); o.scale = scl * max(s, 0.001)
            o.location = base + (loc - base) * s
        elif kind == "popbase":  # grows up out of its own base (chimneys out of the roof)
            zmin = min(v.co.z for v in o.data.vertices)
            o.scale = scl * max(s, 0.001); o.location.z = loc.z + zmin * (1 - s)
        elif kind == "slide":  # slides in from below the table edge
            o.location.z = loc.z - (1 - s) * 2.5
        elif kind in ("drop", "hop"):
            o.location.z = loc.z + (1 - s) * (2.0 if kind == "drop" else 1.2)
            if kind == "hop":
                dt = t - t0; o.rotation_euler.y += math.exp(-3 * dt) * math.sin(dt * 14) * 0.12 if dt > 0 else 0
        # the boil: a hair of jitter per pose
        o.location += Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))) * 0.004
        o.rotation_euler.z += rnd.uniform(-1, 1) * 0.006

def render(t, p, out):
    pose(t, p); sc.render.filepath = str(out); bpy.ops.render.render(write_still=True)

if MODE == "stills":
    (HERE / "stills").mkdir(exist_ok=True)
    for t in [float(v) for v in ARGS[1].split(",")]:
        render(t, round(t * PPS), HERE / "stills" / f"clay_t{t:.2f}.png")
else:
    (HERE / "poses").mkdir(exist_ok=True)
    first, last = opt("--from", 0), opt("--to", int(DUR * PPS) - 1)
    for p in range(first, last + 1):
        out = HERE / "poses" / f"p{p:03d}.png"
        if not out.exists(): render(p / PPS, p, out)
