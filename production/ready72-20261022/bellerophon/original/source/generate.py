# SPDX-License-Identifier: MIT
"""Original fossil-form model; no reference image, traced mesh or scan inputs.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
Only params.json and bundled Python helpers are required.
"""
from pathlib import Path
import sys, math, json, argparse, hashlib, shutil
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from asset_common import setup_scene, make_material, mesh_object, export_asset, _look_at, srgb_to_linear
SOURCE=Path(__file__).resolve().parent
P=json.loads((SOURCE/'params.json').read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x): Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def smooth(t): return t*t*(3-2*t)
def interpolate(rows,t):
    i=min(int(t*(len(rows)-1)),len(rows)-2); u=t*(len(rows)-1)-i
    vals=[]
    for k in range(len(rows[0])):
        p0=rows[max(0,i-1)][k]; p1=rows[i][k]; p2=rows[i+1][k]; p3=rows[min(len(rows)-1,i+2)][k]
        vals.append(.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u))
    return vals

def make_geometry(collection):
    # Longitudinal oval loft: posterior involute body, terminal expansion,
    # preserved thick margin, and attached shallow mineral-filled cap.
    n=P['angular_segments']; m=P['body_rings']; verts=[]; faces=[]; mids=[]
    # y, half-width, half-height, center-z, expansion blend (millimetres).
    controls=[(11,0,0,12,0),(10.5,4.2,5.2,12,0),(8.4,7.9,9.6,12.4,0),
      (5.2,10.1,11.8,12.7,0),(1.4,10.6,12.6,12.9,0),(-2.4,10.5,11.9,13.4,0),
      (-5.3,10.2,10.3,14.5,0),(-7.5,10.4,8.1,16.2,.12),
      (-9.4,12.6,8.3,18.0,.62),(-11.5,15.1,9.3,19.5,1)]
    verts.append((0,11,12))
    for j in range(1,m+1):
        t=j/m; yy,w,h,zc,flare=interpolate(controls,t)
        for i in range(n):
            a=2*math.pi*i/n; c=math.cos(a); s=math.sin(a)
            # Right-hand rim (front image-right) is not reconstructed.
            chip=smooth(max(0,math.cos(a)))
            rimloss=flare*chip
            rw=w*(1-.30*rimloss)*(1-.18*flare*max(0,-s)); rh=h*(1-.14*rimloss)
            x=rw*c; z=zc+rh*s
            y=yy + flare*(.24*(z-zc)+2.0*chip)
            # Bilateral shallow umbilical depressions, no through-hole.
            dent=2.6*math.exp(-(((y+.3)/3.2)**2+((z-12.8)/3.4)**2))
            x-=math.copysign(dent*abs(c)**3,x)
            # Small coiling shoulder around the depression, not exposed multiple turns.
            r=math.sqrt(((y+.3)/1.0)**2+((z-12.8)/1.06)**2)
            ph=math.atan2(z-12.8,y+.3)
            shoulder=.20*math.exp(-((r-(3.7+.38*ph))/0.65)**2)*abs(c)**4
            x+=math.copysign(shoulder,x)
            # Subdued growth increments and median band, sculpted into the surface.
            growth=.080*math.cos(2*math.pi*(t*16+.09*math.cos(2*a)))*(math.sin(math.pi*t)**.6)
            grain=.018*(math.sin(i*2.174+j*1.87)+.45*math.sin(i*5.19-j*3.13))
            bump=(growth+grain)*(math.sin(math.pi*t)**.4)
            x+=bump*c; z+=bump*s
            # Central band continues across visible front-lower body.
            band=.13*math.exp(-(x/.65)**2)*max(0,-s)*math.sin(math.pi*t)
            z-=band; y-=band*.7
            if flare>.7:
                edgewear=(flare-.7)/.3*.06*(math.sin(i*2.3)+.45*math.cos(i*4.11))
                x+=edgewear*c; z+=edgewear*s
            # R1: localized asymmetric loss, not a completed circular rim.
            angle=math.atan2(math.sin(a),math.cos(a))
            profile=[(-.90,0),(-.68,.65),(-.53,1.50),(-.30,1.10),(-.10,2.40),(.12,1.75),(.40,2.0),(.57,2.75),(.79,2.30),(.99,1.70),(1.12,0)]
            cut=0.0
            for (a0,v0),(a1,v1) in zip(profile,profile[1:]):
                if a0<=angle<a1:cut=v0+(v1-v0)*(angle-a0)/(a1-a0);break
            loss=smooth(max(0,min(1,(t-.82)/.18)))*cut
            x-=loss*c;z-=loss*s;y+=loss*.12
            if j>1:y=min(y,verts[1+(j-2)*n+i][1]-.025)
            verts.append((x,y,z))
    def idx(j,i): return 1+(j-1)*n+i%n
    for i in range(n): faces.append((0,idx(1,i+1),idx(1,i))); mids.append(0)
    for j in range(1,m):
        for i in range(n):
            a=idx(j,i); b=idx(j,i+1); c=idx(j+1,i+1); d=idx(j+1,i)
            # alternating triangulation avoids long aligned diagonal bands.
            fs=[(a,b,c),(a,c,d)] if (i+j)%2 else [(a,b,d),(b,c,d)]
            field=math.sin(i*.19+j*.31)+.48*math.sin(i*.63-j*.17)
            material=1 if field>1.22 else (2 if field<-1.24 else 0)
            angle=math.atan2(math.sin(2*math.pi*i/n),math.cos(2*math.pi*i/n))
            if -.78<angle<1.11 and j>=m-7:material=3
            faces.extend(fs); mids.extend([material]*2)
    outer=list(verts[1+(m-1)*n:1+m*n]); prev=[idx(m,i) for i in range(n)]
    body_tree=BVHTree.FromPolygons(verts,faces,all_triangles=True,epsilon=0)
    # Rolled edge has actual thickness, but only the surviving arc is high.
    for k,scale in enumerate([.982,.952]+[.92*(1-q/18) for q in range(18)]):
        cur=[]
        for i,(x,y,z) in enumerate(outer):
            a=2*math.pi*i/n
            centerz=19.5
            xx=x*scale; zz=centerz+(z-centerz)*scale
            # shallow inset closes the entire fossil: max ~2 mm, never a lumen.
            depth=.25 if k==0 else .70+.90*(1-scale)**.6
            damage=smooth(max(0,math.cos(a)))
            angle=math.atan2(math.sin(a),math.cos(a))
            if -.78<angle<1.11:damage=1.0
            depth*=1-.99*damage*scale**2
            yy=-11.5+.24*(zz-centerz) + (y-(-11.5+.24*(z-centerz)))*scale**2 + depth
            yy+=(.14*math.sin(xx*1.25)*math.cos(zz*1.12)+.16*math.sin(xx*.54+zz*.37))*math.sin(math.pi*scale)
            hit,normal,face,distance=body_tree.ray_cast(Vector((xx,-100,zz)),Vector((0,1,0)),200)
            if hit is not None: yy=min(yy,hit.y-.55*math.sin(math.pi*scale)**.5)
            if k>1:
                for dx,dz in [(-.35,0),(.35,0),(0,-.35),(0,.35)]:
                    near,_,_,_=body_tree.ray_cast(Vector((xx+dx,-100,zz+dz)),Vector((0,1,0)),200)
                    if near is not None:yy=min(yy,near.y-.4*math.sin(math.pi*scale)**.5)
            cur.append(len(verts)); verts.append((xx,yy,zz))
        for i in range(n):
            a=prev[i];b=prev[(i+1)%n];c=cur[(i+1)%n];d=cur[i]
            faces.extend([(a,b,c),(a,c,d)])
            mi=0 if k<2 and math.cos(2*math.pi*i/n)<.35 else 3
            mids.extend([mi,mi])
        prev=cur
    center=len(verts)
    hit,normal,face,distance=body_tree.ray_cast(Vector((0,-100,19.5)),Vector((0,1,0)),200)
    cy=min(-9.90,hit.y-.55) if hit is not None else -9.90
    verts.append((0,cy,19.5))
    for i in range(n): faces.append((prev[i],prev[(i+1)%n],center)); mids.append(3)
    # Preserve factual approximate dimensions; fit once, not per-view display scaling.
    lo=[min(v[k] for v in verts) for k in range(3)]; hi=[max(v[k] for v in verts) for k in range(3)]
    if 'baseline_raw_bounds_mm' in P:lo=P['baseline_raw_bounds_mm']['min'];hi=P['baseline_raw_bounds_mm']['max']
    size=[P['width_X'],P['depth_Y'],P['height_Z']]
    verts=[tuple(((v[k]-(lo[k]+hi[k])/2)/(hi[k]-lo[k])*size[k]) if k<2 else (v[k]-lo[k])/(hi[k]-lo[k])*size[k] for k in range(3)) for v in verts]
    mats=[make_material('chalky-shell','#B6AA96',.91),make_material('subtle-pale-weathering','#B9AD99',.94),make_material('worn-stone','#B2A692',.94),make_material('shallow-mineral-fill','#9F998D',.97)]
    ob=mesh_object('coiled-shell-with-preserved-flare-and-mineral-fill',verts,faces,mats,collection)
    for p,mi in zip(ob.data.polygons,mids): p.material_index=mi; p.use_smooth=(p.index<n+(m-3)*n*2 and mi!=3)
    bm=bmesh.new();bm.from_mesh(ob.data)
    if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
    bm.to_mesh(ob.data);bm.free();ob.data.update()
    ob['interpretation']='Original conservative fossil-form study of NMS G.1958.1.2964; left/top lip retained, right lip incomplete; mineral cap shallow.'
    ob['topology']='Single watertight connected outer surface, no floating rim, no internal chambers.'
    ob['mirror_damage']=False
    return ob

