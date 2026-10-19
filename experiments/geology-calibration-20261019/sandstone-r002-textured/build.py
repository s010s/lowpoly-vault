# SPDX-License-Identifier: MIT
"""Original sandstone r002: continuous weathered shell + baked analytic color atlas.
blender -b -t 2 --python experiments/geology-calibration-20261019/sandstone-r002-textured/build.py
The consulted NPS image is never loaded or sampled by this generator.
"""
import bpy,sys,math,json,struct,zlib,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from asset_common import setup_scene,make_material,mesh_object,export_asset
SEED=20261019;SLUG='cross-bedded-sandstone';SIZE=512
# Original coherent shell: rounded joint block, broad fracture truncations,
# a few resistance-related ledges and shallow recesses, no lamina-by-lamina slots.
def point(u,v,w):
 k=(abs(u)**5+abs(v)**5+abs(w)**5)**(-.2)
 x=.41*u*k;y=.24*v*k;z=.265*(w*k+1)
 x*=1-.12*z/.53;x+=.023*math.sin(z*7)
 # Upper oblique fracture and broken left shoulder, deliberately large planes.
 z=min(z,.475-.22*x+.055*y,.575+.42*x-.05*y)
 x=max(x,-.365+.065*z+.07*y)
 # Differential resistance is concentrated in two broad, interrupted ledges.
 bed=z-.22*x-.05*y
 ledge=.028*math.exp(-((bed-.145)/.032)**2)*(.6+.4*math.cos(x*5+y*3))
 recess=.036*math.exp(-((bed-.285)/.070)**2)*math.exp(-((x+.08)/.28)**2)
 y+=math.copysign(ledge-recess,v) if abs(v)>.01 else 0
 # Larger chipped front-right shoulder and quiet undulating break surfaces.
 chip=.050*math.exp(-((x-.23)/.15)**2-((z-.37)/.11)**2)
 y+=chip*max(0,-v)
 x+=.009*math.sin(z*17+y*6)*math.exp(-((z-.20)/.18)**2)
 return (x,y,z)

def base(face,a,b):
 return [(1,a,b),(-1,a,b),(a,1,b),(a,-1,b),(a,b,1),(a,b,-1)][face]

def color(x,y,z):
 # Unequal crossbed sets, one dominant inclined set, faint overlying truncation.
 lower=.125+.06*x+.013*math.sin(y*9+x*4)
 upper=.365-.035*x+.009*math.sin(y*7)
 if z<lower:slope=.16;offset=.010;strength=.66
 elif z<upper:slope=.31;offset=.027;strength=1.0
 else:slope=-.07;offset=.004;strength=.46
 t=z-slope*x-.075*y+.004*math.sin(9*x+4*y)+.002*math.sin(13*y)
 phase=(t*94+1.35*math.sin(t*18)+.15*math.sin(x*14+y*5)+offset)*math.pi
 # Vary thickness and visibility continuously; no index/modulo stripe palette.
 narrow=math.exp(-(math.sin(phase)**2)/.055)
 broad=math.sin(phase*.39+1.1)*.7+math.sin(phase*.17-.6)*.3
 continuity=.35+.65*(.5+.5*math.sin(x*8+y*4+t*35))
 weather=.42+.58*(1-math.exp(-((x-.08)/.25)**2-((z-.27)/.13)**2))
 lamina=(-.070*narrow*continuity+.020*broad)*strength*weather
 mottle=.016*math.sin(11*x+5*y+7*z)+.010*math.sin(21*z-7*x+3*y)
 iron=.011*math.exp(-((z-.16-.12*x)/.055)**2)*(.5+.5*math.sin(x*9+y*6))
 return (.695+lamina+mottle+iron,.649+lamina+mottle*.9+iron*.35,.551+lamina*.9+mottle*.8-iron*.4)

def png_chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)

def bake():
 # Six original face fields packed into a padded 3x2 atlas. Texture pixels are
 # sRGB bytes, generated from authored positions, never from a photograph.
 raw=bytearray();pad=3
 for py in range(SIZE):
  raw.append(0)
  vv=1-(py+.5)/SIZE
  for px in range(SIZE):
   uu=(px+.5)/SIZE;cx=min(2,int(uu*3));cy=min(1,int(vv*2));face=cy*3+cx
   a=((uu-cx/3)*SIZE-pad)/(SIZE/3-2*pad)*2-1
   b=((vv-cy/2)*SIZE-pad)/(SIZE/2-2*pad)*2-1
   a=max(-1,min(1,a));b=max(-1,min(1,b));x,y,z=point(*base(face,a,b));c=color(x,y,z)
   # Deterministic fine grain, low contrast and at the available atlas texel scale.
   n=((px*73856093)^(py*19349663)^SEED)&0xffffffff;n=(n^(n>>13))*1274126177&0xffffffff
   grain=((n&65535)/65535-.5)*.026
   raw.extend(max(0,min(255,round((v+grain)*255))) for v in c)
 data=b'\x89PNG\r\n\x1a\n'+png_chunk(b'IHDR',struct.pack('>IIBBBBB',SIZE,SIZE,8,2,0,0,0))+png_chunk(b'IDAT',zlib.compress(bytes(raw),9))+png_chunk(b'IEND',b'')
 p=H/'sandstone-original-basecolor-512.png';p.write_bytes(data);return p

