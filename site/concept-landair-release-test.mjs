if(process.argv.includes('--batches5155-only')){await testBatches5155();process.exit(0);}
if(process.argv.includes('--batches5657-only')){await testBatches5657();process.exit(0);}
if(process.argv.includes('--batches52-53-only')){await testBatches5253();process.exit(0);}
/** Bounded land/air quartet: exact revisions, immutable baseline and no formal promotion. */
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, writeFile, rm, rename, symlink } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { collectConceptLandairRelease, CONCEPT_LANDAIR_IDS, CONCEPT_LANDAIR_PACK } from './concept-landair-release.mjs';
import { CONCEPT_LANDAIR_RELEASE as fixed } from './accepted-concept-landair-release.mjs';
import { collectConceptQuartetsRelease } from './concept-quartets-release.mjs';

// Run exact new-scope tamper checks without repeating model rendering.
async function testBatches5155(){
 const {readdir,link,unlink}=await import('node:fs/promises');
 const {collectBatches5155Additions}=await import('./concept-landair-release.mjs');
 const {BATCHES5155_RELEASES:fixed}=await import('./accepted-concept-landair-release.mjs');
const source=process.cwd(),root=await mkdtemp(join(dirname(source),'batch5155-negative-'));let passed=0;
async function snapshot(dir,rel=''){for(const e of await readdir(dir,{withFileTypes:true})){if(['.git','node_modules','out'].includes(e.name))continue;const p=join(rel,e.name),s=join(source,p),d=join(root,p);if(e.isDirectory()){await mkdir(d,{recursive:true});await snapshot(s,p);}else if(e.isFile()){await mkdir(dirname(d),{recursive:true});await link(s,d);}}}await snapshot(source);
async function rejected(label,batch,path,change){const p=join(root,path);let old;try{old=await readFile(p);}catch(e){assert.equal(e.code,'ENOENT');}if(old)await unlink(p);await mkdir(dirname(p),{recursive:true});await writeFile(p,change(old));try{await assert.rejects(()=>collectBatches5155Additions(root,fixed.find(x=>x.release.scope.startsWith('batch'+batch+'-')).descriptor));passed++;console.log('PASS',label);}finally{await unlink(p);if(old)await writeFile(p,old);}}
try{
 for(const f of fixed){const result=await collectBatches5155Additions(root,f.descriptor);assert.equal(result.additions.length,4);passed++;const b=f.release.scope.startsWith('batch51')?51:55,a=f.release.additions[0];for(const [label,path]of [['descriptor',f.descriptor.path],['source bundle',f.release.source_bundle.path],['metadata',a.metadata.path],['candidate',a.candidate.path],['GLB',JSON.parse(await readFile(join(root,a.metadata.path))).glb],['poster',a.poster.path],['reference',a.capture_reference.path],['independent image review',f.release.capture.independent_review.path]])await rejected(`${b} rejects ${label} byte mutation`,b,path,old=>Buffer.concat([old,Buffer.from(' ')]));}
 const a=fixed[0].release.original_review_archive;await rejected('51 retains original QA alias',51,a.archive_path,old=>Buffer.concat([old,Buffer.from('changed')]));
 const d=JSON.parse(await readFile(join(root,fixed[1].release.historical_evidence_disclosure.path)));await rejected('55 rejects fabricated historical log',55,d.declarations[0].historical_checksum_audit.missing_entries[0].path,()=>Buffer.from('fabricated'));
 console.log(JSON.stringify({status:'PASS',checks:passed,formal_acceptance:'BLOCKED',gallery_output:'NOT_RUN',publication_ci:'NOT_RUN'}));
}finally{await rm(root,{recursive:true,force:true});}

}

