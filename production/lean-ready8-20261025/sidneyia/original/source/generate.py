# SPDX-License-Identifier: MIT
"""Original Sidneyia inexpectans. Deliberate shell lofts, complete paired appendages.
Rebuild: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
Only bundled Python dependencies; no imported model or image data.
"""
from pathlib import Path
import sys,json,hashlib,argparse,math
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
P={};C=None;M={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,d):Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def mesh(name,vs,fs,mat,**props):
    o=mesh_object(name,[(x*.001,y*.001,z*.001) for x,y,z in vs],fs,mat,C)
    for k,v in props.items():o[k]=v
    return o

def tube(name,points,radii,mat,sides=6,**props):
    pts=[Vector(p) for p in points];vs=[];fs=[]
    for i,p in enumerate(pts):
        axis=(pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)]).normalized()
        ref=Vector((0,0,1)) if abs(axis.z)<.9 else Vector((0,1,0))
        u=axis.cross(ref).normalized();v=axis.cross(u).normalized()
        for j in range(sides):vs.append(tuple(p+radii[i]*(math.cos(j*2*math.pi/sides)*u+math.sin(j*2*math.pi/sides)*v)))
    fs.append(tuple(range(sides-1,-1,-1)))
    for i in range(len(pts)-1):
        for j in range(sides):fs.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    fs.append(tuple((len(pts)-1)*sides+j for j in range(sides)))
    return mesh(name,vs,fs,mat,**props)

def loft(name,rows,mat,n=16,**props):
    vs=[];fs=[]
    for y,w,lo,hi in rows:
        for j in range(n):
            t=j*2*math.pi/n;vs.append((w*math.cos(t),y,(lo+hi)/2+(hi-lo)/2*math.sin(t)))
    fs=[tuple(range(n-1,-1,-1))]
    for k in range(len(rows)-1):
        for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    fs.append(tuple((len(rows)-1)*n+j for j in range(n)))
    return mesh(name,vs,fs,mat,**props)

def shield(name,outline,center,crown,edge,thickness,mat):
    # Closed curved shield from a star-visible notched outline; real vaulted underside.
    n=len(outline);vs=[];fs=[]
    for bottom in [False,True]:
        vs.append((center[0],center[1],crown-(thickness if bottom else 0)))
        for t in [.42,.76,1.]:
            for x,y in outline:
                # Head's posterior edge keeps the transverse vault, unlike its rounded front.
                edge_here=edge
                if name=='cephalic-shield':edge_here+=(crown-edge-.4)*max(0,1-abs(x)/25)**.9*max(0,min(1,(y+30)/2))
                vs.append((center[0]+(x-center[0])*t,center[1]+(y-center[1])*t,edge_here+(crown-edge_here)*(1-t**1.8)-(thickness if bottom else 0)))
    half=1+3*n
    for b in [0,half]:
        for j in range(n):fs.append((b,b+1+j,b+1+(j+1)%n))
        for k in range(2):
            for j in range(n):a=b+1+k*n+j;d=b+1+k*n+(j+1)%n;fs.append((a,d,d+n,a+n))
    for j in range(n):a=1+2*n+j;b=1+2*n+(j+1)%n;fs.append((a,b,b+half,a+half))
    return mesh(name,vs,fs,mat,anatomical_role='short broad notched cephalic shield')

def tergite(i,y,w,crown):
    ts=[-1,-.94,-.77,-.48,0,.48,.77,.94,1];vs=[];fs=[];n=len(ts);th=P['anatomy']['shell_thickness_mm']
    for bottom in [False,True]:
        for r in [0,.28,1.]:
            for t in ts:
                sweep=3.1*abs(t)**1.7
                yy=y+7.8*r+sweep
                width=w*(1-.025*r)
                edge=9.0-0.14*i
                zz=edge+(crown-edge)*(1-abs(t)**1.7)+(-1.0+1.2*r)-(th if bottom else 0)
                vs.append((width*t,yy,zz))
    half=3*n
    for b in [0,half]:
        for row in range(2):
            for j in range(n-1):a=b+row*n+j;fs.append((a,a+1,a+n+1,a+n))
    boundary=list(range(n))+[2*n-1,3*n-1]+list(range(3*n-2,2*n-1,-1))+[n]
    for j,a in enumerate(boundary):b=boundary[(j+1)%len(boundary)];fs.append((a,b,b+half,a+half))
    o=mesh('tergite-%02d'%(i+1),vs,fs,[M['shell'],M['shell_rim']],anatomical_role='overlapping trunk tergite',tergite_index=i+1)
    for p in o.data.polygons:
        if p.index>=4*(n-1) or p.normal.z<0:p.material_index=1
    return o

