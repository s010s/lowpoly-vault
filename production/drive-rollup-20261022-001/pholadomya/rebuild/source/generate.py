#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Pholadomya fossil-form geometry, not a reference mesh conversion."""
import argparse, hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / 'deps'))
import bpy, bmesh
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, ground_asset, export_asset


def bezier(a, b, c, d, t):
    s = 1-t
    return tuple(s*s*s*a[k]+3*s*s*t*b[k]+3*s*t*t*c[k]+t*t*t*d[k] for k in (0, 1))


def smoothstep(t):
    t=max(0,min(1,t)); return t*t*(3-2*t)


def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser(); ap.add_argument('--config',type=Path,required=True)
    ap.add_argument('--output-root',type=Path,required=True); a=ap.parse_args(argv)
    p=json.loads(a.config.read_text()); assert bpy.app.version_string==p['blender_version']
    col=setup_scene('pholadomya',p['seed'])
    mats=[make_material(n,c,roughness=.94) for n,c in zip(['Neutral fossil exterior','Inferred inner shell'],p['palette_srgb'])]
    boundary=[]
    for seg in p['outline_beziers_mm']:
        for j in range(seg[4]): boundary.append(bezier(*seg[:4],j/seg[4]))
    n=len(boundary); rings=p['radial_rings']; cx,cz=p['umbo_center_mm']
    source_reports=[]
    for label,sign,inflation_ratio in [('Left valve',1,p['left_inflation_ratio']),('Right valve',-1,1)]:
        verts=[]; faces=[]; groups={}; ring_ids=[]
        # A star-shaped, asymmetric side profile is swept out from the near-anterior umbo.
        # All ribs displace this one surface; no detached rib tubes or ornaments.
        for r in rings:
            row=[]
            for j,(bx,bz) in enumerate(boundary):
                x=cx+r*(bx-cx)
                z=cz+r*(bz-cz)
                gape=p['rim_half_gap_mm']+p['posterior_additional_half_gape_mm']*smoothstep((bx-61)/29)
                height=p['inflation_mm']*max(0,1-r*r)**.62*(.68+.32*math.sin(math.pi*r))
                # The upper lip folds toward the paired umbones, rather than a fan-shaped planar plate.
                height*=1-.08*max(0,(bz-cz)/8)
                height*=inflation_ratio
                sweeping_phase=j+p['rib_curvature_boundary_units']*math.sin(math.pi*r)
                rib=0
                for k,center in enumerate(p['rib_end_boundary_indices']):
                    d=abs((sweeping_phase-center+n/2)%n-n/2)
                    if d<p['rib_width_boundary_units']:
                        strength=1 if 2<=k<=6 else .72
                        rib+=strength*math.cos(d/p['rib_width_boundary_units']*math.pi/2)**2
                envelope=smoothstep(r/.22)*(.55+.45*math.sin(math.pi*r))
                relief=p['rib_relief_mm']*rib*envelope
                growth=p['growth_relief_mm']*math.sin(r*math.pi*14)*math.sin(math.pi*r)**2
                y=height+gape*r**4+relief+growth
                row.append(len(verts)); verts.append((x*.001,sign*y*.001,z*.001))
            ring_ids.append(row)
        pole=len(verts); verts.append((cx*.001,sign*p['inflation_mm']*.68*inflation_ratio*.001,cz*.001))
        for j in range(n): faces.append((pole,ring_ids[0][j],ring_ids[0][(j+1)%n]))
        for k in range(len(rings)-1):
            for j in range(n): faces.append((ring_ids[k][j],ring_ids[k+1][j],ring_ids[k+1][(j+1)%n],ring_ids[k][(j+1)%n]))
        if sign<0: faces=[tuple(reversed(f)) for f in faces]
        # Keep outer and inner surfaces as strictly ordered graphs over the same
        # injective XZ disk. This avoids inward normal offsets folding at the umbo.
        # Shell thickness is lateral-axis separation, not claimed normal thickness.
        outer_count=len(verts); outer_faces=len(faces); outer_rim=ring_ids[-1]
        thicknesses=[]
        for v in list(verts):
            thickness=min(p['shell_thickness_mm']*.001,v[1]*sign-.00008)
            assert thickness>0
            thicknesses.append(thickness)
            verts.append((v[0],v[1]-sign*thickness,v[2]))
        inner_faces=[tuple(outer_count+i for i in reversed(f)) for f in faces]
        faces+=inner_faces
        for j in range(n):
            q=outer_rim[j]; r=outer_rim[(j+1)%n]
            faces.append((q,r,outer_count+r,outer_count+q))
        obj=mesh_object(label,verts,faces,mats,col)
        for i,face in enumerate(obj.data.polygons): face.material_index=1 if outer_faces<=i<2*outer_faces else 0
        for name,ids in [('Exterior with swept radial ribs',list(range(outer_count))),('Inferred inner cavity surface',list(range(outer_count,2*outer_count))),('Posterior natural gape lip',[i for i in outer_rim if verts[i][0]>.066]),('Anterior umbo',[pole]+[i for row in ring_ids[:3] for i in row])]:
            obj.vertex_groups.new(name=name).add(ids,1,'REPLACE')
        obj['construction']='A separately closed, manifold volumetric valve with geometric ribs, a parameterized inner cavity surface and a real rim. No duplicate rib objects.'
        obj['scientific_scope']=p['claim_scope']; obj['unseen_inner_surface']='Artistic interpolation. No internal hinge teeth or soft body reconstructed.'
        bm=bmesh.new(); bm.from_mesh(obj.data); volume=bm.calc_volume(signed=True)
        edges={'boundary':sum(e.is_boundary for e in bm.edges),'nonmanifold':sum(not e.is_manifold for e in bm.edges),'wire':sum(e.is_wire for e in bm.edges)}
        bm.free(); assert volume>0 and not any(edges.values()), (label,volume,edges)
        source_reports.append({'name':label,'vertices':len(verts),'faces':len(faces),'signed_volume_m3':volume,'edges':edges,'lateral_thickness_range_m':[min(thicknesses),max(thicknesses)],'midplane_clearance_m':min(v[1]*sign for v in verts)})
    # Set the stated artistic maximum length exactly while preserving all other inferred dimensions.
    all_x=[v.co.x for o in col.objects if o.type=='MESH' for v in o.data.vertices]
    span=max(all_x)-min(all_x); scale_x=p['nominal_maximum_length_m']/span
    for obj in col.objects:
        if obj.type=='MESH':
            for v in obj.data.vertices: v.co.x*=scale_x
    ground_asset(col,center_xy=True)
    for name,body in [('generate.py',Path(__file__).read_text()),('params.json',a.config.read_text())]: bpy.data.texts.new(name).write(body)
    rec=export_asset('pholadomya',{'en':'Pholadomya gaping ribbed fossil bivalve','zh':'Pholadomya 开口肋双壳类化石'},'animals',col,
        metadata={'description':{'en':'Original elongated inflated paired fossil shell with continuous sweeping radial ribs and a natural posterior opening, informed by P. lirata.','zh':'依据 P. lirata 实图制作的长膨双壳化石形态，具有连续弯放射肋和真实后端开口。'},'generator':'source/generate.py','revision':p['revision'],'scientific_scope':p['claim_scope'],
        'scale_note':'Maximum length 0.090 m is a nominal artistic scale, not a transcribed specimen measurement. Height, inflation, thickness and gape width are inferred.','orientation_note':'Blender +X posterior, -X anterior, Y valve depth, +Z dorsal. Anatomical side camera -Y; posterior camera +X. Grounded museum pose, not a life position.',
        'reconstruction_notes':['Two separately manifold shell solids; assembly is intentionally open at posterior.','Sztajner 2020 Figure 12D supports the side form; Figure 1D/E supports cross-specimen paired shape. Fossil compaction alters observed gape.','No exact single-specimen reconstruction or original shell color claim.','Unseen interior, shell thickness, total size and exact gape are artistic interpolation.','No soft tissue, siphon, pearl or invented hinge teeth. Fine growth sculpture is deliberately simplified.','Figure 1H/I and other species are excluded; source photographs are not model textures.'],
        'sources':[{'id':'S1','title':'Sztajner 2020, The Mode of Life in the Genus Pholadomya as Inferred from the Fossil Record, Figures 12D and 1D/E','url':'https://www.mdpi.com/2076-3263/10/10/397','doi':'10.3390/geosciences10100397'}]},output_root=a.output_root,render=False,max_triangles=p['budget']['max_triangles'],max_materials=2,max_primitives=4)
    out=a.output_root/'pholadomya'
    (out/'source-geometry-selfcheck.json').write_text(json.dumps({'status':'pass','scope':'Maker measured source topology and explicit shell construction, not independent review.','valves':source_reports,'longitudinal_scale_correction':scale_x,'valve_intersections':'Excluded by strict opposite signed Y halfspaces before shared centering. Each halfspace clearance is above zero.','bound_dimensions_blender_m':rec['blender_dimensions_m']},indent=2)+'\n')
    metrics={'glb_sha256':rec['sha256']['glb'],'triangles':rec['triangles'],'glb_bytes':rec['glb_bytes'],'dimensions_blender_m':rec['blender_dimensions_m'],'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'params_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest()}
    (a.output_root/'build-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n'); print(json.dumps(metrics))


if __name__=='__main__': main()
