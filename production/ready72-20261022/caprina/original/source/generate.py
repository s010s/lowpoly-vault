#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original paired-valve Caprina fossil study, IGM-6448. No source imagery is loaded.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out DIR
Optional --clay makes a private shape diagnostic, not the delivered asset.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
import io_scene_gltf2
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source, _vertices_world, _bounds
from qa_glb import audit_glb

P=Path(__file__).resolve().parent
params=json.loads((P/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=P.parent); ap.add_argument('--clay',action='store_true'); args=ap.parse_args(argv)
out=args.out.resolve(); out.mkdir(parents=True,exist_ok=True); evidence=out/'qa/evidence'; evidence.mkdir(parents=True,exist_ok=True)
coll=setup_scene(params['asset_id'],params['seed']); root=bpy.data.objects[coll['asset_root']]
root['taxon']='Caprina sp.'; root['reference_specimen']='IGM-6448, Plate II Fig. 9, Pantoja-Alor et al. 1994'
root['interpretation']='Original fossil interpretation. Scale and hidden depth estimated. No restored basal extension.'
root['anatomy']='Two unequal valves, external hook concavity, no shell aperture or invented canals.'
palette=[('#A59D8B','weathered_limestone_shell'),('#B2A995','pale_growth_laminae'),('#908977','mineral_stained_shell'),('#BEB39E','exposed_fossil_break')]
if args.clay: palette=[('#999999',n) for c,n in palette]
mats=[make_material(n,c,roughness=0.9) for c,n in palette]

# Catmull-Rom of measured-by-eye posterior projected contour stations, in mm.
def interp(stations,t):
    v=t*(len(stations)-1); i=min(int(v),len(stations)-2); q=v-i
    a=stations[max(0,i-1)]; b=stations[i]; c=stations[i+1]; d=stations[min(len(stations)-1,i+2)]
    return [0.5*((2*b[k])+(-a[k]+c[k])*q+(2*a[k]-5*b[k]+4*c[k]-d[k])*q*q+(-a[k]+3*b[k]-3*c[k]+d[k])*q*q*q) for k in range(len(b))]

def loft(name,stations,rings,sides,phase,paired=False):
    vv=[]; ff=[]; slots=[]
    for j in range(rings):
        t=j/(rings-1)
        if paired:
            ox,oz,ix,iz,dep,y=interp(stations,t)
            x=(ox+ix)/2;z=(oz+iz)/2;rad=math.hypot(ox-ix,oz-iz)/2
        else:
            x,y,z,rad,dep=interp(stations,t)
        pm=interp(stations,max(0,t-0.0001)); pp=interp(stations,min(1,t+0.0001))
        tangent=Vector((pp[0]-pm[0],0,pp[2]-pm[2])).normalized()
        across=Vector((ox-ix,0,oz-iz)).normalized() if paired else Vector((1,0,0))
        for k in range(sides):
            a=2*math.pi*k/sides
            # Broad irregular growth corrugations; not repeated extruded rings.
            wave=math.sin(2*math.pi*(t*13.2)+0.45*math.sin(3*a+phase))
            ridge=0.22*(max(0,wave)**4-0.17)
            weather=0.16*math.sin(17.7*t+3*a+phase)+0.13*math.sin(53*t-7*a+1.9*phase)+0.09*math.sin(91*t+11*a)
            longwave=0.16*math.sin(5*a+5*t+phase)
            edge=(math.exp(-t*30)+math.exp(-(1-t)*30))*(0.32*math.sin(7*a+phase)+0.17*math.sin(11*a))
            relief_factor=max(0.20,1.0-3.0*max(0,t-0.55)) if paired else 1.0
            if paired and t>0.40:
                relief_factor*=0.20+0.80*max(0,math.cos(a))**2
            ridge*=relief_factor; weather*=relief_factor; longwave*=relief_factor; edge*=relief_factor
            r=rad+ridge+weather+longwave+edge
            depth=dep+0.8*ridge+weather+0.6*longwave
            point=Vector((x,y,z))+across*(r*math.cos(a))+Vector((0,depth*math.sin(a),0))
            # Small preserved chips disturb the broken terminal rim, not new anatomy.
            chip_weight=math.exp(-(1-t)*22) if paired else math.exp(-t*22)
            point.z+=chip_weight*(0.34*math.sin(3*a+phase)+0.20*math.sin(7*a))
            vv.append(tuple(point*0.001))
    for j in range(rings-1):
        t=(j+0.5)/(rings-1)
        for k in range(sides):
            a=2*math.pi*(k+0.5)/sides
            # Large coherent mineral patches, avoiding per-triangle confetti.
            shade=math.sin(8.5*t+1.7*math.sin(2*a)+phase)+0.4*math.sin(16*t-3*a)
            idx=1 if shade>0.95 else 2 if shade< -1.0 else 0
            u=j*sides+k; v=j*sides+(k+1)%sides; w=(j+1)*sides+(k+1)%sides; q=(j+1)*sides+k
            ff.extend([(u,v,w),(u,w,q)]); slots.extend([idx,idx])
    # Preserved blunt broken ends are solid weathered faces, not open apertures.
    for j in (0,rings-1):
        ring=vv[j*sides:(j+1)*sides]; center=tuple(sum(v[k] for v in ring)/sides for k in range(3)); ci=len(vv); vv.append(center)
        for k in range(sides):
            ff.append((ci,j*sides+k,j*sides+(k+1)%sides)); slots.append(3)
    obj=mesh_object(name,vv,ff,mats,coll)
    for face,idx in zip(obj.data.polygons,slots): face.material_index=idx
    obj['part_interpretation']='Asymmetrical fossil valve, closed material volume; hidden reverse inferred.'
    return obj

lower=loft('attached_lower_valve',params['lofts']['lower_stations_mm'],params['lofts']['lower_rings'],params['lofts']['sides'],0.4)
upper=loft('curved_free_valve',params['lofts']['upper_stations_mm'],params['lofts']['upper_rings'],params['lofts']['sides'],2.3,paired=True)
# Lock the prepared rounded 50 x 35 x 60 mm envelope. The values are estimates,
# not a claim of precise caliper measurements of the fossil.
lo,hi=_bounds(_vertices_world(coll))
if 'normalization_reference' in params:
    lo=params['normalization_reference']['min']; hi=params['normalization_reference']['max']
scale=[params['width']/(hi[0]-lo[0]),params['depth']/(hi[1]-lo[1]),params['height']/(hi[2]-lo[2])]
for obj in (lower,upper):
    for v in obj.data.vertices:
        v.co.x=(v.co.x-(lo[0]+hi[0])/2)*scale[0]
        v.co.y=(v.co.y-(lo[1]+hi[1])/2)*scale[1]
        v.co.z=(v.co.z-lo[2])*scale[2]
    obj.data.update()
# Root stays at lowest preserved attached-valve footprint, not bbox center.
low_ring=[v.co for v in lower.data.vertices[:params['lofts']['sides']]]
foot=Vector((sum(v.x for v in low_ring)/len(low_ring),sum(v.y for v in low_ring)/len(low_ring),0))
for obj in (lower,upper):
    for v in obj.data.vertices: v.co-=foot
    obj.data.update()
root['origin']='Lowest preserved attached-valve mounting point; fracture edge, not a fabricated foot.'
bpy.context.view_layer.update()
source=audit_source(coll,params['geometry_policy']['max_triangles'])
if source['errors']: raise RuntimeError(source['errors'])
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
bpy.ops.object.select_all(action='DESELECT')
for obj in coll.all_objects: obj.select_set(True)
bpy.context.view_layer.objects.active=root
opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
if set(opts)-available: raise RuntimeError('Missing exporter options: '+repr(set(opts)-available))
bpy.ops.export_scene.gltf(**opts)
glb=audit_glb(out/'model.glb',params['geometry_policy']['max_triangles'],params['geometry_policy']['max_materials'],params['geometry_policy']['max_primitives'])
if glb['errors']: raise RuntimeError(glb['errors'])
if glb['bytes']>params['geometry_policy']['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
b=source['bounds_blender_m']; emin=[b['min'][0],b['min'][2],-b['max'][1]]; emax=[b['max'][0],b['max'][2],-b['min'][1]]
delta=max(abs(glb['bounds_m'][which][i]-expected[i]) for which,expected in [('min',emin),('max',emax)] for i in range(3))
if delta>1e-7 or source['triangles']!=glb['scene_triangles']: raise RuntimeError('Export geometry mismatch')
report={'schema_version':1,'asset_id':params['asset_id'],'revision':params['revision'],'status':'PASS','claim_scope':'Source geometry and emitted static GLB only; not independent visual or factual approval.','blender_version':bpy.app.version_string,'glb_exporter_version':'.'.join(map(str,io_scene_gltf2.bl_info['version'])),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((P/'params.json').read_bytes()).hexdigest(),'source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_blend_sha256':hashlib.sha256((out/'model.blend').read_bytes()).hexdigest(),'scaling_note':params['note'],'materials':[{'name':n,'srgb':c} for c,n in palette]}
(evidence/'geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('CAPRINA_BUILD',json.dumps({'out':str(out),'triangles':glb['scene_triangles'],'bytes':glb['bytes'],'sha256':glb['sha256'],'semantic':glb.get('semantic_sha256')}))
