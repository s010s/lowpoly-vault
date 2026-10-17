# SPDX-License-Identifier: MIT
import bpy,json,hashlib,sys
from pathlib import Path
p=Path(__file__).resolve().parent
values=[]
for folder in [p.parent/'candidate-r12',p]:
 bpy.ops.wm.open_mainfile(filepath=str(folder/'conifer-tree.blend'),load_ui=False,use_scripts=False)
 obj=next(o for o in bpy.data.objects if o.type=='MESH' and 'woody' in o.name)
 data={'vertices':[list(v.co) for v in obj.data.vertices],'faces':[list(f.vertices) for f in obj.data.polygons],'world_matrix':[list(r) for r in obj.matrix_world]}
 values.append(data)
report={'check':'r12-wood-preservation','status':'pass' if values[0]==values[1] else 'fail','exact_local_vertices_faces_world_matrix_equal':values[0]==values[1],'vertices':len(values[1]['vertices']),'sha256':[hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest() for x in values]}
(p/'wood-preservation.report.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
if report['status']!='pass':raise RuntimeError('Wood differs')
