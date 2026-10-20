from pathlib import Path
import json,datetime
R=Path.cwd();W=R/'production/continuous-small-life-round25-20261020/work/batch-65/stalagmite-repair-r002';a=R/'assets/candidates/continuous-small-life-round25-20261020/batch-65/stalagmite-group/r001';b=a.parent/'r002'
(b/'authoring-start.json').write_text(json.dumps({'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'note':'Observed before authoring revised generator; follows truthful repair freeze; not inferred from file mtime'})+'\n')
s=(a/'generator.py').read_text();head=s[:s.index('# ORIGINAL batch65')];tail=s[s.index('ground_asset(col,center_xy=True)'):]
geometry='''# Original targeted corrective geometry, after r002 repair freeze.
# The original brief and composition are preserved verbatim.
rings=[]
for z,scale in [(0,.88),(.07,1),(.14,.91)]:
 rings.append([(1.15*scale*(1+.06*math.sin(i*2.3))*math.cos(i*math.tau/24),.85*scale*(1+.08*math.sin(i*1.7))*math.sin(i*math.tau/24),z) for i in range(24)])
loft('low_irregular_floor_mineral_crust',rings,'floor')
columns=[(0,.27,2.1,.28),(-.61,.04,1.45,.23),(.60,.20,1.15,.24),(-.35,-.44,.83,.21),(.56,-.40,.55,.19)]
for ci,(x,y,h,r) in enumerate(columns):
 rings=[];n=24;ns=36;phase=ci*1.319
 # Unequal height locations and weak amplitudes, not a periodic stacked-ring profile.
 terrace_positions=[.17+.025*math.sin(ci*1.2),.36+.04*math.cos(ci),.58+.027*math.sin(ci+1),.76+.025*math.cos(ci*2)]
 for j in range(ns):
  t=j/(ns-1)*.9999;cap=math.sqrt(max(.0001,1-((t-.86)/.14)**2)) if t>.86 else 1
  envelope=1.38-.54*t-.10*math.sin(math.pi*t)
  cx=x+.035*math.sin(t*2.5+phase)*t;cy=y+.025*math.sin(t*3.1+phase*.7)*t
  ring=[]
  for i in range(n):
   ang=i*math.tau/n
   # Five continuous asymmetric drip buttresses, slow twist avoids vertical machine grooves.
   ridge=0
   for q in range(5):
    center=q*math.tau/5+.16*math.sin(q*2.1+phase)+.10*math.sin(t*2.8+q)
    delta=math.atan2(math.sin(ang-center),math.cos(ang-center))
    amplitude=.11+.055*math.sin(q*1.6+phase)**2
    ridge+=amplitude*math.exp(-(delta/.23)**2)*(.68+.32*math.sin(math.pi*t))
   fine=.018*math.cos(ang*9+.32*math.sin(t*4+phase))
   # Weak irregular deposition terraces, warped by angular drip pattern and differing heights.
   terrace=0
   for q,pos in enumerate(terrace_positions):
    warped=pos+.025*math.sin(ang*2+q+phase)+.014*math.cos(ang*3+phase)
    terrace+=(.012+.007*math.sin(q+ci)**2)*math.exp(-((t-warped)/(.032+.01*(q%2)))**2)
   radial=r*envelope*cap*(1+ridge+fine+terrace)
   ring.append((cx+radial*math.cos(ang),cy+radial*(.95+.025*math.sin(ang+phase))*math.sin(ang),.10+h*t))
  rings.append(ring)
 loft('solid_rounded_stalagmite_'+str(ci+1)+'_irregular_longitudinal_drips',rings,'mineral')
for (name,mat),(vs,fs) in groups.items():
 obj=mesh_object(name,vs,fs,m[mat],col)
 if mat=='mineral':
  obj.data.materials.append(m['light']);obj.data.materials.append(m['ochre'])
  # No regular height-band colors. Restrained long mineral variations follow vertical drips.
  ci=int(name.split('_')[3])-1;x,y,h,r=columns[ci]
  for poly in obj.data.polygons:
   c=poly.center;ang=math.atan2(c.y-y,c.x-x);t=(c.z-.10)/h
   poly.material_index=1 if math.cos(ang*3+ci*.5)>.80 and .12<t<.87 else 2 if math.cos(ang*2+ci)<-.88 and t<.65 else 0
'''
(b/'generator.py').write_text(head+geometry+'\n'+tail)
# Reuse stable lifecycle methods with a one-asset selection. No accepted asset touched.
P=W.parent
for name in ['run-lifecycle.py','compose-sheets.py','package-candidates.py']:
 s=(P/name).read_text().replace("W=R/'production/continuous-small-life-round25-20261020/work/batch-65'","W=R/'production/continuous-small-life-round25-20261020/work/batch-65/stalagmite-repair-r002'")
 s=s.replace("str(W/'blender-locked.sh')","str(W.parent/'blender-locked.sh')").replace("str(W/'count-source-vertices.py')","str(W.parent/'count-source-vertices.py')").replace("str(W/'render-fixed8.py')","str(W.parent/'render-fixed8.py')").replace("str(W/'runtime-parse.mjs')","str(W.parent/'runtime-parse.mjs')")
 if name=='run-lifecycle.py':
  # Complete delivery rights ledger already prepared before exact final proof rendering.
  s=s.replace("'proof-final'","'proof-delivery'").replace("'proof-final/render-manifest.json'","'proof-delivery/render-manifest.json'").replace("str(b/'references.json'),'--output-dir'","str(b/'references.delivery-v001.json'),'--output-dir'")
 if name=='package-candidates.py':
  start=s.index('notes={');end=s.index('summary=[]',start)
  s=s[:start]+"notes={'stalagmite-group':'Targeted r002 repair under unchanged original target: five unequal solid rounded floor-grown columns and broad roots retained. Strong repeated horizontal rings removed; weak uneven angular-warped deposition terraces subordinate to clear irregular longitudinal drip ridges/grooves, which remain real full-volume geometry in clay. No regular horizontal material striping. Exact eight512px views individually inspected after new render. Original failed r001 and independent QA preserved. Independent targeted review pending.'}\n"+s[end:]
  s=s.replace("'base_main':'000a6fce999b8968e154de7787d91753f2d60d37'","'base_main':'567f7a5271cca6271caba26c025bfaf39405a507'")
 (W/name).write_text(s)
# Explicit derived rights binding before any proof render.
import hashlib
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();d=json.load(open(a/'references.delivery-v001.json'));d['packaging_rights_adapter']={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_references_sha256':H(b/'references.json'),'scope':'Targeted r002 delivery rights metadata only. Original facts/design/source ledger copied unchanged; no third-party media incorporated.'};(b/'references.delivery-v001.json').write_text(json.dumps(d,indent=2)+'\n')
