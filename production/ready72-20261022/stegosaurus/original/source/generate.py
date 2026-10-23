#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Sophie-size Stegosaurus. Blender 4.3.2, no external assets.
Usage: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
The source is faceted, semantically editable, and intentionally assembled from
closed intersecting anatomical solids rather than represented as a printable union.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

class Builder:
    def __init__(self): self.v=[]; self.f=[]; self.mi=[]; self.groups=[]
    def add(self,name,v,f,indices=None):
        n=len(self.v); self.v.extend(v); self.f.extend([[n+i for i in face] for face in f]); self.mi.extend(indices or [0]*len(f)); self.groups.append((name,n,len(v)))
    def object(self,name,mats,collection):
        ob=mesh_object(name,self.v,self.f,mats,collection)
        for face,idx in zip(ob.data.polygons,self.mi): face.material_index=idx
        for group,start,count in self.groups: ob.vertex_groups.new(name=group).add(list(range(start,start+count)),1,'REPLACE')
        return ob

def loft_y(builder,name,rings,segments=12,belly=False):
    # Ring: y,z,width radius,height radius. Closed, explicit profile topology.
    v=[(rx*math.cos(2*math.pi*j/segments),y,z+rz*math.sin(2*math.pi*j/segments)) for y,z,rx,rz in rings for j in range(segments)]
    f=[]; mi=[]
    for k in range(len(rings)-1):
        for j in range(segments):
            f.append([k*segments+j,k*segments+(j+1)%segments,(k+1)*segments+(j+1)%segments,(k+1)*segments+j])
            mi.append(1 if belly and math.sin(2*math.pi*(j+.5)/segments)<-.45 else 0)
    f.extend([list(range(segments-1,-1,-1)),list(range((len(rings)-1)*segments,len(rings)*segments))]); mi.extend([0,0])
    builder.add(name,v,f,mi)

def loft_z(builder,name,rings,segments=10):
    # Ring: x,y,z,x radius,y radius.
    v=[(x+rx*math.cos(2*math.pi*j/segments),y+ry*math.sin(2*math.pi*j/segments),z) for x,y,z,rx,ry in rings for j in range(segments)]
    f=[]
    for k in range(len(rings)-1):
        for j in range(segments): f.append([k*segments+j,k*segments+(j+1)%segments,(k+1)*segments+(j+1)%segments,(k+1)*segments+j])
    f.extend([list(range(segments-1,-1,-1)),list(range((len(rings)-1)*segments,len(rings)*segments))])
    builder.add(name,v,f)

def ellipsoid(builder,name,c,r,n=8,m=4):
    v=[(c[0],c[1],c[2]-r[2])]
    for k in range(1,m):
        p=-math.pi/2+math.pi*k/m
        for j in range(n):
            t=2*math.pi*j/n; v.append((c[0]+r[0]*math.cos(p)*math.cos(t),c[1]+r[1]*math.cos(p)*math.sin(t),c[2]+r[2]*math.sin(p)))
    v.append((c[0],c[1],c[2]+r[2])); top=len(v)-1
    f=[[0,1+(j+1)%n,1+j] for j in range(n)]
    for k in range(m-2):
        for j in range(n): f.append([1+k*n+j,1+k*n+(j+1)%n,1+(k+1)*n+(j+1)%n,1+(k+1)*n+j])
    f.extend([[top,1+(m-2)*n+j,1+(m-2)*n+(j+1)%n] for j in range(n)])
    builder.add(name,v,f)

def spike(builder,name,base,tip,radius):
    axis=(Vector(tip)-Vector(base)); w=axis.normalized(); u=w.cross(Vector((0,0,1))).normalized(); vv=w.cross(u).normalized()
    verts=[]
    for t,r in [(0,radius),(.36,radius*.70),(.76,radius*.30)]:
        center=Vector(base)+t*axis
        for j in range(8): verts.append(tuple(center+r*(math.cos(j*math.pi/4)*u+math.sin(j*math.pi/4)*vv)))
    verts.append(tuple(tip)); faces=[list(range(7,-1,-1))]
    for k in range(2):
        for j in range(8): faces.append([8*k+j,8*k+(j+1)%8,8*(k+1)+(j+1)%8,8*(k+1)+j])
    faces.extend([[16+j,16+(j+1)%8,24] for j in range(8)]); builder.add(name,verts,faces)

