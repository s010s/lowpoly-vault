# 只读复核方法

在仓库根目录、报告基准 commit 的 checkout 运行以下 Python；仅将结果写到 `/tmp/production-baseline-data.json`，不改资产或 QA。分位数使用 nearest rank。只支持本次实际全部为 TRIANGLES 的静态 GLB；不是完整 glTF 验证器。POSITION 数为每个 primitive 的 stream 合计；几何字节为去重 bufferView 长度合计，不是 GPU 分配。

```python
import json, struct, hashlib, math, subprocess
from pathlib import Path
from collections import Counter
root=Path.cwd()
manifest=root/'assets/manifest.json'; m=json.loads(manifest.read_text());rows=[]
for a in m['assets']:
 p=root/a['glb']; b=p.read_bytes(); length=struct.unpack_from('<I',b,12)[0];d=json.loads(b[20:20+length]);acc=d.get('accessors',[]); ps=[p for mesh in d.get('meshes',[]) for p in mesh['primitives']]
 tri=sum((acc[p['indices']]['count'] if 'indices'in p else acc[p['attributes']['POSITION']]['count'])//3 for p in ps if p.get('mode',4)==4)
 assert all(p.get('mode',4)==4 for p in ps)
 assert tri==a['triangles'],a['id']
 assert hashlib.sha256(b).hexdigest()==a['sha256']['glb'],a['id']
 image_views={im['bufferView'] for im in d.get('images',[]) if 'bufferView'in im}
 image_bytes=sum(d['bufferViews'][i]['byteLength'] for i in image_views)
 attribute_views={acc[i]['bufferView'] for p in ps for i in list(p['attributes'].values())+([p['indices']] if 'indices'in p else []) if 'bufferView'in acc[i]}
 geometry_bytes=sum(d['bufferViews'][i]['byteLength'] for i in attribute_views)
 rows.append(dict(id=a['id'],category=a['category'],glb=a['glb'],sha256=hashlib.sha256(b).hexdigest(),triangles=tri,glb_bytes=len(b),position_stream_vertices=sum(acc[p['attributes']['POSITION']]['count']for p in ps),primitives=len(ps),materials=len({p.get('material')for p in ps}),images=len(d.get('images',[])),embedded_image_bytes=image_bytes,geometry_buffer_view_bytes=geometry_bytes,other_file_bytes=len(b)-geometry_bytes-image_bytes,quality_status=a.get('quality_status'),packs=a.get('packs',[])))
def summary(rs):
 def dist(k):
  x=sorted(r[k]for r in rs)
  return dict(min=x[0],p50=x[math.ceil(len(x)*.5)-1],p90=x[math.ceil(len(x)*.9)-1],max=x[-1],sum=sum(x))
 return dict(n=len(rs),triangles=dist('triangles'),glb_bytes=dist('glb_bytes'),under_100kb=sum(r['glb_bytes']<100000 for r in rs),over_500kb=sum(r['glb_bytes']>500000 for r in rs),over_1mb=sum(r['glb_bytes']>1000000 for r in rs),over_14ktri=sum(r['triangles']>14000 for r in rs),textured=sum(r['images']>0 for r in rs),primitives=dist('primitives'))
recent=[r for r in rows if any('round11-'in s or 'round12-'in s for s in r['packs'])]
out=dict(base_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),scope='Published manifest entries only; unique mesh definitions; nearest-rank quantiles; bytes decimal. Not candidate attempts, scientific certification or hardware performance.',all=summary(rows),recent_round11_12=summary(recent),by_category={k:summary([r for r in rows if r['category']==k])for k in sorted({r['category']for r in rows})},assets=rows)
print(json.dumps({k:v for k,v in out.items()if k!='assets'},indent=2))
Path('/tmp/production-baseline-data.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
```

最近24份 brief 的路径及逐项政策已保存在 measurements.json 的 recent_brief_policies。存在候选 brief 时读取 source_url 指向目录内 brief.json；未打包候选 brief 的项目读取同轮 production/items/<id>/brief.json。它们均为14,000tri、1,000,000B、6 materials、30 primitives、软500,000B；纹理均为1张、256px、编码65,536B、解码估计524,288B。未据这些数字改写批准。

## 远端增量复核

175件快照固定commit `de413ef720463a2999516faf92c606bcdf9ab1b7`。对上面程序，将manifest读取替换为 `manifest_bytes=subprocess.check_output(['git','show',COMMIT+':assets/manifest.json'])` 再 `json.loads`；每个GLB改为 `subprocess.check_output(['git','show',COMMIT+':'+a['glb']])`，manifest hash也以manifest_bytes计算。recent筛选补入`round13-`。实际报告执行了这些读取和原有逐件hash/tri断言。remote-main-175.json包含175件明细与新增12份brief的路径、hash和政策，前24份见measurements.json。两份都是历史快照，不应随之后main移动覆盖。
