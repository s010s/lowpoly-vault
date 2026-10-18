# SPDX-License-Identifier: MIT
"""Original deterministic batch12 teaching geometry; Blender 4.3.2."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from mesh_utils import *

def generate(c,m):
 leaves=Part('small-stolon-linked-freshwater-leaf-rosettes',m);stolons=Part('persistent-branching-stolons-at-waterline',m);roots=Part('hanging-adventitious-and-simple-branched-root-bundles',m);veins=Part('restrained-original-leaf-midribs',m)
 nodes=[Vector((-.065,-.020,0)),Vector((-.005,.012,0)),Vector((.058,-.011,0)),Vector((.030,.065,0))]
 for a,bb in [(0,1),(1,2),(1,3)]:
  start,end=nodes[a],nodes[bb];mid=(start+end)*.5+Vector((0,.005,.001));curve_tube(stolons,[start,mid,end],.0013,.00105,1,9,5)
 for j,node in enumerate(nodes):
  for leafno in range(2):
   a=j*.83+(0 if leafno==0 else 2.4);u=Vector((math.cos(a),math.sin(a),0));w=Vector((-u.y,u.x,0));length=.030+.005*math.sin(j+leafno);width=.0145+.003*math.cos(j*.8+leafno);nr=14;n=16;v=[]
   for h in range(nr+1):
    t=h/nr;ww=.0008+width*math.sin(pi*t)**.72;center=node+u*(length*t)+Vector((0,0,.0018+.0040*math.sin(pi*t)+.003*t*t));thick=.00065+.0002*math.sin(pi*t)
    for k in range(n):
     q=k*2*pi/n;v.append(tuple(center+w*(ww*math.cos(q))+Vector((0,0,thick*math.sin(q)+.0012*math.cos(q)**2*math.sin(pi*t)))))
   f=[tuple(reversed(range(n)))]+[(h*n+k,h*n+(k+1)%n,(h+1)*n+(k+1)%n,(h+1)*n+k) for h in range(nr) for k in range(n)]+[tuple(nr*n+k for k in range(n))];leaves.add(v,f,0)
   pts=[node+u*(length*t)+Vector((0,0,.0026+.004*math.sin(pi*t)+.003*t*t)) for t in [.05,.25,.5,.75,.95]];curve_tube(veins,pts,.00018,.00007,2,5,2)
  for k in range(5):
   a=k*2*pi/5+j*.4;d=Vector((math.cos(a),math.sin(a),0));length=.028+.012*((j+k)%3)/2;pts=[node,node+d*.003+Vector((0,0,-.010)),node+d*.007+Vector((0,0,-length*.72)),node+d*.010+Vector((.002*math.sin(k),0,-length))];curve_tube(roots,pts,.00065,.00012,3,7,3)
   if k==1:
    p=pts[2]
    for sign in [-1,1]:curve_tube(roots,[p,p+Vector((sign*.006,0,-.006)),p+Vector((sign*.010,.001,-.010))],.00026,.00008,3,5,2)
 leaves.finish(c,True);stolons.finish(c,True);roots.finish(c,True);veins.finish(c,True)

def main():
 p=argparse.ArgumentParser();p.add_argument('--asset',default='limnobiophyllum');p.add_argument('--config',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--no-preview',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);cfg=json.loads(a.config.read_text());s='limnobiophyllum';assert a.asset==cfg['asset_id']==s
 c=setup_scene(s,cfg['seed']);m=[make_material(s+'-'+str(i),color,roughness=.80) for i,color in enumerate(['#9CAC79', '#809568', '#BAC59B', '#92816B'])];generate(c,m)
 if s!='limnobiophyllum':ground_asset(c,center_xy=False)
 brief=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'brief.json').read_text());refs=json.loads((ROOT/'production/continuous-small-life-round04-20261018/items'/s/'references.json').read_text())
 meta={'description':{'en':brief['modeling_brief']['en'],'zh':brief['modeling_brief']['zh']},'generator':str(Path(__file__).relative_to(ROOT)),'habitat':'freshwater floating wetland plant; never marine vegetation','claim_scope':brief['claim_scope'],'surface_profile':'original palette-only geometry; no textures','representation':cfg['representation'],'reconstruction_notes':{'en':'Nominal scale, palette, pose, leaf/root/frond counts and fine relief are artistic. Original geometry only; no exact species, microscopic, locality, salinity or coexistence restoration. Limnobiophyllum mounting origin is the freshwater waterline; its roots extend below it.','zh':'名义尺度、配色、姿态、叶/根/羽片数量及细小起伏为美术选择。仅含原创几何；不主张精确物种、显微结构、地点、耐盐性或同域共存复原。Limnobiophyllum 原点为淡水水面，根部下垂。'},'sources':refs['sources'],'maker_thread':'01a15056-509d-725f-bad0-871371cd7010'}
 export_asset(s,{'en':'Limnobiophyllum-inspired freshwater floating rosettes','zh':'受 Limnobiophyllum 启发的淡水浮生叶丛'},'plants',c,metadata=meta,output_root=a.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30)
 if not a.no_preview:render_previews(c,a.output/s,('hero','reversehero','front','side','rear','top','clay','silhouette'),512,16,transparent=True)
 print('BATCH12_COMPLETE',s)
if __name__=='__main__':main()