def blade(name,outline,center,thickness,mat,**props):
    # Closed physical foil, cambered at its center, thin but not a single plane.
    n=len(outline);vs=[];fs=[]
    for sign in [-1,1]:
        vs.append((center[0],center[1],center[2]+sign*thickness))
        for x,y,z in outline:vs.append((x,y,z+sign*thickness*.24))
    for off in [0,n+1]:
        for j in range(n):fs.append((off,off+1+j,off+1+(j+1)%n))
    for j in range(n):fs.append((1+j,1+(j+1)%n,n+2+(j+1)%n,n+2+j))
    return mesh(name,vs,fs,mat,**props)

def eye(name,c,rs,mat,n=10,m=6):
    vs=[(c[0],c[1],c[2]-rs[2])];fs=[]
    for k in range(1,m):
        a=-math.pi/2+k*math.pi/m
        for j in range(n):t=j*2*math.pi/n;vs.append((c[0]+rs[0]*math.cos(a)*math.cos(t),c[1]+rs[1]*math.cos(a)*math.sin(t),c[2]+rs[2]*math.sin(a)))
    end=len(vs);vs.append((c[0],c[1],c[2]+rs[2]))
    for j in range(n):fs.append((0,1+j,1+(j+1)%n))
    for k in range(m-2):
        for j in range(n):a=1+k*n+j;b=1+k*n+(j+1)%n;fs.append((a,b,b+n,a+n))
    for j in range(n):fs.append((end,end-n+j,end-n+(j+1)%n))
    return mesh(name,vs,fs,mat,anatomical_role='stalked eye')

def limb(s,i,y,w,head=False):
    side='L' if s<0 else 'R';kind='cephalic' if head else 'trunk';prefix='%s-%02d-%s'%(kind,i+1,side)
    role={'appendage_group':kind,'pair_index':i+1,'side':side}
    # Robust coxa enters the ventral body, then branches into leg and lamellae.
    tube(prefix+'-gnathobase',[(s*3.5,y,9),(s*7,y+.2,8.0),(s*11.5,y+.6,7.5)],[1.9,2.15,1.8],M['ventral'],8,**role)
    for q in range(2):
        tube(prefix+'-gnathobasic-tooth-%d'%(q+1),[(s*4.2,y-.7+q*1.5,7.3),(s*2.45,y-.6+q*1.5,6.1)],[.65,.18],M['claw'],5,**role)
    extent=w+(.8 if head else 1.4); knee=w*.82
    path=[(s*10.6,y+.5,7.5),(s*15.0,y+.9,6.8),(s*knee,y+1.7,5.4),(s*extent,y+3.0,1.6),(s*(extent-.4),y+3.8,.65)]
    tube(prefix+'-walking-branch',path,[1.6,1.3,.95,.66,.43],M['limb'],6,**role)
    # Segment collars emphasize articulation rather than implying fossil-exact podomeres.
    for j in [1,2]:
        p=Vector(path[j]);d=(Vector(path[j+1])-Vector(path[j-1])).normalized()
        tube(prefix+'-joint-%d'%j,[p-d*.38,p+d*.38],[1.36 if j==1 else 1.03]*2,M['ventral'],6,**role)
    tube(prefix+'-terminal-claw',[path[-1],(s*(extent-1.1),y+4.5,.18),(s*(extent-2.0),y+4.8,.4)],[.45,.27,.10],M['claw'],6,**role)
    if not head:
        tube(prefix+'-exopod-axis',[(s*10.5,y,8.3),(s*(w*.86),y+4.7,7.3)],[1.1,.55],M['limb'],6,**role)
        for j in range(3):
            yy=y+j*1.7
            outline=[(s*10.5,yy,8.1),(s*(w*.68),yy-1,8.4),(s*(w*.94),yy+.4,7.9),(s*(w*.99),yy+2.7,6.6),(s*(w*.79),yy+4.2,6.5),(s*11.5,yy+2.3,7.5)]
            blade(prefix+'-gill-blade-%d'%(j+1),outline,(s*(w*.7),yy+1.5,7.9),.28,M['gill'],**role)

