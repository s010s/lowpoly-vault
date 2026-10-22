#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original curved, chevron-ribbed closed Rastellum-form shell. No external geometry or imagery used."""
import argparse,hashlib,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset

def interp(x,knots):
    for (a,va),(b,vb) in zip(knots,knots[1:]):
        if a<=x<=b:return va+(vb-va)*(x-a)/(b-a)
    return knots[0][1] if x<knots[0][0] else knots[-1][1]

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--config',type=Path,required=True);ap.add_argument('--output-root',type=Path,required=True);a=ap.parse_args(argv)
    p=json.loads(a.config.read_text());assert bpy.app.version_string==p['blender_version']
    col=setup_scene('rastellum',p['seed'])
    mats=[make_material(n,c,roughness=.94) for n,c in zip(['Stone shell','Pale ridge planes','Quiet tan planes','Recessed closed commissure'],p['palette_srgb'])]
    ribknots=[(0,0),(.055,0)]
    for i,(s,strength) in enumerate(zip(p['rib_stations'],p['rib_strengths'])):
        if i:ribknots.append(((p['rib_stations'][i-1]+s)*.5,-.75*(p['rib_strengths'][i-1]+strength)*.5))
        ribknots.append((s,strength))
    ribknots.extend([(.97,0),(1,0)])
    # Every rib crest and trough has a topology row; shoulders keep deliberate large planes.
    rows=sorted(set([.016,.034,.976,.992]+[v[0] for v in ribknots if 0<v[0]<1]+[(a[0]+b[0])/2 for a,b in zip(ribknots,ribknots[1:]) if a[0]>0 and b[0]<1]))
    cross=p['cross_sections'];n=len(cross);ring_n=2*n+2
    def station(s,u):
        # Bifurcating V ribs lean toward the growing end from a real raised central keel.
        q=s+p['branch_offset']*abs(u)*math.sin(math.pi*s)
        return max(0,min(1,q))
    def xyz(s,u,side):
        q=station(s,u);x=.070*(q-.5)
        y=p['bend_m']*math.sin(math.pi*q)-.006
        dx=.070;dy=p['bend_m']*math.pi*math.cos(math.pi*q);d=math.hypot(dx,dy)
        nx,ny=-dy/d,dx/d
        w=interp(q,p['width_knots'])*(1+.025*interp(s,ribknots)*abs(u))
        wave=interp(s,ribknots);env=math.sin(math.pi*q)**.58
        seam=p['fold_amplitude_m']*wave*(.30+.70*abs(u)**.9)
        # Unlike the concept image, the entire valve is convex across the keel, never canoe-concave.
        if side=='upper':
            dome=p['upper_height_m']*env*(1-abs(u)**.83)
            z=dome+seam+p['seam_lip_halfheight_m']
        elif side=='lower':
            dome=p['lower_height_m']*env*(1-abs(u)**1.24)*(1+.075*u)
            z=-dome+seam-p['seam_lip_halfheight_m']
        else:
            # Continuous inward bevel rather than an open slit or inserted tooth strip.
            w=max(0,w-.00011*env);z=seam
        return (x+nx*u*w,y+ny*u*w,z)
    verts=[];groups={'convex_keel_valve':[],'shallower_reverse_valve':[],'closed_zigzag_commissure':[],'quiet_hinge_zone':[]}
    for s in rows:
        for u in cross:
            groups['convex_keel_valve'].append(len(verts));verts.append(xyz(s,u,'upper'))
        groups['closed_zigzag_commissure'].append(len(verts));verts.append(xyz(s,1,'seam'))
        for u in reversed(cross):
            groups['shallower_reverse_valve'].append(len(verts));verts.append(xyz(s,u,'lower'))
        groups['closed_zigzag_commissure'].append(len(verts));verts.append(xyz(s,-1,'seam'))
        if s<.085:groups['quiet_hinge_zone'].extend(range(len(verts)-ring_n,len(verts)))
    faces=[];face_mats=[]
    for ri in range(len(rows)-1):
        s=(rows[ri]+rows[ri+1])/2
        for j in range(ring_n):
            k=(j+1)%ring_n
            faces.append((ri*ring_n+j,(ri+1)*ring_n+j,(ri+1)*ring_n+k,ri*ring_n+k))
            seam_face=j in (n-1,n,2*n,2*n+1)
            if seam_face:mat=3
            elif s<.08:mat=0
            elif j in (3,4,5,6) and interp(s,ribknots)>.18:mat=1
            elif (j<3 or j>2*n-3) and s>.25:mat=2
            else:mat=0
            face_mats.append(mat)
    # Terminal poles are unique vertices, avoiding degenerate collapsed UV-grid rows.
    for which,s,ri in [('hinge',0,0),('growth',1,len(rows)-1)]:
        pole=len(verts);verts.append((.070*(s-.5),-.006,0))
        for j in range(ring_n):
            faces.append((pole,ri*ring_n+j,ri*ring_n+(j+1)%ring_n));face_mats.append(0)
        if which=='hinge':groups['quiet_hinge_zone'].append(pole)
    obj=mesh_object('Articulated shell - continuous unequal valves',verts,faces,mats,col)
    for f,mi in zip(obj.data.polygons,face_mats):f.material_index=mi
    for name,ids in groups.items():obj.vertex_groups.new(name=name).add(ids,1,'REPLACE')
    obj['construction']='One closed watertight shell with two semantic valve surfaces and a recessed continuous complementary seam; no floating tooth objects or hidden inner caps.'
    obj['scientific_scope']=p['claim_scope']
    obj['hinge']='Quiet terminal completion is artistic; no invented internal hinge teeth or scars.'
    shift=ground_asset(col,center_xy=True)
    meta={'description':{'en':'Rastellum comb-edged oyster: original curved narrow, keeled and V-ribbed closed fossil-form study informed by R. carinatum.','zh':'Rastellum 梳缘牡蛎类：参考 R. carinatum 的长弯窄壳、中央脊和 V 形分叉肋的原创闭合化石形态研究。'},'generator':'source/generate.py','revision':p['revision'],'scientific_scope':p['claim_scope'],'scale_note':'70 x 28 x 20 mm approximate artist envelope, not specimen measurement. No use of mould C-prime as articulated depth.','orientation_note':'Blender X is long axis, hinge at -X, broad convex valve +Z; -Y front is long concave commissural edge. Ground origin is a display pose, not life reconstruction.','surface_profile':'palette-only static low-poly','reconstruction_notes':['Complete pair is genus-level art, not replica of fragmentary RGF VR35/33.','The paper material/caption conflict on right versus left valve is unresolved. No handedness assigned.','Median keel and bifurcating V ribs informed by Fig7 H/I; museum photographs inform curved shell only.','Exact hidden reverse, pair thickness, hinge completion, rib count, scale and palette are artistic choices.'],'sources':[{'title':'Radulović et al. 2019, Fig7 H/I','url':'https://doi.org/10.1016/j.cretres.2019.07.005'},{'title':'Clemson BCGM10590','url':'https://digitalcollections.clemson.edu/single-item-view/?oid=CUIR:B91CEA18233DA5243C219920FD3BA121'}]}
    rec=export_asset('rastellum',{'en':'Rastellum comb-edged oyster','zh':'Rastellum（梳缘牡蛎类）'},'animals',col,metadata=meta,output_root=a.output_root,render=False,max_triangles=p['budget']['max_triangles'],max_materials=4,max_primitives=4)
    metrics={'rows':len(rows),'ring_vertices':ring_n,'primary_rib_groups':10,'mesh_objects':1,'semantic_valves':2,'ground_shift':list(shift) if shift else None,'dimensions_blender_m':rec['blender_dimensions_m'],'triangles':rec['triangles'],'glb_bytes':rec['glb_bytes'],'glb_sha256':rec['sha256']['glb'],'config_sha256':hashlib.sha256(a.config.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (a.output_root/'build-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics))
if __name__=='__main__':main()
