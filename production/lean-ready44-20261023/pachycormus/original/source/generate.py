# SPDX-License-Identifier: MIT
"""Deterministic same-species Pachycormus reconstruction. Run with Blender.
Usage: blender --background --factory-startup --python-exit-code 1 --python source/generate.py -- --output .
All modeling dependencies are package-relative; colors and soft tissue are inferred.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
import bpy
from mathutils import Vector
SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE/'deps'))
import asset_common as common
from qa_glb import audit_glb


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def lerp(a,b,t): return a*(1-t)+b*t

def build(p):
    collection=common.setup_scene('pachycormus',seed=p['seed'])
    root=bpy.data.objects['pachycormus']
    root['authoring_forward']='+X'
    root['origin']='Swimming mount at median axial center; no ground contact'
    root['representation']='same-species-composite living reconstruction'
    root['nominal_total_length_m']=p['nominal_total_length_m']
    mats={key:common.make_material(key,value,roughness=0.78 if key!='Eye' else 0.45) for key,value in p['palette_srgb'].items()}
    controls=p['body_sections']
    # Catmull-Hermite interpolation of deliberately placed anatomical sections.
    def section(x):
        idx=next((i for i in range(len(controls)-1) if controls[i][0]<=x<=controls[i+1][0]),len(controls)-2)
        a,b=controls[idx],controls[idx+1]; h=b[0]-a[0]; t=(x-a[0])/h
        v=[x]
        for j in range(1,4):
            l=controls[max(0,idx-1)]; r=controls[min(len(controls)-1,idx+2)]
            m0=(b[j]-l[j])/(b[0]-l[0]); m1=(r[j]-a[j])/(r[0]-a[0])
            v.append((2*t**3-3*t*t+1)*a[j]+(t**3-2*t*t+t)*h*m0+(-2*t**3+3*t*t)*b[j]+(t**3-t*t)*h*m1)
        return v
    xs=sorted(set([r[0] for r in controls]+[(a[0]+b[0])/2 for a,b in zip(controls,controls[1:])]))
    radial=p['radial_segments']; verts=[]; faces=[]; indices=[]
    for i,x in enumerate(xs):
        _,w,d,zc=section(x)
        for j in range(radial):
            t=2*math.pi*j/radial
            # Smooth ellipsoid sections, faceted topology, no external scales/armor.
            verts.append((x,w*math.cos(t),zc+d*math.sin(t)))
    faces.append(tuple(reversed(range(radial)))); indices.append(1)
    for i in range(len(xs)-1):
        for j in range(radial):
            a=i*radial+j;b=i*radial+(j+1)%radial;c=(i+1)*radial+(j+1)%radial;d=(i+1)*radial+j
            # Single coherent faceted hull; no interpenetrating head/body primitives.
            faces.append((a,b,c,d))
            z=math.sin(2*math.pi*(j+0.5)/radial)
            indices.append(0 if z>0.50 else 2 if z < -0.55 else 1)
    faces.append(tuple((len(xs)-1)*radial+j for j in range(radial))); indices.append(1)
    body=common.mesh_object('Fusiform_body_and_short_rostrum',verts,faces,[mats['Dorsal'],mats['Flank'],mats['Ventral']],collection)
    for poly,idx in zip(body.data.polygons,indices): poly.material_index=idx
    body['method']='Anatomical profile loft; width and flesh inferred, not a single skeleton scan'
    body['maximum_depth_m']=0.130

    # Paired finite-thickness scythe fins. Convex leading and concave trailing edges.
    for sign,label in [(-1,'right'),(1,'left')]:
        st=p['pectoral_sections']; cols=10; v=[]; f=[]; mi=[]
        for surface in [-1,1]:
            for k,(y,lead,trail,z) in enumerate(st):
                t=k/(len(st)-1); half=lerp(0.00065,0.00018,t)
                for j in range(cols+1):
                    u=j/cols
                    # Raised fine corrugation tracks fin rays within the membrane.
                    ridge=0.00025*math.sin(math.pi*u)**2*math.sin(math.pi*t)
                    v.append((lerp(lead,trail,u),sign*y,z+surface*(half+ridge)))
        n=len(st)*(cols+1)
        for surface in range(2):
            off=surface*n
            for k in range(len(st)-1):
                for j in range(cols):
                    a=off+k*(cols+1)+j;b=a+1;c=b+cols+1;d=a+cols+1
                    f.append((a,b,c,d));mi.append(1 if j in [1,4,7] else 0)
        perimeter=list(range(cols+1))+[k*(cols+1)+cols for k in range(1,len(st))]+[(len(st)-1)*(cols+1)+j for j in range(cols-1,-1,-1)]+[k*(cols+1) for k in range(len(st)-2,0,-1)]
        for a,b in zip(perimeter,perimeter[1:]+perimeter[:1]): f.append((a,b,b+n,a+n));mi.append(0)
        fin=common.mesh_object('Scythe_pectoral_'+label,v,f,[mats['Fin'],mats['Flank']],collection)
        for poly,idx in zip(fin.data.polygons,mi):poly.material_index=idx
        fin['evidence']='Cawley Fig5 BRLSI M1395; sweep and spread inferred'

    def fan_fin(name,outline,center,thickness,ray_pattern=False):
        # Closed, two-sided finite-thickness fin, not double-sided rendering.
        v=[];f=[];mi=[]
        n=len(outline)
        for sign in [-1,1]:
            v.append((center[0],sign*thickness,center[1]))
            v.extend((x,sign*thickness*0.23,z) for x,z in outline)
        for s in range(2):
            off=s*(n+1)
            for j in range(n): f.append((off,off+j+1,off+(j+1)%n+1));mi.append(1 if ray_pattern and j%3==1 else 0)
        for j in range(n):
            a=j+1;b=(j+1)%n+1;f.append((a,b,b+n+1,a+n+1));mi.append(0)
        fin=common.mesh_object(name,v,f,[mats['Fin'],mats['Flank']] if ray_pattern else mats['Fin'],collection)
        for poly,idx in zip(fin.data.polygons,mi):poly.material_index=idx
        return fin
    fan_fin('Small_posterior_dorsal',p['dorsal_outline'],[-0.082,0.049],0.0015)
    fan_fin('Small_posterior_anal',p['anal_outline'],[-0.183,-0.018],0.0013)
    tail=fan_fin('Forked_caudal_reconstructed_tips',p['caudal_outline'],[-0.236,0],0.0028,True)
    tail['uncertainty']='Distal outer edges inferred; M1393 tips broken at nodule boundary'

    # Flattened eyeballs sit into the head, circular on flank, not exposed spheres.
    for sign,label in [(-1,'right'),(1,'left')]:
        cx,cz=0.276,0.021
        v=[];f=[];mi=[];rings=[(0.0108,-0.00015),(0.0093,0.00055),(0.0067,0.00115),(0.0033,0.00140)]
        n=20
        for radius,bulge in rings:
            for j in range(n):
                t=2*math.pi*j/n
                x,z=cx+radius*math.cos(t),cz+radius*math.sin(t)
                _,w,d,zc=section(x)
                y=w*math.sqrt(max(0,1-((z-zc)/d)**2))+bulge
                v.append((x,sign*y,z))
        for k in range(len(rings)-1):
            for j in range(n):
                f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j));mi.append(0 if k<1 else 1)
        f.extend([tuple(reversed(range(n))),tuple((len(rings)-1)*n+j for j in range(n))]);mi.extend([0,1])
        eye=common.mesh_object('Eye_'+label,v,f,[mats['Iris'],mats['Eye']],collection)
        for poly,idx in zip(eye.data.polygons,mi):poly.material_index=idx

    # Mouth and gill seams are thin shallow closed tubes, attached to the hull.
    v=[];f=[]
    def tube(points,radius):
        start=len(v); n=5
        for i,pt in enumerate(points):
            t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
            t.normalize();u=t.cross(Vector((0,0,1))).normalized();w=t.cross(u).normalized()
            for j in range(n):v.append(tuple(Vector(pt)+radius*(math.cos(2*math.pi*j/n)*u+math.sin(2*math.pi*j/n)*w)))
        f.append(tuple(start+j for j in reversed(range(n))))
        for i in range(len(points)-1):
            for j in range(n):f.append((start+i*n+j,start+i*n+(j+1)%n,start+(i+1)*n+(j+1)%n,start+(i+1)*n+j))
        f.append(tuple(start+(len(points)-1)*n+j for j in range(n)))
    for sign in [-1,1]:
        # Place semantic lines on the evaluated profile, retaining shallow lips.
        mouth=[]
        for x,z in [(0.321,-0.0005),(0.306,-0.006),(0.285,-0.011),(0.261,-0.016),(0.242,-0.020)]:
            _,w,d,zc=section(x);y=w*math.sqrt(max(0,1-((z-zc)/d)**2))+0.00035;mouth.append((x,sign*y,z))
        tube(mouth,0.00062)
        gill=[]
        for x,z in [(0.201,0.041),(0.189,0.025),(0.183,0.002),(0.188,-0.022),(0.204,-0.038),(0.221,-0.040)]:
            _,w,d,zc=section(x);y=w*math.sqrt(max(0,1-((z-zc)/d)**2))+0.00035;gill.append((x,sign*y,z))
        tube(gill,0.00062)
    seams=common.mesh_object('Closed_mouth_and_opercular_seams',v,f,mats['Eye'],collection)
    seams['style']='Subtle inset-like surface seam; no exposed skeleton or giant teeth'
    return collection


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=SOURCE.parent);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((SOURCE/'params.json').read_text())
    collection=build(p)
    # Portable saved UI/render destinations, with no local workspace locators.
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
    # Canonical export helper supplies source audit, glTF options and axis check.
    raw=out/'private/raw-export'
    common.export_asset('pachycormus',{'en':'Pachycormus','zh':'厚茎鱼'},'animals',collection,metadata={'description':'Same-species composite living reconstruction','export_texcoords':False},output_root=raw,render=False,max_triangles=24000,max_materials=6,max_primitives=16)
    produced=raw/'pachycormus'
    shutil.copyfile(produced/'pachycormus.glb',out/'model.glb')
    shutil.copyfile(produced/'pachycormus.blend',out/'model.blend')
    qa=json.loads((produced/'qa.json').read_text());qa['glb']['file']='model.glb'
    # Public report keeps exact measurements but strips the helper's runtime file locator.
    qa['glb_sha256']=sha(out/'model.glb')
    qa['generator_sha256']=sha(SOURCE/'generate.py');qa['params_sha256']=sha(SOURCE/'params.json')
    qa['mounting_origin']='Axial swimming mount at (0,0,0); negative min Z is intentional, no ground contact'
    qa['style']='Flat body and fin facets; opaque single-sided closed solids'
    qa['profile']='palette-only static living reconstruction'
    qa['runtime']={'blender':bpy.app.version_string,'python':sys.version.split()[0],'threads':bpy.context.scene.render.threads}
    qa['budget_checks']={
        'triangles':qa['glb']['scene_triangles']<=24000,
        'materials':qa['glb']['materials']<=6,
        'primitives':qa['glb']['scene_primitives_estimated_base_draw_calls']<=16,
        'bytes':qa['glb']['bytes']<=2500000}
    if not all(qa['budget_checks'].values()):raise RuntimeError('Frozen budget exceeded')
    write(out/'qa/evidence/source-export.json',qa)
    print('BUILD_COMPLETE',qa['glb']['sha256'],qa['glb']['scene_triangles'])
if __name__=='__main__':main()