def under_shell_body():
    # The original ventral mass follows the actual inner carapace, rather than a
    # generic ellipsoid protruding through plates or disconnected hidden supports.
    shells=[o for o in C.all_objects if o.name=='cephalic-shield' or o.name.startswith('tergite-')]
    widths=[(-42,5),(-38,10),(-34,14),(-29,16),(-23,19),(-17,20),(-8,20),(0,19),(8,17),(16,13),(23,9),(26.5,6)]
    ys=sorted(set([y for y,w in widths]+[-41+i*1.5 for i in range(46) if -41+i*1.5<26.5]))
    ts=[-1,-.78,-.42,0,.42,.78,1];vs=[];fs=[];n=14
    for y in ys:
        for k in range(len(widths)-1):
            if widths[k][0]<=y<=widths[k+1][0]:
                t=(y-widths[k][0])/(widths[k+1][0]-widths[k][0]);w=widths[k][1]*(1-t)+widths[k+1][1]*t;break
        for t in ts:
            x=w*t;hits=[]
            for ob in shells:
                ok,p,normal,idx=ob.ray_cast(Vector((x*.001,y*.001,0)),Vector((0,0,1)))
                if ok:hits.append(p.z*1000)
            if not hits:raise RuntimeError('No shell above ventral roof '+str((x,y)))
            vs.append((x,y,min(hits)+.10))
        for t in reversed(ts):vs.append((w*t,y,7.2+.9*abs(t)))
    start_center=len(vs);vs.append(tuple(sum(p[k] for p in vs[:n])/n for k in range(3)))
    end_center=len(vs);vs.append(tuple(sum(p[k] for p in vs[(len(ys)-1)*n:len(ys)*n])/n for k in range(3)))
    for j in range(n):fs.append((start_center,j,(j+1)%n))
    for k in range(len(ys)-1):
        for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
    for j in range(n):fs.append((end_center,(len(ys)-1)*n+j,(len(ys)-1)*n+(j+1)%n))
    return mesh('ventral-body',vs,fs,M['ventral'],anatomical_role='continuous under-carapace body and limb attachment volume')