if(!process.argv.includes('--batch54-only')&&!process.argv.includes('--batches58-61-only')) {
const BASE_COUNT = 186;
const revisions = { sapeornis: 'r001', longirostravis: 'r001', dunbaria: 'r001', chimerarachne: 'r001' };
const expectedIds = Object.keys(revisions).sort();
const descriptorPath = 'assets/releases/concept-landair-20261019.json';
const root = await mkdtemp(join(tmpdir(), 'vault-concept-landair-'));
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const pin = async path => ({ path, sha256: sha(await readFile(resolve(root, path))) });
const json = async path => JSON.parse(await readFile(resolve(root, path), 'utf8'));
let checks = 0;

async function mutate(path, change, action) {
  const full = resolve(root, path), bytes = await readFile(full);
  try {
    const value = JSON.parse(bytes);
    change(value);
    await writeFile(full, JSON.stringify(value));
    await action();
    checks++;
  } finally {
    await writeFile(full, bytes);
  }
}

async function tamper(path, action) {
  const full = resolve(root, path), bytes = await readFile(full);
  try {
    await writeFile(full, Buffer.concat([bytes, Buffer.from('\ntamper')]));
    await action();
    checks++;
  } finally {
    await writeFile(full, bytes);
  }
}

function validateCandidate(path, requireApproved = false) {
  const run = spawnSync('python3', [
    'scripts/validate_candidate.py', path, '--root', root, '--json',
    ...(requireApproved ? ['--require-approved'] : []),
  ], { cwd: root, encoding: 'utf8', timeout: 30000, maxBuffer: 2 * 1024 * 1024 });
  assert.ifError(run.error);
  assert([0, 1].includes(run.status), run.stderr);
  return { exitCode: run.status, report: JSON.parse(run.stdout) };
}

try {
  // Mutations are confined to an isolated copy; reviewed files in the checkout stay untouched.
  for (const path of ['assets', 'production', 'qa', 'scripts', 'experiments', 'package-lock.json']) {
    execFileSync('cp', ['-a', '--reflink=auto', path, resolve(root, path)]);
  }
  await mkdir(resolve(root, 'site'));
  await writeFile(resolve(root, 'site/viewer.js'), await readFile('site/viewer.js'));
  const collect = async () => collectConceptLandairRelease(root, await pin(descriptorPath));
  assert.deepEqual(CONCEPT_LANDAIR_IDS, expectedIds, 'Only the four independently reviewed land/air IDs are authorized');
  assert.deepEqual(fixed.additions.map(entry => entry.id).sort(), expectedIds);
  for (const entry of fixed.additions) {
    assert.equal(entry.revision, revisions[entry.id], `${entry.id}: exact reviewed revision`);
    assert.equal(entry.source_commit, 'e874e99d20b3b98c73cddb8496bcd7e89be4e28c');
    assert.equal(entry.review_commit, '3d024e53c36863d1887abd726998fa0f0d7b3831');
    assert.equal(entry.original_review_freeze, '68483aa3b8eed2d86f9e59a930128d99579b0838');
    assert.equal(entry.delivery_review_commit, 'b0426b7e3a696b30fea4de9e8b46c3772bab3f23');
    const sourceRoot = `production/concept-small-land-air-20261019/${entry.id}/r001`;
    assert.equal(entry.source_metadata.path, `${sourceRoot}/output/${entry.id}/metadata.json`);
    for (const key of ['glb', 'blend']) assert.equal(entry.artifacts[key].path, `${sourceRoot}/output/${entry.id}/${entry.id}.${key}`);
    assert.equal(entry.candidate.path, `${sourceRoot}/candidate.json`);
  }
  checks++;

  const baseline = await collectConceptQuartetsRelease(root, fixed.base_descriptor);
  const manifest = await collect();
  const before = await json('assets/manifest.json');
  assert.equal(baseline.assets.length, BASE_COUNT);
  assert.equal(manifest.assets.length, BASE_COUNT + CONCEPT_LANDAIR_IDS.length);
  assert.deepEqual(manifest.assets.slice(0, BASE_COUNT), baseline.assets, 'Every field of the existing 186 assets is preserved');
  assert.deepEqual(manifest.assets.slice(0, BASE_COUNT), before.assets.slice(0, BASE_COUNT), 'The existing published manifest is unchanged');
  assert.deepEqual(manifest.assets.slice(BASE_COUNT).map(asset => asset.id).sort(), expectedIds);
  assert.equal(new Set(manifest.assets.map(asset => asset.id)).size, manifest.assets.length);
  assert.deepEqual(manifest.publication.approved_concept_landair_ids, expectedIds);
  const { concept_landair_descriptor, approved_concept_landair_ids, ...previousPublication } = manifest.publication;
  assert.deepEqual(previousPublication, baseline.publication, 'Earlier publication provenance is preserved');
  assert.deepEqual(concept_landair_descriptor, await pin(descriptorPath));
  for (const id of fixed.excluded_ids) assert(!manifest.assets.some(asset => asset.id === id), `${id} remains excluded`);
  assert(!manifest.assets.some(asset => asset.id === 'ctenoimbricata'));
  for (const asset of baseline.assets) {
    for (const key of ['glb', 'blend', 'preview']) {
      const original = await readFile(asset[key]);
      assert.deepEqual(await readFile(resolve(root, asset[key])), original, `${asset.id}: pre-existing ${key} bytes are preserved`);
      assert.equal(sha(original), asset.sha256[key], `${asset.id}: baseline ${key} keeps its accepted digest`);
    }
  }
  checks++;

  for (const asset of manifest.assets.slice(BASE_COUNT)) {
    const entry = fixed.additions.find(item => item.id === asset.id);
    const source = await json(entry.source_metadata.path);
    assert.equal(asset.quality_status, 'independent_qa_accepted_stylized_prop');
    assert.deepEqual(asset.packs, [CONCEPT_LANDAIR_PACK]);
    assert.deepEqual(asset.sha256, entry.sha256);
    for (const key of ['triangles', 'dimensions', 'axes', 'bounds_glb_m', 'blender_dimensions_m', 'export_options', 'materials', 'generator']) {
      assert.deepEqual(asset[key], source[key], `${asset.id}: measured ${key} is unchanged`);
    }
    assert.deepEqual(asset.sources, (await json(entry.artifacts.references.path)).sources);
    assert(asset.sources.length > 0);
    for (const key of ['name', 'description', 'scientific_scope']) {
      for (const lang of ['en', 'zh']) assert(asset[key]?.[lang]?.trim(), `${asset.id}: ${key}.${lang}`);
    }
    const provenance = asset.approval_provenance;
    assert.equal(provenance.source_commit, entry.source_commit);
    assert.equal(provenance.review_commit, entry.review_commit);
    assert.equal(provenance.review_sha256, entry.review.sha256);
    assert.equal(provenance.delivery_review_commit, entry.delivery_review_commit);
    assert.equal(provenance.delivery_review_sha256, entry.delivery_review.sha256);
    assert.equal(provenance.candidate_record_approved_for_brief, false);
    assert.equal(provenance.formal_profile_acceptance, 'BLOCKED');
    assert.equal(provenance.hardware_gpu_verified, false);
    assert.equal(provenance.target_scene_verified, false);
    assert(!Object.hasOwn(provenance, 'validation_profile'));
    for (const key of ['candidate_record', 'validation_profile', 'profile', 'approved_for_brief', 'approval', 'qa', 'publication_status', 'downloads']) {
      assert(!Object.hasOwn(asset, key), `${asset.id}: candidate-only ${key} cannot collide with published metadata`);
    }
    const candidate = await json(entry.candidate.path);
    assert.equal(candidate.asset_id, entry.id);
    assert.equal(candidate.revision, revisions[entry.id]);
    assert.equal(candidate.approval.status, 'pending');
    for (const stage of Object.values(candidate.stages)) {
      assert.equal(stage.status, 'unknown', 'A bounded gallery release cannot silently approve a formal QA stage');
    }
    const { exitCode, report } = validateCandidate(entry.candidate.path, true);
    assert.equal(exitCode, 1, 'Limited website publication cannot satisfy the formal approval CLI gate');
    assert.equal(report.valid, true);
    assert.equal(report.approved_for_brief, false);
    assert.equal(report.validation_profile, 'legacy-v1');
    assert(report.approval_blockers.length > 0);
    for (const stage of ['factual', 'gpu', 'runtime_parse', 'scene', 'specification', 'technical', 'visual']) {
      assert(report.approval_blockers.includes(`${stage}: unknown`), `${stage}: formal stage stays unknown`);
    }
    assert.equal(report.measurements.materials, source.material_count, 'Actual exported material count is preserved separately from authored palette inventory');
    assert(source.materials.length >= source.material_count);
    const ordinary = validateCandidate(entry.candidate.path);
    assert.equal(ordinary.exitCode, 0);
    assert.deepEqual(ordinary.report, report);
    assert.deepEqual(report, await json(entry.candidate_validation.path));
    checks++;
  }

  // Even recomputing the outer descriptor hash must not authorize a different release.
  const descriptorChanges = [
    ['missing addition', value => value.additions.pop()],
    ['duplicate addition', value => value.additions.push(value.additions[0])],
    ['unreviewed ID', value => { value.additions[0].id = 'ctenoimbricata'; }],
    ['old revision', value => { value.additions[0].revision = 'r002'; }],
    ['missing authorization', value => { value.authorization = 'pending'; }],
    ['formal acceptance claim', value => { value.formal_profile_acceptance = 'PASS'; }],
    ['hardware acceptance claim', value => { value.hardware_gpu_verified = true; }],
    ['target scene acceptance claim', value => { value.target_scene_verified = true; }],
    ['different acceptance scope', value => { value.acceptance_scope = 'approved_for_brief'; }],
    ['source commit substitution', value => { value.additions[0].source_commit = '0'.repeat(40); }],
    ['delivery review commit substitution', value => { value.additions[0].delivery_review_commit = '0'.repeat(40); }],
    ['delivery review substitution', value => { value.additions[0].delivery_review.sha256 = '0'.repeat(64); }],
    ['review commit substitution', value => { value.additions[0].review_commit = '0'.repeat(40); }],
    ['review freeze substitution', value => { value.additions[0].original_review_freeze = '0'.repeat(40); }],
    ['added formal profile', value => { value.validation_profile = 'production-v1'; }],
    ['removed exclusions', value => { value.excluded_ids = []; }],
    ['source bundle substitution', value => { value.source_bundle.sha256 = '0'.repeat(64); }],
    ['unbound publication policy', value => { value.publication_policy.sha256 = '0'.repeat(64); }],
    ['base descriptor traversal', value => { value.base_descriptor.path = '../escape'; }],
    ['base descriptor substitution', value => { value.base_descriptor.sha256 = '0'.repeat(64); }],
    ['candidate validation promotion', value => { value.additions[0].approved_for_brief = true; }],
  ];
  for (const [label, change] of descriptorChanges) {
    await mutate(descriptorPath, change, () => assert.rejects(collect, /Only.*authorized/, label));
  }
  const originalDescriptor = await pin(descriptorPath);
  await assert.rejects(() => collectConceptLandairRelease(root, { ...originalDescriptor, sha256: '0'.repeat(64) }), /hash mismatch/);
  await assert.rejects(() => collectConceptLandairRelease(root, { ...originalDescriptor, path: '../escape' }));
  checks += 2;

  const entry = fixed.additions[0];
  for (const change of [
    value => { value.description.en = 'Exact scientific reconstruction'; },
    value => { value.scientific_scope.en = 'Formally approved for the target museum scene on physical hardware'; },
    value => { value.sources = []; },
    value => { value.sha256.glb = '0'.repeat(64); },
    value => { value.approval_provenance = { approved_for_brief: true }; },
    value => { value.quality_status = 'approved_for_brief'; },
    value => { value.packs = ['other']; },
    value => { value.dimensions = [1, 1, 1]; },
    value => { value.downloads = { glb: 'https://example.invalid/unreviewed.glb' }; },
    ...['validation_profile', 'profile', 'approved_for_brief', 'approval', 'candidate_record', 'qa', 'publication_status', 'turntable', 'card_preview', 'formal_profile_acceptance', 'hardware_gpu_verified', 'target_scene_verified'].map(key => value => { value[key] = key.endsWith('_verified') || key === 'approved_for_brief' ? true : 'forged-approval'; }),
  ]) {
    await mutate(entry.metadata.path, change, async () => {
      await assert.rejects(collect, /hash mismatch/, 'Changed metadata is rejected by its existing pin');
      const metadata = await pin(entry.metadata.path);
      await mutate(descriptorPath, value => { value.additions[0].metadata = metadata; }, () => assert.rejects(collect, /Only.*authorized/, 'Re-pinning metadata cannot expand frozen claims'));
    });
  }

  // A coordinated image/index rewrite must not reauthorize a different card image,
  // even when its new byte length and digest form a self-consistent public seal.
  const publicIndexPath = 'assets/turntables/index.json';
  const publicCards = (await json(publicIndexPath)).posters.filter(row => expectedIds.includes(row.id));
  assert.equal(publicCards.length, expectedIds.length);
  for (const [index, card] of publicCards.entries()) {
    const file = resolve(root, card.path), original = await readFile(file);
    const replacement = await readFile(resolve(root, publicCards[(index + 1) % publicCards.length].path));
    assert.notEqual(sha(replacement), card.sha256);
    try {
      await writeFile(file, replacement);
      await mutate(publicIndexPath, value => {
        const row = value.posters.find(row => row.id === card.id);
        row.sha256 = sha(replacement);
        row.bytes = replacement.length;
      }, () => assert.rejects(collect, /Public card must match/, `${card.id}: coordinated card/index substitution is rejected`));
    } finally {
      await writeFile(file, original);
    }
    await mutate(publicIndexPath, value => { value.posters.push(value.posters.find(row => row.id === card.id)); },
      () => assert.rejects(collect, /Public card must match/, `${card.id}: duplicate public card rows are rejected`));
    await mutate(publicIndexPath, value => { value.posters = value.posters.filter(row => row.id !== card.id); },
      () => assert.rejects(collect, /Public card must match/, `${card.id}: missing public card rows are rejected`));
  }

  // Exercise every quartet's public artifacts and the evidence used to support publication.
  const evidencePaths = new Set([fixed.source_bundle.path, fixed.publication_policy.path, fixed.base_descriptor.path, fixed.integration_audit.path, ...publicCards.map(card => card.path)]);
  for (const addition of fixed.additions) {
    const asset = manifest.assets.find(item => item.id === addition.id);
    for (const key of ['glb', 'blend', 'preview']) evidencePaths.add(asset[key]);
    for (const key of ['review', 'delivery_review', 'source_metadata', 'candidate', 'candidate_validation', 'proof', 'runtime']) evidencePaths.add(addition[key].path);
    for (const item of Object.values(addition.artifacts)) evidencePaths.add(item.path);
    for (const item of Object.values(addition.technical)) evidencePaths.add(item.path);
    for (const item of Object.values(addition.capture)) evidencePaths.add(item.path);
    const proof = await json(addition.proof.path);
    assert.equal(proof.frames.length, 11);
    const expectedProofDirectory = addition.id === 'chimerarachne' ? 'proof-macro-attempt02' : 'proof';
    assert.equal(addition.proof.path, `production/concept-small-land-air-20261019/${addition.id}/r001/${expectedProofDirectory}/render-manifest.json`);
    for (const frame of proof.frames) evidencePaths.add(`${dirname(addition.proof.path)}/${frame.path}`);
  }
  for (const path of evidencePaths) await tamper(path, () => assert.rejects(collect, /hash mismatch/, `${path}: tampering must fail closed`));

  await tamper('site/viewer.js', () => assert.rejects(collect, 'A changed viewer cannot retain the frozen capture attestation'));

  for (const addition of fixed.additions) {
    await mutate(addition.candidate.path, value => { value.approval.status = 'approved_for_brief'; }, async () => {
      const { exitCode, report } = validateCandidate(addition.candidate.path, true);
      assert.equal(exitCode, 1);
      assert.equal(report.valid, false);
      assert.equal(report.approved_for_brief, false, 'Forged candidate approval is never promoted');
      assert(report.errors.length > 0);
      await assert.rejects(collect, /hash mismatch/);
      const candidate = await pin(addition.candidate.path);
      await mutate(descriptorPath, value => { value.additions.find(item => item.id === addition.id).candidate = candidate; }, () => assert.rejects(collect, /Only.*authorized/));
    });
  }

  for (const path of [manifest.assets[BASE_COUNT].glb, publicCards[0].path, publicIndexPath]) {
    const artifact = resolve(root, path), saved = `${artifact}.saved`;
    await rename(artifact, saved);
    try {
      await symlink(saved, artifact);
      await assert.rejects(collect, /symlinks forbidden/i, `${path}: byte-identical symlink substitution is rejected`);
      checks++;
    } finally {
      await rm(artifact, { force: true });
      await rename(saved, artifact);
    }
  }
  assert.deepEqual(await collect(), manifest, 'Every destructive test restores the exact valid release');
  checks++;
  console.log(`Concept-landair release: ${checks} checks passed; exact reviewed quartet, unchanged ${BASE_COUNT}, frozen source/QA bindings, and blocked formal/hardware/scene gates preserved.`);
} finally {
  await rm(root, { recursive: true, force: true });
}

}

