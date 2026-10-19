# SPDX-License-Identifier: MIT
"""Original four-fish profile modeling. Blender 4.3.2, cloud-only.
blender -b -t 2 --python-exit-code 1 --python generator.py -- --config CONFIG --output-dir OUTPUT
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

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p/'scripts/asset_common.py').exists())
sys.path.insert(0,str(REPO/'scripts'))
from asset_common import setup_scene, mesh_object, make_material, export_asset


class Fish:
    def __init__(self,config):
        self.config=config
        self.slug=config['asset_id']
        self.length=config['length_m']
        self.collection=setup_scene(self.slug,config['seed'])
        palettes={
          'metaspriggina':['#DB998C','#F2D5BC','#BA716C','#E9B5A1','#192F39','#F4ECE0'],
          'falcatus':['#709D98','#E9DBBB','#4C7778','#A4C2B2','#192F39','#F4ECE0'],
          'pteraspis':['#CDA66A','#E5C592','#9E784C','#82715E','#192F39','#F4ECE0'],
          'dorypterus':['#A498C5','#E9D9CE','#7A739C','#BDB0D4','#192F39','#F4ECE0']}
        self.materials=[make_material(n,c,roughness=.78 if i<4 else .48) for i,(n,c) in enumerate(zip(['body','belly','landmark','transition','eye','eye-rim'],palettes[self.slug]))]

    def v(self,u,x,z):
        return (x*self.length,-u*self.length,z*self.length)

    def mesh(self,name,verts,faces,mat=0):
        return mesh_object(name,[self.v(*v) for v in verts],faces,self.materials[mat] if isinstance(mat,int) else mat,self.collection)

    def loft(self,name,sections,sides=16,mat=0,belly=True):
        # Each section is longitudinal position, half width, half height, center Z.
        verts=[];faces=[]
        for u,w,h,z in sections:
            for j in range(sides):
                a=2*math.pi*j/sides
                verts.append((u,w*math.cos(a),z+h*math.sin(a)))
        for k in range(len(sections)-1):
            for j in range(sides):
                a=k*sides+j;b=k*sides+(j+1)%sides;c=b+sides;d=a+sides
                # Deliberate diagonal alternation follows loft stations, without vertex noise.
                faces.extend([(a,b,c),(a,c,d)] if (j+k)%2 else [(a,b,d),(b,c,d)])
        verts.append((sections[0][0],0,sections[0][3]));s=len(verts)-1
        verts.append((sections[-1][0],0,sections[-1][3]));e=len(verts)-1
        for j in range(sides):
            faces.extend([(s,(j+1)%sides,j),(e,(len(sections)-1)*sides+j,(len(sections)-1)*sides+(j+1)%sides)])
        mats=self.materials if belly else self.materials[mat]
        obj=self.mesh(name,verts,faces,mats)
        if belly:
            for f in obj.data.polygons:
                z=sum(obj.data.vertices[i].co.z for i in f.vertices)/len(f.vertices)/self.length
                # Quiet, coherent regional colours; no per-face random palette.
                f.material_index=1 if z<-.035 else mat
        return obj

    def ellipsoid(self,name,center,radii,mat=0,sides=16,rings=6):
        u,x,z=center;ru,rx,rz=radii
        verts=[(u,x,z+rz)];faces=[]
        for k in range(1,rings):
            a=math.pi*k/rings
            for j in range(sides):
                b=2*math.pi*j/sides
                verts.append((u+ru*math.sin(a)*math.cos(b),x+rx*math.sin(a)*math.sin(b),z+rz*math.cos(a)))
        verts.append((u,x,z-rz));bot=len(verts)-1
        for j in range(sides):faces.append((0,1+j,1+(j+1)%sides))
        for k in range(rings-2):
            for j in range(sides):
                a=1+k*sides+j;b=1+k*sides+(j+1)%sides
                faces.append((a,a+sides,b+sides,b))
        for j in range(sides):faces.append((bot,1+(rings-2)*sides+(j+1)%sides,1+(rings-2)*sides+j))
        return self.mesh(name,verts,faces,mat)

    def eye_pair(self,u,w,z,r):
        for sign,label in [(-1,'left'),(1,'right')]:
            self.ellipsoid(label+'-eye-rim',(u,sign*w,z),(r, r*.27,r),5,16,6)
            self.ellipsoid(label+'-eye',(u+r*.03,sign*(w+r*.19),z),(r*.76,r*.19,r*.76),4,16,6)
            self.ellipsoid(label+'-catchlight',(u+r*.23,sign*(w+r*.35),z+r*.28),(r*.15,r*.06,r*.15),5,8,4)

    def fin(self,name,points,x=0,thick=.006,mat=2):
        # Closed biconvex fin. Ridge thickness is larger than border thickness.
        n=len(points);u=sum(p[0] for p in points)/n;z=sum(p[1] for p in points)/n
        verts=[]
        for sign in [-1,1]:
            verts.extend((a,x+sign*thick*.25,b) for a,b in points)
        verts.extend([(u,x-thick,z),(u,x+thick,z)])
        faces=[]
        for j in range(n):
            k=(j+1)%n
            faces.extend([(2*n,j,k),(2*n+1,n+k,n+j),(j,n+j,n+k,k)])
        return self.mesh(name,verts,faces,mat)

    def blade(self,name,points,mat=2):
        # points: u,x,z, thickness. Tube follows path, with real closed volume.
        n=8;verts=[];faces=[]
        for u,x,z,r in points:
            verts.extend((u+r*math.cos(2*math.pi*j/n),x+r*.6*math.sin(2*math.pi*j/n),z) for j in range(n))
        for k in range(len(points)-1):
            for j in range(n):faces.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
        faces.extend([tuple(range(n-1,-1,-1)),tuple((len(points)-1)*n+j for j in range(n))])
        return self.mesh(name,verts,faces,mat)

    def paired_fin(self,name,root,tip,rear,mat=0):
        # Wedge with a central dorsal ridge, symmetric pair with positive geometry.
        for s,label in [(-1,'left'),(1,'right')]:
            pts=[root,tip,rear]
            verts=[(u,s*x,z+dz) for dz in [-.004,.004] for u,x,z in pts]
            verts.extend([(sum(p[0] for p in pts)/3,s*sum(p[1] for p in pts)/3,sum(p[2] for p in pts)/3+.012)])
            faces=[(0,2,1),(0,1,4,3),(1,2,5,4),(2,0,3,5),(3,4,6),(4,5,6),(5,3,6)]
            self.mesh(label+'-'+name,verts,faces,mat)

    def build(self):
        if self.slug=='metaspriggina':self.metaspriggina()
        elif self.slug=='falcatus':self.falcatus()
        elif self.slug=='pteraspis':self.pteraspis()
        elif self.slug=='dorypterus':self.dorypterus()

    def metaspriggina(self):
        self.loft('soft-body',[(-.49,.009,.010,0),(-.4,.022,.025,.006),(-.28,.04,.046,.009),(-.14,.057,.067,.01),(0,.073,.083,.008),(.14,.083,.089,0),(.26,.079,.078,-.006),(.35,.061,.06,-.009),(.40,.034,.037,-.006),(.416,.008,.015,-.003)],20)
        self.eye_pair(.326,.057,.024,.034)
        self.fin('continuous-dorsal-tail-fold',[(-.48,.003),(-.52,.065),(-.44,.037),(-.30,.071),(-.12,.098),(.02,.106),(.14,.083),(-.23,.038)],thick=.004,mat=3)
        self.fin('ventral-tail-fold',[(-.49,.003),(-.49,-.037),(-.40,-.026),(-.28,-.018),(-.18,-.035),(-.29,-.03)],thick=.003,mat=3)
        # Seven paired rounded gill-region ribs, following the side envelope.
        for i in range(7):
            u=.23-i*.037
            w=.081 if i<4 else .079-(i-4)*.0018
            h=.086 if i<4 else .090
            for s,label in [(-1,'left'),(1,'right')]:
                self.blade(f'{label}-gill-region-{i+1}',[(u-.007,s*w*.67,h*.72,.004),(u-.012,s*w*.96,h*.30,.0045),(u-.009,s*w*1.025,-h*.15,.0045),(u,s*w*.80,-h*.59,.0035)],2)
        # Three broad chevron muscle cues in posterior, all restrained in one value.
        for i in range(3):
            u=-.14-i*.075;w=.05-i*.01
            for s,label in [(-1,'left'),(1,'right')]:
                self.blade(f'{label}-myomere-cue-{i}',[(u,s*w*.7,.043-i*.008,.0018),(u-.025,s*w,.007,.0018),(u,s*w*.7,-.03+i*.006,.0018)],3)

    def falcatus(self):
        self.loft('fusiform-body',[(-.37,.009,.014,0),(-.29,.024,.031,.004),(-.17,.045,.055,.003),(-.04,.066,.072,.002),(.10,.079,.081,0),(.23,.072,.069,-.004),(.33,.054,.053,-.007),(.39,.031,.031,-.01),(.414,.007,.013,-.01)],20)
        self.eye_pair(.297,.052,.017,.034)
        self.fin('heterocercal-caudal',[(-.35,.01),(-.47,.20),(-.54,.232),(-.485,.085),(-.46,.015),(-.51,-.115),(-.447,-.085),(-.376,-.018)],thick=.007,mat=2)
        self.paired_fin('pectoral',(.14,.055,-.028),(-.07,.22,-.11),(-.09,.061,-.055),0)
        self.paired_fin('pelvic',(-.14,.035,-.04),(-.25,.11,-.084),(-.27,.026,-.035),0)
        self.fin('posterior-dorsal',[(-.16,.048),(-.185,.104),(-.225,.115),(-.225,.043)],thick=.004,mat=2)
        # Spine is a curved closed loft with a visible separate tip above head.
        self.blade('male-forward-sword-spine',[(.085,0,.067,.016),(.10,0,.12,.013),(.15,0,.183,.010),(.23,0,.228,.007),(.32,0,.265,.0045),(.41,0,.29,.002)],2)
        for i in range(4):
            u=.19-i*.025
            for s,label in [(-1,'left'),(1,'right')]:
                self.blade(f'{label}-gill-slit-{i}',[(u,s*.074,.031,.002),(u-.004,s*.079,.003,.002),(u+.001,s*.067,-.027,.0017)],2)

    def pteraspis(self):
        self.loft('posterior-trunk',[(-.40,.008,.014,0),(-.29,.023,.031,0),(-.17,.041,.046,0),(-.06,.060,.059,0),(.055,.072,.068,0)],16,3,False)
        self.loft('head-shield',[(-.06,.073,.072,0),(.02,.095,.084,0),(.14,.104,.082,-.004),(.25,.082,.059,-.008),(.32,.051,.037,-.01),(.34,.031,.025,-.01)],16)
        self.loft('pointed-rostral-shield',[(.28,.055,.040,-.005),(.36,.035,.025,-.005),(.44,.015,.012,-.006),(.50,.002,.003,-.006)],12,0,False)
        self.eye_pair(.245,.081,.018,.020)
        self.paired_fin('rigid-branchial-shield-flange',(.015,.078,-.003),(-.12,.17,-.012),(-.10,.071,-.01),0)
        self.fin('dorsal-shield-spine',[(.025,.073),(-.04,.225),(-.08,.238),(-.075,.059)],thick=.009,mat=2)
        self.fin('hypocercal-caudal',[(-.37,.009),(-.47,.090),(-.50,.095),(-.463,.018),(-.54,-.12),(-.46,-.074),(-.38,-.013)],thick=.007,mat=3)
        # Ordered seams on hard armor, not a borrowed fossil texture.
        for s,label in [(-1,'left'),(1,'right')]:
            self.blade(label+'-shield-division',[(.12,s*.072,.059,.0025),(.13,s*.101,.005,.0025),(.12,s*.079,-.055,.002)],2)

    def dorypterus(self):
        self.loft('deep-compressed-body',[(-.36,.009,.017,.0),(-.29,.027,.049,-.005),(-.19,.05,.115,-.002),(-.07,.068,.177,.008),(.07,.075,.194,.012),(.20,.065,.165,.001),(.29,.047,.113,-.018),(.34,.027,.060,-.03),(.357,.008,.022,-.037)],24)
        self.eye_pair(.265,.046,.035,.033)
        self.fin('high-pennant-dorsal',[(.23,.137),(.18,.265),(.10,.37),(-.015,.445),(-.09,.456),(-.04,.40),(-.085,.29),(-.17,.20),(-.265,.08),(-.18,.10),(-.05,.18)],thick=.008,mat=2)
        self.fin('small-caudal',[(-.33,.018),(-.47,.10),(-.452,.025),(-.47,-.073),(-.36,-.032)],thick=.006,mat=3)
        self.fin('anal-fin',[(-.06,-.161),(-.11,-.22),(-.25,-.16),(-.275,-.059),(-.19,-.11)],thick=.006,mat=2)
        self.paired_fin('pectoral',(.18,.058,-.035),(.015,.145,-.154),(.02,.056,-.10),3)
        self.paired_fin('jugular-pelvic',(.225,.023,-.08),(.155,.072,-.215),(.13,.021,-.13),2)
        # Sparse sail rays follow the large pennant rather than a uniform grid.
        for i,(a,b,c,d) in enumerate([(.15,.19,.06,.345),(.045,.195,-.02,.39),(-.065,.155,-.08,.275)]):
            for s in [-1,1]:self.blade(f'sail-ray-{i}-{s}',[(a,s*.008,b,.0025),(c,s*.008,d,.0018)],3)
        # Small closed lower-lip volume, no teeth or fake factual detail.
        self.ellipsoid('lower-lip',(.338,0,-.055),(.022,.025,.009),1,12,4)


def main():
    argv=sys.argv[sys.argv.index('--')+1:]
    parser=argparse.ArgumentParser()
    parser.add_argument('--config',required=True,type=Path)
    parser.add_argument('--output-dir',required=True,type=Path)
    a=parser.parse_args(argv);cfg=json.loads(a.config.read_text())
    start=datetime.now(timezone.utc).isoformat();t=time.monotonic()
    f=Fish(cfg);f.build()
    # Do not ground a swimming asset. This explicitly documented mount is midbody.
    record=export_asset(f.slug,{'en':f.slug.title()+'-inspired swimmer','zh':f.slug+' 风格化小鱼'},'animals',f.collection,
        metadata={'reconstruction_notes':'Original child-friendly inspired scene prop; not a scientific reconstruction. See frozen brief/reference limits.','mount_origin':cfg['mount_origin'],'generator':str(Path(__file__).relative_to(REPO)),'surface_profile':'palette-only'},
        output_root=a.output_dir.parent,render=False,max_triangles=cfg['max_triangles'],max_materials=cfg['max_materials'],max_primitives=cfg['max_primitives'])
    produced=a.output_dir.parent/f.slug
    if produced!=a.output_dir:
        a.output_dir.mkdir(parents=True,exist_ok=True)
        for p in produced.iterdir():p.rename(a.output_dir/p.name)
        produced.rmdir()
        # Paths in metadata must identify delivered outputs after relocation.
        for k in ['blend','glb','preview']:
            record[k]=str((a.output_dir/Path(record[k]).name).relative_to(REPO)) if a.output_dir.is_relative_to(REPO) else str(a.output_dir/Path(record[k]).name)
        (a.output_dir/'metadata.json').write_text(json.dumps(record,indent=2)+'\n')
    (a.output_dir/'build-timing.json').write_text(json.dumps({'started_at':start,'finished_at':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t,'blender':bpy.app.version_string,'threads':bpy.context.scene.render.threads,'render_included':False},indent=2)+'\n')


if __name__=='__main__':main()
