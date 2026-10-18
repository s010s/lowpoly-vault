# SPDX-License-Identifier: MIT
"""Original batch-01 models. Blender 4.3.2. No third-party geometry or maps.
blender -b -t 2 --python-exit-code 1 --python <this> -- --asset archaeopteryx --output /tmp/build
Output is an isolated parent containing <asset>/, suitable for deterministic rebuild.
"""
import bpy, sys, math, json, argparse, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset,render_previews
from math import sin,cos,pi
P=ROOT/'production/continuous-small-life-20261018'
class Shape:
 def __init__(self):self.v=[];self.f=[]
 def add(self,v,f):
  n=len(self.v);self.v.extend(v);self.f.extend(tuple(n+i for i in face) for face in f)
 def tube(self,points,radii,sides=10,aspect=1):
  ps=[Vector(p) for p in points];vs=[];fs=[]
  for j,p in enumerate(ps):
   t=(ps[min(j+1,len(ps)-1)]-ps[max(0,j-1)]).normalized();ref=Vector((0,0,1)) if abs(t.z)<.95 else Vector((1,0,0));a=t.cross(ref).normalized();b=t.cross(a).normalized()
   for k in range(sides):vs.append(tuple(p+radii[j]*(a*cos(2*pi*k/sides)+b*sin(2*pi*k/sides)*aspect)))
  for j in range(len(ps)-1):
   for k in range(sides):a=j*sides+k;b=j*sides+(k+1)%sides;fs.append((a,b,b+sides,a+sides))
  fs+=[tuple(reversed(range(sides))),tuple((len(ps)-1)*sides+k for k in range(sides))];self.add(vs,fs)
 def ellipsoid(self,c,r,segments=16,rings=10):
  # Single vertices at poles, no zero-area collapsed latitude rings.
  c=Vector(c);v=[tuple(c+Vector((0,0,r[2])))];f=[]
  for j in range(1,rings):
   t=pi*j/rings
   for k in range(segments):a=2*pi*k/segments;v.append(tuple(c+Vector((r[0]*sin(t)*cos(a),r[1]*sin(t)*sin(a),r[2]*cos(t)))))
  bot=len(v);v.append(tuple(c-Vector((0,0,r[2]))))
  for k in range(segments):f.append((0,1+k,1+(k+1)%segments))
  for j in range(rings-2):
   for k in range(segments):a=1+j*segments+k;b=1+j*segments+(k+1)%segments;f.append((a,a+segments,b+segments,b))
  for k in range(segments):f.append((bot,1+(rings-2)*segments+(k+1)%segments,1+(rings-2)*segments+k))
  self.add(v,f)
 def loft_y(self,sections,sides=16):
  # y,cx,cz, width radius,height radius; tailored cross sections, closed caps.
  v=[];f=[]
  for y,x,z,w,h in sections:
   for k in range(sides):a=2*pi*k/sides;v.append((x+w*cos(a),y,z+h*sin(a)))
  for j in range(len(sections)-1):
   for k in range(sides):a=j*sides+k;b=j*sides+(k+1)%sides;f.append((a,a+sides,b+sides,b))
  f.extend([tuple(range(sides)),tuple(reversed([(len(sections)-1)*sides+k for k in range(sides)]))]);self.add(v,f)
 def blade(self,base,tip,width,thick=.006,bend=.02):
  # Biconvex closed leaf/feather with ridge and a curved tapered planform.
  base=Vector(base);tip=Vector(tip);d=tip-base;a=Vector((-d.y,d.x,0)).normalized();v=[];f=[]
  for j,t in enumerate([0,.2,.48,.75,.94]):
   c=base+d*t+Vector((0,0,bend*sin(pi*t)));w=width*[.08,.75,1,.68,.22][j]
   v.extend([tuple(c-a*w),tuple(c+Vector((0,0,thick))),tuple(c+a*w),tuple(c-Vector((0,0,thick*.5)))])
  n=len(v);v.append(tuple(tip))
  f.append((3,2,1,0))
  for j in range(4):
   for k in range(4):a0=j*4+k;b0=j*4+(k+1)%4;f.append((a0,b0,b0+4,a0+4))
  for k in range(4):f.append((16+k,16+(k+1)%4,n))
  self.add(v,f)

