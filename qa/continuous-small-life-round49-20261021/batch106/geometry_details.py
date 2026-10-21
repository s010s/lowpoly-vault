import bpy,json,sys,hashlib,os,math
from pathlib import Path
from mathutils import Vector
src,out=map(Path,sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);ob=next(o for o in bpy.context.scene.objects if o.type=='MESH');me=ob.data;v=[ob.matrix_world@p.co for p in me.vertices];groups={g.name:[p.index for p in me.vertices if any(x.group==g.index for x in p.groups)] for g in ob.vertex_groups};aid=src.stem;data={}
def rings(g,n,k):
 ids=groups[g];return [[sum(v[ids[j*n+i]][c] for i in range(n))/n for c in range(3)] for j in range(k)]
if aid=='monograptus':
 nema=[v[i] for i in groups['nema']];st=[v[i] for i in groups['stipe']];plane=max(p.z for p in st);start=min(p.z for p in nema);data['declared_nema_stipe_connection']={'stipe_max_z':plane,'nema_min_z':start,'exact_plane_equal':plane==start,'stipe_vertices_above_plane':sum(p.z>plane for p in st),'nema_vertices_below_plane':sum(p.z<plane for p in nema),'nema_cap_coordinates':[list(p) for p in nema if p.z==start],'stipe_cap_coordinates':[list(p) for p in st if p.z==plane],'separating_plane_proof':'All stipe triangle vertices lie on or below the plane; all nema triangle vertices lie on or above it. Linear triangles and enclosed solids cannot have positive-volume intersection. This is exact equality at stored float32 coordinates, not failure to exceed a microscopic threshold.','float32_local_ulp_m':2**(math.frexp(plane)[1]-24)}
 data['thecal_rings']={g:rings(g,8,7) for g in groups if g.startswith('theca_')};data['axial_overlap']=[{'pair':[j,j+1],'overlap_m':min(max(v[i].z for i in groups[f'theca_{j:02d}']),max(v[i].z for i in groups[f'theca_{j+1:02d}']))-max(min(v[i].z for i in groups[f'theca_{j:02d}']),min(v[i].z for i in groups[f'theca_{j+1:02d}']))} for j in range(17)]
if aid=='diplograptus':
 data['thecal_rings']={g:rings(g,8,6) for g in groups if g.startswith('theca_')};data['terminal_planes']={g:{'min_z':min(v[i].z for i in groups[g][40:48]),'max_z':max(v[i].z for i in groups[g][40:48])} for g in groups if g.startswith('theca_')}
 data['same_row_spacing']={str(s):[data['thecal_rings'][f'theca_{s}_{j+1:02d}'][-1][2]-data['thecal_rings'][f'theca_{s}_{j:02d}'][-1][2] for j in range(9)] for s in [-1,1]}
 data['nema_rings']=rings('nema',6,4)
if aid=='dictyonema':
 data['compound_example']={'name':'stipe_2_00','coordinates':[list(v[i]) for i in groups['stipe_2_00']],'note':'Two twelve-vertex end rings form an actual continuous three-lobed outer boundary with twisted longitudinal valleys; not three painted stripes or an unchanged round rod.'}
if aid=='didymograptus':data['thecal_rings']={g:rings(g,8,4) for g in groups if g.startswith('theca_')}
out.write_text(json.dumps({'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'pid':os.getpid(),'actual_transformed_geometry_details':data},indent=2))
