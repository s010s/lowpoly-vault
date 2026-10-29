#!/usr/bin/env python3
"""Future-only static textured export and read-only report; never grants model acceptance."""
import argparse
import hashlib
import io
import math
import json
import struct
from pathlib import Path

PROFILE = 'lowpoly-lighttexture-v1'

def export_options(has_normal_map=False):
    return dict(export_format='GLB', use_selection=True, export_yup=True,
                export_apply=True, export_normals=True, export_texcoords=True,
                export_tangents=bool(has_normal_map), export_materials='EXPORT',
                export_vertex_color='NONE', export_animations=False, export_skins=False,
                export_morph=False, export_cameras=False, export_lights=False,
                export_extras=True, export_gpu_instances=False, export_gn_mesh=False,
                export_draco_mesh_compression_enable=False, export_use_gltfpack=False)

def export_glb(path, *, has_normal_map=False):
    import bpy
    path = Path(path)
    if path.exists():
        raise ValueError('Refuse to overwrite an existing candidate')
    options = export_options(has_normal_map)
    available = {p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
    missing = set(options) - available
    if missing:
        raise ValueError('Unsupported exporter flags: ' + ', '.join(sorted(missing)))
    bpy.ops.export_scene.gltf(filepath=str(path), **options)

def _index(items, value, label):
    if type(value) is not int or not 0 <= value < len(items):
        raise ValueError('Invalid ' + label + ' index')
    return items[value]

def report(path, require_texture=True):
    result = dict(profile=PROFILE, status='FAIL', errors=[], grants_acceptance=False,
                  grants_publication=False, visual_review='UNKNOWN', source_color_space='UNKNOWN')
    try:
        from PIL import Image
        raw = Path(path).read_bytes()
        result.update(glb_bytes=len(raw), glb_sha256=hashlib.sha256(raw).hexdigest())
        if len(raw)<20 or struct.unpack_from('<4sII',raw)!=(b'glTF',2,len(raw)):
            raise ValueError('Invalid GLB header')
        chunks=[]; pos=12
        while pos<len(raw):
            if pos+8>len(raw): raise ValueError('Truncated chunk header')
            size,kind=struct.unpack_from('<I4s',raw,pos);pos+=8
            if size%4 or pos+size>len(raw): raise ValueError('Invalid chunk bounds')
            chunks.append((kind,raw[pos:pos+size]));pos+=size
        if [c[0] for c in chunks] != [b'JSON',b'BIN\0']:
            raise ValueError('Expected JSON and embedded BIN chunks')
        doc=json.loads(chunks[0][1]); binary=chunks[1][1]
        if doc.get('extensionsUsed') or doc.get('extensionsRequired'):
            raise ValueError('Extensions outside this narrow profile; separate review required')
        if doc.get('skins') or doc.get('animations'):
            raise ValueError('Only static assets supported')
        buffers=doc.get('buffers',[])
        if len(buffers)!=1 or 'uri' in buffers[0] or buffers[0]['byteLength']>len(binary):
            raise ValueError('Expected one embedded buffer')
        images=[]
        for i,im in enumerate(doc.get('images',[])):
            if 'uri' in im or 'bufferView' not in im: raise ValueError('Images must be embedded')
            v=_index(doc['bufferViews'],im['bufferView'],'image bufferView'); start=v.get('byteOffset',0);size=v['byteLength']
            if type(v.get('buffer',0)) is not int or v.get('buffer',0)!=0 or start<0 or size<=0 or start+size>buffers[0]['byteLength']:
                raise ValueError('Image buffer bounds invalid')
            data=binary[start:start+size]
            with Image.open(io.BytesIO(data)) as image:
                image.load(); width,height=image.size;fmt=image.format
                if {'PNG':'image/png','JPEG':'image/jpeg'}.get(fmt)!=im.get('mimeType'):
                    raise ValueError('Unsupported image or MIME mismatch')
            images.append(dict(index=i,width=width,height=height,bytes=size,mime_type=im['mimeType'],sha256=hashlib.sha256(data).hexdigest()))
        slots=[]; used_images=set()
        for mi,mesh in enumerate(doc.get('meshes',[])):
            for pi,p in enumerate(mesh['primitives']):
                if p.get('mode',4)!=4 or p.get('targets'): raise ValueError('Only static triangles supported')
                if 'material' not in p: continue
                mat=_index(doc['materials'],p['material'],'material');pbr=mat.get('pbrMetallicRoughness',{})
                candidates=[('baseColor',pbr.get('baseColorTexture'),'sRGB'),('metallicRoughness',pbr.get('metallicRoughnessTexture'),'linear data; G roughness, B metallic'),('normal',mat.get('normalTexture'),'linear tangent-space +Y'),('occlusion',mat.get('occlusionTexture'),'linear data; R'),('emissive',mat.get('emissiveTexture'),'sRGB')]
                for name,info,space in candidates:
                    if info is None: continue
                    if info.get('extensions'): raise ValueError('Texture extensions unsupported')
                    tex=_index(doc['textures'],info['index'],'texture');idx=tex['source']
                    if type(idx) is not int or not 0<=idx<len(images): raise ValueError('Missing image source')
                    uv='TEXCOORD_'+str(info.get('texCoord',0))
                    if uv not in p['attributes']: raise ValueError('Texture has no corresponding '+uv)
                    accessor=_index(doc.get('accessors',[]),p['attributes'][uv],uv+' accessor')
                    position=_index(doc.get('accessors',[]),p['attributes'].get('POSITION'),'POSITION accessor')
                    count=accessor.get('count')
                    if type(count) is not int or count<=0 or count!=position.get('count') or position.get('type')!='VEC3':
                        raise ValueError('UV/POSITION count or type invalid')
                    component=accessor.get('componentType')
                    if accessor.get('type')!='VEC2' or component not in (5126,5121,5123) or (component!=5126 and accessor.get('normalized') is not True):
                        raise ValueError('Invalid UV accessor type')
                    if 'sparse' in accessor: raise ValueError('Sparse UV requires separate validation profile')
                    view=_index(doc.get('bufferViews',[]),accessor.get('bufferView'),'UV bufferView')
                    width={5126:4,5121:1,5123:2}[component]; element=2*width
                    offset=accessor.get('byteOffset',0);stride=view.get('byteStride',element)
                    start=view.get('byteOffset',0); length=view.get('byteLength')
                    if any(type(x) is not int for x in (offset,stride,start,length)) or offset<0 or start<0 or stride<element or stride%width or offset%width or type(view.get('buffer',0)) is not int or view.get('buffer',0)!=0 or offset+(count-1)*stride+element>length or start+length>buffers[0]['byteLength']:
                        raise ValueError('UV accessor data range invalid')
                    if component==5126:
                        for row in range(count):
                            if not all(math.isfinite(x) for x in struct.unpack_from('<2f',binary,start+offset+row*stride)):
                                raise ValueError('Nonfinite UV coordinate')
                    if 'TANGENT' in p['attributes']:
                        tangent=_index(doc.get('accessors',[]),p['attributes']['TANGENT'],'TANGENT accessor')
                        if tangent.get('type')!='VEC4' or tangent.get('componentType')!=5126 or tangent.get('count')!=count or 'sparse' in tangent:
                            raise ValueError('Invalid TANGENT accessor')
                        tv=_index(doc.get('bufferViews',[]),tangent.get('bufferView'),'TANGENT bufferView')
                        to=tangent.get('byteOffset',0);ts=tv.get('byteStride',16);tb=tv.get('byteOffset',0);tl=tv.get('byteLength')
                        if any(type(x) is not int for x in (to,ts,tb,tl)) or to<0 or tb<0 or ts<16 or ts%4 or to%4 or type(tv.get('buffer',0)) is not int or tv.get('buffer',0)!=0 or to+(count-1)*ts+16>tl or tb+tl>buffers[0]['byteLength']:
                            raise ValueError('TANGENT data range invalid')
                        for row in range(count):
                            if not all(math.isfinite(x) for x in struct.unpack_from('<4f',binary,tb+to+row*ts)):
                                raise ValueError('Nonfinite tangent')
                    used_images.add(idx);slots.append(dict(mesh=mi,primitive=pi,slot=name,image=idx,uv=uv,color_space_semantics=space,explicit_tangents='TANGENT' in p['attributes']))
        if require_texture and not slots: raise ValueError('Expected a material-referenced texture; none exported')
        if set(range(len(images)))-used_images: raise ValueError('Unreferenced embedded images')
        result.update(status='PASS',images=images,texture_slots=slots,
                      embedded_image_bytes=sum(x['bytes'] for x in images),
                      note='Narrow structural report only; official validation, source setup and visual review remain required')
    except (OSError,ValueError,KeyError,IndexError,TypeError,AttributeError,struct.error,ImportError) as exc:
        result['errors'].append(str(exc))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('glb');p.add_argument('--allow-untextured',action='store_true');a=p.parse_args()
    r=report(a.glb,not a.allow_untextured);print(json.dumps(r,indent=2));raise SystemExit(0 if r['status']=='PASS' else 1)
