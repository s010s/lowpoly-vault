# SPDX-License-Identifier: MIT
"""Deterministic original Hippurites shell reconstruction. Blender 4.3.2.
Usage: blender -b --threads 2 --python source/generate.py -- --out OUTPUT [--render] [--clay]
Only source/params.json and bundled source/deps/*.py are required. No images/mesh input.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import bpy, bmesh
from asset_common import setup_scene, make_material, mesh_object, export_asset
from render_four import render_four

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d): p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def circ_delta(a,b): return math.atan2(math.sin(a-b),math.cos(a-b))
def build(p):
    c=setup_scene(p['asset_id'],p['seed']); n=p['radial_segments']; bodytop=.2052
    mats={k:make_material('Chalky '+k,color,.91) for k,color in p['palette'].items()}
    # A subtly curved centerline, basal footprint origin unchanged.
    def center(t): return (.0045*math.sin(t*math.pi*.78), -.003*math.sin(t*math.pi*.66))
    def scalar(z,a):
        t=z/bodytop
        # Abraded narrow base, expanding low third, increasingly cylindrical upper valve.
        shape=.225+.775*(1-(1-t)**1.48)
        rib=(.021*math.cos(p['longitudinal_ribs']*a+.25*math.sin(t*3.1))+.007*math.cos(7*a+1.2))* (.45+.55*t)
        asym=.025*math.cos(3*a+.4)+.012*math.sin(5*a-.7)
        furrows=sum(.036*math.exp(-(circ_delta(a,math.radians(f)+.035*math.sin(2*t))/.105)**2) for f in p['furrow_angles_degrees'])
        band=0
        for zc,amp,width,phase in [(.047,.022,.0045,.2),(.087,.018,.004,1.5),(.133,.021,.005,2.2),(.170,.018,.004,3.6)]:
            shifted=zc+.0016*math.sin(3*a+phase)
            band+=amp*math.exp(-((z-shifted)/width)**2)
        return shape*(1+rib+asym-furrows+band)
    vertices=[]; rings=p['lower_z_rings']
    for z in rings:
        t=z/bodytop; cx,cy=center(t)
        for i in range(n):
            a=2*math.pi*i/n; rad=scalar(z,a)
            # Growth-band heights remain low and uneven, but seam and contact are planar.
            zz=z if z==0 or z>=.2037 else z+.00055*math.sin(3*a+z*80)*math.sin(math.pi*t)
            vertices.append((cx+.0575*rad*math.cos(a),cy+.0525*rad*math.sin(a),zz))
    faces=[]; material_indices=[]
    for k in range(len(rings)-1):
        for i in range(n):
            j=(i+1)%n; faces.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i)); material_indices.append(1 if k==len(rings)-2 else 0)
    faces.append(tuple(reversed(range(n)))); material_indices.append(0)
    faces.append(tuple((len(rings)-1)*n+i for i in range(n))); material_indices.append(1)
    lower=mesh_object('Right valve - thick tapered shell',vertices,faces,[mats['body'],mats['seam']],c)
    for poly,mi in zip(lower.data.polygons,material_indices): poly.material_index=mi
    lower['representation']='Original outer shell; hidden pillars and hinge intentionally not reconstructed'
    # Opercular upper valve. A nearly planar circular/oval disk, not a dome or hollow cup.
    cx,cy=center(1); verts=[]
    caprings=[(1.0,.2052),(1.006,.2060),(.992,.2078),(.88,.2088),(.55,.20925),(.20,.2097)]
    for r,z in caprings:
        for i in range(n):
            a=2*math.pi*i/n; rim=scalar(bodytop,a)
            relief=.00022*math.cos(20*a+.3)*r*(1-r) if r<.995 else 0
            verts.append((cx+.0575*rim*r*math.cos(a),cy+.0525*rim*r*math.sin(a),z+relief))
    f=[]
    for k in range(len(caprings)-1):
        for i in range(n):
            j=(i+1)%n; f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
    f.append(tuple(reversed(range(n))))
    verts.append((cx,cy,.21)); ci=len(verts)-1
    for i in range(n): f.append(((len(caprings)-1)*n+i,(len(caprings)-1)*n+(i+1)%n,ci))
    lid=mesh_object('Left valve - restored low operculum',verts,f,mats['lid'],c)
    lid['representation']='Genus-level low opercular valve restoration; NOT asserted preserved on PRI 80129'
    # Fit authoring dimensions exactly while keeping the basal pivot at (0,0,0).
    objects=[lower,lid]; points=[v.co for obj in objects for v in obj.data.vertices]
    sx=p['max_width']/(max(v.x for v in points)-min(v.x for v in points)); sy=p['max_depth']/(max(v.y for v in points)-min(v.y for v in points))
    for obj in objects:
        for v in obj.data.vertices: v.co.x*=sx; v.co.y*=sy
        obj.data.update()
    root=bpy.data.objects.get(p['asset_id']); root['claim_scope']='Interpretive fossil shell; low restored lid supported at genus level'; root['specimen_scale_basis']='PRI 80129 length 21 cm; XY proportions estimated'
    scene=bpy.context.scene; scene.render.threads_mode='FIXED'; scene.render.threads=2
    geometry=[]
    for obj in objects:
        bm=bmesh.new(); bm.from_mesh(obj.data); vol=bm.calc_volume(signed=True)
        geometry.append({'part':obj.name,'closed':all(e.is_manifold for e in bm.edges),'signed_volume_m3':vol,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)})
        assert vol>0 and all(e.is_manifold for e in bm.edges); bm.free()
    return c,geometry

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    a=argparse.ArgumentParser(); a.add_argument('--out',type=Path,default=SOURCE.parent); a.add_argument('--render',action='store_true'); a.add_argument('--clay',action='store_true'); args=a.parse_args(argv)
    p=json.loads((SOURCE/'params.json').read_text()); out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True)
    c,geometry=build(p)
    budget=p['geometry_policy']; stage=out/'private'/'build-stage'
    record=export_asset(p['asset_id'],{'en':'Hippurites rudist shell','zh':'Hippurites 厚壳蛤化石壳'},'fossils',c,metadata={'description':{'en':'Original low-poly fossil-form reconstruction. 21 cm specimen-based height; estimated width/depth and genus-level restored low lid.','zh':'原创低多边形化石壳形态复原。高度依据 21 厘米标本；宽深估计，低平上盖为属级复原。'},'generator':'source/generate.py','reconstruction_notes':p['interpretive_parameters'],'surface_profile':'palette-only','threejs_version':p['runtime']['threejs_consumer']},output_root=stage,render=False,max_triangles=budget['max_triangles'],max_materials=budget['max_materials'],max_primitives=budget['max_primitives'])
    built=stage/p['asset_id']
    for ext in ('blend','glb'): shutil.copy2(built/(p['asset_id']+'.'+ext),out/('model.'+ext))
    assert (out/'model.glb').stat().st_size<=budget['max_glb_bytes']
    qa=json.loads((built/'qa.json').read_text()); qa['glb']['file']='model.glb'
    dump(out/'qa/evidence/source-glb.json',qa)
    dump(out/'qa/evidence/geometry.json',{'status':'PASS','glb_sha256':sha(out/'model.glb'),'parts':geometry,'contact':'Lower valve and cap share a planar interface at Blender Z=0.2052 m; touching closed shells, no air gap.','basal_plane_z_m':0,'lower_lid_interface_z_m':.2052,'lid_total_relief_height_m':.0048,'width_depth_are_estimates':True})
    record['glb']='model.glb'; record['blend']='model.blend'; record['preview']='preview.png'
    record['generator_sha256']=sha(SOURCE/'generate.py'); record['params_sha256']=sha(SOURCE/'params.json')
    dump(out/'qa/evidence/build-metadata.json',record)
    if args.render:
        evidence=render_four(out/'model.glb',out/'views',384 if args.clay else 768,8 if args.clay else 24,args.clay)
        shutil.copy2(out/'views/perspective.png',out/'preview.png')
        dump(out/'qa/evidence/views.json',evidence)
    print('HIPPU_COMPLETED',json.dumps({'glb_sha256':sha(out/'model.glb'),'triangles':qa['glb']['scene_triangles'],'out':str(out)}))
if __name__=='__main__': main()
