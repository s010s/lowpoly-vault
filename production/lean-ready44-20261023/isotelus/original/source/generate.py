# SPDX-License-Identifier: MIT
"""Deterministic original Isotelus gigas living reconstruction, approximately 30 mm.
Run: blender -b -t 2 --python source/generate.py -- --output-dir output
Only sibling dependencies, Blender and the Python standard library are required.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).parent.mkdir(parents=True,exist_ok=True);Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def lerp(x,knots):
    for (a,v),(b,w) in zip(knots,knots[1:]):
        if a<=x<=b:return v+(w-v)*(x-a)/(b-a)
    return knots[0][1] if x<knots[0][0] else knots[-1][1]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text()); col=setup_scene('isotelus',p['seed']);root=bpy.data.objects[col['asset_root']]
    root['taxon']='Isotelus gigas';root['body_length_m']=.03;root['thoracic_tergites']=8
    root['reference']='PRI76285 dorsal fossil scan; body about 3 cm excluding rock.'
    root['restoration']='Ventral anatomy, restrained small-specimen genal tips, color and posture inferred. No reference mesh or texture copied.'
    mats={k:make_material(k,v,roughness=.78 if k!='eyes' else .57) for k,v in p['palette'].items()};parts=[]
    def mesh(name,v,f,mat,meta=None):
        ob=mesh_object(name,v,f,mats[mat],col)
        for k,val in (meta or {}).items():ob[k]=val
        parts.append(ob);return ob
    def tube(name,pts,radii,mat,sides=6,meta=None):
        pts=list(map(Vector,pts));v=[];f=[]
        for j,pt in enumerate(pts):
            tangent=(pts[min(j+1,len(pts)-1)]-pts[max(0,j-1)]).normalized();ref=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((0,1,0))
            u=tangent.cross(ref).normalized();w=tangent.cross(u).normalized()
            for i in range(sides):
                a=2*math.pi*i/sides;v.append(tuple(pt+radii[j]*(math.cos(a)*u+math.sin(a)*w)))
        f.append(tuple(reversed(range(sides))))
        for j in range(len(pts)-1):
            for i in range(sides):
                a=j*sides+i;b=j*sides+(i+1)%sides;f.append((a,b,b+sides,a+sides))
        f.append(tuple((len(pts)-1)*sides+i for i in range(sides)))
        return mesh(name,v,f,mat,meta)
    def ellipsoid(name,c,scale,mat,n=20,rings=8,meta=None):
        v=[(c[0],c[1],c[2]-scale[2])];f=[]
        for j in range(1,rings):
            lat=-math.pi/2+math.pi*j/rings
            for i in range(n):
                a=2*math.pi*i/n;v.append((c[0]+scale[0]*math.cos(lat)*math.cos(a),c[1]+scale[1]*math.cos(lat)*math.sin(a),c[2]+scale[2]*math.sin(lat)))
        top=len(v);v.append((c[0],c[1],c[2]+scale[2]))
        for i in range(n):f.append((0,1+(i+1)%n,1+i))
        for j in range(rings-2):
            for i in range(n):
                a=1+j*n+i;b=1+j*n+(i+1)%n;f.append((a,b,b+n,a+n))
        for i in range(n):f.append((top,1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n))
        return mesh(name,v,f,mat,meta)
    # Broad closed low shield loft. End-point rows avoid coincident pole vertices.
    def shield(name,sections,zfun,mat):
        xs=[-1,-.96,-.86,-.72,-.56,-.40,-.28,-.14,0,.14,.28,.40,.56,.72,.86,.96,1]
        v=[];f=[];rows=[]
        for y,w in sections:
            if w==0:rows.append([len(v)]);v.append((0,y,zfun(0,y,True)));continue
            ids=[]
            for t in xs:ids.append(len(v));v.append((w*t,y,zfun(t,y,False)))
            rows.append(ids)
        for A,B in zip(rows,rows[1:]):
            if len(A)==1:
                for i in range(len(B)-1):f.append((A[0],B[i],B[i+1]))
            elif len(B)==1:
                for i in range(len(A)-1):f.append((A[i],B[0],A[i+1]))
            else:
                for i in range(len(A)-1):f.append((A[i],B[i],B[i+1],A[i+1]))
        boundary=[r[0] for r in rows]+rows[-1][1:]+[r[-1] for r in reversed(rows[:-1])]+list(reversed(rows[0][1:-1]))
        boundary=list(dict.fromkeys(boundary));off=len(v)
        # Duplicate the border below the dorsal surface, then cap a solid underside.
        for index in boundary:
            x,y,z=v[index];v.append((x,y,.00130))
        for i,a in enumerate(boundary):b=boundary[(i+1)%len(boundary)];f.append((a,b,off+(i+1)%len(boundary),off+i))
        center=len(v);v.append((0,(sections[0][0]+sections[-1][0])*.5,.00130))
        for i in range(len(boundary)):f.append((center,off+i,off+(i+1)%len(boundary)))
        return mesh(name,v,f,mat)
    # Cephalon: smooth shallow fused glabellar region, not a separately perched ball.
    head=[(-.015,0),(-.0147,.0023),(-.0140,.0041),(-.013,.0058),(-.0118,.0070),(-.0104,.0080),(-.0088,.00865),(-.0070,.00895),(-.00485,.0089)]
    def hz(t,y,tip):
        if tip:return .00178
        longitudinal=max(0,1-((y+.0086)/.0066)**2)
        return .00178+.00105*(1-t*t)*(.35+.65*longitudinal)+.00050*math.exp(-(t/.43)**4)*longitudinal
    shield('cephalon_broad_parabolic',head,hz,'shell')
    # Delicate border is part of the silhouette, not ornamental spines.
    edge=[(w,y,hz(1,y,False)+.000025) for y,w in head if w>0]
    edge=[(-x,y,z) for x,y,z in reversed(edge)]+[(0,-.015,.00180)]+edge
    tube('cephalic_border',edge,[.00010]*len(edge),'rim',sides=6)
    # Raised crescent-like eye ridges; eyes are conspicuous but not spheres on stalks.
    for s in (-1,1):
        ellipsoid('raised_eye_platform_'+str(s),(s*.00395,-.0084,.00304),(.00105,.00165,.00055),'axis',n=20,rings=8)
        ellipsoid('eye_visual_surface_'+str(s),(s*.00426,-.00855,.00339),(.00065,.00123,.00030),'eyes',n=18,rings=6)
        # Small specimens can retain short genal points. A 1.2 mm extension is inferred.
        tube('inferred_short_genal_tip_'+str(s),[(s*.00882,-.00555,.00186),(s*.00904,-.00472,.00177),(s*.00910,-.00405,.00167)],[.00027,.00017,.000055],'shell',meta={'inferred':True,'not_resolved_in_PRI_preview':True,'free_extension_m':.0012})
    # Eight distinct free thoracic tergites with lowered anterior flanges.
    # They overlap by 26 percent of pitch, including lateral pleurae. No empty slots.
    widths=[.00890,.00894,.00892,.00887,.00878,.00864,.00847,.00827]
    profile=[(-1,.00178),(-.94,.00198),(-.78,.00227),(-.60,.00258),(-.46,.00273),(-.39,.00268),(-.34,.00272),(-.28,.00315),(-.17,.00342),(0,.00352),(.17,.00342),(.28,.00315),(.34,.00272),(.39,.00268),(.46,.00273),(.60,.00258),(.78,.00227),(.94,.00198),(1,.00178)]
    pitch=.010/8;centers=[]
    for j,w in enumerate(widths):
        y0=-.005+j*pitch;centers.append(y0+.00058);v=[];f=[];n=len(profile);nr=5
        for bottom in (False,True):
            for k in range(nr):
                u=k/(nr-1)
                for x,z in profile:
                    xx=x*w;yy=y0-.00046+pitch*1.26*u+.00027*abs(x)**1.8
                    zz=.00127 if bottom else z+lerp(u,[(0,-.00022),(.25,.000015),(.5,.00008),(.75,.000015),(1,-.00011)])-.000045*j
                    v.append((xx,yy,zz))
        layer=n*nr
        for b in (0,1):
            for k in range(nr-1):
                for i in range(n-1):
                    q=b*layer+k*n+i;f.append((q,q+1,q+n+1,q+n) if b==0 else (q+n,q+n+1,q+1,q))
        perimeter=list(range(n))+[k*n+n-1 for k in range(1,nr)]+list(range(layer-2,layer-n-1,-1))+[k*n for k in range(nr-2,0,-1)]
        for k,a in enumerate(perimeter):b=perimeter[(k+1)%len(perimeter)];f.append((a,b,b+layer,a+layer))
        ob=mesh('thoracic_tergite_%02d'%(j+1),v,f,'shell',{'free_thoracic_index':j+1,'anterior_overlap_pitch_fraction':.26,'solid_pleural_laps':True})
        ob.data.materials.append(mats['axis'])
        for poly in ob.data.polygons:
            vv=[ob.data.vertices[i].co for i in poly.vertices]
            if max(abs(c.x) for c in vv)<w*.29 and sum(c.z for c in vv)/len(vv)>.00265:poly.material_index=1
    # Large smooth subtriangular pygidium, nearly the length and breadth of the head.
    tail=[(.00440,.00830),(.0055,.00835),(.0068,.00805),(.0083,.00745),(.0098,.00655),(.0112,.00535),(.0124,.00405),(.0135,.00275),(.0144,.00140),(.015,0)]
    def tz(t,y,tip):
        if tip:return .00152
        length=max(0,1-(y-.005)/.010)
        return .00160+.00108*(1-t*t)*(.30+.70*length)+.00032*math.exp(-(t/.34)**4)*length
    shield('pygidium_large_subtriangular',tail,tz,'shell')
    # A weak axial zone is incorporated into the shield surface, not deep ring grooves.
    # Species account mentions faint fused rings; exact relief not resolved here.
    edge=[(w,y,tz(1,y,False)+.00002) for y,w in tail if w>0]
    edge=[(-x,y,z) for x,y,z in edge]+[(0,.015,.00154)]+list(reversed(edge))
    tube('pygidial_smooth_border',edge,[.00009]*len(edge),'rim',sides=6)
    # Conservative ventral body and hypostome, concealed by dorsal shields from above.
    ellipsoid('ventral_body_inferred',(0,0,.00138),(.0058,.0138,.00039),'underside',n=28,rings=8)
    ellipsoid('inferred_hypostome',(0,-.0111,.00102),(.00135,.00215,.00030),'underside',n=16,rings=6)
    for s in (-1,1):
        tube('inferred_antenna_'+str(s),[(s*.00125,-.0123,.00112),(s*.0018,-.015,.00113),(s*.00315,-.0171,.00121),(s*.0047,-.0186,.00133),(s*.00535,-.0191,.00142)],[.00014,.00013,.00010,.000075,.00004],'underside',sides=7,meta={'evidence_scope':'Conservative reconstruction; not preserved PRI soft parts.'})
    def limbs(prefix,y,w,scale=1,pygidial=False):
        for s in (-1,1):
            z=.00112 if not pygidial else .00103
            pts=[(s*.0017*scale,y,z),(s*w*.45,y+.00013*scale,z-.00015),(s*w*.74,y-.00005*scale,.00067),(s*w*.91,y+.00012*scale,.00028),(s*w*.99,y+.00031*scale,.000075)]
            tube(prefix+'_walking_branch_'+str(s),pts,[.000145*scale,.000165*scale,.00013*scale,.00010*scale,.00006*scale],'underside',sides=6,meta={'inferred':True,'limb_region':'pygidial' if pygidial else 'cephalic_or_thoracic'})
            outer=[(s*w*.43,y+.00012*scale,z),(s*w*.66,y+.00042*scale,z+.000025),(s*w*.83,y+.00065*scale,z-.00008)]
            tube(prefix+'_outer_branch_'+str(s),outer,[.00010*scale,.00009*scale,.000055*scale],'underside',sides=5)
            for k in range(2):
                x=w*(.52+.17*k);yy=y+(.00028+.00021*k)*scale
                tube(prefix+'_filament_%d_%d'%(s,k),[(s*x,yy,z),(s*(x+.00038*scale),yy+.00034*scale,z-.00010)],[max(.000018,.000045*scale),max(.000018,.000035*scale)],'underside',sides=5)
    # Three cephalic pairs; first is deliberately smaller near the hypostome.
    for j,(y,w,sc) in enumerate([(-.0117,.0041,.66),(-.0094,.0067,.9),(-.0069,.0084,1)]):limbs('inferred_cephalic_pair_%02d'%(j+1),y,w,sc)
    for j,(y,w) in enumerate(zip(centers,widths)):limbs('inferred_thoracic_pair_%02d'%(j+1),y,w*1.04,.96)
    # Twelve small pairs concentrate along the axis beneath the large tail.
    # This is a declared visualization convention, NOT a soft-part count from PRI76285.
    for j in range(12):
        t=j/11;limbs('inferred_pygidial_pair_%02d'%(j+1),.0053+j*.00066,.00535*(1-.75*t),.58-.23*t,True)
    minz=min(v.co.z for ob in parts for v in ob.data.vertices)
    for ob in parts:
        for v in ob.data.vertices:v.co.z-=minz
    bpy.context.view_layer.update();src=audit_source(col,max_triangles=40000);write(out/'source-audit.json',src)
    if src['errors']:raise RuntimeError('Source audit errors: '+repr(src['errors']))
    bpy.context.preferences.filepaths.save_version=0
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:space.params.directory=b'.'*1023;space.params.directory=b'//';space.params.filename=''
    bpy.context.scene.render.filepath='//';bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),relative_remap=True)
    # Export-only batching keeps every semantic editable part in the native source.
    vertices=[];faces=[];mi=[];allmats=list(mats.values())
    for ob in parts:
        off=len(vertices);vertices.extend(tuple(v.co) for v in ob.data.vertices)
        for poly in ob.data.polygons:faces.append(tuple(off+i for i in poly.vertices));mi.append(allmats.index(ob.data.materials[poly.material_index]))
    combined=mesh_object('Isotelus_export_batched',vertices,faces,allmats,col)
    for poly,idx in zip(combined.data.polygons,mi):poly.material_index=idx
    bpy.ops.object.select_all(action='DESELECT');root.select_set(True);combined.select_set(True);bpy.context.view_layer.objects.active=combined
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={x.identifier for x in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Missing exporter RNA flags')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    report=audit_glb(out/'model.glb',40000,6,8);write(out/'glb-audit.json',report)
    if report['errors']:raise RuntimeError('GLB audit errors: '+repr(report['errors']))
    b=src['bounds_blender_m'];expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    delta=max(abs(report['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
    assert src['triangles']==report['scene_triangles'] and delta<1e-7
    write(out/'build-metadata.json',{'asset_id':'isotelus','revision':'r001','generator_sha256':digest(__file__),'params_sha256':digest(HERE/'params.json'),'blender_version':bpy.app.version_string,'seed':p['seed'],'export_options':options,'source_parts':len(parts),'source_triangles':src['triangles'],'source_to_glb_max_bounds_delta_m':delta,'glb_sha256':digest(out/'model.glb'),'semantic_sha256':report['semantic_sha256'],'nominal_dorsal_body_length_m':.03,'thoracic_free_tergites':8,'inferred_cephalic_limb_pairs':3,'inferred_thoracic_biramous_pairs':8,'inferred_pygidial_limb_pairs':12,'pygidial_limb_count_status':'Declared visualization convention, not measured PRI count or a proven dorsal-ring correspondence.','genal_tip_status':'Restrained short points consistent with possible small I. gigas condition; not resolved in the scan preview.','palette':p['palette'],'source_format':'Editable semantic meshes without preview stage. Export-only batching is regenerated.'})
    print(json.dumps({'status':'BUILT','triangles':report['scene_triangles'],'bytes':report['bytes'],'semantic_sha256':report['semantic_sha256']}))
if __name__=='__main__':main()
