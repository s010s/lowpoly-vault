"""Narrow profile unit tests with a valid textured triangle; not visual evidence."""
import copy
import io
import json
import struct
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from lighttexture_profile import report, export_options

class ProfileTests(unittest.TestCase):
    def fixture(self, mutate=lambda d: None, fmt='PNG'):
        im=Image.new('RGB',(4,4),(25,80,140));out=io.BytesIO();im.save(out,format=fmt);image=out.getvalue(); geometry=struct.pack('<9f6f',0,0,0,1,0,0,0,1,0,0,0,1,0,0,1); data=geometry+image
        doc={'asset':{'version':'2.0'},'buffers':[{'byteLength':len(data)}],
             'bufferViews':[{'buffer':0,'byteOffset':60,'byteLength':len(image)},{'buffer':0,'byteOffset':0,'byteLength':36,'target':34962},{'buffer':0,'byteOffset':36,'byteLength':24,'target':34962}],
             'accessors':[{'bufferView':1,'componentType':5126,'count':3,'type':'VEC3','min':[0,0,0],'max':[1,1,0]},{'bufferView':2,'componentType':5126,'count':3,'type':'VEC2'}],
             'scenes':[{'nodes':[0]}],'scene':0,'nodes':[{'mesh':0}],
             'images':[{'bufferView':0,'mimeType':'image/png' if fmt=='PNG' else 'image/jpeg'}],
             'textures':[{'source':0}], 'materials':[{'pbrMetallicRoughness':{'baseColorTexture':{'index':0}}}],
             'meshes':[{'primitives':[{'attributes':{'POSITION':0,'TEXCOORD_0':1},'material':0}]}]}
        mutate(doc);j=json.dumps(doc).encode();j+=b' '*(-len(j)%4);b=data+b'\0'*(-len(data)%4)
        raw=struct.pack('<4sII',b'glTF',2,28+len(j)+len(b))+struct.pack('<I4s',len(j),b'JSON')+j+struct.pack('<I4s',len(b),b'BIN\0')+b
        p=Path(self.tmp.name)/'fixture.glb';p.write_bytes(raw);return report(p)
    def setUp(self): self.tmp=tempfile.TemporaryDirectory()
    def tearDown(self): self.tmp.cleanup()
    def test_png(self): self.assertEqual(self.fixture()['status'],'PASS')
    def test_jpeg(self): self.assertEqual(self.fixture(fmt='JPEG')['status'],'PASS')
    def test_uv_missing(self): self.assertEqual(self.fixture(lambda d:d['meshes'][0]['primitives'][0]['attributes'].clear())['status'],'FAIL')
    def test_image_missing(self): self.assertEqual(self.fixture(lambda d:d['images'].clear())['status'],'FAIL')
    def test_external(self): self.assertEqual(self.fixture(lambda d:d['images'][0].update(uri='foo.png'))['status'],'FAIL')
    def test_unreferenced(self): self.assertEqual(self.fixture(lambda d:d['materials'][0].clear())['status'],'FAIL')
    def test_mime(self): self.assertEqual(self.fixture(lambda d:d['images'][0].update(mimeType='image/jpeg'))['status'],'FAIL')
    def test_range(self): self.assertEqual(self.fixture(lambda d:d['bufferViews'][0].update(byteLength=99999))['status'],'FAIL')
    def test_extension(self): self.assertEqual(self.fixture(lambda d:d.update(extensionsUsed=['KHR_texture_basisu']))['status'],'FAIL')
    def test_not_acceptance(self): self.assertFalse(self.fixture()['grants_acceptance']);self.assertEqual(self.fixture()['visual_review'],'UNKNOWN')
    def test_malformed_slot(self): self.assertEqual(self.fixture(lambda d:d['materials'][0]['pbrMetallicRoughness'].update(baseColorTexture=1))['status'],'FAIL')
    def test_uv_negative(self): self.assertEqual(self.fixture(lambda d:d['meshes'][0]['primitives'][0]['attributes'].update(TEXCOORD_0=-1))['status'],'FAIL')
    def test_uv_string(self): self.assertEqual(self.fixture(lambda d:d['meshes'][0]['primitives'][0]['attributes'].update(TEXCOORD_0='bad'))['status'],'FAIL')
    def test_tangent_bad_index(self): self.assertEqual(self.fixture(lambda d:d['meshes'][0]['primitives'][0]['attributes'].update(TANGENT=-1))['status'],'FAIL')
    def test_uv_bad_index(self): self.assertEqual(self.fixture(lambda d:d['meshes'][0]['primitives'][0]['attributes'].update(TEXCOORD_0=999999))['status'],'FAIL')
    def test_uv_bad_type(self): self.assertEqual(self.fixture(lambda d:d['accessors'][1].update(type='VEC3'))['status'],'FAIL')
    def test_uv_bad_count(self): self.assertEqual(self.fixture(lambda d:d['accessors'][1].update(count=9))['status'],'FAIL')
    def test_uv_bad_range(self): self.assertEqual(self.fixture(lambda d:d['accessors'][1].update(byteOffset=9999))['status'],'FAIL')
    def test_negative_index(self): self.assertEqual(self.fixture(lambda d:d['materials'][0]['pbrMetallicRoughness']['baseColorTexture'].update(index=-1))['status'],'FAIL')
    def test_export_uv(self): self.assertTrue(export_options()['export_texcoords']);self.assertTrue(export_options(True)['export_tangents'])

if __name__=='__main__':unittest.main()
