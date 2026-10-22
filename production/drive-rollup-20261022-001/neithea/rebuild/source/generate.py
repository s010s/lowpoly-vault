#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Neithea fossil-form asset; no imported imagery or meshes.
Run: blender -b -t 2 --python-exit-code 1 --python generate.py -- --config params.json --output-root ../artifacts
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent/'deps'))
import bpy
from asset_common import setup_scene, make_material, mesh_object, export_asset

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser(); ap.add_argument('--config',required=True,type=Path); ap.add_argument('--output-root',required=True,type=Path)
    args=ap.parse_args(argv); p=json.loads(args.config.read_text())
    if bpy.app.version_string!=p['blender_version']: raise RuntimeError('Pinned Blender version mismatch: '+bpy.app.version_string)
    col=setup_scene(p['asset_id'],p['seed'])
    mats=[make_material(n,c,roughness=.92) for n,c in zip(['Warm limestone','Pale stone planes','Ochre stone planes','Exposed rib stone','Weathered margin'],p['palette_srgb'])]
    nq=p['angular_segments']; nr=p['radial_segments']; H=p['height_m']; W=p['width_m']; peaks=p['primary_rib_q']
    verts=[]; faces=[]; semantic=[]; grid={}; vertex_tags={}; radii=sorted([(i/nr)**1.04 for i in range(1,nr+1)]+p['umbo_extra_rows']); nr=len(radii)
    # One closed continuous envelope: front = deep right valve; back = flat left valve.
    # Shared perimeter avoids overlapping hidden caps and detached shell fragments.
    verts.append((0,p['umbo_tip_y_m'],H-p['umbo_tip_drop_m'])); vertex_tags[0]=('umbo',0,0)
    def lerp_knots(t,knots):
        for (ta,a),(tb,b) in zip(knots,knots[1:]):
            if ta<=t<=tb: return a+(b-a)*(t-ta)/(tb-ta)
        return knots[-1][1]
    crown_t=(1/p['radial_segments'])**1.04
    def lobes(q): return sum(math.exp(-((q-c)/.081)**2) for c in peaks)
    def pos(t,q,side):
        rib=lobes(q)
        # Pear/fan silhouette, curved distal edge; modest uneven ears only near hinge.
        xe=W*.5*math.sin(q*math.pi/2)
        ze=.00036+.00735*abs(q)**2.18-.00034*rib
        x=(t+t*t*(1-t)*abs(q)**5)*xe
        x+=math.copysign(1,q)*(.00052 if q<0 else .00036)*math.exp(-((t-.20)/.105)**2)*abs(q)**12 if q else 0
        z=H+t*(ze-H)
        # r003: bend only the upper <=20% into a modest inward/downward beak.
        # Crown is above a lowered tip, giving visible curvature rather than merely a seam offset.
        # No exact hinge dimensions are claimed; the lower accepted shell remains unchanged.
        seam=.00035*(1-t)**4
        if t<.20:
            seam=lerp_knots(t,[(0,p['umbo_tip_y_m']),(.025,.00100),(crown_t,.00060),(.085,.00034),(.125,.00018),(.20,.00035*.80**4)])
            raw_z=z
            crown_z=H-.00025*abs(q)**1.8-(.00010*max(0,math.cos(q*math.pi/2)) if side=='left' else 0)
            second_z=H-.00022-.00020*abs(q)**1.8-(.00010*max(0,math.cos(q*math.pi/2)) if side=='left' else 0)
            target_z=lerp_knots(t,[(0,H-p['umbo_tip_drop_m']),(.025,H-.00020-.00018*abs(q)**1.8),(crown_t,crown_z),(.085,second_z),(.125,H-.00110+.00045*abs(q)**1.8),(.20,H+.20*(ze-H))])
            z=target_z
        across=max(0,math.cos(q*math.pi/2))**.65
        bulb=math.sin(math.pi*t)**.86*across
        if side=='right':
            y=seam-p['right_valve_depth_m']*bulb-p['rib_relief_m']*math.sin(math.pi*t)**.72*rib*across
            # Very subordinate intercalary relief; primary rib count remains six.
            y-=.000045*bulb*(.5+.5*math.cos(36*math.pi*q))
            y+=.000018*bulb*math.sin(t*24+q*8)*math.sin(q*25-t*7)
        else:
            y=seam+p['left_valve_depth_m']*bulb+.000065*math.sin(math.pi*t)**.86*rib*across
        return (x,y,z)
    for side in ('right','left'):
        for r,t in enumerate(radii,1):
            for j in range(nq+1):
                q=-1+2*j/nq
                # Weld both valve outlines exactly. The two surfaces have no interior cap.
                if side=='left' and (j in (0,nq) or r==nr):
                    grid[(side,r,j)]=grid[('right',r,j)]; continue
                idx=len(verts); verts.append(pos(t,q,side)); grid[(side,r,j)]=idx; vertex_tags[idx]=(side,t,q)
        for j in range(nq):
            tri=(0,grid[(side,1,j)],grid[(side,1,j+1)])
            faces.append(tri if side=='right' else tri[::-1]); semantic.append((side,radii[0]*.5,-1+(j+.5)*2/nq))
        for r in range(1,nr):
            for j in range(nq):
                a,b,c,d=(grid[(side,r,j)],grid[(side,r+1,j)],grid[(side,r+1,j+1)],grid[(side,r,j+1)])
                # Alternating explicit triangulation, deterministic and fully editable.
                pair=((a,b,c),(a,c,d)) if (r+j)%2 else ((a,b,d),(b,c,d))
                # At the two distal corners, avoid a triangle made entirely of welded seam vertices.
                if r==nr-1 and j==0: pair=((a,b,d),(b,c,d))
                if r==nr-1 and j==nq-1: pair=((a,b,c),(a,c,d))
                for tri in pair:
                    faces.append(tri if side=='right' else tri[::-1]); semantic.append((side,(radii[r-1]+radii[r])*.5,-1+(j+.5)*2/nq))
    # Match measured 15 mm height, 12.2 mm width exactly after ruffled edge and ear completion.
    lo=[min(v[i] for v in verts) for i in range(3)]; hi=[max(v[i] for v in verts) for i in range(3)]
    verts=[((x-(lo[0]+hi[0])/2)*W/(hi[0]-lo[0]),y,(z-lo[2])*H/(hi[2]-lo[2])) for x,y,z in verts]
    obj=mesh_object('Neithea paired valve envelope',verts,faces,mats,col)
    for poly,(side,t,q) in zip(obj.data.polygons,semantic):
        # Broad low-contrast stone regions, not a photographic texture or tiny color noise.
        region=math.sin(7*q+6*t)+.5*math.cos(10*t-3*q)
        idx=1 if region>.65 else 2 if region<-.85 else 0
        if t>.94: idx=4 if side=='left' else 2
        if side=='right' and lobes(q)>.82 and t>.20: idx=3 if region>.0 else 1
        poly.material_index=idx
    for name in ('right_convex_valve','left_flat_valve','umbo_and_hinge'):
        vg=obj.vertex_groups.new(name=name)
        ids=[i for i,(side,t,q) in vertex_tags.items() if (name=='right_convex_valve' and side=='right') or (name=='left_flat_valve' and side=='left') or (name=='umbo_and_hinge' and t<.22)]
        if ids: vg.add(ids,1,'REPLACE')
    for k,c in enumerate(peaks,1):
        vg=obj.vertex_groups.new(name=f'primary_rib_{k:02d}')
        ids=[i for i,(side,t,q) in vertex_tags.items() if side=='right' and abs(q-c)<.09]
        if ids: vg.add(ids,1,'REPLACE')
    obj['design']='Six major radial ribs; deep right and shallow left valves; continuous closed envelope.'
    obj['uncertainty']='Depth, articulated pairing, hinge completion and color are artistic, not measurements.'
    root=bpy.data.objects[col['asset_root']]; root['mounting']='Upright fossil display; lower rim at Z=0, hinge plane center at X=Y=0. Not a natural-life pose.'
    # Record exact input/runtime identity in source, independent of output directory.
    scene=bpy.context.scene; scene['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(); scene['config_sha256']=hashlib.sha256(args.config.read_bytes()).hexdigest()
    metadata={'description':{'en':'Original low-poly Neithea grandicosta-informed fossil shell, with six main ribs, a convex right valve and a flatter left valve. Pairing, thickness and color are artistic.','zh':'参考 Neithea grandicosta 的原创低多边形化石壳：六条主肋、右壳深凸、左壳较平。配壳、厚度和色彩为艺术补全。'},'generator':'source/generate.py','config':'source/params.json','scientific_scope':p['scientific_scope'],'artistic_choices':p['artistic_choices'],'reference_size_m':{'height':H,'width':W,'source':'CASG 71190 right valve, Iba et al. 2011 Table 1; paired left valve is not the same individual'},'sources':[{'url':'https://doi.org/10.2517/1342-8144-15.2.062','title':'Iba, Sano & Tanabe (2011), Paleontological Research 15(2):62–67'},{'url':'https://www.palaeo-soc-japan.jp/publications/92%20Friends%20of%20Fossils.pdf','title':'Iba, Sano & Tanabe illustrated explanation, 化石 92 (2012), p.31'}],'mounting':'Upright museum-display shell; minimum rim Z=0; root identity at hinge-plane center; no substrate','primary_rib_count':6,'three_version':p['three_version'],'surface_profile':'palette-only','normal_style':'deliberate flat facets','generator_sha256':scene['generator_sha256'],'config_sha256':scene['config_sha256']}
    rec=export_asset('neithea',{'en':'Neithea fossil shell','zh':'Neithea 化石壳'},'animals',col,metadata=metadata,output_root=args.output_root,render=False,max_triangles=p['max_triangles'],max_materials=p['max_materials'],max_primitives=p['max_primitives'])
    if rec['glb_bytes']>p['max_glb_bytes']: raise RuntimeError('GLB byte budget exceeded')
    print('NEITHEA_BUILD_COMPLETE',json.dumps({'triangles':rec['triangles'],'bytes':rec['glb_bytes'],'dimensions':rec['dimensions'],'sha256':rec['sha256']}))
if __name__=='__main__': main()
