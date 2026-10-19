# SPDX-License-Identifier: MIT
"""Original volumetric four-creature modeling, authored after the frozen concept brief.
blender -b -t 2 --python generator.py -- --config CONFIG --output-dir OUTPUT
"""
import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sys
import time
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from asset_common import setup_scene, mesh_object, make_material, export_asset, ground_asset

class Creature:
    def __init__(self,c):
        self.c=c;self.slug=c['asset_id'];self.L=c['length_m']
        self.collection=setup_scene(self.slug,c['seed'])
        palettes={
          'sapeornis':['#AA7D4E','#EEE0BC','#715339','#D0AD77','#22302D','#CBBA97','#E2C58E','#43352B'],
          'longirostravis':['#8B9270','#E8DFBC','#615B43','#B6B58C','#25322B','#C58A51','#A49D77','#554839'],
          'dunbaria':['#B4783E','#E9CE93','#8D5B32','#D39E55','#292D29','#BE8D53','#F3DFB2','#715136'],
          'chimerarachne':['#A87650','#C7A77D','#75503B','#BC9368','#242C29','#A18259','#D2B38C','#654737']}
        self.m=[make_material(n,h,roughness=.84 if i!=4 else .5) for i,(n,h) in enumerate(zip(['body','underside','dark-structure','transition','eye','accent','light-structure','feet'],palettes[self.slug]))]

    def world(self,p):
        u,x,z=p;return (x*self.L,-u*self.L,z*self.L)

    def mesh(self,name,v,f,mat=0):
        return mesh_object(name,[self.world(p) for p in v],f,self.m[mat] if isinstance(mat,int) else mat,self.collection)

    def loft(self,name,sections,mat=0,n=12,belly=False):
        # Longitudinal section: u, half-width, half-height, center-z.
        v=[];f=[]
        for u,w,h,z in sections:
            v.extend((u,w*math.cos(2*math.pi*j/n),z+h*math.sin(2*math.pi*j/n)) for j in range(n))
        for k in range(len(sections)-1):
            for j in range(n):
                a=k*n+j;b=k*n+(j+1)%n
                f.extend([(a,b,b+n),(a,b+n,a+n)])
        v.extend([(sections[0][0],0,sections[0][3]),(sections[-1][0],0,sections[-1][3])]);a=len(v)-2;b=a+1
        for j in range(n):f.extend([(a,(j+1)%n,j),(b,(len(sections)-1)*n+j,(len(sections)-1)*n+(j+1)%n)])
        o=self.mesh(name,v,f,self.m if belly else mat)
        if belly:
            for p in o.data.polygons:
                p.material_index=1 if p.normal.z<-.22 else mat
        return o

    def ellipsoid(self,name,center,radii,mat=0,n=12,rings=6):
        u,x,z=center;a,b,c=radii;v=[(u,x,z+c)];f=[]
        for k in range(1,rings):
            t=math.pi*k/rings
            for j in range(n):
                s=2*math.pi*j/n;v.append((u+a*math.sin(t)*math.cos(s),x+b*math.sin(t)*math.sin(s),z+c*math.cos(t)))
        v.append((u,x,z-c));bot=len(v)-1
        for j in range(n):f.append((0,j+1,(j+1)%n+1))
        for k in range(rings-2):
            for j in range(n):
                a1=1+k*n+j;b1=1+k*n+(j+1)%n;f.append((a1,a1+n,b1+n,b1))
        for j in range(n):f.append((bot,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
        return self.mesh(name,v,f,mat)

    def tube(self,name,points,radii,mat=2,n=7):
        v=[];f=[];pts=[Vector(p) for p in points]
        for k,p in enumerate(pts):
            t=(pts[min(k+1,len(pts)-1)]-pts[max(k-1,0)]).normalized()
            ref=Vector((0,0,1)) if abs(t.z)<.9 else Vector((0,1,0))
            a=t.cross(ref).normalized();b=t.cross(a).normalized()
            for j in range(n):v.append(tuple(p+radii[k]*(a*math.cos(2*math.pi*j/n)+b*math.sin(2*math.pi*j/n))))
        for k in range(len(pts)-1):
            for j in range(n):
                a=k*n+j;b=k*n+(j+1)%n;f.append((a,b,b+n,a+n))
        f.extend([tuple(reversed(range(n))),tuple((len(pts)-1)*n+j for j in range(n))])
        return self.mesh(name,v,f,mat)

    def blade(self,name,start,end,width,thick,mat=2,n=8):
        # Full closed lanceolate volume: longitudinal loft oriented along a 3D axis.
        a=Vector(start);b=Vector(end);d=b-a;t=d.normalized();across=t.cross(Vector((0,0,1))).normalized()
        if across.length<.1:across=Vector((0,1,0))
        up=across.cross(t).normalized();v=[];f=[]
        for s,w in [(0,.14),(.18,.82),(.56,1),(.86,.63),(1,.05)]:
            p=a+d*s
            for j in range(n):
                q=2*math.pi*j/n;v.append(tuple(p+across*(width*w*math.cos(q))+up*(thick*max(.25,w)*math.sin(q))))
        for k in range(4):
            for j in range(n):
                x=k*n+j;y=k*n+(j+1)%n;f.append((x,y,y+n,x+n))
        f.extend([tuple(reversed(range(n))),tuple(4*n+j for j in range(n))])
        return self.mesh(name,v,f,mat)

    def eyes(self,u,x,z,r=.025):
        for s in [-1,1]:self.ellipsoid(('left' if s<0 else 'right')+'-eye',(u,s*x,z),(r,r*.42,r),4,n=10,rings=5)

    def bird(self,spread):
        z=0 if spread else .38
        self.loft('feathered-body',[(-.39,.035,.045,z),(-.28,.13,.14,z),(-.08,.175,.19,z+.015),(.15,.15,.18,z+.04),(.28,.09,.13,z+.09),(.34,.055,.10,z+.14)],belly=True,n=16)
        self.loft('neck',[ (.16,.09,.09,z+.1),(.25,.095,.12,z+.19),(.33,.085,.11,z+.25),(.39,.07,.07,z+.26)],belly=True)
        self.ellipsoid('head',(.38,0,z+.27),(.14,.105,.115),0,n=16,rings=8)
        self.ellipsoid('throat',(.42,0,z+.205),(.105,.09,.065),1)
        self.eyes(.425,.096,z+.30,.026)
        if spread:
            self.loft('short-snouted-jaw',[(.46,.055,.036,z+.24),(.54,.038,.025,z+.222),(.585,.008,.007,z+.209)],2,n=8)
        else:
            self.loft('slender-downcurved-rostrum',[(.46,.043,.026,z+.25),(.55,.026,.023,z+.24),(.65,.015,.017,z+.215),(.74,.008,.010,z+.17),(.78,.004,.006,z+.13)],2,n=8)
            for s in [-1,1]:self.ellipsoid('rust-cheek-'+str(s),(.36,s*.098,z+.245),(.047,.012,.035),5,n=10,rings=5)
        for s in [-1,1]:
            side='left' if s<0 else 'right'
            if spread:
                self.blade(side+'-wing-arm',(.14,s*.12,z+.06),(-.03,s*.64,z+.12),.13,.047,0)
                self.blade(side+'-wing-hand',(-.03,s*.57,z+.11),(-.16,s*1.02,z+.10),.10,.035,0)
                for j in range(9):
                    x=.24+j*.077;u=.10-j*.035
                    self.blade(side+f'-secondary-{j}',(u,s*x,z+.115),(u-.36,s*(x+.04),z+.055),.061,.014,2 if j%3 else 0)
                for j in range(7):
                    x=.76+j*.052;u=-.015-j*.038
                    self.blade(side+f'-primary-{j}',(u,s*x,z+.11),(-.29+j*.035,s*(.97+j*.049),z+.085-j*.007),.075,.016,2)
                for j in range(8):
                    x=.21+j*.095
                    self.blade(side+f'-covert-{j}',(.10-j*.029,s*x,z+.15),(-.055-j*.028,s*(x+.045),z+.16),.052,.015,3 if j<4 else 1)
                ankle=(-.11,s*.07,z-.20)
                self.tube(side+'-tucked-leg',[(-.13,s*.09,z-.1),(-.03,s*.08,z-.17),ankle],[.025,.018,.013],7)
                for j in [-1,0,1]:self.tube(side+f'-tucked-toe-{j}',[ankle,(-.18,s*.07+j*.025,z-.21),(-.22,s*.07+j*.028,z-.20)],[.012,.009,.006],7,n=6)
            else:
                self.blade(side+'-folded-wing',(.15,s*.16,z+.095),(-.46,s*.14,z-.07),.105,.045,2)
                for j in range(5):
                    self.blade(side+f'-wing-covert-{j}',(.17-j*.07,s*.19,z+.10-j*.01),(-.03-j*.07,s*.20,z+.02-j*.012),.058,.022,0 if j<3 else 3)
                self.tube(side+'-leg',[(-.06,s*.085,z-.1),(-.13,s*.09,.17),(-.025,s*.105,.035)],[.027,.019,.013],7)
                for j in [-1,0,1]:self.tube(side+f'-toe-{j}',[(-.025,s*.105,.035),(.08,s*.105+j*.04,.015),(.13,s*.105+j*.045,.012)],[.013,.009,.006],7,n=6)
                self.tube(side+'-back-toe',[(-.025,s*.105,.035),(-.12,s*.105,.02),(-.15,s*.105,.014)],[.012,.009,.006],7,n=6)
        if spread:
            for j in range(9):
                a=(j-4)*.11
                self.blade(f'tail-fan-{j}',(-.28,a*.25,z-.005),(-.70+abs(a)*.20,a*.60,z-.06),.046,.012,0 if j%2 else 3)
        else:
            for s in [-1,1]:self.blade('paired-tail-'+str(s),(-.29,s*.04,z+.01),(-.99,s*.065,z-.035),.033,.010,3)

    def insect_wing(self,name,s,root,span,sweep,chord):
        # Station-based closed wing with integrated structural colour bands.
        v=[];f=[];steps=[(0,.022),(.15,.115),(.38,chord),(.58,chord*.94),(.78,chord*.70),(.94,chord*.35),(1,.007)]
        for t,w in steps:
            u=root-sweep*t;x=s*(.07+span*t);z=.13+.035*math.sin(math.pi*t)
            v.extend([(u+w*.5,x,z),(u,x,z+.012),(u-w*.5,x,z),(u,x,z-.009)])
        for k in range(len(steps)-1):
            for j in range(4):
                a=k*4+j;b=k*4+(j+1)%4;f.append((a,b,b+4,a+4))
        f.extend([(3,2,1,0),tuple((len(steps)-1)*4+j for j in range(4))])
        o=self.mesh(name,v,f,self.m)
        for p in o.data.polygons:
            t=abs(p.center.x)/self.L/span if False else 0
            k=p.index//4
            p.material_index=2 if k in [2,4] else 1
        # Sparse main vein stays within the thick wing surface.
        self.tube(name+'-costa',[(root,.07*s,.132),(root-sweep*.45,s*(.07+span*.45),.165),(root-sweep*.9,s*(.07+span*.9),.145)],[.009,.007,.004],5,n=6)

    def insect(self):
        self.loft('segmented-abdomen',[(-.53,.014,.02,.10)]+[(-.50+i*.047,.038+.015*math.sin(i*.34),.039+.010*math.sin(i*.34),.10) for i in range(11)],0,n=10)
        # Continuous regional dorsal bands, no random polygon colour noise.
        body=bpy.data.objects['segmented-abdomen'];body.data.materials.append(self.m[3])
        for p in body.data.polygons:
            if (p.index//20)%2:p.material_index=1
        self.loft('thorax',[(-.03,.055,.055,.12),(.09,.08,.07,.13),(.20,.06,.053,.14),(.24,.045,.04,.14)],0,n=12)
        self.ellipsoid('head',(.29,0,.14),(.07,.057,.06),0)
        self.eyes(.305,.05,.16,.032)
        for s in [-1,1]:
            side='left' if s<0 else 'right'
            self.insect_wing(side+'-forewing',s,.14,.78,-.04,.24)
            self.insect_wing(side+'-hindwing',s,-.025,.72,.35,.23)
            self.blade(side+'-small-prothoracic-lobe',(.205,s*.045,.175),(.265,s*.20,.20),.060,.018,3)
            self.tube(side+'-antenna',[(.32,s*.027,.18),(.41,s*.06,.22),(.48,s*.11,.22)],[.009,.006,.004],2,n=6)
            for j in range(3):
                u=.15-j*.105
                self.tube(side+f'-walking-leg-{j}',[(u,s*.055,.105),(u+.045-j*.02,s*.15,.08),(u+.08-j*.055,s*.22,.012),(u+.12-j*.06,s*.25,.008)],[.018,.015,.009,.006],7)
            self.tube(side+'-cercus',[(-.51,s*.018,.10),(-.72,s*.06,.105),(-.93,s*.10,.14)],[.009,.006,.004],2,n=6)
        self.tube('piercing-rostrum',[(.33,0,.12),(.46,0,.045),(.62,0,-.005)],[.017,.012,.006],2)

    def arachnid(self):
        self.loft('segmented-opisthosoma',[(-.59,.07,.075,.23),(-.52,.14,.12,.25),(-.42,.18,.145,.26),(-.31,.19,.15,.26),(-.20,.175,.14,.25),(-.09,.14,.11,.23),(-.02,.07,.07,.22)],0,n=10)
        for j in range(5):
            u=-.48+j*.093
            self.tube('dorsal-segment-boundary-'+str(j),[(u,-.12,.31),(u,0,.405-abs(j-2)*.01),(u,.12,.31)],[.016,.019,.016],3,n=6)
        self.loft('front-body',[(-.06,.06,.06,.22),(.02,.16,.07,.23),(.16,.18,.085,.245),(.29,.13,.07,.24),(.34,.07,.05,.22)],0,n=12)
        for s in [-1,1]:
            for j in range(4):
                u=.24-j*.075
                kneeu=[.51,.32,-.12,-.42][j];footu=[.68,.43,-.28,-.63][j]
                self.tube(('left' if s<0 else 'right')+f'-walking-leg-{j+1}',[(u,s*.12,.23),(kneeu,s*(.30+j*.035),.36),(footu,s*(.48+j*.035),.14),(footu+.025,s*(.55+j*.025),.018)],[.036,.029,.021,.015],2 if j%2 else 0,n=7)
            self.tube('small-pedipalp-'+str(s),[(.30,s*.07,.20),(.41,s*.10,.17),(.46,s*.085,.12)],[.035,.027,.020],1)
            self.ellipsoid('chelicera-'+str(s),(.345,s*.032,.165),(.055,.029,.032),2,n=8,rings=4)
            self.ellipsoid('small-eye-'+str(s),(.285,s*.065,.292),(.026,.019,.025),4,n=8,rings=4)
            for j in range(2):
                self.tube('underside-spinneret-'+str(s)+'-'+str(j),[(-.46+j*.07,s*.052,.16),(-.49+j*.07,s*.055,.105)],[.024,.016],1,n=6)
        # Long slender curve made from many real tapered mesh stations; not a sting.
        points=[];r=[]
        for k in range(17):
            t=k/16;points.append((-.56-1.10*t,.26*math.sin(t*math.pi*.85),.23+.12*math.sin(math.pi*t)))
            r.append(.031*(1-t)+.012*t)
        self.tube('segmented-whip-tail',points,r,2,n=7)

    def build(self):
        if self.slug in ['sapeornis','longirostravis']:self.bird(self.slug=='sapeornis')
        elif self.slug=='dunbaria':self.insect()
        else:self.arachnid()
        if self.slug!='sapeornis':ground_asset(self.collection,center_xy=True)

def main():
    argv=sys.argv[sys.argv.index('--')+1:];p=argparse.ArgumentParser();p.add_argument('--config',required=True,type=Path);p.add_argument('--output-dir',required=True,type=Path);a=p.parse_args(argv)
    started=datetime.now(timezone.utc).isoformat();tic=time.monotonic();c=json.loads(a.config.read_text());obj=Creature(c);obj.build()
    brief=json.loads((a.config.parent/'brief.json').read_text())
    export_asset(obj.slug,{'en':brief['label'],'zh':brief['label_zh']},'small-life',obj.collection,metadata={'description':{'en':brief['design'],'zh':'原创自然配色低多边形场景生物；仅候选，非科学复原。'},'claim_scope':brief['scope'],'generator':str(Path(__file__).relative_to(REPO)),'sources':json.loads((a.config.parent/'references.json').read_text())['sources'],'reconstruction_notes':brief['concept_interpretation'],'origin_detail':c['mount_origin']},output_root=a.output_dir,render=False,max_triangles=c['max_triangles'],max_materials=c['max_materials'],max_primitives=c['max_primitives'],collection_id='candidate')
    (a.output_dir/obj.slug/'build-timing.json').write_text(json.dumps({'started_at':started,'completed_at':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-tic,'blender_version':bpy.app.version_string,'generator':str(Path(__file__).relative_to(REPO))},indent=2)+'\n')

if __name__=='__main__':main()
