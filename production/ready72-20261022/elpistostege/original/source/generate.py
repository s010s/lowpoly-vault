# SPDX-License-Identifier: MIT
"""Elpistostege watsoni, original fossil relief study; no imported mesh or image.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output OUTPUT
All dependencies and numerical design inputs are inside this source directory.
"""
from pathlib import Path
import argparse, hashlib, json, math, random, shutil, sys
import bpy
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, export_asset
P = json.loads((HERE/'params.json').read_text())
argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args(argv)
OUT=args.output.resolve(); OUT.mkdir(parents=True,exist_ok=True)
COL=setup_scene('elpistostege',P['seed']); rng=random.Random(P['seed'])
bpy.context.scene.render.threads_mode='FIXED'; bpy.context.scene.render.threads=2
M={k:make_material(k,v,roughness=.91) for k,v in P['palette_srgb'].items()}
GROUPS={}; SEM=[]
def store(name,verts,faces,mat,element=None):
    g=GROUPS.setdefault(name,{'v':[],'f':[],'mat':mat,'elements':[]}); n=len(g['v'])
    g['v']+=verts; g['f'] += [tuple(n+i for i in f) for f in faces]
    if element:
        rec={'name':element,'group':name,'vertex_start':n,'vertex_count':len(verts),
             'centroid_m':[sum(v[i] for v in verts)/len(verts) for i in range(3)],
             'bounds_m':{'min':[min(v[i] for v in verts) for i in range(3)],'max':[max(v[i] for v in verts) for i in range(3)]}}
        SEM.append(rec); g['elements'].append(element)
def plate(name,poly,z,h,mat,element=None,bevel=.14):
    # Closed low-relief solid with inset raised cap; gaps are real open spaces between solids.
    n=len(poly); cx=sum(x for x,y in poly)/n; cy=sum(y for x,y in poly)/n
    verts=[(x,y,z) for x,y in poly]+[(x,y,z+h*.36) for x,y in poly]+[(x+(cx-x)*bevel,y+(cy-y)*bevel,z+h) for x,y in poly]
    faces=[tuple(reversed(range(n))),tuple(range(2*n,3*n))]
    for i in range(n):
        j=(i+1)%n; faces.extend([(i,j,n+j,n+i),(n+i,n+j,2*n+j,2*n+i)])
    store(name,verts,faces,mat,element)
def tube(name,points,width,height,mat,element=None):
    # Closed five-sided ribbon prism for fossil rays and fracture lines.
    vs=[]; fs=[]; N=6
    for i,p in enumerate(points):
        prev=points[max(0,i-1)]; nex=points[min(len(points)-1,i+1)]; dx=nex[0]-prev[0]; dy=nex[1]-prev[1]; l=math.hypot(dx,dy)
        nx,ny=-dy/l,dx/l; w=width*(1-.45*i/max(1,len(points)-1))
        for j in range(N):
            a=2*math.pi*j/N; vs.append((p[0]+nx*w*math.cos(a),p[1]+ny*w*math.cos(a),p[2]+height*math.sin(a)))
    fs=[tuple(reversed(range(N))),tuple((len(points)-1)*N+j for j in range(N))]
    for i in range(len(points)-1):
        for j in range(N): fs.append((i*N+j,i*N+(j+1)%N,(i+1)*N+(j+1)%N,(i+1)*N+j))
    store(name,vs,fs,mat,element)
# Artist-designed support: the original preparation outline is not asserted to be reproduced.
slab=[(-.10,-.835),(.065,-.835),(.171,-.785),(.19,-.66),(.208,-.43),(.201,-.22),(.185,-.015),(.21,.19),(.177,.38),(.191,.58),(.135,.788),(.055,.835),(-.073,.825),(-.164,.765),(-.195,.57),(-.183,.38),(-.21,.19),(-.181,-.05),(-.209,-.31),(-.19,-.51),(-.183,-.715)]
plate('01_matrix_slab',slab,0,.025,'matrix',bevel=.055)
# Small geological fracture traces remain inside the stone support and are not anatomy.
for i,pts in enumerate([[(-.18,-.55),(-.123,-.535),(-.096,-.56)],[(.105,-.78),(.071,-.72),(.09,-.68)],[(.202,-.2),(.16,-.23),(.145,-.185)], [(-.204,.19),(-.155,.17),(-.12,.22),(-.105,.19)],[(.181,.56),(.115,.525),(.085,.54)], [(-.12,.77),(-.082,.70),(-.094,.65)]]):
    tube('02_matrix_fractures',[(x,y,.0252) for x,y in pts],.0008,.00035,'dark','matrix_fracture_%02d'%i)
