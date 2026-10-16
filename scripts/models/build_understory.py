"""Original cycad, fern and horsetail: deliberate, reproducible solid low-poly forms.

Build with Blender 4.3.2, from the cloud repository:
  blender -b -t 4 --python scripts/models/build_understory.py -- --asset all
Authored for Leon Made This / s010s; CC-BY-4.0. No imported geometry/textures.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys

import bpy
from mathutils import Vector

SCRIPT = Path(__file__).resolve()
REPO = SCRIPT.parents[2]
sys.path.insert(0, str(REPO / 'scripts'))
import asset_common as common

PALETTE = {
    'fern_deep': '#294C43', 'fern_mid': '#47745C', 'fern_light': '#719366',
    'dry_olive': '#A1A276', 'bark_deep': '#4F443D', 'bark_mid': '#79624B',
}
SEED = 20261016
AUTHORING = {
    'author': 'Leon Made This / s010s', 'license': 'CC-BY-4.0',
    'originality': {'en': 'Entirely original procedural mesh design; no third-party model, texture or palette assets.',
                    'zh': '全部为原创参数化几何；未使用第三方模型、纹理或下载色板。'},
    'scientific_scope': {'en': 'Evidence-informed stylized plant concept, not a taxon or site reconstruction.',
                         'zh': '有依据的风格化植物概念，并非具体物种或化石地点复原。'},
    'generator': 'scripts/models/build_understory.py',
    'modeling_runtime': 'GPT-6 Astra; xhigh; Blender 4.3.2; cloud only',
    'topology_notes': {'en': 'Leaves are closed folded blades with a slight ridge and real thickness. No alpha cards. Separate semantic fronds remain editable.',
                       'zh': '叶片均为具浅脊线与真实厚度的闭合折面实体；不使用透明贴片。语义分组叶片可分别编辑。'},
    'scale_note': {'en': 'Dimensions are artistic asset specifications in meters, not measured fossil dimensions.',
                   'zh': '米制尺寸为美术资产规格，不是化石测量值。'},
}


class MeshBuilder:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.material_indices = []

    def append(self, vertices, faces, mat=0):
        start = len(self.vertices)
        self.vertices.extend(tuple(v) for v in vertices)
        self.faces.extend(tuple(start + i for i in f) for f in faces)
        self.material_indices.extend([mat] * len(faces) if isinstance(mat, int) else mat)

    def finish(self, name, materials, collection):
        obj = common.mesh_object(name, self.vertices, self.faces, materials, collection)
        for face, index in zip(obj.data.polygons, self.material_indices):
            face.material_index = index
        return obj


def tube(builder, points, radii, sides=5, mat=0, bands=None, phase=0):
    """Closed section loft, with consistent parallel-like frames and optional bands."""
    pts = [Vector(p) for p in points]
    vertices = []
    reference = Vector((1, 0, 0))
    for k, (point, radius) in enumerate(zip(pts, radii)):
        tangent = (pts[min(k + 1, len(pts) - 1)] - pts[max(k - 1, 0)]).normalized()
        ref = reference if abs(tangent.dot(reference)) < .92 else Vector((0, 1, 0))
        u = tangent.cross(ref).normalized()
        v = tangent.cross(u).normalized()
        for j in range(sides):
            a = math.tau * j / sides + phase
            vertices.append(point + radius * (math.cos(a) * u + math.sin(a) * v))
    faces = [tuple(reversed(range(sides)))]
    indices = [mat]
    for k in range(len(pts) - 1):
        for j in range(sides):
            faces.append((k * sides + j, k * sides + (j + 1) % sides,
                          (k + 1) * sides + (j + 1) % sides, (k + 1) * sides + j))
            indices.append(bands[k] if bands else mat)
    faces.append(tuple((len(pts) - 1) * sides + j for j in range(sides)))
    indices.append(mat)
    builder.append(vertices, faces, indices)


def blade(builder, base, tip, width, fold, shape='lance', mat=0, twist=0):
    """A closed volume with a designed outline and two faceted ridge surfaces."""
    base, tip = Vector(base), Vector(tip)
    axis = tip - base
    side = axis.cross(Vector((0, 0, 1))).normalized()
    if side.length < .5:
        side = Vector((1, 0, 0))
    normal = side.cross(axis).normalized()
    side = side * math.cos(twist) + normal * math.sin(twist)
    normal = side.cross(axis).normalized()
    if shape == 'lance':
        outline = [base, base + axis * .38 + side * width,
                   tip, base + axis * .38 - side * width]
    elif shape == 'fern':
        outline = [base, base + axis * .23 + side * width,
                   base + axis * .40 + side * width * .52,
                   base + axis * .60 + side * width * .78, tip,
                   base + axis * .62 - side * width * .72,
                   base + axis * .42 - side * width * .44,
                   base + axis * .24 - side * width * .88]
    else:
        outline = [base, base + axis * .27 + side * width * .82,
                   base + axis * .60 + side * width,
                   tip, base + axis * .64 - side * width * .80,
                   base + axis * .25 - side * width * .74]
    n = len(outline)
    ridge = base + axis * .44
    verts = outline + [ridge + normal * fold, ridge - normal * max(.0014, fold * .35)]
    faces = []
    for j in range(n):
        faces += [(j, (j + 1) % n, n), ((j + 1) % n, j, n + 1)]
    builder.append(verts, faces, mat)


def materials(*names):
    return {n: common.make_material(n, PALETTE[n], roughness=.85) for n in names}


def metadata(slug, description, tags, sources, parameters, notes):
    return {
        **AUTHORING, 'description': description, 'tags': tags,
        'sources': sources, 'design_parameters': parameters,
        'reconstruction_notes': notes,
        'generator_sha256': hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        'seed': SEED, 'style': 'faceted-prehistoric-environments',
        'palette_srgb': {k: PALETTE[k] for k in parameters['palette']},
    }


def deliver(slug, title, collection, data, args):
    common.ground_asset(collection)
    output = common.export_asset(
        slug, title, 'plants', collection, metadata=data,
        render=not args.no_render, output_root=args.output_root,
        views=('hero', 'reversehero', 'front', 'side', 'rear', 'top'),
        max_triangles=2600, max_materials=5, max_primitives=24,
        resolution=args.resolution, samples=args.samples, diagnostics=not args.no_diagnostics)
    outdir = REPO / Path(output['glb']).parent
    (outdir / 'parameters.json').write_text(json.dumps(data['design_parameters'], ensure_ascii=False, indent=2) + '\n')
    print('UNDERSTORY_COMPLETE ' + json.dumps({'slug': slug, 'triangles': output['triangles'], 'glb': output['glb'], 'dimensions': output['dimensions']}, ensure_ascii=False))
    return output


def build_cycad(args):
    slug = 'cycad'
    col = common.setup_scene(slug, SEED)
    mats = materials('bark_mid', 'bark_deep', 'fern_deep', 'fern_mid', 'fern_light')
    trunk = MeshBuilder()
    tube(trunk, [(0, 0, 0), (.012, -.005, .09), (.025, .004, .23), (.020, .010, .42), (.025, .014, .50), (.018, .010, .565)],
         [.205, .18, .159, .143, .124, .11], sides=9)
    trunk.finish('Short stout caudex', mats['bark_mid'], col)
    scars = MeshBuilder()
    for row, (z, radius, count) in enumerate([(.13, .168, 7), (.29, .150, 7), (.45, .134, 6)]):
        for j in range(count):
            a = math.tau * (j + row * .37) / count
            radial = Vector((math.cos(a), math.sin(a), 0))
            side = Vector((-math.sin(a), math.cos(a), 0))
            center = Vector((.020, .008, z)) + radial * radius
            verts = [center + Vector((0, 0, -.060)), center + side * .036,
                     center + Vector((0, 0, .068)), center - side * .036,
                     center + radial * .013, center - radial * .015]
            faces = [(k, (k+1)%4, 4) for k in range(4)] + [((k+1)%4, k, 5) for k in range(4)]
            scars.append(verts, faces, [0, 0, 1, 0, 1, 1, 1, 1])
    scars.finish('Faceted persistent leaf bases', [mats['bark_mid'], mats['bark_deep']], col)
    rachises = MeshBuilder()
    # Six long lower leaves and three shorter, more erect crown leaves.
    fronds = [(16, 1.04, 1.12, .98, 'fern_mid'),
              (79, .96, 1.02, .88, 'fern_deep'),
              (146, 1.10, 1.21, 1.06, 'fern_mid'),
              (212, .92, 1.04, .91, 'fern_mid'),
              (276, 1.02, 1.18, 1.04, 'fern_deep'),
              (333, .97, 1.10, .96, 'fern_mid'),
              (43, .70, 1.28, .47, 'fern_light'),
              (176, .75, 1.19, .47, 'fern_light'),
              (297, .68, 1.23, .48, 'fern_mid')]
    for number, (angle, length, rise, bend, color) in enumerate(fronds):
        a = math.radians(angle)
        radial = Vector((math.cos(a), math.sin(a), 0))
        sideways = Vector((-math.sin(a), math.cos(a), 0))
        def path(t):
            return radial * (.045 + length * t) + sideways * (.055 * math.sin(math.pi * t) * (-1 if number % 2 else 1)) + Vector((.02, .01, .51 + rise * t - bend * t * t))
        ts = [0, .18, .40, .64, .84, 1.0]
        tube(rachises, [path(t) for t in ts], [.015, .014, .012, .009, .006, .002], sides=3)
        leaves = MeshBuilder()
        for j in range(9):
            t0 = .14 + j * .095
            for handed in [-1, 1]:
                t = t0 + (.016 if handed == 1 else 0)
                taper = math.sin(math.pi * (t - .06)) ** .72
                leaflet_length = (.25 if number < 6 else .205) * taper
                base = path(t)
                tip = base + sideways * handed * leaflet_length + radial * leaflet_length * .40 + Vector((0, 0, .030 - .055 * t + .006 * handed))
                blade(leaves, base, tip, .025 * taper, .0062, 'lance', twist=handed * .09)
        # Single narrow terminal spear closes the feather without a blunt edge.
        blade(leaves, path(.90), path(1.06), .019, .005, 'lance')
        leaves.finish(f'Rigid pinnate crown frond {number+1:02d}', mats[color], col)
    rachises.finish('Tapering stiff rachises', mats['fern_deep'], col)
    buds = MeshBuilder()
    for a, height in [(18, .88), (143, .95), (269, .83)]:
        a = math.radians(a)
        radial = Vector((math.cos(a), math.sin(a), 0))
        blade(buds, radial * .025 + Vector((.02, .01, .55)),
              radial * .10 + Vector((.02, .01, height)), .032, .012, 'lance')
    buds.finish('Three compact emerging crown spears', mats['fern_light'], col)
    data = metadata(slug,
        {'en': 'A short, armored caudex supporting two uneven tiers of stiff, tapered pinnate leaves.',
         'zh': '短粗叶基干上展开两层高低错落的硬挺羽状叶，叶轴与狭长小叶逐段收细。'},
        ['prehistoric', 'plants', 'cycad', 'mesozoic-concept', 'original', 'low-poly'],
        [{'title': 'Smithsonian: About Cycads', 'url': 'https://qrius.si.edu/taxonomy/term/11978'},
         {'title': 'NHM: How to grow a dinosaur garden', 'url': 'https://www.nhm.ac.uk/discover/how-to-grow-a-dinosaur-garden.html'}],
        {'palette': list(mats), 'frond_count': 9, 'lower_tier_fronds': 6, 'upper_tier_fronds': 3,
         'leaflet_pairs_per_frond': 9, 'emerging_crown_spears': 3, 'caudex_height_m': .565, 'seed': SEED,
         'silhouette_signature': 'stout patterned caudex; rigid radial feather crown; asymmetric two-tier negative spaces'},
        {'en': 'A cycad-inspired Mesozoic planting concept, not a palm and not a Bennettitalean identification. Leaf count, caudex proportions and color are stylized. No reproductive organ is asserted.',
         'zh': '苏铁形中生代植物概念，不是棕榈，也不据羽状叶判为本内苏铁。叶数、干形比例及颜色为风格化；未添加用于分类的生殖器官。'})
    return deliver(slug, {'en': 'Cycad rosette', 'zh': '苏铁形植株'}, col, data, args)


def build_fern(args):
    slug = 'fern-cluster'
    col = common.setup_scene(slug, SEED + 1)
    mats = materials('fern_deep', 'fern_mid', 'fern_light')
    crown = MeshBuilder()
    tube(crown, [(0, 0, 0), (0, 0, .027), (0, 0, .057)], [.108, .091, .042], sides=7)
    crown.finish('Low grounded rhizome crown', mats['fern_deep'], col)
    axes = MeshBuilder()
    # Long low outer arches, intermediate side fronds, and a taller rear fan.
    fronds = [(-80, .78, .48, 'fern_mid', -.04),
              (-27, .73, .57, 'fern_mid', .025),
              (37, .61, .79, 'fern_light', -.015),
              (88, .68, .71, 'fern_mid', .035),
              (146, .81, .59, 'fern_deep', -.02),
              (203, .72, .41, 'fern_mid', .02),
              (310, .61, .64, 'fern_light', .018)]
    for number, (angle, length, rise, color, sway) in enumerate(fronds):
        a = math.radians(angle)
        radial = Vector((math.cos(a), math.sin(a), 0))
        side = Vector((-math.sin(a), math.cos(a), 0))
        origin = radial * (.02 + (number % 3) * .012)
        def path(t):
            return origin + radial * length * t + side * (sway * math.sin(math.pi * t)) + Vector((0, 0, .025 + rise * (.86 * math.sin(math.pi * t) + .19 * t)))
        ts = [0, .14, .29, .45, .61, .77, .90, 1.02]
        tube(axes, [path(t) for t in ts], [.014, .013, .011, .009, .007, .005, .003, .0014], sides=3)
        pinnae = MeshBuilder()
        for j in range(7):
            t0 = .13 + j * .123
            for handed in [-1, 1]:
                t = t0 + (.028 if handed == 1 else 0)
                taper = (math.sin(math.pi * (t - .025))) ** .75
                pinnalength = (.226 if number in [0, 3, 4] else .202) * taper
                base = path(t)
                # Broad pinnae are slightly swept, then droop off the softer axis.
                tip = base + side * handed * pinnalength + radial * pinnalength * .36 + Vector((0, 0, -.035 * taper - .018 * t))
                blade(pinnae, base, tip, .045 * taper, .0085 * taper, 'fern', twist=handed * (.13 + .1 * t))
        blade(pinnae, path(.92), path(1.04), .012, .004, 'lance')
        pinnae.finish(f'Arching fern frond {number+1:02d}', mats[color], col)
    axes.finish('Flexible tapering petioles and rachises', mats['fern_deep'], col)
    # A deliberately exposed young crozier at the front-left, with one readable roll.
    crozier = MeshBuilder()
    center = Vector((-.22, -.18, .46))
    side = Vector((1, 0, 0))
    points = [Vector((-.08, -.10, .008)), Vector((-.15, -.14, .20))]
    radii = [.018, .016]
    for j in range(15):
        theta = -math.pi / 2 + j * (math.tau * 1.05 / 14)
        radius = .078 * (1 - j / 18)
        points.append(center + side * (math.cos(theta) * radius) + Vector((0, 0, math.sin(theta) * radius)))
        radii.append(.014 - .008 * j / 14)
    tube(crozier, points, radii, sides=4)
    crozier.finish('Unfurling crozier', mats['fern_light'], col)
    shoots = MeshBuilder()
    for j, handed in enumerate([-1, 1, -1]):
        z = .27 + j * .037
        fraction = (z - .20) / (.382 - .20)
        base = Vector((-.15 - .07 * fraction, -.14 - .04 * fraction, z))
        blade(shoots, base, base + Vector((handed * (.045 - j*.005), -.018, .045)), .014, .004, 'young')
    shoots.finish('Small young pinnae below crozier', mats['fern_light'], col)
    data = metadata(slug,
        {'en': 'Seven soft arching fronds with staggered, folded pinnae and an exposed young fiddlehead.',
         'zh': '七片柔曲拱形叶轴带交错宽羽片，近地叶丛外缘下垂，并保留一片清楚的新卷芽。'},
        ['prehistoric', 'plants', 'fern', 'groundcover', 'mesozoic-concept', 'original', 'low-poly'],
        [{'title': 'NHM: Unfurl the secrets of ferns', 'url': 'https://www.nhm.ac.uk/discover/ferns.html'}],
        {'palette': list(mats), 'frond_count': 7, 'pinna_pairs_per_frond': 7, 'crozier_count': 1,
         'seed': SEED + 1, 'silhouette_signature': 'ground-level crown; three frond heights; bowed drooping pinnae; one unfurling crozier'},
        {'en': 'A generalized Mesozoic fern-form concept. The simplified pinnae, growth stage and color are artistic choices; it is not an identification of a living fern species, seed fern, or fossil specimen. Reproduces no flowers or seed clusters.',
         'zh': '宽泛的中生代蕨形概念。简化羽片、生长阶段及配色为美术选择；不是现生蕨种、种子蕨或某件化石标本的鉴定。不制作花或种子串。'})
    return deliver(slug, {'en': 'Ground fern cluster', 'zh': '地被蕨丛'}, col, data, args)


def build_horsetail(args):
    slug = 'horsetail-cluster'
    col = common.setup_scene(slug, SEED + 2)
    mats = materials('fern_deep', 'fern_mid', 'fern_light', 'dry_olive')
    stems = MeshBuilder()
    branches = {'fern_mid': MeshBuilder(), 'fern_light': MeshBuilder()}
    cones = MeshBuilder()
    # Lean, height, whorl count and spacing vary structurally, not with random noise.
    specs = [(-.18, .08, 1.48, -.045, .030, 4, False),
             (.13, .14, 1.27, .055, .015, 4, False),
             (.28, -.10, .95, .070, -.018, 3, False),
             (-.22, -.19, 1.04, -.035, -.035, 3, False),
             (.02, -.23, .77, .015, -.045, 2, False),
             (-.04, .24, 1.36, -.012, .025, 0, True),
             (.33, .13, .64, .040, .020, 0, True)]
    for index, (x, y, height, leanx, leany, whorls, cone) in enumerate(specs):
        r = .023 if height > 1.2 else .019
        def pos(t):
            return Vector((x + leanx * t * t, y + leany * t, height * t))
        # The expanded dark node sheaths are part of the solid stem mesh.
        ts, radii, bands = [0], [r * 1.05], []
        for node in [.17, .36, .56, .76]:
            ts += [node, node + .017]
            radii += [r * (1.15 - node*.23), r * (1.15 - node*.23)]
            bands += [0, 1]
        ts += [.96, 1.0]
        radii += [r*.58, r*.35]
        bands += [0, 0]
        tube(stems, [pos(t) for t in ts], radii, sides=5, bands=bands, phase=index*.17)
        if whorls:
            levels = [.19, .38, .58, .78][:whorls]
            for level_index, t in enumerate(levels):
                count = 5 if index < 2 else 4
                length = (.27 if index < 2 else .23) * (1 - .45 * t) * (.89 if index == 4 else 1)
                for j in range(count):
                    a = math.tau * j / count + index*.55 + level_index*.31
                    direction = Vector((math.cos(a), math.sin(a), 0))
                    base = pos(t)
                    mid = base + direction * length*.64 + Vector((0, 0, length*.20))
                    tip = base + direction * length + Vector((0, 0, length*.60))
                    color = 'fern_light' if level_index == whorls-1 else 'fern_mid'
                    tube(branches[color], [base, mid, tip], [.0095, .0065, .0016], sides=3, phase=a)
        if cone:
            top = pos(1)
            tube(cones, [top, top+Vector((0, 0, .023)), top+Vector((0, 0, .080)), top+Vector((0, 0, .108))],
                 [.014, .034, .026, .004], sides=6)
    stems.finish('Seven jointed upright stems with dark node sheaths', [mats['fern_mid'], mats['fern_deep']], col)
    branches['fern_mid'].finish('Lower open whorls of slender branches', mats['fern_mid'], col)
    branches['fern_light'].finish('Younger upper whorls', mats['fern_light'], col)
    cones.finish('Two quiet terminal spore cones', mats['dry_olive'], col)
    data = metadata(slug,
        {'en': 'Seven unequal jointed stems with dark node sheaths, tiered slender branch whorls, and two unbranched cone-bearing shoots.',
         'zh': '七根高低不一的分节立茎，节鞘清晰；细侧枝分层轮生，另有两根少枝顶穗茎。'},
        ['prehistoric', 'plants', 'horsetail', 'sphenopsid', 'wet-margin', 'mesozoic-concept', 'original', 'low-poly'],
        [{'title': 'NHM: Go on a Jurassic scavenger hunt', 'url': 'https://www.nhm.ac.uk/discover/jurassic-scavenger-hunt.html'},
         {'title': 'Smithsonian: The Age of Oxygen', 'url': 'https://forces.si.edu/atmosphere/02_02_06.html'}],
        {'palette': list(mats), 'stem_count': 7, 'branched_stems': 5, 'unbranched_fertile_shoots': 2,
         'node_levels_per_stem': 4, 'stem_heights_m': [s[2] for s in specs], 'seed': SEED + 2,
         'silhouette_signature': 'upright segmented stems; sparse and dense groups; tiered threadlike branch whorls'},
        {'en': 'A small horsetail-form concept appropriate to a stylized Mesozoic wet margin. It is not bamboo or a Carboniferous Calamites tree. Size, density, branch count, cones and colors are simplified artistic choices, not a fossil-locality reconstruction.',
         'zh': '适用于风格化中生代湿润岸边的小型木贼形概念；不是竹子，也不能放大冒称石炭纪芦木。尺寸、疏密、枝数、顶穗与颜色为艺术简化，不代表某层位复原。'})
    return deliver(slug, {'en': 'Jointed horsetail cluster', 'zh': '木贼群落'}, col, data, args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset', choices=['all', 'cycad', 'fern-cluster', 'horsetail-cluster'], default='all')
    parser.add_argument('--resolution', type=int, default=1024)
    parser.add_argument('--samples', type=int, default=24)
    parser.add_argument('--no-render', action='store_true')
    parser.add_argument('--no-diagnostics', action='store_true')
    parser.add_argument('--output-root', default=None, help='Alternate output parent for independent reproducibility tests.')
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    builds = {'cycad': build_cycad, 'fern-cluster': build_fern, 'horsetail-cluster': build_horsetail}
    for slug, build in builds.items():
        if args.asset in ['all', slug]:
            build(args)


if __name__ == '__main__':
    main()
