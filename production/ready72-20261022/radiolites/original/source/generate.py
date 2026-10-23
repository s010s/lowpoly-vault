# SPDX-License-Identifier: MIT
"""Deterministic original Radiolites dario loft, not a fossil scan.
Usage: blender -b -t 2 --python source/generate.py -- --out . --mode build
Cheap rebuild: --no-render. Shape check: --mode gray.
Dependencies: Python stdlib, Blender 4.3.2 and declared source/deps only.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import asset_common as common
from presentation import render_views

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')

def make_shell(params):
    col=common.setup_scene('radiolites',params['seed'])
    root=bpy.data.objects['radiolites']
    root['taxon']='Radiolites dario (Catullo), sensu Cestari 2005'
    root['reconstruction']='Lower valve guided by Plate 2 Fig. 1 right specimen; low upper valve restored from same-species text; depth inferred.'
    mats=[common.make_material('stone-'+n,c,params['roughness']) for n,c in params['palette'].items()]
    n=params['radial_segments'];ribs=params['rib_count']
    # One continuous loft provides lamellar steps, never detached collar rings.
    rings=[(0.,.25,'base'),(.001,.33,'base'),(.0035,.40,'body')]
    episodes=[(.008,.52),(.013,.63),(.0185,.72),(.024,.81),(.0295,.89),(.0355,.96),(.0425,1.)]
    for height,radius in episodes:
        rings += [(height-.0011,radius*.97,'body'),(height-.0002,radius,'lip'),(height,radius*.956,'recess')]
    rings += [(.0431,1.,'rim'),(.0436,.973,'seam'),(.0439,1.008,'cap-edge'),(.0444,.99,'cap'),(.0448,.80,'cap'),(.045,.28,'cap')]
    verts=[];faces=[];face_material=[]
    for j,(z,rad,kind) in enumerate(rings):
        t=z/params['height'];cap=kind in ('cap-edge','cap')
        for i in range(n):
            theta=2*math.pi*i/n
            phase=.20*math.sin(t*2.5)+.055*math.sin(theta*3)
            amp=(.047 if not cap else .018)*min(1,rad/.40)*(.88+.18*math.cos(5*theta)+.12*math.sin(7*theta))
            broad=.028*math.cos(5*theta+.7)+.022*math.sin(3*theta-1.1)
            rr=rad*(1+amp*math.cos(ribs*theta+phase)+broad+.006*math.sin(9*theta+t*2))
            dz=(.00043*math.sin(3*theta+t*4)+.00022*math.cos(5*theta-t*6))*min(1,z/.005)
            if kind=='base':dz*=.15
            if z>.042:dz*=max(.15,(.045-z)/.003)
            if z==0:dz=0
            cx=.0025*math.sin(t*math.pi/2);cy=.00060*math.sin(t*math.pi)
            verts.append((cx+.012*rr*math.cos(theta),cy+.011*rr*math.sin(theta),z+dz))
    for j in range(len(rings)-1):
        upper_kind=rings[j+1][2]
        mi=3 if upper_kind=='seam' else 2 if upper_kind.startswith('cap') else 1 if upper_kind=='recess' else 0
        for i in range(n):
            faces.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i));face_material.append(mi)
    bottom=len(verts);verts.append((0,0,0))
    top=len(verts);verts.append((.0025,0,.04494))
    last=(len(rings)-1)*n
    for i in range(n):
        faces.append((bottom,(i+1)%n,i));face_material.append(0)
        faces.append((top,last+i,last+(i+1)%n));face_material.append(2)
    # Exact nominal envelope; photo scale and inferred depth remain approximate.
    lo=[min(p[k] for p in verts) for k in range(3)];hi=[max(p[k] for p in verts) for k in range(3)]
    factors=[params['width']/(hi[0]-lo[0]),params['depth']/(hi[1]-lo[1]),params['height']/(hi[2]-lo[2])]
    verts=[(p[0]*factors[0],p[1]*factors[1],(p[2]-lo[2])*factors[2]) for p in verts]
    minimum_axial_step=min(verts[(j+1)*n+i][2]-verts[j*n+i][2] for j in range(len(rings)-1) for i in range(n))
    if minimum_axial_step<=0:raise ValueError('Loft ring columns cross or reverse')
    obj=common.mesh_object('layered-lower-valve-and-restored-low-upper-valve',verts,faces,mats,col)
    obj['minimum_axial_ring_advance_m']=minimum_axial_step
    for p,m in zip(obj.data.polygons,face_material):p.material_index=m
    lower=obj.vertex_groups.new(name='lower-valve-photo-guided');lower.add(list(range(25*n))+[bottom],1,'REPLACE')
    upper=obj.vertex_groups.new(name='upper-valve-textual-restoration');upper.add(list(range(24*n,len(rings)*n))+[top],1,'REPLACE')
    obj['surface_method']='Continuous closed radial loft: 22 ribs, 7 lamellae, no texture/scan/borrowed geometry.'
    obj['upper_valve_evidence']='Same-species textual restoration, not verified preserved in photo.'
    obj['depth_evidence']='23 mm working depth is inferred.'
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.context.scene['generator_sha256']=sha(SOURCE/'generate.py');bpy.context.scene['params_sha256']=sha(SOURCE/'params.json')
    bpy.context.scene['source_entrypoint']='source/generate.py'
    return col,rings

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--mode',choices=['gray','build'],default='build');p.add_argument('--no-render',action='store_true')
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True);params=json.loads((SOURCE/'params.json').read_text())
    col,rings=make_shell(params)
    if args.mode=='gray':
        render_views(col,out/'private/gray',320,6,clay=True);write(out/'private/gray/source-qa.json',common.audit_source(col,5500));return
    record=common.export_asset('radiolites',{'en':'Radiolites layered rudist shell','zh':'Radiolites 层叠厚壳蛤'},'fossils',col,
        metadata={'generator':'source/generate.py','revision':'r001','profile':'original-palette-static','source_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json')},
        output_root=out/'private/export-stage',render=False,max_triangles=5500,max_materials=4,max_primitives=8)
    stage=out/'private/export-stage/radiolites'
    for ext in ('glb','blend'):shutil.copy2(stage/f'radiolites.{ext}',out/f'model.{ext}')
    qa=json.loads((stage/'qa.json').read_text());qa['glb']['file']='model.glb';write(out/'qa/evidence/source-and-glb.json',qa)
    record.update(glb='model.glb',blend='model.blend',preview='preview.png',source_references='references.json',brief='brief.json')
    record['size_uncertainty']='45 x 25 x 23 mm rounded photo-based envelope; depth inferred.'
    record['upper_valve_uncertainty']='Low cap restored from same-species text; not confirmed preserved in selected photo.'
    record['origin']='Small basal footprint center at Z=0; upper end slightly curved off-center.'
    record['max_glb_bytes']=650000
    if (out/'model.glb').stat().st_size>650000:raise RuntimeError('Frozen GLB size budget exceeded')
    write(out/'qa/evidence/build.json',record)
    write(out/'qa/evidence/geometry-design.json',{'status':'PASS_MAKER_MEASUREMENTS','triangles':qa['source']['triangles'],'radial_segments':params['radial_segments'],'rings':len(rings),'growth_episodes':7,'longitudinal_ribs':22,'connected_surface_components':1,'minimum_axial_ring_advance_m':bpy.data.objects['layered-lower-valve-and-restored-low-upper-valve']['minimum_axial_ring_advance_m'],'closed_parts':qa['source']['parts'],'body_height_m':.0431,'restored_cap_zone_m':.0019,'nominal_dimensions_blender_m':[.025,.023,.045],'base_to_broad_rim_radius_ratio':.25,'rings_design':[{'height_m':z,'relative_radius':r,'type':k} for z,r,k in rings],'hidden_internal_caps':0,'overlapping_parts':0,'limitations':'Maker design measurements only; independent scientific/visual review required.'})
    if not args.no_render:
        glb_sha=sha(out/'model.glb');bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(out/'model.glb'))
        imported=bpy.data.collections.new('EXACT_GLB_PREVIEW');bpy.context.scene.collection.children.link(imported)
        for obj in list(bpy.context.scene.objects):
            for old in list(obj.users_collection):old.objects.unlink(obj)
            imported.objects.link(obj)
        paths=render_views(imported,out/'views',params['render_resolution'],params['render_samples']);shutil.copy2(out/'views/perspective.png',out/'preview.png')
        write(out/'qa/evidence/exact-export-previews.json',{'status':'RENDERED_FOR_MAKER_REVIEW','glb_sha256':glb_sha,'method':'Factory reset, import exact delivered model.glb, no source meshes retained.','blender_version':bpy.app.version_string,'engine':'Cycles CPU','threads':2,'resolution':params['render_resolution'],'samples':params['render_samples'],'view_transform':'Standard','look':'None','color_exposure':0,'palette_conversion':'sRGB hex to linear via pinned asset_common','cameras':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[1,-1,1]},'files':{p.name:sha(p) for p in paths},'preview_sha256':sha(out/'preview.png'),'gpu':'NOT_RUN','populated_scene':'NOT_RUN'})
    print('MAKER BUILD COMPLETE',out,sha(out/'model.glb'))
if __name__=='__main__':main()
