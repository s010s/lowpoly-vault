#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic, editable Mesohippus bairdi living reconstruction.
Run with Blender in background mode, pass -- --output DIR [--gray].
Only Python standard-library and the declared relative deps are used.
The coordinates are artistic estimates, not measurements of CM 961.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, shutil, sys
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, export_asset

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

class Mesh:
    def __init__(self): self.v=[]; self.f=[]; self.mi=[]
    def add(self,verts,faces,mat=0):
        n=len(self.v); self.v.extend(verts); self.f.extend(tuple(n+i for i in f) for f in faces); self.mi.extend([mat]*len(faces))
    def tube(self,rings,n=10,mat=0):
        # rings: x,y,z, transverse radius, sagittal radius. Ring frame follows path.
        verts=[]; faces=[]
        for i,r in enumerate(rings):
            a=Vector(rings[max(i-1,0)][:3]); b=Vector(rings[min(i+1,len(rings)-1)][:3]); t=(b-a).normalized()
            cross=Vector((1,0,0)); cross=(cross-t*cross.dot(t)).normalized(); depth=t.cross(cross).normalized()
            for j in range(n):
                q=2*math.pi*j/n
                verts.append(tuple(Vector(r[:3])+cross*(r[3]*math.cos(q))+depth*(r[4]*math.sin(q))))
        for i in range(len(rings)-1):
            for j in range(n): faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        verts += [tuple(rings[0][:3]),tuple(rings[-1][:3])]
        for j in range(n): faces.extend([(len(verts)-2,(j+1)%n,j),(len(verts)-1,(len(rings)-1)*n+j,(len(rings)-1)*n+(j+1)%n)])
        self.add(verts,faces,mat)
    def body(self,rings,n=12):
        verts=[]; faces=[]; indices=[]
        for y,z,rx,rz in rings:
            for j in range(n):
                q=2*math.pi*j/n; verts.append((rx*math.cos(q),y,z+rz*math.sin(q)))
        for i in range(len(rings)-1):
            for j in range(n):
                faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
                indices.append(1 if j in (7,8,9,10) else 0)
        verts += [(0,rings[0][0],rings[0][1]),(0,rings[-1][0],rings[-1][1])]
        for j in range(n):
            faces.extend([(len(verts)-2,(j+1)%n,j),(len(verts)-1,(len(rings)-1)*n+j,(len(rings)-1)*n+(j+1)%n)]); indices.extend([0,0])
        self.add(verts,faces); self.mi=indices
    def emit(self,name,mats,coll):
        o=mesh_object(name,self.v,self.f,mats,coll)
        for p,mi in zip(o.data.polygons,self.mi): p.material_index=mi
        o['construction']='Original profile-loft; closed semantic component. Intersections between components are intentional.'
        return o

