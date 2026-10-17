# SPDX-License-Identifier: MIT
"""Build original static Bothriolepis and Waptia environment props.

Run Blender 4.3.2 headless, e.g.:
blender -b -t 2 --python-exit-code 1 --python scripts/models/small_fauna/build_aquatic_pair.py -- --config path/build-config.json
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, export_asset, render_previews
from aquatic_pair_geometry import Shape, loft_y


def bothriolepis(collection,mats):
    armor,accent,soft,eye=mats
    # Cross sections describe a deep, vaulted armor, with a steeply inclined
    # cephalic face and highest median crest toward the posterior.
    # Units here are meters before the common mounting-origin translation.
    sections=[(-.156,.027,.008,.016,.026),(-.146,.039,.007,.025,.046),
              (-.116,.051,.007,.041,.068),(-.079,.052,.007,.048,.074),
              (-.037,.041,.009,.048,.079),(-.001,.025,.012,.041,.066)]
    # Ten points around each ring: shoulders are broad angular planes; the
    # dorsal median ridge is intentional and does not become a separate fin.
    vertices=[]
    for y,w,b,shoulder,top in sections:
        vertices += [(0,y,top),(w*.58,y,top-.009),(w,y,shoulder),
                     (w*.92,y,b+.009),(w*.56,y,b),(0,y,b),
                     (-w*.56,y,b),(-w*.92,y,b+.009),(-w,y,shoulder),(-w*.58,y,top-.009)]
    faces=[tuple(range(9,-1,-1))]; indices=[0]
    for i in range(len(sections)-1):
        for j in range(10):
            faces.append((i*10+j,i*10+(j+1)%10,(i+1)*10+(j+1)%10,(i+1)*10+j))
            indices.append(1 if (j in (3,4,5,6) or (i==0 and j in (0,1,8,9))) else 0)
    faces.append(tuple((len(sections)-1)*10+j for j in range(10))); indices.append(0)
    armorobj=mesh_object('vaulted-cephalic-and-trunk-armor',vertices,faces,[armor,accent],collection)
    for face,i in zip(armorobj.data.polygons,indices): face.material_index=i
    # Long, scale-less tapering posterior body, 64% of whole body length.
    body_sections=[(-.008,0,.036,.024,.028),(.018,.001,.035,.024,.027),
                   (.058,.003,.031,.021,.024),(.105,.006,.025,.015,.018),
                   (.155,.012,.024,.0095,.012),(.202,.014,.031,.006,.008),
                   (.251,.01,.037,.0035,.0045),(.284,.004,.034,.0012,.0015)]
    body=loft_y(body_sections,12)
    body.object('long-soft-posterior-body',collection,soft)
    # One dorsal fin around the mid-body, and an asymmetrical caudal web.
    fins=Shape()
    fins.side_fin([(.073,.043),(.078,.071),(.089,.086),(.105,.087),(.117,.078),(.121,.040)],.0012)
    fins.side_fin([(.145,.022),(.178,.015),(.203,.001),(.231,-.003),(.250,.003),(.267,.015),(.280,.032),(.256,.034),(.210,.028),(.174,.028)],.001)
    fins.object('single-dorsal-and-caudal-web',collection,soft)
    # One pair of retracted armored pectorals. Two tapered pieces on each
    # side make proximal/distal articulation legible without a moving joint.
    p=Shape()
    for s in (-1,1):
        p.tube([(s*.041,-.122,.019),(s*.055,-.103,.018),(s*.056,-.068,.023),(s*.052,-.036,.031)],
               [.008,.010,.008,.0058],sides=6,material=0,flatten=.66)
        p.tube([(s*.052,-.038,.031),(s*.052,-.029,.033),(s*.047,.006,.042),(s*.041,.018,.046)],
               [.0058,.0056,.0031,.00085],sides=6,material=1,flatten=.68)
    p.object('paired-articulated-pectoral-armor',collection,[armor,accent])
    # Eyes small and dorsally placed, within a pale integrated orbital panel.
    eyes=Shape()
    for s in (-1,1):
        eyes.ellipsoid((s*.0086,-.137,.050),(.0033,.0026,.0022),segments=10,rings=4)
    eyes.object('paired-dorsal-eyes',collection,eye)
    # Subtle plate boundaries are broad-form design cues, not a claim to an
    # exact plate atlas. Short strips sit on the fitted surface, no random noise.
    sutures=Shape()
    for s in (-1,1):
        sutures.tube([(s*.009,-.116,.0664),(s*.029,-.116,.059),(s*.0506,-.116,.041)],
                     [.00040,.00040,.00040],sides=4)
        sutures.tube([(0,-.060,.0763),(s*.026,-.074,.064),(s*.051,-.079,.048)],
                     [.00035,.00035,.00035],sides=4)
    sutures.object('restrained-armor-plate-boundaries',collection,accent)


def waptia(collection,mats):
    shell,rim,limb,eye=mats
    # An 80-mm body (front head to tips of paired caudal rami), with antennules
    # extending beyond the anatomical length. The posterior is gently curved.
    body_sections=[(-.032,0,.005,.0045,.004),(-.023,0,.005,.006,.005),
                   (-.011,0,.004,.0062,.0055),(.001,0,.003,.0058,.005),
                   (.010,.0002,.002,.0046,.004),(.018,.0004,.0005,.004,.0035),
                   (.026,.0007,-.0012,.0035,.003),(.033,.001,-.0035,.0028,.0025),
                   (.039,.001,-.006,.0022,.002)]
    body=loft_y(body_sections,10)
    # Six broad annular rings remain visible beyond the carapace; a thin
    # reduced-diameter underlying abdomen joins them, rather than loose beads.
    for i,(y,cx,cz,rx,rz) in enumerate(body_sections[4:]):
        ring=loft_y([(y-.0014,cx,cz,rx*1.04,rz*1.04),(y-.0006,cx,cz,rx*1.13,rz*1.13),(y+.0011,cx,cz,rx*1.02,rz*1.02)],10)
        body.add(ring.vertices,ring.faces,1)
    body.object('ringed-body-and-limbless-abdomen',collection,[shell,rim])
    # Two separate thin convex valves attached dorsally. Each side is a closed
    # solid shell sheet, not an opaque filled ellipsoid hiding the limbs.
    valves=Shape()
    # Border travels from the anterior dorsal edge around the ventral margin
    # to the posterior hinge, in a side-oriented Y/Z profile.
    boundary=[(-.031,.010),(-.033,.006),(-.029,-.002),(-.021,-.005),
              (-.010,-.005),(-.001,-.001),(.004,.006),(.001,.012),(-.009,.016),(-.022,.016)]
    for s in (-1,1):
        n=len(boundary); verts=[]
        cy=-.014; cz=.006
        for f,offset in [(1,0),(.53,0),(0,.001)]:
            if f==0: continue
            for y,z in boundary:
                # Maximum lateral bulge in the middle, narrowed at hinge.
                x=s*(.0035 if f==1 else .0108)
                if f==1 and z>.011: x=s*.0012
                verts.append((x,cy+(y-cy)*f,cz+(z-cz)*f))
        verts.append((s*.012,cy,cz+.0003)); center=2*n
        faces=[]; mids=[]
        for j in range(n):
            faces.append((j,(j+1)%n,n+(j+1)%n,n+j)); mids.append(0)
            faces.append((n+j,n+(j+1)%n,center)); mids.append(0)
        # Thin inward return is fully closed along the perimeter.
        original=list(verts); offset=len(verts)
        verts.extend((x-s*.00038,y,z) for x,y,z in original)
        faces.extend(tuple(offset+i for i in reversed(f)) for f in list(faces)); mids.extend(list(mids))
        for j in range(n):
            faces.append((j,offset+j,offset+(j+1)%n,(j+1)%n)); mids.append(1)
        base=len(valves.faces); valves.add(verts,faces); valves.material_indices[base:]=mids
    valves.object('paired-bivalved-carapace',collection,[shell,rim])
    # Deliberately separated appendages: three anterior grasping pairs, one
    # transitional pair and six broad lamellar pairs. Fine setae are omitted.
    limbs=Shape()
    for s in (-1,1):
        for i,y in enumerate([-.027,-.023,-.019]):
            z=.001-i*.0004
            limbs.tube([(s*.004,y,z),(s*.007,y-.001,-.007),(s*.010,y-.005,-.011),(s*.008,y-.010,-.009)],
                       [.00085,.0007,.00055,.00028],sides=5)
        limbs.tube([(s*.005,-.014,0),(s*.008,-.012,-.006),(s*.011,-.015,-.010)],
                   [.001,.00085,.00035],sides=5)
        for i,y in enumerate([-.012,-.008,-.004,0,.004,.008]):
            # Sequential fans are connected to the anterior limb-bearing trunk,
            # not to the later limbless abdominal rings.
            reach=.009+(.0015 if i in (2,3) else 0)
            outline=[(s*.004,y,.000),(s*.008,y-.001,-.004),
                     (s*(.006+reach),y+.001,-.0105+i*.0004),
                     (s*(.005+reach),y+.004,-.010+i*.0004),
                     (s*.007,y+.003,-.003)]
            limbs.plate(outline,.00048,ridge=(s*.010,y+.001,-.003))
        # The two terminal caudal rami remain visibly split.
        limbs.plate([(s*.0006+.001,.037,-.0055),(s*.0045+.001,.039,-.0068),
                     (s*.008+.001,.045,-.009),(s*.006+.001,.048,-.0095),
                     (s*.0018+.001,.046,-.0082)],.00055,
                    ridge=(s*.0038+.001,.043,-.0069))
    limbs.object('separated-lamellar-appendages-and-paired-caudal-rami',collection,limb)
    antennae=Shape()
    for s in (-1,1):
        antennae.tube([(s*.0034,-.031,.003),(s*.007,-.039,.003),(s*.009,-.047,.004),
                       (s*.011,-.056,.005),(s*.014,-.062,.007)],
                      [.0007,.00058,.00044,.00032,.00019],sides=5)
        antennae.tube([(s*.004,-.030,.006),(s*.008,-.034,.010),(s*.010,-.035,.011)],
                      [.0009,.00085,.0008],sides=6)
    antennae.object('paired-antennules-and-eye-peduncles',collection,rim)
    eyes=Shape()
    for s in (-1,1):
        eyes.ellipsoid((s*.010,-.035,.011),(.0022,.002,.002),segments=10,rings=5)
    eyes.object('paired-stalked-eyes',collection,eye)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--config',type=Path,required=True)
    ap.add_argument('--output-root',type=Path); ap.add_argument('--no-render',action='store_true')
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    config=json.loads(args.config.read_text()); slug=config['asset_id']
    output_root=(args.output_root or ROOT/'assets'/'prehistoric'/'fauna').resolve()
    collection=setup_scene(slug,config['seed'])
    materials=[make_material(p['name'],p['srgb'],roughness=p['roughness']) for p in config['materials']]
    {'bothriolepis':bothriolepis,'waptia':waptia}[slug](collection,materials)
    # A non-grounded static aquatic prop uses an explicit center mounting pivot.
    # Translation is baked into vertices, leaving identity root and object scale.
    mount=Vector(config['mount_origin_authoring_m'])
    for obj in collection.objects:
        if obj.type=='MESH':
            for v in obj.data.vertices: v.co-=mount
    root=bpy.data.objects[collection['asset_root']]
    root['mounting_contract']='Suspended aquatic prop; body-center pivot, not ground contact'
    root['static_asset']=True
    root['animation_ready']=False
    scene=bpy.context.scene; scene.render.threads_mode='FIXED'; scene.render.threads=2
    metadata={
      'name_zh':config['name_zh'], 'description':config['description'],
      'representation':'artistic interpretation, evidence-informed static environment prop',
      'quality_tier':'environment-prop','static_asset':True,'animated':False,'rigged':False,
      'generator':'scripts/models/small_fauna/build_aquatic_pair.py',
      'generator_helper':'scripts/models/small_fauna/aquatic_pair_geometry.py',
      'config':f'assets/prehistoric/fauna/{slug}/build-config.json',
      'config_sha256':hashlib.sha256(args.config.read_bytes()).hexdigest(),
      'sources':config['sources'],'reconstruction_notes':config['reconstruction_notes'],
      'nominal_body_length_m':config['nominal_body_length_m'],
      'mounting_origin':{'type':'body-center suspended mount','authoring_offset_m':list(mount)},
      'surface_profile':'original quiet region-based palette; no external textures or copied geometry',
      'creation_provenance':{'geometry':'Original procedural profile and hand-designed topology','textures':'None','third_party_components':'None'},
      'runtime_profile':{'three_version':'0.180.0','glTF':'2.0 static, uncompressed, opaque palette'},
      'delivery_status':'candidate; independent acceptance pending'}
    record=export_asset(slug,{'en':config['name_en'],'zh':config['name_zh']},'fauna',collection,metadata,
        output_root=output_root,render=False,max_triangles=12000,max_materials=4,max_primitives=8)
    out=output_root/slug
    # A transparent source thumbnail is helpful early; exact export evidence is
    # generated separately by a clean GLB import and hash-bound view manifest.
    if not args.no_render:
        render_previews(collection,out,views=('hero',),resolution=768,samples=24,transparent=True)
    print('ASSET_RESULT '+json.dumps({'asset_id':slug,'triangles':record['triangles'],'bytes':record['glb_bytes'],'sha256':record['sha256']}))

if __name__=='__main__': main()