def build_archaeopteryx():
 parts={};add=lambda n:parts.setdefault(n,Shape())
 # One flowing torso/neck/head profile replaces a chain of spheres.
 add('body').loft_y([(.13,0,.30,.012,.015),(.07,0,.33,.09,.09),(-.04,0,.36,.13,.14),(-.18,0,.39,.115,.15),(-.28,0,.45,.075,.11),(-.32,0,.56,.055,.085),(-.39,0,.65,.07,.075),(-.49,0,.66,.065,.06),(-.55,0,.65,.035,.033)],20)
 add('jaw').loft_y([(-.48,0,.62,.055,.022),(-.55,0,.628,.04,.018),(-.64,0,.634,.012,.012)],12)
 add('upper-jaw').loft_y([(-.49,0,.658,.058,.027),(-.57,0,.655,.035,.018),(-.65,0,.647,.009,.009)],12)
 for s in [-1,1]:
  add('eyes').ellipsoid((s*.063,-.46,.683),(.014,.017,.017),12,8)
  add('eye-glint').ellipsoid((s*.074,-.466,.69),(.004,.005,.005),8,6)
  # restrained visible tooth hints in the small jaw opening
  for j in range(3):add('teeth').tube([(s*(.033-j*.006),-.55-j*.024,.645),(s*(.033-j*.006),-.55-j*.024,.636)],[.004,.0025],5)
  # shoulder -> elbow -> wrist; feathers are part of the same wing, no extra arms
  opened=s==1
  pts=[(s*.025,-.19,.43),(s*.13,-.15,.43),(s*(.24 if opened else .16),-.07,.40),(s*(.31 if opened else .19),.06,.34)]
  add('wing-coverts').tube(pts,[.035,.065,.055,.018],12,.65)
  for j in range(9):
   t=j/8;base=(s*(.17+.14*t if opened else .125+.06*t),-.09+.16*t,.41-.07*t);tip=(s*(.30+.15*t if opened else .20+.07*t),.16+.15*t,.31-.07*t)
   add('flight-feathers').blade(base,tip,.035-.01*t,.006,.015)
  for j in range(3):
   x=s*(.30 if opened else .19);y=.035+j*.018;z=.375-j*.014
   add('wing-claws').tube([(x,y,z),(x+s*.025,y-.02,z+.025),(x+s*.035,y-.035,z+.018)],[.007,.005,.003],7)
  add('thighs').tube([(s*.065,-.03,.33),(s*.085,-.07,.22),(s*.078,-.015,.15)],[.055,.045,.026],12)
  add('legs').tube([(s*.078,-.015,.16),(s*.082,-.08,.055),(s*.082,-.08,.025)],[.018,.012,.012],10)
  for j in range(3):
   x=s*.082+(j-1)*.022;add('feet').tube([(s*.082,-.08,.026),(x,-.135,.017),(x+(j-1)*.008,-.19+.012*abs(j-1),.012)],[.011,.008,.005],8)
  add('feet').tube([(s*.082,-.08,.026),(s*.10,-.025,.015)],[.009,.005],8)
 # Long underlying axis with feather vanes all along its length, not a modern fan.
 tail=[(0,.09,.34),(0,.29,.32),(.012,.49,.33),(.025,.72,.37),(.03,.92,.41)]
 add('tail-axis').tube(tail,[.045,.033,.021,.012,.005],12)
 for j in range(12):
  t=j/11;y=.16+t*.69;x=.03*t;z=.328+.075*t*t
  for s in [-1,1]:add('tail-feathers').blade((x,y,z),(x+s*(.085-.045*t),y+.15-.045*t,z-.008),.045-.022*t,.005,.009)
 return parts,{'body':'#62767A','jaw':'#A08A67','upper-jaw':'#A08A67','eyes':'#272D2D','eye-glint':'#D9DED5','teeth':'#D9DED5','wing-coverts':'#62767A','flight-feathers':'#40575D','wing-claws':'#A08A67','thighs':'#62767A','legs':'#A08A67','feet':'#A08A67','tail-axis':'#62767A','tail-feathers':'#40575D'},.4,'length'

