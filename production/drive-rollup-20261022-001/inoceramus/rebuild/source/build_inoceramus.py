# SPDX-License-Identifier: MIT
"""Deterministic original geometry; no photo tracing/texture use. Run with Blender 4.3.2."""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'helpers'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
ap=argparse.ArgumentParser(); ap.add_argument('--params',type=Path,required=True); ap.add_argument('--output-root',type=Path,required=True)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]); p=json.loads(a.params.read_text())
C=setup_scene(p['asset_id'],p['seed']); N=p['segments']; R=p['growth_rings']
M=[make_material(n,c,roughness=.9) for n,c in zip(['fossil-limestone','weathered-cream','muted-grey','reverse-closure'],p['palette'])]
verts=[]; faces=[]; face_mats=[]; front_ids=[]; back_ids=[]
def planar(t,ang):
    si=math.sin(ang); co=math.cos(ang)
    # Asymmetrically expanding growth ovals, narrower above and broader below.
    x=p['apex_x_m']+p['growth_center_x_m']*t+p['width_radius_m']*t*co*(1-.19*si)
    z=p['apex_z_m']+p['growth_center_z_m']*t+p['height_radius_m']*t*si
    x+=.0021*t*t*math.sin(3*ang+.4); z+=.0010*t*t*math.sin(4*ang+.6)
    return x,z

def front_depth(t,ang):
    base=p['rim_depth_m']+p['umbo_depth_m']*((1-t)**.77)+.0035*math.sin(math.pi*t)
    # Softer compressed dorsal arcs; six rounded folds, not independent stacked shells.
    arc=.38+.62*((1-math.sin(ang))/2)**.55
    fold=sum(amp*math.exp(-((t-c)/p['fold_width'])**2) for c,amp in zip(p['fold_centers'],p['fold_amplitudes_m']))
    natural=.00045*t*(1-t)*(math.sin(7*ang+5*t)+.5*math.cos(11*ang-3*t))
    return base+arc*fold+natural

def addface(f,mid): faces.append(f); face_mats.append(mid)
verts.append((p['apex_x_m'],-front_depth(0,0),p['apex_z_m'])); front_ids.append(0)
front_rings=[]
for k in range(1,R+1):
    t=k/R; ids=[]
    for j in range(N):
        ang=2*math.pi*j/N
        # Small deterministic angular/radial staggering breaks machine-perfect spokes.
        ang+=.010*math.sin(j*2.31+k*.74)*math.sin(math.pi*t)
        tt=t+.0017*math.sin(j*1.37+k*.62)*math.sin(math.pi*t)
        x,z=planar(tt,ang); ids.append(len(verts)); front_ids.append(len(verts)); verts.append((x,-front_depth(tt,ang),z))
    front_rings.append(ids)
for j in range(N): addface((0,front_rings[0][j],front_rings[0][(j+1)%N]),0)
for k in range(R-1):
    for j in range(N):
        ja=(j+1)%N; aa=front_rings[k][j]; bb=front_rings[k][ja]; cc=front_rings[k+1][ja]; dd=front_rings[k+1][j]
        ang=2*math.pi*(j+.5)/N; t=(k+1.5)/R
        tone=math.sin(ang*2.7+t*7)+.38*math.sin(ang*6-t*8)
        mid=1 if tone>.98 else 2 if tone<-.99 else 0
        if (j+k)%2: addface((aa,bb,dd),mid); addface((bb,cc,dd),mid)
        else: addface((aa,bb,cc),mid); addface((aa,cc,dd),mid)
# Conservative reverse closure. This is not a diagnostic fossil interior or another valve.
back_center=len(verts); verts.append((p['apex_x_m'],p['reverse_depth_m'],p['apex_z_m'])); back_ids.append(back_center)
back_rings=[]
for k in range(1,p['reverse_rings']):
    t=k/p['reverse_rings']; ids=[]
    for j in range(N):
        ang=2*math.pi*j/N; x,z=planar(t,ang)
        y=p['reverse_depth_m']*(1-t*t)-p['rim_depth_m']*t*t
        ids.append(len(verts)); back_ids.append(len(verts)); verts.append((x,y,z))
    back_rings.append(ids)
