"""Original low-poly geology and trace assets, authored in meters in Blender 4.3.2.

No downloaded mesh, texture, palette, or third-party geometry is used. Build:
  blender -b -t 3 --python scripts/models/build_geology_traces.py -- --asset all
Use --quick for two 640 px draft renders, or --no-render for geometry verification.
"""
from pathlib import Path
import sys, math, json, argparse
import bpy, bmesh
from mathutils import Vector
from mathutils.geometry import delaunay_2d_cdt, tessellate_polygon

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene, make_material, mesh_object, export_asset, ground_asset, render_previews, render_diagnostics

PALETTE={'earth':'#8A715B','warm_stone':'#A89578','stone_light':'#C7B798','ochre':'#BD8B4D'}
SOURCES={
    'stratified-cliff':[{'title':'NPS: Kayenta Formation','url':'https://www.nps.gov/zion/learn/nature/kayenta.htm','use':'Sedimentary bedding context, not a reconstructed fossil locality.'}],
    'natural-arch':[{'title':'NPS Geodiversity Atlas: Arches','url':'https://www.nps.gov/articles/nps-geodiversity-atlas-arches-national-park-utah.htm','use':'Erosion and jointing context; original silhouette is not a copy of a named arch.'}],
    'dinosaur-nest':[{'title':'AMNH: Dinosaur Eggs','url':'https://www.amnh.org/dinosaurs/dinosaur-eggs','use':'Attribution of eggs requires evidence; this is an unassigned teaching concept.'},{'title':'AMNH: Follow the Fossil Specimen','url':'https://www.amnh.org/research/paleontology/vertebrate/fossil-preparation/follow-the-specimen','use':'Context for adults associated with nests, not a measurement source.'}],
    'three-toed-track':[{'title':'NPS: Footprints to Fossils','url':'https://www.nps.gov/zion/learn/nature/fossil-footprints.htm','use':'True tracks are depressions in a substrate.'},{'title':'NPS: Dinosaurs in the Fossil Record','url':'https://www.nps.gov/subjects/fossils/dinosaurs-in-the-fossil-record.htm','use':'Tracks are trace evidence and do not automatically identify a genus.'}]
}

def materials():
    return {name:make_material(name,value) for name,value in PALETTE.items()}

def closed_loft(name,rings,mat,col):
    n=len(rings[0]); verts=[tuple(p) for ring in rings for p in ring]
    assert all(len(r)==n for r in rings)
    faces=[tuple(range(n-1,-1,-1))]
    for j in range(len(rings)-1):
        for i in range(n):
            k=(i+1)%n
            faces.append((j*n+i,j*n+k,(j+1)*n+k,(j+1)*n+i))
    faces.append(tuple((len(rings)-1)*n+i for i in range(n)))
    return mesh_object(name,verts,faces,mat,col)

def block(name,center,size,angle,mat,col,lean=(0.0,0.0)):
    # An intentionally fractured, chamfered prism, not a displaced sphere.
    outline=[(-.48,-.28),(-.30,-.50),(.28,-.46),(.50,-.17),(.45,.27),(.20,.47),(-.28,.43),(-.50,.15)]
    profiles=[(0,.86),(0.18,1.0),(0.81,.88),(1,.62)]
    rings=[]
    for iz,(z,scale) in enumerate(profiles):
        ring=[]
        for i,(x,y) in enumerate(outline):
            px=x*size[0]*scale+lean[0]*z; py=y*size[1]*scale+lean[1]*z
            X=math.cos(angle)*px-math.sin(angle)*py+center[0]
            Y=math.sin(angle)*px+math.cos(angle)*py+center[1]
            Z=center[2]+z*size[2]
            if iz==3: Z+=size[2]*(.07*x-.04*y)
            ring.append((X,Y,Z))
        rings.append(ring)
    return closed_loft(name,rings,mat,col)

