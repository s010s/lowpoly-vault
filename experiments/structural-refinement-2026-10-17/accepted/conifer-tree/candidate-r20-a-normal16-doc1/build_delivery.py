#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Rebuild the frozen A geometry then apply NORMAL16 delivery storage only.
Run in Blender, one bounded process. Keeps canonical float export as evidence.
"""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
P=Path(__file__).resolve().parent
REPO=next(x for x in P.parents if (x/'scripts/qa_glb.py').exists());sys.path.insert(0,str(REPO/'scripts'))
from qa_glb import audit_glb
spec=importlib.util.spec_from_file_location('frozen_A_geometry',P/'build_airy_conifer.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
spec=importlib.util.spec_from_file_location('normal16_storage',P/'pack_normal16.py');storage=importlib.util.module_from_spec(spec);spec.loader.exec_module(storage)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--config',type=Path,default=P/'build-config.json');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]);out=args.output_dir.resolve();config=json.loads(args.config.read_text())
 core.main()
 directory=out/'conifer-tree';canonical=out/'canonical-export';canonical.mkdir()
 (directory/'conifer-tree.glb').rename(canonical/'conifer-tree.glb')
 canonical_sha=H(canonical/'conifer-tree.glb')
 if canonical_sha!='e912444734c357017d3b839c0ba009dfc994d0e57acdb8d1d1a4fe431c0357c8':raise RuntimeError('Canonical geometry export differs from the r19 frozen GLB; stop before packaging')
 equivalence=storage.pack(canonical/'conifer-tree.glb',directory/'conifer-tree.glb',out/'normal16-equivalence.report.json')
 qa=json.loads((directory/'qa.json').read_text());qa['glb']=audit_glb(directory/'conifer-tree.glb',config['budgets']['max_triangles'],3,3);qa['delivery_storage']={'profile':'normalized SHORT normals at8-byte stride; FLOAT32 positions unchanged','extension':'KHR_mesh_quantization','external_decoder':'none','equivalence_report':'../normal16-equivalence.report.json'}
 if qa['glb']['errors']:raise RuntimeError(qa['glb']['errors'])
 (directory/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
 metadata=json.loads((directory/'metadata.json').read_text());metadata['generator']=str((P/'build_delivery.py').relative_to(REPO));metadata['generator_sha256']=H(P/'build_delivery.py');metadata['geometry_generator_sha256']=H(P/'build_airy_conifer.py');metadata['packing_generator_sha256']=H(P/'pack_normal16.py');metadata['glb_bytes']=qa['glb']['bytes'];metadata['sha256']['glb']=qa['glb']['sha256'];metadata['delivery_storage']=qa['delivery_storage'];metadata['canonical_float_glb_sha256']=canonical_sha
 (directory/'metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n')
 measured=json.loads((out/'build-measurements.json').read_text());(out/'build-measurements.json').rename(canonical/'build-measurements.json');measured.update(glb_bytes=qa['glb']['bytes'],glb_sha256=qa['glb']['sha256'],delivery_profile='normal16, no position edits',canonical_float_glb_sha256=canonical_sha,normal16_equivalence=equivalence)
 (out/'build-measurements.json').write_text(json.dumps(measured,indent=2)+'\n');(out/'build-config.json').write_text(json.dumps(config,indent=2)+'\n')
 print(json.dumps({'status':'built_pending_independent_acceptance','packed_glb_sha256':qa['glb']['sha256'],'packed_glb_bytes':qa['glb']['bytes'],'canonical_r19_glb_byte_identical':True},indent=2))
if __name__=='__main__':main()
