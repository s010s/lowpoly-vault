import json,sys,hashlib,datetime
from pathlib import Path
O=Path(__file__).parent;R=Path('/workspace/shared/lowpoly-batch85-height-repair-20261020');OLD=Path('/workspace/shared/lowpoly-batch85-20261020');sys.dont_write_bytecode=True;sys.path.insert(0,str(R/'scripts'))
from qa_glb import read_glb,accessor_values,audit_glb
h=json.load(open(R/'production/small-life-batch85-height-repair/maker-handoff.json'));records=[]
for item in h['items']:
 aid=item['asset_id'];a,b,_=read_glb(OLD/'production/small-life-batch85'/aid/item['previous_revision']/'artifacts'/(aid+'.glb'));c,d,_=read_glb(R/item['artifacts']['glb']['path']);issues=[];parts=[]
 for key in ['nodes','scenes','scene','materials','textures','images','skins','animations','extensionsUsed','extensionsRequired']:
  if a.get(key)!=c.get(key):issues.append(key+' changed')
 for ma,mc in zip(a['meshes'],c['meshes']):
  changed=0;xy=True;inds=True;nonpos_attrs=True
  for pa,pc in zip(ma['primitives'],mc['primitives']):
   va=accessor_values(a,b,pa['attributes']['POSITION']);vc=accessor_values(c,d,pc['attributes']['POSITION']);assert len(va)==len(vc)
   xy=xy and all(x[0]==y[0] and x[2]==y[2] for x,y in zip(va,vc));changed+=sum(x!=y for x,y in zip(va,vc));inds=inds and accessor_values(a,b,pa['indices'])==accessor_values(c,d,pc['indices']);assert pa.get('material')==pc.get('material')
   for attr in pa['attributes']:
    if attr not in ['POSITION','NORMAL']:nonpos_attrs=nonpos_attrs and accessor_values(a,b,pa['attributes'][attr])==accessor_values(c,d,pc['attributes'][attr])
  parts.append({'mesh':ma['name'],'planar_xz_stream_identical':xy,'indices_identical':inds,'non_position_normal_attributes_identical':nonpos_attrs,'changed_position_stream_entries':changed})
  if not (xy and inds and nonpos_attrs):issues.append(ma['name']+' unexpected non-height change')
 report={'asset_id':aid,'glb_sha256':item['artifacts']['glb']['sha256'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_material_definitions_nodes_scenes_extensions_unchanged':not any(' changed' in i for i in issues),'parts':parts,'issues':issues,'status':'pass' if not issues else 'fail'};(O/aid/'glb-difference.json').write_text(json.dumps(report,indent=2)+'\n');records.append(report)
print(json.dumps(records,indent=2))