def build_canadaspis():
 parts={};add=lambda n:parts.setdefault(n,Shape())
 # Two deep suboval valves with dorsal hinge and a narrow anterior end.
 for s in [-1,1]:
  sec=[(-.43,s*.04,.31,.02,.045),(-.35,s*.12,.31,.085,.16),(-.18,s*.16,.31,.13,.23),(.04,s*.17,.31,.14,.25),(.24,s*.14,.31,.115,.205),(.38,s*.075,.33,.05,.12),(.40,s*.05,.34,.01,.05)]
  add('valve-'+str(s)).loft_y(sec,20)
  # lower rim follows the shell contour instead of a contrasting stripe grid
  add('rims').tube([(s*.06,-.40,.25),(s*.16,-.25,.105),(s*.21,0,.065),(s*.17,.23,.12),(s*.08,.38,.23)],[.012]*5,8)
 add('head').ellipsoid((0,-.40,.25),(.11,.095,.11))
 for s in [-1,1]:
  add('eye-stalks').tube([(s*.055,-.43,.30),(s*.11,-.52,.34)],[.018,.014],8)
  add('eyes').ellipsoid((s*.11,-.53,.34),(.023,.03,.025),12,8)
  add('sensory').tube([(s*.04,-.45,.24),(s*.075,-.61,.245),(s*.13,-.76,.27)],[.016,.011,.006],8)
  add('antennulae').tube([(s*.08,-.44,.22),(s*.18,-.54,.20),(s*.22,-.61,.23)],[.02,.016,.009],8)
  for j in range(8):
   y=-.28+j*.078;z=.22
   add('walking-legs').tube([(s*.08,y,z),(s*.20,y-.012,.12),(s*.29,y-.04,.035),(s*.32,y-.065,.012)],[.024,.023,.016,.009],8)
   add('outer-branches').blade((s*.16,y,.16),(s*.30,y+.04,.14),.038,.006,.015)
 # exposed tapering abdomen, no walking legs posterior to valve
 for j in range(7):
  y=.30+j*.095;w=.102-j*.009
  add('abdomen').loft_y([(y,0,.27,w*.91,w*.83),(y+.025,0,.27,w,w*.88),(y+.087,0,.27,w*.85,w*.76)],14)
  for s in [-1,1]:add('abdominal-spines').tube([(s*w*.7,y+.065,.22),(s*w*1.1,y+.105,.205)],[.012,.005],6)
 for s in [-1,1]:add('terminal-processes').tube([(s*.028,.93,.27),(s*.07,1.09,.285),(s*.08,1.17,.29)],[.021,.012,.004],8)
 return parts,{'valve--1':'#AF8060','valve-1':'#AF8060','rims':'#C79F78','head':'#82604A','eye-stalks':'#82604A','eyes':'#26363A','sensory':'#C79F78','antennulae':'#C79F78','walking-legs':'#A78B67','outer-branches':'#A78B67','abdomen':'#82604A','abdominal-spines':'#C79F78','terminal-processes':'#A78B67'},.08,'body'

