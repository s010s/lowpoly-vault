# SPDX-License-Identifier: MIT
import bpy, math, sys, json, argparse, shutil
from pathlib import Path
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,_vertices_world,_bounds
args=sys.argv[sys.argv.index('--')+1:]
p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True);opt=p.parse_args(args)
cfg=json.loads(opt.config.read_text()); out=opt.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
c=setup_scene('phoenicopsis',cfg['seed']); mats=[make_material(n,col) for n,col in zip(['twig-brown','shoot-warm','strap-olive','strap-sage','strap-deep'],cfg['palette'])]

def tube(name,points,radii,mat,n=8):
    vv=[];ff=[]
    for j,(pt,rad) in enumerate(zip(points,radii)):
        t=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(j-1,0)]);t.normalize(); u=t.cross(Vector((0,1,0))).normalized();v=t.cross(u).normalized()
        vv.extend(tuple(Vector(pt)+rad*(math.cos(k*2*math.pi/n)*u+math.sin(k*2*math.pi/n)*v)) for k in range(n))
    for j in range(len(points)-1):
        for k in range(n): ff.append((j*n+k,j*n+(k+1)%n,(j+1)*n+(k+1)%n,(j+1)*n+k))
    ff.extend([tuple(reversed(range(n))),tuple((len(points)-1)*n+k for k in range(n))]);return mesh_object(name,vv,ff,mat,c)
points=[(-.135+i*.034, .006*math.sin(i*.6), .018+.010*math.sin(i*.44)) for i in range(9)]
tube('curved-detached-twig',points,[.0115-.00055*i for i in range(9)],mats[0])
for b in range(3):
    bx=[-.100,-.006,.094][b]; by=[-.005,.006,.013][b];bz=.028+.007*(1-abs(b-1))
    tube('short-shoot-'+str(b+1),[(bx,by,bz-.007),(bx+.002,by,bz+.005),(bx+.003,by,bz+.018)],[.0105,.0088,.0067],mats[1],7)
    for l in range(5):
        s=l-2; base=Vector((bx+.003+s*.0023,by+(l%2-.5)*.003,bz+.013+(abs(s)%2)*.002))
        # Each bundle is a fan of unforked straps, with unequal lengths and depth arcs.
        dx=[-.070,-.010,.055][b]+s*.031
        length=[.177,.219,.169][b]*(1-.058*abs(s))*(1+.035*math.sin(l*2.1+b))
        dy=(s*.009+[.004,-.015,.011][b])
        width=.0090*(1+.08*math.sin(b*3+l))
        vv=[];ff=[];N=cfg['leaf_sections']
        for j in range(N):
            t=j/(N-1)
            center=base+Vector((dx*(.22*t+.78*t*t),dy*t+.011*math.sin(t*math.pi)*(1 if l%2 else -1),length*(t-.12*t*t)))
            # Tilted broad face gives readable top/side volume; no zero-area tip.
            twist=.10*s+.13*b+.13*t
            u=Vector((math.cos(twist),math.sin(twist),-dx/length*.25)).normalized(); n=Vector((-math.sin(twist),math.cos(twist),.08)).normalized()
            shape=[.44,.80,1,1,.98,.96,.92,.84,.65,.16][j]
            hw=width*shape/2; thick=.00072*(.65+.35*(1-t))
            vv.extend(tuple(center+u*sw*hw+n*sn*thick/2) for sw,sn in [(-1,-1),(1,-1),(1,1),(-1,1)])
        for j in range(N-1):
            for k in range(4):ff.append((4*j+k,4*j+(k+1)%4,4*(j+1)+(k+1)%4,4*(j+1)+k))
        ff.extend([(3,2,1,0),tuple(4*(N-1)+k for k in range(4))]);mesh_object('shoot-%d-strap-%d'%(b+1,l+1),vv,ff,mats[2+(l+b)%3],c)
# Bake exact nominal bbox once into vertices, retain identity object/root transforms.
lo,hi=_bounds(_vertices_world(c)); scale=[cfg['nominal_blender_xyz_m'][i]/(hi[i]-lo[i]) for i in range(3)];mid=[(lo[i]+hi[i])/2 for i in range(2)]
for obj in c.all_objects:
    if obj.type=='MESH':
        for v in obj.data.vertices:v.co=Vector(((v.co.x-mid[0])*scale[0],(v.co.y-mid[1])*scale[1],(v.co.z-lo[2])*scale[2]))
record=export_asset('phoenicopsis','Phoenicopsis strap-leaf short shoots','plants',c,output_root=out/'stage',render=False,max_triangles=14000,max_materials=6,max_primitives=30,metadata={'nominal_blender_xyz_m':cfg['nominal_blender_xyz_m'],'nominal_glb_xyz_m':[.32,.26,.12],'dimensions_claim':'Artistic nominal bounds; measured bounds independent in this metadata.','representation':'fossil-specimen','scope':'Stylized detached foliage only; no complete plant or reproductive organs.','textures':[]})
for f in (out/'stage/phoenicopsis').iterdir():shutil.move(str(f),str(out/f.name))
shutil.rmtree(out/'stage')
# Keep actual source vertex count separate from exported POSITION stream count.
(out/'source-counts.json').write_text(json.dumps({'authored_vertices':sum(len(o.data.vertices) for o in c.all_objects if o.type=='MESH'),'evaluated_vertices':sum(len(o.data.vertices) for o in c.all_objects if o.type=='MESH'),'visible_mesh_parts':sum(o.type=='MESH' for o in c.all_objects),'modifiers':0},indent=2)+'\n')