// Selected-scope checks are independently runnable without repeating old model QA.
if(!process.argv.includes('--batches58-61-only')){
 const {collectBatch54Additions}=await import('./concept-landair-release.mjs');
 const {BATCH54_RELEASE:accepted}=await import('./accepted-concept-landair-release.mjs');
 const {copyFile}=await import('node:fs/promises');
 const sandbox=await mkdtemp(join(tmpdir(),'vault-batch54-'));
 const digest=b=>createHash('sha256').update(b).digest('hex');
 const descriptorPath='assets/releases/batch54-20261020.json';
 const descriptor={path:descriptorPath,sha256:digest(await readFile(descriptorPath))};
 const bundle=JSON.parse(await readFile(accepted.source_bundle.path));
 const index=JSON.parse(await readFile(accepted.capture.index.path));
 const paths=new Set([descriptorPath,accepted.source_bundle.path,accepted.publication_policy.path,'site/viewer.js','assets/turntables/index.json','production/continuous-small-life-round19-20261020/batch-54-QA-SCOPE.json',...bundle.files.map(p=>p.path)]);
 for(const entry of accepted.additions){paths.add(entry.metadata.path);const a=JSON.parse(await readFile(entry.metadata.path));for(const kind of ['glb','blend','preview'])paths.add(a[kind]);paths.add(index.posters.find(p=>p.id===a.id).path);}
 let cases=0;
 try{
  for(const path of paths){await mkdir(dirname(resolve(sandbox,path)),{recursive:true});await copyFile(path,resolve(sandbox,path));}
  const collect=()=>collectBatch54Additions(sandbox,descriptor);const initial=await collect();assert.equal(initial.additions.length,4);cases++;
  for(const a of initial.additions){assert.equal(a.approval_provenance.formal_profile_acceptance,'BLOCKED');assert.equal(a.approval_provenance.hardware_gpu_verified,false);assert.equal(a.approval_provenance.target_scene_verified,false);assert.equal(a.approval_provenance.candidate_record_approved_for_brief,false);}
  const tamper=async(path,modify)=>{const file=resolve(sandbox,path),old=await readFile(file);try{await writeFile(file,modify(old));await assert.rejects(collect,/hash mismatch|Only exact|symlinks forbidden/);cases++;}finally{await writeFile(file,old);}};
  const append=b=>Buffer.concat([b,Buffer.from('tamper')]);
  for(const entry of accepted.additions){const a=JSON.parse(await readFile(entry.metadata.path));for(const path of [entry.candidate.path,entry.metadata.path,a.glb,a.blend,a.preview])await tamper(path,append);}
  for(const path of [accepted.review.path,accepted.dispatch_binding.path,accepted.capture.report.path,accepted.capture.index.path,accepted.source_bundle.path])await tamper(path,append);
  for(const field of ['formal_profile_acceptance','hardware_gpu_verified','target_scene_verified'])await tamper(descriptorPath,b=>{const d=JSON.parse(b);d[field]=field==='formal_profile_acceptance'?'PASS':true;return JSON.stringify(d);});
  const a=initial.additions[0],file=resolve(sandbox,a.glb),saved=file+'.saved';await rename(file,saved);try{await symlink(saved,file);await assert.rejects(collect,/symlinks forbidden/);cases++;}finally{await rm(file);await rename(saved,file);}
  assert.deepEqual(await collect(),initial);cases++;
  console.log(`Batch54 bounded release: ${cases} checks passed; exact four candidates, immutable source/QA/capture pins, tamper/symlink rejection, no formal approval promotion.`);
 }finally{await rm(sandbox,{recursive:true,force:true});}
}

