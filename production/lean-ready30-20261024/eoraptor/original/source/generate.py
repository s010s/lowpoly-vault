#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Eoraptor lunensis reconstruction. Run with Blender 4.3.2.

Use --output to choose an empty build directory; --gray renders a low-cost
structural checkpoint. All build dependencies are sibling files in deps.
The animal is not a specimen scan. Skin, colors and the tail are artistic.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, shutil, sys
import bpy
from mathutils import Vector
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
import asset_common as common
from qa_glb_scale_aware import audit_glb

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class Form:
    """Editable closed lofts with deliberate profiles, never a primitive stack."""
    def __init__(self, name):
        self.name=name; self.vertices=[]; self.faces=[]; self.mats=[]
    def loft(self, rings, sides=12, axis='Y', material=0, palette=False):
        # rings are center, half-width, half-height; endpoints must stay nonzero.
        base=len(self.vertices)
        for k,(center,w,h) in enumerate(rings):
            c=Vector(center)
            if axis=='Y': u=Vector((1,0,0)); v=Vector((0,0,1))
            else:
                prev=Vector(rings[max(k-1,0)][0]); nxt=Vector(rings[min(k+1,len(rings)-1)][0])
                t=(nxt-prev).normalized(); ref=Vector((1,0,0))
                if abs(t.dot(ref))>0.92: ref=Vector((0,1,0))
                u=(ref-t*t.dot(ref)).normalized(); v=t.cross(u).normalized()
            for j in range(sides):
                a=2*math.pi*j/sides
                self.vertices.append(tuple(c+u*(w*math.cos(a))+v*(h*math.sin(a))))
        # Fan caps avoid collinear end triangles in elongated rings.
        start=len(self.vertices); self.vertices.append(tuple(rings[0][0]))
        end=len(self.vertices); self.vertices.append(tuple(rings[-1][0]))
        for j in range(sides):
            self.faces.append((start,base+(j+1)%sides,base+j)); self.mats.append(material)
        for k in range(len(rings)-1):
            for j in range(sides):
                a=base+k*sides+j; b=base+k*sides+(j+1)%sides
                c=base+(k+1)*sides+(j+1)%sides; d=base+(k+1)*sides+j
                self.faces.append((a,b,c,d))
                angle=2*math.pi*(j+0.5)/sides
                self.mats.append(1 if palette and math.sin(angle)>0.5 else 2 if palette and math.sin(angle)<-0.5 else material)
        for j in range(sides):
            self.faces.append((end,base+(len(rings)-1)*sides+j,base+(len(rings)-1)*sides+(j+1)%sides)); self.mats.append(material)
    def finish(self, collection, materials):
        obj=common.mesh_object(self.name,self.vertices,self.faces,materials,collection)
        for p,m in zip(obj.data.polygons,self.mats): p.material_index=m
        # Remove unused slots to keep export submissions proportional to visible use.
        used=sorted(set(self.mats)); remap={old:new for new,old in enumerate(used)}
        obj.data.materials.clear()
        for old in used: obj.data.materials.append(materials[old])
        for p,m in zip(obj.data.polygons,self.mats): p.material_index=remap[m]
        return obj

