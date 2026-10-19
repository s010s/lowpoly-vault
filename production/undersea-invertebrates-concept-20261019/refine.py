from pathlib import Path
import shutil,json
B=Path('production/undersea-invertebrates-concept-20261019');A=Path('assets/candidates/undersea-invertebrates-concept-20261019')
s=(B/'generator.py').read_text()
s=s.replace('n=40;L=10;v=[];f=[];mi=[]','n=36;L=9;v=[];f=[];mi=[]').replace('a=2*pi*i/n;v.append((.030*cos(t)*cos(a)', 'a=2*pi*(i+.30*sin(j*1.71))/n;v.append((.030*cos(t)*cos(a)')
s=s.replace("pore=j>0 and j<9 and ((i//5+j//3)%3!=0)","pore=j>0 and j<8 and ((i//4+j//2)%3!=0)")
a=s.index('   start=len(v)\n   for q in corners:');z=s.index('\n f.append(tuple(L*n+i',a)
s=s[:a]+'''   start=len(v)
   # Octagonal mouths with tapered cavity walls, clustered across curved regions.
   inner=[]
   for k,q in enumerate(corners):
    for near in [corners[(k-1)%4],corners[(k+1)%4]]:
     inner.append(ctr+(q-ctr)*.40+(near-ctr)*.13)
   for q in inner:v.append(tuple(q))
   for q in inner:v.append(tuple(ctr+(q-ctr)*.70-normal*.00070))
   for k in range(4):
    q=(k+1)%4
    f.append((ids[k],start+2*k,start+2*k+1));mi.append(0)
    f.append((ids[k],ids[q],start+2*q,start+2*k+1));mi.append(0)
   for k in range(8):
    q=(k+1)%8;f.append((start+k,start+q,start+8+q,start+8+k));mi.append(1)
   f.append(tuple(start+8+k for k in range(8)));mi.append(1)'''+s[z:]
# More readable radial ridges; a genuinely shallow concavo-convex profile, not a flat slab.
s=s.replace('rib=.5+.5*cos(32*(a+pi/2))','rib=.5+.5*cos(32*(a+pi/2))')
s=s.replace('base=.004+.0008*r-.0022*sin(pi*r)*cos(a)**2','base=.0045-.0025*sin(pi*r)*cos(a)**2')
s=s.replace('z=base+(.0015+.0005*r*rib if side==0 else -.0025*sin(pi*r*.75)-.0008)','z=base+(.0007+.00115*sqrt(r)*rib if side==0 else -.00075+.0008*sqrt(r)*rib)')
s=s.replace("mi.append(1 if .53<((j+1)/J)<.79 else 0)","mi.append(1 if j in [7,8] and i%6 in [1,2,3,4] else 0)")
(B/'generator-r002.py').write_text(s)
for slug in ['prasopora','strophomena']:
 old=A/slug/'r001';new=A/slug/'r002';new.mkdir(exist_ok=True)
 for n in ['references.json','brief.md']:shutil.copy2(old/n,new/n)
 (new/'brief.md').write_text((new/'brief.md').read_text()+'\nRevision r002 follows actual quick-GLB pixel inspection. Named change: '+('replace machine-like square pores with octagonal recessed pores and phase-shifted regional rows.' if slug=='prasopora' else 'make radial ribs legible in neutral clay and reduce thick slab rim; preserve straight hinge and shallow concavo-convex profile.')+' Prior r001 remains preserved.\n')
 cfg=json.loads((old/'build-config.json').read_text());cfg['revision']='r002';(new/'build-config.json').write_text(json.dumps(cfg,indent=2)+'\n');(new/'generator.py').write_text(s)
# Scoped renderer changes only framing clamp; no geometry normalization.
r=Path('scripts/render_candidate_views.py').read_text().replace("sys.path.insert(0, str(Path(__file__).resolve().parent))","sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p/'scripts/asset_common.py').exists())/'scripts'))").replace('radius = max(radius,0.025)','radius = max(radius,0.00001)')
(B/'render_exact_glb.py').write_text(r)
notes={'inspected':'quick-contact.png, 20 exact exported-GLB views','observations':{'mackenzia':'Eight continuous folded sac and stalk readable in all five views; no tentacles.','prasopora':'Dome and basal rim read well but square grid pores look manufactured; revise pore mouth corners and regional phases.','strophomena':'Flat thick slab with weak radial ribs. Revise actual rib relief, thin perimeter and shallow opposing curvatures.','ctenoimbricata':'Bilateral spine ring and anterior comb present but 0.025m renderer radius clamp makes 20mm specimen too small. Remove clamp in scoped renderer; keep meters and geometry unchanged.'},'status':'maker-self-inspection-only; independent QA pending'}
(B/'quick-inspection.json').write_text(json.dumps(notes,indent=2)+'\n')
j=json.loads((B/'build-jobs.json').read_text());j['jobs']=[q for q in j['jobs'] if q['asset_id'] in ['prasopora','strophomena']]
for q in j['jobs']:
 q['revision']='r002';q['job_id']='refined-build'
 q['inputs']={k:v.replace('/r001/','/r002/') for k,v in q['inputs'].items()}
(B/'refined-build-jobs.json').write_text(json.dumps(j,indent=2)+'\n')