# Flattened trunk with articulate lateral outline. The slab deliberately remains visible around it.
rings=[(-.527,.092,.032,.010),(-.485,.101,.0325,.0105),(-.43,.104,.0325,.0105),(-.36,.096,.032,.010),(-.28,.084,.031,.009),(-.20,.078,.0305,.008),(-.12,.071,.030,.0075),(-.04,.066,.030,.0075),(.04,.056,.0295,.007),(.12,.046,.029,.0065),(.20,.042,.029,.006),(.30,.035,.0285,.0055),(.40,.032,.028,.005),(.50,.027,.028,.005),(.60,.02,.0275,.0045),(.68,.012,.027,.004)]
vs=[]; fs=[]; N=12
for j,(y,w,zc,h) in enumerate(rings):
    xc=.006*math.sin((y+.4)*7)
    for k in range(N):
        a=2*math.pi*k/N; vs.append((xc+w*math.cos(a),y,zc+h*math.sin(a)))
fs=[tuple(reversed(range(N))),tuple((len(rings)-1)*N+i for i in range(N))]
for j in range(len(rings)-1):
    for k in range(N): fs.append((j*N+k,j*N+(k+1)%N,(j+1)*N+(k+1)%N,(j+1)*N+k))
store('03_compressed_trunk',vs,fs,'fossil_base','flattened_body')
def profile(y):
    for a,b in zip(rings,rings[1:]):
        if a[0]<=y<=b[0]:
            t=(y-a[0])/(b[0]-a[0]); return tuple(a[i]*(1-t)+b[i]*t for i in range(1,4))
    return rings[-1][1:]
# Broad triangular cranial roof, not a living head or a round fish snout.
skull=[(-.016,-.785),(.018,-.782),(.061,-.746),(.086,-.69),(.099,-.623),(.125,-.542),(.108,-.507),(.064,-.513),(.025,-.53),(-.035,-.522),(-.098,-.50),(-.121,-.53),(-.105,-.618),(-.078,-.699),(-.045,-.759)]
plate('04_cranial_substrate',skull,.026,.018,'fossil_base','broad_triangular_skull',bevel=.09)
cranial=[('rostral',[(-.017,-.779),(.017,-.776),(.045,-.746),(.028,-.72),(-.022,-.722),(-.041,-.749)],.044,.005),
('left_premaxillary',[(-.044,-.745),(-.024,-.719),(-.032,-.69),(-.075,-.686),(-.071,-.708)],.043,.005),
('right_premaxillary',[(.049,-.741),(.073,-.707),(.079,-.682),(.039,-.686),(.026,-.717)],.043,.005),
('median_nasal',[(-.02,-.717),(.024,-.715),(.032,-.681),(.021,-.652),(-.023,-.654),(-.029,-.687)],.044,.007),
('median_frontals',[(-.024,-.648),(.022,-.646),(.032,-.611),(.020,-.572),(-.025,-.574),(-.035,-.613)],.043,.008),
('posterior_roof',[(-.024,-.569),(.024,-.567),(.057,-.534),(.024,-.534),(-.021,-.533),(-.06,-.52)],.041,.008),
('left_cheek',[(-.083,-.68),(-.055,-.674),(-.052,-.631),(-.039,-.616),(-.045,-.584),(-.10,-.607)],.041,.007),
('right_cheek',[(.056,-.672),(.086,-.676),(.097,-.613),(.047,-.589),(.039,-.619),(.05,-.637)],.041,.007),
('left_posterolateral',[(-.102,-.598),(-.049,-.579),(-.037,-.557),(-.074,-.521),(-.105,-.511),(-.116,-.534)],.039,.009),
('right_posterolateral',[(.049,-.584),(.10,-.604),(.119,-.544),(.105,-.519),(.071,-.524),(.038,-.556)],.039,.009)]
for i,(name,poly,z,h) in enumerate(cranial): plate('05_cranial_roof_plates',poly,z,h,'fossil_mid',name)
# Paired dorsal orbit depressions, no eyeballs. Low rims sit in the skull roof.
for side in [-1,1]:
    cx=side*.042; cy=-.659; n=12
    pol=[(cx+.012*math.cos(k*2*math.pi/n),cy+.017*math.sin(k*2*math.pi/n)) for k in range(n)]
    plate('06_orbit_floors',pol,.044,.0014,'dark','dorsal_orbit_'+str(side),bevel=.02)
    outer=[(cx+.0148*math.cos(k*2*math.pi/n),cy+.0198*math.sin(k*2*math.pi/n),.0505) for k in range(n)]
    inner=[(cx+.0117*math.cos(k*2*math.pi/n),cy+.0167*math.sin(k*2*math.pi/n),.0495) for k in range(n)]
    vs=outer+inner+[(x,y,.044) for x,y,z in outer+inner]
    fs=[]
    for k in range(n):
        j=(k+1)%n; fs += [(k,j,n+j,n+k),(k,2*n+k,2*n+j,j),(n+k,n+j,3*n+j,3*n+k),(2*n+k,3*n+k,3*n+j,2*n+j)]
    store('07_orbit_bone_rims',vs,fs,'fossil_light','orbit_bone_rim_'+str(side))
