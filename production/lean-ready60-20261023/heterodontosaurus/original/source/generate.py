#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic original Heterodontosaurus living reconstruction.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --out OUTPUT [--clay]
Only the adjacent params.json and SHA-pinned deps/ are project dependencies.
"""
from pathlib import Path
import sys, json, math, argparse, shutil, hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent/'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, mesh_object, make_material, export_asset, render_previews, ground_asset
P=json.loads((Path(__file__).with_name('params.json')).read_text())
COL=None; MAT={}

def loft_y(name, sections, mats=('flank','dorsal','belly'), n=12):
    # Explicit transverse profiles: y, centre_z, half_width, half_height.
    verts=[]; faces=[]
    for y,z,rx,rz in sections:
        verts.extend((rx*math.cos(2*math.pi*j/n),y,z+rz*math.sin(2*math.pi*j/n)) for j in range(n))
    faces.append(tuple(reversed(range(n))))
    for i in range(len(sections)-1):
        for j in range(n):faces.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    faces.append(tuple((len(sections)-1)*n+j for j in range(n)))
    obj=mesh_object(name,verts,faces,[MAT[k] for k in mats],COL)
    if len(mats)==3:
        for poly in obj.data.polygons:
            if len(poly.vertices)!=4:continue
            # Material regions follow body surface, no floating overlay geometry.
            ring_angle=2*math.pi*((poly.index-1)%n+.5)/n
            poly.material_index=1 if math.sin(ring_angle)>.48 else 2 if math.sin(ring_angle)<-.48 else 0
    return obj

def tube(name, points, radii, mat='flank', n=8, ellipse=1):
    ps=[Vector(p) for p in points];v=[];f=[]
    for i,p in enumerate(ps):
        tangent=(ps[min(i+1,len(ps)-1)]-ps[max(0,i-1)]).normalized()
        ref=Vector((1,0,0)) if abs(tangent.x)<.85 else Vector((0,1,0))
        u=(ref-tangent*ref.dot(tangent)).normalized();w=tangent.cross(u).normalized()
        for j in range(n):
            a=2*math.pi*j/n;v.append(tuple(p+u*(radii[i]*math.cos(a))+w*(radii[i]*ellipse*math.sin(a))))
    f.append(tuple(reversed(range(n))))
    for i in range(len(ps)-1):
        for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
    f.append(tuple((len(ps)-1)*n+j for j in range(n)))
    return mesh_object(name,v,f,MAT[mat],COL)

def ellipsoid(name, c, r, mat, n=12, rings=5):
    v=[(c[0],c[1],c[2]+r[2])];f=[]
    for k in range(1,rings):
        a=math.pi*k/rings
        for j in range(n):
            b=2*math.pi*j/n;v.append((c[0]+r[0]*math.sin(a)*math.cos(b),c[1]+r[1]*math.sin(a)*math.sin(b),c[2]+r[2]*math.cos(a)))
    end=len(v);v.append((c[0],c[1],c[2]-r[2]))
    for j in range(n):f.append((0,1+j,1+(j+1)%n))
    for k in range(rings-2):
        for j in range(n):
            a=1+k*n+j;b=1+k*n+(j+1)%n;f.append((a,b,b+n,a+n))
    for j in range(n):f.append((end,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
    return mesh_object(name,v,f,MAT[mat],COL)

def build():
    global COL,MAT
    COL=setup_scene(P['asset_id'],P['seed']);MAT={k:make_material(k,v,roughness=.86 if k!='eye' else .55) for k,v in P['palette'].items()}
    # Deliberate oval cross sections, lean thorax, high pelvic base and tapering long tail.
    loft_y('Trunk_profile', [(-.155,.405,.030,.045),(-.115,.410,.058,.080),(-.045,.402,.078,.099),(.035,.402,.082,.102),(.115,.411,.073,.096),(.177,.415,.052,.070),(.205,.415,.032,.045)])
    loft_y('Tail_long_balance',[(.145,.419,.052,.065),(.235,.423,.043,.053),(.335,.436,.032,.041),(.45,.453,.022,.029),(.57,.472,.014,.019),(.68,.484,.007,.010),(.762,.491,.0018,.0026)],n=10)
    # S-arched neck retains a narrow throat and leads into a deep, short skull.
    tube('Neck_S_profile',[(0,-.118,.424),(0,-.164,.475),(0,-.199,.529),(0,-.247,.563),(0,-.282,.590)],[.050,.044,.035,.033,.035],n=12,ellipse=1.14)
    loft_y('Skull_deep_profile',[(-.272,.606,.026,.044),(-.292,.611,.041,.052),(-.326,.613,.049,.054),(-.359,.605,.042,.045),(-.391,.599,.032,.032),(-.415,.592,.025,.021)],n=12)
    loft_y('Short_upper_beak',[(-.412,.590,.025,.020),(-.427,.590,.022,.018),(-.438,.586,.015,.011)],mats=('keratin',),n=10)
    loft_y('Lower_jaw',[(-.285,.555,.029,.019),(-.318,.543,.038,.019),(-.361,.540,.034,.016),(-.399,.545,.026,.013),(-.424,.550,.020,.010)],mats=('flank','flank','belly'),n=10)
    loft_y('Short_lower_beak',[(-.417,.550,.020,.009),(-.435,.554,.014,.008)],mats=('keratin',),n=8)
    # A dark recessed oral volume is bounded within the gape, not a huge open gape.
    loft_y('Oral_recess',[(-.304,.563,.027,.011),(-.350,.562,.029,.010),(-.398,.566,.020,.007)],mats=('mouth',),n=8)
    for s,label in [(1,'R'),(-1,'L')]:
        # Teeth remain within lateral jaw region, enlarged but not oversized tusks.
        tube(label+'_Upper_caniniform',[(s*.029,-.395,.582),(s*.030,-.394,.570),(s*.029,-.391,.554),(s*.028,-.387,.549)],[.0058,.005,.0028,.0007],mat='tooth',n=7,ellipse=.8)
        tube(label+'_Lower_caniniform',[(s*.022,-.415,.554),(s*.023,-.412,.565),(s*.023,-.408,.578)],[.0047,.0034,.0006],mat='tooth',n=7,ellipse=.8)
        # Posterior cheek teeth are intentionally subtle, not exposed monster fangs.
        for j in range(6):
            y=-.375+j*.010
            tube(label+'_Cheek_tooth_%02d'%j,[(s*(.030+j*.0009),y,.570),(s*(.030+j*.0009),y,.564)],[.0028,.0011],mat='tooth',n=5,ellipse=.65)
        ellipsoid(label+'_Eye_socket',(s*.044,-.329,.627),(.008,.015,.014),'dorsal',n=12,rings=5)
        ellipsoid(label+'_Eye_iris',(s*.050,-.331,.628),(.005,.009,.009),'iris',n=12,rings=5)
        ellipsoid(label+'_Eye_pupil',(s*.054,-.332,.628),(.0028,.0049,.006),'eye',n=10,rings=5)
        ellipsoid(label+'_Nostril',(s*.024,-.414,.601),(.0022,.004,.0025),'eye',n=8,rings=4)
        # Hindlimb zigzag: femur forward; tibia back; elongated metatarsus forward.
        tube(label+'_Hind_thigh',[(s*.055,.106,.420),(s*.081,.069,.371),(s*.086,-.014,.281)],[.049,.047,.029],n=10,ellipse=1.15)
        tube(label+'_Hind_shin',[(s*.086,-.014,.281),(s*.085,.059,.173),(s*.077,.101,.102)],[.026,.020,.013],n=9,ellipse=.85)
        tube(label+'_Metatarsus',[(s*.077,.101,.105),(s*.080,.063,.055),(s*.082,.035,.027)],[.014,.012,.014],n=8,ellipse=.8)
        # Three main forward toes and a short elevated medial hallux, not theropod talons.
        for j in range(3):
            x=s*(.082+(j-1)*.020);start=(s*.082,.035,.028);end_y=-.061-(.021 if j==1 else 0)
            tube(label+'_Foot_digit_%d'%(j+2),[start,(x,-.010,.018),(x+s*(j-1)*.005,end_y,.014)],[.010,.0075,.0045],mat='flank',n=7,ellipse=.7)
            tube(label+'_Foot_claw_%d'%(j+2),[(x+s*(j-1)*.005,end_y,.014),(x+s*(j-1)*.006,end_y-.015,.008),(x+s*(j-1)*.006,end_y-.019,.005)],[.0048,.003,.0006],mat='keratin',n=6,ellipse=.7)
        tube(label+'_Small_hallux',[(s*.070,.051,.040),(s*.057,.069,.029),(s*.052,.084,.025)],[.005,.0037,.001],mat='keratin',n=6)
        # Humerus, radius/ulna envelope and inward palm. No flat-down pronation.
        tube(label+'_Upper_arm',[(s*.050,-.110,.446),(s*.067,-.156,.393),(s*.077,-.175,.353)],[.022,.017,.013],n=8)
        tube(label+'_Forearm',[(s*.077,-.175,.353),(s*.086,-.217,.346),(s*.095,-.249,.348)],[.014,.012,.010],n=8,ellipse=.85)
        tube(label+'_Medial_palm',[(s*.095,-.245,.348),(s*.098,-.263,.335),(s*.099,-.276,.319)],[.011,.015,.012],n=8,ellipse=.63)
        # Main finger axes spread in sagittal plane; hooks curve inwards towards palm.
        for j in range(3):
            y=-.280+j*.013;z=.323-j*.006;length=[.039,.051,.043][j]
            start=(s*.100,y,z);bend=(s*.103,y-.013,z-length*.67);tip=(s*.096,y-.020,z-length)
            tube(label+'_Hand_main_digit_%d'%(j+1),[start,bend,tip],[.0057,.0044,.0031],n=7)
            tube(label+'_Hand_main_claw_%d'%(j+1),[tip,(s*.089,y-.025,z-length-.003),(s*.083,y-.024,z-length+.004)],[.0038,.0025,.0005],mat='keratin',n=6)
        for j in range(2):
            tube(label+'_Hand_reduced_digit_%d'%(j+4),[(s*.098,-.246+j*.009,.320),(s*.101,-.250+j*.010,.307),(s*.098,-.252+j*.010,.302)],[.0036,.0027,.001],n=6)
    # Normalize entire original construction to frozen 1.2 m nose-to-tail envelope.
    points=[v.co for o in COL.objects if o.type=='MESH' for v in o.data.vertices]
    length=max(p.y for p in points)-min(p.y for p in points)
    scale=P['total_length_m']/length
    # Shift sole centre to root; geometry, not object transforms, carries the adjustment.
    for obj in COL.objects:
        if obj.type=='MESH':
            for v in obj.data.vertices:
                v.co*=scale;v.co.y-=.004*scale
    ground_asset(COL,center_xy=False)
    return COL

def main():
    av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    pa=argparse.ArgumentParser();pa.add_argument('--out',type=Path,required=True);pa.add_argument('--clay',action='store_true');args=pa.parse_args(av)
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    col=build()
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    metadata={'generator':'source/generate.py','generator_seed':P['seed'],'revision':P['revision'],'representation':'living-reconstruction','scale_basis':'NHM genus length estimate 1.2 m, not a measured AM4766 specimen','source_dependencies':'Adjacent params.json and deps/ only','description':{'en':'Original faceted Heterodontosaurus: compact deep head, short beak, differentiated teeth and inward grasping hands.','zh':'原创低多边形异齿龙全身复原，短喙、分化齿列和内向抓握手。'}}
    stage=out/'private'/'export-stage'
    export_asset(P['asset_id'],{'en':'Heterodontosaurus','zh':'异齿龙'},'dinosaurs',col,metadata,output_root=stage,render=False,max_triangles=10000,max_materials=8,max_primitives=96)
    generated=stage/P['asset_id']
    shutil.copyfile(generated/(P['asset_id']+'.glb'),out/'model.glb');shutil.copyfile(generated/(P['asset_id']+'.blend'),out/'model.blend')
    ev=out/'qa'/'evidence';ev.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(generated/'qa.json',ev/'source-and-glb.json');shutil.copyfile(generated/'metadata.json',ev/'build-metadata.json')
    if args.clay:
        clay=make_material('_gray_diagnostic','#949494',roughness=.86)
        bpy.context.view_layer.material_override=clay
        render_previews(col,out/'private'/'clay',views=('front','side','top','hero'),resolution=480,samples=8)
    print('BUILD_COMPLETE '+str(out/'model.glb'))
if __name__=='__main__':main()
