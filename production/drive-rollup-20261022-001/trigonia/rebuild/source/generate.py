# SPDX-License-Identifier: MIT
"""Original Trigonia genus-level fossil form, informed by T. reticulata Fig. 5.
Continuous paired-valve surface; no source images, scans or reference meshes.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'))
from asset_common import setup_scene, make_material, mesh_object, export_asset


def interp(controls,s):
    # C1 cubic Hermite interpolation with slope-limited component tangents.
    if s<=controls[0][0]: return controls[0][1:]
    if s>=controls[-1][0]: return controls[-1][1:]
    i=next(i for i in range(len(controls)-1) if controls[i][0]<=s<=controls[i+1][0])
    a,b=controls[i],controls[i+1]; d=b[0]-a[0]; u=(s-a[0])/d
    out=[]
    for k in (1,2):
        sec=(b[k]-a[k])/d
        l=controls[max(0,i-1)]; r=controls[min(len(controls)-1,i+2)]
        m0=(b[k]-l[k])/(b[0]-l[0]); m1=(r[k]-a[k])/(r[0]-a[0])
        if m0*sec<=0: m0=0
        if m1*sec<=0: m1=0
        m0=math.copysign(min(abs(m0),3*abs(sec)),m0)
        m1=math.copysign(min(abs(m1),3*abs(sec)),m1)
        out.append((2*u**3-3*u*u+1)*a[k]+(u**3-2*u*u+u)*d*m0+(-2*u**3+3*u*u)*b[k]+(u**3-u*u)*d*m1)
    return out

def peak(v,c,w): return max(0.0,1.0-abs(v-c)/w)
def fade(v,a,b):
    t=max(0,min(1,(v-a)/(b-a)))
    return t*t*(3-2*t)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',type=Path,required=True)
    parser.add_argument('--output-root',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    p=json.loads(args.config.read_text()); col=setup_scene('trigonia',p['seed'])
    mats=[make_material(q['name'],q['hex'],roughness=q['roughness']) for q in p['palette']]
    ring=p['radial_samples']; angular=p['angular_samples']; controls=p['outline_controls']
    verts=[]; faces=[]; tags=[]; lookup={}; params=[]
    # Boundary vertices are shared by both valve surfaces. The pair is one closed
    # manifold solid rather than overlapping ellipsoids or a hollow open seam.
    def vid(sign,i,j):
        t=ring[i]; s=angular[j]
        if i==len(ring)-1 and s>.9999: s=1.0; j=len(angular)-1
        key=(0,0,0) if i==0 else (0,i,j) if i==len(ring)-1 or j in (0,len(angular)-1) else (sign,i,j)
        if key in lookup:return lookup[key]
        by,bz=interp(controls,s); u=p['umbo']
        y=u[0]+t*(by-u[0]); z=u[1]+t*(bz-u[1])
        env=max(0,math.sin(math.pi*t))
        ang=max(0,math.sin(math.pi*s))
        x=.31*env**.83*ang**.48
        # Weakly inflated umbo with a tip bent toward the posterior (+Y).
        y-=.26*t*math.exp(-t/.16)
        flank=1-fade(s,.735,.775)
        ribs=max(peak(t,c,p['rib_half_width']) for c in p['ribs'])
        x+=p['rib_height']*ribs*flank*ang**.3*fade(t,0,.15)*(1-fade(t,.94,1))
        # Main flank/area carina and the more subdued median area carina.
        x+=env*(.020*peak(s,.76,.025)+.009*peak(s,.855,.018))
        area=fade(s,.76,.79)*(1-fade(s,.925,.95))
        radial=max(peak(s,c,.012) for c in p['area_costellae'])
        x+=area*env*(.006*ribs+.004*radial+.0025*ribs*radial)
        # A low raised escutcheon border, surrounding a depressed elongated
        # heart-shaped dorsal field. Crucially the center seam is NOT a tall
        # knife-edge, nor the empty open slit in the art concept.
        rim=peak(s,.95,.035)
        x+=.006*env*rim
        z+=-.028*env*fade(s,.90,.94)+.018*env*rim-.040*env*fade(s,.96,1)-.0018*env*fade(s,.9999,1)
        if i==0 or i==len(ring)-1 or j in (0,len(angular)-1): x=0
        index=len(verts); lookup[key]=index
        verts.append((sign*x,y,z)); params.append((sign,t,s,ribs))
        return index
    for sign in (1,-1):
        for i in range(len(ring)-1):
            for j in range(len(angular)-1):
                if i==0:
                    f=[vid(sign,0,j),vid(sign,1,j),vid(sign,1,j+1)]
                else:
                    f=[vid(sign,i,j),vid(sign,i+1,j),vid(sign,i+1,j+1),vid(sign,i,j+1)]
                if len(set(f))!=len(f):
                    if i==len(ring)-2 and j==len(angular)-2: f=list(dict.fromkeys(f))
                    else: raise ValueError('unintended collapsed topology')
                if len(f)<3: raise ValueError('invalid tapered seam face')
                faces.append(f if sign==1 else list(reversed(f)))
                tags.append((sign,(ring[i]+ring[i+1])/2,(angular[j]+angular[j+1])/2))
    # Normalize designed silhouette to the published 260/1 bounding dimensions.
    # This is specimen-grounded presentation scale, never a scan/replica claim.
    lo=[min(v[k] for v in verts) for k in range(3)]; hi=[max(v[k] for v in verts) for k in range(3)]
    dims=[p['inflation_m'],p['length_m'],p['height_m']]
    verts=[tuple((v[k]-(lo[k]+hi[k])/2)*dims[k]/(hi[k]-lo[k]) if k<2 else (v[k]-lo[k])*dims[k]/(hi[k]-lo[k]) for k in range(3)) for v in verts]
    obj=mesh_object('Paired-valves_continuous-flanks-area-escutcheon',verts,faces,mats,col)
    for poly,(sign,t,s) in zip(obj.data.polygons,tags):
        rib=max(peak(t,c,p['rib_half_width']*1.8) for c in p['ribs'])
        if s>.9999: idx=2  # narrow closed mineral seam, not an opening
        elif s>.95: idx=3
        elif s>.775:idx=2
        elif rib>.48:idx=1
        else:idx=0
        poly.material_index=idx
    # Semantic valve regions remain directly editable in the source mesh.
    for name,predicate in [('right-valve',lambda v:v[0]>=0),('left-valve',lambda v:v[0]<=0),('flank',lambda v:v[2]<.76),('posterior-area',lambda v:.76<=v[2]<=.95),('escutcheon',lambda v:v[2]>.95)]:
        vg=obj.vertex_groups.new(name=name)
        inds=[i for i,q in enumerate(params) if predicate(q)]
        if inds:vg.add(inds,1,'REPLACE')
    obj['representation']='Original genus-level fossil-form, T. reticulata-informed, not measured replica'
    obj['closed_pair']='single shared-boundary surface, two equivalved sides, no internal faces'
    obj['scientific_narrowing']='Fine nodes confined to posterior reticulate area; no giant flank beads'
    root=bpy.data.objects[col['asset_root']]
    root['anterior']='-Y'; root['posterior']='+Y'; root['valve_axis']='X'; root['dorsal']='+Z'
    rec=export_asset('trigonia',{'en':'Trigonia, reticulate-area fossil shell','zh':'Trigonia（后区网纹双壳类化石）'},'animals',col,
        metadata={'description':{'en':'Original closed paired fossil-shell form informed by T. reticulata: curved commarginal flank ribs, distinct posterior carina and depressed dorsal escutcheon. Not an exact specimen replica.','zh':'参考 T. reticulata 的原创合壳化石形态：弯曲同心肋、分隔后区的壳脊及下凹背盾面；并非标本精确复刻。'},
        'generator':'source/generate.py','parameters_sha256':hashlib.sha256(args.config.read_bytes()).hexdigest(),'surface_profile':'palette-only, flat faceted, opaque single-sided PBR',
        'scale_basis':{'specimen':'BSPG 2014V 260/1','length_mm':23.3,'height_mm':20.2,'total_inflation_mm':14.5,'claim':'Template dimensions only; genus model, not a measured specimen replica'},
        'sources':[{'title':'Ayoub-Hannaa et al. (2024), Jurassic Trigoniida from Gebel Maghara','url':'https://doi.org/10.1017/jpa.2023.79','location':'Fig. 5.1–6; description p.1218; Table 5','use':'Consulted scientific reference only; no image/mesh included'}],
        'reconstruction_notes':['Original continuous parametric paired shell, artistic limestone palette and facets.','Genus-level Trigonia asset inspired by identified T. reticulata, not a universal genus size.','Fig.5 overrides concept giant nodules and incorrect knife-edge dorsal slit.','Main flank ribs are commarginal; fine reticulation and tiny tubercles confined to the posterior area.','Upright display pose on ventral margin; not an assertion of life position.']},
        output_root=args.output_root,render=False,max_triangles=p['max_triangles'],max_materials=4,max_primitives=4)
    print('GENERATED',json.dumps({'id':rec['id'],'triangles':rec['triangles'],'hash':rec['sha256']['glb']}))
if __name__=='__main__':main()
