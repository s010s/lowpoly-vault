#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original recovery specimen, not recovered historical geometry.

Run on Blender 4.3.2. All dimensions are meters after explicit mm conversion.
Scientific limitations live in the frozen brief; concept imagery is not a mesh.
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, math, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
import bpy, bmesh
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
from asset_common import setup_scene, make_material, mesh_object, export_asset


def interpolate(points, t, field):
    # Nonuniform cubic Hermite centerline/profile avoids discontinuous ring axes.
    for i,(a,b) in enumerate(zip(points,points[1:])):
        if t<=b['t']:
            h=b['t']-a['t']; u=(t-a['t'])/h
            left=points[max(0,i-1)]; right=points[min(len(points)-1,i+2)]
            ma=(b[field]-left[field])/(b['t']-left['t'])
            mb=(right[field]-a[field])/(right['t']-a['t'])
            return (2*u**3-3*u*u+1)*a[field]+(u**3-2*u*u+u)*h*ma+(-2*u**3+3*u*u)*b[field]+(u**3-u*u)*h*mb
    return points[-1][field]


def build(config):
    col = setup_scene(config['asset_id'], config['seed'])
    mats = [make_material(p['name'], p['hex'], roughness=.88) for p in config['palette']]
    points=config['control_profile_mm']; sides=config['cross_section_sides']; count=config['loft_samples']
    verts=[]; faces=[]; material_ids=[]
    # Primary continuous shell mass; cross sections follow a short curved axis.
    for k in range(count+1):
        t=k/count
        cy=interpolate(points,t,'y'); cz=interpolate(points,t,'z')
        ta=max(0,t-.001); tb=min(1,t+.001)
        dy=interpolate(points,tb,'y')-interpolate(points,ta,'y')
        dz=interpolate(points,tb,'z')-interpolate(points,ta,'z')
        tangent=Vector((0,dy,dz)).normalized(); radial=Vector((0,tangent.z,-tangent.y))
        rx=interpolate(points,t,'rx'); ry=interpolate(points,t,'ry')
        relief=config['growth_relief_mm']*math.sin(t*config['growth_cycles']*2*math.pi)*(1-.75*t)
        for i in range(sides):
            a=2*math.pi*i/sides
            # Organized imperfection only at missing apex; no random facet noise.
            break_offset=(.22*math.sin(3*a)+.12*math.cos(5*a))*(1-t)**12
            p=Vector((0,cy,cz))+Vector((rx*math.cos(a),0,0))+radial*((ry+relief)*math.sin(a))+tangent*break_offset
            verts.append(tuple(p*.001))
        if k:
            for i in range(sides):
                j=(i+1)%sides
                faces.append(((k-1)*sides+i,(k-1)*sides+j,k*sides+j,k*sides+i))
                material_ids.append(1 if k<13 and k%4==0 else 0)
    # Closed sediment-bearing damaged end, not a restored apex or open pipe.
    base_center=Vector((0,points[0]['y'],points[0]['z']))*.001
    base_center+=Vector((0,.00015,.0001))
    q=len(verts);verts.append(tuple(base_center))
    for i in range(sides): faces.append((q,(i+1)%sides,i));material_ids.append(2)
    # Broad preserved contracted upper envelope; NOT an upward open bowl.
    q=len(verts);verts.append((0,points[-1]['y']*.001,(points[-1]['z']+.35)*.001))
    for i in range(sides): faces.append((q,count*sides+i,count*sides+(i+1)%sides));material_ids.append(0)
    obj=mesh_object('Preserved compressed cyrtocone',verts,faces,mats,col)
    for p,mat in zip(obj.data.polygons,material_ids):p.material_index=mat
    obj['specimen']='SM 75 holotype; damaged retained extent'
    obj['representation']='Original stylized preserved shell; hidden relief interpretive'
    obj['missing_apex']=True
    obj['no_restored_hyponomic_tube']=True
    # Surface-aware shallow U recess on expanded dorsal flank. On this expanding
    # flank its outward normal has +Y and -Z components, not the top-bowl +Z.
    outline=[(-5.65,4.35),(-6.15,3.7),(-5.9,2.75),(-5.25,1.9),(-4.95,-.9),(-4.25,-2.45),(-3,-3.65),(-1.5,-4.35),(0,-4.55),(1.5,-4.35),(3,-3.65),(4.25,-2.45),(4.95,-.9),(5.25,1.9),(5.9,2.75),(6.15,3.7),(5.65,4.35),(4.65,4.5),(3.75,3.8),(3.5,2.8),(3.85,1.6),(3.5,-.6),(2.9,-1.85),(2,-2.7),(1,-3.15),(0,-3.3),(-1,-3.15),(-2,-2.7),(-2.9,-1.85),(-3.5,-.6),(-3.85,1.6),(-3.5,2.8),(-3.75,3.8),(-4.65,4.5)]
    center_z=config['aperture_center_z_mm']; depth=config['aperture_depth_mm']
    def ring_at_z(z):
        lo=0.; hi=1.
        for _ in range(45):
            mid=(lo+hi)/2
            if interpolate(points,mid,'z')<z:lo=mid
            else:hi=mid
        t=(lo+hi)/2
        return tuple(interpolate(points,t,k) for k in ['y','rx','ry'])
    cutter_verts=[]
    for inner in [True,False]:
        for x,h in outline:
            z=center_z+h; cy,rx,ry=ring_at_z(z)
            y=cy+ry*math.sqrt(max(0,1-(x/rx)**2))
            # Depth floor follows the surface; it does not assume a deep cavity.
            cutter_verts.append((x*.001,(y-depth if inner else y+4)*.001,z*.001))
    n=len(outline); cutter_faces=[]
    poly=[Vector((x,h,0)) for x,h in outline]
    for tri in tessellate_polygon([poly]):
        ids=[v if isinstance(v,int) else next(i for i,p in enumerate(poly) if (p-v).length<1e-8) for v in tri]
        cutter_faces.extend([tuple(reversed(ids)),tuple(i+n for i in ids)])
    for i in range(n):j=(i+1)%n;cutter_faces.append((i,j,j+n,i+n))
    cut=mesh_object('TEMP shallow U cutter',cutter_verts,cutter_faces,mats[3],col)
    mod=obj.modifiers.new('Original shallow contracted U','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
    bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cut,do_unlink=True)
    # Conservative interrupted hyponomic remnant, not a reconstructed tube.
    # New damage connects the shallow remnant across the nearest upper crest.
    # The asymmetric edges and end truncation are declared stylization, not a
    # source-resolved fracture contour. The body and dorsal U remain unchanged.
    levels=config['hyponomic_damage_profile_mm']; vs=[]; fs=[]
    for z,left,right,floor_y in levels:
        vs.extend([(left*.001,-.018,z*.001),(right*.001,-.018,z*.001),
                   (right*.001,floor_y*.001,z*.001),(left*.001,floor_y*.001,z*.001)])
    fs.append((0,3,2,1))
    for k in range(1,len(levels)):
        a=(k-1)*4; b=k*4
        for i in range(4): j=(i+1)%4; fs.append((a+i,a+j,b+j,b+i))
    q=(len(levels)-1)*4;fs.append((q,q+1,q+2,q+3))
    cut=mesh_object('TEMP incomplete abraded hyponomic margin',vs,fs,mats[2],col)
    mod=obj.modifiers.new('Short interrupted damaged hyponomic rim','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut
    bpy.context.view_layer.objects.active=obj;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
    bm=bmesh.new();bm.from_mesh(obj.data)
    # Explicit microscopic Boolean sliver cleanup, at 0.02 mm, far below visible
    # aperture width. No helper tolerance is relaxed and full source QA still runs.
    before_vertices=len(bm.verts)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00002)
    bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=.00002)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    obj['boolean_cleanup_max_distance_m']=.00002
    obj['boolean_cleanup_vertices_removed']=before_vertices-len(bm.verts)
    bm.to_mesh(obj.data);bm.free()
    obj.data.shade_flat()
    # Keep all output in meters with an identity root and baked geometry origin.
    low=min(v.co.z for v in obj.data.vertices)
    for v in obj.data.vertices:v.co.z-=low
    obj['ground_shift_m']=-low
    obj['aperture_direction']='Dorsal +Y with downward -Z surface normal; no exact angle claim'
    bpy.context.scene['frozen_config_json']=json.dumps(config,sort_keys=True)
    return col


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    config=json.loads(args.config.read_text()); out=args.output_dir
    if out.exists() and any(out.iterdir()):raise RuntimeError('Output must be new and empty')
    col=build(config)
    record=export_asset(config['asset_id'],{'en':'Phragmoceras · SM 75 preserved shell','zh':'隔角石 · SM 75 缺损标本'},'animals',col,
        metadata={'description':{'en':'Evidence-informed stylized depiction of the damaged SM 75 holotype. Missing apex and incomplete hyponomic margin retained. Aperture depth, hidden surfaces and limestone palette are original conservative interpretations, not measured restoration.','zh':'依原文制作的 SM 75 缺损壳标本风格化表现；不补顶端及完整漏斗口。口腔深度、隐藏面及色彩属于明确标注的保守推定。'},
        'taxon':'Phragmoceras koneprusensis','specimen':'SM 75','revision':'recovery-r001','generator':'build_phragmoceras.py',
        'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'config_sha256':hashlib.sha256(args.config.read_bytes()).hexdigest(),
        'scale_semantics':config['scale_semantics'],'sources':['Manda 2007 p127 Fig8A-D; DOI10.3140/bull.geosci.2007.02.119'],'era':'Silurian, Ludlow, Ludfordian; upper S. linearis Zone','locality':'Velký vrch Hill, Koněprusy; Kopanina Formation','scope':'New original recovery candidate, not historical r002 byte recovery','threejs_version':'0.180.0'},
        output_root=out,render=False,diagnostics=False,max_triangles=config['max_triangles'],max_materials=config['max_materials'],max_primitives=config['max_primitives'])
    if record['glb_bytes']>config['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    print('PHRAGMOCERAS_BUILD_RESULT='+json.dumps({'triangles':record['triangles'],'glb_bytes':record['glb_bytes'],'glb_sha256':record['sha256']['glb']}))

if __name__=='__main__':main()