def build_ceratomyrmex():
 parts={};add=lambda n:parts.setdefault(n,Shape())
 # Ant anatomy uses designed mesosoma/waist/gaster profiles rather than sphere stacks.
 add('mesosoma').loft_y([(-.17,0,.29,.055,.065),(-.09,0,.31,.09,.09),(.06,0,.29,.075,.075),(.18,0,.25,.052,.055)],16)
 add('neck').tube([(0,-.13,.30),(0,-.23,.34)],[.045,.055],12)
 add('head').loft_y([(-.19,0,.37,.06,.07),(-.28,0,.40,.105,.12),(-.40,0,.40,.105,.115),(-.46,0,.37,.075,.065)],18)
 add('petiole').tube([(0,.15,.25),(0,.24,.255),(0,.29,.29),(0,.34,.26)],[.035,.027,.042,.029],12)
 add('gaster').loft_y([(.31,0,.26,.028,.032),(.40,0,.27,.105,.095),(.55,0,.27,.14,.125),(.69,0,.27,.12,.11),(.78,0,.27,.065,.065),(.82,0,.27,.018,.02)],18)
 # Forehead horn rising between antennae, forward-curved padded spatulate apex.
 add('horn').tube([(0,-.385,.47),(0,-.42,.60),(0,-.48,.74),(0,-.57,.80)],[.045,.033,.035,.055],12,.65)
 # Upward jaws stop below the horn with visible negative space; calm open static pose.
 for s in [-1,1]:
  add('mandibles').tube([(s*.055,-.43,.34),(s*.07,-.56,.32),(s*.065,-.67,.40),(s*.045,-.68,.53),(s*.023,-.63,.63)],[.025,.024,.022,.016,.008],10,.7)
  add('eyes').ellipsoid((s*.099,-.34,.43),(.021,.033,.03),12,8)
  add('antennae').tube([(s*.06,-.38,.47),(s*.17,-.47,.53),(s*.22,-.63,.54),(s*.25,-.72,.49)],[.015,.013,.010,.006],8)
  for j in range(3):
   y=-.09+j*.105
   add('legs').tube([(s*.06,y,.29),(s*.15,y+(.03 if j else -.03),.27),(s*.30,y+(.16 if j==2 else -.10 if j==0 else .015),.18),(s*.36,y+(.23 if j==2 else -.17 if j==0 else .04),.015)],[.025,.022,.016,.009],8)
   add('tarsi').tube([(s*.36,y+(.23 if j==2 else -.17 if j==0 else .04),.015),(s*.40,y+(.26 if j==2 else -.20 if j==0 else .07),.009)],[.010,.006],7)
 return parts,{'mesosoma':'#7D4E35','neck':'#7D4E35','head':'#A46C42','petiole':'#7D4E35','gaster':'#6C4738','horn':'#B78C59','mandibles':'#B78C59','eyes':'#242E2B','antennae':'#A46C42','legs':'#A46C42','tarsi':'#A46C42'},.01,'body'