# Isolated opercular pieces are original low-poly approximations to the articulated fragmented roof.
for side in [-1,1]:
    poly=[(side*x,y) for x,y in [(.083,-.50),(.119,-.496),(.126,-.458),(.098,-.441),(.083,-.464)]]
    plate('08_opercular_fragments',poly,.029,.012,'fossil_mid','opercular_'+str(side))
# Articulated ganoid rhombi, individually closed shells rather than an image texture.
sc=0
for row in range(42):
    y=-.476+row*.0215
    w,zc,h=profile(y); cx=.006*math.sin((y+.4)*7)
    for c in range(-8,9):
        x=c*.018+(row%2)*.009+cx
        if abs(x-cx)>w*.90: continue
        # Patchy posterior preservation; do not restore a fully armoured tail not seen in Fig.1.
        if y>.12 and rng.random()<.38: continue
        # Explicit virtual cutaway footprint: clear the overlying scales, preserving an in-situ reveal.
        if -.495<y<-.318 and x>.066: continue
        z=zc+h*math.sqrt(max(0,1-((x-cx)/w)**2))-.0015
        size=.0086*(1-.2*max(0,y)); poly=[(x,y-.0102),(x+size,y),(x,y+.0102),(x-size,y)]
        plate('09_articulated_scales',poly,z,.0033,'fossil_mid','scale_%03d'%sc,bevel=.08); sc+=1
# Fine posterior flank fragments signal preserved broken scale patches.
for i in range(37):
    y=.22+rng.random()*.37; w,zc,h=profile(y); x=(rng.random()*1.1-.55)*w
    dx=.003+rng.random()*.002; dy=.005+rng.random()*.005
    z=zc+h*math.sqrt(max(0,1-(x/w)**2))-.0003
    plate('10_posterior_fragments',[(x-dx,y),(x,y-dy),(x+dx*.7,y),(x+.0015,y+dy)],z,.0018,'fossil_light','posterior_fragment_%02d'%i,bevel=.08)