c=setup_scene(SLUG,SEED);tex=bake();mat=make_material('original-baked-sandstone','#FFFFFF',.91)
img=bpy.data.images.load(str(tex));img.colorspace_settings.name='sRGB';img.pack()
node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=img;node.interpolation='Linear';node.extension='EXTEND'
shader=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED');mat.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])
verts=[];faces=[];uvs=[];lookup={}
# 22x16x16 surface lattice: 3,840 export triangles, connected manifold shell.
for face in range(6):
 na,nb=[(16,16),(16,16),(22,16),(22,16),(22,16),(22,16)][face]
 ids={}
 for j in range(nb+1):
  b=-1+2*j/nb
  for i in range(na+1):
   a=-1+2*i/na;q=base(face,a,b);key=tuple(round(t,8) for t in q)
   if key not in lookup:lookup[key]=len(verts);verts.append(point(*q))
   ids[i,j]=lookup[key]
 for j in range(nb):
  for i in range(na):
   corners=[(i,j),(i+1,j),(i+1,j+1),(i,j+1)];faces.append(tuple(ids[q] for q in corners))
   col=face%3;row=face//3;pad=3
   uvs.append([((col/3*SIZE+pad+(ii/na)*(SIZE/3-2*pad))/SIZE,(row/2*SIZE+pad+(jj/nb)*(SIZE/2-2*pad))/SIZE) for ii,jj in corners])
o=mesh_object('single-continuous-weathered-sandstone-shell',verts,faces,mat,c,recalculate_normals=False)
# Correct face winding together with UV order, rather than losing UV association
# through a post-hoc topology edit.
# Rebuild winding before authoring loops; preserve texture orientation.
start=0
for face in range(6):
 na,nb=[(16,16),(16,16),(22,16),(22,16),(22,16),(22,16)][face];count=na*nb
 if face in [1,2,5]:
  for j in range(start,start+count):faces[j]=tuple(reversed(faces[j]));uvs[j]=list(reversed(uvs[j]))
 start+=count
# Replace only this newly-authored mesh with the correctly wound source.
old=o.data;m=bpy.data.meshes.new('editable-weathered-shell');m.from_pydata(verts,[],faces);m.update();o.data=m;bpy.data.meshes.remove(old);m.materials.append(mat)
uv=m.uv_layers.new(name='Original-512-atlas')
for p,coords in zip(m.polygons,uvs):
 # Keep the major fractured cap and left break explicit; flank erosion stays smooth.
 p.use_smooth=not (p.index>=1216 and p.index<1568 or 256<=p.index<512)
 for loop,q in zip(p.loop_indices,coords):uv.data[loop].uv=q
# Ground-center origin; same real-world meter convention as prior versions.
lo=min(v.co.z for v in m.vertices)
for v in m.vertices:v.co.z-=lo
export_asset(SLUG,{'en':'Cross-bedded sandstone textured experiment r002','zh':'交错层理砂岩纹理实验第二版'},'geology',c,output_root=H,render=False,max_triangles=14000,max_materials=2,max_primitives=2,metadata={'export_texcoords':True,'generator':'../build.py','purpose':'stylized natural-scene outcrop fragment, not a site-specific reconstruction','reference_pixel_status':'NPS Scotts Bluff reference actually viewed via authorized Drive inline on 2026-10-19','description':{'en':'Original continuous weathered shell; original baked fine crossbed color and grain. No reference photo pixels included.','zh':'原创连续风化石体，原创烘焙细层理与颗粒颜色；不含参考照片像素。'},'candidate_status':'experimental only; no production approval','texture_profile':'one original 512x512 RGB PNG base color; roughness constant 0.91; no normal map'})
(H/'build-parameters.json').write_text(json.dumps({'seed':SEED,'atlas':[512,512],'texture':'original analytic 3D field baked to padded UV atlas','material_count':1,'roughness':.91,'tri_budget_trial':[3000,6000],'hard_caps_retained':{'triangles':14000,'glb_bytes':1000000},'smooth_exterior':'mixed: fractured cap and left break flat, weathered flanks smooth; no individual lamina extrusion','geometry':'six connected surface patches, two broad resistance ledges, oblique fracture truncations'},indent=2))
