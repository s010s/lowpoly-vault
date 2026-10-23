# SPDX-License-Identifier: MIT
"""Original Whatcheeria reconstruction. Blender 4.3.2, deterministic meters.
blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
Optional --clay is a structural diagnostic, not the final color asset.
Scientific sources: references.json. Soft tissues are artistic interpretations.
"""
from pathlib import Path
import sys, argparse, json, math, hashlib, shutil
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, export_asset

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT.parent);parser.add_argument('--clay',action='store_true')
    args=parser.parse_args(argv);out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    params=json.loads((ROOT/'params.json').read_text());collection=setup_scene('whatcheeria',params['seed'])
    mats={k:make_material(k,'#929292' if args.clay else v,roughness=.86 if k!='eye' else .4) for k,v in params['palette'].items()}
    groups={}
    def append(name,verts,faces,indices,materials):
        if name not in groups:groups[name]={'v':[],'f':[],'mi':[],'mats':materials}
        g=groups[name];n=len(g['v']);g['v'].extend(verts);g['f'].extend([tuple(i+n for i in f) for f in faces]);g['mi'].extend(indices)
    def rings(name,sections,n=16,materials=('skin',),palette=False):
        verts=[];faces=[];ids=[]
        for cx,y,cz,rx,rz in sections:
            for j in range(n):
                a=2*math.pi*j/n;verts.append((cx+rx*math.sin(a),y,cz+rz*math.cos(a)))
        for k in range(len(sections)-1):
            for j in range(n):
                faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
                c=math.cos(2*math.pi*(j+.5)/n);ids.append(2 if palette and c<-.65 else 1 if palette and c<.25 else 0)
        faces.extend([tuple(range(n-1,-1,-1)),tuple((len(sections)-1)*n+j for j in range(n))]);ids.extend([0,0])
        append(name,verts,faces,ids,materials)
    def tube(name,path,n=12,materials=('skin',)):
        verts=[];faces=[]
        for k,(xyz,r1,r2) in enumerate(path):
            p=Vector(xyz);prev=Vector(path[max(0,k-1)][0]);nxt=Vector(path[min(len(path)-1,k+1)][0]);tangent=(nxt-prev).normalized()
            ref=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((0,1,0));a=tangent.cross(ref).normalized();b=tangent.cross(a).normalized()
            for j in range(n):
                th=2*math.pi*j/n;verts.append(tuple(p+a*(r1*math.cos(th))+b*(r2*math.sin(th))))
        for k in range(len(path)-1):
            for j in range(n):faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
        faces.extend([tuple(range(n-1,-1,-1)),tuple((len(path)-1)*n+j for j in range(n))])
        append(name,verts,faces,[0]*len(faces),materials)
    def ellipsoid(name,center,radii,materials=('eye',),lon=12,lat=6):
        x,y,z=center;rx,ry,rz=radii;verts=[(x,y,z+rz)];faces=[]
        for k in range(1,lat):
            a=math.pi*k/lat
            for j in range(lon):
                b=2*math.pi*j/lon;verts.append((x+rx*math.sin(a)*math.cos(b),y+ry*math.sin(a)*math.sin(b),z+rz*math.cos(a)))
        end=len(verts);verts.append((x,y,z-rz))
        for j in range(lon):faces.append((0,1+j,1+(j+1)%lon))
        for k in range(lat-2):
            for j in range(lon):faces.append((1+k*lon+j,1+k*lon+(j+1)%lon,1+(k+1)*lon+(j+1)%lon,1+(k+1)*lon+j))
        for j in range(lon):faces.append((end,1+(lat-2)*lon+(j+1)%lon,1+(lat-2)*lon+j))
        append(name,verts,faces,[0]*len(faces),materials)
    # Continuous shoulder-to-tail axial loft, not a chain of primitives.
    rings('axial_body',[(0,-.576,.267,.072,.082),(0,-.53,.268,.088,.094),(0,-.46,.268,.112,.111),
        (0,-.36,.263,.145,.122),(0,-.23,.256,.156,.128),(0,-.07,.248,.157,.125),
        (0,.10,.232,.146,.116),(0,.24,.217,.139,.106),(0,.34,.199,.115,.096),
        (.004,.43,.180,.088,.080),(.012,.53,.156,.067,.063),(.025,.64,.129,.046,.047),
        (.044,.75,.102,.029,.033),(.062,.85,.079,.016,.021),(.074,.925,.066,.007,.011),(.078,.96,.061,.0015,.002)],
        n=params['cross_section_sides'],materials=('skin','flank','belly'),palette=True)
    # Angular deep narrow skull, with pronounced cheek planes and tapered muzzle.
    head=[(-.94,.031,.287,.191),(-.92,.051,.309,.184),(-.87,.063,.328,.180),(-.80,.076,.345,.185),(-.72,.087,.363,.193),(-.64,.104,.373,.204),(-.57,.100,.357,.215),(-.535,.071,.329,.225)]
    verts=[];faces=[];ids=[]
    for y,w,top,bottom in head:
        mid=(top+bottom)/2
        profile=[(0,top),(.65*w,top-.008),(w,mid+.038),(.98*w,bottom+.018),(.72*w,bottom),(0,bottom-.004),(-.72*w,bottom),(-.98*w,bottom+.018),(-w,mid+.038),(-.65*w,top-.008)]
        verts.extend((x,y,z) for x,z in profile)
    for k in range(len(head)-1):
        for j in range(10):faces.append((10*k+j,10*k+(j+1)%10,10*(k+1)+(j+1)%10,10*(k+1)+j));ids.append(1 if 2<=j<=7 else 0)
    faces.extend([tuple(range(9,-1,-1)),tuple((len(head)-1)*10+j for j in range(10))]);ids.extend([0,0])
    append('deep_narrow_skull',verts,faces,ids,('skin','flank'))
    rings('mandible',[(0,-.937,.166,.025,.018),(0,-.916,.157,.046,.027),(0,-.86,.153,.059,.028),(0,-.78,.157,.070,.030),(0,-.69,.170,.079,.032),(0,-.60,.192,.081,.032),(0,-.555,.216,.058,.026)],n=10,materials=('flank','belly','belly'),palette=True)
    rings('mouth_details',[(0,-.936,.189,.028,.009),(0,-.91,.181,.047,.009),(0,-.85,.180,.058,.011),(0,-.77,.184,.068,.012),(0,-.68,.197,.077,.010),(0,-.59,.217,.067,.008)],n=10,materials=('mouth',))
    for s in (-1,1):
        ellipsoid('eyes',(s*.088,-.695,.330),(.011,.018,.012),lon=12,lat=6)
        ellipsoid('mouth_details',(s*.056,-.904,.286),(.005,.008,.005),materials=('mouth',),lon=8,lat=4)
        # Restrained visible anterior fangs. Exact visible count is artistic.
        for y,x,z in [(-.884,.051,.194),(-.847,.058,.192)]:
            tube('anterior_fangs',[((s*x,y,z),.006,.006),((s*(x-.001),y-.002,z-.012),.004,.004),((s*(x-.003),y-.004,z-.025),.0006,.0006)],n=7,materials=('teeth',))
    for s in (-1,1):
        # Forelimbs: robust shoulder, lateral elbow and forward-carried lower arm.
        tube('robust_limbs_and_digits',[((s*.090,-.385,.268),.061,.067),((s*.151,-.356,.237),.065,.065),((s*.220,-.305,.173),.052,.055),((s*.254,-.316,.126),.043,.043),((s*.286,-.374,.070),.032,.034),((s*.305,-.414,.038),.038,.024),((s*.308,-.440,.028),.041,.021)],n=12)
        # Weight-bearing hind limbs, no frog-like elongated jumping segments.
        tube('robust_limbs_and_digits',[((s*.088,.245,.217),.073,.076),((s*.155,.280,.181),.075,.067),((s*.222,.324,.126),.059,.052),((s*.253,.300,.085),.045,.038),((s*.288,.230,.046),.033,.029),((s*.306,.201,.027),.043,.022)],n=12)
        for fy,fx in [(-.433,.309),(.204,.307)]:
            for idx,(dx,dy) in enumerate([(-.054,-.063),(-.019,-.111),(.021,-.105),(.059,-.072)]):
                bx=s*(fx+(idx-1.5)*.011);ex=s*(fx+dx)
                tube('robust_limbs_and_digits',[((bx,fy+.010,.029),.014,.013),((s*(fx+(idx-1.5)*.019),fy-.017,.021),.013,.011),((ex,fy+dy*.73,.017),.010,.008),((ex+s*.004,fy+dy,.012),.005,.005)],n=8)
    objects=[]
    for name,g in groups.items():
        obj=mesh_object(name,g['v'],g['f'],[mats[k] for k in g['mats']],collection)
        for poly,idx in zip(obj.data.polygons,g['mi']):poly.material_index=idx
        obj['semantic_part']=name;objects.append(obj)
    minz=min(v.co.z for ob in objects for v in ob.data.vertices)
    contacts=[v.co for ob in objects if ob.name=='robust_limbs_and_digits' for v in ob.data.vertices if v.co.z<=minz+.002]
    contact_y=(min(v.y for v in contacts)+max(v.y for v in contacts))/2
    for ob in objects:
        for v in ob.data.vertices:
            v.co.z-=minz;v.co.y-=contact_y
    bpy.context.scene['origin_convention']='Identity root at floor-contact bounding rectangle center, within 2 mm contact band.'
    bpy.context.scene['origin_shift_y_m']=-contact_y
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.context.scene['reconstruction']='Whatcheeria deltae artistic adult, 1.9 m target, not measured individual.'
    bpy.context.scene['source_notes']='Whitney et al. 2022 Fig1 body; Rawson 2021 abstract narrow skull; Field Museum 2022 size.'
    work=out/'private'/'canonical-output'
    record=export_asset('whatcheeria',{'en':'Whatcheeria','zh':'沃切螈'},'animals',collection,
        metadata={'representation':'living-reconstruction','description':{'en':'Original artistic reconstruction of the early tetrapod Whatcheeria deltae. Deep narrow skull, robust limbs and a short tapering tail.','zh':'沃切螈原创复原模型，深窄头颅、粗壮四肢和逐渐收细的较短尾部。'},
        'generator':'source/generate.py','revision':'r001','threejs_target_version':'0.180.0',
        'uncertainty':'1.9 m artistic adult; skin, color, pose, visible digits and fang exposure reconstructed, not specimen measurements.'},
        output_root=work,render=False,max_triangles=6000,max_materials=6,max_primitives=12,diagnostics=False)
    built=work/'whatcheeria';evidence=out/'qa'/'evidence';evidence.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(built/'whatcheeria.glb',out/'model.glb');shutil.copyfile(built/'whatcheeria.blend',out/'model.blend')
    qa=json.loads((built/'qa.json').read_text());record['glb']='model.glb';record['blend']='model.blend';record['preview']='preview.png'
    (evidence/'geometry.json').write_text(json.dumps(qa,indent=2)+'\n');(evidence/'build-metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
    (evidence/'runtime-dependencies.json').write_text(json.dumps({'blender':bpy.app.version_string,'python':sys.version,'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((ROOT/'params.json').read_bytes()).hexdigest(),'dependencies_sha256':hashlib.sha256((ROOT/'dependencies.json').read_bytes()).hexdigest(),'asset_mesh_objects':len(objects),'used_gray_override':args.clay,'all_helpers_relative_to_source':True},indent=2)+'\n')
    print(json.dumps({'status':'BUILT_NOT_INDEPENDENTLY_REVIEWED','glb':str(out/'model.glb'),'sha256':record['sha256']['glb'],'triangles':record['triangles'],'glb_bytes':record['glb_bytes']}))
if __name__=='__main__':main()