# Pectoral fin coordinate system. Right fin is the disclosed analytical virtual cutaway.
def finxy(u,v,side=1): return (side*(.077+.35*v+u),-.50+v)
finpoly=[(-.034,-.005),(.023,-.005),(.030,.016),(.050,.070),(.048,.13),(.026,.188),(.001,.214),(-.026,.185),(-.039,.12),(-.036,.06)]
for side in [-1,1]:
    plate('11_pectoral_fin_impressions',[finxy(u,v,side) for u,v in finpoly],.027,.0035,'fossil_base','pectoral_fin_'+str(side),bevel=.08)
    # Peripheral and distal rays preserve a fin web beyond the endoskeleton, not exposed digits.
    for k in range(24):
        u0=-.034+k*.0034; vend=.173+.038*math.sin(math.pi*k/23); uend=-.025+k*.00225
        vstart=.105+.047*math.sin(math.pi*k/23)
        p=[finxy(u0,vstart,side),finxy((u0+uend)*.5,(vstart+vend)*.5,side),finxy(uend,vend,side)]
        tube('12_pectoral_lepidotrichia',[(x,y,.0318) for x,y in p],.00065,.0007,'fossil_light','pectoral_ray_%d_%02d'%(side,k))
    if side==-1:
        # Opposite fin remains a normal fossil impression, not a second invented dorsal skeleton.
        for k in range(8):
            p=[finxy(-.023+k*.006,.045,-1),finxy(-.028+k*.0065,.128,-1)]
            tube('12_pectoral_lepidotrichia',[(x,y,.0335) for x,y in p],.0013,.0009,'fossil_mid','left_proximal_ray_%02d'%k)
# CT Fig.3d inspired compressed sequence. Deliberately unequal, staggered bone rows, never five straight fingers.
bones=[('humerus', '13_reveal_humerus',
  [(-0.025362, 0.009062), (-0.014082, 0.002482), (0.007538, 0.004362), (0.015058, 0.016582), (0.013178, 0.034442),
   (0.030098, 0.040082), (0.020698, 0.047602), (-0.002802, 0.044782), (-0.015022, 0.033502), (-0.026302, 0.024102)]),
 ('radius', '14_reveal_radius',
  [(-0.0196914, 0.0497886), (-0.0074714, 0.0497886), (-0.0008914, 0.0591886), (-0.0046514, 0.0761086),
   (-0.0196914, 0.0770486), (-0.0262714, 0.0667086), (-0.0253314, 0.0563686)]),
 ('ulna', '15_reveal_ulna',
  [(0.00386, 0.0509), (0.02078, 0.0509), (0.02454, 0.06312), (0.03018, 0.07252), (0.02078, 0.07722),
   (0.00386, 0.07534)]),
 ('intermedium', '16_reveal_carpals',
  [(-0.00261, 0.082352), (0.00087, 0.081482), (0.00348, 0.092792), (0.00174, 0.100622), (-0.00348, 0.099752)]),
 ('radial_proximal', '16_reveal_carpals',
  [(-0.01861, 0.0837767), (-0.0073, 0.0837767), (-0.00904, 0.0976967), (-0.016, 0.1072667), (-0.0247, 0.1055267),
   (-0.02035, 0.0959567)]),
 ('ulnare', '16_reveal_carpals',
  [(0.00782, 0.0825817), (0.02174, 0.0825817), (0.02696, 0.0921517), (0.03218, 0.0956317), (0.02435, 0.1034617),
   (0.00695, 0.1025917)]),
 ('radial_preaxial', '16_reveal_carpals',
  [(-0.029272, 0.112754), (-0.022312, 0.111884), (-0.017962, 0.118844), (-0.021442, 0.124064), (-0.031012, 0.121454)]),
 ('radial_1', '17_reveal_distal_row1',
  [(0.025728, 0.109998), (0.031568, 0.110728), (0.036678, 0.118028), (0.031568, 0.120948), (0.026458, 0.117298)]),
 ('radial_2', '17_reveal_distal_row1',
  [(0.01689, 0.1107), (0.022, 0.1107), (0.02784, 0.12311), (0.02419, 0.12603), (0.01908, 0.11946)]),
 ('radial_3', '17_reveal_distal_row1',
  [(0.006296, 0.110808), (0.011406, 0.110808), (0.015056, 0.121758), (0.009946, 0.127598), (0.006296, 0.121028)]),
 ('radial_4', '17_reveal_distal_row1',
  [(-0.003568, 0.110106), (8.2e-05, 0.110106), (0.000812, 0.118866), (-0.003568, 0.122516), (-0.005758, 0.117406)]),
 ('radial_5', '17_reveal_distal_row1',
  [(-0.01246, 0.1082825), (-0.00881, 0.1090125), (-0.00881, 0.1148525), (-0.01392, 0.1148525)]),
 ('radial_6', '17_reveal_distal_row1',
  [(-0.011838, 0.122106), (-0.007458, 0.123566), (-0.007458, 0.129406), (-0.013298, 0.133786), (-0.016948, 0.130136)]),
 ('distal_axis_1a', '18_reveal_distal_row2',
  [(0.02954, 0.12708), (0.03538, 0.12708), (0.03246, 0.13365), (0.02662, 0.13219)]),
 ('distal_axis_2a', '18_reveal_distal_row2',
  [(0.01808, 0.129782), (0.02246, 0.131242), (0.02611, 0.137082), (0.02246, 0.140002), (0.01589, 0.134892)]),
 ('distal_axis_3a', '18_reveal_distal_row2',
  [(0.006864, 0.134512), (0.011974, 0.133052), (0.013434, 0.140352), (0.009054, 0.144732), (0.004674, 0.140352)]),
 ('distal_axis_4a', '18_reveal_distal_row2',
  [(-0.003838, 0.130728), (-0.000188, 0.130728), (0.000542, 0.137298), (-0.005298, 0.140948), (-0.008218, 0.137298)]),
 ('distal_axis_5a', '18_reveal_distal_row2',
  [(-0.012406, 0.139998), (-0.008026, 0.141458), (-0.007296, 0.148028), (-0.011676, 0.150948), (-0.014596, 0.146568)]),
 ('digit_like_distal_1', '19_reveal_digit_like_elements',
  [(0.025998, 0.145162), (0.030378, 0.141512), (0.036218, 0.144432), (0.034758, 0.148082), (0.029648, 0.148812)]),
 ('digit_like_distal_2', '19_reveal_digit_like_elements',
  [(0.013836, 0.150026), (0.018946, 0.147106), (0.022596, 0.151486), (0.021866, 0.157326), (0.016756, 0.158056)]),
 ('digit_like_distal_3', '19_reveal_digit_like_elements',
  [(0.001134, 0.14662), (0.005514, 0.14735), (0.008434, 0.15246), (0.005514, 0.15611), (0.000404, 0.15246)]),
 ('digit_like_distal_4', '19_reveal_digit_like_elements',
  [(-0.009218, 0.157242), (-0.004838, 0.155782), (0.000272, 0.161622), (-0.001918, 0.165272), (-0.006298, 0.163082)])]
