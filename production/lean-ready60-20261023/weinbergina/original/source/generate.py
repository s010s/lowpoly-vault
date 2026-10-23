# SPDX-License-Identifier: MIT
"""Build an original Weinbergina opitzi reconstruction.

Run with Blender's factory-startup background mode and two threads:
  blender -b -t 2 --python source/generate.py -- --output .
Only the adjacent params.json and declared source/deps are required.
The canonical export adapter emits intermediate names and maps them to the
contract's model.blend and model.glb at build time, never during packaging.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import shutil
import sys
import tempfile

SOURCE = Path(__file__).resolve().parent
sys.path.insert(0, str(SOURCE / 'deps'))
import bpy
from mathutils import Vector
from asset_common import setup_scene, make_material, mesh_object, export_asset


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


class Parts:
    """One editable semantic mesh; named vertex groups retain component identity."""
    def __init__(self, name, material, collection):
        self.name, self.material, self.collection = name, material, collection
        self.v, self.f, self.groups = [], [], []

    def add(self, name, vertices, faces):
        n = len(self.v)
        self.v += [tuple(v) for v in vertices]
        self.f += [tuple(n+i for i in f) for f in faces]
        self.groups.append((name, list(range(n, len(self.v)))))

    def finish(self, yshift, zshift):
        obj = mesh_object(self.name, [(x,y+yshift,z+zshift) for x,y,z in self.v], self.f, self.material, self.collection)
        for name, ids in self.groups:
            obj.vertex_groups.new(name=name).add(ids, 1.0, 'REPLACE')
        obj['component_names'] = [n for n,_ in self.groups]
        obj['construction'] = 'Original closed profile-based meshes; articulated joints overlap intentionally.'
        return obj


def tube(group, name, points, radii, sides=8):
    points = list(map(Vector,points))
    verts, faces = [], []
    for i,p in enumerate(points):
        tangent = (points[min(i+1,len(points)-1)] - points[max(i-1,0)]).normalized()
        basis = Vector((0,0,1))
        if abs(tangent.dot(basis)) > .9: basis=Vector((0,1,0))
        u = tangent.cross(basis).normalized()
        v = tangent.cross(u).normalized()
        for j in range(sides):
            a = 2*math.pi*j/sides
            verts.append(p + radii[i]*(math.cos(a)*u+math.sin(a)*v))
    faces += [tuple(reversed(range(sides)))]
    for i in range(len(points)-1):
        for j in range(sides):
            a=i*sides+j; b=i*sides+(j+1)%sides
            faces.append((a,b,b+sides,a+sides))
    faces += [tuple((len(points)-1)*sides+j for j in range(sides))]
    group.add(name,verts,faces)


def solid_patch(group, name, rows, bottom_depth):
    """Closed two-sided grid without duplicated seams or zero-area poles."""
    nr,nc=len(rows),len(rows[0]); verts=[tuple(p) for row in rows for p in row]
    topn=len(verts)
    verts += [(x,y,z-bottom_depth) for x,y,z in verts]
    faces=[]
    for r in range(nr-1):
        for c in range(nc-1):
            a=r*nc+c; b=a+1; d=a+nc; e=d+1
            faces += [(a,b,e,d),(a+topn,d+topn,e+topn,b+topn)]
    border=list(range(nc)) + [r*nc+nc-1 for r in range(1,nr)] + list(range((nr-1)*nc+nc-2,(nr-1)*nc-1,-1)) + [r*nc for r in range(nr-2,0,-1)]
    for i,a in enumerate(border):
        b=border[(i+1)%len(border)];faces.append((a,a+topn,b+topn,b))
    group.add(name,verts,faces)


def build(params):
    col=setup_scene('weinbergina',params['seed'])
    palette=params['palette']
    mats={k:make_material('Weinbergina-'+k,v,roughness=.83) for k,v in palette.items()}
    groups={k:Parts(n,mats[k],col) for k,n in [('shield','Prosoma-vaulted-shield'),('tergites','Opisthosoma-ten-free-tergites'),('legs','Six-pairs-walking-legs'),('chelicerae','One-pair-chelicerae'),('blade_feet','Six-inferred-blade-foot-groups'),('telson','Triangular-tapering-telson')]}
    # Rounded anterior shield, posterior notch, no modern long genal spines.
    outline=[]
    for i in range(33):
        a=math.pi*i/32
        outline.append((.0275*math.cos(a),-.040*math.sin(a)))
    for i in range(1,17):
        x=-.0275+.055*i/17
        outline.append((x,-.0010*math.exp(-(x/.010)**2)))
    N=len(outline); center=(0,-.017)
    verts=[(0,-.017,.020)]
    ring_scales=[.22,.45,.68,.85,1.0]
    for s in ring_scales:
        for x,y in outline:
            xx=center[0]+s*(x-center[0]); yy=center[1]+s*(y-center[1])
            height=.010+.010*(1-s*s)**.75
            # Subtle ophthalmic/cardial lobes, not conspicuous invented eyes.
            height += .00055*math.exp(-((abs(xx)-.0085)/.0035)**2-((yy+.014)/.013)**2)*(1-s)
            verts.append((xx,yy,height))
    faces=[]
    for j in range(N):faces.append((0,1+j,1+(j+1)%N))
    for r in range(len(ring_scales)-1):
        for j in range(N):
            a=1+r*N+j;b=1+r*N+(j+1)%N
            faces.append((a,b,b+N,a+N))
    lowerstart=len(verts)
    verts += [(x,y,.0087) for x,y in outline]
    for j in range(N):
        a=1+(len(ring_scales)-1)*N+j;b=1+(len(ring_scales)-1)*N+(j+1)%N
        faces.append((a,lowerstart+j,lowerstart+(j+1)%N,b))
    faces.append(tuple(reversed(range(lowerstart,lowerstart+N))))
    groups['shield'].add('Broad-vaulted-shield',verts,faces)
    # Ten genuinely separated segments; last three stay near equal in width.
    widths=[.049,.046,.042,.038,.033,.028,.0215,.017,.016,.015]
    xs=[-1,-.94,-.78,-.55,-.28,0,.28,.55,.78,.94,1]
    for i,width in enumerate(widths):
        y0=-.0012+i*.0036; length=.00320
        rows=[]
        for t in [0,.2,.52,.80,1]:
            row=[]
            for x in xs:
                # Broad axial dome and very modest pleural nodes; lateral blunt tips.
                yt=y0+t*length + .0006*(abs(x)**5)*t
                z=.0097-.00017*i + (.0040-.00018*i)*(1-x*x) + .00035*math.sin(math.pi*t)
                z += .00038*math.exp(-((abs(x)-.55)/.17)**2)*math.sin(math.pi*t)
                row.append((x*width/2*(.96+.055*math.sin(math.pi*t)),yt,z))
            rows.append(row)
        solid_patch(groups['tergites'],f'Free-tergite-{i+1:02d}',rows,.00115)
    # Seven pairs of prosomal appendages: one short cheliceral pair, six walking pairs.
    foot_y=[-.039,-.028,-.016,-.003,.010,.022]
    foot_x=[.024,.034,.039,.039,.035,.029]
    contacts=[]
    for side in [-1,1]:
        side_name='L' if side<0 else 'R'
        for i in range(6):
            cy=-.029+.0060*i; fy=foot_y[i]; fx=foot_x[i]
            pts=[(side*.0038,cy,.0093),(side*.0110,cy-.001,.0090),(side*.021,cy+(fy-cy)*.48,.0100),(side*fx,fy,.006),(side*(fx+.0023),fy+.0012,.0025),(side*(fx+.0014),fy-.0007,.0008)]
            tube(groups['legs'],f'{side_name}-walking-leg-{i+1}',pts,[.00165,.0018,.00145,.0011,.0007,.00040])
            # Single pointed tip and one small spur, not large terminal pincers.
            tip=(side*(fx+.0011),fy-.0020,0)
            tube(groups['legs'],f'{side_name}-terminal-claw-{i+1}',[pts[-1],tip],[.00044,.00012],6)
            tube(groups['legs'],f'{side_name}-short-spur-{i+1}',[pts[-2],(side*(fx+.0034),fy-.0003,.0014)],[.00043,.00013],6)
            contacts.append(tip)
        cp=[(side*.0028,-.026,.0085),(side*.0031,-.032,.0070),(side*.0040,-.035,.0058)]
        tube(groups['chelicerae'],side_name+'-chelicera-stem',cp,[.0011,.0010,.00075])
        tube(groups['chelicerae'],side_name+'-chelicera-fixed-digit',[cp[-1],(side*.0048,-.038,.0053),(side*.0039,-.039,.0052)],[.00065,.00045,.00014],6)
        tube(groups['chelicerae'],side_name+'-chelicera-moving-digit',[cp[-1],(side*.0026,-.037,.0053),(side*.0032,-.0384,.0052)],[.00055,.00036,.00014],6)
    # Six blade-foot groups are a disclosed composite restoration, not six fully preserved pairs.
    for i in range(6):
        width=widths[i]*.77; y0=.0010+i*.0037
        for side in [-1,1]:
            rows=[]
            for t in [0,.35,.70,1]:
                row=[]
                for j in range(17):
                    u=j/16
                    x=side*(.0013+(width/2-.0013)*u)
                    tooth=(.00034 if j%2 else -.00010)*t*t
                    y=y0+.0031*t*(.75+.25*math.sin(math.pi*u)) + tooth
                    z=.0075-.0001*i-.0011*t + .00020*math.sin(math.pi*u)
                    row.append((x,y,z))
                rows.append(row)
            solid_patch(groups['blade_feet'],f'Inferred-blade-group-{i+1}-{side}',rows,.0005)
    # Long slender triangular-section tail spine, inferred alive rather than bent fossil pose.
    tube(groups['telson'],'Triangular-section-taper',[ (0,.0347,.009),(0,.039,.0080),(0,.047,.0067),(0,.055,.0052) ],[.0021,.0017,.0010,.00013],3)
    # Root centered on actual terminal-claw floor footprint; no arbitrary display normalization.
    yshift=-(min(p[1] for p in contacts)+max(p[1] for p in contacts))/2
    objects=[g.finish(yshift,0) for g in groups.values()]
    # Clamp authored floor-contact terminal vertices once, preserving closed geometry.
    low=min(v.co.z for o in objects for v in o.data.vertices)
    for o in objects:
        for v in o.data.vertices:v.co.z-=low
    root=bpy.data.objects[col['asset_root']]
    root['taxon']='Weinbergina opitzi'
    root['free_tergites']=10;root['walking_pairs']=6;root['cheliceral_pairs']=1
    root['blade_foot_groups']=6;root['blade_foot_evidence']='Inferred published restoration; not six completely preserved pairs.'
    root['scale_basis']='95 mm approximate overall anatomy length; image-based estimate, about 15 percent uncertainty.'
    root['eye_evidence']='Uncertain; subtle relief only.'
    return col,objects


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path('.'))
    args=ap.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
    params=json.loads((SOURCE/'params.json').read_text())
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    collection,objects=build(params)
    bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=2
    bpy.context.preferences.filepaths.temporary_directory='//'
    bpy.context.scene.render.filepath='//'
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type=='FILE_BROWSER' and space.params:
                    space.params.directory=b'//'
    with tempfile.TemporaryDirectory(prefix='weinbergina-export-') as stage:
        record=export_asset('weinbergina',{'en':'Weinbergina opitzi','zh':'魏因贝尔吉纳鲎'},'invertebrates',collection,
            metadata={'generator':'source/generate.py','surface_profile':'palette-only','representation':'living-reconstruction'},
            output_root=stage,render=False,max_triangles=40000,max_materials=6,max_primitives=8,diagnostics=False)
        built=Path(stage)/'weinbergina'
        shutil.copyfile(built/'weinbergina.glb',out/'model.glb')
        shutil.copyfile(built/'weinbergina.blend',out/'model.blend')
        qa=json.loads((built/'qa.json').read_text());qa['glb']['file']='model.glb'
    report={'asset_id':'weinbergina','revision':'r001','glb_sha256':sha(out/'model.glb'),'source_sha256':sha(SOURCE/'generate.py'),'params_sha256':sha(SOURCE/'params.json'),
        'blender_version':bpy.app.version_string,'generator_seed':params['seed'],'exporter_version':'4.3.47',
        'geometry_policy':{'max_triangles':40000,'max_materials':6,'max_primitives':8,'max_glb_bytes':8388608},
        'export_options':record['export_options'],'source':qa['source'],'glb':qa['glb'],'bounds_roundtrip_max_error_m':qa['bounds_roundtrip_max_error_m'],
        'anatomical_components':{o.name:[n for n in o['component_names']] for o in objects},'authoring_forward':'-Y','glb_forward':'+Z','units':'meters',
        'interpretation':'Original living reconstruction; six blade-foot groups inferred, not fully preserved; no exact specimen scan.',
        'scope':'Static source/export geometry audit only; not independent visual acceptance, GPU, populated scene, user approval or publication.'}
    write(out/'build-report.json',report)
    print('BUILD_COMPLETE',report['glb_sha256'],report['glb']['scene_triangles'])


if __name__=='__main__':main()