back_rings.append(front_rings[-1])
for j in range(N): addface((back_center,back_rings[0][(j+1)%N],back_rings[0][j]),3)
for k in range(len(back_rings)-1):
    for j in range(N):
        ja=(j+1)%N; aa=back_rings[k][j]; bb=back_rings[k][ja]; cc=back_rings[k+1][ja]; dd=back_rings[k+1][j]
        addface((aa,dd,cc),3); addface((aa,cc,bb),3)
# Preserve real 180 mm height; mounting origin is lowest basal rim point, not a unit-box normalization.
zmin=min(v[2] for v in verts); zmax=max(v[2] for v in verts); scale=p['height_m']/(zmax-zmin)
bottom=min(verts,key=lambda v:v[2]); ox,oy=bottom[:2]
verts=[((x-ox)*scale,(y-oy)*scale,(z-zmin)*scale) for x,y,z in verts]
obj=mesh_object('single-valve-concentric-fold-surface',verts,faces,M,C)
for poly,mid in zip(obj.data.polygons,face_mats): poly.material_index=mid
for name,ids in [('outer-folds-supported-form',front_ids),('reverse-artistic-closure',back_ids),('basal-rim',front_rings[-1])]:
    vg=obj.vertex_groups.new(name=name); vg.add(ids,1,'REPLACE')
obj['construction']='One continuous closed single-valve fossil solid; outer growth mesh with plain reverse closure.'
obj['reverse_uncertainty']='Reverse depth and closure are artistic non-diagnostic completion, not measured interior anatomy.'
obj['reference']='Niebuhr & Wilmsen 2023 Figure 4, BGR Ma 14105; genus-level form, not exact specimen replica.'
metadata={'description':{'en':'Original single-valve Inoceramus fossil-form study with broad oblique growth folds; reverse and thickness are artistic completion.','zh':'单瓣 Inoceramus 化石形态原创低多边形模型，保留宽斜同心生长褶；背面与厚度为艺术补全。'},'representation':'fossil-specimen','taxon':'Inoceramus','scientific_anchor':'I. stuemckei BGR Ma 14105, 180 mm right valve, lower–middle Upper Turonian','generator':'source/build_inoceramus.py','params':'source/params.json','generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256(a.params.read_bytes()).hexdigest(),'sources':['https://doi.org/10.1007/s12542-022-00615-9'],'uncertainty':['Not an exact museum replica or scan.','Width, thickness and plain reverse closure are artistic estimates.','Stone colors, low-poly faceting and upright mounting are presentation choices.'],'source_media_incorporated':False,'runtime_three_version':'0.180.0','art_direction':'Palette-only static faceted geometry; no radial fan ribs, paired valve, spiral, soft tissue or rock matrix.'}
record=export_asset(p['asset_id'],{'en':'Inoceramus single-valve fossil form','zh':'Inoceramus 单瓣化石形态'},'animals',C,metadata=metadata,output_root=a.output_root,render=False,max_triangles=p['max_triangles'],max_materials=p['max_materials'],max_primitives=p['max_primitives'])
# Additional source geometric facts, not an independent visual verdict.
obj.data.calc_loop_triangles(); signed_volume=sum(Vector(obj.data.vertices[t.vertices[0]].co).dot(Vector(obj.data.vertices[t.vertices[1]].co).cross(Vector(obj.data.vertices[t.vertices[2]].co)))/6 for t in obj.data.loop_triangles)
report={'blender_version':bpy.app.version_string,'exporter_version':getattr(__import__('io_scene_gltf2'),'bl_info',{}).get('version'),'vertices':len(obj.data.vertices),'polygons':len(obj.data.polygons),'triangles':len(obj.data.loop_triangles),'signed_volume_m3':signed_volume,'positive_signed_volume':signed_volume>0,'source_meshes':1,'front_vertices':len(front_ids),'reverse_vertices':len(back_ids),'material_count':len(M),'height_m':max(v[2] for v in verts),'mounting_origin':'lowest basal rim contact','stage_objects':len([o for o in bpy.data.objects if o.type in {'CAMERA','LIGHT'}]),'glb_sha256':record['sha256']['glb'],'source_claim':'closed manifold construction, not proof of fossil anatomy or printability'}
(a.output_root/p['asset_id']/'construction-report.json').write_text(json.dumps(report,indent=2)+'\n')
print('BUILD_COMPLETE',json.dumps(report))