def build_hydropteris():
 parts={};add=lambda n:parts.setdefault(n,Shape())
 rh=[(-.48,-.08,.13),(-.25,-.03,.15),(0,0,.16),(.25,.06,.17),(.45,.12,.15)]
 add('rhizome').tube(rh,[.025,.028,.029,.025,.018],10)
 add('rhizome').tube([(-.16,-.02,.15),(-.10,-.20,.15),(.10,-.35,.14),(.25,-.40,.13)],[.024,.022,.02,.012],10)
 for j,(x,y,z) in enumerate(rh[:-1]+[(-.10,-.20,.15),(.10,-.35,.14)]):
  for k in range(3):
   a=k*2.1+j*.65
   add('roots').tube([(x,y,z),(x+.06*cos(a),y+.06*sin(a),.07),(x+.11*cos(a+.3),y+.11*sin(a+.3),.008)],[.009,.006,.0035],7)
 # Six fronds on separate rhizome nodes, varied growth directions and open spaces.
 specs=[(-.38,-.06,-2.4,.70),(-.19,-.015,2.35,.90),(.02,0,.7,1.0),(.30,.08,.15,.82),(-.07,-.22,-1.7,.88),(.16,-.37,-.3,.63)]
 for j,(x,y,a,L) in enumerate(specs):
  dx,dy=cos(a),sin(a)
  def center(t):return Vector((x+dx*L*.48*t*t,y+dy*L*.48*t*t,.15+L*(.85*t-.18*t*t)))
  add('rachides').tube([center(t) for t in [0,.2,.4,.6,.8,1]],[.012,.011,.009,.007,.005,.0025],8)
  for k in range(7):
   for s in [-1,1]:
    t=.20+k*.105+(0.025 if s==1 else 0);b=center(t);length=L*.20*(sin(pi*(t+.07))**.8);side=Vector((-dy*s,dx*s,0));tip=b+side*length+Vector((dx*.055,dy*.055,.016-.055*t))
    add('pinnae-light' if (k+j)%3==0 else 'pinnae').blade(b,tip,length*.29,.0045*L,.012)
  add('pinnae').blade(center(.87),center(1.05),.025*L,.003,.004)
  if j in [0,2,4]:add('sporocarps').ellipsoid((x+.035,y+.018,.18),(.045,.034,.037),12,8)
 return parts,{'rhizome':'#79654A','roots':'#79654A','rachides':'#66917B','pinnae':'#467664','pinnae-light':'#66917B','sporocarps':'#AE8054'},.08,'height'

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--asset',required=True,choices=['archaeopteryx','canadaspis','ceratomyrmex','hydropteris']);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--render',action='store_true');parser.add_argument('--config',type=Path)
 args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);a=args.asset;cfg=args.config or P/'items'/a/'build-config.json';config=json.loads(cfg.read_text());brief=json.loads((P/'items'/a/'brief.json').read_text());c=setup_scene(a,config['seed']);parts,palette,target,axis=globals()['build_'+a]()
 points=[v for sh in parts.values() for v in sh.v];lo=[min(v[i] for v in points) for i in range(3)];hi=[max(v[i] for v in points) for i in range(3)]
 # body excludes antennae/jaws as stipulated; Canadaspis excludes sensory reach.
 if a=='ceratomyrmex': span=.82-(-.46)
 elif a=='canadaspis':span=1.17-(-.43)
 else:span=hi[2]-lo[2] if axis=='height' else hi[1]-lo[1]
 scale=target/span
 colors={hex:make_material('palette-'+hex[1:],hex,.83) for hex in set(palette.values())}
 for name,sh in parts.items():
  vs=[(v[0]*scale,v[1]*scale,(v[2]-lo[2])*scale) for v in sh.v]
  o=mesh_object(name,vs,sh.f,colors[palette[name]],c)
  # Mixed smooth shading on organic profile meshes; distinct ridged blades retain facets.
  smooth=not any(s in name for s in ['feather','pinnae','branches'])
  for f in o.data.polygons:f.use_smooth=smooth
 desc={'en':'Original evidence-informed stylized-inspired static teaching art; artistic colors, pose and nominal dimensions. Not a strict scientific reconstruction.','zh':'原创、依据基础形态的儿童友好风格化静态教学美术；色彩、姿态与标称尺寸属艺术选择，不是严格科学复原。'}
 meta={'description':desc,'generator':str(Path(__file__).relative_to(ROOT)),'sources':json.loads((P/'items'/a/'references.json').read_text())['sources'],'claim_scope':brief['claim_scope'],'nominal_scale':brief['scale'],'texture_profile':'palette-only; no textures or external media','originality':'Original profile, tube and biconvex blade topology authored for this batch. No reference image, scan, mesh or texture incorporated.','reconstruction_notes':{'en':'Fine feather/digit/segment counts, soft tissue, colors and pose are simplified artistic choices; static only.','zh':'羽序、趾节、节数、软组织、颜色和姿态均作合理艺术简化；仅静态。'},'mounting':'lowest intended root/foot contact at Z=0; identity root at contact centerline','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),cfg,P/'items'/a/'brief.json',P/'items'/a/'references.json',ROOT/'scripts/asset_common.py']}}
 export_asset(a,brief['subject']['inventory_name'],brief['subject']['category'],c,metadata=meta,output_root=args.output,render=False,max_triangles=14000,max_materials=6,max_primitives=30,collection_id='continuous-small-life')
 if args.render:
  # View helper's historical minimum span is 10cm; scale only the temporary presentation
  # for tiny specimens and normalize lighting to that scale. Saved source/GLB stay meters.
  presentation=max(1,.35/(max(hi[i]-lo[i] for i in range(3))*scale));root=bpy.data.objects[c['asset_root']];root.scale=(presentation,)*3;bpy.context.view_layer.update()
  render_previews(c,args.output/a,views=tuple(config['required_views']),resolution=512,samples=16,transparent=True)
 print('BATCH01_BUILT',a)
if __name__=='__main__':main()
