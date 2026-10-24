# SPDX-License-Identifier: MIT
"""Original deterministic Aegirocassis reconstruction.

Run with Blender background Python and arguments: -- --output DESTINATION
--clay produces only inexpensive private blockout views. --no-render rebuilds
editable source and GLB without presentation. All imports are package-relative.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import shutil
import sys
import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'deps'))
import asset_common as common
from qa_glb_scale_aware import audit_glb, read_glb, semantic_digest


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Geometry:
    def __init__(self):
        self.vertices = []
        self.faces = []
    def add(self, vertices, faces):
        base = len(self.vertices)
        self.vertices.extend(tuple(v) for v in vertices)
        self.faces.extend(tuple(base + i for i in f) for f in faces)
    def tube(self, points, radii, sides=6, flatten=1.0):
        points = [Vector(p) for p in points]
        vertices, faces = [], []
        for i, p in enumerate(points):
            tangent = (points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
            guide = Vector((1,0,0))
            if abs(tangent.dot(guide)) > 0.95: guide = Vector((0,1,0))
            a = (guide - tangent * tangent.dot(guide)).normalized()
            b = tangent.cross(a).normalized()
            radius = radii[i] if isinstance(radii, (list,tuple)) else radii
            for j in range(sides):
                angle = 2 * math.pi * j / sides
                vertices.append(p + a * (math.cos(angle)*radius*flatten) + b * (math.sin(angle)*radius))
        for i in range(len(points)-1):
            for j in range(sides):
                k = i*sides+j; n = i*sides+(j+1)%sides
                faces.append((k,n,n+sides,k+sides))
        faces.append(tuple(reversed(range(sides))))
        faces.append(tuple((len(points)-1)*sides+j for j in range(sides)))
        self.add(vertices, faces)
    def loft_y(self, rings, sides=12):
        # Rings are y, center-x, center-z, half-width, half-height.
        vs, fs = [], []
        for y,x,z,w,h in rings:
            for j in range(sides):
                a = 2*math.pi*j/sides
                vs.append((x+w*math.cos(a),y,z+h*math.sin(a)))
        for i in range(len(rings)-1):
            for j in range(sides):
                fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
        fs.append(tuple(reversed(range(sides))))
        fs.append(tuple((len(rings)-1)*sides+j for j in range(sides)))
        self.add(vs,fs)
    def solid_outline(self, outline, thickness, normal=(0,0,1), crown=0.0):
        n = Vector(normal).normalized(); points=[Vector(p) for p in outline]; count=len(points)
        center=sum(points,Vector())/count
        vs=[p+n*thickness/2 for p in points]+[p-n*thickness/2 for p in points]
        vs.extend([center+n*(thickness/2+crown),center-n*thickness/2])
        fs=[]
        for i in range(count):
            j=(i+1)%count
            fs.extend([(2*count,i,j),(2*count+1,count+j,count+i),(i,count+i,count+j,j)])
        self.add(vs,fs)
    def object(self, name, material, collection, smooth=False):
        obj=common.mesh_object(name,self.vertices,self.faces,material,collection)
        if smooth:
            for p in obj.data.polygons: p.use_smooth=True
        return obj


def make_model(params):
    coll=common.setup_scene('aegirocassis',params['seed'])
    mats={k:common.make_material(k,v,roughness=0.84) for k,v in params['palette'].items()}
    root=bpy.data.objects['aegirocassis']
    root['reconstruction']='living-reconstruction; fossil-informed original geometry'
    root['limits']='Colours, eyes, pose and soft tissues inferred; sparse enlarged setae; no exact mesh-size claim'
    # Low central shield with a deliberate axial keel and closed underside.
    g=Geometry()
    sections=[(-1.05,.005,.499,.506),(-.91,.059,.501,.531),(-.72,.108,.508,.568),(-.50,.151,.516,.610),(-.29,.179,.522,.637),(-.12,.177,.516,.630),(-.025,.139,.506,.599),(.015,.042,.501,.548)]
    vs=[]
    for y,w,edge,top in sections:
        # A mildly peaked six-point dorsal arc plus a shallow ventral return.
        for xf,z in [(-1,edge),(-.69,edge+(top-edge)*.56),(0,top),(.69,edge+(top-edge)*.56),(1,edge),(.68,edge-.013),(0,edge-.020),(-.68,edge-.013)]:
            vs.append((xf*w,y,z))
    fs=[]
    for i in range(len(sections)-1):
        for j in range(8): fs.append((i*8+j,i*8+(j+1)%8,(i+1)*8+(j+1)%8,(i+1)*8+j))
    fs.extend([tuple(reversed(range(8))),tuple((len(sections)-1)*8+j for j in range(8))])
    g.add(vs,fs)
    # Modest posterior-lateral downturned processes are integral shell components.
    for sign in [-1,1]:
        g.solid_outline([(sign*.177,-.26,.526),(sign*.174,-.09,.513),(sign*.154,-.017,.493),(sign*.187,-.105,.457)],.009,normal=(sign,0,.25))
    g.object('central-keel-shield',mats['carapace'],coll)
    # Narrow soft head connection, entirely beneath the shell.
    g=Geometry();g.loft_y([(-.42,0,.420,.05,.025),(-.29,0,.438,.11,.059),(-.08,0,.438,.137,.062),(.045,0,.438,.143,.062)])
    g.object('cephalic-soft-connection',mats['underside'],coll)
    for sign,side in [(-1,'left'),(1,'right')]:
        g=Geometry();g.loft_y([(-.59,sign*.104,.427,.010,.014),(-.50,sign*.142,.430,.038,.060),(-.34,sign*.164,.431,.046,.081),(-.17,sign*.167,.434,.041,.077),(-.045,sign*.153,.443,.025,.056),(.008,sign*.136,.451,.006,.017)],12)
        g.object(side+'-oval-lateral-shield',mats['carapace'],coll)
        # Small inferred eyes in posterior shield gaps, not anterior stalks.
        g=Geometry();g.loft_y([(-.061,sign*.155,.525,.008,.008),(-.047,sign*.159,.525,.018,.022),(-.026,sign*.160,.525,.018,.022),(-.014,sign*.155,.525,.008,.008)],10)
        g.object(side+'-inferred-eye',mats['inferred_eyes'],coll,True)
    # Eleven broad low segments: the first ten bear paired flap tiers.
    centers=[.071,.174,.277,.380,.483,.586,.689,.792,.888,.975,1.032]
    widths=[.153,.172,.181,.177,.168,.154,.138,.117,.095,.068,.038]
    lengths=[.102]*8+[.090,.077,.049]
    core=Geometry();core.loft_y([(y,0,.420,w*.86,.047*(.66+.34*w/.181)) for y,w in zip([.012]+centers+[1.059],[.142]+widths+[.018])],12)
    core.object('continuous-ventral-trunk-core',mats['underside'],coll)
    for i,(y,w,length) in enumerate(zip(centers,widths,lengths)):
        h=.064*(.65+.35*w/.181)
        g=Geometry();g.loft_y([(y-length*.49,0,.438,w*.94,h*.89),(y-length*.31,0,.438,w,h),(y+length*.33,0,.436,w*.985,h*.99),(y+length*.49,0,.434,w*.91,h*.85)],12)
        g.object(f'trunk-segment-{i+1:02}',mats['body'],coll)
        if i==10: continue
        # Simplified fore-aft setal-blade ridges form a transverse dorsal band.
        g=Geometry()
        for j in range(9):
            x=(j-4)*w*.19
            z=.439+h*math.sqrt(max(.1,1-(x/w)**2))
            g.solid_outline([(x-.003,y-.029,z),(x+.003,y-.029,z),(x+.003,y+.027,z-.001),(x-.003,y+.027,z-.001)],.005,crown=.002)
        g.object(f'dorsal-setal-blade-band-{i+1:02}',mats['body'],coll)
        span=.146*(.40+.60*w/.181)
        fin_scale=.40+.60*w/.181
        for sign,side in [(-1,'left'),(1,'right')]:
            # Dorsal shark-fin form: raised pointed tip and recurved trailing margin.
            x=w*.88; z=.472
            outline=[(x,y-.039,z),(x+.039,y-.035,z+.043),(x+.092,y-.003,z+.103),(x+.076,y+.009,z+.062),(x+.075,y+.025,z+.031),(x+.045,y+.035,z+.008),(x,y+.038,z)]
            g=Geometry();g.solid_outline([(sign*(x+(a-x)*fin_scale),b,z+(c-z)*fin_scale) for a,b,c in outline],.009,normal=(sign*.25,0,1),crown=.006)
            # Only the failed insertion roots move; the external fin contour is fixed.
            if i in (0,4,5,6,7,8,9):
                for vi in (0,6,7,13):
                    a,b,c=g.vertices[vi];g.vertices[vi]=(a-sign*.020,b,c)
            g.object(f'{side}-dorsal-flap-{i+1:02}',mats['flaps'],coll)
            # Longer lower paddles have rounded polygonal tips and real air gaps.
            x=w*.90; z=.396
            outline=[(x,y-.040,z),(x+span*.60,y-.026,z-.026),(x+span*.94,y+.002,z-.041),(x+span,y+.021,z-.044),(x+span*.93,y+.036,z-.040),(x+span*.57,y+.038,z-.023),(x,y+.038,z)]
            g=Geometry();g.solid_outline([(sign*a,b,c) for a,b,c in outline],.010,crown=.007)
            for vi in (0,6,7,13):
                a,b,c=g.vertices[vi];g.vertices[vi]=(a-sign*min(.040,w*.5),b,c)
            g.object(f'{side}-ventral-flap-{i+1:02}',mats['flaps'],coll)
    # Open bilateral filter basket. Six long endites per side follow the 2023
    # revision; a separate short proximal endite is not counted among the six.
    for sign,side in [(-1,'left'),(1,'right')]:
        shaft=Geometry(); bristles=Geometry()
        for j in range(7):
            y=-.155-j*.050
            x=sign*(.132+.005*j)
            z=.383-.003*j
            shaft.loft_y([(y-.023,x,z,.020,.024),(y-.014,x,z,.025,.029),(y+.014,x,z,.025,.029),(y+.023,x,z,.020,.024)],8)
        shaft.object(side+'-schematic-articulated-shaft',mats['underside'],coll)
        for j in range(6):
            y0=-.205-j*.050; x0=.137+.005*j; z0=.380-.003*j
            length=.350-.004*j
            def curve(t):
                return Vector((sign*(x0-.065*t**1.5),y0-.067*t**3,z0-length*t))
            path=[curve(t/8) for t in range(9)]
            radii=[.0120,.0118,.0112,.0107,.0100,.0090,.0074,.0052,.0025]
            g=Geometry();g.tube(path,radii,6,.58)
            g.object(f'{side}-long-endite-{j+1}',mats['carapace'],coll)
            count=params['sixth_setae_per_endite'] if j==5 else params['fine_setae_per_endite']
            for k in range(count):
                t=.105+.80*k/(count-1); p=curve(t); p.y-=.007
                # The sixth row is shorter, stouter and more curved, not a copy.
                length_s=.028 if j==5 else .052
                r=.0023 if j==5 else .00145
                end=p+Vector((-sign*length_s*.74,-length_s*.77,-.007 if j==5 else .001))
                mid=p+Vector((-sign*length_s*.45,-length_s*.43,.005 if j==5 else .002))
                first=len(bristles.vertices)
                bristles.tube([p,mid,end],[r,r*.75,r*.28],4)
                if (j<5 and k>=count-2) or (j==5 and k==count-1):
                    # Inset the four root-ring vertices only; keep mid/tip and radii.
                    for vi in range(first,first+4):
                        a,b,c=bristles.vertices[vi];bristles.vertices[vi]=(a,b+.005,c)
        # One short proximal comb with seven coarser teeth.
        g=Geometry();base=Vector((sign*.131,-.151,.380)); end=Vector((sign*.105,-.174,.224))
        g.tube([base,base.lerp(end,.5),end],[.012,.010,.005],6,.65)
        g.object(side+'-short-proximal-comb',mats['carapace'],coll)
        for k in range(params['proximal_comb_setae']):
            t=.20+.70*k/(params['proximal_comb_setae']-1); p=base.lerp(end,t)
            bristles.tube([p,p+Vector((-sign*.018,-.014,.002)),p+Vector((-sign*.030,-.031,.001))],[.002,.0015,.0008],4)
        bristles.object(side+'-representative-filter-setae',mats['filter_setae'],coll)
    # Preserve an identity root; center horizontally and mount the lowest tip.
    shift=Vector(common.ground_asset(coll,center_xy=True))
    for obj in coll.objects:
        if obj.type=='MESH':
            # Bake placement into original editable mesh coordinates.
            matrix=obj.matrix_basis.copy()
            obj.data.transform(matrix)
            obj.matrix_basis.identity()
    bpy.context.view_layer.update()
    return coll, {'source_centering_shift_m':list(shift),'trunk_segments':11,'dorsal_flaps':20,'ventral_flaps':20,'long_endites':12,'short_proximal_endites':2,'dorsal_bands':10,'eyes':2,'mouth':'omitted; unresolved species-specific oral cone','no_tail_fan':True,'no_textures':True}


def render_exact(glb, output, params, clay=False):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(glb.resolve()))
    imported=[o for o in bpy.context.scene.objects if o.type=='MESH']
    # The stock Blender importer restores Blender Z-up and -Y forward.
    bpy.context.view_layer.update()
    points=[o.matrix_world @ v.co for o in imported for v in o.data.vertices]
    low,high=common._bounds(points); center=Vector([(a+b)/2 for a,b in zip(low,high)])
    span=max(b-a for a,b in zip(low,high))
    scene=bpy.context.scene; scene.render.engine='CYCLES';scene.cycles.device='CPU'
    scene.cycles.samples=8 if clay else params['renderer']['samples'];scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    resolution=400 if clay else params['renderer']['resolution']
    scene.render.resolution_x=resolution;scene.render.resolution_y=resolution;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=True
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('neutral-studio');world.use_nodes=True;scene.world=world
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.75,.75,.75,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
    # Same scale-aware soft key/fill and exposure convention as common helper.
    lights=[('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]
    for name,position,energy,size in lights:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(position)*span/2;common._look_at(ob,center)
    cam_data=bpy.data.cameras.new('diagnostic-camera');cam_data.type='ORTHO'
    cam=bpy.data.objects.new('diagnostic-camera',cam_data);scene.collection.objects.link(cam);scene.camera=cam
    if clay:
        mat=common.make_material('neutral-clay','#A0A0A0',roughness=.9)
        bpy.context.view_layer.material_override=mat
    directions={'front':(0,-1,0),'side':(1,0,0),'top':(0,0,1),'perspective':tuple(params['renderer']['perspective_direction'])}
    records={}
    output.mkdir(parents=True,exist_ok=True)
    for label,direction in directions.items():
        cam.location=center+Vector(direction).normalized()*span*4;common._look_at(cam,center);bpy.context.view_layer.update()
        inverse=cam.matrix_world.inverted(); projected=[inverse@p for p in points]
        xs=[p.x for p in projected];ys=[p.y for p in projected]
        cam.location+=cam.matrix_world.to_3x3()@Vector(((min(xs)+max(xs))/2,(min(ys)+max(ys))/2,0))
        cam_data.ortho_scale=max(max(xs)-min(xs),max(ys)-min(ys))*(1.18 if clay else 1.16)
        scene.render.filepath=str((output/(label+'.png')).resolve());bpy.ops.render.render(write_still=True)
        records[label]={'direction_blender':list(direction),'camera_location_m':list(cam.location),'orthographic_scale_m':cam_data.ortho_scale,'image_sha256':sha(output/(label+'.png'))}
    return {'glb_sha256':sha(glb),'clean_import':True,'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','samples':scene.cycles.samples,'resolution':[resolution,resolution],'threads':2,'transparent':True,'colour_management':{'view':'Standard','look':'None','exposure':0,'gamma':1},'views':records,'scope':'Exact delivered GLB import in Blender only; not browser GPU or populated scene validation'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);parser.add_argument('--no-render',action='store_true');parser.add_argument('--clay',action='store_true');parser.add_argument('--render-only',action='store_true')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=Path(args.output).expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
    params=json.loads((HERE/'params.json').read_text());budget=params['geometry_policy']
    if not args.render_only:
        collection,anatomy=make_model(params)
        source=common.audit_source(collection,max_triangles=budget['max_triangles'])
        if source['errors']: raise RuntimeError(source['errors'])
        scene=bpy.context.scene;scene.render.threads_mode='FIXED';scene.render.threads=2
        # Runtime-resolved absolute save target prevents cwd-relative save hazards.
        bpy.context.preferences.filepaths.save_version=0
        scene.render.filepath='//'
        # Factory UI state can retain an absolute file-browser directory.
        for screen in bpy.data.screens:
            for area in screen.areas:
                for space in area.spaces:
                    if space.type=='FILE_BROWSER' and space.params is not None:
                        space.params.directory=b'//'
                        space.params.filename=''
        bpy.ops.wm.save_as_mainfile(filepath=str((out/'model.blend').resolve()),relative_remap=True)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in collection.all_objects: obj.select_set(True)
        options=dict(filepath=str((out/'model.glb').resolve()),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
        available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
        missing=set(options)-available
        if missing: raise RuntimeError('Required exporter options absent: '+repr(sorted(missing)))
        bpy.ops.export_scene.gltf(**options)
        audit=audit_glb(out/'model.glb',max_triangles=budget['max_triangles'],max_materials=budget['max_materials'],max_primitives=budget['max_primitives']);audit['file']='model.glb'
        bounds=source['bounds_blender_m']; expected_min=[bounds['min'][0],bounds['min'][2],-bounds['max'][1]];expected_max=[bounds['max'][0],bounds['max'][2],-bounds['min'][1]]
        delta=max(abs(audit['bounds_m'][key][i]-expected[i]) for key,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
        audit['source_export_bounds_max_error_m']=delta
        if delta>0.0001: audit['errors'].append('Source/export axis-converted bounds differ')
        if audit.get('scene_triangles')!=source['triangles']: audit['errors'].append('Source/export triangle count mismatch')
        if audit['errors']: raise RuntimeError(audit['errors'])
        if audit['bytes']>budget['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
        if audit['materials']>budget['max_materials']: raise RuntimeError('Material budget exceeded')
        doc,binary,raw=read_glb(out/'model.glb')
        record={'asset_id':params['asset_id'],'revision':params['revision'],'blender':bpy.app.version_string,'seed':params['seed'],'source_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'dependencies_sha256':sha(HERE/'dependencies.json'),'source_audit':source,'glb_audit':audit,'semantic_digest':semantic_digest(doc,binary),'anatomy_inventory':anatomy,'export_settings':{k:v for k,v in options.items() if k!='filepath'},'file_sha256':{'model.glb':sha(out/'model.glb'),'model.blend':sha(out/'model.blend')},'gpu':'UNKNOWN','scene':'UNKNOWN'}
        write_json(out/'qa/evidence/build.json',record)
    if not args.no_render:
        viewpath=out/'clay-views' if args.clay else out/'views'
        record=render_exact(out/'model.glb',viewpath,params,args.clay)
        write_json(out/'qa/evidence/exact-glb-views.json',record)
        if not args.clay: shutil.copyfile(out/'views/perspective.png',out/'preview.png')

if __name__=='__main__': main()