def base_metadata(slug,description,notes,features):
    return {'description':description,'generator':'scripts/models/build_geology_traces.py',
        'generator_model':'GPT-6 Astra, xhigh','generator_parameters':{'seed':29,'asset':slug},
        'sources':SOURCES[slug],'design_notes':notes,'recognition_features':features,
        'scientific_scope':{'en':'Evidence-informed stylized teaching/environment concept; not a species, specimen, or site reconstruction.','zh':'有依据的风格化教学或环境概念；不是具体物种、标本或地点的科学复原。'},
        'provenance':{'geometry':'Original procedural geometry with manually designed profiles and arrangements.','textures':'None','palette':'Original fixed lowpoly-vault palette','license':'CC-BY-4.0','author':'Leon Made This / s010s'}}


def build_cliff():
    slug='stratified-cliff'; col=setup_scene(slug,seed=29); m=materials()
    # Clockwise profile: the long, stepped -Y exposure is the main cliff face.
    outline=[(-2.10,-.22),(-2.00,-.57),(-1.73,-.75),(-1.22,-.81),(-.94,-.69),
             (-.42,-.74),(-.07,-.87),(.38,-.88),(.66,-.80),(.83,-.62),
             (1.22,-.63),(1.57,-.54),(1.99,-.29),(2.10,.08),(1.86,.48),
             (1.36,.70),(.76,.73),(.20,.66),(-.34,.76),(-.97,.64),(-1.58,.48),(-1.97,.20)]
    # Broad hard beds alternate with narrow, slightly recessed mudstone seams.
    levels=[0,.43,.67,1.20,1.42,2.04,2.52]
    material_keys=['warm_stone','earth','warm_stone','earth','warm_stone','stone_light']
    retreat=[(1,1),(1.0,1),(.985,.97),(.95,.96),(.91,.95),(.84,.92),(.78,.88)]
    for bed in range(6):
        lo,hi=levels[bed:bed+2]; thick=hi-lo
        rings=[]
        for step,t in enumerate([0,.12,.79,1]):
            height=lo+thick*t
            rx=retreat[bed][0]*(1-t)+retreat[bed+1][0]*t
            ry=retreat[bed][1]*(1-t)+retreat[bed+1][1]*t
            # Only soft beds erode noticeably; the stronger beds keep wide faces.
            inset=(.031 if bed in (1,3) else .012)*math.sin(math.pi*t)
            ring=[]
            for i,(x,y) in enumerate(outline):
                X=x*(rx-inset)+(-.10*height)
                # Upper right shoulder retreats at the actual fracture break.
                if x>.75: X-=max(0,height-1.35)*(.25+.09*(x-.75))
                Y=y*(ry-inset)+.025*height
                tilt=(.055*X+.018*Y)*min(1,height/.3)
                Z=height+tilt
                if bed==5 and step==3:
                    Z+=.015
                ring.append((X,Y,Z))
            rings.append(ring)
        obj=closed_loft(f'Bed_{bed+1:02d}_{"recessed_mudstone" if bed in (1,3) else "resistant_sandstone"}',rings,m[material_keys[bed]],col)
        obj['structure']='Continuous sedimentary bed with shallow dip; independent editable solid.'
    # Detached buttress preserves the slope at the right side and a real cleft.
    buttress=block('Right_fractured_buttress',(1.90,-.38,0),(1.04,1.00,1.48),-.19,m['warm_stone'],col,lean=(-.12,.04))
    buttress.data.materials.append(m['earth'])
    split_horizontal_bands(buttress,[.43,.67,1.20,1.42],[0,1,0,1,0])
    # Five deliberately unequal scree pieces, clustered at two fracture exits.
    for name,p,s,a,key in [
        ('Talus_front_left',(-1.78,-.87,0),(.61,.48,.34),-.24,'warm_stone'),
        ('Talus_left_chip',(-1.30,-1.01,0),(.29,.31,.15),.31,'stone_light'),
        ('Talus_right_slab',(.93,-.91,0),(.62,.44,.26),.28,'warm_stone'),
        ('Talus_right_chip',(1.55,-.70,0),(.33,.26,.14),-.43,'earth'),
        ('Talus_far_right',(1.99,-.43,0),(.34,.37,.23),.18,'warm_stone')]:
        block(name,p,s,a,m[key],col)
    ground_asset(col)
    md=base_metadata(slug,{'en':'A broad, asymmetrical sedimentary cliff with six tilted beds, recessed soft seams, a fractured shoulder, and restrained scree.','zh':'宽厚偏心的沉积岩崖：六层微倾层理、后退软层、断裂侧肩与少量崩积块。'},
        ['The high left mass, lower right shoulder, and two localized scree groups create a 60/30/10 hierarchy.','Bed colors encode sedimentary units; no polygon-wise random colors.','The present-day eroded landform is not asserted to exist in a particular prehistoric landscape.'],
        ['Continuous tilted bedding','High left plateau and lowered fractured shoulder','Localized angular scree'])
    return slug,{'en':'Stratified Cliff','zh':'层理岩崖'},'geology',col,md


