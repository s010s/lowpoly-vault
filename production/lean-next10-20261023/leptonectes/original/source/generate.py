# SPDX-License-Identifier: MIT
"""Deterministic Leptonectes r001. Run in Blender 4.3.2 with -- --output DIR.
Modes: build, gray (fresh build and four source-clay diagnostics), final (clean
import of output/model.glb and four final exact-export images). No external data.
"""
import argparse, hashlib, json, math, shutil, sys, time
from pathlib import Path
from datetime import datetime, timezone
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source,link_object,_look_at,_vertices_world,_bounds,srgb_to_linear
from qa_glb import audit_glb
P=json.loads((HERE/'params.json').read_text())
N=P['ring_segments']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,obj):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def parts(name,verts,faces,mats,indices,col):
    ob=mesh_object(name,verts,faces,mats,col)
    for poly,index in zip(ob.data.polygons,indices): poly.material_index=index
    return ob

def loft(name,sections,mat,col,ns=24,axis='X'):
    verts=[]; faces=[]; indices=[]
    # Sections: centre XYZ, two radii. Ring tangent basis is (Y,Z) or (X,Z).
    for x,y,z,a,b in sections:
        for j in range(ns):
            t=2*math.pi*j/ns
            verts.append((x,y+a*math.cos(t),z+b*math.sin(t)) if axis=='X' else (x+a*math.cos(t),y,z+b*math.sin(t)))
    for i in range(len(sections)-1):
        for j in range(ns):
            faces.append((i*ns+j,i*ns+(j+1)%ns,(i+1)*ns+(j+1)%ns,(i+1)*ns+j))
            s=math.sin(2*math.pi*(j+.5)/ns)
            indices.append((0 if s>.28 else 1 if s>-.47 else 2) if len(mat)==3 else (0 if s>=0 else 1))
    faces.extend([tuple(reversed(range(ns))),tuple((len(sections)-1)*ns+j for j in range(ns))]); indices.extend([0,0])
    return parts(name,verts,faces,mat,indices,col)

def profile(x):
    r=P['profile_x_z_ry_rz']
    for a,b in zip(r,r[1:]):
        if a[0]<=x<=b[0]:
            t=(x-a[0])/(b[0]-a[0]); return [a[k]*(1-t)+b[k]*t for k in range(1,4)]
    raise ValueError(x)

def body_sections():
    rows=P['profile_x_z_ry_rz']; out=[]
    for i,a in enumerate(rows[:-1]):
        b=rows[i+1]; p0=rows[max(0,i-1)]; p3=rows[min(len(rows)-1,i+2)]
        for t in [0,.5]:
            vals=[]
            for k in range(1,4):
                v=.5*((2*a[k])+(-p0[k]+b[k])*t+(2*p0[k]-5*a[k]+4*b[k]-p3[k])*t*t+(-p0[k]+3*a[k]-3*b[k]+p3[k])*t*t*t)
                vals.append(max(.001,v) if k>1 else v)
            out.append((a[0]*(1-t)+b[0]*t,0,*vals))
    out.append((rows[-1][0],0,*rows[-1][1:]))
    return out

def solid_fin(name,outline,center,thick,mat,col):
    verts=[(x,0,z) for x,z in outline]+[(center[0],-thick,center[1]),(center[0],thick,center[1])]
    n=len(outline); faces=[]
    for i in range(n): faces.extend([(n,i,(i+1)%n),(n+1,(i+1)%n,i)])
    return mesh_object(name,verts,faces,mat,col)