for name,group,poly in bones:
    plate(group,[finxy(u,v) for u,v in poly],.042 if name=='humerus' else .037,.006 if name=='humerus' else .0052,'reveal_bone',name,bevel=.16)
# Pelvic fins are far posterior to the shoulders, with ray-bearing outline rather than feet.
for side,basey in [(-1,.20),(1,.18)]:
    poly=[(side*.036,basey),(side*.074,basey+.025),(side*.105,basey+.13),(side*.07,basey+.143),(side*.04,basey+.074)]
    plate('20_pelvic_fin_impressions',poly,.026,.004,'fossil_base','pelvic_fin_'+str(side),bevel=.10)
    for k in range(11):
        pts=[(side*(.037+k*.0011),basey+.016,.031),(side*(.059+k*.0035),basey+.103+k*.0037,.0315)]
        tube('21_pelvic_fin_rays',pts,.0007,.0008,'fossil_light','pelvic_ray_%d_%d'%(side,k))
# Small anal fin is separated from the caudal fan; no dorsal fin is invented.
plate('22_anal_impression',[(-.024,.439),(-.056,.48),(-.061,.56),(-.039,.587),(-.024,.528)],.026,.0035,'fossil_base','anal_fin')
for k in range(8): tube('23_anal_rays',[(-.026,.46+k*.006,.0305),(-.054+k*.002,.51+k*.01,.031)],.0006,.00065,'fossil_light','anal_ray_%d'%k)
# Asymmetric caudal preservation, low notched terminal margin, total fossil extent 1.570 m.
tail=[(-.021,.543),(-.037,.597),(-.066,.673),(-.075,.746),(-.053,.785),(-.008,.758),(.027,.782),(.061,.754),(.059,.699),(.04,.641),(.018,.581)]
plate('24_caudal_fin_impression',tail,.0255,.0045,'fossil_base','caudal_fin',bevel=.045)
for k in range(25):
    t=k/24; xend=-.063+.119*t; yend=.759+.018*abs(2*t-1)-.012*math.exp(-((t-.52)/.12)**2)
    pts=[(-.010+.025*t,.584+.035*abs(2*t-1),.031),((xend)*.63,.687,.032),(xend,yend,.031)]
    tube('25_caudal_lepidotrichia',pts,.0008,.0009,'fossil_mid','caudal_ray_%02d'%k)
