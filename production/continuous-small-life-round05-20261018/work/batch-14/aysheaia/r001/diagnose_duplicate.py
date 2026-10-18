import bpy,sys
bpy.ops.wm.open_mainfile(filepath=sys.argv[-1],load_ui=False)
for o in bpy.data.objects:
 if o.type!='MESH':continue
 m=o.data;m.calc_loop_triangles();areas=[(t.index,t.area,t.vertices[:]) for t in m.loop_triangles];print(o.name,len(m.vertices),len(m.polygons),len(m.loop_triangles),sorted(areas,key=lambda a:a[1])[:4]);print('VALIDATE',m.validate(verbose=True,clean_customdata=True));m.calc_loop_triangles();print('AFTER',len(m.polygons),len(m.loop_triangles))
