# SPDX-License-Identifier: MIT
"""Original Dactylioceras fossil geometry, not a scan or traced specimen.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output /path/output
Only local declared Python dependencies and Blender's bundled modules are imported.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--params',type=Path,default=HERE/'params.json')
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    p=json.loads(args.params.read_text()); out=args.output; out.mkdir(parents=True,exist_ok=True)
    col=setup_scene('dactylioceras',p['seed']); root=bpy.data.objects[col['asset_root']]
    root['representation']='fossil specimen; closed mineral fracture; no body chamber or soft anatomy'
    root['inference']='Opposite flank is approximately bilaterally reconstructed, not observed surface damage.'
    root['reference']='Howarth 1962, plate 16 figures 7a,b, GSM 26407; genus-level study'
    mats=[make_material('Weathered warm-grey limestone','#928978',.92),
          make_material('Worn rib crests','#A39A87',.90),
          make_material('Ochre mineral patches','#8D806A',.95),
          make_material('Closed broken mineral end','#777367',.98)]
    S=p['steps_per_turn']; turns=p['visible_complete_turns']; N=S*turns; C=p['cross_steps_per_flank']
    q=p['radial_growth_per_turn']; k=math.log(q)/(2*math.pi); end=2*math.pi*turns
    endangle=math.radians(p['terminal_angle_degrees']); startangle=endangle-end
    verts=[]; faces=[]; faceinfo=[]; lookup={}; groups={'Front_flank':set(),'Inferred_reverse_flank':set(),'Ribbed_venter':set(),'Closed_fracture':set(),'Nucleus':set()}
    # Both flanks are joined as a solid spiral-relief disk. Internal spiral seams
    # are welded at nonzero depth, not intersecting stacks of closed torus tubes.
    def vertex(i,j,side):
        if j==0 and i>=S: return vertex(i-S,C,side)
        outer=(j==C and i>=N-S)
        key=(i,j,0 if outer else side)
        if key in lookup: return lookup[key]
        t=i/S*2*math.pi; a=startangle+t; phi=math.pi*j/C; u=(1-math.cos(phi))/2
        R=math.exp(k*(t-end)); r=R*(1/q+(1-1/q)*u)
        primary_phase=46*(t-end)+.12*math.sin(phi)**2
        wear=.89+.07*math.sin(2.7*t+.8)+.04*math.sin(7.1*t+1.1)
        crest=max(0,math.cos(primary_phase))**2*wear
        secondary=max(0,math.cos(2*primary_phase+.08))**3
        # Shallow primary ribs are carved into the whole rounded cross-section.
        # A subdued secondary shoulder subdivision reaches the venter.
        ribs=p['rib_height_fraction']*crest + .024*secondary*u**5
        B=p['unscaled_half_breadth']*R
        def seam_y(ii):
            tt=ii/S*2*math.pi
            if ii>=N-S: return 0.0
            # Smoothly fade the internal seam depth at the emergence of the
            # free outer margin, avoiding a step at the terminal fracture.
            fade=min(1.,max(0.,(N-S-ii)/5.))
            return p['seam_depth_fraction']*p['unscaled_half_breadth']*math.exp(k*(tt-end))*fade
        yi=seam_y(i-S); yo=seam_y(i)
        y=(B*math.sin(phi)*(1+ribs)+(yi*(1-u)+yo*u)*abs(math.cos(phi))**4)
        # Radius modulation is identical at welded seams, so rib continuity is
        # structural rather than hidden overlapping floating ornament.
        r*=1+.0105*max(0,math.cos(46*t))**2
        # Small irregular fractured contour is confined to the final 3 rows.
        frac=max(0.,(i-(N-3))/3.)
        angle=a+frac*(.012*math.sin(phi*3.7)+.008*math.sin(phi*6.3))
        # Opposite sides share gross shape only; tiny weathering is asymmetric.
        y*=1+(.006*math.sin(3.1*t+phi)*math.sin(phi) if side>0 else -.005*math.sin(2.3*t+phi)*math.sin(phi))
        pos=(r*math.cos(angle),side*y,r*math.sin(angle))
        idx=len(verts); verts.append(pos); lookup[key]=idx
        groups['Front_flank' if side<0 else 'Inferred_reverse_flank'].add(idx)
        if j>=C-2: groups['Ribbed_venter'].add(idx)
        return idx
    for side in (-1,1):
        for i in range(N):
            for j in range(C):
                quad=[vertex(i,j,side),vertex(i+1,j,side),vertex(i+1,j+1,side),vertex(i,j+1,side)]
                faces.append(quad if side<0 else quad[::-1]); faceinfo.append(('body',i,j,side))
    # Fill the tiny inner nucleus, with a shallow offset fan center to avoid
    # degenerate collinear triangles at the radial beginning of the spiral.
    for side in (-1,1):
        contour=[vertex(i,0,side) for i in range(S+1)]+[vertex(0,j,side) for j in range(C-1,0,-1)]
        r0=math.exp(-k*end)/q
        theta=startangle-math.pi/2
        center=len(verts); verts.append((r0*.14*math.cos(theta),side*r0*.19,r0*.14*math.sin(theta))); groups['Nucleus'].add(center)
        for n in range(len(contour)):
            tri=[center,contour[n],contour[(n+1)%len(contour)]]
            faces.append(tri if side<0 else tri[::-1]); faceinfo.append(('nucleus',n,0,side))
    # The preserved growth end is a CLOSED irregular mineral face, not a lip or
    # living aperture. Its polygonal fan covers the full solid whorl section.
    endcontour=[vertex(N,j,-1) for j in range(C+1)]+[vertex(N,j,1) for j in range(C-1,-1,-1)]
    # Inner endpoint lies on the prior outer edge and is shared, so remove repeat.
    if endcontour[-1]==endcontour[0]: endcontour.pop()
    mid=Vector((0,0,0))
    for idx in endcontour: mid+=Vector(verts[idx])
    mid/=len(endcontour)
    mid+=Vector((-math.sin(endangle),0,math.cos(endangle)))*.004
    ci=len(verts); verts.append(tuple(mid)); groups['Closed_fracture'].update(endcontour+[ci])
    for n in range(len(endcontour)):
        faces.append([ci,endcontour[n],endcontour[(n+1)%len(endcontour)]]); faceinfo.append(('fracture',n,0,0))
    # Normalize only to declared real size, never a display unit cube.
    outerpoints=[verts[vertex(i,C,-1)] for i in range(N-S,N+1)]
    diameter=max(math.hypot(a[0]-b[0],a[2]-b[2]) for a in outerpoints for b in outerpoints)
    xzscale=p['maximum_diameter']/diameter
    ys=max(v[1] for v in verts)-min(v[1] for v in verts); yscale=p['outer_whorl_breadth']/ys
    verts=[(x*xzscale,y*yscale,z*xzscale) for x,y,z in verts]
    lo=[min(v[a] for v in verts) for a in range(3)]; hi=[max(v[a] for v in verts) for a in range(3)]
    shift=(-(hi[0]+lo[0])/2,-(hi[1]+lo[1])/2,-lo[2])
    verts=[tuple(v[a]+shift[a] for a in range(3)) for v in verts]
    # Measure anatomical design landmarks from the final vertex coordinates.
    inner_ids=[vertex(i,0,-1) for i in range(N-S,N+1)]
    inner_points=[verts[i] for i in inner_ids]
    umbilicus_measured=max(math.hypot(a[0]-b[0],a[2]-b[2]) for a in inner_points for b in inner_points)
    endinner=Vector(verts[vertex(N,0,-1)]); endouter=Vector(verts[vertex(N,C,-1)])
    whorl_height_measured=(endouter-endinner).length
    obj=mesh_object('Continuous_ribbed_coil_and_closed_fossil_fracture',verts,faces,mats,col)
    for poly,info in zip(obj.data.polygons,faceinfo):
        kind,i,j,side=info
        if kind=='fracture': poly.material_index=3
        elif kind=='nucleus': poly.material_index=0
        else:
            t=(i+.5)/S*2*math.pi; u=(j+.5)/C
            patch=math.sin(1.7*t+2*u)+.52*math.sin(5*t-3*u+side)
            # Sparse coherent mineral patches, no random per-face rainbow noise.
            poly.material_index=2 if patch>1.10 else 1 if math.cos(46*t)>.70 and .12<u<.94 else 0
        poly.use_smooth=False
    for name,inds in groups.items():
        g=obj.vertex_groups.new(name=name); g.add(sorted(inds),1.,'REPLACE')
    obj['method']='Welded continuous logarithmic spiral relief surface; rounded cross-whorl loft; integrated primary ribs'
    obj['primary_ribs_per_revolution']=46; obj['modeled_complete_turns']=turns
    obj['unobserved_reverse_flank']='Bilateral geometric inference, not an observed specimen face'
    obj['fracture']='Closed mineral break; no internal chamber anatomy reconstructed'
    source=audit_source(col,max_triangles=28000)
    write(out/'source-audit.json',source)
    if source['errors']: raise RuntimeError(str(source['errors']))
    bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects: o.select_set(True)
    bpy.context.view_layer.objects.active=root
    opts=dict(filepath=str(out/'model.glb'),export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={v.identifier for v in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(opts)-available: raise RuntimeError('Required export option missing')
    bpy.ops.export_scene.gltf(**opts)
    glb=audit_glb(out/'model.glb',28000,6,16); glb['file']='model.glb'
    b=source['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(glb['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
    write(out/'glb-audit.json',glb)
    report={'asset_id':'dactylioceras','revision':'r001','blender_version':bpy.app.version_string,'python_version':sys.version,'resolved_asset_helper_modules':{name:Path(sys.modules[name].__file__).resolve().relative_to(HERE).as_posix() for name in ['asset_common','qa_glb']},'glb_sha256':digest(out/'model.glb'),'generator_sha256':digest(__file__),'params_sha256':digest(args.params),'geometry_digest':glb.get('semantic_sha256'),'source_triangles':source['triangles'],'source_export_bounds_max_delta_m':delta,'diameter_m':p['maximum_diameter'],'breadth_m':p['outer_whorl_breadth'],'umbilicus_width_design_m':p['maximum_diameter']/q,'umbilicus_width_measured_m':umbilicus_measured,'terminal_whorl_height_m':whorl_height_measured,'umbilicus_method':'Diameter of first outer-whorl inner seam under logarithmic radial ratio; not a through-hole','complete_turns':turns,'primary_ribs':46,'origin':'Floor contact bbox center, identity root','export_options':{k:v for k,v in opts.items() if k!='filepath'},'flat_shading':'Intentional low-poly faceting, fracture flat; no smoothing needed to hide geometry','source_warning_review':source['warnings'],'reverse_flank_inference':True,'build_scope':'Maker technical evidence only; not independent acceptance'}
    write(out/'build.json',report)
    if glb['errors'] or glb['bytes']>2500000 or delta>1e-6 or source['triangles']!=glb['scene_triangles']: raise RuntimeError('GLB/build contract failure: '+str(glb))
    print('BUILD_COMPLETE '+json.dumps(report))
if __name__=='__main__': main()
