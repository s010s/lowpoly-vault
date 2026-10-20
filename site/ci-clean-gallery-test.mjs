/** Source-bound pre-capture inputs and a collector-free artifact producer. */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,rmSync,symlinkSync} from 'node:fs';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {fixture,buildFixture} from './ci-model-proof-test.mjs';
import {assertPreCaptureInputs} from './ci-clean-gallery.mjs';
import {computeModelInputs,assertBuiltRenderInputs,MODEL_PROOF_ENTRYPOINTS,EXECUTED_QA_ENTRYPOINTS,PUBLICATION_ONLY_MODULES,modelExecutionDependencies} from './ci-model-proof.mjs';
const f=fixture(3);
try{
 await buildFixture(f);
 const result=await assertPreCaptureInputs({root:f.root});
 assert.deepEqual(result.catalog_ids,f.manifest.assets.map(asset=>asset.id));
 assert.throws(()=>computeModelInputs({root:f.root,built:result}),/independent in-process verification/);
 // Incomplete gallery is expected before capture, but never a complete proof.
 const last=f.manifest.assets.at(-1),resources=JSON.parse(readFileSync(join(f.root,'dist/gallery/resources.json')));
 for(const path of [resources.posters[last.id].detail,resources.posters[last.id].wheel])rmSync(join(f.root,'dist',path));
 delete resources.posters[last.id];resources.files=resources.files.filter(row=>!row.path.includes(last.id));
 f.put('dist/gallery/resources.json',resources);
 assert.equal((await assertPreCaptureInputs({root:f.root})).catalog_ids.length,3);
 await assert.rejects(()=>assertBuiltRenderInputs({root:f.root}),/poster coverage/);
 const manifestPath=join(f.root,'dist/assets/manifest.json'),manifestBytes=readFileSync(manifestPath),manifest=JSON.parse(manifestBytes);
 manifest.assets[0].dimensions=[99,99,99];writeFileSync(manifestPath,JSON.stringify(manifest,null,2)+'\n');
 await assert.rejects(()=>assertPreCaptureInputs({root:f.root}),/manifest differs/);writeFileSync(manifestPath,manifestBytes);
 const glbPath=join(f.root,'dist',last.glb),glb=readFileSync(glbPath);writeFileSync(glbPath,'changed model');
 await assert.rejects(()=>assertPreCaptureInputs({root:f.root}),/delivered glb differs/);writeFileSync(glbPath,glb);
 rmSync(glbPath);symlinkSync(join(f.root,last.glb),glbPath);
 await assert.rejects(()=>assertPreCaptureInputs({root:f.root}),/symlink/);
}finally{f.close();}
const workflow=readFileSync('site/../.github/workflows/full-release-review.yml','utf8');
const job=name=>{const start=workflow.indexOf(`  ${name}:\n`);assert(start>=0,`Missing job ${name}`);const end=workflow.slice(start+3).search(/^  [\w-]+:\n/m);return end<0?workflow.slice(start):workflow.slice(start,start+3+end);};
const source=job('prepare-source'),clean=job('prepare'),audit=job('audit-prepared-build'),aggregate=job('model-coverage');
assert(source.includes('npm run build')&&source.includes('raw-full-review-built-site'));
assert(clean.includes('needs: [scope, prepare-source]')&&clean.includes('npm ci --ignore-scripts'));
const commands=[...clean.matchAll(/\brun: (.+)/g)].map(match=>match[1]);
assert.deepEqual(commands,[
 'npm ci --ignore-scripts','node site/ci-clean-gallery.mjs','node site/ci-install-chromium.mjs',
 'npm run gallery:posters && node site/gallery-assets.mjs --dist --complete','node site/ci-incremental-models.mjs plan','node site/ci-model-shards.mjs seal-build'
]);
assert(!clean.includes('site/audit-release.mjs')&&!clean.includes('site/ci-publication.mjs'));
// Every executable Node contract before GPU/card proof production must remain a
// protected closure root, even if it is unchanged when a new archive is added.
for(const section of [clean,job('build'),aggregate])for(const match of section.matchAll(/(?:node |npx )(site\/[A-Za-z0-9_./-]+\.mjs)/g))assert(MODEL_PROOF_ENTRYPOINTS.includes(match[1]),`Untracked clean consumer root: ${match[1]}`);
assert(MODEL_PROOF_ENTRYPOINTS.includes('site/capture-gallery-posters.mjs')&&MODEL_PROOF_ENTRYPOINTS.includes('site/render-web-previews.mjs'));
// Check the real repository import graph as well as the small proof fixtures.
// Historical preparation scripts are still protected bytes, not executable
// roots merely because they share a directory with one active browser harness.
const inventory=execFileSync('git',['ls-files','-z'],{maxBuffer:128*1024*1024}).toString().split('\0').filter(Boolean);
const executionSources=['site/ci-review.mjs','package.json',...inventory.filter(path=>/^\.github\/workflows\/.*\.ya?ml$/.test(path))].map(path=>readFileSync(path,'utf8')).join('\n');
assert.deepEqual([...new Set([...executionSources.matchAll(/\bnode (qa\/[A-Za-z0-9_./-]+\.mjs)/g)].map(match=>match[1]))].sort(),[...EXECUTED_QA_ENTRYPOINTS].sort());
// These command definitions are themselves always hash-protected. A new or
// computed subprocess route changes policy and cannot inherit an old baseline.
const closure=modelExecutionDependencies(inventory,path=>readFileSync(path));
assert(!closure.has('qa/conifer-doc1-integration/prepare-review.mjs'),'Unused historical preparation must not be a render entrypoint');
assert.deepEqual(PUBLICATION_ONLY_MODULES.filter(path=>closure.has(path)),[],'Real proof consumers must not execute publication collectors');
assert(audit.includes('node site/ci-model-shards.mjs audit-build'));
const auditWrapper=readFileSync('site/ci-model-shards.mjs','utf8');
assert(auditWrapper.includes("['site/audit-release.mjs']")&&auditWrapper.includes("REQUIRE_COMPLETE_GALLERY: '1'"));
assert.equal((audit.match(/node site\/ci-model-shards.mjs verify-build/g)||[]).length,2);
assert(!audit.includes('upload-artifact'));
assert(aggregate.includes('needs: [scope, prepare, build, audit-prepared-build]')&&aggregate.includes('test "$AUDIT_RESULT" = success'));
console.log('Clean gallery contracts passed: exact manifest/model bytes, missing-poster boundary, symlink rejection, unforgeable final proof and isolated producer/audit sequencing.');
