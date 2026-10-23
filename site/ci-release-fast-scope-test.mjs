import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {classifyReleaseAppend} from './ci-release-fast-scope.mjs';
import {assertFastArtifact,fastArtifactName} from './ci-release-fast-base.mjs';
const clone=structuredClone,read=p=>JSON.parse(readFileSync(p));
const manifest=read('assets/manifest.json'),catalog=read('site/catalog-data.json');
function fixture(){
 const before={'assets/manifest.json':clone(manifest),'site/catalog-data.json':clone(catalog),'production/production-releases-r002.json':{schema_version:1,kind:'production-release-set-v1',descriptors:[],asset_ids:[]},'site/shared.mjs':'protected code','assets/old-proof.json':'immutable evidence'};
 const after=clone(before),asset=clone(manifest.assets[0]);asset.id='fast-path-fixture';asset.packs=['fast-path-pack'];for(const k of ['glb','blend','preview'])asset[k]=`assets/additions/${asset.id}/r001/model.${k==='preview'?'png':k}`;
 after['assets/manifest.json'].assets.push(asset);after['site/catalog-data.json'].packs.push({id:'fast-path-pack',name:{en:'Fixture',zh:'测试'},description:{en:'Fixture only',zh:'仅测试'},asset_ids:[asset.id]});
 after['production/production-releases-r002.json'].descriptors.push({path:'production/fast-path-fixture/release.json',bytes:1,sha256:'a'.repeat(64)});after['production/production-releases-r002.json'].asset_ids.push(asset.id);
 after['production/fast-path-fixture/release.json']={assets:[{id:asset.id}]};for(const k of ['glb','blend','preview'])after[asset[k]]='fixture';after['production/fast-path-fixture/source.py']='# source data, not executed';
 return {before,after};
}
const bytes=x=>Buffer.from(typeof x==='string'?x:JSON.stringify(x)),entries=m=>Object.entries(m).map(([path,x])=>({path,type:'blob',mode:'100644',oid:createHash('sha1').update(bytes(x)).digest('hex')}));
function run(f){return classifyReleaseAppend({beforeEntries:entries(f.before),afterEntries:entries(f.after).map(e=>({...e,mode:f.modes?.[e.path]??e.mode})),readBefore:p=>f.before[p],readAfter:p=>f.after[p],readAfterBytes:p=>bytes(f.after[p])});}
assert.equal(run(fixture()).eligible,true,JSON.stringify(run(fixture())));let checks=1;
for(const edit of [
 f=>f.after['site/shared.mjs']='changed',f=>f.after['site/new.mjs']='new',f=>delete f.after['assets/old-proof.json'],f=>f.after['assets/old-proof.json']='changed',
 f=>f.after['assets/manifest.json'].assets.shift(),f=>f.after['assets/manifest.json'].assets[0].name='changed',f=>f.after['assets/manifest.json'].assets.push(f.after['assets/manifest.json'].assets.at(-1)),
 f=>f.after['assets/manifest.json'].publication.injected=true,f=>f.after['site/catalog-data.json'].packs[0].asset_ids.push('fast-path-fixture'),
 f=>f.after['production/production-releases-r002.json'].unknown=true,f=>f.after['production/production-releases-r002.json'].asset_ids.push('unknown'),
 f=>f.after['production/fast-path-fixture/run.mjs']='untrusted',f=>f.after['qa/new-evidence.json']={},f=>f.after['package-lock.json']='new',
]){const f=fixture();edit(f);assert.equal(run(f).eligible,false);checks++;}
const baseline={source_commit:'a'.repeat(40),run_id:3,run_attempt:1,repository_id:7},data=Buffer.from('artifact');
const meta={id:8,name:fastArtifactName(baseline.source_commit,3,1),expired:false,workflow_run:{id:3,head_sha:baseline.source_commit,repository_id:7,head_repository_id:7},digest:'sha256:'+createHash('sha256').update(data).digest('hex')};assertFastArtifact(meta,baseline,data);checks++;
for(const edit of [m=>m.expired=true,m=>m.workflow_run.head_sha='b'.repeat(40),m=>m.workflow_run.head_repository_id=8,m=>m.name='wrong',m=>m.digest='sha256:'+'0'.repeat(64)]){const m=clone(meta);edit(m);assert.throws(()=>assertFastArtifact(m,baseline,data));checks++;}
console.log(`Fast release: ${checks} positive/negative append and artifact-binding checks passed. No hosted baseline or GPU PASS claimed.`);

