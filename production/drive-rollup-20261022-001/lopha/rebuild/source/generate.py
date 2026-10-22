#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Original Actinostreon-informed Lopha fossil-form. No image, scan or external mesh input."""
import argparse, hashlib, json, math, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from asset_common import setup_scene,make_material,mesh_object,export_asset

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser(); ap.add_argument('--config',type=Path,required=True); ap.add_argument('--output-root',type=Path,required=True); a=ap.parse_args(argv)
    p=json.loads(a.config.read_text()); assert bpy.app.version_string==p['blender_version']
    col=setup_scene('lopha',p['seed'])
    mats=[make_material(n,c,roughness=.94) for n,c in zip(['Warm grey shell','Pale fold planes','Muted attachment stone','Earth toned shell'],p['palette_srgb'])]
    # The outline and angular sampling are original parametric design, not traced.
    peaks=p['fold_angles']; strengths=p['fold_strengths']
    wave_knots=[(-math.pi,0.)]
    for i,(theta,s) in enumerate(zip(peaks,strengths)):
        if i==0: wave_knots.append((theta-.18,-.28))
        else: wave_knots.append(((peaks[i-1]+theta)/2,-.68*(strengths[i-1]+s)/2))
        wave_knots.append((theta,s))
    wave_knots.extend([(peaks[-1]+.19,-.20),(math.pi,0.)])
    # Sample every peak, trough and shoulder: clean angular facets resolve folded margin.
    angles=[]
    for (t0,v0),(t1,v1) in zip(wave_knots,wave_knots[1:]):
        angles.extend([t0,t0+(t1-t0)*.5])
    n=len(angles); rows=p['radial_rows']; nr=len(rows)
    def interp(t,knots):
        for (t0,v0),(t1,v1) in zip(knots,knots[1:]):
            if t0<=t<=t1:return v0+(v1-v0)*(t-t0)/(t1-t0)
        return knots[-1][1]
    def smooth(a,b,x):
        t=max(0,min(1,(x-a)/(b-a))); return t*t*(3-2*t)
    def attach_radius(t):
        return interp(t,p['attachment_boundary_knots'])
    def point(r,t,side):
        # Broad dorsal attached sheet, not an elliptical radial hub. Its irregular
        # lower boundary is original and continues to the quiet dorsal margins.
        wave=interp(t,wave_knots); rad=interp(t,p['outline_knots'])
        attach=attach_radius(t)
        chart_r=r
        boundary=p['attachment_chart_boundary']
        # Align a complete topology ring to the irregular attachment boundary.
        # This avoids the stair-step teeth produced by crossing a fixed radial grid.
        r=(chart_r/boundary*attach) if chart_r<=boundary else (attach+(chart_r-boundary)/(1-boundary)*(1-attach))
        delay=interp(t,[(-math.pi,.08)]+list(zip(peaks,p['fold_onset_offsets']))+[(math.pi,.08)])
        ridge_start=attach+delay if side=='left' else max(.12,attach-.16+delay)
        onset=smooth(ridge_start,ridge_start+.13,r)
        # The outer commissure uses one identical wave on both valves. Different
        # onsets are internal to each valve and blend into the shared edge.
        edge_wave=p['fold_relief_m']*wave*r**1.15
        corr=edge_wave*onset
        seam=-corr+.0005*math.sin(1.3*t+.4)*r*r
        if chart_r>=p['radial_rows'][-2]:
            seam=-edge_wave+.0005*math.sin(1.3*t+.4)*r*r
        radius_factor=r*(1+.020*wave*onset)
        if chart_r==rows[-2]:radius_factor=1.015*(1+.020*wave)
        if chart_r==1:radius_factor=.994*(1+.020*wave)
        x=-.003+math.sin(t)*rad*radius_factor
        z=.043-math.cos(t)*rad*radius_factor
        x+=.0013*math.sin(t*.8)*r*(1-r)
        if side=='left':
            # A nearly planar asymmetric attached face bends sharply away into
            # the ribbed apron. No crater, decorative slab or copied damage.
            attached_y=-p['front_depth_m']-.055*(z-.043)+.035*x
            # Two broad low-relief bends make the attached face quiet shell, not
            # a geometrically perfect cut plane or a textured rock surface.
            attached_y+=.00080*abs((x+.003)/.025)+.00045*abs((z-.035)/.022)
            if r<=attach:
                y=attached_y
            else:
                u=(r-attach)/(1-attach)
                return_fraction=interp(u,p['free_shell_depth_profile'])
                y=attached_y*(1-return_fraction)+seam
        else:
            # Preserve the shallow counterpart; only its fold hierarchy changes.
            dome=max(0,1-r**2.8)**.86
            y=seam+p['reverse_depth_m']*dome
        if chart_r==rows[-2]:y=seam+(-1 if side=='left' else 1)*p['seam_lip_m']
        if chart_r==1:y=seam
        return x,y,z
    verts=[point(0,0,'left'),point(0,0,'right')]; faces=[]; tags=[]; vidtags={0:('left',0,0),1:('right',0,0)}; grid={}
    for side,center in [('left',0),('right',1)]:
        for ri,r in enumerate(rows):
            for j,t in enumerate(angles):
                if side=='right' and ri==nr-1:grid[side,ri,j]=grid['left',ri,j];continue
                idx=len(verts);verts.append(point(r,t,side));grid[side,ri,j]=idx;vidtags[idx]=(side,r,t)
        for j,t in enumerate(angles):
            k=(j+1)%n; tri=(center,grid[side,0,j],grid[side,0,k]);faces.append(tri);tags.append((side,rows[0]/2,t))
        for ri in range(nr-1):
            for j,t in enumerate(angles):
                k=(j+1)%n;a0,b0,c0,d0=grid[side,ri,j],grid[side,ri+1,j],grid[side,ri+1,k],grid[side,ri,k]
                pair=((a0,b0,c0),(a0,c0,d0)) if (ri+j)%2 else ((a0,b0,d0),(b0,c0,d0))
                for tri in pair:faces.append(tri);tags.append((side,(rows[ri]+rows[ri+1])/2,t))
    # Physical envelope at reference scale, no display-unit normalization.
    low=[min(v[i] for v in verts) for i in range(3)]; high=[max(v[i] for v in verts) for i in range(3)]
    verts=[((v[0]-(low[0]+high[0])/2)*p['width_m']/(high[0]-low[0]),v[1]*p['depth_target_m']/(high[1]-low[1]),(v[2]-low[2])*p['height_m']/(high[2]-low[2])) for v in verts]
    obj=mesh_object('Lopha complete paired oyster shell',verts,faces,mats,col)
    for poly,(side,r,t) in zip(obj.data.polygons,tags):
        region=math.sin(t*2.4+r*4.3)+.35*math.cos(t*4-r*6)
        idx=1 if region>.85 else 3 if region<-.9 else 0
        if side=='left' and r<=p['attachment_chart_boundary']:idx=0
        if r>.975:idx=2
        poly.material_index=idx
    for name,select in [('left_deep_valve',lambda s,r,t:s=='left'),('right_shallow_valve',lambda s,r,t:s=='right'),('broad_attachment_area',lambda s,r,t:s=='left' and r<=p['attachment_chart_boundary']),('zigzag_commissure',lambda s,r,t:r>.95)]:
        group=obj.vertex_groups.new(name=name);ids=[i for i,(s,r,t) in vidtags.items() if select(s,r,t)];group.add(ids,1,'REPLACE')
    for i,theta in enumerate(peaks,1):
        group=obj.vertex_groups.new(name=f'primary_fold_{i:02d}');ids=[j for j,(s,r,t) in vidtags.items() if abs(t-theta)<.14 and r>.3];group.add(ids,1,'REPLACE')
    obj['design']='One closed paired shell; broad irregular dorsal attachment sheet bent into an unequal folded apron, with a shared geometric zigzag commissure.'
    obj['scope']=p['scientific_scope'];obj['primary_folds']=len(peaks)
    root=bpy.data.objects[col['asset_root']];root['mounting']='Upright museum display; ventral margin grounded; broad attached left valve faces -Y; no substrate.'
    scene=bpy.context.scene;scene['generator_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();scene['config_sha256']=hashlib.sha256(a.config.read_bytes()).hexdigest()
    meta={'description':{'en':'Original low-poly folded oyster fossil form, historically called Lopha, informed by Actinostreon marshii. Unequal complete valves, broad attachment region, irregular radial folds and a geometric zigzag commissure.','zh':'历史名称 Lopha 的原创低多边形折缘牡蛎化石形态，参考 Actinostreon marshii：不等双壳、宽附着区、不规则放射褶与几何锯齿接缝。'},'generator':'source/generate.py','config':'source/params.json','scientific_scope':p['scientific_scope'],'artistic_choices':p['artistic_choices'],'reference_size_m':{'height':.0557,'length':.0582,'source':'BSPG 2015 XIII 1; Fürsich et al. 2019 p152'},'sources':[{'url':'https://www.zobodat.at/pdf/Zitteliana-A-B_93_0143-0204.pdf','title':'Fürsich et al. 2019, p152 and Plate 2 Fig.11'}],'mounting':root['mounting'],'primary_fold_count':15,'three_version':p['three_version'],'surface_profile':'palette-only','normal_style':'deliberate flat angular folds','generator_sha256':scene['generator_sha256'],'config_sha256':scene['config_sha256']}
    result=export_asset('lopha',{'en':'Lopha folded-margin oyster · Actinostreon-informed','zh':'Lopha 折缘牡蛎 · 参考 Actinostreon'},'animals',col,metadata=meta,output_root=a.output_root,render=False,max_triangles=p['max_triangles'],max_materials=p['max_materials'],max_primitives=p['max_primitives'])
    assert result['glb_bytes']<=p['max_glb_bytes']
    (a.output_root/'build-metrics.json').write_text(json.dumps({'angular_samples':n,'radial_rows':nr,'triangles':result['triangles'],'dimensions_glb_m':result['dimensions'],'glb_bytes':result['glb_bytes'],'sha256':result['sha256']},indent=2)+'\n')
    print('LOPHA_BUILD_COMPLETE',json.dumps({'triangles':result['triangles'],'bytes':result['glb_bytes'],'dimensions':result['dimensions'],'sha256':result['sha256']}))
if __name__=='__main__':main()
