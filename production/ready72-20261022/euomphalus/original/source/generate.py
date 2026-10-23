# SPDX-License-Identifier: MIT
"""Original Euomphalus fossil-form reconstruction. Blender 4.3.2, no external assets.
Usage: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output DIR
The axis, end fill, angular shoulder and inferred shallow basal recess are semantic
modeling decisions, not a scan or exact reproduction of a photographed specimen.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy, bmesh
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, mesh_object, make_material, audit_source
from qa_glb import audit_glb

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,obj): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((HERE/'params.json').read_text())
    col=setup_scene('euomphalus',cfg['seed']);scene=bpy.context.scene
    scene.render.threads_mode='FIXED';scene.render.threads=2
    mats=[make_material('Shell limestone warm gray',cfg['palette']['shell'],roughness=cfg['roughness']),make_material('Terminal mineral fill',cfg['palette']['fill'],roughness=.98),make_material('Terminal mineral subtle facets',cfg['palette']['fill_shadow'],roughness=.98)]
    # Profile: inner shelf -> blunt high shoulder -> convex outer wall -> obtuse basal keel.
    prof=[(-1,.20),(-.92,.36),(-.63,.52),(-.30,.69),(.04,.85),(.19,.90),(.31,.86),(.61,.66),(.85,.36),(1,-.02),(.94,-.39),(.68,-.72),(.22,-.94),(-.20,-.89),(-.62,-.62),(-.92,-.29)]
    n=cfg['longitudinal_sections'];m=len(prof);turns=cfg['turns'];total=turns*2*math.pi;k=math.log(cfg['growth_per_turn'])/(2*math.pi)
    rend=.020;wend=cfg['radial_halfwidth_ratio']*rend;hend=cfg['vertical_halfheight'];theta_end=math.radians(cfg['terminal_angle_degrees'])
    vertices=[];faces=[];indices=[]
    def frame(t):
        q=math.exp(k*(t-total));r=rend*q;theta=theta_end+total-t
        # Small coherent original variation, not reference-derived texture.
        r*=1+.008*math.sin(3.1*theta+.4)*q
        xy=Vector((math.cos(theta),math.sin(theta),0));tangent=Vector((math.sin(theta),-math.cos(theta),0))
        center=xy*r+Vector((0,0,.0092+.0012*(1-q)))
        return q,theta,xy,tangent,center
    for i in range(n+1):
        t=total*i/n;q,theta,rad,tan,center=frame(t)
        for j,(u,z) in enumerate(prof):
            # Growth marks remain below 0.06 mm and do not become sculptural ribs.
            bend=.7*u+.5*z*z
            relief=cfg['surface_relief_m']*q**1.5*(.45*math.sin(cfg['growth_lines_per_turn']*t+bend)+.25*math.sin(91*t+2*j))
            broad=cfg['coherent_weathering_m']*q*(math.sin(7*theta+1.3*z)+.45*math.sin(13*theta+.8*u))
            chip=.00022*q*math.exp(-((total-t)/.12)**2)*max(0,math.sin(j*1.8+.3))
            rr=wend*q*u+(relief+broad-chip)*u
            zz=hend*q**cfg['vertical_growth_exponent']*z+(relief+.35*broad-chip*.5)*z
            v=center+rad*rr+Vector((0,0,zz))
            vertices.append(tuple(v))
    for i in range(n):
        for j in range(m):
            faces.append((i*m+j,i*m+(j+1)%m,(i+1)*m+(j+1)%m,(i+1)*m+j));indices.append(0)
    # Earliest whorl is filled/closed. No arbitrary drilled central hole.
    center=sum((Vector(v) for v in vertices[:m]),Vector())/m
    first=len(vertices);vertices.append(tuple(center))
    for j in range(m):faces.append((first,(j+1)%m,j));indices.append(0)
    # The final face is solid, irregular mineral fill. Shallow relief only.
    end_start=n*m;q,theta,rad,tan,c=frame(total)
    perimeter=[Vector(v) for v in vertices[end_start:end_start+m]]
    centroid=sum(perimeter,Vector())/m;last=list(range(end_start,end_start+m))
    # A constrained irregular triangulation avoids a radial star pattern in the fill.
    from mathutils.geometry import delaunay_2d_cdt
    import random
    rng=random.Random(cfg['seed']+31)
    ring2d=[Vector(((v-centroid).dot(rad)*.94,(v-centroid).z*.94)) for v in perimeter]
    points=list(ring2d)
    def inside(x,y):
        hit=False
        for j in range(m):
            aa=ring2d[j];bb=ring2d[(j+1)%m]
            if (aa.y>y)!=(bb.y>y) and x<(bb.x-aa.x)*(y-aa.y)/(bb.y-aa.y)+aa.x:hit=not hit
        return hit
    xlo,xhi=min(v.x for v in ring2d),max(v.x for v in ring2d)
    zlo,zhi=min(v.y for v in ring2d),max(v.y for v in ring2d)
    while len(points)<m+74:
        x=rng.uniform(xlo,xhi);z=rng.uniform(zlo,zhi)
        if inside(x,z) and all((Vector((x,z))-p).length>.00058 for p in points):points.append(Vector((x,z)))
    vv,ee,ff,origv,orige,origf=delaunay_2d_cdt(points,[(j,(j+1)%m) for j in range(m)],[list(range(m))],1,1e-9)
    offset=len(vertices);rimmap={}
    for idx,v in enumerate(vv):
        boundary=next((j for j,p in enumerate(ring2d) if (v-p).length<1e-8),None)
        relief=-.00004 if boundary is not None else rng.uniform(-.00013,.00014)
        vertices.append(tuple(centroid+rad*v.x+Vector((0,0,v.y))+tan*relief))
        if boundary is not None:rimmap[boundary]=offset+idx
    assert len(rimmap)==m
    for j in range(m):
        faces.append((last[j],last[(j+1)%m],rimmap[(j+1)%m],rimmap[j]));indices.append(0)
    for j,f in enumerate(ff):
        faces.append(tuple(offset+i for i in f));indices.append(2 if j%7==0 else 1)
    # The unresolved earliest mineralized whorl closes the center, appressed to the first turn.
    # This original sub-millimetre lobe avoids an unsupported through-hole, not a drilled plug.
    nc=Vector((0,0,.01045));nr=.00064;nh=.00140;ns=20;nl=8
    pole0=len(vertices);vertices.append(tuple(nc+Vector((0,0,-nh))))
    loops=[]
    for row in range(1,nl):
        phi=-math.pi/2+math.pi*row/nl;loop=[]
        for j in range(ns):
            ang=2*math.pi*j/ns;loop.append(len(vertices));vertices.append(tuple(nc+Vector((nr*math.cos(phi)*math.cos(ang),nr*math.cos(phi)*math.sin(ang),nh*math.sin(phi)))))
        loops.append(loop)
    for j in range(ns):faces.append((pole0,loops[0][(j+1)%ns],loops[0][j]));indices.append(0)
    for aa,bb in zip(loops,loops[1:]):
        for j in range(ns):faces.append((aa[j],aa[(j+1)%ns],bb[(j+1)%ns],bb[j]));indices.append(0)
    pole1=len(vertices);vertices.append(tuple(nc+Vector((0,0,nh))))
    for j in range(ns):faces.append((loops[-1][j],loops[-1][(j+1)%ns],pole1));indices.append(0)
    # Scale the descriptive material-level dimensions. Center the footprint, set lowest point to Z=0.
    lo=[min(v[a] for v in vertices) for a in range(3)];hi=[max(v[a] for v in vertices) for a in range(3)]
    scale_x=cfg['diameter']/(hi[0]-lo[0]);scale_y=cfg['inplane_depth']/(hi[1]-lo[1]);scale_z=cfg['height']/(hi[2]-lo[2])
    vertices=[((v[0]-(lo[0]+hi[0])/2)*scale_x,(v[1]-(lo[1]+hi[1])/2)*scale_y,(v[2]-lo[2])*scale_z) for v in vertices]
    obj=mesh_object('Continuous angular coiled fossil with filled termination',vertices,faces,mats,col)
    for poly,mi in zip(obj.data.polygons,indices):poly.material_index=mi;poly.use_smooth=(mi==0)
    # Longitudinal shoulder and basal keel stay definite while around-whorl curvature is smooth.
    for edge in obj.data.edges:
        a,b=edge.vertices
        if a<(n+1)*m and b<(n+1)*m and a%m==b%m and a%m in (5,12):edge.use_edge_sharp=True
    obj['representation']='Genus-level Euomphalus fossil form, E. pentangulatus-informed, Carboniferous'
    obj['surface']='Original parametric profile loft; mineral-filled cross-section; no textures or soft parts'
    obj['basal_uncertainty']='Conservatively inferred wide closed-bottom umbilical depression; no direct basal photo of anchor individual'
    root=bpy.data.objects[col['asset_root']];root['reference_scale']='M Coy 1844 species-description material, not selected photo individual measurements'
    bpy.context.view_layer.update()
    source=audit_source(col,max_triangles=24000)
    if source['errors']:raise RuntimeError(source['errors'])
    bm=bmesh.new();bm.from_mesh(obj.data)
    from mathutils.bvhtree import BVHTree
    bvh=BVHTree.FromBMesh(bm)
    axis=Vector((-(lo[0]+hi[0])/2*scale_x,-(lo[1]+hi[1])/2*scale_y,0))
    tested=missed=0
    for ii in range(-140,141):
        for jj in range(-140,141):
            xx=ii*.0001;yy=jj*.0001
            if xx*xx+yy*yy>.014**2:continue
            tested+=1
            hit=bvh.ray_cast(Vector((axis.x+xx,axis.y+yy,.05)),Vector((0,0,-1)),.1)[0]
            if hit is None:missed+=1
    if missed:raise RuntimeError('Projected inner disk has through-gap rays: '+str(missed))
    top={'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'inner_disk_top_ray_test':{'radius_m':.014,'grid_step_m':.0001,'tested':tested,'missed':missed,'scope':'100 micrometre sampled vertical occlusion across inner coil, not a general self-intersection proof'},'note':'A capped profile-loft plus closed earliest-whorl nucleus. Adjacent appressed whorls and the nucleus have small intended overlap; manifold edge check is not an intersection or printability certificate.'};bm.free()
    if top['boundary_edges'] or top['nonmanifold_edges'] or top['signed_volume_m3']<=0:raise RuntimeError(top)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'))
    bpy.ops.object.select_all(action='DESELECT')
    for o in col.all_objects:o.select_set(True)
    bpy.context.view_layer.objects.active=obj
    flags=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    options=bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
    missing=sorted(set(flags)-set(options))
    if missing:raise RuntimeError('Missing exporter options '+str(missing))
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**flags)
    glb=audit_glb(out/'model.glb',max_triangles=24000,max_materials=6,max_primitives=16)
    if glb['errors']:raise RuntimeError(glb['errors'])
    if (out/'model.glb').stat().st_size>2500000:raise RuntimeError('GLB size budget')
    write(out/'source-qa.json',source);write(out/'glb-audit.json',glb);write(out/'geometry.json',top)
    import io_scene_gltf2
    write(out/'build.json',{'asset_id':'euomphalus','revision':'r001','era':'Carboniferous','original_planning_interval':'Devonian','blender':bpy.app.version_string,'gltf_exporter':list(io_scene_gltf2.bl_info['version']),'generator_sha256':sha(__file__),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'semantic_sha256':glb.get('semantic_sha256'),'flags':flags,'seed':cfg['seed'],'threads':2,'dimensions_m':list(obj.dimensions),'palette':cfg['palette'],'origin':'Floor contact footprint center','authoring_axes':'Z up, -Y front; terminal points toward -Y in +X sector','scope':'maker technical checks only; no independent, GPU, scene, user, deployment approval'})
    print('EUOMPHALUS_BUILD_COMPLETE '+json.dumps({'glb_sha256':sha(out/'model.glb'),'semantic_sha256':glb.get('semantic_sha256'),'bytes':(out/'model.glb').stat().st_size,'triangles':source.get('triangles'),'dimensions':list(obj.dimensions)}))
if __name__=='__main__':main()