def render(glb,out,gray=False,res=768,samples=32):
    out.mkdir(parents=True,exist_ok=True); collection=setup_scene('bellerophon-render')
    before=set(bpy.data.objects); bpy.ops.import_scene.gltf(filepath=str(glb))
    meshes=[o for o in bpy.data.objects if o not in before and o.type=='MESH']
    if gray:
        mat=make_material('gray-diagnostic','#989898',.9)
        for ob in meshes:
            for i in range(len(ob.data.materials)): ob.data.materials[i]=mat
    points=[o.matrix_world@v.co for o in meshes for v in o.data.vertices]
    lo=Vector([min(v[k] for v in points) for k in range(3)]); hi=Vector([max(v[k] for v in points) for k in range(3)])
    center=Vector(P['presentation_preset']['target_m']) if 'presentation_preset' in P else (lo+hi)/2
    radius=P['presentation_preset']['ortho_scale_m']/2.2 if 'presentation_preset' in P else max((v-center).length for v in points)
    scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.cycles.device='CPU'; scene.cycles.samples=samples; scene.cycles.use_denoising=False
    scene.render.threads_mode='FIXED';scene.render.threads=2
    scene.render.resolution_x=scene.render.resolution_y=res;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
    scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    world=bpy.data.worlds.new('Neutral-studio');world.use_nodes=True;scene.world=world
    nt=world.node_tree;bg=nt.nodes.get('Background');bg.inputs[0].default_value=(.75,.75,.75,1);bg.inputs[1].default_value=.3
    cam_bg=nt.nodes.new('ShaderNodeBackground');cam_bg.inputs[0].default_value=tuple(srgb_to_linear(x/255) for x in (232,228,220))+(1,);cam_bg.inputs[1].default_value=1
    lp=nt.nodes.new('ShaderNodeLightPath');mix=nt.nodes.new('ShaderNodeMixShader');nt.links.new(lp.outputs['Is Camera Ray'],mix.inputs[0]);nt.links.new(bg.outputs[0],mix.inputs[1]);nt.links.new(cam_bg.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],nt.nodes['World Output'].inputs[0])
    for name,direction,energy,size in [('key',(-3,-4,6),450,4),('fill',(4,-1,3),150,5)]:
        d=bpy.data.lights.new(name,'AREA');d.energy=energy*(2*radius)**2/4;d.shape='DISK';d.size=size*radius
        o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=center+Vector(direction)*radius;_look_at(o,center)
    cam=bpy.data.cameras.new('camera');o=bpy.data.objects.new('camera',cam);scene.collection.objects.link(o);scene.camera=o
    cam.type='ORTHO';cam.ortho_scale=2*radius*1.10;cam.clip_start=.00001;cam.clip_end=10
    record={'glb_sha256':sha(glb),'source':'clean import of exact GLB','renderer':'Blender '+bpy.app.version_string+' Cycles CPU','gray':gray,'samples':samples,'resolution':[res,res],'view_transform':'Standard','look':'None','exposure':0,'target_m':list(center),'ortho_scale_m':cam.ortho_scale,'views':{}}
    for name,vec in [('front',(0,-1,0)),('side',(1,0,0)),('top',(0,0,1)),('perspective',(1,-1,1))]:
        o.location=center+Vector(vec).normalized()*radius*6;_look_at(o,center);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
        record['views'][name]={'file':name+'.png','sha256':sha(out/(name+'.png')),'camera_direction':vec}
    write(out/'view-manifest.json',record)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--render',choices=['gray','final']);ap.add_argument('--render-only',action='store_true');args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if not args.render_only:
        coll=setup_scene('bellerophon',P['seed']);ob=make_geometry(coll)
        record=export_asset('bellerophon',{'en':'Bellerophon fossil','zh':'Bellerophon 对称盘卷化石'},'geology',coll,output_root=out/'build',render=False,max_triangles=24000,max_materials=6,max_primitives=16,metadata={'source_generator':'source/generate.py','representation':'fossil-specimen','runtime_profile':'static palette-only','specimen_reference':'NMS G.1958.1.2964','reconstruction':'Original geometry; shallow mineral fill; asymmetrically incomplete terminal lip.'})
        p=out/'build/bellerophon'
        shutil.copyfile(p/'bellerophon.blend',out/'model.blend');shutil.copyfile(p/'bellerophon.glb',out/'model.glb')
        write(out/'build-report.json',{'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'generator_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),'metrics':record,'qa':json.loads((p/'qa.json').read_text()),'blender_version':bpy.app.version_string})
    if args.render:render(out/'model.glb',out/('gray' if args.render=='gray' else 'views'),gray=args.render=='gray',res=384 if args.render=='gray' else 896,samples=8 if args.render=='gray' else 48)
if __name__=='__main__':main()