def split_horizontal_bands(obj,heights,mat_indices):
    bm=bmesh.new(); bm.from_mesh(obj.data)
    for z in heights:
        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,
                              plane_co=(0,0,z),plane_no=(0,0,1),clear_outer=False,clear_inner=False)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
    bm.to_mesh(obj.data); bm.free(); obj.data.update()
    for p in obj.data.polygons:
        z=sum(obj.data.vertices[i].co.z for i in p.vertices)/len(p.vertices)
        band=sum(z>h+1e-5 for h in heights)
        p.material_index=mat_indices[band]


def build_arch():
    slug='natural-arch'; col=setup_scene(slug,seed=29); m=materials()
    # Paired inner/outer profiles are deliberately nonconcentric. The left mass
    # carries more visual weight; the opening's crown is shifted right.
    outer=[(-2.55,0),(-2.48,.57),(-2.40,1.15),(-2.22,1.77),(-1.99,2.25),(-1.65,2.70),
           (-1.18,3.02),(-.62,3.21),(-.05,3.24),(.56,3.13),(1.15,2.89),(1.66,2.50),
           (2.04,2.02),(2.29,1.45),(2.43,.78),(2.53,0)]
    inner=[(-1.20,0),(-1.17,.43),(-1.10,.89),(-.97,1.28),(-.76,1.68),(-.46,2.02),
           (-.08,2.26),(.38,2.35),(.83,2.27),(1.17,2.08),(1.40,1.78),(1.51,1.39),
           (1.56,1.02),(1.61,.66),(1.63,.31),(1.63,0)]
    verts=[]; faces=[]; n=len(outer)
    cross=[(0,.15),(.12,0),(.85,-.02),(1,.14),(1,.84),(.88,1.0),(.13,.98),(0,.83)]
    for i,((ox,oz),(ix,iz)) in enumerate(zip(outer,inner)):
        t=i/(n-1)
        front=-.58-.10*math.sin(t*math.pi)+.045*math.sin(i*1.1)
        thickness=1.31-.20*math.sin(t*math.pi)+.08*math.cos(i*.8)
        for u,d in cross:
            x=ix+(ox-ix)*u; z=iz+(oz-iz)*u
            y=front+thickness*d
            # Depth-dependent lateral lean avoids a flat extruded sign silhouette.
            x+=(d-.5)*(.11*math.sin(t*math.pi))
            if i not in (0,n-1): z+=(d-.5)*.075*math.cos(t*math.pi)
            verts.append((x,y,z))
    for i in range(n-1):
        for j in range(8): faces.append((i*8+j,i*8+(j+1)%8,(i+1)*8+(j+1)%8,(i+1)*8+j))
    faces.extend([tuple(range(7,-1,-1)),tuple((n-1)*8+j for j in range(8))])
    obj=mesh_object('Continuous_weathered_arch',verts,faces,[m['warm_stone'],m['earth'],m['stone_light']],col)
    split_horizontal_bands(obj,[.52,.66,1.62,1.74,2.74,2.91],[0,1,0,1,0,2,0])
    obj['structure']='Single connected arch volume with a true, full-depth opening and unequal foot thickness.'
    # Substantial foot rocks reinforce contact without constructing an artificial bridge.
    block('Left_foot_bedding',(-2.26,-.10,0),(.94,1.47,.28),-.12,m['warm_stone'],col)
    block('Right_foot_scree',(2.23,-.52,0),(.69,.67,.29),.28,m['warm_stone'],col)
    block('Left_toe_chip',(-1.64,-.78,0),(.36,.31,.19),-.3,m['stone_light'],col)
    ground_asset(col)
    md=base_metadata(slug,{'en':'A weathered natural stone arch with a right-shifted opening, heavy left support, thinner right leg, and subtle sedimentary seams.','zh':'原创侵蚀石拱：拱孔向右偏移、左侧厚重、右支脚收窄，并保留低调沉积层缝。'},
        ['The stone is a continuous volume; the hole is genuine geometry visible from both sides.','The arch profile was designed point by point rather than cut from the cliff or formed from a torus.','Rock deposition age and arch formation age are not treated as the same.'],
        ['Off-center full-depth opening','Unequal supports and thick crown','Broad weathered facets with continuous bedding'])
    md['budget_note']='672 triangles in the initial design: the broad continuous arch needs fewer than the T2 target; no filler subdivisions were added.'
    return slug,{'en':'Natural Arch','zh':'天然石拱'},'geology',col,md


