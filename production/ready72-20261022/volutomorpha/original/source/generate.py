#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Volutomorpha fossil interpretation. No scan/image input required.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUT
Use --gray for a gray authoring diagnostic. All geometry is deterministic.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent/'deps'))
import bpy, bmesh
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb

HERE=Path(__file__).resolve().parent

def dump(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def interp(rows,z,col):
    # Shape-preserving cubic Hermite interpolation avoids false terraces at knots.
    if z<=rows[0][0]: return rows[0][col]
    if z>=rows[-1][0]: return rows[-1][col]
    slopes=[(b[col]-a[col])/(b[0]-a[0]) for a,b in zip(rows,rows[1:])]
    def tangent(k):
        if k==0: return slopes[0]
        if k==len(rows)-1: return slopes[-1]
        left,right=slopes[k-1],slopes[k]
        if left*right<=0: return 0
        h0=rows[k][0]-rows[k-1][0]; h1=rows[k+1][0]-rows[k][0]
        w1=2*h1+h0; w2=h1+2*h0
        return (w1+w2)/(w1/left+w2/right)
    for i,(a,b) in enumerate(zip(rows,rows[1:])):
        if z<=b[0]:
            h=b[0]-a[0]; t=(z-a[0])/h
            return (2*t**3-3*t*t+1)*a[col]+(t**3-2*t*t+t)*h*tangent(i)+(-2*t**3+3*t*t)*b[col]+(t**3-t*t)*h*tangent(i+1)
def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,required=True); ap.add_argument('--gray',action='store_true'); args=ap.parse_args(argv)
    P=json.loads((HERE/'params.json').read_text()); out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    C=setup_scene(P['asset_id'],P['seed']); root=bpy.data.objects[C['asset_root']]
    root['representation']='Original fossil-shell interpretation, not a downloaded scan'
    root['specimen']='PRI 78029'; root['width_depth']='Inferred working proportions; no caliper measurements'
    root['preservation']='Shallow gray aperture interpretation; no specific sediment diagnosis'
    root['mount']='Surviving blunt basal tip at floor, long axis +Z, aperture -Y'
    palette=P['palette']; mats=[make_material(name,('#969696' if args.gray else color),roughness=.93) for name,color in palette.items()]
    profile=P['profile_mm']; heights=P['row_heights_mm']; qvals=P['aperture_cross_section']; n_outer=P['outer_segments']; N=len(qvals)+n_outer-1
    verts=[]; faces=[]; mids=[]; tags=[]
    # Each row runs left columellar rim -> shallow aperture -> outer lip -> back.
    for j,z in enumerate(heights):
        rx,ry,cx,cy=[interp(profile,z,k) for k in range(1,5)]
        af=interp(P['aperture_factor'],z,1)
        left=-1.80; right=left+1.18*af+.10*(1-af)
        depth=interp(P['recess_mm'],z,1)
        angles=[left+(right-left)*q for q in qvals]+[right+(left+2*math.pi-right)*k/n_outer for k in range(1,n_outer)]
        for k,theta in enumerate(angles):
            q=qvals[k] if k<len(qvals) else None
            # Subdued original growth undulation and fine longitudinal weathering.
            growth=.10*math.sin(26*theta+.22*z)+.065*math.sin(47*theta-.11*z)
            spire=max(0,min(1,(z-77)/8)); phase=2*math.pi*(z-79)/5.8-theta
            suture=min(.68,rx*.20)*math.exp(-((math.sin(phase/2)/.42)**2))*spire
            rmod=growth*(1-spire*.5)-suture
            x=cx+(rx+rmod)*math.cos(theta); y=cy+(ry+rmod)*math.sin(theta)
            if q is not None and z<86:
                # The mouth is actual concave geometry, closed by interpreted fossil fill.
                xl=cx+rx*math.cos(left); xr=cx+rx*math.cos(right)
                yl=cy+ry*math.sin(left); yr=cy+ry*math.sin(right)
                x=xl+(xr-xl)*q
                # Shallow lip height with softly irregular outline, not pristine knife edge.
                rim=-.48*af*(math.exp(-(q/.060)**2)+math.exp(-((1-q)/.060)**2))
                y=yl+(yr-yl)*q+depth*(math.sin(math.pi*q)**.84)+rim
                y+=.09*math.sin(17*q+.72*z)*math.sin(math.pi*q)*af
                x+=.12*math.sin(.87*z)*math.sin(math.pi*q)*af
            verts.append((x*.001,y*.001,z*.001))
            tags.append((z,theta,q,phase))
    for j in range(len(heights)-1):
        for k in range(N):
            kk=(k+1)%N; faces.append((j*N+k,j*N+kk,(j+1)*N+kk,(j+1)*N+k))
            z=(heights[j]+heights[j+1])*.5
            q=(qvals[k]+qvals[k+1])*.5 if k<len(qvals)-1 else None
            theta=tags[j*N+k][1]
            if q is not None and .075<q<.925 and z<83:
                m=3 if math.sin(z*.47+q*12)+.4*math.sin(z*.82-q*19)>-.35 else 4
            elif q is not None and z<84 and (q<=.075 or q>=.925): m=5
            else:
                noise=math.sin(theta*3.1+z*.39)+.52*math.sin(theta*7.2-z*.20)+.18*math.cos(theta*19+z*.81)
                m=0 if noise<.62 else 1
                if noise<-.92: m=2
            mids.append(m)
    # Basal broken/fossil-filled face, kept blunt; the top closes on a tiny worn point.
    faces.append(tuple(reversed(range(N)))); mids.append(2)
    top=len(verts); verts.append((-.0041,.002,.100))
    for k in range(N): faces.append(((len(heights)-1)*N+k,(len(heights)-1)*N+(k+1)%N,top)); mids.append(0)
    # The center of the actual blunt basal footprint is the identity-root contact.
    foot=verts[:N]
    contact=tuple((min(v[i] for v in foot)+max(v[i] for v in foot))*.5 for i in (0,1))
    verts=[(v[0]-contact[0],v[1]-contact[1],v[2]) for v in verts]
    obj=mesh_object('Preserved_shell_and_shallow_aperture',verts,faces,mats,C)
    obj['basal_contact_center_m']=[0.0,0.0,0.0]
    for poly,mi in zip(obj.data.polygons,mids): poly.material_index=mi; poly.use_smooth=False
    # Semantic vertex groups retain direct access to the mouth and exterior.
    aperture=[i for i,t in enumerate(tags) if t[2] is not None and .075<t[2]<.925 and t[0]<83]
    obj.vertex_groups.new(name='Shallow_apertural_surface').add(aperture,1,'REPLACE')
    obj.vertex_groups.new(name='Low_spire').add([i for i,t in enumerate(tags) if t[0]>78]+[top],1,'REPLACE')
    obj.vertex_groups.new(name='Preserved_blunt_basal_channel').add([i for i,t in enumerate(tags) if t[0]<22],1,'REPLACE')
    obj['construction']='Closed row loft with integrated shallow concave apertural chord; no stock primitives'
    bpy.context.view_layer.update(); report=audit_source(C,max_triangles=40000)
    # Verify watertightness and outward volume, independently of the renderer.
    bm=bmesh.new(); bm.from_mesh(obj.data); volume=bm.calc_volume(signed=True)
    topo={'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':volume,'euler_characteristic':len(bm.verts)-len(bm.edges)+len(bm.faces)}; bm.free()
    if report['errors']: raise RuntimeError(report['errors'])
    if topo['boundary_edges'] or topo['nonmanifold_edges'] or volume<=0: raise RuntimeError(topo)
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    bpy.context.scene['generator_sha256']=sha(Path(__file__)); bpy.context.scene['params_sha256']=sha(HERE/'params.json')
    bpy.context.scene['source_note']='Editable named mesh with semantic vertex groups; no stage cameras/lights in source'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in C.all_objects: o.select_set(True)
    bpy.context.view_layer.objects.active=obj
    settings=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    props=bpy.ops.export_scene.gltf.get_rna_type().properties
    missing=[k for k in settings if k not in props]
    if missing: raise RuntimeError('Unsupported exporter flags '+repr(missing))
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**settings)
    glb=audit_glb(out/'model.glb',max_triangles=40000,max_materials=6,max_primitives=8)
    if glb['errors']: raise RuntimeError(glb['errors'])
    low=report['bounds_blender_m']['min']; hi=report['bounds_blender_m']['max']
    metrics={'asset_id':P['asset_id'],'revision':P['revision'],'glb_sha256':sha(out/'model.glb'),'semantic_sha256':glb['semantic_sha256'],'blender_version':bpy.app.version_string,'python_version':sys.version.split()[0],'gltf_exporter_version':'4.3.47','consumer_threejs_version':'0.180.0','generator_sha256':sha(Path(__file__)),'params_sha256':sha(HERE/'params.json'),'gray_diagnostic':args.gray,'export_settings':settings,'source':report,'glb':glb,'geometry':topo,'basal_mount_translation_m':[-contact[0],-contact[1],0.0],'glb_bytes':(out/'model.glb').stat().st_size,'bounds_expected_gltf_m':{'min':[low[0],low[2],-hi[1]],'max':[hi[0],hi[2],-low[1]]},'scientific_limits':['Length approximately 10 cm from PRI. Width and depth are inferred working proportions.','Single apertural reference cannot establish backside detail or cavity fill diagnosis.','No elongation of truncated basal channel; no soft body or invented columellar folds.']}
    dump(out/'build.json',metrics); print(json.dumps({'output':str(out),'triangles':report['triangles'],'sha256':metrics['glb_sha256'],'geometry':topo}))
if __name__=='__main__': main()