def make_animal(params, gray=False):
    col=common.setup_scene('eoraptor',params['seed'])
    colors=params['palette']
    mats=[common.make_material(name,'#929292' if gray else color,roughness=.82) for name,color in colors.items()]
    # Main light fusiform body, sternum, hip transition and tail have explicit rings.
    trunk=Form('Trunk_light_ribcage')
    trunk.loft([((0,-.225,.465),.025,.040),((0,-.192,.465),.047,.069),((0,-.135,.454),.065,.080),((0,-.06,.450),.072,.086),((0,.015,.465),.066,.074),((0,.085,.477),.055,.055),((0,.145,.477),.040,.038)],sides=16,palette=True)
    trunk.finish(col,mats)
    tail=Form('Tail_balancing_taper')
    tail.loft([((0,.08,.476),.049,.045),((0,.17,.474),.042,.039),((.005,.27,.467),.031,.031),((.014,.39,.451),.022,.024),((.021,.51,.433),.015,.018),((.022,.63,.423),.010,.012),((.016,.72,.430),.0055,.007),((.005,.79,.446),.0018,.002)],sides=12,palette=True)
    tail.finish(col,mats)
    neck=Form('Neck_moderate_S_profile')
    neck.loft([((0,-.20,.478),.035,.045),((0,-.234,.505),.032,.044),((0,-.263,.551),.027,.041),((0,-.284,.601),.024,.034),((0,-.312,.631),.023,.027),((0,-.344,.635),.024,.027)],sides=12,palette=True)
    neck.finish(col,mats)
    head=Form('Head_compact_low_skull')
    head.loft([((0,-.328,.644),.024,.024),((0,-.352,.653),.034,.035),((0,-.383,.652),.033,.034),((0,-.411,.649),.029,.026),((0,-.444,.643),.024,.020),((0,-.478,.637),.020,.016),((0,-.508,.631),.015,.012)],sides=16,palette=True)
    head.finish(col,mats)
    jaw=Form('Jaw_slender_closed')
    jaw.loft([((0,-.337,.618),.022,.010),((0,-.372,.616),.027,.012),((0,-.407,.615),.024,.009),((0,-.452,.616),.020,.007),((0,-.490,.616),.016,.005),((0,-.508,.618),.013,.003)],sides=12,material=2)
    jaw.finish(col,mats)
    # Separate, digitigrade, slightly offset legs. Their hocks remain above ground.
    for s,label,dy in [(-1,'L',.012),(1,'R',-.012)]:
        leg=Form('Hindlimb_'+label+'_digitigrade')
        x=.056*s
        leg.loft([((x,.060+dy,.470),.037,.041),((s*.071,.024+dy,.422),.040,.046),((s*.083,-.030+dy,.360),.027,.032),((s*.084,-.046+dy,.330),.022,.024),((s*.083,-.006+dy,.270),.019,.022),((s*.082,.040+dy,.188),.012,.015),((s*.083,.048+dy,.153),.011,.013),((s*.084,.014+dy,.100),.009,.011),((s*.084,-.032+dy,.040),.009,.012)],sides=12,axis='path',material=0)
        leg.finish(col,mats)
        foot=Form('Foot_'+label+'_three_weightbearing_toes')
        for j in [-1,0,1]:
            x0=s*.084+j*.007
            endx=s*.084+j*.031
            endy=-.158+dy+(abs(j)*.018)
            foot.loft([((x0,-.025+dy,.038),.009,.009),((s*.084+j*.017,-.074+dy,.022),.008,.009),((endx,endy+.024,.014),.005,.007)],sides=8,axis='path',material=0)
            foot.loft([((endx,endy+.026,.014),.0055,.007),((endx+j*.002,endy+.011,.010),.0038,.0045),((endx+j*.003,endy,.007),.0018,.002)],sides=8,axis='path',material=3)
        # Small raised inner hallux; it does not share the weightbearing floor.
        foot.loft([((s*.075,.007+dy,.065),.0055,.006),((s*.066,.027+dy,.047),.004,.005),((s*.062,.035+dy,.044),.002,.0025)],sides=8,axis='path',material=0)
        foot.finish(col,mats)
        arm=Form('Forelimb_'+label+'_flexed_grasp')
        arm.loft([((s*.043,-.182,.480),.021,.023),((s*.061,-.171,.441),.018,.021),((s*.081,-.148,.397),.013,.016),((s*.086,-.145,.371),.011,.012),((s*.092,-.180,.377),.009,.011),((s*.099,-.219,.387),.0075,.010)],sides=10,axis='path')
        arm.finish(col,mats)
        hand=Form('Hand_'+label+'_three_primary_two_reduced_digits')
        # Inward-facing palms, not permanently pronated bird wings.
        hand.loft([((s*.099,-.212,.387),.008,.012),((s*.103,-.234,.379),.009,.015),((s*.105,-.244,.367),.008,.014)],sides=10,axis='path',material=0)
        # Primary fingers fan primarily in depth/height with open gaps in oblique view.
        for j,(off,fy,fz) in enumerate([(-.013,-.270,.348),(0,-.288,.338),(.013,-.272,.327)]):
            start=(s*(.103+off),-.239,.372-off*.5)
            mid=(s*(.109+off*1.5),fy+.011,fz+.011)
            tip=(s*(.105+off*1.8),fy,fz)
            hand.loft([(start,.005,.006),(mid,.0045,.005),(tip,.0035,.004)],sides=8,axis='path',material=0)
            hand.loft([(tip,.0037,.0045),((s*(.100+off*1.8),fy-.004,fz-.009),.0027,.003),((s*(.093+off*1.8),fy+.003,fz-.013),.0013,.0016)],sides=8,axis='path',material=3)
        for j in [0,1]:
            hand.loft([((s*(.116+j*.004),-.232,.375),.0038,.0045),((s*(.126+j*.004),-.245,.366+j*.005),.003,.0034),((s*(.127+j*.004),-.251,.361+j*.006),.0018,.002)],sides=8,axis='path',material=0)
        hand.finish(col,mats)
    if not gray:
        for s,label in [(-1,'L'),(1,'R')]:
            features=Form('Facial_features_'+label)
            # Surface-mounted faceted eye lens with small dark pupil.
            features.loft([((s*.0295,-.372,.661),.010,.010),((s*.0345,-.372,.661),.009,.009),((s*.036,-.372,.661),.0065,.007)],sides=12,axis='path',material=4)
            features.loft([((s*.036,-.373,.661),.004,.0045),((s*.037,-.373,.661),.0038,.0042)],sides=10,axis='path',material=5)
            features.loft([((s*.018,-.481,.641),.0034,.002),((s*.020,-.481,.641),.0028,.0017)],sides=8,axis='path',material=5)
            features.finish(col,mats)
        # A geometric lip line avoids large exposed carnivore teeth on a light head.
        lips=Form('Closed_mouth_lip_line')
        for s in [-1,1]:
            lips.loft([((s*.025,-.369,.625),.0014,.0015),((s*.024,-.410,.625),.0013,.0014),((s*.019,-.461,.623),.0012,.0012),((s*.014,-.503,.621),.001,.001)],sides=6,axis='path',material=5)
        lips.finish(col,mats)
    common.ground_asset(col, center_xy=False)
    root=bpy.data.objects.get('eoraptor')
    root['taxon']='Eoraptor lunensis'; root['representation']='living-reconstruction'
    root['scientific_limit']='Original artistic soft tissues, coloration, posture and tail; not a measured holotype copy or a modern phylogenetic assertion.'
    return col