def ellipsoid(name,center,scale,mat,coll,n=12,r=6):
    # Latitude rings omit the poles, avoiding collapsed quads.
    m=Mesh(); verts=[]; faces=[]
    for k in range(1,r):
        t=math.pi*k/r
        for j in range(n):
            a=2*math.pi*j/n; verts.append((center[0]+scale[0]*math.sin(t)*math.cos(a),center[1]+scale[1]*math.sin(t)*math.sin(a),center[2]+scale[2]*math.cos(t)))
    for k in range(r-2):
        for j in range(n): faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    verts += [(center[0],center[1],center[2]+scale[2]),(center[0],center[1],center[2]-scale[2])]
    for j in range(n): faces.extend([(len(verts)-2,j,(j+1)%n),(len(verts)-1,(r-2)*n+(j+1)%n,(r-2)*n+j)])
    m.add(verts,faces); return m.emit(name,mat,coll)

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--gray',action='store_true'); args=ap.parse_args(argv)
    p=json.loads((BASE/'params.json').read_text()); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    coll=setup_scene(p['asset_id'],p['seed'])
    colors=p['palette']; mats={k:make_material(k,'#919191' if args.gray else v) for k,v in colors.items()}
    body=Mesh(); body.body([(.355,.465,.045,.09),(.305,.466,.109,.137),(.20,.452,.142,.143),(.05,.436,.150,.132),(-.12,.447,.133,.143),(-.235,.447,.105,.132),(-.286,.45,.060,.092)])
    body.emit('trunk_chest_and_rump',[mats['coat'],mats['belly']],coll)
    neck=Mesh(); neck.tube([(0,-.22,.46,.087,.100),(0,-.286,.505,.075,.087),(0,-.346,.563,.059,.071),(0,-.403,.615,.048,.060),(0,-.446,.646,.041,.046)],12)
    neck.emit('modest_sloping_neck',mats['coat'],coll)
    head=Mesh(); head.body([(-.416,.645,.030,.040),(-.451,.638,.054,.066),(-.493,.618,.060,.072),(-.535,.599,.048,.060),(-.577,.578,.036,.043),(-.621,.560,.030,.032),(-.653,.551,.027,.027)],12)
    head.emit('short_equine_head_and_deep_cheek',[mats['coat'],mats['belly']],coll)
    muzzle=Mesh(); muzzle.body([(-.631,.550,.030,.027),(-.657,.548,.030,.026),(-.669,.550,.024,.021)],10)
    muzzle.emit('tapered_soft_muzzle',[mats['muzzle'],mats['muzzle']],coll)
    # Forelegs hang beneath the chest; elbow, carpus and fetlock change thickness.
    feet=[]
    for side,label,offset in [(-1,'left',.014),(1,'right',-.012)]:
        x=side*.103; y=-.237+offset
        fore=Mesh(); fore.tube([(side*.081,-.208+offset,.486,.052,.067),(x,-.197+offset,.385,.033,.042),(x,-.227+offset,.296,.022,.024),(x,-.246+offset,.231,.024,.025),(x,-.248+offset,.154,.014,.017),(x,-.259+offset,.084,.021,.021)],10)
        fore.emit(label+'_forelimb',mats['coat'],coll); feet.append((label+'_forefoot',x,-.259+offset))
        # Forward stifle, rearward hock, then near-vertical metatarsal.
        hind=Mesh(); hind.tube([(side*.093,.258,.476,.065,.082),(side*.116,.176+offset,.375,.044,.053),(side*.118,.240+offset,.283,.027,.034),(side*.118,.304+offset,.217,.026,.025),(side*.118,.290+offset,.149,.014,.017),(side*.118,.277+offset,.084,.020,.020)],10)
        hind.emit(label+'_hindlimb',mats['coat'],coll); feet.append((label+'_hindfoot',side*.118,.277+offset))
    for name,x,y in feet:
        foot=Mesh()
        for d in (-1,0,1):
            side=bool(d); dx=d*.043; dest_y=y+(.003 if side else -.014); w=.012 if side else .019; depth=.023 if side else .031
            foot.tube([(x+d*.012,y,.083,.011 if side else .019,.014),(x+dx*.80,dest_y+.004,.049,w*.82,depth*.58),(x+dx,dest_y,.028,w*.90,depth*.80)],8,0)
            foot.tube([(x+dx,dest_y-.009,.001,w,depth),(x+dx,dest_y-.008,.014,w*1.04,depth*1.02),(x+dx,dest_y,.033,w*.82,depth*.72)],8,1)
        ob=foot.emit(name+'_three_distinct_toes',[mats['coat'],mats['hoof']],coll); ob['diagnostic_toes']=3; ob['middle_toe_larger']=True
    # Short pointed pinnae, with a recessed dark inner polygon, not oversized foal ears.
    for side,label in [(-1,'left'),(1,'right')]:
        x=side*.035
        ear=Mesh(); ear.tube([(x,-.440,.677,.019,.014),(x+side*.012,-.431,.715,.017,.010),(x+side*.015,-.444,.753,.0025,.002)],7,0)
        # Inner inset is a thin closed wedge instead of a single open face.
        v=[(x-side*.010,-.452,.688),(x+side*.011,-.443,.738),(x+side*.012,-.451,.710),(x-side*.010,-.449,.688),(x+side*.011,-.440,.738),(x+side*.012,-.448,.710)]
        ear.add(v,[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)],1)
        ear.emit(label+'_pointed_pinna',[mats['coat'],mats['ear']],coll)
        ellipsoid(label+'_eye',(side*.054,-.481,.642),(.009,.012,.010),mats['eye'],coll,10,5)
        ellipsoid(label+'_nostril',(side*.027,-.647,.563),(.004,.009,.0055),mats['eye'],coll,8,4)
    tail=Mesh(); tail.tube([(0,.330,.514,.026,.028),(0,.409,.477,.020,.023),(.009,.470,.383,.015,.018),(.015,.501,.277,.011,.014),(.022,.546,.195,.020,.028),(.026,.563,.173,.005,.009)],10)
    tail.emit('modest_tapered_tail',mats['muzzle'],coll)
    # Hair is an explicitly artistic restrained ridge, not a modern long mane.
    mane=Mesh(); mane.tube([(0,-.431,.676,.013,.012),(0,-.389,.663,.014,.012),(0,-.335,.615,.014,.014),(0,-.281,.563,.014,.015),(0,-.241,.536,.010,.010)],8)
    mane.emit('short_reconstruction_hair_ridge',mats['muzzle'],coll)
    # Center floor contacts, preserving meters and identity root.
    zmin=min((o.matrix_world@v.co).z for o in coll.all_objects if o.type=='MESH' for v in o.data.vertices)
    for ob in coll.all_objects:
        if ob.type=='MESH':
            for v in ob.data.vertices: v.co.z-=zmin
    bpy.context.scene['scientific_scope']='Mesohippus bairdi original living reconstruction; dimensions and soft tissues estimated.'
    bpy.context.scene['generator_source']='source/generate.py'; bpy.context.scene['generator_parameters']='source/params.json'
    # Keep source UI state portable; no working-directory or cache paths saved.
    bpy.context.scene.render.filepath='//render/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'.'*1000
                    space.params.directory=b'//'
    # Canonical helper owns export flags, source audit and export consistency.
    old=Path.cwd(); os.chdir(out)
    try:
        record=export_asset(p['asset_id'],{'en':'Mesohippus bairdi','zh':'渐新马'},'mammals',coll,
            metadata={'description':{'en':'Original early three-toed horse reconstruction.','zh':'原创早期三趾马活体复原。'},'generator':'source/generate.py','sources':p['reference_urls']},output_root=out,render=False,max_triangles=18000,max_materials=8,max_primitives=36)
        generated=out/p['asset_id']
        shutil.copy2(generated/(p['asset_id']+'.blend'),out/'model.blend'); shutil.copy2(generated/(p['asset_id']+'.glb'),out/'model.glb')
        qa=json.loads((generated/'qa.json').read_text())
        qa['glb']['file']='model.glb'
        write(out/'build-report.json',{'schema_version':1,'status':'PASS','asset_id':p['asset_id'],'revision':p['revision'],'gray_model':args.gray,'blender_version':bpy.app.version_string,'seed':p['seed'],'generator_sha256':sha(BASE/'generate.py'),'params_sha256':sha(BASE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'source_audit':qa['source'],'glb_audit':qa['glb'],'bounds_roundtrip_max_error_m':qa['bounds_roundtrip_max_error_m'],'export_options':record['export_options'],'limitations':'Technical source/static-GLB checks only; not independent visual review, GPU rendering or publication approval.'})
    finally: os.chdir(old)
    print('BUILD_COMPLETE',sha(out/'model.glb'))
if __name__=='__main__': main()
