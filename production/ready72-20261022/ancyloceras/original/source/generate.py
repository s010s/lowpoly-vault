# SPDX-License-Identifier: MIT
"""Original deterministic compressed fossil loft. Blender -b -t 2 --python generate.py -- --output DIR.
Only params.json and declared local deps are read. No source image is embedded.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,data): Path(p).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--clay',action='store_true')
    args=ap.parse_args(av);out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text());cp=p['source_control_points_pixels']
    col=setup_scene(p['asset_id'],p['seed']);root=bpy.data.objects[col['asset_root']]
    root['interpretation']='Compressed and historically repaired MNHN.F.B46086-informed fossil, not pristine living shell.'
    root['repair_uncertainty']='Subdued early coil bridge is indicative; exact angular extent of historical plaster is not established.'
    root['reference']='Delanoy and Baudouin 2023, Fig.2; MNHN.F.B46086'
    def point(t):
        i=min(int(t),len(cp)-2);f=t-i;a=cp[max(0,i-1)];b=cp[i];c=cp[i+1];d=cp[min(len(cp)-1,i+2)]
        return [0.5*((2*b[k])+(-a[k]+c[k])*f+(2*a[k]-5*b[k]+4*c[k]-d[k])*f*f+(-a[k]+3*b[k]-3*c[k]+d[k])*f*f*f) for k in range(3)]
    dense=[point((len(cp)-1)*i/4000) for i in range(4001)];lengths=[0.]
    for a,b in zip(dense,dense[1:]):lengths.append(lengths[-1]+math.hypot(b[0]-a[0],b[1]-a[1]))
    total=lengths[-1];rings=p['ring_count'];sides=p['cross_section_sides'];stations=[];idx=0
    for i in range(rings):
        s=total*i/(rings-1)
        while idx<len(lengths)-2 and lengths[idx+1]<s:idx+=1
        f=(s-lengths[idx])/(lengths[idx+1]-lengths[idx]);v=[dense[idx][k]*(1-f)+dense[idx+1][k]*f for k in range(3)];stations.append((s,v))
    mats=[make_material(n,'#999999' if args.clay else c,roughness=.94) for n,c in zip(['Fossil-matrix','Weathered-dark','Weathered-light','Documented-plaster-inferred-bridge','Mineral-filled-termination'],p['palette'])]
    verts=[];faces=[];mis=[];repair_stations=[];phase=0.;prior_s=0
    for i,(s,(x,z,r)) in enumerate(stations):
        prev=stations[max(0,i-1)][1];nxt=stations[min(rings-1,i+1)][1]
        tangent=Vector((nxt[0]-prev[0],0,-(nxt[1]-prev[1]))).normalized();normal=Vector((tangent.z,0,-tangent.x))
        ry=7.+.275*r;phase+=(s-prior_s)/((16.+.34*r)*(1+.08*math.sin(s*.021)));prior_s=s
        repair=(18.<=2*r*.374<=27.) and s<total*.21
        if repair:repair_stations.append(i)
        endfade=min(1.,i/4.,(rings-1-i)/7.)
        for j in range(sides):
            a=2*math.pi*j/sides
            q=phase+.21*math.cos(a)+.08*math.sin(a*2)+.045*math.sin(s*.018)
            peak=max(0,math.cos(2*math.pi*q))**2;minor=max(0,math.cos(2*math.pi*(q+.5)))**5
            strength=(1.+.052*r)*(.13 if repair else 1.)*endfade*(.85+.15*math.sin(phase*2.1))
            rib=strength*(peak+(.50 if s<total*.25 else .35 if s<total*.75 else .14)*minor)
            nodules=(max(0,math.cos(a-4.0))**12+max(0,math.cos(a-5.4))**12+max(0,math.cos(a-1.2))**14)*peak*(.4+.027*r)*endfade
            rough=(math.sin(s*.107+a*3)+.48*math.sin(s*.247-a*5))*(.23+.009*r)*(.15 if repair else 1.)
            rr=r+rib*.38+rough;depth=(ry+rib+nodules+rough*.45)*(1+.045*math.cos(a*3+s*.015))
            pt=Vector((x-445,0,995-z))+normal*(rr*math.cos(a))+Vector((0,depth*math.sin(a),0));verts.append(tuple(pt))
        if i:
            for j in range(sides):
                faces.append(((i-1)*sides+j,(i-1)*sides+(j+1)%sides,i*sides+(j+1)%sides,i*sides+j))
                a=2*math.pi*(j+.5)/sides;tone=math.sin(s*.012+a*2)+.5*math.sin(s*.034-a)
                mis.append(3 if repair else 1 if tone<-1.05 else 2 if tone>1.24 else 0)
    for ri in (0,rings-1):
        ring=[Vector(verts[ri*sides+j]) for j in range(sides)];center=sum(ring,Vector())/sides;last=ri*sides
        if ri:
            prev=stations[-2][1];end=stations[-1][1];forward=Vector((end[0]-prev[0],0,prev[1]-end[1])).normalized();radius=end[2]
            for shrink,depth in ((.86,.32),(.48,.57)):
                start=len(verts)
                for j in range(sides):
                    a=2*math.pi*j/sides
                    verts.append(tuple(center+(ring[j]-center)*shrink+forward*radius*(depth+.045*math.sin(a*3)+.035*math.cos(a*5))))
                for j in range(sides):faces.append((last+j,last+(j+1)%sides,start+(j+1)%sides,start+j));mis.append(4)
                last=start
            center+=forward*radius*.69
        else:center+=Vector((.1,0,.2))
        ci=len(verts);verts.append(tuple(center))
        for j in range(sides):faces.append((last+j,last+(j+1)%sides,ci));mis.append(4)
    lo=[min(v[k] for v in verts) for k in range(3)];hi=[max(v[k] for v in verts) for k in range(3)];target=[p['width_estimate'],p['axial_thickness_estimate'],p['height']];scale=[target[k]/(hi[k]-lo[k]) for k in range(3)]
    verts=[((v[0]-(lo[0]+hi[0])/2)*scale[0],(v[1]-(lo[1]+hi[1])/2)*scale[1],(v[2]-lo[2])*scale[2]) for v in verts]
    obj=mesh_object('Continuous-compressed-coil-shaft-crook',verts,faces,mats,col)
    for poly,mi in zip(obj.data.polygons,mis):poly.material_index=mi
    obj['geometry']='Single closed manifold loft with continuous integrated ribs, worn filled caps and subdued inferred repair.';obj['repair_stations']=json.dumps([min(repair_stations),max(repair_stations)]);obj['repair_is_uncertain']=True
    source=audit_source(col,max_triangles=24000)
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=root;bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2;bpy.context.scene['generator_parameters']=json.dumps(p,ensure_ascii=False)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    rna=bpy.ops.export_scene.gltf.get_rna_type().properties;missing=[k for k in opts if k not in rna]
    if missing:raise RuntimeError('Exporter profile unavailable: '+repr(missing))
    bpy.ops.export_scene.gltf(**opts)
    exported=audit_glb(out/'model.glb',max_triangles=24000,max_materials=6,max_primitives=16)
    if exported['errors']:raise RuntimeError(exported['errors'])
    dims=source['bounds_blender_m']['size']
    save(out/'build-report.json',{'asset_id':p['asset_id'],'revision':p['revision'],'blender':bpy.app.version_string,'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'source':source,'exported':exported,'expected_gltf_dimensions_m':[dims[0],dims[2],dims[1]],'export_options':opts|{'filepath':'model.glb'},'clay':args.clay,'seed':p['seed'],'repair_station_interval':[min(repair_stations),max(repair_stations)],'geometry_definition':'single manifold, integrated low blunt ribs, compressed irregular oval cross-sections','epistemic_limit':'Interpretation, not photogrammetry. Plaster angular extent and maximum thickness not precisely established.'})
    print('BUILD_OK '+str(out))
if __name__=='__main__':main()