// The general classifier still rejects JavaScript; only exact new owned archives
// receive this outer proof. Full production acceptance remains a separate gate.
const dep='production/fast-path-fixture/fast-path-fixture/original/source/deps/check.mjs';
function helperFixture(){
 const f=fixture(),d='production/fast-path-fixture/release.json',prefix='production/fast-path-fixture/fast-path-fixture/';
 const pin=p=>({path:p,bytes:bytes(f.after[p]).length,sha256:createHash('sha256').update(bytes(f.after[p])).digest('hex')});
 f.after[dep]='// archived, not executed';
 f.after[prefix+'metadata.json']={id:'fast-path-fixture',production_release:d};
 f.after[prefix+'record.json']={asset_id:'fast-path-fixture',build_closure:[pin(dep)]};
 f.seal=()=>{f.after[d]={kind:'typed-production-release-v1',assets:[{id:'fast-path-fixture',metadata:pin(prefix+'metadata.json'),evidence:pin(prefix+'record.json')}]};f.after['production/production-releases-r002.json'].descriptors=[pin(d)];};f.seal();return f;
}
assert.equal(run(helperFixture()).eligible,true,JSON.stringify(run(helperFixture())));let helperChecks=1;
const record=f=>f.after['production/fast-path-fixture/fast-path-fixture/record.json'];
for(const edit of [
 f=>record(f).build_closure=[],
 f=>record(f).build_closure[0].sha256='0'.repeat(64),
 f=>record(f).build_closure[0].bytes++,
 f=>record(f).asset_id='another-asset',
 f=>{const p=dep.replace('/fast-path-fixture/original/','/other-asset/original/');f.after[p]=f.after[dep];delete f.after[dep];record(f).build_closure[0].path=p;},
 f=>{const p=dep.replace('original/source/deps/','original/');f.after[p]=f.after[dep];delete f.after[dep];record(f).build_closure[0].path=p;},
 f=>{f.before[dep]='old helper';},
 f=>{f.modes={[dep]:'100755'};},
 f=>{f.after[dep+'.unknown']='unknown';},
 f=>{f.before['production/fast-path-fixture/release.json']=f.after['production/fast-path-fixture/release.json'];},
 f=>{f.after['site/shared.mjs']='changed';},
 f=>{record(f).build_closure.push({...record(f).build_closure[0]});},
]){const f=helperFixture();edit(f);f.seal();const r=run(f);assert.equal(r.eligible,false,JSON.stringify(r));helperChecks++;}
console.log(`Owned archived helpers: ${helperChecks} positive/negative checks passed; ordinary Python source behavior preserved.`);

const actualLayout=helperFixture(),metadataPath='assets/additions/fast-path-fixture/r001/metadata.production.json';
actualLayout.after[metadataPath]=actualLayout.after['production/fast-path-fixture/fast-path-fixture/metadata.json'];
actualLayout.after['production/fast-path-fixture/release.json'].assets[0].metadata={path:metadataPath,bytes:bytes(actualLayout.after[metadataPath]).length,sha256:createHash('sha256').update(bytes(actualLayout.after[metadataPath])).digest('hex')};
const dpath='production/fast-path-fixture/release.json';
actualLayout.after['production/production-releases-r002.json'].descriptors=[{path:dpath,bytes:bytes(actualLayout.after[dpath]).length,sha256:createHash('sha256').update(bytes(actualLayout.after[dpath])).digest('hex')}];
assert.equal(run(actualLayout).eligible,true,JSON.stringify(run(actualLayout)));
const wrong=clone(actualLayout.after);wrong[dpath].assets[0].metadata.path='assets/additions/other-asset/r001/metadata.production.json';wrong[wrong[dpath].assets[0].metadata.path]=wrong[metadataPath];wrong['production/production-releases-r002.json'].descriptors=[{path:dpath,bytes:bytes(wrong[dpath]).length,sha256:createHash('sha256').update(bytes(wrong[dpath])).digest('hex')}];
assert.equal(run({before:actualLayout.before,after:wrong}).eligible,false);
console.log('Actual assets/additions metadata layout PASS; cross-asset metadata remains FULL.');