for name,g in GROUPS.items():
    ob=mesh_object(name,g['v'],g['f'],M[g['mat']],COL)
    ob['semantic_elements']=json.dumps(g['elements']); ob['representation']='original low-poly fossil relief'
root=bpy.data.objects[COL['asset_root']]
root['ct_reveal_notice']='Right pectoral endoskeleton is a virtual analytical cutaway informed by CT Fig.3d, not naturally exposed dorsal fossil bones.'
root['taxon']='Elpistostege watsoni'; root['specimen_reference']='MHNM06-2067'; root['claim_scope']='bounded fossil-specimen study; not scientific segmentation'
record=export_asset('elpistostege',P['name'],'fossils',COL,metadata={
    'description':{'en':root['ct_reveal_notice'],'zh':'完整扁平化石研究；右胸鳍内骨骼为原位 CT 分析揭示，并非自然裸露的背面手骨。'},
    'generator':'source/generate.py','reference_specimen':'MHNM06-2067','claim_scope':root['claim_scope'],
    'source_references':['https://www.nature.com/articles/s41586-020-2100-8/figures/1','https://www.nature.com/articles/s41586-020-2100-8/figures/3'],
    'uncertainty':'Original generated approximate relief, not CT segmentation. Slab depth, scale count and small bone shapes simplified.'},
    output_root=OUT/'private'/'helper-export',render=False,max_triangles=P['budgets']['max_triangles'],max_materials=P['budgets']['max_materials'],max_primitives=P['budgets']['max_primitives'],diagnostics=False)
STAGE=OUT/'private'/'helper-export'/'elpistostege'
# Canonical helper exports by slug; the public model-task-v2 filenames are explicit generator outputs.
for ext in ['blend','glb']: shutil.copyfile(STAGE/f'elpistostege.{ext}',OUT/f'model.{ext}')
qa=json.loads((STAGE/'qa.json').read_text()); qa['glb']['file']='model.glb'; record['glb']='model.glb'; record['blend']='model.blend'; record['preview']='preview.png'; record['origin']='slab bottom center at Z=0'
evidence=OUT/'qa'/'evidence'; evidence.mkdir(parents=True,exist_ok=True)
(evidence/'source-and-glb.json').write_text(json.dumps(qa,indent=2)+'\n')
(evidence/'build-metadata.json').write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n')
(evidence/'semantic-anatomy.json').write_text(json.dumps({'glb_sha256':record['sha256']['glb'],'elements':SEM,'scale_count':sc,'ct_bone_elements':len(bones),'fossil_tip_to_tail_m':1.57,'pectoral_bone_extent_m':.167,'bone_containment_check':'qa/evidence/anatomy-geometry.json','ct_cutaway':root['ct_reveal_notice'],'method':'Original designed closed polygons, sequence based on Fig.3d; not traced segmentation.'},indent=2)+'\n')
assert (OUT/'model.glb').stat().st_size<=P['budgets']['max_glb_bytes']
print(json.dumps({'status':'BUILT_NOT_REVIEWED','glb_sha256':record['sha256']['glb'],'triangles':record['triangles'],'objects':len(GROUPS),'output':str(OUT)}))