def plate(builder,name,y,z,side,width,height,thickness,offset,surface):
    # Broad, asymmetrical pentagonal/diamond plate. Thin lens, not a fin sheet.
    outline=[(-.45,0),(-.59,.33),(-.37,.73),(-.08,1),(.22,.94),(.52,.56),(.46,.16),(.30,0)]
    v=[]
    for sign in [-1,1]:
        for yy,zz in outline:
            basal=surface(y+width*yy,offset)-.025
            v.append((side*offset+side*.075*height*zz+sign*thickness*.32,y+width*yy,(1-zz)*basal+zz*z+height*zz))
        v.append((side*offset+side*.075*height*.48+sign*thickness*.62,y,z+height*.48))
    f=[]; mi=[]
    for sign in range(2):
        b=sign*9
        for j in range(8): f.append([b+8,b+j,b+(j+1)%8]); mi.append(1 if j in [1,2,3] else 0)
    for j in range(8): f.append([j,(j+1)%8,9+(j+1)%8,9+j]); mi.append(0)
    builder.add(name,v,f,mi)

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x): Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]); out=args.output; out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((HERE/'params.json').read_text()); col=setup_scene('stegosaurus',seed=381001)
    mats=[make_material('body-olive','#7F8870'),make_material('underside-sand','#B2AF8D'),make_material('plates-earth','#9E654B'),make_material('plate-facet-ochre','#B5815C'),make_material('keratin-ivory','#D0C3A1'),make_material('eye-mouth-charcoal','#282B27')]
    body=Builder()
    rings=cfg['body_profile_y_z_rx_rz']
    loft_y(body,'neck-torso-tail-continuous',rings,16,True)
    loft_y(body,'small-low-beaked-skull',[[-2.02,.66,.042,.040],[-1.94,.682,.072,.064],[-1.85,.699,.105,.084],[-1.76,.70,.091,.080],[-1.69,.71,.062,.055]],10,True)
    body.object('axial-body-neck-head-tail',[mats[0],mats[1]],col)
    keratin=Builder(); eyes=Builder()
    loft_y(keratin,'small-beak',[[-2.05,.653,.028,.030],[-2.015,.66,.046,.040],[-1.965,.661,.050,.037]],10)
    for s in [-1,1]:
        ellipsoid(eyes,'eye-'+str(s),(s*.100,-1.855,.726),(.014,.019,.018),8,4)
        ellipsoid(eyes,'nostril-'+str(s),(s*.053,-1.967,.683),(.005,.009,.006),6,4)
        ellipsoid(eyes,'closed-mouth-'+str(s),(s*.073,-1.90,.652),(.004,.084,.006),8,4)
        for limb,y,hipz,x in [('fore',-.70,1.04,.37),('hind',.70,1.36,.42)]:
            leg=Builder()
            if limb=='fore':
                rr=[(s*.28,y,1.20,.07,.08),(s*.39,y,.98,.155,.165),(s*.405,y+.07,.72,.115,.12),(s*.43,y-.05,.30,.092,.105),(s*.43,y-.08,.105,.10,.11)]
            else:
                rr=[(s*.24,y,1.44,.075,.10),(s*.44,y,1.16,.225,.25),(s*.46,y+.12,.92,.20,.21),(s*.47,y+.16,.65,.15,.16),(s*.47,y-.06,.28,.10,.11),(s*.47,y-.10,.105,.105,.115)]
            loft_z(leg,limb+'-limb',rr,10)
            footx=rr[-1][0]; footy=rr[-1][1]-.035
            loft_z(leg,limb+'-weight-bearing-foot',[(footx,footy,.0,.12,.17),(footx,footy-.015,.035,.145,.195),(footx,footy,.10,.135,.17),(footx,footy+.045,.18,.095,.105)],10)
            leg.object(limb+'-leg-'+('left' if s<0 else 'right'),[mats[0]],col)
            n=2 if limb=='fore' else 3
            for j in range(n):
                nailx=footx+(j-(n-1)/2)*.074
                ellipsoid(keratin,f'{limb}-foot-{s}-blunt-nail-{j+1}',(nailx,footy-.163,.040),(.037,.045,.032),6,4)
    plates=Builder(); plate_records=[]
    def profile(y):
        for a,b in zip(rings,rings[1:]):
            if a[0]<=y<=b[0]:
                t=(y-a[0])/(b[0]-a[0]); return [a[k]*(1-t)+b[k]*t for k in range(1,4)]
        raise ValueError(y)
    def surface(y,x):
        zc,rx,rz=profile(y)
        # Interpolate the same 16-sided elliptical skin profile used by the torso.
        x=min(abs(x),rx*.97)
        samples=sorted((rx*math.cos(j*math.pi/8),rz*math.sin(j*math.pi/8)) for j in range(5))
        for (xa,za),(xb,zb) in zip(samples,samples[1:]):
            if xa-1e-8<=x<=xb+1e-8: return zc+za+(zb-za)*(x-xa)/(xb-xa)
        return zc+rz
    for i,(y,w,h) in enumerate(cfg['plates_y_width_height']):
        s=-1 if i%2==0 else 1; offset=min(.065+.070*(h/.80),profile(y)[1]*.33); th=.035+.020*(h/.80)
        # slightly embed in dorsal skin and follow elliptical shoulder curvature
        z=surface(y,offset)-.025
        plate(plates,f'plate-{i+1:02d}-'+('left' if s<0 else 'right'),y,z,s,w,h,th,offset,surface)
        plate_records.append({'id':i+1,'row':'left' if s<0 else 'right','center_y':y,'base_z':z,'height':h,'longitudinal_width':w,'lateral_offset':s*offset,'thickness_max':th*1.24})
    plateob=plates.object('nineteen-staggered-dorsal-plates',[mats[2],mats[3]],col); plateob['plate_count_total']=19; plateob['row_counts']='10 left, 9 right; alternating, not paired'
    spike_records=[]
    for pair,(y,x,z,dx,dy,dz) in enumerate(cfg['tail_spike_pairs']):
        for s in [-1,1]:
            base=(s*x,y,z); tip=(s*(x+dx),y+dy,z+dz); name=f'tail-spike-pair{pair+1}-'+('left' if s<0 else 'right')
            spike(keratin,name,base,tip,.058 if pair==0 else .050); spike_records.append({'name':name,'base':base,'tip':tip,'length':(Vector(tip)-Vector(base)).length})
    keratin.object('four-tail-spikes-beak-and-blunt-toenails',[mats[4]],col)
    eyes.object('eyes-nostrils-closed-mouth',[mats[5]],col)
    # Placement root is the center of the four actual Z=0 foot contact polygons,
    # not the full-body AABB center (the long tail would move that placement).
    contacts=[v.co.copy() for ob in col.all_objects if ob.type=='MESH' for v in ob.data.vertices if abs(v.co.z)<1e-8]
    origin_shift=[-(min(v.x for v in contacts)+max(v.x for v in contacts))/2,-(min(v.y for v in contacts)+max(v.y for v in contacts))/2,0.0]
    for ob in col.all_objects:
        if ob.type=='MESH':
            for v in ob.data.vertices: v.co+=Vector(origin_shift)
    for record in plate_records: record['center_y']+=origin_shift[1]
    for record in spike_records:
        for key in ['base','tip']: record[key]=list(Vector(record[key])+Vector(origin_shift))
    bpy.context.view_layer.update()
    root=bpy.data.objects[col['asset_root']]; root['specimen']='NHMUK PV R36730 size class, approximately 5.5 m'; root['reconstruction']='Original living reconstruction; soft tissue, keratin, colours and pose inferred'; root['scale_length_m']=5.5
    source=audit_source(col,6500)
    # Component-wise orientation check: each closed solid must have positive signed volume.
    components=[]
    for ob in col.all_objects:
        if ob.type!='MESH': continue
        bm=bmesh.new(); bm.from_mesh(ob.data); unseen=set(bm.verts); rows=[]
        while unseen:
            seed=next(iter(unseen)); stack=[seed]; comp=set()
            while stack:
                v=stack.pop()
                if v in comp: continue
                comp.add(v); stack.extend(e.other_vert(v) for e in v.link_edges if e.other_vert(v) not in comp)
            unseen-=comp; faces={f for v in comp for f in v.link_faces}; volume=0
            for f in faces:
                vs=[v.co for v in f.verts]
                for k in range(1,len(vs)-1): volume+=vs[0].dot(vs[k].cross(vs[k+1]))/6
            rows.append({'vertices':len(comp),'faces':len(faces),'signed_volume_m3':volume})
        components.append({'object':ob.name,'components':rows}); bm.free()
    if source['errors']: raise RuntimeError(source['errors'])
    if any(c['signed_volume_m3']<=0 for ob in components for c in ob['components']): raise RuntimeError('Non-positive solid orientation')
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available: raise RuntimeError('Missing required export settings')
    bpy.ops.export_scene.gltf(**options)
    glb=audit_glb(out/'model.glb',6500,6,12)
    b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in ['min','max'] for i in range(3))
    if glb['errors'] or glb['scene_triangles']!=source['triangles'] or delta>1e-4 or glb['bytes']>2000000: raise RuntimeError('Export/source audit failure '+str(glb['errors']))
    report={'asset_id':'stegosaurus','revision':'r001','status':'PASS','scope':'Maker technical source/export and component orientation checks, not independent factual or visual acceptance','source':source,'glb':glb,'bounds_roundtrip_max_error_m':delta,'closed_components':components,'features':{'plate_count':len(plate_records),'plates':plate_records,'tail_spike_count':len(spike_records),'tail_spikes':spike_records,'weight_bearing_feet':4},'origin':{'placement':'ground-contact footprint center','applied_geometry_translation_m':origin_shift},'profile':'static-palette-only-faceted','scale_note':'5.5 m tip-to-snout living reconstruction, not maximum adult','construction_note':'Closed intersecting anatomical solids; not a boolean printable union. Flat normals intentional. Plate fan creates a shallow convex broadside, with rounded profile corners approximated as facets.','runtime':{'blender':bpy.app.version_string,'gltf_exporter':'4.3.47','three_js_consumer':'0.180.0','seed':381001},'export_options':{k:v for k,v in options.items() if k!='filepath'},'source_hashes':{'generate.py':digest(__file__),'params.json':digest(HERE/'params.json')},'palette':[{'name':m.name,'srgb':m['palette_srgb']} for m in mats]}
    save(out/'technical.json',report)
    print(json.dumps({'status':'BUILT','output':str(out),'triangles':glb['scene_triangles'],'materials':glb['materials'],'glb_sha256':glb['sha256'],'semantic_sha256':glb['semantic_sha256']}))
if __name__=='__main__': main()
