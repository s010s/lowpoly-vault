#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Saltasaurus living reconstruction; Blender 4.3.2, no external assets.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output .
Geometry is original; scale, pose and armour distribution are reconstruction.
"""
import argparse, hashlib, json, math, os, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from asset_common import setup_scene,make_material,mesh_object,ground_asset,audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

class Profiles:
    def __init__(self,name,mats): self.name=name;self.mats=mats;self.v=[];self.f=[];self.mi=[];self.groups={}
    def add(self,name,v,f,mi=None):
        n=len(self.v);self.v.extend(v);self.f.extend(tuple(n+i for i in q) for q in f);self.mi.extend(mi if mi is not None else [0]*len(f));self.groups[name]=list(range(n,len(self.v)))
    def axial(self,name,sections,n=24,palette=False):
        v=[];f=[];mi=[]
        for y,z,rx,up,down in sections:
            for j in range(n):
                a=2*math.pi*j/n;s=math.sin(a);v.append((rx*math.cos(a),y,z+(up if s>=0 else down)*s))
        for k in range(len(sections)-1):
            for j in range(n):
                f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
                s=math.sin(2*math.pi*(j+.5)/n);mi.append(1 if palette and s>.70 else 2 if palette and s<-.68 else 0)
        for k,rev in [(0,True),(len(sections)-1,False)]:
            c=len(v);v.append((0,sections[k][0],sections[k][1]))
            for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j) if rev else (c,k*n+j,k*n+(j+1)%n));mi.append(0)
        self.add(name,v,f,mi)
    def tube(self,name,nodes,n=12,frame=(1,0,0)):
        centers=[Vector(a[:3]) for a in nodes];v=[];f=[];ref=Vector(frame)
        for k,a in enumerate(nodes):
            tangent=(centers[min(k+1,len(nodes)-1)]-centers[max(k-1,0)]).normalized();u=ref-tangent*ref.dot(tangent)
            if u.length<.001:u=Vector((0,1,0))-tangent*tangent.y
            u.normalize();w=tangent.cross(u).normalized()
            for j in range(n):
                t=2*math.pi*j/n;v.append(tuple(centers[k]+u*a[3]*math.cos(t)+w*a[4]*math.sin(t)))
        for k in range(len(nodes)-1):
            for j in range(n):f.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
        for k,rev in [(0,True),(len(nodes)-1,False)]:
            c=len(v);v.append(tuple(centers[k]))
            for j in range(n):f.append((c,k*n+(j+1)%n,k*n+j) if rev else (c,k*n+j,k*n+(j+1)%n))
        if name.endswith('Forelimb') or name.endswith('Hindlimb'):
            for j in range((len(nodes)-1)*n,len(nodes)*n):v[j]=(v[j][0],v[j][1],0.0)
            v[-1]=(v[-1][0],v[-1][1],0.0)
            v=[(x,y,max(0.0,z)) for x,y,z in v]
        self.add(name,v,f)
    def lens(self,name,c,ry,rz,d,sg,n=10):
        x,y,z=c;v=[(x,y+ry*math.cos(2*math.pi*j/n),z+rz*math.sin(2*math.pi*j/n)) for j in range(n)];v.extend([(x+sg*d,y,z),(x-sg*.008,y,z)]);f=[]
        for j in range(n):f.extend([(j,(j+1)%n,n),((j+1)%n,j,n+1)])
        self.add(name,v,f)
    def plate(self,name,point,normal,width,length,height,flat=False):
        c=Vector(point);n=Vector(normal).normalized();u=Vector((0,1,0));u=(u-u.dot(n)*n).normalized();w=n.cross(u);v=[];f=[];count=6 if flat else 8
        # Basal rim lies within the hide. Ossicles have a FLAT outward surface,
        # never the rounded basal face shown in the fossil cluster photograph.
        profiles=[(-.004,1),(height, .72)] if flat else [(-.012,1),(.003,.94),(height,.28)]
        for h,s in profiles:
            for j in range(count):
                a=2*math.pi*j/count;v.append(tuple(c+n*h+u*(length/2*s*math.cos(a))+w*(width/2*s*math.sin(a))))
        for k in range(len(profiles)-1):
            for j in range(count):f.append((k*count+j,k*count+(j+1)%count,(k+1)*count+(j+1)%count,(k+1)*count+j))
        f.append(tuple(reversed(range(count))));f.append(tuple((len(profiles)-1)*count+j for j in range(count)))
        self.add(name,v,f)
    def finish(self,col):
        ob=mesh_object(self.name,self.v,self.f,self.mats,col)
        for poly,idx in zip(ob.data.polygons,self.mi):poly.material_index=idx
        for name,ids in self.groups.items():ob.vertex_groups.new(name=name).add(ids,1,'REPLACE')
        ob['construction']='Closed deliberate polygon profiles; semantic editable anatomical vertex groups. Soft-tissue joins use intentional overlapping envelopes.'
        return ob

def build(p):
    col=setup_scene(p['asset_id'],p['seed']);rng=random.Random(p['seed']);m={k:make_material('Saltasaurus_'+k,c,roughness=.89) for k,c in p['palette'].items()}
    body=Profiles('Continuous_SmallHead_Neck_BroadTrunk_TaperingTail',[m['skin'],m['dorsal'],m['ventral']])
    body.axial('Complete_Axial_Envelope',[
        (-3.35,2.875,.055,.065,.055),(-3.29,2.900,.104,.100,.084),
        (-3.18,2.960,.128,.145,.115),(-3.06,3.000,.144,.163,.133),
        (-2.95,2.990,.130,.158,.145),(-2.86,2.925,.117,.145,.149),
        (-2.70,2.790,.130,.160,.165),(-2.48,2.580,.156,.185,.193),
        (-2.23,2.355,.184,.219,.230),(-1.97,2.155,.222,.265,.279),
        (-1.70,1.995,.286,.340,.350),(-1.45,1.865,.410,.435,.425),
        (-1.20,1.760,.570,.530,.505),(-.95,1.690,.702,.610,.580),
        (-.65,1.650,.790,.668,.650),(-.32,1.635,.825,.695,.705),
        (0.02,1.635,.838,.705,.725),(.36,1.650,.815,.695,.703),
        (.68,1.665,.755,.672,.650),(.94,1.660,.659,.625,.560),
        (1.18,1.630,.528,.548,.460),(1.42,1.565,.414,.458,.370),
        (1.72,1.465,.322,.373,.301),(2.05,1.380,.259,.297,.241),
        (2.42,1.315,.206,.234,.190),(2.82,1.263,.162,.181,.145),
        (3.23,1.224,.122,.139,.110),(3.65,1.188,.087,.103,.082),
        (4.06,1.142,.060,.074,.060),(4.43,1.084,.039,.052,.041),
        (4.75,1.015,.025,.035,.028),(5.01,.932,.014,.023,.018),
        (5.24,.829,.007,.013,.010),(5.45,.702,.002,.003,.003)
    ],palette=True)
    trunk=body.finish(col)
    legs=Profiles('Four_Stout_Weightbearing_Limbs',[m['skin']]);nails=Profiles('Hindfoot_BluntUnguals',[m['nails']]);dark=Profiles('SmallEyes_Nares_ClosedMouth',[m['dark']])
    for sg,label,step in [(1,'Left',-.055),(-1,'Right',.055)]:
        def mir(a):return [(sg*x,y,z,rx,rz) for x,y,z,rx,rz in a]
        # Forelimb shorter than hindlimb: no elevated Brachiosaurus shoulders.
        legs.tube(label+'_Forelimb',mir([
            (.48,-.93+step,1.83,.245,.285),(.59,-1.02+step,1.57,.220,.240),
            (.635,-1.08+step,1.30,.165,.185),(.66,-1.10+step,1.06,.135,.150),
            (.665,-1.065+step,.80,.115,.130),(.67,-1.05+step,.52,.105,.120),
            (.68,-1.05+step,.25,.120,.140),(.68,-1.08+step,.095,.155,.180),
            (.68,-1.09+step,.037,.163,.188)
        ]),n=12)
        legs.tube(label+'_Hindlimb',mir([
            (.48,.71+step,1.91,.295,.325),(.62,.66+step,1.64,.300,.330),
            (.72,.58+step,1.36,.254,.290),(.75,.50+step,1.11,.185,.210),
            (.74,.56+step,.89,.145,.165),(.73,.69+step,.61,.112,.135),
            (.73,.72+step,.34,.115,.140),(.735,.64+step,.155,.175,.205),
            (.735,.56+step,.075,.210,.275),(.735,.55+step,.033,.215,.280)
        ]),n=12)
        for digit,dx,dy in [('I',-.125,-.005),('II',0,-.028),('III',.125,.018)]:
            nails.tube(label+'_HindUngual_'+digit,mir([
                (.735+dx,.337+step+dy,.085,.052,.044),(.735+dx,.280+step+dy,.071,.050,.040),(.735+dx,.250+step+dy,.060,.035,.030)
            ]),n=8)
        dark.lens(label+'_Eye',(sg*.140,-3.067,3.057),.036,.034,.013,sg,n=12)
        dark.lens(label+'_Naris',(sg*.113,-3.251,2.978),.016,.011,.005,sg,n=8)
        dark.tube(label+'_ClosedMouth',mir([
            (.059,-3.345,2.866,.0027,.0027),(.098,-3.288,2.863,.0027,.0027),
            (.122,-3.181,2.877,.0027,.0027),(.135,-3.074,2.902,.0027,.0027)
        ]),n=6,frame=(0,0,1))
    legs.finish(col);nails.finish(col);dark.finish(col)
    armour=Profiles('Embedded_DermalPlates_InferredPlacement',[m['armour']]);ossicles=Profiles('TrueScale_FlatExternal_OssiclePatches',[m['dorsal']])
    # Position on the actual faceted envelope rather than floating over an ellipse.
    bv=BVHTree.FromPolygons([v.co.copy() for v in trunk.data.vertices],[tuple(q.vertices) for q in trunk.data.polygons],all_triangles=False)
    placed=[];tries=0
    while len(placed)<p['armour_large_count'] and tries<8000:
        tries+=1;x=rng.uniform(-.76,.76);y=rng.uniform(-1.10,1.24)
        hit,n,idx,d=bv.ray_cast(Vector((x,y,3.8)),Vector((0,0,-1)),4)
        if hit is None or n.z<.28 or hit.z<1.86 or any((hit-v).length<.157 for v in placed):continue
        width=rng.uniform(.087,.113);height=rng.uniform(.023,.034)
        armour.plate('DermalPlate_%02d'%len(placed),hit,n,width,width*rng.uniform(1.02,1.25),height);placed.append(hit)
    assert len(placed)==p['armour_large_count']
    # Sparse local study patches at true millimetre scale. They are not enlarged
    # for thumbnail readability and do not claim complete armour distribution.
    count=0
    for x0,y0 in [(-.34,-.63),(.34,-.35),(-.44,.32),(.40,.78)]:
        for j in range(14):
            x=x0+(j%4)*.011+(j//4%2)*.004;y=y0+(j//4)*.011
            hit,n,idx,d=bv.ray_cast(Vector((x,y,3.8)),Vector((0,0,-1)),4)
            if hit is None:continue
            width=rng.uniform(*p['ossicle_width_range_m']);ossicles.plate('Flat_Ossicle_%02d'%count,hit,n,width,width,.0009,flat=True);count+=1
    assert count==p['ossicle_count'];armour.finish(col);ossicles.finish(col)
    shift=ground_asset(col,center_xy=False)
    points=[o.matrix_world@v.co for o in col.all_objects if o.type=='MESH' for v in o.data.vertices if (o.matrix_world@v.co).z<.045]
    shift[1]=-(min(v.y for v in points)+max(v.y for v in points))/2
    for ob in col.all_objects:
        if ob.type=='MESH':ob.location.y+=shift[1]
    bpy.context.view_layer.update();root=bpy.data.objects[p['asset_id']]
    root['representation']='living-reconstruction';root['scale_basis']='8.8 m estimate for Hartman 2022 reconstruction, not measured complete specimen'
    root['scientific_limits']='Neck posture, missing anatomy, soft tissue, colour, plate positions and patches are reconstructed. Associated PVL4017 bones need not represent one individual.'
    root['armour_note']='48 small embedded plates and 56 true-scale 7-10 mm ossicles; outer ossicle faces flat, basal rounded faces not exposed. Inferred distribution, not a fossil row pattern.'
    return col,shift

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--output',type=Path,default=HERE.parent);a=pa.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text());assert bpy.app.version_string==p['blender_version'];col,shift=build(p)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2;audit=audit_source(col,p['max_triangles']);assert not audit['errors'],audit['errors']
    bpy.context.preferences.filepaths.save_version=0;bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:space.params.directory=b'_'*1023;space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),check_existing=False)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[p['asset_id']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={q.identifier for q in bpy.ops.export_scene.gltf.get_rna_type().properties};assert not set(flags)-available
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags);os.chdir(out);glb=audit_glb(Path('model.glb'),p['max_triangles'],p['max_materials'],p['max_primitives']);assert not glb['errors'],glb['errors'];assert glb['bytes']<=p['max_glb_bytes']
    b=audit['bounds_blender_m'];exp={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]};delta=max(abs(glb['bounds_m'][s][i]-exp[s][i]) for s in ['min','max'] for i in range(3));assert delta<.0001 and audit['triangles']==glb['scene_triangles']
    report={'status':'PASS','scope':'Source geometry and emitted static GLB, not independent visual or target GPU acceptance','glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'blender_version':bpy.app.version_string,'gltf_exporter_version':'4.3.47','exporter_required_flags_probed':True,'export_options':flags,'source':audit,'glb':glb,'source_export_bounds_error_m':delta,'ground_translation_m':shift,'profile':'Static uncompressed texture-free palette-only','source_components':'Six editable mesh objects; all anatomical profiles and armour pieces have semantic vertex groups','scale_note':'8.8 m horizontal nose-to-tail extent, estimated reconstructed scale rather than complete specimen measurement','armour_geometry':{'large_plate_count':48,'large_plate_width_m':[.087,.113],'exposed_plate_height_m':[.023,.034],'ossicle_count':56,'ossicle_width_m':[.007,.010],'ossicle_exposed_height_m':.0009,'ossicle_outward_face':'flat polygonal; curved basal face not exposed','placement':'Artistic hypothesis; not known exact whole-body distribution'}}
    write(out/'qa/evidence/source-export.json',report);print(json.dumps({'status':'BUILT','glb_sha256':report['glb_sha256'],'triangles':glb['scene_triangles'],'bytes':glb['bytes']}))
if __name__=='__main__':main()
