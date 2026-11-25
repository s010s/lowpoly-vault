import {test} from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync,spawnSync} from 'node:child_process';
import {mkdtemp,mkdir,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {
 MAX_GLB_BYTES,
 MAX_NONMETAL_METALLIC_FACTOR,
 TRUE_METAL_WHITELIST,
 inferAssetId,
 inspectGlbBuffer,
 checkGlbFile,
 checkGlbDirectory,
 checkGitChangedGlbs,
 checkReleaseGlbMaterials,
} from './glb-material-gate.mjs';

const CLI=fileURLToPath(new URL('./glb-material-gate.mjs',import.meta.url));

export function makeSyntheticGlb(materials,{binBytes=16,version='2.0',extraDoc={}}={}){
 const doc={asset:{version},...(materials===undefined?{}:{materials}),...extraDoc};
 let jsonBuf=Buffer.from(JSON.stringify(doc),'utf8');
 const jsonPad=(4-(jsonBuf.length%4))%4;
 if(jsonPad)jsonBuf=Buffer.concat([jsonBuf,Buffer.alloc(jsonPad,0x20)]);
 const binPad=(4-(binBytes%4))%4;
 const binBuf=Buffer.alloc(binBytes+binPad,0);
 const totalLength=12+8+jsonBuf.length+8+binBuf.length;
 const out=Buffer.alloc(totalLength);
 out.write('glTF',0,'ascii');
 out.writeUInt32LE(2,4);
 out.writeUInt32LE(totalLength,8);
 out.writeUInt32LE(jsonBuf.length,12);
 out.writeUInt32LE(0x4e4f534a,16);
 jsonBuf.copy(out,20);
 const binOffset=20+jsonBuf.length;
 out.writeUInt32LE(binBuf.length,binOffset);
 out.writeUInt32LE(0x004e4942,binOffset+4);
 binBuf.copy(out,binOffset+8);
 return out;
}

test('true-metal whitelist contains ONLY pyrite-cube-cluster and native-copper-dendrite',()=>{
 assert.deepEqual([...TRUE_METAL_WHITELIST].sort(),['native-copper-dendrite','pyrite-cube-cluster']);
 assert.equal(MAX_GLB_BYTES,5_000_000);
 assert.equal(MAX_NONMETAL_METALLIC_FACTOR,0.1);
});

test('rejects omitted metallicFactor without metallicRoughnessTexture',()=>{
 const omitted=makeSyntheticGlb([{name:'mat0',pbrMetallicRoughness:{baseColorFactor:[0.6,0.5,0.4,1],roughnessFactor:0.9}}]);
 const res=inspectGlbBuffer(omitted,{id:'scutellosaurus'});
 assert.equal(res.ok,false);
 assert.equal(res.violations[0].code,'omitted_metallic_factor');
 const noPbr=makeSyntheticGlb([{name:'mat1'}]);
 assert.equal(inspectGlbBuffer(noPbr,{id:'pachyornis'}).ok,false);
 const noMaterials=makeSyntheticGlb([]);
 assert.equal(inspectGlbBuffer(noMaterials,{id:'pachyornis'}).violations[0].code,'missing_materials');
});

test('rejects explicit metallicFactor > 0.1 without metallicRoughnessTexture',()=>{
 for(const mf of [0.1001,0.35,0.65,0.8,1.0]){
  const glb=makeSyntheticGlb([{name:'high',pbrMetallicRoughness:{metallicFactor:mf,roughnessFactor:0.9}}]);
  const res=inspectGlbBuffer(glb,{id:'conglomerate-outcrop'});
  assert.equal(res.ok,false,`expected reject for metallicFactor=${mf}`);
  assert.equal(res.violations[0].code,'high_metallic_factor');
 }
});

test('accepts metallicFactor <= 0.1 without metallicRoughnessTexture',()=>{
 for(const mf of [0,0.0,0.05,0.1]){
  const glb=makeSyntheticGlb([{name:'matte',pbrMetallicRoughness:{metallicFactor:mf,roughnessFactor:0.9}}]);
  const res=inspectGlbBuffer(glb,{id:'scutellosaurus'});
  assert.equal(res.ok,true,`expected accept for metallicFactor=${mf}`);
  assert.deepEqual(res.violations,[]);
 }
});

test('accepts omitted or high metallicFactor when metallicRoughnessTexture is present',()=>{
 const withTexOmitted=makeSyntheticGlb([{name:'pbr',pbrMetallicRoughness:{metallicRoughnessTexture:{index:0}}}]);
 assert.equal(inspectGlbBuffer(withTexOmitted,{id:'tyrannosaurus'}).ok,true);
 const withTexHigh=makeSyntheticGlb([{name:'pbr2',pbrMetallicRoughness:{metallicFactor:1.0,metallicRoughnessTexture:{index:1}}}]);
 assert.equal(inspectGlbBuffer(withTexHigh,{id:'tyrannosaurus'}).ok,true);
});

test('exempts ONLY pyrite-cube-cluster and native-copper-dendrite',()=>{
 const omitted=makeSyntheticGlb([{name:'metal',pbrMetallicRoughness:{roughnessFactor:0.35}}]);
 const high=makeSyntheticGlb([{name:'metal',pbrMetallicRoughness:{metallicFactor:0.95,roughnessFactor:0.35}}]);
 for(const allowed of ['pyrite-cube-cluster','native-copper-dendrite']){
  assert.equal(inspectGlbBuffer(omitted,{id:allowed}).ok,true);
  assert.equal(inspectGlbBuffer(omitted,{id:allowed}).exempt,true);
  assert.equal(inspectGlbBuffer(high,{id:allowed}).ok,true);
 }
 for(const denied of ['pyrite-cube-cluster-copy','native-copper-dendrite-lod','quartz-prism-cluster','obsidian-flow-face','gold-nugget',null]){
  assert.equal(inspectGlbBuffer(omitted,{id:denied}).ok,false);
  assert.equal(inspectGlbBuffer(high,{id:denied}).ok,false);
 }
});

test('enforces configurable byte size limit even for whitelisted true metals',()=>{
 const glb=makeSyntheticGlb([{name:'matte',pbrMetallicRoughness:{metallicFactor:0.0,roughnessFactor:0.9}}],{binBytes:2048});
 assert.equal(inspectGlbBuffer(glb,{id:'scutellosaurus',maxBytes:1024}).ok,false);
 assert.equal(inspectGlbBuffer(glb,{id:'scutellosaurus',maxBytes:1024}).violations[0].code,'size_exceeded');
 assert.equal(inspectGlbBuffer(glb,{id:'pyrite-cube-cluster',maxBytes:1024}).ok,false);
 assert.equal(inspectGlbBuffer(glb,{id:'scutellosaurus',maxBytes:4096}).ok,true);
 assert.equal(inspectGlbBuffer(glb,{id:'scutellosaurus',maxBytes:null}).ok,true);
});

test('rejects corrupt or non-GLB binaries',()=>{
 assert.equal(inspectGlbBuffer(Buffer.alloc(0),{id:'toy'}).violations[0].code,'empty_file');
 assert.equal(inspectGlbBuffer(Buffer.from('not a glb file at all!!'),{id:'toy'}).violations[0].code,'invalid_glb');
});

test('directory mode and path-based ID inference for whitelisted and non-whitelisted assets',async t=>{
 const root=await mkdtemp(join(tmpdir(),'material-gate-dir-'));
 t.after(()=>rm(root,{recursive:true,force:true}));
 await mkdir(join(root,'scutellosaurus'),{recursive:true});
 await mkdir(join(root,'pyrite-cube-cluster'),{recursive:true});
 await mkdir(join(root,'bad-animal'),{recursive:true});
 await writeFile(join(root,'scutellosaurus/model.glb'),makeSyntheticGlb([{pbrMetallicRoughness:{metallicFactor:0,roughnessFactor:0.9}}]));
 await writeFile(join(root,'pyrite-cube-cluster/model.glb'),makeSyntheticGlb([{pbrMetallicRoughness:{metallicFactor:0.95,roughnessFactor:0.3}}]));
 await writeFile(join(root,'bad-animal/model.glb'),makeSyntheticGlb([{pbrMetallicRoughness:{metallicFactor:0.65,roughnessFactor:0.9}}]));
 const report=await checkGlbDirectory(root);
 assert.equal(report.status,'FAIL');
 assert.equal(report.checked_count,3);
 assert.equal(report.passed_count,2);
 assert.equal(report.failed_count,1);
 assert.equal(report.failures[0].id,'bad-animal');
 const pyrite=await checkGlbFile(join(root,'pyrite-cube-cluster/model.glb'),{root});
 assert.equal(pyrite.ok,true);
 assert.equal(pyrite.id,'pyrite-cube-cluster');
 assert.equal(pyrite.exempt,true);
});

test('inferAssetId resolves parent asset slug across hashed stems and display/release revision folders',async t=>{
 const root=await mkdtemp(join(tmpdir(),'material-gate-hashed-'));
 t.after(()=>rm(root,{recursive:true,force:true}));
 const cases=[
  ['assets/additions/pyrite-cube-cluster/reviewed-release-20261114-08/model-abcdef012345.glb','pyrite-cube-cluster',true],
  ['assets/additions/native-copper-dendrite/reviewed-release-20261114-05/model-vad43637ae5e5.glb','native-copper-dendrite',true],
  ['assets/additions/echmatocrinus/reviewed-release-20261114-08/model-no-index-0395510b.glb','echmatocrinus',false],
  ['assets/additions/desiccation-crack-surface/display-reviewed-v1/model-716a4eb672bc.glb','desiccation-crack-surface',false],
  ['assets/additions/kalligramma/display-optimized-v1/model.glb','kalligramma',false],
 ];
 const metallicGlb=makeSyntheticGlb([{pbrMetallicRoughness:{metallicFactor:0.95,roughnessFactor:0.3}}]);
 for(const [rel,expectedId,shouldPass] of cases){
  const full=join(root,rel);
  await mkdir(join(full,'..'),{recursive:true});
  await writeFile(full,metallicGlb);
  assert.equal(await inferAssetId(full,{root}),expectedId,`inferAssetId failed for ${rel}`);
  const res=await checkGlbFile(full,{root});
  assert.equal(res.id,expectedId);
  assert.equal(res.exempt,shouldPass);
  assert.equal(res.ok,shouldPass);
 }
 const dirReport=await checkGlbDirectory(root);
 assert.equal(dirReport.checked_count,cases.length);
 assert.equal(dirReport.passed_count,2);
 assert.equal(dirReport.failed_count,3);
 assert.deepEqual(
  dirReport.failures.map(f=>f.id).sort(),
  ['desiccation-crack-surface','echmatocrinus','kalligramma']
 );
});

test('git-changed mode and incremental release gate handle legacy debt vs changed assets',async t=>{
 const root=await mkdtemp(join(tmpdir(),'material-gate-git-'));
 t.after(()=>rm(root,{recursive:true,force:true}));
 await mkdir(join(root,'assets/legacy'),{recursive:true});
 await mkdir(join(root,'assets/fixed'),{recursive:true});
 const badGlb=makeSyntheticGlb([{pbrMetallicRoughness:{roughnessFactor:0.9}}]);
 const goodGlb=makeSyntheticGlb([{pbrMetallicRoughness:{metallicFactor:0.0,roughnessFactor:0.9}}]);
 await writeFile(join(root,'assets/legacy/model.glb'),badGlb);
 const manifest={assets:[{id:'legacy',glb:'assets/legacy/model.glb',sha256:{glb:'a'.repeat(64)}}]};
 await writeFile(join(root,'assets/manifest.json'),JSON.stringify(manifest));
 const git=(...a)=>execFileSync('git',['-C',root,...a],{encoding:'utf8'});
 git('init','-q');
 git('add','.');
 git('-c','user.name=Test','-c','user.email=test@users.noreply.github.com','commit','-qm','baseline');
 const baselineCommit=git('rev-parse','HEAD').trim();

 // Clean repo: git-changed passes with 0 files, release gate skips unchanged legacy debt
 const cleanGit=await checkGitChangedGlbs({root});
 assert.equal(cleanGit.status,'PASS');
 assert.equal(cleanGit.checked_count,0);
 const cleanRelease=await checkReleaseGlbMaterials({root,baselineCommit,manifest});
 assert.equal(cleanRelease.status,'CHANGED_ASSETS_PASS');
 assert.equal(cleanRelease.changed_count,0);
 assert.equal(cleanRelease.unchanged_count,1);

 // Adding a bad new GLB fails both git-changed and release gate
 await writeFile(join(root,'assets/fixed/model.glb'),makeSyntheticGlb([{pbrMetallicRoughness:{metallicFactor:0.65}}]));
 manifest.assets.push({id:'fixed',glb:'assets/fixed/model.glb',sha256:{glb:'b'.repeat(64)}});
 await writeFile(join(root,'assets/manifest.json'),JSON.stringify(manifest));
 const badGit=await checkGitChangedGlbs({root});
 assert.equal(badGit.status,'FAIL');
 assert.equal(badGit.failed_count,1);
 await assert.rejects(checkReleaseGlbMaterials({root,baselineCommit,manifest}),e=>e.report?.status==='BLOCKED_CHANGED_ASSETS');

 // Fixing the new GLB passes both
 await writeFile(join(root,'assets/fixed/model.glb'),goodGlb);
 const goodGit=await checkGitChangedGlbs({root});
 assert.equal(goodGit.status,'PASS');
 assert.equal(goodGit.checked_count,1);
 const goodRelease=await checkReleaseGlbMaterials({root,baselineCommit,manifest});
 assert.equal(goodRelease.status,'CHANGED_ASSETS_PASS');
 assert.equal(goodRelease.changed_count,1);
});

test('CLI supports --files, --id, --max-bytes, --json and returns proper exit codes',async t=>{
 const root=await mkdtemp(join(tmpdir(),'material-gate-cli-'));
 t.after(()=>rm(root,{recursive:true,force:true}));
 const goodPath=join(root,'scutellosaurus.glb');
 const badPath=join(root,'broken.glb');
 await writeFile(goodPath,makeSyntheticGlb([{pbrMetallicRoughness:{metallicFactor:0,roughnessFactor:0.9}}]));
 await writeFile(badPath,makeSyntheticGlb([{pbrMetallicRoughness:{roughnessFactor:0.9}}]));
 const ok=spawnSync(process.execPath,[CLI,'--files',goodPath,'--json'],{encoding:'utf8'});
 assert.equal(ok.status,0,ok.stderr);
 assert.equal(JSON.parse(ok.stdout).status,'PASS');
 const fail=spawnSync(process.execPath,[CLI,'--files',badPath,'--json'],{encoding:'utf8'});
 assert.equal(fail.status,1);
 assert.equal(JSON.parse(fail.stdout).failures[0].violations[0].code,'omitted_metallic_factor');
 const exempt=spawnSync(process.execPath,[CLI,'--files',badPath,'--id','native-copper-dendrite','--json'],{encoding:'utf8'});
 assert.equal(exempt.status,0,exempt.stderr);
 assert.equal(JSON.parse(exempt.stdout).results[0].exempt,true);
 const tinyCap=spawnSync(process.execPath,[CLI,'--files',goodPath,'--max-bytes','10','--json'],{encoding:'utf8'});
 assert.equal(tinyCap.status,1);
 assert.equal(JSON.parse(tinyCap.stdout).failures[0].violations[0].code,'size_exceeded');
});