async function testBatches5253(){
const {readFile,writeFile,mkdir,copyFile,mkdtemp,rm}=await import('node:fs/promises');const {tmpdir}=await import('node:os');const {resolve,dirname,join}=await import('node:path');const {default:assert}=await import('node:assert/strict');const {collectBatches5253Additions}=await import('./concept-landair-release.mjs');const {ACCEPTED_BOUNDED_BATCHES}=await import('./accepted-bounded-batches.mjs');
const root=process.cwd(),sandbox=await mkdtemp(join(tmpdir(),'batch5253-bounded-')),paths=new Set(['site/viewer.js','assets/turntables/index.json']),descriptors=[];
for(const entry of ACCEPTED_BOUNDED_BATCHES.filter(e=>['assets/releases/batch52-original-three-20261020.json','assets/releases/batch52-aturia-repair-20261020.json','assets/releases/batch53-20261020.json'].includes(e.descriptor.path))){const d=JSON.parse(await readFile(entry.descriptor.path));descriptors.push([entry.descriptor,d]);for(const p of [entry.descriptor,d.source_bundle,d.publication_policy,...d.files,...d.additions.flatMap(x=>[x.metadata,x.source_metadata,x.candidate,x.review,x.capture_reference])])paths.add(p.path);for(const a of d.additions){const m=JSON.parse(await readFile(a.metadata.path));for(const k of ['glb','blend','preview'])paths.add(m[k]);}const index=JSON.parse(await readFile(d.capture.index.path));for(const a of d.additions)paths.add(index.posters.find(p=>p.id===a.id).path);}
for(const p of paths){await mkdir(dirname(resolve(sandbox,p)),{recursive:true});await copyFile(resolve(root,p),resolve(sandbox,p));}
let cases=0;const records=[];
try{for(const [pin,d] of descriptors){await collectBatches5253Additions(sandbox,pin);cases++;const targets=[pin.path,d.source_bundle.path,d.review.path,d.capture.independent_review.path,d.capture.report.path,...d.additions.flatMap(a=>[a.metadata.path,a.candidate.path,a.capture_reference.path])];for(const p of [...new Set(targets)]){const path=resolve(sandbox,p),before=await readFile(path);try{await writeFile(path,Buffer.concat([before,Buffer.from(' ')]));await assert.rejects(()=>collectBatches5253Additions(sandbox,pin));cases++;records.push({scope:d.scope,path:p,result:'rejected_tamper'});}finally{await writeFile(path,before);}}await collectBatches5253Additions(sandbox,pin);cases++;}
 await mkdir(resolve(root,'out'),{recursive:true});await writeFile(resolve(root,'out/bounded-collector-tests.json'),JSON.stringify({status:'pass',cases,scopes:descriptors.map(x=>x[1].scope),tests:records,claim:'Local bounded addition collectors only; not full publication CI or actual incremental reuse'},null,2)+'\n');console.log('PASS',cases,'bounded collector cases; original source untouched');}
finally{await rm(sandbox,{recursive:true,force:true});}

}
if(!process.argv.includes('--batch54-only')&&!process.argv.includes('--batches58-61-only')) await testBatches5253();