def build():
    global C,M
    C=setup_scene('sidneyia',P['seed']);M={k:make_material(k,v,roughness=.86 if k!='eye' else .48) for k,v in P['surface']['palette_srgb'].items()}
    right=[(0,-45),(10,-44.4),(18,-41.6),(23,-37.8),(24.6,-34.8),(24.2,-33),(20.6,-33),(20.6,-30.3),(24.5,-29.5),(25,-26.0),(13,-27),(0,-28)]
    outline=right+[(-x,y) for x,y in right[-2:0:-1]]
    shield('cephalic-shield',outline,(0,-35.5),18.7,10.0,.8,M['shell'])
    a=P['anatomy']
    for i,(y,w,z) in enumerate(zip(a['trunk_front_y_mm'],a['trunk_half_width_mm'],a['trunk_crown_z_mm'])):tergite(i,y,w,z)
    under_shell_body()
    # Two explicitly selected limbless abdominal sclerites, not a trilobite pygidium.
    loft('abdominal-ring-01',[(25,7.6,7.9,13.7),(27,7.9,7.8,13.8),(32.8,6.7,8.1,12.4)],M['shell'],14,anatomical_role='limbless abdominal sclerite',abdominal_index=1)
    loft('abdominal-ring-02',[(31.5,6.6,8.2,12.1),(33,6.8,8.1,12.3),(40.6,5.3,8.6,10.8)],M['shell'],14,anatomical_role='limbless abdominal sclerite',abdominal_index=2)
    blade('central-telson',[(0,39.0,10.4),(4.4,40.7,10),(4.1,44.5,9.7),(0,55,8.8),(-4.1,44.5,9.7),(-4.4,40.7,10)],(0,44.2,10.6),.5,M['shell'],anatomical_role='triangular central telson')
    for s in [-1,1]:
        blade('tail-flap-'+('L' if s<0 else 'R'),[(s*3.0,38.8,9.8),(s*7.0,40.2,9.5),(s*12,45.1,8.7),(s*13.3,50,8.2),(s*10.1,52,8.3),(s*5.5,49,8.9),(s*3.5,43,9.5)],(s*7.5,45.1,9.9),.45,M['shell'],anatomical_role='lateral tail flap with attached root')
        tube('eye-stalk-'+str(s),[(s*19.5,-31.8,10.8),(s*23,-32,12.1),(s*25.1,-32.6,12.8)],[1.0,.82,.65],M['ventral'],8)
        eye('eye-'+str(s),(s*25.3,-32.9,13.1),(1.6,1.9,1.65),M['eye'])
        # Slender clearly segmented antennae, forward and outward from head notches.
        points=[]
        for j in range(a['antenna_segments']+1):
            t=j/a['antenna_segments'];points.append((s*(19.7+13.1*(1-(1-t)**1.6)),-32.7-31.8*t,10.7+3.3*t+1.3*math.sin(t*math.pi)))
        for j in range(len(points)-1):
            radius=.72*(1-j/a['antenna_segments'])+.12
            tube('antenna-%s-segment-%02d'%('L' if s<0 else 'R',j+1),[points[j],points[j+1]],[radius,radius*.82],M['limb'],6,anatomical_role='segmented antenna',side='L' if s<0 else 'R',segment=j+1)
        for i,y in enumerate(a['cephalic_limb_root_y_mm']):limb(s,i,y,20.3+i*.6,True)
        for i,(y,w) in enumerate(zip(a['trunk_front_y_mm'],a['trunk_half_width_mm'])):limb(s,i,y+3.7,w,False)
    # Modest under-head hypostome and mouth; no internal digestive anatomy.
    shield('hypostome',[(-3.4,-40.2),(3.4,-40.2),(4,-37),(2.6,-34.8),(-2.6,-34.8),(-4,-37)],(0,-37.8),7.8,7.3,.5,M['ventral'])
    tube('mouth-region',[(0,-35.5,7.2),(0,-34.8,7.2)],[1.3,1.1],M['claw'],8)
    # Exact physical conversion already happened in mesh(). Center intended foot contact footprint.
    claws=[o for o in C.all_objects if o.type=='MESH' and o.name.endswith('terminal-claw')]
    feet=[v.co for o in claws for v in o.data.vertices]
    cy=(min(p.y for p in feet)+max(p.y for p in feet))/2;ground=min(p.z for p in feet)
    for o in C.all_objects:
        if o.type=='MESH':
            for v in o.data.vertices:v.co.y-=cy;v.co.z-=ground
    C['construction_to_origin_offset_m']=[0,-cy,-ground];bpy.context.view_layer.update()
    return C

