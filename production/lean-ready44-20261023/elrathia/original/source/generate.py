# SPDX-License-Identifier: MIT
"""Original deterministic Elrathia living reconstruction. Run in Blender 4.3.2.
Usage: blender -b -t 2 --python source/generate.py -- --output-dir output
Only local sibling dependencies, Blender and the standard library are needed.
"""
from pathlib import Path
import argparse, hashlib, json, math, sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'deps'))
from asset_common import setup_scene, make_material, mesh_object, audit_source
from qa_glb import audit_glb


def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def interp(x, knots):
    for (a,v),(b,w) in zip(knots,knots[1:]):
        if a<=x<=b: return v+(w-v)*(x-a)/(b-a)
    return knots[0][1] if x<knots[0][0] else knots[-1][1]


def main():
    a=argparse.ArgumentParser(); a.add_argument('--output-dir',type=Path,required=True)
    args=a.parse_args(sys.argv[sys.argv.index('--')+1:]); out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=True)
    p=json.loads((HERE/'params.json').read_text()); collection=setup_scene(p['asset_id'],p['seed']); root=bpy.data.objects[collection['asset_root']]
    root['taxon']='Elrathia kingii'; root['reconstruction']='Conservative living restoration; ventral appendages inferred, not preserved in PRI76837.'
    root['thoracic_tergites']=13; root['body_length_m']=0.04; root['source_anchor']='Larger PRI76837 individual, approximately 4 cm; intact dorsal test reconstructed, not injury anatomy.'
    palette=p['palette']; mats={k:make_material(k,v,roughness=0.78 if k!='eyes' else 0.62) for k,v in palette.items()}
    parts=[]
    def mesh(name,v,f,mat,meta=None):
        obj=mesh_object(name,v,f,mats[mat],collection)
        if meta:
            for k,val in meta.items(): obj[k]=val
        parts.append(obj); return obj
    def ellipsoid(name,center,scale,mat,n=16,rings=6):
        v=[(center[0],center[1],center[2]-scale[2])]; f=[]
        for j in range(1,rings):
            lat=-math.pi/2+j*math.pi/rings
            for i in range(n):
                th=2*math.pi*i/n; v.append((center[0]+scale[0]*math.cos(lat)*math.cos(th),center[1]+scale[1]*math.cos(lat)*math.sin(th),center[2]+scale[2]*math.sin(lat)))
        top=len(v); v.append((center[0],center[1],center[2]+scale[2]))
        for i in range(n): f.append((0,1+(i+1)%n,1+i))
        for j in range(rings-2):
            for i in range(n):
                q=1+j*n+i; r=1+j*n+(i+1)%n; f.append((q,r,r+n,q+n))
        for i in range(n): f.append((top,1+(rings-2)*n+i,1+(rings-2)*n+(i+1)%n))
        return mesh(name,v,f,mat)
    def tube(name,points,radii,mat,sides=6):
        v=[]; f=[]; pts=list(map(Vector,points))
        for j,pt in enumerate(pts):
            tangent=(pts[min(j+1,len(pts)-1)]-pts[max(j-1,0)]).normalized()
            ref=Vector((0,0,1)) if abs(tangent.z)<.92 else Vector((0,1,0))
            u=tangent.cross(ref).normalized(); w=tangent.cross(u).normalized()
            for i in range(sides):
                th=2*math.pi*i/sides; v.append(tuple(pt+radii[j]*(math.cos(th)*u+math.sin(th)*w)))
        f.append(tuple(reversed(range(sides))))
        for j in range(len(pts)-1):
            for i in range(sides):
                q=j*sides+i; r=j*sides+(i+1)%sides; f.append((q,r,r+sides,q+sides))
        f.append(tuple((len(pts)-1)*sides+i for i in range(sides)))
        return mesh(name,v,f,mat)
    # Closed, fully modeled ventral body, kept below the shield margins.
    ellipsoid('ventral_body_inferred',(0,-.0005,.00245),(.0085,.0181,.00073),'underside',n=24,rings=8)
    # Semi-circular cephalon with deliberate longitudinal sections, not an untouched primitive.
    head_sections=[(-.020,0),(-.0197,.00265),(-.019,.0048),(-.0178,.0070),(-.0162,.0090),(-.0142,.0107),(-.0118,.0117),(-.0095,.0120),(-.008,.0119)]
    xs=[-1,-.9,-.72,-.5,-.28,0,.28,.5,.72,.9,1]
    v=[]; f=[]; rows=[]
    for y,w in head_sections:
        if w==0: rows.append([len(v)]); v.append((0,y,.00265)); continue
        ids=[]
        for t in xs:
            x=w*t; z=.00265+.00122*(1-t*t)+.00015*math.cos((y+.014)*180)
            ids.append(len(v)); v.append((x,y,z))
        rows.append(ids)
    for j in range(len(rows)-1):
        A,B=rows[j:j+2]
        if len(A)==1:
            for i in range(len(B)-1):f.append((A[0],B[i],B[i+1]))
        else:
            for i in range(len(A)-1):f.append((A[i],B[i],B[i+1],A[i+1]))
    boundary=[rows[0][0]]+[r[-1] for r in rows[1:]]+list(reversed(rows[-1][:-1]))+[r[0] for r in reversed(rows[1:-1])]
    underside=len(v); v.append((0,-.013,.00235))
    for i in range(len(boundary)): f.append((underside,boundary[(i+1)%len(boundary)],boundary[i]))
    mesh('cephalon_semicircular_intact',v,f,'shell',{'dorsal_reference':'PRI76837 larger individual','injury_reconstruction':'No break or injury is copied into normal anatomy.'})
    # Narrow modest glabella, rounded anterior lobe. Small eyes remain on cheeks.
    ellipsoid('glabella',(0,-.0133,.00389),(.003,.0051,.00115),'axis',n=20,rings=8)
    for sign in (-1,1):
        ellipsoid('small_eye_'+str(sign),(sign*.00535,-.0125,.00378),(.00062,.00105,.00040),'eyes',n=12,rings=6)
        tube('palpebral_ridge_'+str(sign),[(sign*.0047,-.0135,.0039),(sign*.0052,-.013,.00405),(sign*.0053,-.0118,.00397)], [.00016,.00018,.00013],'axis')
        tube('short_genal_point_'+str(sign),[(sign*.01155,-.0090,.00285),(sign*.012,-.0076,.00265),(sign*.0121,-.0068,.0025)],[.00040,.00024,.000065],'shell')
    # Anterior border ridge follows the same semi-circular shield, not a crown of spines.
    border=[]
    for i in range(25):
        th=math.pi*i/24; border.append((.0118*math.cos(th),-.008-.0118*math.sin(th),.00271))
    tube('cephalic_smooth_border',border,[.00022]*25,'rim',sides=6)
    # 13 free thoracic tergites: narrow raised axial lobe, two broad pleural lobes.
    widths=[.0118,.01185,.0118,.01165,.0114,.01105,.0106,.0101,.00955,.00895,.0083,.00755,.00675]
    xprofile=[(-1,.0026),(-.88,.0029),(-.65,.00335),(-.43,.00365),(-.30,.00358),(-.265,.00352),(-.22,.00435),(-.13,.00482),(0,.0050),(.13,.00482),(.22,.00435),(.265,.00352),(.30,.00358),(.43,.00365),(.65,.00335),(.88,.0029),(1,.0026)]
    # Each plate has a lowered anterior articulation flange and 0.22-pitch lap.
    # The first flange extends under the head rim; no lateral background slots.
    pitch=.023/13; rib_centers=[]
    for j,w in enumerate(widths):
        y0=-.008+j*pitch; rib_centers.append(y0+.00065); v=[]; f=[]
        n=len(xprofile); rows_n=5
        for bottom in (False,True):
            for k in range(rows_n):
                u=k/(rows_n-1)
                for x,z in xprofile:
                    outer=abs(x); yy=y0-.00065+u*pitch*1.22+.00048*outer**1.7
                    xx=x*w*(.99+.01*math.sin(math.pi*u))
                    zz=(.0020 if bottom else z+interp(u,[(0,-.00036),(.25,-.00005),(.5,.00011),(.75,.00003),(1,-.00010)])*(1-.24*j/12))
                    v.append((xx,yy,zz))
        layer=n*rows_n
        for b in (0,1):
            for k in range(rows_n-1):
                for i in range(n-1):
                    q=b*layer+k*n+i; f.append((q,q+1,q+1+n,q+n) if not b else (q+n,q+1+n,q+1,q))
        perimeter=list(range(n))+[k*n+n-1 for k in range(1,rows_n)]+list(range(layer-2,layer-n-1,-1))+[k*n for k in range(rows_n-2,0,-1)]
        for k in range(len(perimeter)):
            u=perimeter[k]; v1=perimeter[(k+1)%len(perimeter)]; f.append((u,v1,v1+layer,u+layer))
        obj=mesh('thoracic_tergite_%02d'%(j+1),v,f,'shell',{'free_thoracic_index':j+1,'paired_pleural_ribs':True})
        # Axial area uses the same geometry, only a restrained material distinction.
        obj.data.materials.append(mats['axis'])
        for poly in obj.data.polygons:
            coords=[obj.data.vertices[i].co for i in poly.vertices]
            if max(abs(co.x) for co in coords)<w*.225 and sum(co.z for co in coords)/len(coords)>.0035: poly.material_index=1
    # Small round smooth pygidium. Four low fused axial ridges, not free tergites.
    # Centered ellipse cap terminates at +0.020 m; anterior half is concealed by last rib.
    ellipsoid('small_rounded_pygidium',(0,.01635,.00288),(.00615,.00365,.00112),'shell',n=28,rings=8)
    ellipsoid('pygidial_axis',(0,.01625,.00381),(.00142,.00255,.00040),'axis',n=14,rings=6)
    for j in range(4):
        y=.0150+j*.00073; width=.00125*(1-.14*j)
        tube('fused_pygidial_axial_ridge_%d'%(j+1),[(-width,y,.00398),(0,y-.00006,.00422-j*.00008),(width,y,.00398)],[.00011,.00012,.00011],'axis',sides=6)
    # Restored paired antennules. Not preserved in the dorsal PRI fossil preview.
    for s in (-1,1):
        tube('inferred_antenna_'+str(s),[(s*.0017,-.0177,.0021),(s*.0024,-.020,.0020),(s*.0042,-.022,.0021),(s*.0059,-.0240,.00225),(s*.0065,-.0251,.00235)],[.00022,.00019,.00015,.00010,.000055],'underside',sides=8)
    # Biramous legs. One unit per free tergite, plus three conservative cephalic pairs.
    # Walking ramus is jointed; small outer filaments stay below the pleurae.
    def limb_pair(prefix,y,w,scale=1):
        for s in (-1,1):
            pts=[(s*.0022*scale,y,.00234),(s*w*.48,y+.00025,.00195),(s*w*.78,y-.00012,.00145),(s*w*.91,y+.00013,.00052),(s*w*.99,y+.00041,.00013)]
            obj=tube(prefix+'_endopod_'+str(s),pts,[r*scale for r in [.00022,.00024,.00021,.00016,.00010]],'underside',sides=6); obj['evidence_scope']='Group-informed restoration, not preserved PRI76837 soft parts.'
            base=(s*w*.45,y+.00015,.0021)
            outer=[base,(s*w*.70,y+.00065,.00216),(s*w*.91,y+.0010,.00195)]
            tube(prefix+'_outer_branch_'+str(s),outer,[.00016*scale,.00014*scale,.000075*scale],'underside',sides=6)
            for k in range(3):
                t=(k+1)/4; x=w*(.47+.35*t); yy=y+.00018+.00065*t
                tube(prefix+'_filament_%d_%d'%(s,k),[(s*x,yy,.0021),(s*(x+.00065*scale),yy+.00052*scale,.00184)],[.000065*scale,.000045*scale],'underside',sides=5)
    for j,(y,w) in enumerate(zip(rib_centers,widths)): limb_pair('inferred_thoracic_pair_%02d'%(j+1),y,w*1.045,scale=.92)
    for j,(y,w) in enumerate([(-.0164,.0072),(-.0139,.0095),(-.0112,.0111)]):limb_pair('inferred_cephalic_pair_%d'%(j+1),y,w,scale=.85)
    # Exactly four selected visualization pairs under the pygidial shield, progressively smaller.
    for j in range(4):
        limb_pair('inferred_pygidial_pair_%d'%(j+1),.0153+j*.00085,.0059-j*.0011,scale=.65-j*.095)
    # Place the lowest walking contact at Z=0 without changing the nominal dorsal length.
    minz=min(v.co.z for obj in parts for v in obj.data.vertices)
    for obj in parts:
        for v in obj.data.vertices:v.co.z-=minz
    bpy.context.view_layer.update(); src=audit_source(collection,max_triangles=40000)
    write(out/'source-audit.json',src)
    if src['errors']: raise RuntimeError('Source audit: '+repr(src['errors']))
    bpy.context.preferences.filepaths.save_version=0
    # Clear startup UI directories before serializing the editable source.
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params is not None:
                    space.params.directory=b'.'*1023
                    space.params.directory=b'//'
                    space.params.filename=''
    bpy.context.scene.render.filepath='//'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'model.blend'),relative_remap=True)
    # Export-only material batching preserves all named source parts in model.blend.
    vertices=[];faces=[];indices=[]; allmats=list(mats.values())
    for obj in parts:
        off=len(vertices); vertices.extend(tuple(v.co) for v in obj.data.vertices)
        for poly in obj.data.polygons:
            faces.append(tuple(off+i for i in poly.vertices)); indices.append(allmats.index(obj.data.materials[poly.material_index]))
    combined=mesh_object('Elrathia_export_batched',vertices,faces,allmats,collection)
    for poly,idx in zip(combined.data.polygons,indices):poly.material_index=idx
    bpy.ops.object.select_all(action='DESELECT'); root.select_set(True); combined.select_set(True); bpy.context.view_layer.objects.active=combined
    options=dict(export_format='GLB',use_selection=True,export_yup=True,export_apply=True,export_normals=True,export_texcoords=False,export_tangents=False,export_materials='EXPORT',export_vertex_color='NONE',export_animations=False,export_skins=False,export_morph=False,export_cameras=False,export_lights=False,export_extras=True,export_gpu_instances=False,export_gn_mesh=False,export_draco_mesh_compression_enable=False,export_use_gltfpack=False)
    available={v.identifier for v in bpy.ops.export_scene.gltf.get_rna_type().properties}
    if set(options)-available:raise RuntimeError('Missing exporter RNA flags')
    bpy.ops.export_scene.gltf(filepath=str(out/'model.glb'),**options)
    report=audit_glb(out/'model.glb',40000,6,8); write(out/'glb-audit.json',report)
    if report['errors']:raise RuntimeError('GLB audit: '+repr(report['errors']))
    b=src['bounds_blender_m']; expected={'min':[b['min'][0],b['min'][2],-b['max'][1]],'max':[b['max'][0],b['max'][2],-b['min'][1]]}
    error=max(abs(report['bounds_m'][k][i]-expected[k][i]) for k in expected for i in range(3))
    assert report['scene_triangles']==src['triangles'] and error<1e-7
    write(out/'build-metadata.json',{'asset_id':'elrathia','revision':'r001','generator_sha256':digest(__file__),'params_sha256':digest(HERE/'params.json'),'blender_version':bpy.app.version_string,'seed':p['seed'],'export_options':options,'source_triangles':src['triangles'],'source_parts':len(parts),'source_to_glb_max_bounds_delta_m':error,'glb_sha256':digest(out/'model.glb'),'semantic_sha256':report['semantic_sha256'],'nominal_dorsal_body_length_m':.04,'thoracic_free_tergites':13,'inferred_cephalic_limb_pairs':3,'inferred_thoracic_biramous_pairs':13,'inferred_pygidial_limb_pairs':4,'pygidial_limb_count_status':'Artistic group-informed visualization, not established from PRI76837.','palette':palette,'source_format':'Editable semantic meshes, no render stage; export-only batching is regenerated.'})
    print(json.dumps({'status':'BUILT','triangles':report['scene_triangles'],'bytes':report['bytes'],'semantic_sha256':report['semantic_sha256']}))
if __name__=='__main__':main()