/** Negative tests mutate only private copies, never the accepted source inputs. */
async function testBatches5657(){
 const {copyFile}=await import('node:fs/promises');
 const {collectBatches5657Additions}=await import('./concept-landair-release.mjs');
 const cwd=process.cwd(),manifest=JSON.parse(await readFile(resolve(cwd,'assets/manifest.json'))),descriptors=manifest.publication.batches56_57_descriptors;
 const sandbox=await mkdtemp(join(tmpdir(),'batch5657-bounded-')),paths=new Set(['site/viewer.js','assets/turntables/index.json']);
 function pins(value){if(!value||typeof value!=='object')return;if(typeof value.path==='string'&&typeof value.sha256==='string')paths.add(value.path);for(const v of Object.values(value))pins(v);}
 for(const descriptor of descriptors){pins(descriptor);const release=JSON.parse(await readFile(resolve(cwd,descriptor.path)));pins(release);pins(JSON.parse(await readFile(resolve(cwd,release.source_bundle.path))));for(const entry of release.additions){const asset=JSON.parse(await readFile(resolve(cwd,entry.metadata.path)));for(const key of ['glb','blend','preview'])paths.add(asset[key]);const index=JSON.parse(await readFile(resolve(cwd,release.capture.index.path)));paths.add(index.posters.find(p=>p.id===entry.id).path);}}
 for(const path of paths){await mkdir(dirname(resolve(sandbox,path)),{recursive:true});await copyFile(resolve(cwd,path),resolve(sandbox,path));}
 try{
  const collect=()=>collectBatches5657Additions(sandbox,descriptors),first=await collect();assert.equal(first.additions.length,7);assert(!first.additions.some(a=>a.id==='nidula-baltica'));const ids=new Set(first.additions.map(a=>a.id));assert.deepEqual(manifest.assets.filter(a=>ids.has(a.id)),first.additions);
  let passed=3;
  async function altered(path,change){const p=resolve(sandbox,path),old=await readFile(p);try{await writeFile(p,change(old));await assert.rejects(collect);passed++;}finally{await writeFile(p,old);}}
  const r=first.releases[0],e=r.additions[0],a=first.additions[0];
  for(const path of [descriptors[0].path,e.metadata.path,e.candidate.path,e.frozen_brief.path,e.proof.path,e.review.path,r.source_bundle.path,r.capture.report.path,r.capture.zip_verification.path,a.glb,a.blend,a.preview])await altered(path,b=>Buffer.concat([b,Buffer.from(' ')]));
  await altered('assets/turntables/index.json',b=>{const x=JSON.parse(b);x.posters.find(p=>p.id===a.id).sha256='0'.repeat(64);return JSON.stringify(x);});
  assert.deepEqual(await collect(),first);passed++;console.log(`Batch56/57 bounded collector checks passed: ${passed}; isolated copies only, no model generation or repeated visual QA.`);
 }finally{await rm(sandbox,{recursive:true,force:true});}
}