class FeatureMesh:
    def __init__(self): self.v=[]; self.f=[]; self.mi=[]
    def add(self,verts,faces,mi):
        off=len(self.v); self.v+=verts; self.f += [tuple(off+j for j in f) for f in faces]; self.mi += [mi]*len(faces)
    def ellipsoid(self,c,r,mi,ns=20,nr=10):
        v=[(c[0],c[1],c[2]+r[2])]; f=[]
        for k in range(1,nr):
            phi=math.pi*k/nr
            for j in range(ns):
                t=2*math.pi*j/ns; v.append((c[0]+r[0]*math.sin(phi)*math.cos(t),c[1]+r[1]*math.sin(phi)*math.sin(t),c[2]+r[2]*math.cos(phi)))
        bot=len(v); v.append((c[0],c[1],c[2]-r[2]))
        for j in range(ns): f.append((0,1+j,1+(j+1)%ns))
        for k in range(nr-2):
            for j in range(ns):
                a=1+k*ns+j;b=1+k*ns+(j+1)%ns; f.append((a,a+ns,b+ns,b))
        off=1+(nr-2)*ns
        for j in range(ns): f.append((bot,off+(j+1)%ns,off+j))
        self.add(v,f,mi)
    def tube(self,centers,radius,mi):
        v=[];f=[]; n=6
        for i,p in enumerate(centers):
            tangent=Vector(centers[min(i+1,len(centers)-1)])-Vector(centers[max(0,i-1)])
            tangent.normalize(); u=tangent.cross(Vector((0,0,1))).normalized(); w=tangent.cross(u).normalized()
            taper=min(1,(i+1)/2,(len(centers)-i)/2)
            for j in range(n): v.append(tuple(Vector(p)+(u*math.cos(j*2*math.pi/n)+w*math.sin(j*2*math.pi/n))*radius*taper))
        for i in range(len(centers)-1):
            for j in range(n): f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        f.extend([tuple(reversed(range(n))),tuple((len(centers)-1)*n+j for j in range(n))]); self.add(v,f,mi)

