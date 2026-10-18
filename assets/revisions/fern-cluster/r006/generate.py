# SPDX-License-Identifier: MIT
"""Original fern structural revision. Blender 4.3.2; deterministic; no textures.
Run: blender -b -t 2 --python-exit-code 1 --python generate.py -- --output-dir ATTEMPT
Geometry CC-BY-4.0 Leon Made This / s010s. Code MIT.
"""
from pathlib import Path
import sys, json, math, argparse, hashlib
import bpy
from mathutils import Vector
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').is_file())
sys.path.insert(0,str(ROOT/'scripts'))
import asset_common as common
sys.path.insert(0,str(Path(__file__).resolve().parent))
sys.path.insert(0,str(ROOT/'scripts/models'))
from build_understory import MeshBuilder, tube
SEED=20261017

def blade(builder,base,axis,normal,length,width,bend=.025,mat=0):
    """Swept thin closed lance, gradual camber; no broad arrow shoulders/folded fan."""
    axis=axis.normalized(); normal=normal.normalized(); side=axis.cross(normal).normalized()
    normal=side.cross(axis).normalized()
    # Section positions consciously concentrate outline changes near base and tip.
    stations=[0,.19,.45,.73,1]
    widths=[.10,.90,1,.60,.018]
    verts=[]
    for i,(t,w) in enumerate(zip(stations,widths)):
        center=base+axis*(length*t)+normal*(bend*math.sin(math.pi*t)-.018*t*t)
        # Gentle along-axis twist and shallow continuous camber, never a single sharp tent fold.
        local_side=(side+normal*(.10*math.sin(math.pi*t))).normalized()
        local_n=local_side.cross(axis).normalized()
        h=max(.00045,width*.075*(math.sin(math.pi*t)**.7))
        # Four-vertex diamond section supplies actual thin volume and two calm upper planes.
        verts.extend([center+local_side*width*w,center+local_n*h,
                      center-local_side*width*w,center-local_n*.0006])
    faces=[(3,2,1,0)]
    for j in range(len(stations)-1):
        for k in range(4):
            a=j*4+k;b=j*4+(k+1)%4;c=(j+1)*4+(k+1)%4;d=(j+1)*4+k
            # Explicit triangulation keeps the intended sweep diagonal after export.
            faces.extend([(a,b,c),(a,c,d)])
    faces.append(tuple((len(stations)-1)*4+k for k in range(4)))
    builder.append(verts,faces,mat)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--config',type=Path,required=True)
    args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    config=json.loads(args.config.read_text())
    assert config['seed']==SEED and config['max_triangles']==12000, 'Unexpected frozen parameters'
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.glob('fern-cluster/*.glb')): raise RuntimeError('Attempt already contains an export; use a new attempt')
    col=common.setup_scene('fern-cluster',SEED)
    palette={'fern_deep':'#294C43','fern_mid':'#47745C','fern_light':'#719366'}
    mats={k:common.make_material(k,v,roughness=.88) for k,v in palette.items()}
    crown=MeshBuilder();tube(crown,[(0,0,.0),(.006,0,.025),(.005,0,.053)],[.072,.064,.032],sides=7)
    crown.finish('Low rhizome crown',mats['fern_deep'],col)
    axes=MeshBuilder()
    # Angles, radial span, peak-height control, terminal height, width, palette.
    # Unequal sector spacing and three height tiers preserve open windows between fronds.
    specs=[(-91,.75,.64,.18,.224,'fern_mid'),(-24,.73,.83,.25,.213,'fern_mid'),
           (42,.58,1.02,.46,.189,'fern_light'),(99,.73,.91,.36,.216,'fern_mid'),
           (157,.76,.76,.24,.222,'fern_deep'),(218,.70,.57,.14,.203,'fern_mid'),
           (278,.49,1.09,.57,.170,'fern_light')]
    endpoints=[]
    for n,(degrees,span,h,tip_z,pwidth,color) in enumerate(specs):
        a=math.radians(degrees);rad=Vector((math.cos(a),math.sin(a),0));lat=Vector((-math.sin(a),math.cos(a),0))
        origin=rad*(.022+.007*(n%3))+Vector((0,0,.028))
        def path(t):
            # Cubic Bezier: near-upright stipe, continuous crest, drooping outward end.
            p0=origin;p1=origin+rad*.035+Vector((0,0,h*.72))
            p2=origin+rad*(span*.55)+Vector((0,0,h));p3=origin+rad*span+Vector((0,0,tip_z))
            return p0*((1-t)**3)+p1*(3*(1-t)**2*t)+p2*(3*(1-t)*t*t)+p3*t**3+lat*(.026*math.sin(math.pi*t)*(1 if n%2 else -1))
        ts=[i/16 for i in range(17)]
        tube(axes,[path(t) for t in ts],[.0105*(1-t)**1.15+.00065 for t in ts],sides=5)
        leaf=MeshBuilder()
        for j in range(12):
            t0=.24+j*.061
            for handed in [-1,1]:
                t=t0+(.014 if handed==1 else 0)
                taper=(math.sin(math.pi*(t-.13)/.91)**.72)*(1-.31*t)
                length=pwidth*taper*(1+.035*handed*math.sin(n+j))
                tangent=(path(t+.002)-path(t-.002)).normalized()
                fn=tangent.cross(lat).normalized()
                # Pinnae follow the curved frond plane and turn gradually toward its tip.
                direction=(lat*handed+tangent*(.25+.34*t)).normalized()
                base=path(t)-direction*.002
                width=min(.0175*(taper**.80),length*.115)
                blade(leaf,base,direction,fn,length,width,bend=.0065*taper)
        # A small gradual terminal blade, visually continuous with the narrowing rachis.
        tangent=(path(1)-path(.97)).normalized();fn=tangent.cross(lat).normalized()
        blade(leaf,path(.96),tangent,fn,.069,.0060,bend=.002)
        obj=leaf.finish(f'Curved pinnate frond {n+1:02d}',mats[color],col)
        # Coherent flat shading across each authored quad's two explicit triangles.
        # Keeps exact triangulated positions and one broad surface plane per quad.
        mesh=obj.data;mesh.update()
        normals=[tuple(poly.normal) for poly in mesh.polygons]
        for block in range(0,len(mesh.polygons),34):
            for j in range(block+1,block+33,2):
                normal=(mesh.polygons[j].normal+mesh.polygons[j+1].normal).normalized()
                normals[j]=normals[j+1]=tuple(normal)
        custom=[(0,0,1)]*len(mesh.loops)
        for poly,normal in zip(mesh.polygons,normals):
            poly.use_smooth=True
            for li in poly.loop_indices:custom[li]=normal
        mesh.normals_split_custom_set(custom)
        endpoints.append(list(path(.56)))
    axes.finish('Seven continuously tapered stipes and rachises',mats['fern_deep'],col)
    # One modest, separate growing crozier: a clean continuous spiral, no flower or seed head.
    young=MeshBuilder();rad=Vector((-.7,-.7,0));across=Vector((.819,.574,0))
    center=Vector((-.23,-.22,.43))
    pts=[Vector((-.018,-.018,.018)),Vector((-.15,-.14,.24)),center+Vector((0,0,-.066))]
    radii=[.010,.009,.008]
    for j in range(21):
        theta=-math.pi/2+j*math.tau*.94/20;r=.066*(1-.72*j/20)
        pts.append(center+across*(math.cos(theta)*r)+Vector((0,0,math.sin(theta)*r)))
        radii.append(.008-.0045*j/20)
    tube(young,pts,radii,sides=5)
    young.finish('Continuous unfurling young frond',mats['fern_light'],col)
    common.ground_asset(col)
    authored=sum(len(o.data.vertices) for o in col.all_objects if o.type=='MESH')
    metadata={'author':'Leon Made This / s010s','license':'CC-BY-4.0','generator':str(Path(__file__).resolve().relative_to(ROOT)),
      'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'generator_seed':SEED,
      'scientific_scope':'Evidence-informed stylized fern concept; no named taxon, fossil specimen, period or locality reconstruction.',
      'description':{'en':'Seven gently arched pinnate fronds with continuous taper, narrow swept pinnae and readable crown gaps.','zh':'七片连续弯曲并逐渐收细的羽状蕨叶，狭长羽片自然接入叶轴，叶丛保留清楚空隙。'},
      'palette_srgb':palette,'authored_source_vertices':authored,'evaluated_source_vertices':authored,
      'modeling_runtime':'GPT-6 Astra xhigh; cloud only; Blender 4.3.2',
      'topology_notes':'Closed thin solid pinnae with gradual sectional camber. No alpha cards, texture veins, displacement or unmodified primitive foliage.',
      'parameters':{'seed':SEED,'fronds':specs,'pinna_pairs':12,'rachis_sections':17,'pinna_sections':5},
      'sources':[{'title':'American Fern Society: About Ferns, shared derived traits / Figure 2','url':'https://www.amerfernsoc.org/about-ferns'}]}
    record=common.export_asset('fern-cluster',{'en':'Ground fern cluster, structural revision','zh':'地被蕨丛·结构修订'},'plants',col,
             metadata=metadata,output_root=out,render=False,max_triangles=12000,max_materials=3,max_primitives=16)
    from pack_static import pack
    from qa_glb import audit_glb
    folder=out/'fern-cluster';packing=pack(folder/'fern-cluster.glb')
    audit=audit_glb(folder/'fern-cluster.glb',max_triangles=12000,max_materials=3,max_primitives=16)
    assert not audit['errors'],audit['errors']
    record['glb_bytes']=audit['bytes'];record['sha256']['glb']=audit['sha256'];record['packing']=packing
    record['topology_notes']='Pinna source remains semantically editable. Custom normals join each authored quad triangle pair without changing positions. Export groups exact POSITION/NORMAL pairs into three material primitives.'
    (folder/'metadata.json').write_text(json.dumps(record,indent=2)+'\n')
    qa=json.loads((folder/'qa.json').read_text());qa['glb']=audit
    (folder/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    (out/'parameters.json').write_text(json.dumps(metadata['parameters'],indent=2)+'\n')
    print('FERN_CANDIDATE '+json.dumps({'triangles':record['triangles'],'glb':record['glb'],'dimensions':record['dimensions']}))
if __name__=='__main__':main()
