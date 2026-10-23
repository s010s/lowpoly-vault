# SPDX-License-Identifier: MIT
"""Original Pinna (Cyrtopinna) socialis fossil-form reconstruction.

Run with Blender 4.3.2:
  blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUTPUT
Only this source tree, the sibling brief/references, and Blender are required.
The two closed valve-envelope solids represent the reconstructed fossil form,
not recovered shell-wall thickness or exposed nacre anatomy.
"""
from pathlib import Path
import argparse, hashlib, json, math, shutil, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from asset_common import setup_scene, make_material, mesh_object, export_asset


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def lerp(t,points):
    if t<=points[0][0]: return points[0][1]
    for (a,x),(b,y) in zip(points,points[1:]):
        if t<=b: return x+(y-x)*(t-a)/(b-a)
    return points[-1][1]


def main():
    args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args(args); out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    params=json.loads((HERE/'params.json').read_text())
    brief=json.loads((HERE.parent/'brief.json').read_text())
    collection=setup_scene('pinna',seed=params['seed'])
    scene=bpy.context.scene; scene.render.threads_mode='FIXED'; scene.render.threads=2
    root=bpy.data.objects['pinna']; root['anterior']='-X'; root['dorsal']='+Z'
    root['representation']='Original reconstructed fossil valve envelopes; not a scan or shell-wall thickness model.'
    root['specimen']='VTT001-7; estimated missing tip after Koppka 2018 Text-fig. 4'
    mats=[make_material('fossil-limestone',params['palette']['base'],0.91),
          make_material('subtle-growth-laminae',params['palette']['growth'],0.94),
          make_material('mating-surface-and-rim',params['palette']['interior'],0.96)]
    ts=params['longitudinal_rows']
    vs=params['cross_section_nodes']
    n=len(vs)
    parts=[]; measures=[]
    for sign,name in [(-1,'right-valve-envelope'),(1,'left-valve-envelope')]:
        verts=[]; faces=[]; indices=[]
        # Pointed tip is author-reconstructed, not intact fossil evidence.
        verts.append((-59.5,sign*0.075,31.65))
        for i,t in enumerate(ts):
            top=lerp(t,params['dorsal_profile_mm'])
            bot=lerp(t,params['ventral_profile_mm'])
            center=bot+(top-bot)*0.55 # ventral sector slightly taller
            # Section transitions from rounded anterior to prominent rhomboid keel.
            inflated=lerp(t,params['inflation_profile_mm'])
            for j,s in enumerate(vs):
                z=center+(top-center)*s if s>=0 else center+(center-bot)*s
                curvature=(3.3+2.0*t)*(abs(s)**3.2)*(math.sin(math.pi*t/2)**0.8)
                x=-59.5+119*t-curvature
                rounded=math.sqrt(max(0,1-s*s))
                keeled=(1-abs(s))**0.84
                adult=max(0,min(1,(t-0.08)/0.34))
                cross=(1-adult)*rounded+adult*keeled
                byssal=0.50*math.exp(-((t-0.26)/0.12)**4)*(max(0,-s)**8)
                edge_gap=0.055+byssal
                radial=(0.16*max(0,(t-0.16)/0.84)*math.sin(math.pi*s)**0.4
                        if s>0 and s<1 and j%2 else 0.0)
                # Five restrained curved growth folds below median keel.
                growth=sum(0.22*math.exp(-((t-u)/0.006)**2) for u in params['growth_fold_rows'])
                growth*=max(0,-s)**0.45*(1-abs(s))**0.6
                y=edge_gap+(inflated-0.055)*cross+radial+growth
                verts.append((x,sign*y,z))
        # Exterior longitudinal profile loft, no default primitives.
        for j in range(n-1): faces.append((0,1+j,2+j)); indices.append(0)
        for i in range(len(ts)-1):
            for j in range(n-1):
                v0=1+i*n+j
                faces.append((v0,v0+n,v0+n+1,v0+1))
                dark=vs[j]<0 and any(abs(ts[i]-u)<0.009 for u in params['growth_fold_rows'])
                indices.append(1 if dark else 0)
        # Continuous boundary wraps tip -> ventral margin -> posterior -> dorsal.
        boundary=[0]+[1+i*n for i in range(len(ts))]+[1+(len(ts)-1)*n+j for j in range(1,n)]+[1+i*n+n-1 for i in reversed(range(len(ts)-1))]
        inner=[]
        for outer_idx in boundary:
            x,y,z=verts[outer_idx]
            if outer_idx==0: sy=0.025
            else:
                row=(outer_idx-1)//n; col=(outer_idx-1)%n
                t=ts[row]; s=vs[col]
                sy=0.025+0.50*math.exp(-((t-0.26)/0.12)**4)*(max(0,-s)**8)
            inner.append(len(verts)); verts.append((x,sign*sy,z))
        center_idx=len(verts); verts.append((15.0,sign*0.025,17.0))
        for j in range(len(boundary)):
            k=(j+1)%len(boundary)
            faces.append((boundary[j],boundary[k],inner[k],inner[j])); indices.append(2)
            faces.append((center_idx,inner[j],inner[k])); indices.append(2)
        # Dimensions are in mm above for readability, converted numerically to m.
        verts=[tuple(c/1000 for c in xyz) for xyz in verts]
        ob=mesh_object(name,verts,faces,mats,collection)
        for poly,mi in zip(ob.data.polygons,indices): poly.material_index=mi
        ob['anatomy']='inflated valve with longitudinal median keel and eight weak dorsal ribs'
        ob['interior_note']='hidden mathematical closure of fossil-form envelope, not anatomic nacre'
        # Flat facets preserve the median keel. Small rib relief remains geometry.
        bm=bmesh.new(); bm.from_mesh(ob.data)
        volumes=bm.calc_volume(signed=True); boundary_edges=sum(e.is_boundary for e in bm.edges)
        nonmanifold=sum(not e.is_manifold for e in bm.edges); bm.free()
        measures.append({'part':name,'signed_volume_m3':volumes,'boundary_edges':boundary_edges,'nonmanifold_edges':nonmanifold,'vertices':len(verts),'polygons':len(faces)})
        parts.append(ob)
    # Numerically ground and scale to the frozen nominal envelope. This does not
    # infer extra specimen precision: length is the paper's estimated restoration.
    allverts=[v for o in parts for v in o.data.vertices]
    lo=[min(v.co[i] for v in allverts) for i in range(3)]
    hi=[max(v.co[i] for v in allverts) for i in range(3)]
    target=[0.119,0.0196,0.032]
    factors=[target[i]/(hi[i]-lo[i]) for i in range(3)]
    for v in allverts:
        v.co.x=(v.co.x-(hi[0]+lo[0])/2)*factors[0]
        v.co.y=v.co.y*factors[1]
        v.co.z=(v.co.z-lo[2])*factors[2]
    bpy.context.view_layer.update()
    limits=brief['geometry_policy']
    record=export_asset('pinna',brief['name'],'invertebrates',collection,
        metadata={'description':{'en':'Reconstructed Jurassic Pinna (Cyrtopinna) socialis fossil shell form, mainly VTT001-7. Missing pointed end follows Koppka 2018 graphical restoration; not an intact scan.','zh':'依 Koppka 2018 及 VTT001-7 复原的侏罗纪江珧壳体；缺失尖端为图示复原，不是完整标本扫描。'},'generator':'source/generate.py','taxon':brief['taxon'],'sources':[{'title':'Koppka 2018, Pinnidae from the Reuchenette Formation','url':'https://doi.org/10.1515/agp-2017-0027'}],'reconstruction_notes':brief['simplifications']+['Hidden interior closure follows a fossil-form envelope, not inferred original shell-wall thickness.']},
        output_root=out/'private'/'build',render=False,
        max_triangles=limits['max_triangles'],max_materials=limits['max_materials'],max_primitives=limits['max_primitives'])
    generated=out/'private'/'build'/'pinna'
    shutil.copy2(generated/'pinna.glb',out/'model.glb'); shutil.copy2(generated/'pinna.blend',out/'model.blend')
    audit=json.loads((generated/'qa.json').read_text())
    audit['glb']['file']='model.glb'
    if (out/'model.glb').stat().st_size>limits['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
    record.update(glb='model.glb',blend='model.blend',preview='preview.png',generator='source/generate.py',
        axes=brief['coordinates'],origin='lateral silhouette centered in X, paired-valve midplane Y=0, lowest ventral edge Z=0',
        source_hash=sha(HERE/'generate.py'),params_hash=sha(HERE/'params.json'),brief_hash=sha(HERE.parent/'brief.json'),references_hash=sha(HERE.parent/'references.json'),
        seed=params['seed'],profile='static untextured low-poly fossil envelope',exporter_version='4.3.47',threejs_consuming_version='0.180.0',
        reconstruction_scale=brief['scale'],glb_bytes=(out/'model.glb').stat().st_size)
    save(out/'qa/evidence/build-metadata.json',record)
    save(out/'qa/evidence/source-and-glb.json',audit)
    # Separate geometric measurements from scientific/visual acceptance.
    geom={'glb_sha256':sha(out/'model.glb'),'method':'source mesh manifold, signed volume, declared profile and local gap inspection; exact export bounds separately checked by qa_glb',
          'parts_before_final_dimension_scaling':measures,'positive_dimension_scale_factors':factors,
          'paired_valves':2,'radial_ribs_per_dorsal_half':8,'ventral_growth_fold_count':len(params['growth_fold_rows']),
          'nominal_dimensions_m':target,'source_measurements_after_scaling':audit['source']['bounds_blender_m'],
          'byssal_gape':{'anterior_t_center':0.26,'at':'ventral meeting edge','maximum_model_gap_m':1.05*factors[1]/1000,'method':'paired inner boundary vertices separated along Y; no decorative stripe'},
          'dorsal_meeting_seam_m':0.05*factors[1]/1000,'anterior_angle_deg_first30percent':math.degrees(math.atan((31.65-lerp(0.30,params['ventral_profile_mm']))/(119*0.30))),
          'interior_geometry':'Two closed fossil-envelope solids. Mating surfaces are mathematical closures, not reconstructed shell wall/nacre anatomy.',
          'surface_self_intersection':'Not established by numeric volume; ordered loft geometry inspected by maker. Independent review pending.',
          'visual_and_factual_status':'pending independent review'}
    save(out/'qa/evidence/geometry.json',geom)
    print(json.dumps({'status':'BUILT_NOT_INDEPENDENTLY_ACCEPTED','glb_sha256':sha(out/'model.glb'),'triangles':audit['glb']['scene_triangles'],'primitives':audit['glb']['scene_primitives_estimated_base_draw_calls'],'bytes':(out/'model.glb').stat().st_size}))

if __name__=='__main__': main()
