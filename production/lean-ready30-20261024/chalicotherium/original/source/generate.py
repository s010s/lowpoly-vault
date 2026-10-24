# SPDX-License-Identifier: MIT
"""Deterministic original Chalicotherium reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output-dir .
Reference images are not runtime inputs and are never embedded in the asset.
"""
from pathlib import Path
import argparse, json, math, sys, shutil, hashlib
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset


def shell(name, sections, material, col, n=16, stagger=False):
    """Loft along Y; each section is y, z, width, upper-radius, lower-radius."""
    vv=[];ff=[]
    for j,(y,z,w,up,down) in enumerate(sections):
        for i in range(n):
            a=2*math.pi*i/n
            vv.append((w*math.cos(a),y,z+(up if math.sin(a)>=0 else down)*math.sin(a)))
    for j in range(len(sections)-1):
        for i in range(n):
            a=j*n+i;b=j*n+(i+1)%n;c=(j+1)*n+(i+1)%n;d=(j+1)*n+i
            if (i+j)%2: ff.extend([(a,b,d),(b,c,d)])
            else: ff.extend([(a,b,c),(a,c,d)])
    ff.append(tuple(reversed(range(n))));ff.append(tuple((len(sections)-1)*n+i for i in range(n)))
    return mesh_object(name,vv,ff,material,col)


def tubes(name, paths, material, col, n=12):
    """Closed custom tapered tubes, independent positive world-coordinate meshes."""
    vv=[];ff=[]
    for path in paths:
        base=len(vv);length=len(path)
        for j,(point,rx,ry) in enumerate(path):
            p=Vector(point)
            tangent=Vector(path[min(j+1,length-1)][0])-Vector(path[max(j-1,0)][0]);tangent.normalize()
            across=Vector((1,0,0));across=across-tangent*across.dot(tangent)
            if across.length<.01: across=Vector((0,1,0));across=across-tangent*across.dot(tangent)
            across.normalize();other=tangent.cross(across).normalized()
            for i in range(n):
                a=2*math.pi*i/n;vv.append(tuple(p+across*(rx*math.cos(a))+other*(ry*math.sin(a))))
        for j in range(length-1):
            for i in range(n):
                a=base+j*n+i;b=base+j*n+(i+1)%n;c=base+(j+1)*n+(i+1)%n;d=base+(j+1)*n+i
                if (i+j)%2:ff.extend([(a,b,d),(b,c,d)])
                else:ff.extend([(a,b,c),(a,c,d)])
        ff.append(tuple(base+i for i in reversed(range(n))))
        ff.append(tuple(base+(length-1)*n+i for i in range(n)))
    return mesh_object(name,vv,ff,material,col)