if(!process.argv.includes('--batch54-only')&&!process.argv.includes('--batches58-61-only')){await testBatches5657();await testBatches5155();}

// Exact selected-scope regression cases; all destructive probes use copied bytes.
{
 const {collectBatches5859Additions}=await import('./concept-landair-release.mjs');
 const {BATCH58_RELEASE,BATCH59_RELEASE}=await import('./accepted-concept-landair-release.mjs');
 const {copyFile}=await import('node:fs/promises');
 const sandbox=await mkdtemp(join(tmpdir(),'vault-batches5859-'));
 const digest=b=>createHash('sha256').update(b).digest('hex');
 const releases=[BATCH58_RELEASE,BATCH59_RELEASE],descriptorPaths=['assets/releases/batch58-20261020.json','assets/releases/batch59-20261020.json'];
 const descriptors=await Promise.all(descriptorPaths.map(async path=>({path,sha256:digest(await readFile(path))})));
 const paths=new Set(['site/viewer.js','assets/turntables/index.json',...descriptorPaths]);
 for(const d of releases){paths.add(d.source_bundle.path);paths.add(d.publication_policy.path);for(const p of d.protected_source_inputs)paths.add(p.path);const bundle=JSON.parse(await readFile(d.source_bundle.path));for(const p of bundle.files)paths.add(p.path);const index=JSON.parse(await readFile(d.capture.index.path));for(const e of d.additions){paths.add(e.metadata.path);const a=JSON.parse(await readFile(e.metadata.path));for(const k of ['glb','blend','preview'])paths.add(a[k]);paths.add(index.posters.find(c=>c.id===a.id).path);}}
 let cases=0;
 try{
  for(const path of paths){await mkdir(dirname(resolve(sandbox,path)),{recursive:true});await copyFile(path,resolve(sandbox,path));}
  const collect=()=>collectBatches5859Additions(sandbox,descriptors),initial=await collect();assert.deepEqual(initial.additions.map(a=>a.id).sort(),['barchan-dune','calamophyton','current-ripple-surface','glacial-erratic','gypsum-cave-flower','perspicaris','stalactite-group']);cases++;
  for(const a of initial.additions){assert.equal(a.approval_provenance.formal_profile_acceptance,'BLOCKED');assert.equal(a.approval_provenance.hardware_gpu_verified,false);assert.equal(a.approval_provenance.target_scene_verified,false);assert.equal(a.approval_provenance.candidate_record_approved_for_brief,false);}
  const tamper=async(path,modify,action=collect)=>{const f=resolve(sandbox,path),old=await readFile(f);try{await writeFile(f,modify(old));await assert.rejects(action);cases++;}finally{await writeFile(f,old);}};
  const append=b=>Buffer.concat([b,Buffer.from('tamper')]);
  for(const d of releases){
   for(const e of d.additions){const a=JSON.parse(await readFile(e.metadata.path));for(const path of [e.candidate.path,e.metadata.path,a.glb,a.blend,a.preview,e.frozen_brief.path,e.proof.path,e.rebuilds[0].path])await tamper(path,append);}
   for(const path of [d.source_bundle.path,d.review.path,d.review_custody.path,d.capture.report.path,d.capture.index.path,d.capture.zip_verification.path,d.capture.independent_review.path])await tamper(path,append);
  }
  for(const field of ['formal_profile_acceptance','hardware_gpu_verified','target_scene_verified','provider_generation_timestamp'])await tamper(descriptorPaths[0],b=>{const d=JSON.parse(b);d[field]=field==='formal_profile_acceptance'?'PASS':field==='provider_generation_timestamp'?'2026-10-20T00:00:00Z':true;return JSON.stringify(d);});
  // Coordinated descriptor+hash edits must still differ from the fixed accepted literal.
  await tamper(descriptorPaths[1],b=>{const d=JSON.parse(b);d.additions[0].id='erbenochile';return JSON.stringify(d);},async()=>{const changed=descriptors.map(x=>({...x}));changed[1].sha256=digest(await readFile(resolve(sandbox,descriptorPaths[1])));return collectBatches5859Additions(sandbox,changed);});
  await tamper('assets/turntables/index.json',b=>{const d=JSON.parse(b);d.posters.push(d.posters.find(x=>x.id==='calamophyton'));return JSON.stringify(d);});
  await tamper('assets/turntables/index.json',b=>{const d=JSON.parse(b);d.posters=d.posters.filter(x=>x.id!=='calamophyton');return JSON.stringify(d);});
  for(const path of [initial.additions[0].glb,'assets/turntables/index.json']){const file=resolve(sandbox,path),saved=file+'.saved';await rename(file,saved);try{await symlink(saved,file);await assert.rejects(collect,/symlinks forbidden/);cases++;}finally{await rm(file);await rename(saved,file);}}
  await tamper('site/viewer.js',append);
  assert.deepEqual(await collect(),initial);cases++;
  console.log(`Batch58/59 bounded release: ${cases} checks passed; seven exact revisions, original candidate/source/review/capture pins, no formal approval promotion, old metadata unaffected.`);
 }finally{await rm(sandbox,{recursive:true,force:true});}
}