def egg_mesh(name,center,length,width,height,angle,tilt,mat,col):
    # Six ten-sided cross sections and pointed caps form a subtly asymmetric egg.
    axis=Vector((math.cos(angle)*math.cos(tilt),math.sin(angle)*math.cos(tilt),math.sin(tilt)))
    side=Vector((-math.sin(angle),math.cos(angle),0))
    up=axis.cross(side).normalized()
    rows=[-.87,-.56,-.13,.31,.66,.88]; segments=10
    verts=[tuple(Vector(center)-axis*length/2)]
    for t in rows:
        radius=math.sqrt(1-t*t)*(1-.12*t)
        for j in range(segments):
            a=2*math.pi*j/segments
            p=Vector(center)+axis*(t*length/2)+side*(math.cos(a)*radius*width/2)+up*(math.sin(a)*radius*height/2)
            verts.append(tuple(p))
    end=len(verts); verts.append(tuple(Vector(center)+axis*length/2)); faces=[]
    for j in range(segments): faces.append((0,1+(j+1)%segments,1+j))
    for row in range(len(rows)-1):
        for j in range(segments):
            a=1+row*segments+j; b=1+row*segments+(j+1)%segments
            faces.append((a,b,b+segments,a+segments))
    start=1+(len(rows)-1)*segments
    for j in range(segments): faces.append((start+j,start+(j+1)%segments,end))
    obj=mesh_object(name,verts,faces,mat,col)
    obj['interpretation']='Intact stylized egg; color and dimensions are artistic, not fossil measurements.'
    return obj


