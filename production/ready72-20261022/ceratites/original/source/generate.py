# SPDX-License-Identifier: MIT
"""Deterministic self-contained Ceratites fossil interpretation. Blender 4.3.2.
Usage: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUTPUT
Only params.json and vendored source/deps Python modules are runtime inputs.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def smooth(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def gaussian(x,w): return math.exp(-0.5*(x/w)**2)

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser(); p.add_argument('--output-dir',type=Path,required=True); args=p.parse_args(argv)
    out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((HERE/'params.json').read_text())
    c=setup_scene('ceratites',cfg['seed'])
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    mats=[make_material(name,color,roughness=cfg['roughness']) for name,color in cfg['palette'].items()]
    N=cfg['angular_sections']; us=cfg['radial_sections']; M=len(us); k=cfg['inner_outer_ratio']; r0=cfg['outer_radius_start_m']; end=1-cfg['terminal_transition_fraction']
    verts=[]; faces=[]; mi=[]; ids={}; vertex_labels=[]
    def shell(s,u,side):
        theta=math.radians(cfg['termination_angle_deg'])-s*2*math.pi
        ideal=r0*k**(-s)
        R=ideal if s<=end else ideal+(r0-ideal)*smooth((s-end)/(1-end))
        core=0.80*r0
        r=2*u*core if u<=0.5 else core+(R-core)*(2*u-1)
        u=r/R
        # Integrated flanks are almost flat; the umbilicus is recessed and closed.
        half=0.0050+0.0145*smooth(r/0.035)
        # Spiral contact grooves are continuous across angular wrap. They are not sutures.
        if r>0.001:
            q=math.log(r/ideal)/math.log(k)
            # Periodic phase plus radius-based depth guarantees wrap continuity.
            valleys=0.0048*smooth(r/0.028)*gaussian(q-round(q),0.11)
            half-=valleys
        # Rounded ventral band, never a knife keel. Flank-to-rim transition is smooth.
        rim=max(0.,(u-0.74)/0.26)
        half*=math.sqrt(max(0.,1-rim*rim))
        nodes=sum(amp*gaussian(s-pos,cfg['node_angular_sigma']) for pos,amp in cfg['shoulder_nodes'])
        # Two integrated shoulder nodules, one on either flank, not added bead objects.
        shoulder=gaussian(u-0.955,0.040)
        r+=nodes*shoulder
        half+=nodes*0.30*shoulder*(1-smooth((u-0.975)/0.025))
        # Lateral relief is substantially lower than nodes and fades on the adult end.
        rib=0.
        for pos,amp in cfg['shoulder_nodes']:
            rib+=gaussian(s-pos-0.013*(1-u),0.022)*(amp/0.0052)
        half+=cfg['subdued_rib_height_m']*rib*gaussian(u-0.71,0.16)*(1-smooth((u-0.94)/0.06))
        # Restrained geometric weathering; no photographic texture or invented sutures.
        half+=0.00016*math.sin(13*theta+7*u)*math.sin(5*theta-10*u)*smooth((r-0.022)/0.018)*(1-smooth((u-0.91)/0.09))
        if u==1: half=0.
        return (r*math.cos(theta),side*half,r*math.sin(theta))
    # Shared outer edge creates a single closed solid. Front/back center vertices are distinct.
    for side in (-1,1):
        ids[(side,0,0)]=len(verts); verts.append((0,side*0.005,0)); vertex_labels.append((side,0,0))
        for j,u in enumerate(us,1):
            for i in range(N):
                if j==M and side==1:
                    ids[(side,j,i)]=ids[(-1,j,i)]; continue
                ids[(side,j,i)]=len(verts); verts.append(shell(i/N,u,side)); vertex_labels.append((side,j,i))
    for side in (-1,1):
        for i in range(N):
            nxt=(i+1)%N
            faces.append((ids[(side,0,0)],ids[(side,1,i)],ids[(side,1,nxt)])); mi.append(0)
        for j in range(1,M):
            for i in range(N):
                nxt=(i+1)%N
                a,b,d,e=ids[(side,j,i)],ids[(side,j,nxt)],ids[(side,j+1,i)],ids[(side,j+1,nxt)]
                # Alternating diagonal avoids a directional tessellation bias.
                pair=((a,d,e),(a,e,b)) if (i+j)%2 else ((a,d,b),(b,d,e))
                s=(i+0.5)/N; u=(us[j-1]+us[j])*0.5
                mat=2 if s>end+0.003 and u>0.54 else 0
                faces.extend(pair); mi.extend([mat,mat])
    # Author exact design dimensions in meters, keeping identity object transforms.
    low=[min(v[a] for v in verts) for a in range(3)]; high=[max(v[a] for v in verts) for a in range(3)]
    scale=[cfg['target_dimensions_blender_m'][a]/(high[a]-low[a]) for a in range(3)]
    transformed=[[(v[0]-(low[0]+high[0])/2)*scale[0],v[1]*scale[1],(v[2]-low[2])*scale[2]] for v in verts]
    # Root is at the floor-contact center, rather than the arbitrary coil center.
    floor=[v for v in transformed if v[2]<1e-7]
    contactx=sum(v[0] for v in floor)/len(floor); contacty=sum(v[1] for v in floor)/len(floor)
    transformed=[(v[0]-contactx,v[1]-contacty,v[2]) for v in transformed]
    obj=mesh_object('mineral-filled-nodose-planispiral-shell',transformed,faces,mats,c)
    for poly,idx in zip(obj.data.polygons,mi):
        poly.material_index=idx
        poly.use_smooth=(idx!=2)
    obj['construction']='Closed bilateral surface with integrated shoulder nodes, shallow spiral valleys, no cavity; reconstructed unseen flanks.'
    obj['not_a_single_specimen_replica']=True
    obj['source_parts']='Main whorl, early coil, paired shoulder nodes and mineral-filled break are editable regions of one manifold mesh.'
    # Vertex groups preserve semantic editing regions while avoiding internal overlapping shells.
    groups={name:obj.vertex_groups.new(name=name) for name in ['early-coil','broad-outer-whorl','paired-shoulder-nodes','solid-terminal-break']}
    for vi,(side,j,i) in enumerate(vertex_labels):
        u=0 if j==0 else us[j-1]; s=i/N
        groups['early-coil' if u<0.49 else 'broad-outer-whorl'].add([vi],1.,'REPLACE')
        if u>0.87 and 0.07<s<0.67: groups['paired-shoulder-nodes'].add([vi],1.,'REPLACE')
        if s>end and u>0.5: groups['solid-terminal-break'].add([vi],1.,'REPLACE')
    source=audit_source(c,max_triangles=24000)
    if source['errors']: raise RuntimeError(source['errors'])
    bm=bmesh.new(); bm.from_mesh(obj.data); vol=bm.calc_volume(signed=True); bm.free()
    if vol<=0: raise RuntimeError('Mesh has non-positive signed volume')
    bpy.context.scene['construction_profile']=cfg['generator_profile']
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in c.all_objects: o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['ceratites']
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available: raise RuntimeError('Missing exporter options: '+str(set(opts)-available))
    bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb(out/'model.glb',24000,6,16)
    if glb['errors']: raise RuntimeError(glb['errors'])
    if glb['bytes']>2500000: raise RuntimeError('GLB size budget exceeded')
    b=source['bounds_blender_m']; expected_min=[b['min'][0],b['min'][2],-b['max'][1]]; expected_max=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][key][i]-expected[i]) for key,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
    if delta>1e-4 or glb['scene_triangles']!=source['triangles']: raise RuntimeError('Source/export mismatch')
    write(out/'build-report.json',{'asset_id':'ceratites','revision':'r001','blender_version':bpy.app.version_string,'generator_sha256':digest(__file__),'params_sha256':digest(HERE/'params.json'),'source':source,'glb':glb,'positive_signed_volume_m3':vol,'source_export_max_bbox_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'warnings_reviewed':['Intentional smooth body normals preserve broad ammonoid flanks. Low-poly topology remains explicit, un-subdivided and editable.'],'interpretation':cfg['interpretation'],'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend')})
    print('BUILD_OK',glb['sha256'],source['triangles'])
if __name__=='__main__': main()