// Batch60/61 delivery selections must not fall back to historical archive anchors.
{
 const {readFile:readActual,writeFile:writeActual,stat,rename:renameActual}=await import('node:fs/promises');const {createHash}=await import('node:crypto');
 const {linkFixtureFile}=await import('./test-fixture-link.mjs');
 const {collectBatches6061Additions}=await import('./concept-landair-release.mjs');
 const {ACCEPTED_BOUNDED_BATCHES}=await import('./accepted-bounded-batches.mjs');
 const descriptors=ACCEPTED_BOUNDED_BATCHES.filter(e=>['assets/releases/batch60-20261020.json','assets/releases/batch61-20261020.json'].includes(e.descriptor.path)).map(e=>e.descriptor);
 if(descriptors.length){
  const sandbox=await mkdtemp(join(tmpdir(),'vault-batches6061-'));
  const paths=new Set(['site/viewer.js','assets/turntables/index.json','site/public/gallery/resources.json']);
  function pins(v){if(!v||typeof v!=='object')return;if(typeof v.path==='string'&&typeof v.sha256==='string')paths.add(v.path);for(const x of Object.values(v))pins(x);}
  for(const d of descriptors){pins(d);const release=JSON.parse(await readActual(d.path));pins(release);pins(JSON.parse(await readActual(release.source_bundle.path)));const index=JSON.parse(await readActual(release.capture.index.path)),receipt=JSON.parse(await readActual(release.capture.gallery_receipt.path));for(const e of release.additions){const a=JSON.parse(await readActual(e.metadata.path));for(const k of ['glb','blend','preview'])paths.add(a[k]);paths.add(index.posters.find(p=>p.id===e.id).path);for(const f of receipt.rows.find(p=>p.id===e.id).files)paths.add('site/public/'+f.path);}}
  const sourceBefore=new Map();
  for(const path of paths){const source=resolve(path);sourceBefore.set(path,{sha256:createHash('sha256').update(await readActual(source)).digest('hex'),mode:(await stat(source)).mode&0o7777});await mkdir(dirname(resolve(sandbox,path)),{recursive:true});await linkFixtureFile(source,resolve(sandbox,path));}
  const readFile=p=>readActual(resolve(sandbox,p));
  // Atomic replacement detaches shared evidence inodes before every probe.
  const writeFile=async(p,b)=>{const out=resolve(sandbox,p),temp=out+'.private-test';await writeActual(temp,b);await renameActual(temp,out);};
  try{
  const result=await collectBatches6061Additions(sandbox,descriptors);assert.equal(result.additions.length,8);assert.deepEqual(result.additions.map(a=>a.id).sort(),['aragonite-frostwork','collinsium','daemonelix-helical-burrow','drumlin','glacial-cirque','mesa','pseudopulex','yardang']);
  const target=descriptors[1].path,bytes=await readFile(target),original=JSON.parse(bytes),hash=b=>createHash('sha256').update(b).digest('hex');
  for(const [name,edit]of [
   ['missing active v003',e=>delete e.active_candidate],
   ['historical candidate fallback',e=>e.active_candidate=e.candidate],
   ['rejected v002 candidate',e=>e.active_candidate.path=e.candidate_root+'/candidate-scale-v002.json'],
   ['old render subject',e=>e.proof.path=e.candidate_root+'/proof-final/render-manifest.json'],
   ['wrong differential QA scope',e=>e.active_review=e.review]
  ]){
   const changed=structuredClone(original);edit(changed.additions.find(a=>a.id==='mesa'));const b=Buffer.from(JSON.stringify(changed));
   try{await writeFile(target,b);await assert.rejects(()=>collectBatches6061Additions(sandbox,[descriptors[0],{path:target,sha256:hash(b)}]),/Only fixed independently reviewed Batch60\/61 bytes authorized/,name);}finally{await writeFile(target,bytes);}
  }
  const mesa=original.additions.find(a=>a.id==='mesa'),proof=await readFile(mesa.proof.path),bad=JSON.parse(proof);bad.subject.brief_sha256='0'.repeat(64);
  try{await writeFile(mesa.proof.path,JSON.stringify(bad));await assert.rejects(()=>collectBatches6061Additions(sandbox,descriptors),/hash mismatch/,'changed v003 render subject');}finally{await writeFile(mesa.proof.path,proof);}
  console.log('Batch60/61: exact8 positive + six isolated historical/active-delivery fail-closed negatives passed; no source re-QA.');
  }finally{try{for(const [path,before]of sourceBefore){assert.equal(createHash('sha256').update(await readActual(resolve(path))).digest('hex'),before.sha256,'Fixture source bytes changed: '+path);assert.equal((await stat(resolve(path))).mode&0o7777,before.mode,'Fixture source mode changed: '+path);}}finally{await rm(sandbox,{recursive:true,force:true});}}
 }
}

