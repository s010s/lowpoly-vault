# SPDX-License-Identifier: MIT
"""Deterministic Castoroides composite living reconstruction, meters, -Y forward.
Run: blender -b -t 2 --python source/generate.py -- --output-dir output
Skull design is informed by NYSM VP47 shape, not assigned Wood's Pittsfield size.
All soft tissue, whole-body dimensions and the narrow tail cross-section are inferred.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
SOURCE=Path(__file__).resolve().parent
sys.path.insert(0,str(SOURCE/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, ground_asset, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')

def main():
    av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',default='output');args=ap.parse_args(av)
    out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=True);os.chdir(out)
    p=json.loads((SOURCE/'params.json').read_text()); c=setup_scene('castoroides',p['seed'])
    main=make_material('fur_warm_umber','#736052',.90)
    belly=make_material('fur_underside','#95836C',.93)
    dark=make_material('tail_feet_muzzle','#52443B',.94)
    black=make_material('eyes_nostrils','#1B1916',.42)
    enamel=make_material('incisor_ochre_ivory','#D9B978',.56)
    ear=make_material('ear_inner','#6E5345',.95)
    mats=[main,belly,dark,black,enamel,ear]
    def obj(name,v,f,mat):
        sx=p['body_width_m']/.53; sz=p['shoulder_m']/.60; sy=p['headbody_m']/1.45
        jawlift=.020 if name=='lower_jaw' or name.startswith('lower_fluted') else 0
        footdrop=0
        vv=[(x*sx,(y*sy if y<=.385 else .385*sy+(y-.385)*p['tail_m']/.60)+.230*sy,(z+jawlift-footdrop)*sz) for x,y,z in v]
        return mesh_object(name,vv,f,mat,c)
    def tube(name,stations,sides,mat,flutes=0):
        # Closed contour loft. Each station: center xyz, radius in local X,
        # radius in local second normal; transport keeps organic joints legible.
        vs=[];fs=[]
        for i,(center,rx,rz) in enumerate(stations):
            center=Vector(center)
            a=Vector(stations[max(i-1,0)][0]); b=Vector(stations[min(i+1,len(stations)-1)][0]); tangent=(b-a).normalized()
            axis=Vector((1,0,0));axis=(axis-tangent*axis.dot(tangent)).normalized()
            if axis.length<.1: axis=Vector((0,1,0))
            other=tangent.cross(axis).normalized()
            for j in range(sides):
                t=2*math.pi*j/sides
                flute=(1+.105*math.cos(flutes*t)) if flutes else 1
                vs.append(tuple(center+axis*(rx*math.cos(t)*flute)+other*(rz*math.sin(t)*flute)))
        for i in range(len(stations)-1):
            for j in range(sides):
                fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
        fs.append(tuple(range(sides-1,-1,-1)));fs.append(tuple((len(stations)-1)*sides+j for j in range(sides)))
        return obj(name,vs,fs,mat)
    def loft_y(name,rings,sides,mat,underside=False):
        # Ring parameters y,halfwidth,z_bottom,z_top; no untouched ellipsoid body.
        verts=[];faces=[]
        for i,(y,rx,lo,hi) in enumerate(rings):
            for j in range(sides):
                a=2*math.pi*j/sides; z=(hi+lo)/2+(hi-lo)/2*math.sin(a)
                x=rx*math.cos(a)*(1+.025*math.sin(i*1.7+j*.9))
                verts.append((x,y,z))
        for i in range(len(rings)-1):
            for j in range(sides):faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
        faces.extend([tuple(range(sides-1,-1,-1)),tuple((len(rings)-1)*sides+j for j in range(sides))])
        ob=obj(name,verts,faces,[mat,belly] if underside else mat)
        if underside:
            for face in ob.data.polygons:
                center=face.center
                if center.z<.225:face.material_index=1
        return ob
    def oval(name,center,radius,mat,segments=12,rings=6,tilt=0):
        # Explicit latitude topology with single poles, baked shape and rotation.
        v=[(0,0,-1)];f=[]
        for k in range(1,rings):
            lat=-math.pi/2+math.pi*k/rings
            for j in range(segments):
                ang=2*math.pi*j/segments
                v.append((math.cos(lat)*math.cos(ang),math.cos(lat)*math.sin(ang),math.sin(lat)))
        v.append((0,0,1)); top=len(v)-1
        for j in range(segments):f.append((0,1+(j+1)%segments,1+j))
        for k in range(rings-2):
            for j in range(segments):
                a=1+k*segments+j;b=1+k*segments+(j+1)%segments;f.append((a,b,b+segments,a+segments))
        for j in range(segments):f.append((top,1+(rings-2)*segments+j,1+(rings-2)*segments+(j+1)%segments))
        verts=[]
        for x,y,z in v:
            x*=radius[0];y*=radius[1];z*=radius[2]
            xx=x*math.cos(tilt)-z*math.sin(tilt);zz=x*math.sin(tilt)+z*math.cos(tilt)
            verts.append((xx+center[0],y+center[1],zz+center[2]))
        return obj(name,verts,f,mat)
    body=loft_y('barrel_torso_neck',[
        (-.765,.100,.305,.535),(-.675,.155,.260,.565),(-.57,.205,.205,.600),
        (-.43,.240,.170,.614),(-.34,.255,.156,.637),(-.22,.265,.145,.658),(-.10,.266,.142,.670),(.015,.258,.142,.663),
        (.115,.247,.148,.643),(.190,.228,.162,.616),(.250,.204,.185,.580),(.340,.138,.235,.470),(.385,.060,.265,.365)],28,main,True)
    body['anatomical_role']='Deep trunk and short muscular neck; composite soft tissue reconstruction.'
    head=loft_y('broad_zygomatic_head',[
        (-1.035,.083,.347,.445),(-.997,.112,.325,.475),(-.928,.135,.323,.511),
        (-.845,.163,.335,.542),(-.804,.163,.342,.550),(-.769,.155,.347,.554),(-.707,.116,.356,.537)],24,main,True)
    head['shape_reference']='NYSM VP47 dorsal photograph; broad zygomatic outline, no specimen-size assignment.'
    loft_y('lower_jaw',[
        (-1.016,.073,.230,.272),(-.978,.100,.226,.284),(-.915,.120,.246,.310),(-.845,.123,.284,.365),(-.775,.107,.332,.413)],16,belly)
    # Dark recessed oral cavity, not a solid painted stripe hiding teeth.
    loft_y('oral_recess',[
        (-1.004,.058,.266,.330),(-.952,.092,.270,.338),(-.881,.106,.304,.353),(-.822,.081,.336,.375)],16,black)
    oval('nose_pad',(0,-1.038,.413),(.080,.026,.033),dark,16,6)
    for s,label in [(-1,'L'),(1,'R')]:
        oval('nostril_'+label,(s*.043,-1.060,.424),(.013,.006,.008),black,10,5)
        # Small lateral eye is partly embedded, no oversized mascot eye.
        oval('eye_rim_'+label,(s*.148,-.854,.481),(.017,.033,.027),dark,12,6)
        oval('eye_'+label,(s*.160,-.862,.489),(.009,.020,.015),black,12,6)
        oval('ear_'+label,(s*.139,-.716,.559),(.030,.026,.043),main,12,6,tilt=-s*.20)
        oval('ear_inner_'+label,(s*.145,-.744,.569),(.019,.007,.027),ear,12,6,tilt=-s*.20)
        # Pairs of exposed incisors. Longitudinal radial fluting is real geometry.
        x=s*.034
        up=tube('upper_fluted_incisor_'+label,[((x,-1.011,.360),.025,.027),((x,-1.043,.349),.025,.025),((x,-1.068,.332),.023,.023),((x,-1.081,.315),.020,.020),((x,-1.082,.305),.017,.017)],32,enamel,8)
        up['surface']='8 longitudinal channels; rounded tapered terminal, not broad chisel or tusk.'
        lo=tube('lower_fluted_incisor_'+label,[((x,-.995,.237),.022,.023),((x,-1.026,.240),.021,.022),((x,-1.055,.248),.020,.021),((x,-1.076,.263),.017,.018),((x,-1.080,.270),.014,.014)],32,enamel,8)
        # Forelimb flowing shoulder to wrist. Both are offset for grounded stance.
        tube('forelimb_'+label,[((s*.177,-.522,.417),.080,.085),((s*.205,-.532,.345),.075,.080),((s*.220,-.535,.292),.062,.068),((s*.219,-.519,.226),.052,.060),((s*.218,-.514,.173),.044,.050),((s*.222,-.568,.078),.035,.038)],16,main)
        tube('forefoot_'+label,[((s*.222,-.534,.064),.042,.036),((s*.225,-.610,.048),.065,.042),((s*.227,-.667,.038),.061,.030),((s*.226,-.699,.031),.039,.022)],12,dark)
        # Hind haunch and flexed shin are larger, with the longer rear foot visible.
        tube('hindlimb_'+label,[((s*.164,.213,.418),.114,.137),((s*.205,.191,.350),.108,.121),((s*.227,.184,.287),.088,.102),((s*.238,.241,.215),.070,.080),((s*.241,.273,.174),.051,.057),((s*.244,.218,.066),.043,.040)],18,main)
        tube('hindfoot_'+label,[((s*.244,.254,.060),.047,.039),((s*.253,.139,.044),.084,.040),((s*.255,.045,.034),.081,.031),((s*.251,-.003,.026),.052,.022)],14,dark)
        # Five rounded short digits per foot. Kept as semantic joined toe groups,
        # with conservative shallow webbing supplied by the broad foot loft.
        for foot,y,xc,w,rad in [('fore',-.697,s*.226,.047,.012),('hind',-.003,s*.251,.064,.015)]:
            digits=[]
            for k in range(-2,3):
                x=xc+k*w*.45; length=.042-abs(k)*.006
                digit=tube(foot+'_digit_'+label+str(k),[
                    ((x,y+.018,.032),rad,rad*.8),((x,y-length*.5,.026),rad*.9,rad*.70),
                    ((x,y-length,.020),rad*.65,rad*.52)],8,dark)
                digits.append(digit)
            bpy.ops.object.select_all(action='DESELECT')
            for digit in digits:digit.select_set(True)
            bpy.context.view_layer.objects.active=digits[0]
            bpy.ops.object.join();digits[0].name=foot+'_five_digits_'+label
    tail=tube('narrow_tapered_tail',[
        ((0,.335,.295),.069,.067),((.016,.440,.228),.057,.053),((.037,.559,.155),.046,.042),
        ((.048,.689,.098),.036,.032),((.050,.810,.062),.026,.023),((.033,.919,.041),.015,.013),((.009,.979,.030),.004,.004)],14,dark)
    tail['uncertainty']='Bell Museum probable long narrow tail; external cross-section and exact length inferred. Not modern Castor paddle.'
    # Raised dorsal surface is restrained broad facet topology, with no haircards.
    root=bpy.data.objects[c['asset_root']]
    root['origin']='Ground contact center between planted fore and hind foot pads';root['representation']='living-reconstruction';root['taxon']='Castoroides ohioensis'
    root['scale_note']='Composite estimated 1.45 m head-body and 0.60 m tail, not one measured specimen.'
    root['reference_separation']='Minnesota juvenile skeleton; NYSM VP47 skull; Wood1914 independent Pittsfield skull.'
    for part in c.all_objects:
        if part.type=='MESH' and part.name.startswith(('forefoot_','hindfoot_')):
            lowest=min(v.co.z for v in part.data.vertices)
            for vertex in part.data.vertices:vertex.co.z-=lowest
    ground_asset(c,False)
    scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
    scene['source_generator']='source/generate.py';scene['consuming_threejs_version']='0.180.0'
    sourceqa=audit_source(c,16000)
    if sourceqa['errors']:raise RuntimeError(sourceqa['errors'])
    scene.render.filepath='//preview.png'
    # Clear default UI browser locations before the first public source save.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'/'*1023
                    space.params.directory=b'//'
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in c.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    options=dict(filepath='model.glb',export_format='GLB',use_selection=True,export_yup=True,export_apply=True,
       export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',
       export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,
       export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={v.identifier for v in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Required exporter options unavailable')
    bpy.ops.export_scene.gltf(**options)
    exported=audit_glb('model.glb',16000,6,48)
    if exported['errors']:raise RuntimeError(exported['errors'])
    if exported['bytes']>2200000:raise RuntimeError('GLB byte budget')
    b=sourceqa['bounds_blender_m'];g=exported['bounds_m']
    delta=max(abs(g[side][i]-value[i]) for side,value in [('min',[b['min'][0],b['min'][2],-b['max'][1]]),('max',[b['max'][0],b['max'][2],-b['min'][1]])] for i in range(3))
    if delta>1e-5:raise RuntimeError('Source/export bounds mismatch')
    write('build.json',{'asset_id':'castoroides','revision':'r001','blender':bpy.app.version_string,'python':sys.version.split()[0],
      'seed':p['seed'],'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'glb_sha256':sha('model.glb'),
      'blend_sha256':sha('model.blend'),'source':sourceqa,'glb':exported,'bounds_export_max_error_m':delta,
      'export_options':options,'consuming_threejs_version':'0.180.0','textures':0,
      'warning_review':'All anatomical meshes and digit components are closed. Intersections at shoulders, haunches, digits and facial anatomy are intentional assembly joins, not a watertight printable union.',
      'scope':'Source/static GLB technical evidence only, not independent review, WebGL rendering or scene performance.'})
    print('BUILD_OK',exported['scene_triangles'],exported['bytes'],sha('model.glb'))

if __name__=='__main__':main()
