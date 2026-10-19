# SPDX-License-Identifier: MIT
"""Original concept-guided marine quartet. Blender 4.3.2; meters, -Y forward.
Run in cloud: blender -b -t 2 --python-exit-code 1 --python generator.py -- --config FILE --output-dir DIR
Closed authored profile shells, radial plate lofts and tapered path tubes; no borrowed meshes.
"""
import argparse
from datetime import datetime, timezone
import json, math, sys, time
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,ground_asset,export_asset

def utc():return datetime.now(timezone.utc).isoformat()

class Marine:
    def __init__(self,c):
        self.c=c;self.slug=c['asset_id'];self.L=c['unit_m'];self.col=setup_scene(self.slug,c['seed'])
        colors={
          'emeraldella':['#76A7A1','#DFD5B8','#4F7B79','#A4C2B2','#AC8E61','#223540'],
          'burgessia':['#D9A067','#F0D2A5','#B37E4C','#E5B784','#BA966C','#223540'],
          'tuzoia':['#AC758A','#E8C6AE','#7E526D','#D39A9A','#B89C74','#28313D'],
          'sanctacaris':['#7799AF','#E7D5B6','#506F8A','#A4BAC7','#C5AA7F','#233340']}
        self.m=[make_material(n,color,roughness=.77 if i!=5 else .47) for i,(n,color) in enumerate(zip(['shell','underside','ridge','transition','limb','eye'],colors[self.slug]))]
    def mesh(self,name,v,f,mat=0):
        return mesh_object(name,[tuple(a*self.L for a in p) for p in v],f,self.m[mat],self.col)
    def tube(self,name,pts,r,mat=4,n=7):
        # Parallel local rings follow the centerline; capped closed tips retain visible volume.
        points=[Vector(p) for p in pts];v=[];f=[]
        radii=[r]*len(points) if isinstance(r,(int,float)) else r
        for i,p in enumerate(points):
            tangent=(points[min(i+1,len(points)-1)]-points[max(i-1,0)]).normalized()
            up=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((1,0,0))
            a=tangent.cross(up).normalized();b=tangent.cross(a).normalized()
            for j in range(n):v.append(p+max(radii[i],.004)*(a*math.cos(2*math.pi*j/n)+b*math.sin(2*math.pi*j/n)))
        for i in range(len(points)-1):
            for j in range(n):f.append((i*n+j,i*n+(j+1)%n,(i+1)*n+(j+1)%n,(i+1)*n+j))
        f.extend([tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+j for j in range(n))])
        return self.mesh(name,v,f,mat)
    def dome(self,name,outline,z,h,mat=0):
        # Four closed cross sections; broad deliberate facets follow the shell, not noise.
        N=len(outline);cx=sum(p[0] for p in outline)/N;cy=sum(p[1] for p in outline)/N
        v=[];f=[]
        for radius,height in [(1,-.05),(1,.08),(.76,.67),(.38,.94)]:
            for x,y in outline:v.append((cx+(x-cx)*radius,cy+(y-cy)*radius,z+h*height))
        v.extend([(cx,cy,z+h),(cx,cy,z-h*.05)]);top=4*N;bottom=top+1
        for k in range(3):
            for j in range(N):
                a=k*N+j;b=k*N+(j+1)%N;c=b+N;d=a+N
                f.extend([(a,b,c),(a,c,d)] if (j+k)%2 else [(a,b,d),(b,c,d)])
        for j in range(N):f.extend([(top,3*N+j,3*N+(j+1)%N),(bottom,(j+1)%N,j)])
        return self.mesh(name,v,f,mat)
    def oval(self,name,center,radii,mat=0,n=12,rings=6):
        x,y,z=center;rx,ry,rz=radii;v=[(x,y,z+rz)];f=[]
        for k in range(1,rings):
            a=math.pi*k/rings
            for j in range(n):
                b=2*math.pi*j/n;v.append((x+rx*math.sin(a)*math.cos(b),y+ry*math.sin(a)*math.sin(b),z+rz*math.cos(a)))
        v.append((x,y,z-rz));bot=len(v)-1
        for j in range(n):f.append((0,1+j,1+(j+1)%n))
        for k in range(rings-2):
            for j in range(n):
                a=1+k*n+j;b=1+k*n+(j+1)%n;f.append((a,b,b+n,a+n))
        for j in range(n):f.append((bot,1+(rings-2)*n+(j+1)%n,1+(rings-2)*n+j))
        return self.mesh(name,v,f,mat)
    def leaf(self,name,a,b,width,mat=1):
        # Thick lens with four perimeter corners, ridge and belly: closed swimming lobe.
        a=Vector(a);b=Vector(b);d=b-a;cross=d.cross(Vector((0,0,1))).normalized()*width
        mid=a+d*.56
        v=[a,mid+cross,b,mid-cross,mid+Vector((0,0,width*.23)),mid-Vector((0,0,width*.23))]
        f=[]
        for j in range(4):f.extend([(4,j,(j+1)%4),(5,(j+1)%4,j)])
        return self.mesh(name,v,f,mat)
    def shield(self,name,width,front,rear,z,h,mat=0):
        outline=[(width*math.cos(math.pi*j/12),rear-(rear-front)*math.sin(math.pi*j/12)) for j in range(13)]
        return self.dome(name,outline,z,h,mat)
    def trunk(self,count,start,step,widths,z=.13,h=.12):
        for i,w in enumerate(widths):
            y=start+i*step
            outline=[(-w*.8,y-step*.48),(0,y-step*.68),(w*.8,y-step*.48),(w,y+step*.25),(w*.76,y+step*.68),(0,y+step*.84),(-w*.76,y+step*.68),(-w,y+step*.25)]
            self.dome(f'trunk-plate-{i+1:02}',outline,z,h*(1-i*.035),0)
    def walking_pair(self,y,w,i,z=.11,spread=.17):
        for s,side in [(-1,'left'),(1,'right')]:
            self.tube(f'{side}-walking-{i:02}',[(s*w*.6,y,z),(s*(w+spread*.5),y+.015,z-.055),(s*(w+spread),y-.03,-.11)],[.020,.014,.005])
    def antennae(self,root_y,tip_y,width=.18,spread=.40,z=.13):
        # Named R2 contour improvement: a deliberate cubic arc replaces hard kinks.
        for s,side in [(-1,'left'),(1,'right')]:
            controls=[Vector((s*width,root_y,z)),Vector((s*(width+.42),root_y-.20,z+.06)),Vector((s*(spread+.18),tip_y+.15,z+.07)),Vector((s*spread,tip_y,z-.02))]
            points=[];radii=[]
            for i in range(13):
                t=i/12;u=1-t
                points.append(controls[0]*u**3+controls[1]*3*u*u*t+controls[2]*3*u*t*t+controls[3]*t**3)
                radii.append(.004+.016*(1-t)**1.25)
            self.tube(side+'-antenna',points,radii,2,8)
    def eyes(self,y,x,z,r=.04):
        for s,side in [(-1,'left'),(1,'right')]:
            self.tube(side+'-eye-stalk',[(s*x*.8,y+.05,z-.03),(s*x,y,z)],[r*.50,r*.47],4,8)
            self.oval(side+'-eye',(s*x,y,z),(r,r*.9,r),5,12,6)
    def emeraldella(self):
        self.shield('smooth-eyeless-head',.31,-.57,-.17,.13,.19)
        self.oval('ventral-soft-body',(0,.04,.08),(.18,.42,.065),1)
        widths=[.29,.29,.28,.26,.24,.22,.20,.18,.15,.12,.09]
        self.trunk(11,-.12,.060,widths)
        for i,w in enumerate(widths):
            y=-.12+i*.060;self.walking_pair(y,w,i)
            for s,side in [(-1,'left'),(1,'right')]:
                self.leaf(f'{side}-swimming-lobe-{i:02}',(s*w*.65,y,.105),(s*(w+.15),y+.09,.055),.037)
        # Five understated cephalic pairs preserve the head underside's limb-bearing role.
        for i in range(5):
            y=-.42+i*.05
            for s,side in [(-1,'left'),(1,'right')]:
                self.tube(f'{side}-cephalic-branch-{i}',[(s*.12,y,.09),(s*(.22+i*.014),y-.04,-.01),(s*(.28+i*.008),y-.07,-.08)],[.015,.010,.005])
        for i,y in enumerate([.59,.67]):self.oval(f'posterior-ring-{i+1}',(0,y,.15),(.078-i*.018,.060,.075-i*.012),2,12,5)
        self.tube('continuous-tail-spine',[(0,.70,.15),(.008,.92,.18),(.014,1.17,.23),(.02,1.42,.29)],[.044,.027,.014,.004],2,10)
        self.antennae(-.48,-1.38,.17,.43)
    def burgessia(self):
        self.shield('single-eyeless-carapace',.60,-.70,.30,.12,.18)
        # Thin rim follows full outline, not a painted ring.
        pts=[(.60*math.cos(math.pi*j/16),.30-math.sin(math.pi*j/16),.12) for j in range(17)]
        self.tube('carapace-rim',pts,[.012]*len(pts),1,7)
        self.oval('ventral-body',(0,-.16,.06),(.27,.38,.07),1)
        for i in range(10):
            y=-.48+i*.075;self.walking_pair(y,.36,i,z=.07,spread=.24)
            for s,side in [(-1,'left'),(1,'right')]:
                if i>=3:self.leaf(f'{side}-gill-branch-{i}',(s*.22,y,.06),(s*.43,y+.02,.015),.022)
        for s,side in [(-1,'left'),(1,'right')]:self.tube(side+'-terminal-short-appendage',[(s*.14,.26,.06),(s*.23,.38,-.01)],[.018,.006])
        self.tube('single-unsegmented-tail-spine',[(0,.29,.14),(0,.65,.155),(.008,1.10,.17),(.02,1.70,.19)],[.035,.025,.014,.004],2,10)
        self.antennae(-.48,-1.45,.21,.68,z=.10)
    def tuzoia(self):
        # Paired vertical valves: YZ outline with a flat top hinge, convex outer face.
        outline=[(-.49,.62),(-.29,.66),(.30,.66),(.50,.60),(.56,.43),(.52,.25),(.36,.10),(0,.055),(-.34,.11),(-.53,.29),(-.56,.45)]
        for s,side in [(-1,'left'),(1,'right')]:
            n=len(outline);cy=sum(y for y,z in outline)/n;cz=sum(z for y,z in outline)/n;v=[];f=[]
            for radius,depth in [(1,.025),(.76,.17),(.40,.245)]:
                for y,z in outline:v.append((s*depth,cy+(y-cy)*radius,cz+(z-cz)*radius))
            v.extend([(s*.27,cy,cz),(s*.014,cy,cz)]);ap=3*n;inn=ap+1
            for k in range(2):
                for j in range(n):
                    a=k*n+j;b=k*n+(j+1)%n;c=b+n;d=a+n;f.extend([(a,b,c),(a,c,d)])
            for j in range(n):f.extend([(ap,2*n+j,2*n+(j+1)%n),(inn,(j+1)%n,j)])
            self.mesh(side+'-deep-valve',v,f,0)
            self.tube(side+'-lateral-keel',[(s*.065,-.52,.36),(s*.22,-.31,.35),(s*.29,0,.35),(s*.22,.31,.35),(s*.065,.52,.36)],[.019,.026,.027,.025,.015],3,7)
            for j,(y,z) in enumerate([(-.39,.125),(-.15,.066),(.12,.071),(.36,.13),(.50,.25)]):
                self.tube(f'{side}-margin-spine-{j}',[(s*.045,y,z),(s*.13,y+.055,z-.065)],[.022,.004],4,7)
            for i in range(6):
                y=-.34+i*.12
                self.tube(f'{side}-walking-{i}',[(s*.05,y,.19),(s*.18,y-.025,.06),(s*.19,y-.08,-.045)],[.019,.013,.004],4,7)
                self.leaf(f'{side}-small-swimming-branch-{i}',(s*.03,y,.15),(s*.16,y+.06,.07),.032,1)
            for i in range(2):self.leaf(f'{side}-caudal-fan-{i}',(s*.035,.49,.25),(s*(.12+i*.07),.76-i*.02,.23+i*.08),.064,3)
        self.tube('straight-dorsal-hinge',[(0,-.49,.63),(0,-.25,.663),(0,.30,.663),(0,.50,.61)],[.023,.024,.024,.017],2,9)
        for y,d in [(-.50,-1),(.50,1)]:self.tube('hinge-process-'+str(d),[(0,y,.62),(0,y+d*.14,.63)],[.022,.004],2,8)
        self.oval('small-ventral-trunk',(0,-.02,.24),(.065,.43,.11),1)
        # R3 connection repair: explicit projecting head encloses the eye/antenna roots
        # and overlaps the ventral trunk. A visible anatomical volume, not a render patch.
        self.oval('projecting-anterior-head',(0,-.51,.32),(.16,.13,.11),1,14,6)
        self.eyes(-.58,.14,.39,.044)
        self.antennae(-.53,-.94,.07,.23,z=.26)
    def sanctacaris(self):
        outline=[(-.50,-.03),(-.27,-.35),(-.17,-.46),(0,-.53),(.17,-.46),(.27,-.35),(.50,-.03),(.20,-.15),(-.20,-.15)]
        self.dome('angular-winged-head',outline,.15,.20)
        self.oval('ventral-body',(0,.06,.10),(.17,.43,.08),1)
        widths=[.255,.255,.25,.24,.23,.21,.19,.17,.15,.13,.105]
        self.trunk(11,-.12,.061,widths,z=.15,h=.135)
        for i,w in enumerate(widths):
            y=-.12+i*.061
            self.walking_pair(y,w,i,z=.12,spread=.12)
            for s,side in [(-1,'left'),(1,'right')]:self.leaf(f'{side}-swimming-flap-{i:02}',(s*w*.55,y,.10),(s*(w+.19),y+.09,.045),.042)
        tail=[(-.08,.54),(.08,.54),(.19,.73),(.17,.88),(0,.94),(-.17,.88),(-.19,.73)]
        self.dome('broad-paddle-telson',tail,.14,.045,3)
        self.eyes(-.39,.22,.20,.037)
        for i in range(6):
            x=.055+i*.038;y=-.30+i*.012;tipx=.08+i*.073;tipy=-.99+i*.061
            for s,side in [(-1,'left'),(1,'right')]:
                pts=[(s*x,y,.12),(s*(x+.035),-.57+i*.014,.10),(s*tipx,tipy+.10,.065),(s*(tipx-.016),tipy,.105)]
                self.tube(f'{side}-frontal-grasping-{i+1}',pts,[.021,.018,.012,.005],4,8)
                # A separately legible narrow sensory branch joins at the limb base.
                self.tube(f'{side}-frontal-sensory-{i+1}',[pts[0],(s*(x+.01),-.58+i*.028,.20),(s*(tipx-.028),tipy+.08,.24)],[.010,.007,.004],2,6)
                p=pts[2]
                self.tube(f'{side}-frontal-blunt-hook-{i+1}',[p,(p[0]-s*.038,p[1]-.02,p[2]+.024)],[.010,.004],1,6)
    def build(self):getattr(self,self.slug)()

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);c=json.loads(a.config.read_text());start=utc();clock=time.monotonic()
    obj=Marine(c);obj.build();shift=ground_asset(obj.col,center_xy=True)
    metadata={'reconstruction':'Stylized evidence-informed scene prop, not scientific reconstruction','generator':str(Path(__file__).relative_to(REPO)),'config_sha256':__import__('hashlib').sha256(a.config.read_bytes()).hexdigest(),'origin_notes':c['mount_origin'],'ground_shift_m':shift,'description':'Original child-friendly concept-guided marine scene creature. Palette and pose artistic; fine anatomy generalized.','independent_qa':'pending parent review','gallery_poster':'pending parent unified gallery renderer; proof frames are diagnostics only'}
    rec=export_asset(obj.slug,obj.slug.title()+'-inspired scene creature','animals',obj.col,metadata=metadata,output_root=a.output_dir.parent,render=False,max_triangles=c['max_triangles'],max_materials=c['max_materials'],max_primitives=c['max_primitives'])
    produced=a.output_dir.parent/obj.slug
    if produced!=a.output_dir:
        a.output_dir.mkdir(parents=True,exist_ok=True)
        for f in produced.iterdir():f.rename(a.output_dir/f.name)
        produced.rmdir()
    (a.output_dir/'build-timing.json').write_text(json.dumps({'started_at':start,'finished_at':utc(),'wall_seconds':time.monotonic()-clock,'blender':bpy.app.version_string,'stage':'modeling_export_execution','authoring_time':'separate events.jsonl; not included in this execution measurement','config':str(a.config),'source_vertices':sum(len(o.data.vertices) for o in obj.col.all_objects if o.type=='MESH')},indent=2)+'\n')
if __name__=='__main__':main()
