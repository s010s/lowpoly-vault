# SPDX-License-Identifier: MIT
"""Original Cyamodus hildegardis reconstruction. Run with Blender and --output DIR.
All run-time source dependencies are relative to this file. No external model is read.
"""
import argparse, hashlib, json, math, random, sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

class Geo:
    def __init__(self): self.v=[]; self.f=[]; self.mi=[]
    def add(self,v,f,mat=0):
        start=len(self.v); self.v.extend(v); self.f.extend(tuple(start+i for i in p) for p in f); self.mi.extend([mat]*len(f))
    def make(self,name,mats,col):
        o=mesh_object(name,self.v,self.f,mats,col)
        for p,i in zip(o.data.polygons,self.mi): p.material_index=i
        return o

def loft(g,rows,n=12,mat=0):
    # Each row is x, y-center, z-center, lateral radius, vertical radius.
    v=[]; f=[]
    for x,y,z,w,h in rows:
        for i in range(n):
            a=2*math.pi*i/n; v.append((x,y+w*math.cos(a),z+h*math.sin(a)))
    for k in range(len(rows)-1):
        for i in range(n):
            j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
    f.extend([tuple(range(n-1,-1,-1)),tuple((len(rows)-1)*n+i for i in range(n))]);g.add(v,f,mat)

def tube(g,points,radii,n=10,mat=0,flatten=1):
    v=[];f=[]
    for k,p in enumerate(points):
        c=Vector(p); tang=Vector(points[min(k+1,len(points)-1)])-Vector(points[max(0,k-1)])
        tang.normalize(); u=tang.cross(Vector((0,0,1))).normalized(); z=u.cross(tang).normalized()
        for i in range(n):
            a=2*math.pi*i/n;v.append(tuple(c+radii[k]*(math.cos(a)*u+flatten*math.sin(a)*z)))
    for k in range(len(points)-1):
        for i in range(n): j=(i+1)%n;f.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
    f.extend([tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+i for i in range(n))]);g.add(v,f,mat)

def ellipsoid(g,c,scale,n=12,rings=6,mat=0):
    v=[(c[0],c[1],c[2]-scale[2])];f=[]
    for j in range(1,rings):
        a=-math.pi/2+math.pi*j/rings
        for i in range(n):
            b=2*math.pi*i/n;v.append((c[0]+scale[0]*math.cos(a)*math.cos(b),c[1]+scale[1]*math.cos(a)*math.sin(b),c[2]+scale[2]*math.sin(a)))
    end=len(v);v.append((c[0],c[1],c[2]+scale[2]))
    for i in range(n):f.append((0,1+(i+1)%n,1+i))
    for j in range(rings-2):
        for i in range(n):k=1+j*n; q=(i+1)%n;f.append((k+i,k+q,k+n+q,k+n+i))
    for i in range(n):f.append((end,1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n))
    g.add(v,f,mat)