def consolidate_for_export(col):
    # Preserve editable source in .blend, then group in-memory export by material.
    meshes=[o for o in col.all_objects if o.type=='MESH'];buffers={};mapping={}
    for o in meshes:
        for matidx,mat in enumerate(o.data.materials):
            faces=[p for p in o.data.polygons if p.material_index==matidx]
            if not faces:continue
            bucket=buffers.setdefault(mat.name,{'vs':[],'fs':[],'parts':[],'mat':mat})
            used=sorted({i for f in faces for i in f.vertices});base=len(bucket['vs']);imap={old:base+j for j,old in enumerate(used)}
            bucket['vs'].extend(tuple(o.matrix_world@o.data.vertices[j].co) for j in used)
            bucket['fs'].extend(tuple(imap[i] for i in f.vertices) for f in faces)
            bucket['parts'].append({'source_object':o.name,'vertex_start':base,'vertex_count':len(used),'properties':dict(o.items())})
    for o in meshes:col.objects.unlink(o)
    for name,b in buffers.items():
        ob=mesh_object('surface-'+name,b['vs'],b['fs'],b['mat'],col);ob['semantic_source_parts']=json.dumps(b['parts'],sort_keys=True,separators=(',',':'));mapping[ob.name]=b['parts']
    return mapping

def main():
    global P
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);a=ap.parse_args(sys.argv[sys.argv.index('--')+1:]);out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    P=json.loads((HERE/'params.json').read_text());col=build();policy=P['geometry_policy']
    source=audit_source(col,policy['max_triangles']);source['authored_vertices']=sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH');source['evaluated_vertices']=source['authored_vertices']
    if source['errors']:raise RuntimeError(source['errors'])
    bodyvs=[v.co for o in col.all_objects if o.type=='MESH' and not o.name.startswith('antenna-') for v in o.data.vertices]
    bodybounds={'min':[min(p[i] for p in bodyvs) for i in range(3)],'max':[max(p[i] for p in bodyvs) for i in range(3)]};bodybounds['size']=[bodybounds['max'][i]-bodybounds['min'][i] for i in range(3)]
    if abs(bodybounds['size'][1]-.1)>1e-6:raise RuntimeError('100 mm body length not maintained')
    bpy.context.scene.render.filepath='//';bpy.context.scene['generator']='source/generate.py';bpy.context.scene['scientific_scope']=P['interpretation'];bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'//';space.params.filename=''
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    semantic_map=consolidate_for_export(col)
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(flags)-available:raise RuntimeError('Missing glTF exporter options')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',policy['max_triangles'],policy['max_materials'],policy['max_primitives']);glb['file']='model.glb'
    b=source['bounds_blender_m'];emin=[b['min'][0],b['min'][2],-b['max'][1]];emax=[b['max'][0],b['max'][2],-b['min'][1]]
    delta=max(abs(glb['bounds_m'][s][i]-e[i]) for s,e in [('min',emin),('max',emax)] for i in range(3))
    if glb['errors'] or delta>1e-6 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>policy['max_glb_bytes']:raise RuntimeError('Source/export audit failed: '+str(glb['errors']))
    import io_scene_gltf2
    dump(out/'technical.json',{'asset_id':'sidneyia','revision':'r001','source':source,'glb':glb,'body_excluding_antennae_bounds_blender_m':bodybounds,'source_export_bounds_delta_m':delta,'blender_version':bpy.app.version_string,'exporter_version':io_scene_gltf2.bl_info['version'],'consumer_three_version':'0.180.0','consumer_scope':'version pin only until separate CPU parser test; GPU not tested','export_options':flags,'source_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'blend_sha256':sha(out/'model.blend'),'construction_to_origin_offset_m':list(col['construction_to_origin_offset_m']),'anatomical_scope':P['interpretation'],'anatomical_counts':{'tergites':9,'cephalic_limb_pairs':3,'trunk_limb_pairs':9,'abdominal_rings':2,'antennae':2,'stalked_eyes':2,'central_telson':1,'lateral_tail_flaps':2},'semantic_export_groups':{k:len(v) for k,v in semantic_map.items()},'semantic_parts':'Editable named meshes in source. Material-grouped export retains source-object vertex ranges and anatomical properties in node extras. No borrowed source geometry.'})
    dump(out/'semantic-export-map.json',{'glb_sha256':sha(out/'model.glb'),'groups':semantic_map,'range_scope':'Pre-export Blender vertex ranges. Export normals split vertices; use source_object names and positions for correspondence, not direct glTF vertex indexing.'})
if __name__=='__main__':main()
