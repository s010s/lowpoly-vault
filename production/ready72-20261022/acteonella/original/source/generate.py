#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Acteonella fossil interpretation. No images or outside inputs.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUTPUT
"""
import sys, json, math, hashlib, argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from asset_common import setup_scene, make_material, mesh_object, audit_source, _bounds, _vertices_world
from qa_glb import audit_glb

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def smoothstep(a,b,v):
    x=max(0.,min(1.,(v-a)/(b-a)))
    return x*x*(3-2*x)
def wrap(v): return (v+math.pi)%(2*math.pi)-math.pi

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',type=Path,default=HERE.parent)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text())
    col=setup_scene('acteonella',p['seed'])
    body=make_material('weathered-ochre-calcite',p['palette']['shell'],.92)
    fill=make_material('muted-mineral-aperture',p['palette']['mineral_fill'],.99)
    fold=make_material('worn-columellar-folds',p['palette']['fold'],.94)
    profile=p['profile']
    def radial(t):
        # Shape-preserving Hermite spline, with local harmonic slopes.
        xs=[x[0] for x in profile]; ys=[x[1] for x in profile]
        k=next((i for i in range(len(xs)-1) if xs[i]<=t<=xs[i+1]),len(xs)-2)
        sec=[(ys[i+1]-ys[i])/(xs[i+1]-xs[i]) for i in range(len(xs)-1)]
        def slope(i):
            if i==0: return sec[0]
            if i==len(xs)-1: return sec[-1]
            return 0 if sec[i-1]*sec[i]<=0 else 2/(1/sec[i-1]+1/sec[i])
        u=(t-xs[k])/(xs[k+1]-xs[k]); h=xs[k+1]-xs[k]
        return (2*u**3-3*u*u+1)*ys[k]+(u**3-2*u*u+u)*h*slope(k)+(-2*u**3+3*u*u)*ys[k+1]+(u**3-u*u)*h*slope(k+1)
    nz=p['height_segments']; na=p['radial_segments']
    verts=[]; faces=[]; face_metadata=[]
    for j in range(1,nz):
        t=j/nz; r=radial(t)
        for i in range(na):
            theta=-math.pi+2*math.pi*i/na
            # Aperture narrows toward the shoulder and widens at its base.
            center=-.67-.25*(1-smoothstep(.08,.36,t))
            width=.56+.25*(1-smoothstep(.12,.38,t))
            d=wrap(theta-center)
            aperture=smoothstep(.025,.10,t)*(1-smoothstep(.86,.968,t))
            cut=(1-smoothstep(width*.24,width*.58,abs(d)))*aperture
            # A surviving, worn outer lip, not an unattached plate.
            outer_lip=math.exp(-((d-width*.65)/.075)**2)*aperture
            inner_lip=math.exp(-((d+width*.65)/.10)**2)*aperture
            relief=0
            for base in p['fold_heights']:
                height=base+.037*(theta+2.2)
                ang=smoothstep(-2.45,-2.05,theta)*(1-smoothstep(-.92,-.60,theta))
                relief += math.exp(-((t-height)/.0125)**2)*ang*.065
            wear_field=(math.sin(theta*9+t*71)+.5*math.sin(theta*17-t*89)+.3*math.cos(theta*31+t*103))
            micro=.0019*wear_field*math.sin(math.pi*t)**1.2
            # Coarse mineral texture only inside the shallow preserved aperture.
            rough=.012*math.sin(i*12.9898+j*7.233)*math.sin(i*3.91-j*17.71)*cut
            # Shallow coiling seam on the concealed apical crown only.
            crown_phase=-.67+math.tau*(t-.925)/.073
            crown_seam=math.exp(-(wrap(theta-crown_phase)/.12)**2)*smoothstep(.917,.94,t)*(1-smoothstep(.982,.999,t))
            rr=r*(1-.22*cut+.035*outer_lip+.013*inner_lip+micro+rough)-.012*crown_seam+relief
            x=.018*rr*math.cos(theta)-.0017*math.sin(math.pi*t)*t
            y=.016*rr*math.sin(theta)
            z=.075*t
            # Low, asymmetrical involute crown closure, without a separate spire.
            if t>.90:
                z += .00028*math.sin(theta+12*t)*(1-smoothstep(.97,1,t))*smoothstep(.90,.95,t)-.00018*crown_seam
            verts.append((x,y,z))
    for j in range(nz-2):
        t=(j+1.5)/nz
        for i in range(na):
            theta=-math.pi+2*math.pi*(i+.5)/na
            a0=j*na+i; b0=j*na+(i+1)%na; c0=(j+1)*na+(i+1)%na; d0=(j+1)*na+i
            faces.append((a0,b0,c0,d0)); face_metadata.append((t,theta))
    bottom=len(verts); verts.append((0,0,0)); top=len(verts); verts.append((-.0001,0,.075))
    for i in range(na):
        faces.append((bottom,(i+1)%na,i)); face_metadata.append((0,0))
        a0=(nz-2)*na+i; b0=(nz-2)*na+(i+1)%na
        faces.append((top,a0,b0)); face_metadata.append((1,0))
    # Real-world dimensions are frozen; no separate display normalization.
    dx=max(x[0] for x in verts)-min(x[0] for x in verts)
    dy=max(x[1] for x in verts)-min(x[1] for x in verts)
    verts=[(x*p['width_X']/dx,y*p['depth_Y_inferred']/dy,z) for x,y,z in verts]
    obj=mesh_object('convolute-shell-with-preserved-aperture',verts,faces,[body,fill,fold],col)
    for poly,(t,theta) in zip(obj.data.polygons,face_metadata):
        center=-.67-.25*(1-smoothstep(.08,.36,t)); width=.56+.25*(1-smoothstep(.12,.38,t))
        d=wrap(theta-center)
        aperture=smoothstep(.025,.10,t)*(1-smoothstep(.86,.968,t))
        mineral=abs(d)<width*.46*aperture and .035<t<.956
        fold_band=any(abs(t-(base+.037*(theta+2.2)))<.015 for base in p['fold_heights']) and -2.27<theta<-.77
        poly.material_index=1 if mineral else 2 if fold_band else 0
        poly.use_smooth=not mineral
    root=bpy.data.objects[col['asset_root']]
    root['taxon']='Acteonella'; root['reference_anchor']='NHMW1965/664/13, Kollmann 2014 Fig. 12A'
    root['inference']='Backside and 32 mm depth inferred from one apertural-oblique specimen photo.'
    obj['anatomy']='Convolute barrel, long shallow mineral-filled aperture, three basal columellar folds.'
    source=audit_source(col,p['max_triangles'])
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects: o.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
        export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
        export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,
        export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    required=set(options); available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if required-available: raise RuntimeError('Missing export settings: '+str(required-available))
    bpy.ops.export_scene.gltf(**options)
    glb=audit_glb(out/'model.glb',p['max_triangles'],6,16)
    b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in expected for i in range(3))
    if glb['errors'] or delta>1e-6 or glb['scene_triangles']!=source['triangles']: raise RuntimeError('Source/export mismatch: '+str(glb['errors']))
    if glb['bytes']>2500000: raise RuntimeError('Frozen GLB budget exceeded')
    report={'asset_id':'acteonella','revision':'r001','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,
       'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','generator_sha256':sha(Path(__file__)),'parameters_sha256':sha(HERE/'params.json'),
       'export_options':{k:v for k,v in options.items() if k!='filepath'},'scope':'Maker technical checks only. Independent visual/factual QA, GPU and combined scene not established.'}
    write(out/'qa/evidence/build.json',report)
    print(json.dumps({'status':'MAKER_TECHNICAL_PASS','glb_sha256':glb['sha256'],'semantic_sha256':glb['semantic_sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes']}))
if __name__=='__main__': main()
