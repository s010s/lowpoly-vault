#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Compsognathus living stylization; Blender 4.3.2.
Run Blender in background with this script, then -- --output DIR --config params.json.
Only the adjacent deps folder and config are generation inputs. No references embedded.
"""
from pathlib import Path
import sys, json, math, shutil
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, ground_asset, export_asset, render_previews


def loft(vertices, faces, ids, points, radii, mat=0, sides=10, bands=False):
    """Closed variable-radius tube following a chosen anatomical centerline."""
    start=len(vertices)
    for i, (p, r) in enumerate(zip(points,radii)):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        tangent.normalize()
        axis=Vector((1,0,0))
        if abs(tangent.dot(axis))>.9: axis=Vector((0,1,0))
        u=(axis-tangent*axis.dot(tangent)).normalized(); v=tangent.cross(u).normalized()
        rx,rz=r if isinstance(r,(tuple,list)) else (r,r)
        for j in range(sides):
            a=2*math.pi*j/sides
            q=Vector(p)+u*rx*math.cos(a)+v*rz*math.sin(a)
            vertices.append(tuple(q))
    faces.append(tuple(start+j for j in reversed(range(sides)))); ids.append(mat)
    for i in range(len(points)-1):
        for j in range(sides):
            face=(start+i*sides+j,start+i*sides+(j+1)%sides,start+(i+1)*sides+(j+1)%sides,start+(i+1)*sides+j)
            faces.append(face)
            if bands:
                z=sum(vertices[k][2] for k in face)/4-(points[i][2]+points[i+1][2])/2
                rz0=(radii[i][1]+radii[i+1][1])/2
                ids.append(2 if z < -rz0*.35 else 1 if z>rz0*.75 else 0)
            else: ids.append(mat)
    end=start+(len(points)-1)*sides
    faces.append(tuple(end+j for j in range(sides)));ids.append(mat)


def sphere(vertices,faces,ids,center,scale,mat=0,n=12,k=6):
    start=len(vertices); vertices.append(tuple(Vector(center)+Vector((0,0,-scale[2]))))
    for i in range(1,k):
        a=-math.pi/2+math.pi*i/k
        for j in range(n):
            b=2*math.pi*j/n
            vertices.append((center[0]+scale[0]*math.cos(a)*math.cos(b),center[1]+scale[1]*math.cos(a)*math.sin(b),center[2]+scale[2]*math.sin(a)))
    top=len(vertices);vertices.append(tuple(Vector(center)+Vector((0,0,scale[2]))))
    for j in range(n):faces.append((start,start+1+(j+1)%n,start+1+j));ids.append(mat)
    for i in range(k-2):
        for j in range(n):faces.append((start+1+i*n+j,start+1+i*n+(j+1)%n,start+1+(i+1)*n+(j+1)%n,start+1+(i+1)*n+j));ids.append(mat)
    for j in range(n):faces.append((top,start+1+(k-2)*n+j,start+1+(k-2)*n+(j+1)%n));ids.append(mat)


def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--config',type=Path,default=HERE/'params.json');parser.add_argument('--gray',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads(args.config.read_text()); out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    coll=setup_scene(p['asset_id'],p['seed'])
    palette=p['palette']; names=['body','dorsal','ventral','claw','eye','iris']
    materials=[make_material(name,'#949494' if args.gray else palette[name],roughness=.85 if name!='eye' else .48) for name in names]
    def part(name, fn, slots=(0,)):
        v,f,mi=[],[],[];fn(v,f,mi)
        o=mesh_object(name,v,f,[materials[x] for x in slots],coll)
        for polygon,idx in zip(o.data.polygons,mi):polygon.material_index=idx
        return o
    # Long narrow trunk flowing into a light S-shaped neck, not a bulky carnivore body.
    body=[(0,.13,.255),(0,.10,.270),(0,.055,.283),(0,-.005,.282),(0,-.065,.280),(0,-.112,.285),(0,-.137,.305),(0,-.155,.330),(0,-.176,.350),(0,-.200,.352)]
    radii=[(.017,.020),(.029,.037),(.038,.047),(.035,.043),(.028,.036),(.020,.029),(.014,.022),(.012,.018),(.011,.015),(.011,.011)]
    part('Torso-and-light-neck',lambda v,f,m:loft(v,f,m,body,radii,sides=12,bands=True),slots=(0,1,2))
    tail=[(0,.115,.259),(0,.16,.257),(.004,.23,.251),(.009,.31,.243),(.014,.39,.233),(.017,.47,.220),(.016,.54,.209),(.012,.595,.202)]
    tr=[(.021,.026),(.018,.022),(.014,.017),(.0105,.013),(.0075,.009),(.005,.006),(.0028,.0035),(.0009,.0012)]
    part('Long-tapering-tail',lambda v,f,m:loft(v,f,m,tail,tr,sides=10,bands=True),slots=(0,1,2))
    head=[(0,-.183,.353),(0,-.202,.360),(0,-.224,.362),(0,-.245,.356),(0,-.277,.351),(0,-.305,.350)]
    hr=[(.010,.012),(.018,.019),(.018,.019),(.013,.012),(.0095,.009),(.006,.0065)]
    part('Thin-low-muzzle-and-cranium',lambda v,f,m:loft(v,f,m,head,hr,sides=12,bands=True),slots=(0,1,2))
    part('Slender-lower-jaw',lambda v,f,m:loft(v,f,m,[(0,-.202,.345),(0,-.239,.341),(0,-.280,.341),(0,-.303,.344)],[(.013,.005),(.012,.0048),(.0085,.0035),(.005,.002)],sides=8),slots=(2,))
    # Mouth creases sit just on the jaw cheek; no exposed oversized teeth.
    def details(v,f,m):
        for s in (-1,1):
            loft(v,f,m,[(s*.014,-.214,.346),(s*.0122,-.244,.345),(s*.009,-.278,.345),(s*.0058,-.299,.347)],[.0006,.0006,.0005,.00035],sides=6)
            sphere(v,f,m,(s*.009,-.288,.355),(.0011,.002,.0012),n=8,k=4)
    part('Mouth-creases-and-nares',details,slots=(4,))
    def eyes(v,f,m):
        for s in (-1,1):
            sphere(v,f,m,(s*.017,-.215,.365),(.003,.0052,.0054),n=12,k=6)
    part('Small-amber-eyes',eyes,slots=(5,))
    def pupils(v,f,m):
        for s in (-1,1):sphere(v,f,m,(s*.0195,-.216,.365),(.0013,.0028,.0032),n=10,k=6)
    part('Dark-pupils',pupils,slots=(4,))
    # Hindlimbs preserve thigh, long shin, and an independently readable long metatarsus.
    for s,shift in [(-1,.017),(1,-.012)]:
        x=s*.034
        hip=(s*.025,.052,.267);knee=(s*.040,-.029+shift,.202);ankle=(s*.041,.053+shift,.112);ball=(s*.042,.020+shift,.016)
        def leg(v,f,m):
            loft(v,f,m,[hip,(s*.034,.022+shift,.243),knee],[(.024,.029),(.021,.025),(.013,.015)],sides=10)
            loft(v,f,m,[knee,(s*.040,.016+shift,.162),ankle],[.012,.009,.0065],sides=10)
            loft(v,f,m,[ankle,(s*.042,.038+shift,.066),ball],[.0065,.005,.006],mat=1,sides=8)
        part(('Left' if s<0 else 'Right')+'-hindlimb',leg,slots=(0,2))
        def foot(v,f,m):
            # Long spreading support digits; middle toe reaches furthest.
            for i,(off,end_y) in enumerate([(-.014,-.074),(0,-.100),(.014,-.080)]):
                a=(ball[0]+off*.22,ball[1],.016);b=(ball[0]+off*.64,-.022+shift,.010);c=(ball[0]+off,end_y+shift,.0055)
                loft(v,f,m,[a,b,c],[.0045,.0035,.0027],sides=8)
                loft(v,f,m,[c,(c[0],c[1]-.009,.005),(c[0],c[1]-.014,.0027)],[.0028,.002,.0008],mat=1,sides=6)
            loft(v,f,m,[(ball[0],ball[1]+.004,.024),(ball[0]-s*.009,ball[1]+.022,.018),(ball[0]-s*.012,ball[1]+.027,.014)],[.003,.002,.0008],sides=6)
        part(('Left' if s<0 else 'Right')+'-long-three-toed-foot',foot,slots=(2,3))
        def arm(v,f,m):
            shoulder=(s*.024,-.103,.279);elbow=(s*.043,-.094,.239);wrist=(s*.034,-.147,.239)
            loft(v,f,m,[shoulder,(s*.037,-.099,.259),elbow,wrist],[.010,.008,.006,.0045],sides=8)
            # Digits lie in a near-sagittal palm plane: palms face inward, never down.
            for j in range(3):
                a=(wrist[0],wrist[1]-.002,wrist[2]+(j-1)*.004)
                b=(s*(.032-j*.001),-.166-j*.003,.235+(j-1)*.004)
                c=(s*(.028-j*.001),-.177-j*.002,.229+(j-1)*.004)
                loft(v,f,m,[a,b,c],[.0027,.002,.0011],sides=6)
                loft(v,f,m,[c,(c[0]-s*.002,c[1]-.004,c[2]-.004)],[.0014,.0006],mat=1,sides=6)
        part(('Left' if s<0 else 'Right')+'-inward-facing-forelimb',arm,slots=(0,3))
    # Root stays identity; translate all semantic mesh parts to floor between the feet.
    root=bpy.data.objects[coll['asset_root']]
    root['representation']='living-reconstruction';root['size_basis']='0.9 m artistic estimate, not a measured specimen or maturity claim'
    root['soft_tissue']='Body breadth, color, covering and posture are inferred'
    for obj in coll.all_objects:
        if obj.type=='MESH':
            for vert in obj.data.vertices:vert.co.y += .035
    ground_asset(coll)
    if args.gray:
        render_previews(coll,out,views=('front','side','hero'),resolution=384,samples=8,transparent=False)
        return
    # Retain portable authoring UI state, not workstation browser locations.
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    bpy.context.preferences.filepaths.temporary_directory='//'
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
                    space.params.filename='model.blend'
    budget=p['geometry_policy']
    record=export_asset(p['asset_id'],{'en':'Compsognathus','zh':'美颌龙'},'animals',coll,
        metadata={'description':{'en':'Original slender living reconstruction; estimated soft tissue, covering and color.','zh':'原创纤细活体复原；软组织、覆盖和颜色均为估计。'},'generator':'source/generate.py','export_texcoords':False},
        output_root=out,render=False,diagnostics=False,max_triangles=budget['max_triangles'],max_materials=budget['max_materials'],max_primitives=budget['max_primitives'])
    stage=out/p['asset_id']
    for ext in ('blend','glb'):shutil.copyfile(stage/(p['asset_id']+'.'+ext),out/('model.'+ext))
    if (out/'model.glb').stat().st_size>budget['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    print('GENERATED',record['triangles'],record['glb_bytes'])

if __name__=='__main__':main()