def render_views(col,out,views,resolution,samples,transparent):
    out.mkdir(parents=True,exist_ok=True)
    for view in views:
        # Reuse the canonical lighting/color/framing helper; set only the recorded
        # diagonal camera direction for the oblique evidence view.
        old_look=common._look_at
        if view=='perspective':
            def diagonal(obj,target):
                if obj.type=='CAMERA':
                    distance=(obj.location-Vector(target)).length
                    obj.location=Vector(target)+Vector((1,-1,1)).normalized()*distance
                old_look(obj,target)
            common._look_at=diagonal
        common.render_previews(col,out,views=('hero' if view=='perspective' else view,),resolution=resolution,samples=samples,transparent=transparent)
        common._look_at=old_look
        (out/('preview-'+('hero' if view=='perspective' else view)+'.png')).rename(out/(view+'.png'))

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=HERE.parent); parser.add_argument('--gray',action='store_true'); parser.add_argument('--render',action='store_true')
    args=parser.parse_args(argv); out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    params=json.loads((HERE/'params.json').read_text()); col=make_animal(params,args.gray)
    bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
    if args.gray:
        render_views(col,out,('front','side','perspective'),320,8,False)
        write(out/'gray-audit.json',common.audit_source(col,18000)); return
    source=common.audit_source(col,18000)
    if source['errors']: raise RuntimeError(str(source['errors']))
    scene=bpy.context.scene; scene['asset_license']='CC-BY-4.0'; scene['asset_author']='Leon Made This / s010s'
    scene['source_generator']='source/generate.py'; scene['source_parameters']='source/params.json'
    bpy.context.preferences.filepaths.save_version=0
    scene.render.filepath='//renders/'
    # A scene datablock library is a normal editable blend with no authoring UI
    # session, embedded scripts, external resources, or saved computer path.
    bpy.data.libraries.write(str(out/'model.blend'),{scene},path_remap='RELATIVE_ALL',fake_user=True,compress=False)
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.all_objects: obj.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['eoraptor']
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    assert not set(options)-available, sorted(set(options)-available)
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    old=os.getcwd(); os.chdir(out)
    try: glb=audit_glb(Path('model.glb'),18000,8,36)
    finally: os.chdir(old)
    if glb['errors']: raise RuntimeError(str(glb['errors']))
    b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][side][i]-expected[side][i]) for side in ['min','max'] for i in range(3))
    assert delta<.0001 and glb['scene_triangles']==source['triangles']
    write(out/'qa/evidence/build.json',{'status':'PASS','scope':'Source/static GLB and axis-converted bounds only','blender_version':bpy.app.version_string,'seed':params['seed'],'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'glb_sha256':digest(out/'model.glb'),'blend_sha256':digest(out/'model.blend'),'source':source,'glb':glb,'bounds_delta_m':delta,'export_options':options})
    if args.render:
        glb_hash=digest(out/'model.glb'); collection=common.setup_scene('eoraptor-proof')
        bpy.ops.import_scene.gltf(filepath=str(out/'model.glb'))
        for obj in list(bpy.context.selected_objects): common.link_object(obj,collection,parent=False)
        imported_meshes=[o for o in collection.all_objects if o.type=='MESH']
        imported_tris=sum(len(o.data.loop_triangles) if (o.data.calc_loop_triangles() is None) else 0 for o in imported_meshes)
        assert imported_tris==glb['scene_triangles']
        render_views(collection,out/'views',('front','side','top','perspective'),640,32,True)
        shutil.copyfile(out/'views/perspective.png',out/'preview.png')
        write(out/'qa/evidence/views.json',{'status':'RENDERED_NOT_INDEPENDENTLY_REVIEWED','source':'Clean Blender import of delivered GLB','glb_sha256':glb_hash,'blender_version':bpy.app.version_string,'engine':'Cycles CPU','resolution':[640,640],'samples':32,'transparent':True,'view_transform':'Standard','look':'None','exposure':0,'gamma':1,'camera':'orthographic','directions':{'front':[0,-1,0],'side':[1,0,0],'top':[0,0,1],'perspective':[1,-1,1]},'lighting':'asset_common canonical neutral key/fill','imported_triangles':imported_tris,'views':{v:{'path':'views/'+v+'.png','sha256':digest(out/'views'/f'{v}.png')} for v in ['front','side','top','perspective']},'preview_sha256':digest(out/'preview.png')})

if __name__=='__main__': main()
