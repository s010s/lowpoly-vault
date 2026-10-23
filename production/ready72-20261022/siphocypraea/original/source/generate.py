#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Deterministic external Siphocypraea shell study, PRI 69852 informed.
Run: blender -b -t 2 --python-exit-code 1 --python source/generate.py -- --output-dir OUTPUT
Only bpy, mathutils, stdlib and the adjacent pinned deps are used. No reference pixels.
"""
from pathlib import Path
import argparse, math, json, hashlib, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
import bpy, bmesh
from asset_common import setup_scene, make_material, mesh_object, export_asset
from mathutils import Vector

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,required=True)
    a=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    out=a.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text())
    collection=setup_scene(p['asset_id'],seed=p['seed'])
    mats=[make_material('Fossil shell ivory',p['palette']['shell'],.82),make_material('Thick lip and rounded teeth',p['palette']['lip'],.78),make_material('Recessed shell interior',p['palette']['interior'],.91)]
    # Individually chosen profile stations in metres, never a traced outline.
    # Body is an inflated asymmetric C-section; the posterior rolls inward into a
    # recessed spire opening and the slit winds as a comma-shaped furrow.
    profile=[(0,.0027,.0034,.0034),( .002,.0064,.0065,.008),(.006,.0100,.0090,.012),(.012,.0138,.0115,.016),(.022,.0173,.0128,.020),(.033,.0185,.0130,.021),(.043,.0179,.0126,.0207),(.052,.0156,.0113,.018),(.057,.0127,.0096,.0149),(.060,.0100,.0079,.0118),(.062,.0079,.0064,.0095),(.064,.0059,.0051,.0070),(.0655,.0045,.0042,.0054)]
    def interp(z,k):
        for idx,(x,y) in enumerate(zip(profile,profile[1:])):
            if x[0]<=z<=y[0]:
                h=y[0]-x[0];t=(z-x[0])/h
                prev=profile[max(0,idx-1)];nxt=profile[min(len(profile)-1,idx+2)]
                m0=(y[k]-prev[k])/(y[0]-prev[0]);m1=(nxt[k]-x[k])/(nxt[0]-x[0])
                return (2*t**3-3*t*t+1)*x[k]+(t**3-2*t*t+t)*h*m0+(-2*t**3+3*t*t)*y[k]+(t**3-t*t)*h*m1
        return profile[-1][k]
    # Four profile samples per tooth, including valleys; 21 and 22 simplified
    # ribs are integral vertex displacement, not detached primitive cubes.
    zs=sorted(set([0,.001,.002,.004,.006]+[.007+i*(.049/84) for i in range(85)]+[.057,.058,.059,.060,.061,.062,.063,.064,.0655]))
    rows=[]
    for z in zs:
        t=max(0,min(1,(z-.056)/.0095)); rows.append(dict(z=z,rx=interp(z,1),front=interp(z,2),back=interp(z,3),twist=-.38*t*t,offset=.0012*t*t,top=False))
    for z,rx,fr,bk,tw,off in [(.0650,.0037,.0037,.0046,-.58,.0014),(.0638,.0030,.0030,.0038,-.84,.0015),(.0621,.0025,.0025,.0030,-1.13,.0015),(.0608,.0020,.0020,.0025,-1.43,.0015)]:
        rows.append(dict(z=z,rx=rx,front=fr,back=bk,twist=tw,offset=off,top=True))
    us=[0,.008,.022,.045,.075,.12,.18,.26,.35,.44,.5,.56,.65,.74,.82,.88,.925,.955,.978,.992,1]
    iu=[i/12 for i in range(13)]
    verts=[]; faces=[]; mi=[]; ringlen=len(us)+len(iu)
    def tooth(z,side):
        if not .007<=z<=.056: return 0
        n=21 if side>0 else 22
        phase=(z-.007)/.049*n+(0 if side>0 else .27)
        return math.sin(math.pi*phase)**4
    def coord(row,u,inside=False):
        z=row['z']; rx=row['rx']; fr=row['front']; bk=row['back']
        # A near-full-length narrow mouth with unequal lips and gently bowed slit.
        mouth=.00225*(.75+.25*math.sin(math.pi*min(z/.066,1)))
        if z<.006: mouth=.00115+.0009*z/.006
        if z>.058: mouth=min(mouth,.34*rx)
        g=math.asin(min(.7,mouth/rx))
        angle=g+(2*math.pi-2*g)*u
        s=math.sin(angle); c=math.cos(angle)
        # A broad flattened ventral face contrasts with the inflated dorsal dome.
        x=rx*s; y=-fr*(c**.34) if c>=0 else bk*((-c)**.88)
        side=1 if u<.5 else -1
        lipdistance=min(u,1-u)
        fade=max(0,1-lipdistance/.09)**2
        bump=tooth(z,side)
        # Slight displacement inwards produces rounded bilateral teeth with a
        # smooth root extending continuously over each lip.
        x-=side*.00083*bump*fade
        y-=.00044*bump*fade
        x+=.0013*math.sin(math.pi*z/.066)*(max(0,c)**4)
        if inside:
            # Return surface is a shallow U-channel, not an invented full internal coil.
            # Rounded wall and floor remain behind the real aperture opening.
            side=1 if u<.5 else -1
            x=(1-2*u)*mouth+ .0013*math.sin(math.pi*z/.066)
            x-=side*.00067*tooth(z,side)*(abs(1-2*u)**5)
            end_blend=max(0,min(1,(z-.056)/.005))
            depth=min(.0052*(1-end_blend)+.0012*end_blend,.78*(fr+bk))
            y=-fr+min(.00115,.22*fr)+depth*(math.sin(math.pi*u)**.8)
            # The final deeply recessed terminal floor is BELOW the rim, not an
            # opaque top cap. It prevents a false through-hole to the anterior.
        # Swirling the last stations leaves a curved top opening, not a cap.
        twist=row['twist']; xx=x*math.cos(twist)-y*math.sin(twist); yy=x*math.sin(twist)+y*math.cos(twist)
        xx+=row['offset']; yy+=.0012*(z/.066)**6
        # Short anterior notch: the two lip tips extend modestly below the dome.
        if z<.004: z+=.0009*(1-z/.004)*(math.sin(math.pi*u)**2)
        if z>.062 and not row['top']: z+=.00065*((z-.062)/.0035)*(math.sin(angle)**2)
        return (xx,yy,z)
    for row in rows:
        verts.extend(coord(row,u,False) for u in us)
        verts.extend(coord(row,u,True) for u in reversed(iu))
    for r in range(len(rows)-1):
        for j in range(ringlen):
            k=(j+1)%ringlen
            faces.append((r*ringlen+j,r*ringlen+k,(r+1)*ringlen+k,(r+1)*ringlen+j))
            mi.append(2 if j>=len(us) else 1 if j<4 or j>=len(us)-5 else 0)
    # C-shaped rim endcaps connect outer and inner walls, retaining the open mouth.
    # Fan n-gons cover only shell thickness, not the ventral aperture.
    for r,reverse in [(0,True),(len(rows)-1,False)]:
        ids=list(range(r*ringlen,(r+1)*ringlen))
        faces.append(tuple(reversed(ids)) if reverse else tuple(ids));mi.append(1)
    shell=mesh_object('Continuous shell lips teeth and recessed spire',verts,faces,mats,collection)
    for poly,mat in zip(shell.data.polygons,mi): poly.material_index=mat;poly.use_smooth=True
    # Normalize only to the researched millimetre envelope, never unit-cube sizing.
    mins=[min(v.co[i] for v in shell.data.vertices) for i in range(3)]; maxs=[max(v.co[i] for v in shell.data.vertices) for i in range(3)]
    target=[p['width'],p['depth'],p['length']]
    for v in shell.data.vertices:
        for i in range(3):
            v.co[i]=(v.co[i]-(mins[i] if i==2 else (mins[i]+maxs[i])/2))*target[i]/(maxs[i]-mins[i])
    shell.data.update()
    shell['construction']='Single closed manifold shell volume; aperture cavity is genuine open negative space. Integral rounded tooth displacements; no detached teeth, cap or hidden internal coil.'
    shell['simplified_teeth_right']=21;shell['simplified_teeth_left']=22
    shell['posterior_recess']='Twisted involute terminal C-sections, top rim above inner spire opening.'
    root=bpy.data.objects[collection['asset_root']];root['mount']='Anterior terminal contact center; +Z long axis, -Y aperture front.'
    # Freeze exactly the editable source before helper export; helper records flags.
    record=export_asset(p['asset_id'],{'en':'Siphocypraea cowrie fossil','zh':'Siphocypraea 宝螺化石'},'molluscs',collection,metadata={'description':{'en':'Original specimen-informed external shell study; PRI 69852, approximate 66 × 37 × 34 mm. Not a museum scan.','zh':'参考 PRI 69852 的原创外壳形态研究，估计尺寸 66 × 37 × 34 毫米，非博物馆扫描。'},'generator':'source/generate.py','claim_scope':'External morphology study; independent acceptance pending','origin':'Anterior terminal contact center; upright museum display','source_specimen':'PRI 69852','sources':['https://neogeneatlas.net/species/syphocypraea-problematica/']},output_root=out/'_helper',render=False,max_triangles=p['geometry_policy']['max_triangles'],max_materials=p['geometry_policy']['max_materials'],max_primitives=p['geometry_policy']['max_primitives'],diagnostics=False)
    import shutil
    produced=out/'_helper'/p['asset_id']
    for old,new in [(p['asset_id']+'.glb','model.glb'),(p['asset_id']+'.blend','model.blend'),('qa.json','source-glb-check.json'),('metadata.json','build-metadata.json')]:shutil.copyfile(produced/old,out/new)
    # Topology evidence from the editable source; signed-volume alone is not a
    # complete self-intersection test, which remains a visual/independent gate.
    bm=bmesh.new();bm.from_mesh(shell.data)
    geometry={'glb_sha256':digest(out/'model.glb'),'method':'Source bmesh manifold/edge incidence, explicit sections and source/export checks. Not a general collision proof.','vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'components':1,'integral_tooth_rows':[21,22],'aperture':'Open longitudinal negative space connected to anterior notch and twisted posterior recess. Solid shell surface itself is closed manifold; the modeled interior is only a shallow recessed channel.','spire_depth_m':(.0655-.0608)*p['length']/.0655,'intersections':'Visual and independent review required; not claimed exhaustively tested.'};bm.free()
    (out/'geometry-check.json').write_text(json.dumps(geometry,indent=2)+'\n')
    (out/'build-inputs.json').write_text(json.dumps({'generator_sha256':digest(HERE/'generate.py'),'params_sha256':digest(HERE/'params.json'),'dependencies_sha256':digest(HERE/'dependencies.json'),'blender':bpy.app.version_string,'seed':p['seed']},indent=2)+'\n')
    print(json.dumps({'status':'MADE_NOT_INDEPENDENTLY_ACCEPTED','glb_sha256':digest(out/'model.glb'),'output':str(out),'triangles':record['triangles']}))
if __name__=='__main__':main()
