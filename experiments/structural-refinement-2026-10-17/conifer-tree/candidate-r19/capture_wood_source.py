#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Capture immutable original woody geometry, groups and world transform only.
Reads the historical r12 source, never saves it or reads old foliage into r19.
"""
import bpy,json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
source=P.parent/'candidate-r12/conifer-tree.blend';target=P/'woody-source.json'
if target.exists():raise RuntimeError('Source snapshot already frozen')
bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False)
obj=next(o for o in bpy.data.objects if o.type=='MESH' and 'woody' in o.name)
vertices=[list(obj.matrix_world@v.co) for v in obj.data.vertices];faces=[list(p.vertices) for p in obj.data.polygons]
groups={g.name:[v.index for v in obj.data.vertices if any(x.group==g.index for x in v.groups)] for g in obj.vertex_groups}
data={'source':'candidate-r12/conifer-tree.blend','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'vertices':vertices,'faces':faces,'vertex_groups':groups,'original_world_matrix':[list(row) for row in obj.matrix_world],'counting':'Exact original wood mesh vertices and polygon indices; world transform baked into copied coordinates, source remains untouched.'}
assert len(vertices)==1525 and sum(len(f)-2 for f in faces)==2914
target.write_text(json.dumps(data,indent=2)+'\n');print('Frozen wood snapshot:',len(vertices),'vertices,2914 triangles.')