def build_nest():
    slug='dinosaur-nest'; col=setup_scene(slug,seed=29); m=materials()
    segments=28
    # Low earthwork with two gaps; the hollow remains open and calm.
    profiles=[(.0,.033),(.27,.042),(.52,.071),(.64,.137),(.73,.172),(.84,.065),(.87,.019)]
    verts=[(0,0,.034)]; rings=[]
    for r,z in profiles[1:]:
        indices=[]
        for i in range(segments):
            a=2*math.pi*i/segments
            radius=r*(1+.055*math.sin(3*a+.4)+.030*math.cos(5*a))
            # Two intentionally collapsed berm sectors, not uniform jitter.
            notch=max(0,math.cos(a+1.80))**10*.105+max(0,math.cos(a-.15))**12*.095
            ridge_weight=max(0,1-abs(r-.70)/.25)
            Z=max(.016,z-notch*ridge_weight)+.007*math.cos(a-.4)*min(1,r/.5)
            indices.append(len(verts)); verts.append((radius*math.cos(a),radius*.85*math.sin(a),Z))
        rings.append(indices)
    faces=[]; mats=[]
    for i in range(segments): faces.append((0,rings[0][i],rings[0][(i+1)%segments])); mats.append(0)
    for j in range(len(rings)-1):
        for i in range(segments):
            faces.append((rings[j][i],rings[j+1][i],rings[j+1][(i+1)%segments],rings[j][(i+1)%segments]))
            mats.append(1 if j==4 and i in (10,11,12,13) else 0)
    bottom=[]
    for idx in rings[-1]:
        x,y,_=verts[idx]; bottom.append(len(verts)); verts.append((x*.95,y*.95,0))
    for i in range(segments): faces.append((rings[-1][i],bottom[i],bottom[(i+1)%segments],rings[-1][(i+1)%segments])); mats.append(0)
    faces.append(tuple(reversed(bottom))); mats.append(0)
    obj=mesh_object('Earthen_nest_basin_with_two_low_rims',verts,faces,[m['earth'],m['warm_stone']],col)
    for p,material_index in zip(obj.data.polygons,mats): p.material_index=material_index
    arrangements=[(3,.405,.365,.164,.150,.10),(29,.43,.348,.156,.144,.13),
                  (87,.425,.378,.159,.151,.06),(115,.437,.351,.152,.144,.13),
                  (183,.41,.367,.166,.149,.08),(210,.434,.342,.155,.142,.11),
                  (273,.413,.358,.161,.148,.06),(301,.43,.338,.153,.139,.09)]
    for i,(degrees,r,length,width,height,tilt) in enumerate(arrangements):
        a=math.radians(degrees); c=(r*math.cos(a),.85*r*math.sin(a),.128+(i%3)*.004)
        egg_mesh(f'Egg_{i+1:02d}_independently_editable',c,length,width,height,a,tilt,m['stone_light'],col)
    ground_asset(col)
    md=base_metadata(slug,{'en':'An unassigned dinosaur egg-nest teaching concept with a shallow earthen basin, two low rim sectors, and eight elongated eggs in four loose pairs.','zh':'不指定物种的恐龙卵窝教学示意：浅土窝、两处低边和四组疏松配对的八枚长卵。'},
        ['This is not a woven bird nest and is not attributed to any dinosaur species or museum animal.','The open center, unequal pair angles, and two collapsed rim sectors prevent a mechanical egg ring.','Egg number, shell color, dimensions, and arrangement are artistic simplifications, not a specimen reconstruction.'],
        ['Shallow concave earthen basin','Eight distinct elongated eggs','Two collapsed rim sectors and open center'])
    md['budget_note']='T2 rather than the initial T1 nest target: editable, recognizably elongated eggs retain broad ten-sided facets.'
    return slug,{'en':'Dinosaur Nest','zh':'恐龙卵窝'},'traces',col,md


def inside_polygon(p,polygon):
    x,y=p; inside=False
    for i in range(len(polygon)):
        ax,ay=polygon[i]; bx,by=polygon[(i+1)%len(polygon)]
        if (ay>y)!=(by>y) and x<(bx-ax)*(y-ay)/(by-ay)+ax: inside=not inside
    return inside


def triangulate_indices(vertices,indices):
    # Constrained triangulation retains concave toe clefts and handles collinear
    # perimeter vertices without the zero-area ears a generic ngon can create.
    coords=[Vector(vertices[i][:2]) for i in indices]
    edges=[(i,(i+1)%len(indices)) for i in range(len(indices))]
    out,_,triangles,_,_,_=delaunay_2d_cdt(coords,edges,[],0,1e-8)
    mapping=[]
    for p in out:
        nearest=min(range(len(coords)),key=lambda i:(coords[i]-p).length_squared)
        assert (coords[nearest]-p).length_squared<1e-10
        mapping.append(indices[nearest])
    result=[]
    for tri in triangles:
        center=(sum(out[i].x for i in tri)/len(tri),sum(out[i].y for i in tri)/len(tri))
        if inside_polygon(center,coords):result.append(tuple(mapping[i] for i in tri))
    return result


