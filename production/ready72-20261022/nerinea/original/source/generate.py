#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Nerinea study. Run: blender -b -t 2 --python generate.py -- --output DIR.
Requires only params.json, copied deps, Blender 4.3.2 and its bundled Python.
No paper, image, absolute model path, network or external geometry is read.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import bpy, bmesh
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def interp(points,z):
    for (z0,r0),(z1,r1) in zip(points,points[1:]):
        if z<=z1:
            t=max(0,min(1,(z-z0)/(z1-z0)))
            return r0+(r1-r0)*t
    return points[-1][1]
def clamp(v,a=0,b=1): return max(a,min(b,v))
def angle_delta(a,b): return (a-b+math.pi)%(2*math.pi)-math.pi

def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--gray',action='store_true');a=ap.parse_args(args)
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((SOURCE/'params.json').read_text()); c=setup_scene('nerinea',seed=p['seed'])
    materials=[make_material(n,('#A0A0A0' if a.gray else color),roughness=0.91) for n,color in p['palette'].items()]
    h=p['height_m'];nr=p['axial_rings'];nt=p['circumference_segments'];A=p['aperture'];vertices=[];uv=[]
    # Non-uniform vertical density follows logarithmic whorl spacing. Bottom receives
    # enough samples to resolve a narrow worn aperture without a separate floating lip.
    zlevels=[0.016*i/42 for i in range(43)]
    zlevels += [0.016+(h-0.016)*(1-(1-i/(nr-42))**1.38) for i in range(1,nr-42+1)]
    for z in zlevels:
        base=interp(p['profile_z_radius_m'],z)
        cx=0.0012*clamp(z/0.014)+0.00045*clamp((z-0.04)/0.019)-0.0021*math.exp(-((z-0.0045)/0.004)**2)*clamp(z/0.0013)
        cy=0.0005*math.sin(math.pi*z/h)*clamp(z/0.012)
        for j in range(nt):
            th=2*math.pi*j/nt
            # Continuous dextral helical relief: z increases with theta on a
            # constant phase, right-handed screw convention. Not stacked rings.
            q=p['whorls']*math.log(1+2*max(0,h-z)/(h-0.016))/math.log(3)
            phase=q+th/(2*math.pi)+0.20
            dist=(phase+0.5)%1-0.5
            spire=clamp((z-0.014)/0.004)
            amplitude=p['suture_depth_m']*clamp(base/0.004,0.28,1)
            groove=-amplitude*math.exp(-(dist/0.105)**2)
            # Broad flattened flank with a very modest upper shoulder.
            shoulder=0.00011*clamp(base/0.005,0.2,1)*math.exp(-((dist-0.24)/0.24)**2)
            r=base+spire*(groove+shoulder)
            # Broad subdued erosion, independent of photographic pixels.
            wear=0.00008*clamp(base/0.005,0,1)*(math.sin(3*th+z*310)+0.45*math.sin(7*th-z*460)+0.35*math.sin(13*th+z*900))
            r+=wear
            # The front-right preserved mouth is a shallow irregular mineral-filled inset.
            # It is continuous with the body surface and NOT a deep reconstructed tunnel.
            v=(z-A['center_z_m'])/A['half_height_m']
            center=math.radians(A['center_angle_deg']) + 0.20*v
            u=angle_delta(th,center)/A['half_angle_rad']
            d=math.sqrt(u*u+v*v)
            rim=A['rim_height_m']*math.exp(-((d-0.92)/0.15)**2)
            inset=A['depth_m']*max(0,1-d*d)**0.72
            mineral_fill=inset*0.66*(0.92+0.08*math.sin(u*4+v*3))-0.0006*math.exp(-((u+0.38)/0.20)**2-((v-0.30)/0.36)**2)
            r+=rim-inset+mineral_fill+0.0012*math.exp(-((z-0.009)/0.005)**2)*math.exp(-(angle_delta(th,math.radians(-32))/0.85)**2)
            vertices.append((cx+r*math.cos(th),cy+p['depth_ratio']*r*math.sin(th),z))
            uv.append((z,th,d,u,v))
    rings=len(zlevels);faces=[];face_info=[]
    for i in range(rings-1):
        for j in range(nt):
            k=(j+1)%nt
            # Explicit stable diagonal winding; mildly faceted rings retain coherent shading.
            a0=i*nt+j;b0=i*nt+k;c0=(i+1)*nt+k;d0=(i+1)*nt+j
            if (i+j)%2: tris=[(a0,b0,d0),(b0,c0,d0)]
            else: tris=[(a0,b0,c0),(a0,c0,d0)]
            faces.extend(tris)
    bot=len(vertices);vertices.append((0,0,0));top=len(vertices);vertices.append((0.00165,0,h))
    for j in range(nt):
        faces.append((bot,(j+1)%nt,j));faces.append((top,(rings-1)*nt+j,(rings-1)*nt+(j+1)%nt))
    obj=mesh_object('continuous-dextral-shell-and-preserved-mouth',vertices,faces,materials,c)
    for f in obj.data.polygons:
        co=f.center
        z=sum(vertices[k][2] for k in f.vertices)/len(f.vertices)
        pts=[uv[k] for k in f.vertices if k<len(uv)]
        md=sum(x[2] for x in pts)/len(pts)
        vv=sum(x[4] for x in pts)/len(pts)
        uu=sum(x[3] for x in pts)/len(pts)
        theta=sum(x[1] for x in pts)/len(pts)
        # Restrained coherent tone patches, not stripes or pseudo-biological ornament.
        pat=math.sin(3*theta+z*170)+0.45*math.sin(5*theta-z*280)
        f.material_index=3 if md<0.67 and vv>0.0 and uu<-0.1 else 2 if md<0.83 else 1 if pat>1.12 else 0
        f.use_smooth=False
    obj['construction']='Single continuous closed profile loft with dextral suture relief, integrated shallow aperture and short basal extension'
    obj['observed']='External taper, near-complete small preserved mouth and proportions based on Kollmann 2014 Fig5C'
    obj['inferred']='Far side, 21mm approximate depth, unseen lip thickness and shallow mineral-filled cavity'
    obj['specimen_anchor']='Nerinea mosae MNHN.F.A49004; original interpretation, not a scan'
    bpy.context.view_layer.update()
    source=audit_source(c,p['geometry_policy']['max_triangles'])
    # Exact mathematical manifold/volume checks supplement helper's topology report.
    bm=bmesh.new();bm.from_mesh(obj.data)
    topology={'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'faces':len(bm.faces),'vertices':len(bm.verts),'components_expected':1};bm.free()
    source['topology']=topology
    if source['errors']: write(out/'source-qa.json',source);raise RuntimeError(str(source['errors']))
    bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in c.all_objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[c['asset_root']]
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available: raise RuntimeError('Required exporter flags unavailable')
    bpy.ops.export_scene.gltf(**opts)
    G=p['geometry_policy'];glb=audit_glb(out/'model.glb',G['max_triangles'],G['max_materials'],G['max_primitives'])
    if glb['errors']:raise RuntimeError(str(glb['errors']))
    if glb['bytes']>G['max_glb_bytes']:raise RuntimeError('Byte budget exceeded')
    b=source['bounds_blender_m'];mins=[b['min'][0],b['min'][2],-b['max'][1]];maxs=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][key][i]-expected[i]) for key,expected in [('min',mins),('max',maxs)] for i in range(3))
    assert delta<1e-6 and source['triangles']==glb['scene_triangles']
    record={'asset_id':p['asset_id'],'revision':p['revision'],'scope':'Maker build and static integrity, not independent acceptance','blender_version':bpy.app.version_string,'exporter_version':'4.3.47','source_sha256':digest(__file__),'params_sha256':digest(SOURCE/'params.json'),'gray':a.gray,'source':source,'glb':glb,'source_export_bounds_max_delta_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'model_blend_sha256':digest(out/'model.blend'),'source_scene_contains_cameras_or_lights':any(o.type in ['CAMERA','LIGHT'] for o in bpy.data.objects),'target_runtime':{'three':'0.180.0','gpu':'NOT_RUN','populated_scene':'NOT_RUN'},'inference':p['uncertainty']}
    write(out/'build-report.json',record)
    print(json.dumps({'status':'BUILT_NOT_INDEPENDENTLY_REVIEWED','output':str(out),'triangles':glb['scene_triangles'],'bytes':glb['bytes'],'glb_sha256':glb['sha256'],'bounds':glb['bounds_m'],'topology':topology}))
if __name__=='__main__':main()
