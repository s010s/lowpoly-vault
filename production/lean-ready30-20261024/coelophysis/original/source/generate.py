# SPDX-License-Identifier: MIT
"""Original deterministic Coelophysis living reconstruction.
Run Blender with two threads, --python-exit-code 1, and --python
source/generate.py -- --output-dir DESTINATION. Rebuilds do not render.
"""
from pathlib import Path
import argparse, hashlib, json, math, os, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene,make_material,mesh_object,audit_source
from qa_glb import audit_glb
from qa_glb_scale_aware import audit_glb as audit_scale_aware
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d): Path(p).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

class Form:
    def __init__(self): self.v=[]; self.f=[]; self.mi=[]
    def loft(self,stations,sides=12,mat=0,band=False):
        base=len(self.v)
        for i,(co,rx,rz) in enumerate(stations):
            c=Vector(co); t=Vector(stations[min(i+1,len(stations)-1)][0])-Vector(stations[max(i-1,0)][0]); t.normalize()
            lateral=Vector((1,0,0)) if abs(t.x)<.88 else Vector((0,1,0))
            lateral=(lateral-t*t.dot(lateral)).normalized(); vertical=t.cross(lateral).normalized()
            for k in range(sides):
                a=2*math.pi*k/sides; self.v.append(tuple(c+lateral*math.cos(a)*rx+vertical*math.sin(a)*rz))
        for i in range(len(stations)-1):
            for k in range(sides):
                a=base+i*sides+k; b=base+i*sides+(k+1)%sides; c=base+(i+1)*sides+(k+1)%sides; d=base+(i+1)*sides+k
                s=math.sin((k+.5)*2*math.pi/sides); m=(2 if s>.72 else 1 if s<-.45 else 0) if band else mat
                self.f.extend([(a,b,d),(b,c,d)] if (i+k)%2 else [(a,b,c),(a,c,d)]); self.mi.extend([m,m])
        for ring,flip in ((0,True),(len(stations)-1,False)):
            center=len(self.v); self.v.append(tuple(stations[ring][0]))
            for k in range(sides):
                a=base+ring*sides+k; b=base+ring*sides+(k+1)%sides; self.f.append((center,b,a) if flip else (center,a,b)); self.mi.append(mat)
    def object(self,name,mats,col):
        o=mesh_object(name,self.v,self.f,mats,col)
        for p,m in zip(o.data.polygons,self.mi): p.material_index=m
        return o

