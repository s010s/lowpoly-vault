# SPDX-License-Identifier: MIT
"""Original Saurichthys curionii living reconstruction.
Run with Blender 4.3.2: blender -b -t 2 --python source/generate.py -- --output .
All generator inputs and imported helpers are within this source package.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset


def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path('.'))
    parser.add_argument('--gray',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads((BASE/'params.json').read_text()); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    col=setup_scene(p['asset_id'], p['seed'])
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    colors=p['palette']
    mats={k:make_material(k, '#929292' if args.gray else c, roughness=.8 if k!='pupil' else .36) for k,c in colors.items()}
    bodym=[mats['dorsal'],mats['flank'],mats['belly']]

    def cx(y): return max(0., y-.10)*.035
    def loft(name,rows,materials=bodym,segments=12):
        # rows: longitudinal Y, X half width, low Z, high Z; caps are real surfaces.
        verts=[]
        for y,w,lo,hi in rows:
            for j in range(segments):
                a=2*math.pi*j/segments
                verts.append((cx(y)+w*math.cos(a),y,(lo+hi)/2+(hi-lo)/2*math.sin(a)))
        faces=[tuple(range(segments-1,-1,-1))]
        for i in range(len(rows)-1):
            for j in range(segments): faces.append((i*segments+j,i*segments+(j+1)%segments,(i+1)*segments+(j+1)%segments,(i+1)*segments+j))
        faces.append(tuple((len(rows)-1)*segments+j for j in range(segments)))
        obj=mesh_object(name,verts,faces,materials,col)
        for poly in obj.data.polygons:
            if len(materials)>1:
                # A longitudinal material band follows the section angle, not nearest-row height.
                if poly.index==0 or poly.index==len(obj.data.polygons)-1:
                    poly.material_index=1
                else:
                    j=(poly.index-1)%segments
                    s=math.sin(2*math.pi*(j+.5)/segments)
                    poly.material_index=0 if s>.35 else 2 if s<-.35 else 1
        return obj

    loft('cranial-and-needle-trunk',p['body_rows'])
    loft('long-pointed-upper-jaw',p['upper_jaw_rows'],segments=8)
    loft('opposing-long-lower-jaw',p['lower_jaw_rows'],segments=8)

    fin_rays=[]
    def fin(name,points,normal,ray_origin=None,ray_targets=None):
        # Finite-thickness closed fin with concave-outline tessellation.
        n=Vector(normal).normalized(); thick=p['fin_thickness_m']; pts=[Vector(x) for x in points]; N=len(pts)
        verts=[tuple(v+n*thick/2) for v in pts]+[tuple(v-n*thick/2) for v in pts]
        tris=tessellate_polygon([pts]); index={tuple(v):i for i,v in enumerate(pts)}
        faces=[]
        for tri in tris:
            ids=tuple(v if isinstance(v,int) else index[tuple(v)] for v in tri); faces.extend([ids,tuple(N+x for x in ids[::-1])])
        for i in range(N): faces.append((i,(i+1)%N,(i+1)%N+N,i+N))
        obj=mesh_object(name,verts,faces,mats['fin'],col)
        if ray_origin is not None:
            for t in ray_targets:
                for sign in [-1,1]:
                    # Half-embedded ribs on both sides, lower relief than membrane width.
                    fin_rays.append((Vector(ray_origin)+n*(thick*.48*sign),Vector(t)+n*(thick*.48*sign),p['ray_radius_m']))
        return obj

    def sagittal(y,z): return (cx(y),y,z)
    for name,key in [('posterior-dorsal-fin','dorsal_fin'),('posterior-anal-fin','anal_fin'),('forked-caudal-fin','caudal_fin')]:
        f=p[key]; pts=[sagittal(*v) for v in f['outline_yz']]; base=sagittal(*f['ray_origin_yz']); targets=[sagittal(*v) for v in f['ray_targets_yz']]
        fin(name,pts,(1,0,0),base,targets)
    for sign,label in [(-1,'left'),(1,'right')]:
        for key in ['pectoral','pelvic']:
            f=p[key+'_fin']; points=[(sign*x+cx(y),y,z) for x,y,z in f['outline_xyz']]
            origin=(sign*f['ray_origin_xyz'][0]+cx(f['ray_origin_xyz'][1]),f['ray_origin_xyz'][1],f['ray_origin_xyz'][2])
            targets=[(sign*x+cx(y),y,z) for x,y,z in f['ray_targets_xyz']]
            fin(label+'-'+key+'-fin',points,(0,0,1),origin,targets)

    if not args.gray:
        def tubes(name,lines,material,sides=5):
            verts=[]; faces=[]
            for a,b,r in lines:
                a,b=Vector(a),Vector(b); d=(b-a).normalized(); ref=Vector((0,0,1)) if abs(d.z)<.9 else Vector((1,0,0)); u=d.cross(ref).normalized(); v=d.cross(u).normalized(); start=len(verts)
                for c,rad in [(a,r),(b,r*.4)]:
                    verts += [tuple(c+rad*(math.cos(2*math.pi*j/sides)*u+math.sin(2*math.pi*j/sides)*v)) for j in range(sides)]
                faces += [tuple(start+j for j in range(sides-1,-1,-1)),tuple(start+sides+j for j in range(sides))]
                faces += [(start+j,start+(j+1)%sides,start+sides+(j+1)%sides,start+sides+j) for j in range(sides)]
            return mesh_object(name,verts,faces,material,col)
        tubes('subtle-finite-fin-rays',fin_rays,mats['belly'],4)
        # Flattened elliptical eyes; eye color and soft anatomy are artistic choices.
        def ellipsoid(name,center,radii,mat,seg=12,rings=5):
            c=Vector(center); verts=[tuple(c+Vector((radii[0],0,0)))]; faces=[]
            for i in range(1,rings):
                t=math.pi*i/rings
                for j in range(seg):
                    a=2*math.pi*j/seg
                    verts.append(tuple(c+Vector((radii[0]*math.cos(t),radii[1]*math.sin(t)*math.cos(a),radii[2]*math.sin(t)*math.sin(a)))))
            verts.append(tuple(c-Vector((radii[0],0,0)))); end=len(verts)-1
            for j in range(seg): faces.append((0,1+j,1+(j+1)%seg)); faces.append((end,1+(rings-2)*seg+(j+1)%seg,1+(rings-2)*seg+j))
            for i in range(rings-2):
                for j in range(seg): faces.append((1+i*seg+j,1+i*seg+(j+1)%seg,1+(i+1)*seg+(j+1)%seg,1+(i+1)*seg+j))
            return mesh_object(name,verts,faces,mat,col)
        gill=[]
        for sign,label in [(-1,'left'),(1,'right')]:
            ellipsoid(label+'-subtle-orbital-rim',(sign*.0089,-.135,.068),(.0017,.0031,.0032),mats['mouth'])
            ellipsoid(label+'-amber-iris',(sign*.01025,-.135,.068),(.0008,.00265,.00265),mats['iris'])
            ellipsoid(label+'-dark-pupil',(sign*.01095,-.135,.068),(.00035,.0012,.00145),mats['pupil'])
            contour=[(sign*.0075,-.110,.0735),(sign*.0105,-.105,.069),(sign*.0114,-.102,.062),(sign*.0102,-.104,.055),(sign*.0071,-.109,.050)]
            gill += [(a,b,.00022) for a,b in zip(contour,contour[1:])]
        tubes('paired-gill-cover-seams',gill,mats['mouth'],4)
        # Small opposing teeth are deliberately sparse and not species-exact dentition.
        teeth=[]
        for i in range(14):
            y=-.275+i*.008
            t=(y+.3)/.16; w=.0008+t*.0038
            for sign in [-1,1]:
                for upper in [True,False]:
                    z=.0619 if upper else .0606
                    teeth.append(((sign*w*.77,y,z),(sign*w*.70,y+.0002,z+(-.00065 if upper else .00065)),.00018))
        tubes('restrained-opposing-teeth',teeth,mats['belly'],4)

    root=bpy.data.objects[col['asset_root']]
    root['representation']='living-reconstruction'; root['taxon_scope']='Saurichthys curionii'
    root['origin']='Virtual mounting point below horizontal swimming specimen; no stand exported.'
    root['inference']='Living cross-section, exact fin-ray count, soft tissues, scale and colors inferred.'
    # Remove machine-specific file-browser startup paths from editable source UI.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.context.scene.render.filepath='//render'
    build=out/'private'/'build'/('gray' if args.gray else 'final')
    record=export_asset(p['asset_id'],{'en':'Saurichthys curionii','zh':'锯齿鱼'},'fish',col,
        metadata={'generator':'source/generate.py','description':{'en':'Original elongate, double-jawed Triassic predatory fish reconstruction.','zh':'原创三叠纪细长双颌捕食性鱼类复原。'},'sources':p['source_urls']},
        output_root=build,render=False,max_triangles=18000,max_materials=8,max_primitives=36)
    built=build/p['asset_id']
    shutil.copyfile(built/(p['asset_id']+'.glb'),out/'model.glb')
    shutil.copyfile(built/(p['asset_id']+'.blend'),out/'model.blend')
    record.update(glb='model.glb',blend='model.blend',preview='preview.png',origin=root['origin'])
    record['python_version']=sys.version
    record['source_inputs']={'generator_sha256':digest(BASE/'generate.py'),'params_sha256':digest(BASE/'params.json'),'dependencies_sha256':digest(BASE/'dependencies.json')}
    write(out/'qa/evidence/build-metadata.json',record)
    qa=json.loads((built/'qa.json').read_text())
    qa['glb']['file']='model.glb'
    qa['subject']={'asset_id':p['asset_id'],'revision':p['revision'],'glb_sha256':digest(out/'model.glb')}
    qa['reviewed_warnings']=['Nonzero lower Z is intentional for the documented virtual mounting point of a swimming fish.']
    write(out/'qa/evidence/source-export.json',qa)
    print('GENERATED',json.dumps({'triangles':record['triangles'],'glb_sha256':digest(out/'model.glb'),'gray':args.gray}))

if __name__=='__main__': main()