// Preserve the immutable main43 manifest before composing the pinned next44.
// The fixed canonical digest works in shallow CI checkouts without historical Git objects.
{
 const {appendBatches5861Release,appendBatches6267Release}=await import('./concept-landair-release.mjs');
 const {appendFortyFourRelease}=await import('./forty-four-release.mjs');
 const {digest}=await import('./model-registry.mjs');
 const {historical295Fixture}=await import('./test-historical295-fixture.mjs');
 const manifest=historical295Fixture(JSON.parse(await readFile('assets/manifest.json')));
 const expected251=structuredClone(manifest);expected251.assets=expected251.assets.slice(0,251);delete expected251.publication.forty_four_descriptors;
 // assets/manifest.json at 43e40fc89f2b369a5f1858e72fa58a0d10318124,
 // hashed with model-registry digest (the entire canonical manifest, not just IDs).
 assert.equal(digest(expected251),'7f6c94c26f0a47b7a1b461f48070868be57f94161c9a1e3c11b5666cd8b273e0','The complete immutable main43 predecessor must remain unchanged');
 const descriptors5859=expected251.publication.batches58_59_descriptors,descriptors6061=expected251.publication.batches60_61_descriptors,descriptors6267=expected251.publication.batches62_67_descriptors;
 const expected232=structuredClone(expected251);expected232.assets=expected232.assets.slice(0,232);delete expected232.publication.batches62_67_descriptors;
 const base=structuredClone(expected232);base.assets=base.assets.slice(0,217);delete base.publication.batches58_59_descriptors;delete base.publication.batches60_61_descriptors;
 const actual232=await appendBatches5861Release(process.cwd(),base,descriptors5859,descriptors6061);
 assert.deepEqual(actual232,expected232);
 const actual251=await appendBatches6267Release(process.cwd(),actual232,descriptors6267);
 assert.equal(actual251.assets.length,251);assert.deepEqual(actual251.assets.slice(0,232),actual232.assets);assert.deepEqual(actual251,expected251);
 const actual295=await appendFortyFourRelease(process.cwd(),actual251,manifest.publication.forty_four_descriptors);
 assert.equal(actual295.assets.length,295);assert.deepEqual(actual295.assets.slice(0,251),actual251.assets);assert.deepEqual(actual295,manifest);
 for(const count of [194,201,216,218,225]){const bad=structuredClone(base);bad.assets=Array.from({length:count},(_,i)=>base.assets[i%217]);await assert.rejects(()=>appendBatches5861Release(process.cwd(),bad,descriptors5859,descriptors6061),/exact217-model predecessor/);}
 const duplicate=structuredClone(base);duplicate.assets[0]=duplicate.assets[1];await assert.rejects(()=>appendBatches5861Release(process.cwd(),duplicate,descriptors5859,descriptors6061),/Duplicate Batch58-61 publication ID/);
 await assert.rejects(()=>appendBatches5861Release(process.cwd(),base,descriptors6061,descriptors5859));
 await assert.rejects(()=>appendBatches5861Release(process.cwd(),base,descriptors5859,undefined));
 console.log('Batch58-67/next44 union: immutable main43 full-manifest digest, exact217+15=232, full232+19=251 and full251+44=295 equality, unchanged old251, and eight fail-closed composition cases passed.');
}