def build_tracks():
    slug='three-toed-track'; col=setup_scene(slug,seed=29); m=materials()
    boundary=[(-1.36,-.41),(-1.16,-.64),(-.64,-.70),(-.23,-.64),(.23,-.71),(.69,-.64),(1.15,-.56),(1.36,-.31),
              (1.39,.13),(1.19,.47),(.85,.60),(.34,.68),(-.14,.59),(-.61,.66),(-1.08,.53),(-1.35,.27)]
    # A single continuous heel / three toe contour. The long middle digit and
    # diverging side digits are illustrative, never a genus diagnosis.
    shape=[(0,.20),(-.065,.19),(-.115,.12),(-.12,.035),(-.19,-.02),(-.26,-.09),
           (-.33,-.18),(-.375,-.29),(-.36,-.335),(-.33,-.35),(-.29,-.30),(-.24,-.23),
           (-.17,-.16),(-.12,-.09),(-.075,-.105),(-.082,-.21),(-.077,-.32),(-.055,-.44),
           (-.015,-.52),(.025,-.515),(.064,-.43),(.085,-.31),(.075,-.21),(.079,-.13),
           (.119,-.10),(.20,-.16),(.28,-.25),(.34,-.30),(.375,-.29),(.385,-.255),
           (.34,-.18),(.27,-.105),(.19,-.045),(.135,.025),(.13,.10),(.072,.18)]

    # Map local -Y toe direction to the slab's +X travel direction.
    placements=[(-.86,.18,math.radians(87),.76),(-.10,-.19,math.radians(97),.74),(.67,.16,math.radians(83),.77)]
    outlines=[]; centers=[]
    for cx,cy,a,s in placements:
        points=[]
        for x,y in shape:
            # Shift the contour center to its visual center before transforming.
            y+=.13
            points.append((cx+s*(x*math.cos(a)-y*math.sin(a)),cy+s*(x*math.sin(a)+y*math.cos(a))))
        outlines.append(points); centers.append((cx,cy))
    outer_rims=[[(cx+(x-cx)*1.13,cy+(y-cy)*1.13) for x,y in ps] for ps,(cx,cy) in zip(outlines,centers)]
    coords=list(boundary); edges=[]; loops=[]
    for poly in [boundary]+outer_rims:
        if poly is boundary: ids=list(range(len(poly)))
        else: ids=list(range(len(coords),len(coords)+len(poly))); coords.extend(poly)
        loops.append(ids)
        edges.extend((ids[i],ids[(i+1)%len(ids)]) for i in range(len(ids)))
    coords.extend([(-1.14,-.2),(-.78,-.42),(-.48,.13),(.28,.05),(.40,-.41),(.89,-.29),(1.10,.20),(-.11,.40)])
    out,_,triangles,_,_,_=delaunay_2d_cdt([Vector(p) for p in coords],edges,[],0,1e-7)
    top=lambda x,y:.133+.006*x+.004*y
    vertices=[(p.x,p.y,top(p.x,p.y)) for p in out]; faces=[]; indices=[]
    for t in triangles:
        if len(t)<3: continue
        center=(sum(out[i].x for i in t)/len(t),sum(out[i].y for i in t)/len(t))
        if inside_polygon(center,boundary) and not any(inside_polygon(center,poly) for poly in outer_rims):
            faces.append(tuple(t)); indices.append(0)
    def topindex(p):
        nearest=min(range(len(out)),key=lambda i:(out[i].x-p[0])**2+(out[i].y-p[1])**2)
        assert (out[nearest].x-p[0])**2+(out[nearest].y-p[1])**2<1e-10
        return nearest
    edge_top=[topindex(p) for p in boundary]
    edge_mid=[]; edge_bottom=[]
    for x,y in boundary:
        edge_mid.append(len(vertices));vertices.append((x*1.008,y*1.008,.048+.004*x))
        edge_bottom.append(len(vertices));vertices.append((x*.975,y*.975,0))
    for a,b in [(edge_top,edge_mid),(edge_mid,edge_bottom)]:
        for i in range(len(a)):
            faces.append((a[i],b[i],b[(i+1)%len(a)],a[(i+1)%len(a)])); indices.append(1)
    bottom_cap=triangulate_indices(vertices,list(reversed(edge_bottom)));faces.extend(bottom_cap); indices.extend([1]*len(bottom_cap))
    cavity_records=[]
    for number,(outline,outer,(cx,cy)) in enumerate(zip(outlines,outer_rims,centers)):
        prev=[topindex(p) for p in outer]
        # Raised pressure lip is 8 mm; the footprint floor is 46 mm BELOW the
        # adjacent substrate. There are no floating or positive toe pieces.
        for scale,offset,material_index in [(1.045,.008,0),(.98,-.006,0),(.78,-.046,1)]:
            ring=[]
            for x,y in outline:
                X=cx+(x-cx)*scale;Y=cy+(y-cy)*scale
                ring.append(len(vertices));vertices.append((X,Y,top(X,Y)+offset))
            for i in range(len(ring)):
                faces.append((prev[i],ring[i],ring[(i+1)%len(ring)],prev[(i+1)%len(ring)]));indices.append(material_index)
            prev=ring
        bottomfaces=triangulate_indices(vertices,prev); faces.extend(bottomfaces);indices.extend([1]*len(bottomfaces))
        cavity_records.append({'index':number+1,'floor_below_adjacent_substrate_m':.046,'rim_above_substrate_m':.008,'toe_count':3})
    obj=mesh_object('Mud_slab_with_three_true_recessed_tracks',vertices,faces,[m['warm_stone'],m['earth']],col)
    for p,material_index in zip(obj.data.polygons,indices): p.material_index=material_index
    obj['track_form']='Negative impressions in a single watertight slab, including shallow pressure lips.'
    ground_asset(col)
    md=base_metadata(slug,{'en':'A thin irregular mud slab with three staggered, genuinely recessed three-toed impressions and small pressure lips.','zh':'薄而不规则的泥板，带三枚交错排列的真实凹陷三趾印与轻微挤压边缘。'},
        ['Each footprint is a geometric cavity 46 mm below its local substrate, with an 8 mm raised lip.','The long middle digit, shorter diverging side digits, and alternating lateral offset establish a clear travel direction.','Depth, step length, toe proportions, and wet/dry color are illustrative. They must not be used to infer a species, speed, or body mass.'],
        ['Three negative tridactyl impressions','Alternating step placement','Thin irregular mud substrate'])
    md['cavity_geometry']=cavity_records
    return slug,{'en':'Three-toed Track Slab','zh':'三趾足迹泥板'},'traces',col,md