def scale_translate(obj,offset=(0,0,0)):
    for v in obj.data.vertices:v.co+=Vector(offset)
    return obj


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,default=HERE.parent);p.add_argument('--params',type=Path,default=HERE/'params.json');p.add_argument('--gray',action='store_true');a=p.parse_args(argv)
    config=json.loads(a.params.read_text());out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    col=setup_scene(config['asset_id'],config['seed'])
    mats={k:make_material(k,'#929292' if a.gray else v) for k,v in config['palette'].items()}
    coat=mats['coat'];shadow=mats['shadow_coat'];muzzle=mats['muzzle'];claw=mats['claw'];eye=mats['eye'];inner=mats['inner_ear']
    # High withers slope down toward the short-backed low hindquarters.
    torso=shell('sloping-barrel-torso',[
      (-.90,1.65,.20,.30,.29),(-.77,1.66,.36,.44,.38),(-.56,1.58,.46,.51,.49),
      (-.30,1.48,.50,.52,.54),(0,1.39,.52,.50,.51),(.31,1.34,.48,.47,.43),
      (.58,1.30,.40,.41,.36),(.79,1.25,.33,.34,.30),(.96,1.21,.22,.24,.21),(1.03,1.20,.10,.12,.11)],coat,col,20)
    # Dorsal facets gently darken, without a painted patch floating above the skin.
    torso.data.materials.append(shadow)
    for poly in torso.data.polygons:
        center=sum((torso.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices)
        if center.z>1.88 and center.y<.05:poly.material_index=1
    tubes('short-upright-neck',[[((0,-.70,1.74),.33,.34),((0,-.87,1.96),.28,.30),((0,-1.00,2.13),.24,.26),((0,-1.13,2.22),.20,.23)]],coat,col,16)
    # Horse-like elongate face, forehead and narrowing long mandible. No primate mask.
    shell('elongate-cranium-and-face',[
      (-.98,2.22,.14,.19,.15),(-1.10,2.26,.23,.25,.18),(-1.26,2.23,.24,.23,.19),
      (-1.42,2.15,.20,.18,.17),(-1.61,2.03,.16,.145,.13),(-1.77,1.94,.15,.12,.115),(-1.87,1.92,.12,.09,.08)],coat,col,16)
    shell('long-mandibular-body',[
      (-1.05,2.12,.14,.08,.12),(-1.21,2.11,.20,.09,.135),(-1.40,2.04,.17,.08,.12),(-1.60,1.94,.13,.07,.09),(-1.79,1.86,.115,.06,.055)],shadow,col,12)
    shell('soft-nasal-muzzle',[
      (-1.70,1.94,.145,.11,.09),(-1.81,1.91,.16,.115,.10),(-1.91,1.90,.135,.085,.075)],muzzle,col,16)
    # Restrained mouth seam follows the jaw, not a toothy or aggressive face.
    tubes('mouth-seam',[[((s*.143,-1.80,1.85),.009,.008),((s*.153,-1.70,1.875),.010,.009),((s*.168,-1.57,1.94),.007,.007)] for s in (-1,1)],claw,col,8)
    for s,label in [(-1,'left'),(1,'right')]:
        # Elongate pinnae, small and intentionally reconstructed.
        tubes(label+'-ear',[[((s*.17,-1.08,2.40),.075,.058),((s*.23,-1.01,2.51),.070,.042),((s*.25,-.99,2.61),.032,.021),((s*.25,-1.0,2.64),.007,.007)]],coat,col,10)
        tubes(label+'-ear-inner',[[((s*.18,-1.135,2.43),.041,.014),((s*.23,-1.055,2.52),.037,.010),((s*.245,-1.027,2.59),.012,.005)]],inner,col,8)
        # Eye and nostril are low-relief closed meshes, separate from the large facial planes.
        tubes(label+'-eye',[[((s*.218,-1.275,2.30),.017,.025),((s*.244,-1.275,2.30),.024,.026),((s*.249,-1.275,2.30),.013,.016)]],eye,col,10)
        tubes(label+'-nostril',[[((s*.131,-1.835,1.945),.016,.025),((s*.149,-1.835,1.945),.021,.026),((s*.153,-1.835,1.945),.012,.019)]],eye,col,10)
        # Long upper arms and exceptionally long forearms. Discrete joints, not a crouch illusion.
        tubes(label+'-powerful-forelimb',[[((s*.28,-.64,1.79),.10,.15),((s*.37,-.63,1.79),.175,.20),((s*.46,-.63,1.65),.19,.22),((s*.49,-.59,1.36),.15,.18),((s*.48,-.55,1.12),.15,.17),((s*.475,-.65,.91),.13,.15),((s*.47,-.77,.63),.115,.13),((s*.465,-.87,.35),.095,.105),((s*.465,-.89,.22),.11,.12)]],coat,col,14)
        # Curl digits below the wrist. Knuckles, not hoof capsules, meet the floor.
        fingers=[];claws=[]
        for i in (-1,0,1):
            x=s*.465+i*.102;y=-.92+(abs(i)*.015)
            fingers.append([((x,y,.27),.054,.070),((x,y-.035,.17),.063,.070),((x,y-.025,.09),.065,.070),((x,y+.05,.075),.060,.070),((x,y+.11,.105),.049,.045)])
            claws.append([((x,y+.09,.105),.049,.043),((x,y+.17,.09),.044,.037),((x,y+.235,.13),.032,.030),((x,y+.27,.19),.018,.018),((x,y+.255,.235),.0035,.004)])
        tubes(label+'-curled-knuckle-digits',fingers,shadow,col,10)
        tubes(label+'-recurved-foreclaws',claws,claw,col,10)
        # Short hindlimbs, with thick thighs and abbreviated lower legs.
        tubes(label+'-short-hindlimb',[[((s*.30,.66,1.35),.23,.27),((s*.37,.73,1.15),.22,.25),((s*.40,.80,.94),.17,.20),((s*.41,.73,.72),.13,.15),((s*.41,.86,.50),.10,.12),((s*.405,.96,.29),.095,.10),((s*.405,.86,.15),.105,.13)]],coat,col,14)
        toes=[];nails=[]
        for i in (-1,0,1):
            x=s*.405+i*.09;y=.73+abs(i)*.025
            toes.append([((x,.88,.17),.055,.06),((x,y+.06,.09),.060,.065),((x,y-.01,.065),.060,.055),((x,y-.09,.065),.048,.042)])
            nails.append([((x,y-.07,.07),.049,.037),((x,y-.14,.055),.039,.028),((x,y-.185,.045),.006,.006)])
        tubes(label+'-three-hind-toes',toes,shadow,col,10)
        tubes(label+'-hind-claws',nails,claw,col,10)
    tubes('short-tapered-tail',[[((0,.93,1.32),.105,.11),((0,1.11,1.24),.080,.08),((0,1.25,1.10),.055,.06),((0,1.30,.96),.035,.04),((0,1.28,.88),.012,.015)]],coat,col,12)
    # Bake the frozen artistic body envelope into the authored meters.
    for obj in col.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices:
                v.co.x*=config['baked_axis_scale'][0];v.co.y*=config['baked_axis_scale'][1];v.co.z*=config['baked_axis_scale'][2]
    # Shift all geometry to exact ground without changing the identity root.
    low=min(v.co.z for obj in col.all_objects if obj.type=='MESH' for v in obj.data.vertices)
    for obj in col.all_objects:
        if obj.type=='MESH':
            for v in obj.data.vertices:v.co.z-=low
    bpy.context.scene['reconstruction_scope']='Genus-level original living stylization. Dimensions, soft tissue, claw sheaths and pose are estimates.'
    bpy.context.scene['reference_policy']='Jaw photo and interpretive skeletal illustration; no whole skeleton photo claimed.'
    # Remove default local UI and render-output paths before saving portable source.
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
    stage=out/'_export'
    record=export_asset(config['asset_id'],{'en':'Chalicotherium','zh':'爪兽'},'mammals',col,
        metadata={'description':{'en':'Original genus-level living reconstruction of the long-armed claw-bearing perissodactyl.','zh':'长前肢、具爪奇蹄类的原创属级活体复建。'},'export_texcoords':False},
        output_root=stage,render=False,diagnostics=False,max_triangles=config['max_triangles'],max_materials=config['max_materials'],max_primitives=config['max_primitives'])
    built=stage/config['asset_id']
    for ext in ('glb','blend'):shutil.move(str(built/(config['asset_id']+'.'+ext)),out/('model.'+ext))
    raw=json.loads((built/'qa.json').read_text())
    summary={'check':'generation-and-static-geometry','status':'PASS' if not raw['source']['errors'] and not raw['glb']['errors'] else 'FAIL','blender_version':bpy.app.version_string,'source':raw['source'],'glb':raw['glb'],'bounds_roundtrip_max_error_m':raw['bounds_roundtrip_max_error_m'],'export_options':record['export_options'],'limitations':'Static source/export structure only; no GPU, populated scene, visual or scientific acceptance.'}
    # Canonical audit stores input pathname; public evidence uses fixed package-relative names.
    summary['glb']['path']='model.glb'
    (out/'geometry.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
    if (out/'model.glb').stat().st_size>config['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    shutil.rmtree(stage)
    print('BUILT',out/'model.glb')

if __name__=='__main__':main()