def interpolate(stations,steps=2):
    result=[]; rows=[list(c)+[a,b] for c,a,b in stations]
    for i in range(len(rows)-1):
        p0,p1,p2,p3=rows[max(0,i-1)],rows[i],rows[i+1],rows[min(len(rows)-1,i+2)]
        for j in range(steps):
            t=j/steps; q=[.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t) for a,b,c,d in zip(p0,p1,p2,p3)]
            result.append((q[:3],max(q[3],.0015),max(q[4],.0015)))
    result.append(stations[-1]); return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True);params=json.loads((HERE/'params.json').read_text());col=setup_scene(params['asset_id'],params['seed'])
    mats=[make_material(n,c,roughness=.86 if n not in ('Eye','Iris') else .36) for n,c in params['palette'].items()]
    skin,ventral,dorsal,eye,iris,tooth,claw,mouth=mats
    body=Form();body.loft(interpolate([
      ((.035,1.43,.79),.0017,.002),((.035,1.30,.785),.007,.009),((.026,1.12,.78),.015,.019),
      ((.016,.92,.765),.024,.030),((.005,.72,.75),.035,.043),((0,.53,.735),.048,.060),
      ((0,.36,.715),.065,.086),((0,.20,.70),.091,.120),((0,.06,.695),.107,.144),
      ((0,-.10,.695),.103,.151),((0,-.23,.705),.084,.139),((0,-.32,.735),.064,.108),
      ((0,-.385,.79),.050,.076),((0,-.44,.865),.040,.059),((0,-.49,.945),.036,.049),
      ((0,-.55,1.015),.035,.045),((0,-.62,1.065),.037,.045),((0,-.70,1.079),.042,.048),
      ((0,-.755,1.075),.040,.046)]),16,band=True);body.object('Axial-body-neck-tail',mats[:3],col)
    head=Form();head.loft(interpolate([
      ((0,-.69,1.080),.033,.045),((0,-.74,1.088),.058,.063),((0,-.80,1.083),.057,.062),
      ((0,-.86,1.077),.046,.048),((0,-.96,1.067),.031,.030),((0,-1.065,1.058),.025,.023),
      ((0,-1.16,1.055),.018,.019),((0,-1.176,1.055),.005,.013)]),12,band=True);head.object('Low-wedge-upper-head',mats[:3],col)
    jaw=Form();jaw.loft(interpolate([
      ((0,-.735,1.039),.041,.023),((0,-.81,1.015),.044,.019),((0,-.92,1.006),.032,.013),
      ((0,-1.05,1.011),.024,.009),((0,-1.154,1.018),.014,.007),((0,-1.17,1.022),.003,.003)]),10);jaw.object('Slender-lower-jaw',[ventral],col)
    inner=Form();inner.loft([((0,-.765,1.030),.031,.010),((0,-.86,1.031),.035,.012),((0,-.98,1.032),.023,.010),((0,-1.12,1.034),.014,.007)],8);inner.object('Recessed-oral-surface',[mouth],col)
    teeth=Form()
    for s in (-1,1):
        for i in range(10):
            y=-.845-i*.029;width=.040-(i/9)*.022;z=1.039-(i/9)*.002;length=.013 if i<6 else .010
            teeth.loft([((s*width,y,z),.0034,.0034),((s*width,y+.001,z-length*.65),.0023,.0020),((s*width,y+.003,z-length),.0011,.0011)],5)
    teeth.object('Restrained-maxillary-tooth-row',[tooth],col)
    dark=Form();ir=Form();pupils=Form();nostrils=Form()
    for s in (-1,1):
        dark.loft([((s*.052,-.783,1.108),.019,.018),((s*.061,-.783,1.108),.017,.016),((s*.063,-.783,1.108),.010,.011)],12)
        ir.loft([((s*.0635,-.789,1.109),.010,.011),((s*.0645,-.789,1.109),.009,.010)],12)
        pupils.loft([((s*.0648,-.792,1.110),.0045,.007),((s*.0655,-.792,1.110),.004,.0065)],10)
        nostrils.loft([((s*.022,-1.119,1.067),.006,.003),((s*.025,-1.119,1.067),.004,.002)],8)
    dark.object('Lateral-eye-lids',[dorsal],col);ir.object('Ochre-irises',[iris],col);pupils.object('Round-eye-pupils',[eye],col);nostrils.object('Nostrils',[mouth],col)
    talons=Form()
    for s in (-1,1):
        dy=.052*s; label='Left' if s<0 else 'Right'
        leg=Form();leg.loft(interpolate([
          ((s*.079,.10+dy,.71),.062,.083),((s*.111,.015+dy,.60),.067,.075),((s*.135,-.075+dy,.475),.041,.043),
          ((s*.135,-.063+dy,.440),.029,.032),((s*.137,.055+dy,.300),.026,.029),((s*.139,.125+dy,.215),.022,.023),
          ((s*.141,.108+dy,.165),.017,.018),((s*.145,.041+dy,.059),.017,.019),((s*.145,.025+dy,.040),.022,.016)]),12)
        leg.object(label+'-thigh-shin-metatarsus',[skin],col);foot=Form()
        for index,spread in enumerate((-.046,0,.046)):
            length=.143 if index==1 else .111;start=Vector((s*.145,.028+dy,.034));end=Vector((s*.145+spread,-length+dy,.020));mid=start.lerp(end,.55);mid.z=.028
            foot.loft([(start,.012,.014),(mid,.011,.012),(end,.008,.008)],8)
            tip=end+Vector((spread*.13,-.034,-.010));talons.loft([(end,.008,.008),(end.lerp(tip,.55),.005,.005),(tip,.0014,.0014)],6)
        foot.loft([((s*.137,.040+dy,.070),.007,.008),((s*.116,.069+dy,.050),.006,.006),((s*.108,.059+dy,.037),.003,.003)],8);foot.object(label+'-three-toed-foot',[ventral],col)
        arm=Form();arm.loft(interpolate([
          ((s*.065,-.263,.740),.027,.034),((s*.101,-.255,.670),.027,.030),((s*.125,-.226,.602),.019,.022),
          ((s*.125,-.256,.582),.016,.017),((s*.132,-.335,.602),.014,.016),((s*.133,-.386,.616),.012,.014)]),10);arm.object(label+'-flexed-forelimb',[skin],col)
        hand=Form();hand.loft([((s*.133,-.380,.617),.015,.020),((s*.136,-.414,.610),.012,.024),((s*.136,-.435,.600),.010,.018)],8)
        for i,dz in enumerate((-.017,0,.017)):
            a=Vector((s*.136,-.427,.608+dz));b=Vector((s*.126,-.466-(.012 if i==1 else 0),.603+dz));c=b+Vector((-s*.013,-.013,-.013))
            hand.loft([(a,.006,.007),(b,.005,.006),(c,.0038,.004)],7);end=c+Vector((-s*.005,.006,-.016));talons.loft([(c,.0045,.0045),(c.lerp(end,.55),.003,.003),(end,.0012,.0012)],6)
        hand.object(label+'-inward-grasping-hand',[ventral],col)
    talons.object('Foot-and-hand-claws',[claw],col)
    # Keep skull length about one eighth of total length, inferred from the casts.
    head_names={'Low-wedge-upper-head','Slender-lower-jaw','Recessed-oral-surface','Restrained-maxillary-tooth-row','Lateral-eye-lids','Ochre-irises','Round-eye-pupils','Nostrils'}
    for o in col.objects:
        if o.name in head_names:
            for v in o.data.vertices:
                v.co.y=-.70+(v.co.y+.70)*.67
                v.co.z=1.07+(v.co.z-1.07)*.88
    meshes=[o for o in col.objects if o.type=='MESH'];minz=min(v.co.z for o in meshes for v in o.data.vertices)
    for o in meshes:
        for v in o.data.vertices: v.co.z-=minz
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    source=audit_source(col,params['budgets']['max_triangles'])
    if source['errors']: raise RuntimeError(source['errors'])
    bpy.context.preferences.filepaths.save_version=0;bpy.context.scene['source_generator']='source/generate.py';bpy.context.scene['reconstruction']='Original Coelophysis bauri living reconstruction; not specimen scan.'
    bpy.context.scene.render.filepath='//renders/'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
                    space.params.filename=''
    os.chdir(out);bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'));bpy.ops.object.select_all(action='DESELECT')
    for o in col.objects: o.select_set(True)
    bpy.context.view_layer.objects.active=bpy.data.objects['coelophysis']
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available: raise RuntimeError('Exporter option mismatch')
    bpy.ops.export_scene.gltf(filepath='model.glb',**options)
    b=params['budgets'];glb=audit_glb(out/'model.glb',b['max_triangles'],b['max_materials'],b['max_primitives']);scale=audit_scale_aware(out/'model.glb',b['max_triangles'],b['max_materials'],b['max_primitives'])
    for report in (glb,scale):
        report.pop('path',None); report['file']='model.glb'
    bb=source['bounds_blender_m'];low=[bb['min'][0],bb['min'][2],-bb['max'][1]];high=[bb['max'][0],bb['max'][2],-bb['min'][1]]
    error=max(abs(glb['bounds_m'][k][i]-v[i]) for k,v in [('min',low),('max',high)] for i in range(3))
    if glb['errors'] or scale['errors'] or error>1e-4 or source['triangles']!=glb['scene_triangles'] or glb['bytes']>b['max_glb_bytes']: raise RuntimeError({'baseline':glb['errors'],'relative':scale['errors'],'bounds_error':error})
    (out/'qa/evidence').mkdir(parents=True,exist_ok=True)
    write(out/'qa/evidence/build.json',{'status':'PASS','claim_scope':'SOURCE_AND_STATIC_GLB_ONLY','blender_version':bpy.app.version_string,'generator_sha256':sha(HERE/'generate.py'),'params_sha256':sha(HERE/'params.json'),'glb_sha256':sha(out/'model.glb'),'blend_sha256':sha(out/'model.blend'),'export_options':options,'source':source,'glb':glb,'scale_aware_audit':scale,'source_export_bounds_error_m':error,'render_threads':2,'unknown':['independent visual review','GPU rendering','combined scene','user acceptance','deployment']})
    print('BUILD_COMPLETE',sha(out/'model.glb'),glb['scene_triangles'],glb['bytes'])
if __name__=='__main__': main()