BUILDERS={'stratified-cliff':build_cliff,'natural-arch':build_arch,'dinosaur-nest':build_nest,'three-toed-track':build_tracks}

def main():
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    ap=argparse.ArgumentParser();ap.add_argument('--asset',default='all',choices=['all']+list(BUILDERS));ap.add_argument('--quick',action='store_true');ap.add_argument('--no-render',action='store_true');ap.add_argument('--output-root');args=ap.parse_args(argv)
    result=[]
    for key,fn in BUILDERS.items():
        if args.asset not in ('all',key): continue
        slug,title,category,col,md=fn()
        bpy.context.scene.render.threads_mode='FIXED';bpy.context.scene.render.threads=3
        views=('hero','top') if args.quick else ('hero','reversehero')
        record=export_asset(slug,title,category,col,metadata=md,output_root=args.output_root,render=not args.no_render,views=views,max_triangles=2600,max_materials=4,max_primitives=24,resolution=640 if args.quick else 1024,samples=16 if args.quick else 40,diagnostics=False)
        if not args.no_render and not args.quick:
            output_dir=Path(args.output_root or ROOT/'assets'/'prehistoric'/category)/slug
            extra=render_previews(col,output_dir,('front','side','rear','top'),resolution=640,samples=24)
            extra+=render_diagnostics(col,output_dir,resolution=640,samples=24)
            qa_path=output_dir/'qa.json';qa=json.loads(qa_path.read_text())
            qa['previews']['files']+= [Path(p).name for p in extra]
            qa['previews']['diagnostic_resolution']=640
            qa['previews']['diagnostic_samples']=24
            qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
        result.append({'id':slug,'triangles':record['triangles'],'glb_bytes':record['glb_bytes'],'dimensions':record['dimensions']})
    print('GEOLOGY_TRACES_RESULT='+json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
