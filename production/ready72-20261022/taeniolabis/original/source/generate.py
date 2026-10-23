# SPDX-License-Identifier: MIT
"""Original deterministic Taeniolabis reconstruction. Blender 4.3.2.
Run: blender -b --threads 2 --python source/generate.py -- --out /path/output
All non-runtime dependencies live beside this file, under deps/. No network.
"""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import asset_common as ac
from qa_glb import audit_glb

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def yloft(name, sections, sides, mats, palette=None, exponent=2.0):
    # Each section: y, width radius, bottom z, top z, optional lateral center.
    verts=[]
    for row in sections:
        y,w,b,t=row[:4]; cx=row[4] if len(row)>4 else 0
        for j in range(sides):
            a=2*math.pi*j/sides; c=math.cos(a); s=math.sin(a)
            x=cx+w*math.copysign(abs(c)**(2/exponent),c)
            z=(b+t)/2+(t-b)/2*math.copysign(abs(s)**(2/exponent),s)
            verts.append((x,y,z))
    faces=[tuple(reversed(range(sides)))]
    for i in range(len(sections)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=b+sides;d=a+sides
            # Deliberate diagonal organization, not randomly noisy triangulation.
            if (i+j)%2: faces.extend([(a,b,d),(b,c,d)])
            else: faces.extend([(a,b,c),(a,c,d)])
    faces.append(tuple((len(sections)-1)*sides+j for j in range(sides)))
    obj=ac.mesh_object(name,verts,faces,mats,COL)
    if palette:
        for p in obj.data.polygons:
            center=sum((obj.data.vertices[i].co for i in p.vertices),Vector())/len(p.vertices)
            p.material_index=palette(center)
    return obj

def tube(name,rows,sides,mats):
    # Rotation-minimizing-style local transverse frame, with all vertices in world meters.
    verts=[]
    for i,row in enumerate(rows):
        center=Vector(row[:3]); rx,ry=row[3:5]
        tangent=Vector(rows[min(i+1,len(rows)-1)][:3])-Vector(rows[max(0,i-1)][:3]);tangent.normalize()
        ref=Vector((1,0,0))
        if abs(tangent.dot(ref))>.92:ref=Vector((0,1,0))
        u=(ref-tangent*ref.dot(tangent)).normalized();v=tangent.cross(u).normalized()
        for j in range(sides):
            a=2*math.pi*j/sides;verts.append(tuple(center+u*(rx*math.cos(a))+v*(ry*math.sin(a))))
    faces=[tuple(reversed(range(sides)))]
    for i in range(len(rows)-1):
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=b+sides;d=a+sides
            faces.extend([(a,b,c),(a,c,d)])
    faces.append(tuple((len(rows)-1)*sides+j for j in range(sides)))
    return ac.mesh_object(name,verts,faces,mats,COL)

def ellipsoid(name,center,scale,mat,rings=7,segs=12):
    verts=[(center[0],center[1],center[2]-scale[2])]
    for i in range(1,rings):
        lat=-math.pi/2+math.pi*i/rings
        for j in range(segs):
            a=2*math.pi*j/segs
            verts.append((center[0]+scale[0]*math.cos(lat)*math.cos(a),center[1]+scale[1]*math.cos(lat)*math.sin(a),center[2]+scale[2]*math.sin(lat)))
    verts.append((center[0],center[1],center[2]+scale[2]));last=len(verts)-1
    faces=[]
    for j in range(segs):faces.append((0,1+(j+1)%segs,1+j))
    for i in range(rings-2):
        for j in range(segs):
            a=1+i*segs+j;b=1+i*segs+(j+1)%segs;faces.extend([(a,b,b+segs),(a,b+segs,a+segs)])
    for j in range(segs):faces.append((last,1+(rings-2)*segs+j,1+(rings-2)*segs+(j+1)%segs))
    return ac.mesh_object(name,verts,faces,mat,COL)

def merge_parts(name,parts):
    verts=[];faces=[];mats=[];indices=[]
    for obj in parts:
        offset=len(verts);verts.extend(tuple(obj.matrix_world@v.co) for v in obj.data.vertices)
        local=[]
        for m in obj.data.materials:
            if m not in mats:mats.append(m)
            local.append(mats.index(m))
        for p in obj.data.polygons:
            faces.append(tuple(offset+i for i in p.vertices));indices.append(local[p.material_index])
    out=ac.mesh_object(name,verts,faces,mats,COL)
    for p,i in zip(out.data.polygons,indices):p.material_index=i
    for obj in parts:bpy.data.objects.remove(obj,do_unlink=True)
    return out

def create():
    global COL
    COL=ac.setup_scene('taeniolabis',P['seed'])
    colors=P['palette_srgb']
    coat=ac.make_material('Fur warm umber',colors['coat'])
    back=ac.make_material('Fur dorsal umber',colors['back'])
    light=ac.make_material('Fur throat taupe',colors['under'])
    skin=ac.make_material('Bare skin and claws',colors['skin'])
    dark=ac.make_material('Eye nose mouth',colors['dark'],roughness=.48)
    tooth=ac.make_material('Incisor ivory',colors['ivory'],roughness=.72)
    body_rows=[[-.251,.047,.219,.300],[-.215,.078,.185,.310],[-.192,.085,.163,.310],[-.145,.108,.129,.315],[-.075,.132,.112,.329],[.015,.142,.106,.335],[.100,.135,.108,.331],[.178,.108,.121,.306],[.225,.060,.155,.269],[.246,.019,.193,.236]]
    def body_palette(v):
        if v.z>.292 and abs(v.x)<.105:return 1
        if v.z<.155:return 2
        return 0
    body=yloft('Barrel torso and neck',body_rows,24,[coat,back,light],None,2.25)
    for poly in body.data.polygons:
        sector=((poly.index-1)//2)%24
        poly.material_index=(1 if 2<=sector<=9 else 2 if 14<=sector<=21 else 0) if 0<poly.index<len(body.data.polygons)-1 else 0
    # Deliberate broad skull with strong masseter/zygomatic width and short muzzle.
    head_rows=[[-.199,.034,.239,.301],[-.224,.069,.229,.326],[-.259,.090,.219,.342],[-.291,.097,.214,.336],[-.321,.086,.218,.322],[-.351,.068,.225,.307],[-.381,.051,.235,.295],[-.398,.036,.246,.286]]
    def head_palette(v):
        if v.z<.246:return 2
        if v.z>.320:return 1
        return 0
    yloft('Broad cranium cheek and muzzle',head_rows,24,[coat],None,2.35)
    # Exposed heavy lower jaw remains connected behind the modest mouth seam.
    yloft('Heavy lower jaw',[[-.265,.060,.211,.246],[-.310,.076,.207,.245],[-.352,.059,.213,.245],[-.388,.033,.229,.250],[-.400,.023,.242,.253]],16,[light],exponent=2.3)
    ellipsoid('Nose pad',(0,-.403,.276),(.029,.009,.0135),dark,6,12)
    # Mouth seam is compact and largely embedded, not a grinning black mask.
    yloft('Mouth seam',[[-.374,.038,.246,.250],[-.399,.028,.247,.252],[-.404,.022,.250,.254]],12,dark,exponent=2.4)
    for s,label in [(-1,'L'),(1,'R')]:
        # Conservative tiny lateral eyes, well behind the muzzle.
        ellipsoid('Eye socket '+label,(s*.074,-.318,.302),(.011,.012,.010),back,6,12)
        ellipsoid('Eye '+label,(s*.081,-.323,.304),(.0065,.008,.007),dark,8,14)
        # Small rounded ears, not pointed squirrel pinnae.
        ellipsoid('Outer ear '+label,(s*.078,-.226,.335),(.020,.013,.023),coat,8,14)
        ellipsoid('Ear recess '+label,(s*.078,-.237,.337),(.0125,.004,.015),skin,7,12)
        # Upper incisors point down and very slightly back, not canine fangs.
        x=s*.009
        yloft('Upper incisor '+label,[[-.407,.0062,.246,.259,x],[-.400,.0066,.242,.257,x],[-.393,.0058,.243,.254,x]],8,tooth,exponent=4)
        # One continuous bent limb mesh per leg maintains silhouette without ball joints.
        tube('Forelimb '+label,[(s*.081,-.142,.253,.041,.041),(s*.104,-.145,.205,.038,.037),(s*.114,-.134,.154,.031,.031),(s*.113,-.162,.095,.023,.024),(s*.111,-.184,.043,.022,.026)],12,coat)
        tube('Hindlimb '+label,[(s*.080,.147,.255,.056,.061),(s*.115,.161,.219,.053,.053),(s*.126,.130,.163,.039,.040),(s*.124,.179,.101,.027,.031),(s*.124,.148,.043,.026,.030)],14,coat)
        for hind in (False,True):
            x=s*(.124 if hind else .111);y=.125 if hind else -.195
            parts=[ellipsoid('Paw '+label,(x,y,.028),(.032,.048 if hind else .038,.028),coat,6,12)]
            for d in range(5):
                dx=(d-2)*.012
                length=(.034 if hind else .028)*(1-.13*abs(d-2))
                ybase=y-(.022 if hind else .017)
                # Rounded short digits and small dull nails, not digging-specialist talons.
                parts.append(tube('Digit',[(x+dx,ybase,.022,.0068,.009),(x+dx,ybase-length*.65,.014,.0062,.008),(x+dx,ybase-length,.010,.0045,.006)],8,coat))
                parts.append(tube('Nail',[(x+dx,ybase-length+.003,.013,.004,.004),(x+dx,ybase-length-.006,.009,.0028,.0025),(x+dx,ybase-length-.009,.007,.0012,.0012)],6,skin))
            merge_parts(('Hind foot ' if hind else 'Fore foot ')+label,parts)
    # Approximately 0.20 m tapered cylindrical tail, never a flattened paddle.
    tube('Round tapered tail',[(0,.221,.212,.027,.027),(.004,.259,.180,.024,.024),(.012,.302,.133,.019,.019),(.025,.345,.095,.014,.014),(.043,.386,.075,.010,.010),(.061,.420,.070,.006,.006),(.075,.441,.074,.0018,.0018)],14,skin)
    # Units, exact generation provenance and scientific cautions remain editable in the blend.
    scene=bpy.context.scene
    scene['taxon']='Taeniolabis taoensis'
    scene['whole_body_scale']='Artistic estimate, not a measured complete fossil'
    scene['cranial_reference']='DMNH EPV.95284: length 161 mm, width 146 mm (Table 5, Krause et al. 2021)'
    scene['tail_limb_coat']='Conservative reconstruction; digging only possible, not established'
    scene.render.threads_mode='FIXED';scene.render.threads=2
    return COL

def render(collection,out,gray=False,resolution=800,samples=24):
    if gray:
        clay=ac.make_material('gray-diagnostic','#999999')
        for obj in collection.all_objects:
            if obj.type=='MESH':
                obj.data.materials.clear();obj.data.materials.append(clay)
                for p in obj.data.polygons:p.material_index=0
    paths=ac.render_previews(collection,out,views=('front','side','top','hero'),resolution=resolution,samples=samples)
    for label in ('front','side','top','hero'):
        src=out/f'preview-{label}.png';dst=out/('perspective.png' if label=='hero' else label+'.png');src.rename(dst)
    return paths

def main():
    global P
    parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);parser.add_argument('--mode',choices=['build','gray','render'],default='build');parser.add_argument('--glb');parser.add_argument('--resolution',type=int,default=800);parser.add_argument('--samples',type=int,default=24)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);P=json.loads((HERE/'params.json').read_text());out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    if args.mode=='render':
        ac.setup_scene('taeniolabis',P['seed']);bpy.ops.import_scene.gltf(filepath=str(Path(args.glb).resolve()));col=bpy.data.collections['EXPORT']
        for obj in list(bpy.context.scene.objects):
            if obj.type=='MESH':ac.link_object(obj,col)
        bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
        render(col,out,resolution=args.resolution,samples=args.samples)
        write(out/'render-evidence.json',{'status':'RENDERED_EXACT_GLB','glb_sha256':sha(Path(args.glb)),'engine':'Cycles CPU','threads':2,'resolution':args.resolution,'samples':args.samples,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'views':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[.574,-.819,.466]},'images':{name:sha(out/name) for name in ['front.png','side.png','top.png','perspective.png']}})
        return
    col=create()
    if args.mode=='gray':
        write(out/'source-metrics.json',ac.audit_source(col,P['budgets']['max_triangles']))
        render(col,out,gray=True,resolution=args.resolution,samples=args.samples);return
    staging=out/'_canonical'
    metadata={'description':{'en':'Conservative whole-animal reconstruction of Taeniolabis taoensis, emphasizing the unusually broad cranium and heavy gnawing/grinding jaws. Body, tail, ears and coat are artistic reconstructions.','zh':'Taeniolabis taoensis 完整活体保守复原，突出宽颅与厚重颌部；躯体、尾、耳和毛色为艺术推定。'},'generator':'source/generate.py','surface_profile':'palette-only','reconstruction_uncertainties':P['uncertainties'],'sources':['https://doi.org/10.1007/s10914-021-09584-3','https://doi.org/10.1007/s12549-025-00671-4']}
    record=ac.export_asset('taeniolabis',{'en':'Taeniolabis','zh':'Taeniolabis'},'animals',col,metadata=metadata,output_root=staging,render=False,diagnostics=False,max_triangles=P['budgets']['max_triangles'],max_materials=P['budgets']['max_materials'],max_primitives=P['budgets']['max_primitives'])
    built=staging/'taeniolabis'
    shutil.copy2(built/'taeniolabis.glb',out/'model.glb');shutil.copy2(built/'taeniolabis.blend',out/'model.blend')
    if (out/'model.glb').stat().st_size>P['budgets']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    write(out/'build-metadata.json',record);write(out/'geometry-audit.json',json.loads((built/'qa.json').read_text()))
    write(out/'build-fingerprint.json',{'asset_id':'taeniolabis','revision':'r001','blender':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'glb_bytes':(out/'model.glb').stat().st_size,'semantic_metrics':{k:record[k] for k in ['triangles','dimensions','materials','export_options','bounds_glb_m']}})
if __name__=='__main__':main()
