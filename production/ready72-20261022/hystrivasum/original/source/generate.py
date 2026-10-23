# SPDX-License-Identifier: MIT
"""Original deterministic Hystrivasum shell study. Blender 4.3.2; no photo input.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir PATH
Editable anatomical regions are vertex groups on one continuous shell envelope.
Only visible aperture/umbilical recess is reconstructed, not hidden chambers.
"""
from pathlib import Path
import argparse, json, math, sys, hashlib
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb
PI=math.pi

def lerp_table(x, pairs):
    if x<=pairs[0][0]: return pairs[0][1]
    for (a,b),(c,d) in zip(pairs,pairs[1:]):
        if x<=c:
            u=(x-a)/(c-a)
            return b+(d-b)*u
    return pairs[-1][1]

def smoothstep(a,b,x):
    u=max(0,min(1,(x-a)/(b-a))); return u*u*(3-2*u)

def gauss(x,w): return math.exp(-(x/w)**2)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d): Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

def main():
    av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args(av)
    out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text())
    col=setup_scene('hystrivasum',seed=p['seed'])
    mats=[make_material('Fossil shell | warm limestone',p['palette'][0],.88),
          make_material('Aperture and callus | pale calcite',p['palette'][1],.8),
          make_material('Scale crests | weathered cream',p['palette'][2],.88)]
    # Anatomical profile in mm. This is a free-designed loft, not a traced photo.
    profile=[(0,2.7),(2,6.4),(6,8),(12,7.6),(19,9),(24,11.9),(30,15.9),(36,19.8),
             (44,24),(52,27),(61,28.4),(68,27.5),(73,25.3),(77,22),(82,18.1),
             (87,14.1),(92,10.6),(97,7.2),(101,4.6),(104,2.4),(106,1.0)]
    # Explicit adaptive heights retain the five broad body ridges and basal cords.
    heights={0,1.1,2.5,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76}
    main_cords=[33,43,53,63,73]
    basal=[4.5,9,13.5,18]
    for c in main_cords:
        heights.update([c-2.4,c-.7,c,c+.6,c+1.8])
    for c in basal: heights.update([c-.8,c,c+.7])
    heights.update([27,29,31,35,37,39,41,45,47])
    heights.update([78,79.5,81,82.5,84,85.5,87,88.5,90,91.5,93,94.5,96,97.5,99,100.5,102,103.2,104.2,105.2,106])
    # Prevent almost-coincident rings, retain exact feature rows.
    H=sorted(heights)
    NO=p['outer_segments'];NI=p['inner_segments'];N=NO+NI
    verts=[];faces=[];face_mats=[];regions={'body':[],'spire':[],'aperture':[],'columellar_folds':[],'siphonal_channel':[],'umbilical_recess':[]}
    def contour(s,theta):
        r=lerp_table(s,profile)
        lower=smoothstep(1,23,s)*(1-smoothstep(72,77,s))
        # A shallow oblique cord pitch. Spire itself is a continuous dextral logarithmic phase.
        z=s+2.3*math.cos(theta-.6)*lower
        crest=0
        for k,c in enumerate(main_cords):
            delta=s-c
            if -3.8<delta<2.4:
                ridge=lerp_table(delta,[(-3.8,0),(-2.4,.26),(-.7,.72),(0,1),(.6,.35),(1.8,0),(2.4,0)])
                wave=(.5+.5*math.cos((12 if k==4 else 14)*theta-.38*k+.14*math.sin(3*theta)))**3
                amp=[1.45,1.7,1.95,2.25,3.2][k]
                if k==4:
                    # Broad plates separated by deep valleys, rather than a narrow serrated ring.
                    plate=smoothstep(-.82,-.10,math.cos(12*theta-.38*k+.14*math.sin(3*theta)))
                    r+=ridge*(.60+6.12*plate)
                    # Upcurled outer ends: continuous wide roots below and an undercut return above.
                    z+=0.0 # Lift applied as a wider continuous return below, avoiding folded self-overlap.
                else:
                    r+=ridge*(amp+wave*amp*1.1)
                    z+=ridge*wave*.6
                crest=max(crest,ridge)
        # The return surface retains the plate uplift over several mm; it does not
        # fold back through the rising outer surface at the lip.
        if 69.2<s<84:
            plate=smoothstep(-.82,-.10,math.cos(12*theta-1.52+.14*math.sin(3*theta)))
            z+=2.2*smoothstep(69.2,73,s)*(1-smoothstep(73,84,s))*plate
        for c in basal: r+=1.0*gauss(s-c,.72)*(.75+.25*math.cos(9*theta+.4))
        if s>=76:
            gap=max(1,107-s)
            phase=2*PI*math.log(gap/31)/math.log(.57)-theta
            ridge=((1+math.cos(phase))*.5)**4
            flare=.14*gap*ridge
            scallop=smoothstep(-.82,-.10,math.cos(10*theta+phase*.13))
            r+=flare*(.12+1.30*scallop)
            crest=max(crest,ridge)
            z+=.55*ridge*scallop*min(1,gap/18)
        # Sparse low-amplitude growth undulation, not photo cracks or dense noise.
        r+=.14*math.sin(19*theta+s*.12)*smoothstep(6,23,s)*(1-smoothstep(82,100,s))
        return r,z,crest
    for row,s in enumerate(H):
        left=math.radians(lerp_table(s,[(0,-110),(5,-105),(20,-110),(34,-102),(46,-84),(57,-82),(65,-77),(72,-72),(78,-84),(106,-84)]))
        width=math.radians(lerp_table(s,[(0,35),(3,58),(13,62),(22,48),(33,73),(48,100),(57,93),(63,77),(69,43),(73,26),(77,26),(106,26)]))
        right=left+width
        # Outer surface long arc, followed by visible concave aperture short arc.
        for j in range(N):
            inside=j>=NO
            if not inside: theta=right+(2*PI-width)*j/NO;f=None
            else: f=(j-NO)/NI;theta=left+f*width+2*PI
            r,z,crest=contour(s,theta)
            region='spire' if s>=76 else 'body'
            mouth=smoothstep(.5,4,s)*(1-smoothstep(65,74,s))
            lip_angle=(theta-right+PI)%(2*PI)-PI
            r+=2.8*gauss(lip_angle,.18)*mouth
            callus_angle=(theta-left+PI)%(2*PI)-PI
            rim_weight=gauss(callus_angle,.21)*mouth
            r=r*(1-.65*rim_weight)+lerp_table(s,profile)*.65*rim_weight
            for zz,amp in [(29,2.7),(37,3.3),(45,4.0)]:
                r+=amp*gauss(s-(zz-2.4*callus_angle),1.45)*gauss(callus_angle-.075,.20)*mouth
            if inside and mouth>0:
                depth=lerp_table(s,[(0,0),(3,4.0),(9,5.8),(18,6.0),(28,11),(40,19),(53,22),(61,19),(67,11),(74,0)])*mouth
                cavity=math.sin(PI*f)**.58*smoothstep(0,.38,f)
                # Suppress exterior cords inside; broad calcite callus stays thick on left.
                raw=lerp_table(s,profile)
                r=(1-cavity)*r+cavity*raw-depth*cavity
                r+=3.8*gauss(f-.08,.115)*mouth
                for zz,amp in [(29,1.5),(37,1.9),(45,2.3)]:
                    fold=amp*gauss(s-(zz-4*f),1.45)*gauss(f-.18,.19)
                    r+=fold
                    if fold>.35: region='columellar_folds'
                if region!='columellar_folds': region='siphonal_channel' if s<24 else 'aperture'
            # A genuine geometric basal recess adjacent to, not a second main aperture.
            da=(theta-math.radians(-132)+PI)%(2*PI)-PI
            recess=4.6*gauss(da,.24)*gauss(s-10,4.1)
            if not inside:
                r-=recess
                if recess>.8: region='umbilical_recess'
            # Slight axial offset tracks the coiling toward the spire.
            cx=1.1*smoothstep(75,106,s);cy=.5*smoothstep(75,106,s)
            verts.append(((r*math.cos(theta)+cx)*.001,(r*math.sin(theta)+cy)*.001,z*.001))
            regions[region].append(len(verts)-1)
    for i in range(len(H)-1):
        s=(H[i]+H[i+1])/2
        for j in range(N):
            faces.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
            inface=j>=NO or j==N-1
            if inface and 2<s<72: mi=1
            elif any(-.8<s-c<.7 for c in main_cords):mi=2
            else:mi=0
            face_mats.append(mi)
    # True pole fans close the tip and the tiny basal contact patch without n-gon ambiguity.
    base=len(verts);verts.append((0,0,0))
    tip=len(verts);verts.append((.0011,.0005,.107))
    for j in range(N):
        faces.append((base,(j+1)%N,j));face_mats.append(0)
        faces.append(((len(H)-1)*N+j,(len(H)-1)*N+(j+1)%N,tip));face_mats.append(0)
    # Scale bounds to the explicitly approximate measured/inferred study dimensions.
    lo=[min(v[k] for v in verts) for k in range(3)];hi=[max(v[k] for v in verts) for k in range(3)]
    frame=p.get('frozen_frame')
    scale=frame['scale'] if frame else [p['width']/(hi[0]-lo[0]),p['depth']/(hi[1]-lo[1]),p['height']/(hi[2]-lo[2])]
    center=frame['center_xy_unscaled'] if frame else [(lo[0]+hi[0])/2,(lo[1]+hi[1])/2]
    zmin=frame['z_min_unscaled'] if frame else lo[2]
    verts=[((v[0]-center[0])*scale[0],(v[1]-center[1])*scale[1],(v[2]-zmin)*scale[2]) for v in verts]
    obj=mesh_object('Continuous dextral shell, aperture and canal',verts,faces,mats,col)
    for poly,mi in zip(obj.data.polygons,face_mats):poly.material_index=mi;poly.use_smooth=True
    for name,ids in regions.items():
        if ids: obj.vertex_groups.new(name=name.replace('_',' ')).add(ids,1,'REPLACE')
    obj['anatomy']='5 main body cords; 3 columellar folds; 4 basal cords; 12 main shoulder scales before aperture interruption'
    obj['reconstruction']='Genus-level external fossil-form study. Accidental breakage and borings omitted; no exact-specimen restoration.'
    src=audit_source(col,p['geometry_policy']['max_triangles'])
    write(out/'source-audit.json',src)
    if src['errors']:raise RuntimeError(src['errors'])
    bpy.context.scene['asset_license']='CC-BY-4.0';bpy.context.scene['asset_author']='Leon Made This / s010s'
    bpy.context.scene['generator_seed']=p['seed'];bpy.context.scene['source_parameter_sha256']=sha(HERE/'params.json')
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.all_objects:ob.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects[col['asset_root']]
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={r.identifier for r in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available:raise RuntimeError('Missing exporter options')
    bpy.ops.export_scene.gltf(**opts)
    g=audit_glb(out/'model.glb',p['geometry_policy']['max_triangles'],p['geometry_policy']['max_materials'],p['geometry_policy']['max_primitives'])
    write(out/'glb-audit.json',g)
    if g['errors']:raise RuntimeError(g['errors'])
    if g['bytes']>p['geometry_policy']['max_glb_bytes']:raise RuntimeError('GLB byte budget exceeded')
    b=src['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    err=max(abs(g['bounds_m'][key][i]-expected[key][i]) for key in ['min','max'] for i in range(3))
    assert err<1e-6 and g['scene_triangles']==src['triangles']
    write(out/'build.json',{'asset_id':'hystrivasum','revision':'r001','blender':bpy.app.version_string,'generator_sha256':sha(__file__),'parameters_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'geometry_semantic_sha256':g['semantic_sha256'],'triangles':g['scene_triangles'],'bounds_roundtrip_max_error_m':err,'exporter_options':{k:v for k,v in opts.items() if k!='filepath'},'applied_bound_scale':scale,'height_rings':len(H),'angular_segments':N,'source_dimensions_m':b['size'],'material_profile':'palette-only opaque single-sided PBR','shading':'intentional smooth interpolation over a curated low-poly loft; crest shape is geometry','reconstruction_limit':'Visible short cavity only. No hidden chambers. Approximate shell geometry, not exact specimen or diagnostic taxonomy.'})
    print('MAKER_BUILD_OK',g['scene_triangles'],g['semantic_sha256'])
if __name__=='__main__':main()