def convex_clip(poly,a,b,c):
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        dp=a*p[0]+b*p[1]-c;dq=a*q[0]+b*q[1]-c
        if dp<=1e-10:out.append(p)
        if (dp<=0)!=(dq<=0):
            t=dp/(dp-dq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
    return out

def plate(g,poly,zfunc,height=.003,mat=0):
    # A closed low bevel cap; seams are narrow original design, not fossil sutures.
    cx=sum(p[0] for p in poly)/len(poly);cy=sum(p[1] for p in poly)/len(poly);n=len(poly)
    p=[(cx+(x-cx)*.97,cy+(y-cy)*.97) for x,y in poly]
    v=[(x,y,zfunc(x,y)-.001) for x,y in p]
    v += [(cx+(x-cx)*.83,cy+(y-cy)*.83,zfunc(x,y)+height) for x,y in p]
    v.append((cx,cy,zfunc(cx,cy)+height+.0005))
    f=[tuple(range(n-1,-1,-1))]
    for i in range(n):j=(i+1)%n;f.extend([(i,j,n+j,n+i),(2*n,n+i,n+j)])
    g.add(v,f,mat)

def shield(g,cx,rx,ry,zrim,height,rng,spacing,power=2.0):
    n=48; v=[]; f=[]
    zfun=lambda x,y:zrim+height*max(0,1-abs((x-cx)/rx)**power-abs(y/ry)**power)**.65
    oval=lambda t:(math.copysign(abs(math.cos(t))**(2/power),math.cos(t)),math.copysign(abs(math.sin(t))**(2/power),math.sin(t)))
    for r in (1,.75,.4):
        for i in range(n):
            t=2*math.pi*i/n;u,w=oval(t);x=cx+rx*r*u;y=ry*r*w;v.append((x,y,zfun(x,y)))
    v.append((cx,0,zrim+height));center=len(v)-1
    for j in range(2):
        for i in range(n):k=(i+1)%n;f.append((j*n+i,j*n+k,(j+1)*n+k,(j+1)*n+i))
    for i in range(n):f.append((center,2*n+i,2*n+(i+1)%n))
    bottom=len(v)
    for i in range(n):x,y,z=v[i];v.append((x,y,z-.006))
    for i in range(n):j=(i+1)%n;f.append((i,bottom+i,bottom+j,j))
    f.append(tuple(bottom+i for i in reversed(range(n))));g.add(v,f)
    domain=[(cx+rx*.985*oval(2*math.pi*i/n)[0],ry*.985*oval(2*math.pi*i/n)[1]) for i in range(n)]
    seeds=[]
    for j in range(-int(ry/spacing)-1,int(ry/spacing)+2):
        for i in range(-int(rx/spacing)-1,int(rx/spacing)+2):
            x=(i+.45*(j%2)+rng.uniform(-.22,.22))*spacing;y=(j+rng.uniform(-.22,.22))*spacing
            if abs(x/rx)**power+abs(y/ry)**power<.96:seeds.append((cx+x,y))
    for a in seeds:
        poly=domain[:]
        for b in seeds:
            if a==b:continue
            poly=convex_clip(poly,b[0]-a[0],b[1]-a[1],(b[0]*b[0]+b[1]*b[1]-a[0]*a[0]-a[1]*a[1])/2)
            if len(poly)<3:break
        if len(poly)>=3:plate(g,poly,zfun,.0019+rng.random()*.0014)
    return zfun

def rimplates(g,cx,rx,ry,zrim,num,extension,taper=False,power=2.0):
    # Separate similarly sized lateral osteoderms, not enlarged horns.
    for sign in (-1,1):
        for j in range(num):
            a=math.radians(25+130*j/(num-1));x=cx+rx*math.copysign(abs(math.cos(a))**(2/power),math.cos(a));y=sign*ry*abs(math.sin(a))**(2/power)
            outward=Vector((.3*math.cos(a),sign*math.sin(a))).normalized(); tangent=Vector((-outward.y,outward.x))
            size=extension*(.55+.45*(1-j/(num-1))) if taper else extension
            center=Vector((x,y)); poly=[]
            for ox,oy in [(-.010,-.006),(.003,-.011),(size,0),(.003,.011),(-.010,.006)]:
                p=center+ox*outward+oy*tangent;poly.append(tuple(p))
            plate(g,poly,lambda x,y:zrim+.001,.004)

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=HERE.parent); args=a.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'qa/evidence').mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text());rng=random.Random(p['seed']);col=setup_scene('cyamodus',p['seed']);root=bpy.data.objects['cyamodus'];root['authoring_forward']='+X';root['anatomy_scope']='Whole C. hildegardis, bounded soft-tissue reconstruction'
    mats={k:make_material('cyamodus_'+k,v,.86 if k!='eye' else .32) for k,v in p['skin_palette'].items()}
    g=Geo();loft(g,[(-.19,0,.043,.026,.013),(-.16,0,.041,.057,.014),(-.10,0,.043,.065,.014),(-.055,0,.044,.079,.016),(.015,0,.044,.087,.019),(.085,0,.046,.080,.017),(.13,0,.051,.046,.013),(.151,0,.064,.038,.021),(.173,0,.065,.039,.021)],16)
    # Soft ventral tones, no ventral armor or plastron.
    for i,face in enumerate(g.f):
        if sum(g.v[k][2] for k in face)/len(face)<.043:g.mi[i]=1
    g.make('soft_body_and_short_neck',[mats['skin'],mats['ventral']],col)
    g=Geo();loft(g,[(.149,0,.068,.042,.021),(.163,0,.069,.064,.023),(.181,0,.070,.070,.023),(.205,0,.070,.060,.023),(.229,0,.067,.046,.0205),(.254,0,.064,.032,.018),(.278,0,.062,.023,.015),(.2925,0,.061,.014,.011)],16);g.make('broad_short_triangular_head',mats['skin'],col)
    # Tail is a continuous taper beneath four diminishing armor rows.
    def tailpos(t):return Vector((-.1735-.262*t,.008*math.sin(math.pi*t),.054-.035*t))
    def tailrad(t):return .025*(1-t)**1.15+.0012
    g=Geo();rows=[]
    for i in range(21):
        t=i/20;c=tailpos(t);r=tailrad(t);rows.append((c.x,c.y,c.z,r,r*.62))
    loft(g,rows,12);g.make('tapered_tail_soft_tissue',mats['skin'],col)
    for fore in (True,False):
        for s in (-1,1):
            g=Geo()
            if fore: pts=[(.087,s*.067,.054),(.077,s*.102,.041),(.055,s*.123,.024),(.040,s*.140,.012)];r=[.022,.017,.014,.017]
            else:pts=[(-.121,s*.044,.049),(-.145,s*.080,.034),(-.174,s*.100,.021),(-.187,s*.116,.012)];r=[.023,.020,.015,.017]
            tube(g,pts,r,n=12,flatten=.65)
            cx,cy,cz=pts[-1]
            ellipsoid(g,(cx,cy,cz),(.024,.020,.011),12,6)
            for d in range(5):
                dx=(d-2)*.0083; length=.017+.005*(1-abs(d-2)/2)
                start=(cx+dx,cy+s*.010,.010)
                end=(cx+dx*1.22,cy+s*(.010+length),.0052)
                tube(g,[start,((start[0]+end[0])*.5,(start[1]+end[1])*.5,.007),end],[.0048,.0041,.0018],8,flatten=.80)
            o=g.make(('fore' if fore else 'hind')+('_left' if s==1 else '_right')+'_inferred_five_short_digits',mats['skin'],col);o['inference']='Feet unknown in C. hildegardis. Five short tips are conservative reconstruction, not fossil phalanges.'
    g=Geo();shield(g,.035,.1025,.097,.066,.029,rng,.027,2.7);g.make('separate_main_dorsal_shield',mats['armor'],col)
    g=Geo();shield(g,-.1255,.05,.066,.059,.023,rng,.025,4.0);g.make('separate_pelvic_dorsal_shield',mats['armor'],col)
    g=Geo();rimplates(g,.035,.088,.096,.065,10,.0115,power=2.7);rimplates(g,-.1255,.043,.065,.060,5,.0095,True,power=4.0);g.make('modest_lateral_shield_osteoderms',mats['rim'],col)
    g=Geo()
    for j in range(21):
        t=.025+j*.045;c=tailpos(t);r=tailrad(t);length=.013*(1-t)+.0035
        for row in ('dorsal','ventral','left','right'):
            if row in ('dorsal','ventral'):
                s=1 if row=='dorsal' else -1;z=c.z+s*r*.63
                poly=[(c.x+length*.55,c.y-r*.38),(c.x-length*.55,c.y-r*.31),(c.x-length*.62,c.y+r*.31),(c.x+length*.55,c.y+r*.38)]
                if s==1:plate(g,poly,lambda x,y,z=z:z,.002*(1-t)+.0006)
                else:
                    h=Geo();plate(h,poly,lambda x,y,z=z:-z,.0014*(1-t)+.0005)
                    g.add([(x,y,-z) for x,y,z in h.v],[tuple(reversed(f)) for f in h.f])
            else:
                s=1 if row=='left' else -1;y=c.y+s*r*.94
                poly=[(c.x+length*.45,y-s*.004*(1-t)),(c.x-length*.55,y-s*.004*(1-t)),(c.x-length*.65,y+s*.007*(1-t)),(c.x+length*.15,y+s*.010*(1-t))]
                plate(g,poly,lambda x,y,z=c.z:z,.003*(1-t)+.0005)
    o=g.make('four_diminishing_tail_armor_rows',mats['rim'],col);o['rows']='dorsal, ventral, left, right';o['row_count']=4
    g=Geo()
    for s in (-1,1):
        ellipsoid(g,(.252,s*.028,.075),(.0080,.0056,.0065),12,6,0)
        ellipsoid(g,(.253,s*.031,.077),(.0048,.0033,.0045),12,6,1)
        ellipsoid(g,(.281,s*.014,.071),(.003,.002,.0012),10,4,0)
        # Very shallow closed-mouth crease in fleshed-over head, no visible dentition.
        tube(g,[(.290,s*.014,.057),(.277,s*.024,.0555),(.254,s*.033,.0535),(.230,s*.045,.0525),(.208,s*.056,.0525)],[.0008]*5,6,0)
    g.make('small_eyes_nostrils_closed_mouth',[mats['dark'],mats['eye']],col)
    for obj in col.all_objects:
        if obj.type=='MESH':
            for vertex in obj.data.vertices:
                vertex.co.x+=.0735
                vertex.co.z-=.001
    bpy.context.view_layer.update();source=audit_source(col,max_triangles=24000)
    if source['errors']:raise RuntimeError(source['errors'])
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.context.preferences.filepaths.save_version=0
    bpy.context.scene.render.filepath=' '*1023
    bpy.context.scene.render.filepath='//'
    # Clear factory file-browser directories before the editable source is saved.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b' '*1023
                    space.params.directory=b'//'
                    space.params.filename='model.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),compress=True)
    for o in bpy.context.selected_objects:o.select_set(False)
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    propkeys=set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys())
    if set(opts)-propkeys:raise RuntimeError('Missing exporter options: '+str(set(opts)-propkeys))
    bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb(out/'model.glb',24000,6,16)
    glb['file']='model.glb'
    if glb['errors']:raise RuntimeError(glb['errors'])
    if glb['bytes']>2500000:raise RuntimeError('Byte budget exceeded')
    lo=source['bounds_blender_m']['min'];hi=source['bounds_blender_m']['max'];expected_min=[lo[0],lo[2],-hi[1]];expected_max=[hi[0],hi[2],-lo[1]]
    delta=max(abs(glb['bounds_m'][k][i]-expected[i]) for k,expected in [('min',expected_min),('max',expected_max)] for i in range(3))
    if delta>0.0001 or source['triangles']!=glb['scene_triangles']:raise RuntimeError('Source to GLB geometry mismatch')
    evidence={'source_to_glb_max_bounds_delta_m':delta,'source_to_glb_triangles_match':True,'status':'PASS','scope':'Source geometry and static baseline export, not independent visual or GPU review','blender':bpy.app.version_string,'exporter':'4.3.47','seed':p['seed'],'source':source,'glb':glb,'expected_glb_bounds':{'min':expected_min,'max':expected_max},'export_options':{k:v for k,v in opts.items() if k!='filepath'},'source_generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256((HERE/'params.json').read_bytes()).hexdigest()}
    (out/'qa/evidence/build.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print('CYAMODUS_BUILD_OK',glb['sha256'],source['triangles'])
if __name__=='__main__':main()