def build(out):
    col=setup_scene(P['asset_id'],P['seed']); root=bpy.data.objects[col['asset_root']]
    root['authoring_forward']='+X'; root['glTF_forward']='+X'; root['representation']='living-reconstruction'; root['scale_reference']='Representative 2.56 m estimate for ROM VP47698; photo specimen identity unverified.'
    root['soft_tissue_uncertainty']='Dorsal and caudal margins, skin, width and pigmentation inferred. Weak caudal flexure retained.'
    mats={name:make_material('Leptonectes_'+name,color,roughness=.78 if name not in ['features','iris'] else .4) for name,color in P['palette'].items()}
    body=loft('01_continuous_head_trunk_axial_tail',body_sections(),[mats['dorsal'],mats['flank'],mats['ventral']],col,N)
    for side in [-1,1]:
        fore=[(.36,.09,.258,.090,.027),(.34,.155,.25,.096,.025),(.30,.23,.233,.080,.018),(.255,.31,.215,.059,.012),(.225,.38,.202,.031,.006),(.21,.435,.198,.0025,.0015)]
        hind=[(-.47,.055,.255,.050,.020),(-.49,.105,.245,.057,.017),(-.515,.165,.224,.044,.011),(-.55,.22,.207,.024,.005),(-.57,.26,.199,.002,.0013)]
        for label,seq in [('fore',fore),('hind',hind)]:
            sec=[(x,side*y,z,a,b) for x,y,z,a,b in seq]
            ob=loft(('02_' if label=='fore' else '03_')+label+('_left' if side<0 else '_right'),sec,[mats['flank'],mats['ventral']],col,16,'Y')
            ob['anatomy']='Attached enclosed paddle, no exposed digits; inferred soft margin.'
    solid_fin('04_low_dorsal_inferred',[(.12,.473),(-.03,.525),(-.16,.585),(-.205,.595),(-.20,.55),(-.26,.49),(-.36,.442),(-.47,.415),(-.25,.41),(.08,.43)],(-.14,.483),.017,mats['dorsal'],col)
    solid_fin('05_modest_caudal_membrane_inferred',[(-1.06,.247),(-1.16,.285),(-1.24,.358),(-1.29,.38),(-1.285,.333),(-1.29,.282),(-1.35,.153),(-1.29,.163),(-1.20,.192),(-1.10,.218)],(-1.238,.249),.010,mats['flank'],col)
    marks=FeatureMesh()
    for side in [-1,1]:
        # Eye diameter is 0.055 m, much smaller than the inferred bony orbital region.
        marks.ellipsoid((.606,side*.065,.357),(.0275,.010,.0275),0)
        marks.ellipsoid((.611,side*.074,.358),(.0135,.0035,.0140),1)
        marks.ellipsoid((.612,side*.077,.358),(.0073,.0017,.0085),0)
        zc,ry,rz=profile(.697); zn=.345; yn=ry*math.sqrt(max(.1,1-((zn-zc)/rz)**2))
        marks.ellipsoid((.697,side*(yn+.0009),zn),(.008,.002,.0034),0,16,8)
        centers=[]
        for i in range(36):
            x=.515+(.681*i/35); zc,ry,rz=profile(x); dz=-.014*(1-(x-.515)/.70)-.0007
            y=ry*math.sqrt(max(.1,1-(dz/rz)**2))+.0006
            centers.append((x,side*y,zc+dz))
        marks.tube(centers,.00065,0)
    parts('06_eyes_nares_closed_jaw_seams',marks.v,marks.f,[mats['features'],mats['iris']],marks.mi,col)
    bpy.context.view_layer.update()
    low=min((obj.matrix_world@v.co).z for obj in col.all_objects if obj.type=='MESH' for v in obj.data.vertices)
    for ob in col.all_objects:
        if ob.type=='MESH':
            for v in ob.data.vertices: v.co.z-=low
    root['mounting_origin']='Identity root at x=0,y=0; lowest geometry z=0; free-swimming display, not physical ground contact.'
    bpy.context.view_layer.update(); source=audit_source(col,24000)
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.scene['asset_license']='CC-BY-4.0'; bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.context.preferences.filepaths.save_version=0
    out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects: ob.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}; assert not set(opts)-available
    bpy.ops.export_scene.gltf(**opts)
    report=audit_glb(out/'model.glb',24000,6,16)
    if report['errors']: raise RuntimeError(report['errors'])
    b=source['bounds_blender_m']; delta=max(abs(report['bounds_m'][s][i]-expected[i]) for s,expected in [('min',[b['min'][0],b['min'][2],-b['max'][1]]),('max',[b['max'][0],b['max'][2],-b['min'][1]])] for i in range(3))
    assert delta<.0001 and source['triangles']==report['scene_triangles'] and report['bytes']<=2500000
    report.update({'source':source,'bounds_roundtrip_max_error_m':delta,'source_blend_sha256':sha(out/'model.blend'),'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'mount_shift_z':-low,'blender_version':bpy.app.version_string,'exporter_version':'4.3.47','export_options':{k:v for k,v in opts.items() if k!='filepath'},'status_scope':'Source and static GLB technical checks only; no visual, factual, GPU or scene approval.'})
    write(out/'qa/evidence/geometry.json',report)
    return col

def render(out,gray=False):
    if gray:
        col=bpy.data.collections['EXPORT']; dst=out/'private/gray-v1'
    else:
        bpy.ops.wm.read_factory_settings(use_empty=True); col=bpy.data.collections.new('EXACT_GLB_IMPORT'); bpy.context.scene.collection.children.link(col)
        bpy.ops.import_scene.gltf(filepath=str(out/'model.glb'))
        for ob in list(bpy.context.scene.objects):
            for old in list(ob.users_collection): old.objects.unlink(ob)
            col.objects.link(ob)
        dst=out/'views'
    dst.mkdir(parents=True,exist_ok=True)
    points=_vertices_world(col); low,high=_bounds(points); center=Vector([(a+b)/2 for a,b in zip(low,high)]); span=max(b-a for a,b in zip(low,high))
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=P['render']['gray_samples' if gray else 'samples']; scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=P['render']['gray_resolution' if gray else 'resolution']; scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Studio'); world.use_nodes=True; nodes=world.node_tree.nodes;links=world.node_tree.links
    bg=nodes['Background'];bg.inputs['Color'].default_value=(.75,.75,.75,1);bg.inputs['Strength'].default_value=.3
    cb=nodes.new('ShaderNodeBackground');cb.inputs['Color'].default_value=tuple(srgb_to_linear(v/255) for v in (232,228,220))+(1,);cb.inputs['Strength'].default_value=1
    lp=nodes.new('ShaderNodeLightPath');mx=nodes.new('ShaderNodeMixShader');links.new(lp.outputs['Is Camera Ray'],mx.inputs[0]);links.new(bg.outputs[0],mx.inputs[1]);links.new(cb.outputs[0],mx.inputs[2]);links.new(mx.outputs[0],nodes['World Output'].inputs[0]);scene.world=world
    lighting=[]
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        data=bpy.data.lights.new(name,'AREA');data.energy=energy*span*span/4;data.shape='DISK';data.size=size*span/2
        ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob);ob.location=center+Vector(direction)*span/2;_look_at(ob,center);lighting.append({'name':name,'direction':direction,'energy':data.energy,'size':data.size})
    camdata=bpy.data.cameras.new('inspection');cam=bpy.data.objects.new('inspection',camdata);scene.collection.objects.link(cam);scene.camera=cam;camdata.type='ORTHO';camdata.clip_start=.001;camdata.clip_end=100
    if gray: bpy.context.view_layer.material_override=make_material('Clay','#929292')
    frames=[]
    for name,direction in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        cam.location=center+Vector(direction).normalized()*span*4;_look_at(cam,center);bpy.context.view_layer.update();inv=cam.matrix_world.inverted();proj=[inv@p for p in points]
        xmin=min(p.x for p in proj);xmax=max(p.x for p in proj);ymin=min(p.y for p in proj);ymax=max(p.y for p in proj)
        cam.location+=cam.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));camdata.ortho_scale=max(xmax-xmin,ymax-ymin)*1.16
        scene.render.filepath=str(dst/(name+'.png'));start=time.monotonic();bpy.ops.render.render(write_still=True)
        frames.append({'path':(dst/(name+'.png')).relative_to(out).as_posix(),'sha256':sha(dst/(name+'.png')),'camera_direction_blender':direction,'camera_position_blender_m':list(cam.location),'camera_rotation_radians':list(cam.rotation_euler),'orthographic_scale':camdata.ortho_scale,'wall_seconds':round(time.monotonic()-start,3)})
    if not gray: shutil.copyfile(dst/'perspective.png',out/'preview.png')
    report={'scope':'Source-scene gray diagnostics, not final export proof.' if gray else 'Four clean-import exact model.glb renders; perspective bytes reused as preview. Not GPU evidence.','source_glb_sha256':sha(out/'model.glb'),'source_blend_sha256':sha(out/'model.blend'),'generator_sha256':sha(__file__),'renderer':'Blender '+bpy.app.version_string+' Cycles CPU','threads':2,'samples':scene.cycles.samples,'resolution':scene.render.resolution_x,'denoising':False,'color_management':{'view_transform':'Standard','look':'None','exposure':0,'gamma':1},'background_srgb':'#E8E4DC','lighting':lighting,'frames':frames,'preview_equals_perspective':not gray,'created_at':datetime.now(timezone.utc).isoformat(),'visual_review':'pending'}
    write(out/('private/gray-v1/render-manifest.json' if gray else 'qa/evidence/render.json'),report)

def main():
    a=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE.parent);parser.add_argument('--mode',choices=['build','gray','final'],default='build');args=parser.parse_args(a);out=args.output.resolve()
    if args.mode!='final': build(out)
    if args.mode in ['gray','final']: render(out,args.mode=='gray')
if __name__=='__main__':main()
