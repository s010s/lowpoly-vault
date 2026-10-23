#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic holotype-informed Crioceratites, not a photogrammetric replica.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT
Every runtime helper is local in source/deps. Parameters hold the authored trace.
"""
import argparse, bisect, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
def catmull(p0,p1,p2,p3,t):
    return [0.5*((2*p1[j])+(-p0[j]+p2[j])*t+(2*p0[j]-5*p1[j]+4*p2[j]-p3[j])*t*t+(-p0[j]+3*p1[j]-3*p2[j]+p3[j])*t**3) for j in range(3)]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--clay',action='store_true')
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]); out=a.out.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((SOURCE/'params.json').read_text()); col=setup_scene(p['asset_id'],p['seed'])
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    mats=[make_material(n,c,roughness=.9) for n,c in zip(['Fossil warm-grey','Worn mineral','Fresh broken mineral'], ['#AAAAAA']*3 if a.clay else p['surface']['palette'])]
    keys=p['centerline_xy_width_px']; dense=[]
    for i in range(len(keys)-1):
        for k in range(20):dense.append(catmull(keys[max(0,i-1)],keys[i],keys[i+1],keys[min(len(keys)-1,i+2)],k/20))
    dense.append(keys[-1]); lengths=[0.]
    for u,v in zip(dense,dense[1:]):lengths.append(lengths[-1]+math.hypot(v[0]-u[0],v[1]-u[1]))
    N=p['rings']; K=p['cross_section_sides']; samples=[]
    for i in range(N):
        dist=lengths[-1]*i/(N-1);k=min(len(dense)-2,max(0,bisect.bisect_right(lengths,dist)-1));t=(dist-lengths[k])/(lengths[k+1]-lengths[k]);samples.append([dense[k][j]*(1-t)+dense[k+1][j]*t for j in range(3)])
    scale=p['last_whorl_height']/keys[-1][2]
    centers=[Vector(((v[0]-420)*scale,0,-v[1]*scale)) for v in samples]
    d=[0.]
    for u,v in zip(centers,centers[1:]): d.append(d[-1]+(v-u).length)
    ribphase=[0.]
    for i in range(1,N):
        width=samples[i][2]*scale;spacing=.00026+.00125*(width/p['last_whorl_height'])**.8
        ribphase.append(ribphase[-1]+(d[i]-d[i-1])/spacing)
    verts=[]; faces=[]
    spines=[(.249,.0022),(.301,.0023),(.350,.0012)]
    for i,c in enumerate(centers):
        t=(centers[min(N-1,i+1)]-centers[max(0,i-1)]).normalized();normal=Vector((t.z,0,-t.x));f=i/(N-1)
        radial=samples[i][2]*scale*.5
        width_ratio=.95-.20*min(1,radial/.006)
        axial=radial*width_ratio
        for j in range(K):
            angle=2*math.pi*j/K; ca=math.cos(angle);si=math.sin(angle)
            inner=ca if ca>-.72 else -.72+(ca+.72)*.35
            phase=ribphase[i]+.15*math.sin(angle)+.07*math.sin(2*angle+f*9)+.055*math.sin(ribphase[i]*1.21)
            wave=max(0,math.cos(2*math.pi*phase))**3
            mature=min(1,max(0,(f-.5)/.2)); main=.82+.18*(.5+.5*math.cos(2*math.pi*phase/4.4))*(1-mature)
            amp=0 if a.clay else min(.00038,radial*.12)*wave*main*(.60+.40*max(0,ca))*(.9+.1*math.sin(i*.29+j*1.7))
            bump=0 if a.clay else sum(h*math.exp(-((f-f0)/.0045)**2)*max(0,ca)**12 for f0,h in spines)
            irregular=0 if a.clay else .000035*(math.sin(i*.53+j*1.9)+.5*math.sin(i*.17-j*.6))*min(1,radial/.004)
            pt=c+normal*(inner*(radial+amp+irregular)+bump)+Vector((0,si*(axial+amp*.72+irregular*.5),0))
            if i==N-1:pt+=t*(.00016*math.sin(j*2.3)+.00007*math.cos(j*.7))
            verts.append(tuple(pt))
    for i in range(N-1):
        for j in range(K):faces.append((i*K+j,i*K+(j+1)%K,(i+1)*K+(j+1)%K,(i+1)*K+j))
    for i in (0,N-1):
        c=centers[i];inner=[]
        for j in range(K):
            v=Vector(verts[i*K+j]);inner.append(len(verts));verts.append(tuple(c+(v-c)*.49))
        centeridx=len(verts);verts.append(tuple(c))
        for j in range(K):
            faces.append((i*K+j,inner[j],inner[(j+1)%K],i*K+(j+1)%K));faces.append((inner[j],centeridx,inner[(j+1)%K]))
    rawspan=max(max(v[k] for v in verts)-min(v[k] for v in verts) for k in (0,2));fit=p['diameter']/rawspan
    verts=[tuple(q*fit for q in v) for v in verts];minz=min(v[2] for v in verts);mx=(max(v[0] for v in verts)+min(v[0] for v in verts))/2
    verts=[(v[0]-mx,v[1],v[2]-minz) for v in verts]
    obj=mesh_object('Continuous fossil coil',verts,faces,mats,col)
    for poly in obj.data.polygons:
        if poly.index >= (N-1)*K:poly.material_index=2 if poly.index >= (N-1)*K+2*K else 1
        # Shell mantle stays one mineral palette; no artificial patchwork texture.
    obj['section']='Subcircular to mildly subellipsoidal; flattened dorsum; width inferred'
    obj['reference']='RGM197188A; Kakabadze & Hoedemaeker 2010, Pl.36 fig.2'
    root=bpy.data.objects[col['asset_root']];root['reconstruction']='Holotype lateral silhouette, unseen width inferred, no living parts'
    source=audit_source(col,max_triangles=24000)
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    missing=set(options)-{x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if missing:raise RuntimeError('Exporter flags unavailable: '+repr(missing))
    bpy.ops.export_scene.gltf(**options)
    glb=audit_glb(out/'model.glb',max_triangles=24000,max_materials=6,max_primitives=16)
    if glb['errors']:raise RuntimeError(glb['errors'])
    if (out/'model.glb').stat().st_size>2500000:raise RuntimeError('GLB byte budget exceeded')
    b=source['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(expected[k][i]-glb['bounds_m'][k][i]) for k in expected for i in range(3))
    if delta>1e-7 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source/export roundtrip mismatch')
    report={'status':'PASS','claim_scope':'Maker technical checks only, not independent acceptance','source':source,'glb':glb,'glb_sha256':sha(out/'model.glb'),'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'blender_version':bpy.app.version_string,'export_options':{k:v for k,v in options.items() if k!='filepath'},'bounds_roundtrip_max_error_m':delta,'measurements':{'lateral_max_extent_m':p['diameter'],'last_section_radial_height_m':p['last_whorl_height']*fit,'inferred_working_axial_width_m':p['axial_thickness_inferred'],'actual_bbox_axial_width_m':b['size'][1],'photograph_fit_scale':fit,'width_not_measured':True},'clay':a.clay,'geometry_notes':{'continuous_single_mesh':True,'centerline_planar':True,'closed_mineral_ends':True,'visible_spine_remnants':'Three subdued integrated bumps on upper intermediate coil only','reference':'Single lateral photograph; unseen width and back conservatively inferred'}}
    write(out/'build-report.json',report)
    print(json.dumps({'status':'BUILT','out':str(out),'triangles':glb['scene_triangles'],'glb_sha256':sha(out/'model.glb')}))
if __name__=='__main__':main()
