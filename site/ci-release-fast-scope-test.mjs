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
function run(f){return classifyReleaseAppend({beforeEntries:entries(f.before),afterEntries:entries(f.after),readBefore:p=>f.before[p],readAfter:p=>f.after[p],readAfterBytes:p=>bytes(f.after[p])});}
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
