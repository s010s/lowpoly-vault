/** Synthetic acceptance fixtures only. No real refinement is approved or published by these tests. */
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, cp, readFile, writeFile, rename, symlink, rm, readdir } from 'node:fs/promises';
import { join, resolve, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { collectRefinedRelease, REFINABLE_ASSET_IDS, INITIAL_PUBLICATION_SHA256 } from './refined-release.mjs';
import { collectInitialRelease, checkPublishedManifest, INITIAL_ASSET_IDS } from './initial-release.mjs';
import { assetFileAllowlist, creditText, deliverManifestAssets } from './asset-delivery.mjs';
import { collectTurntables } from './turntable-delivery.mjs';
import { prepareRenderCapture } from './prepare-render-capture.mjs';

const runFile = promisify(execFile), sourceRoot = fileURLToPath(new URL('../', import.meta.url));
const root = await mkdtemp(join(tmpdir(), 'vault-refined-release-'));
const initialPath = 'assets/initial-publication.json', descriptorPath = 'assets/releases/test-only.json';
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const json = value => JSON.stringify(value, null, 2) + '\n';
const hashFile = async path => sha(await readFile(resolve(root, path)));
const snapshots = new Map();
let checks = 0;
async function save(path, value) { await mkdir(dirname(resolve(root, path)), {recursive:true}); await writeFile(resolve(root, path), json(value)); }
async function readJSON(path) { return JSON.parse(await readFile(resolve(root, path))); }
async function descriptorPin() { return {path:descriptorPath, sha256:await hashFile(descriptorPath)}; }
async function collect() { return collectRefinedRelease(root, await descriptorPin()); }
async function check(name, action) { try { await action(); ++checks; } catch (error) { error.message = `${name}: ${error.message}`; throw error; } }
async function changedJSON(path, mutate, action) {
  const original = await readFile(resolve(root, path)), value = JSON.parse(original);
  mutate(value);
  try { await save(path, value); await action(value); } finally { await writeFile(resolve(root, path), original); }
}
async function rejectDescriptor(name, mutate, pattern) {
  await check(name, () => changedJSON(descriptorPath, mutate, () => assert.rejects(collect, pattern)));
}
// Rehash only the disposable publication pin, never the candidate's evidence/acceptance seal.
async function mutatePinned(role, mutate, action) {
  const descriptor = await readJSON(descriptorPath), entry = descriptor.revisions[0];
  const path = role === 'candidate' ? `${entry.candidate_root}/${entry.candidate.path}` : entry.metadata.path;
  await changedJSON(path, mutate, async () => {
    const digest = await hashFile(path);
    await changedJSON(descriptorPath, d => { d.revisions[0][role].sha256 = digest; }, action);
  });
}
async function rejectPinned(name, role, mutate, pattern) {
  await check(name, () => mutatePinned(role, mutate, () => assert.rejects(collect, pattern)));
}
async function substituteSymlink(path, target, action) {
  const full = resolve(root, path), backup = `${full}.test-backup`;
  await rename(full, backup);
  try { await symlink(target || backup, full); await action(); }
  finally { await rm(full, {force:true}); await rename(backup, full); }
}
// Reuse the evidence validator's explicitly synthetic fixture generator and its rebind helper.
const fixturePython = `import sys,json\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nfrom test_validate_candidate import build_fixture,CandidateGateTests\nroot=Path(sys.argv[2]); asset_id=sys.argv[3]\nc,path=build_fixture(root,base='candidate',glb_name=asset_id+'.glb',profile=sys.argv[4])\nc['asset_id']=asset_id\nhelper=CandidateGateTests(); helper.root=root; helper.candidate=c\nhelper.rebind_brief(lambda brief: brief.update(asset_id=asset_id))\npath.write_text(json.dumps(c,indent=2)+'\\n')\n`;
async function fixture(id, profile = 'production', suffix = '') {
  const candidateRoot = `experiments/synthetic-only/${id}${suffix}`;
  await runFile('python3', ['-c', fixturePython, join(sourceRoot, 'scripts'), resolve(root, candidateRoot), id, profile]);
  return {candidate_root:candidateRoot, candidate:{path:'candidate/candidate.json', sha256:await hashFile(`${candidateRoot}/candidate/candidate.json`)}};
}

try {
  const approval = JSON.parse(await readFile(resolve(sourceRoot, initialPath)));
  assert.equal(sha(await readFile(resolve(sourceRoot, initialPath))), INITIAL_PUBLICATION_SHA256);
  const paths = new Set([initialPath]);
  for (const asset of approval.assets) {
    for (const key of ['glb', 'blend', 'preview']) paths.add(asset[key]);
    for (const name of ['metadata.json', 'qa.json']) paths.add(join(dirname(asset.glb), name));
  }
  for (const path of paths) {
    await mkdir(dirname(resolve(root, path)), {recursive:true});
    await copyFile(resolve(sourceRoot, path), resolve(root, path));
    snapshots.set(path, await hashFile(path));
  }
  const initial = await collectInitialRelease(root), revisions = [];
  for (const id of REFINABLE_ASSET_IDS) {
    const record = await fixture(id), folder = `assets/revisions/${id}/v001`;
    const provenance = {author:'Synthetic revision creator', source_url:'https://example.invalid/synthetic-revision', changes:'SYNTHETIC TEST ONLY: changed branch and silhouette structure.'};
    const asset = {id, revision:'v001', name:{en:`Synthetic ${id}`, zh:'合成测试'}, description:{en:'Synthetic fixture only, not an approved real asset.', zh:'仅用于自动化测试，不是真实模型的审核结论。'},
      category:'test', collection:'prehistoric', license:'CC-BY-4.0', author:provenance.author, source_url:provenance.source_url, triangles:1, dimensions:[1,1,1],
      glb:`${folder}/${id}.glb`, blend:`${folder}/${id}.blend`, preview:`${folder}/preview.png`, sha256:{}};
    await mkdir(resolve(root, folder), {recursive:true});
    for (const [key, file] of [['glb', `${id}.glb`], ['blend', 'source.fixture'], ['preview', 'frame-000.png']]) {
      await copyFile(resolve(root, record.candidate_root, 'candidate', file), resolve(root, asset[key]));
      asset.sha256[key] = await hashFile(asset[key]);
    }
    const metadataPath = `${folder}/release-metadata.json`;
    await save(metadataPath, asset);
    revisions.push({id, revision:'v001', metadata:{path:metadataPath, sha256:await hashFile(metadataPath)}, ...record, sha256:asset.sha256, provenance});
  }
  const publication = {version:1, release_id:'test-only', release_status:'mixed', authorization:'owner_requested_publication_of_accepted_revisions', authorized_on:'2026-10-17T00:00:00Z',
    initial_publication:{path:initialPath, sha256:INITIAL_PUBLICATION_SHA256}, approved_asset_ids:[...REFINABLE_ASSET_IDS], revisions};
  await save(descriptorPath, publication);
  let manifest;
  await check('three accepted synthetic revisions preserve the seven WIP originals', async () => {
    manifest = await collect();
    assert.equal(manifest.release_status, 'mixed'); assert.equal(manifest.quality_status, 'mixed');
    assert.deepEqual(manifest.assets.map(a => a.id).sort(), INITIAL_ASSET_IDS);
    assert.equal(manifest.publication.approved_asset_ids.length, 3);
    assert.equal(manifest.publication.work_in_progress_asset_ids.length, 7);
    for (const asset of manifest.assets) {
      if (REFINABLE_ASSET_IDS.includes(asset.id)) {
        assert.equal(asset.quality_status, 'accepted_for_brief');
        assert(asset.glb.startsWith(`assets/revisions/${asset.id}/v001/`));
      } else assert.deepEqual(asset, initial.assets.find(a => a.id === asset.id));
    }
    assert.deepEqual(await collectInitialRelease(root), initial, 'Revision metadata must not enter legacy recursive discovery');
    await save('assets/manifest.json', manifest);
    assert.deepEqual(await checkPublishedManifest(root), manifest);
  });
  await check('a separately authorized subset leaves nine WIP originals', () => changedJSON(descriptorPath, d => {
    d.approved_asset_ids = [d.approved_asset_ids[0]]; d.revisions = [d.revisions[0]];
  }, async () => { const m = await collect(); assert.equal(m.publication.work_in_progress_asset_ids.length, 9); assert.equal(m.assets.filter(a => a.quality_status === 'accepted_for_brief').length, 1); }));
  await check('explicit CLI pin checks and generates only the expected temporary manifest', async () => {
    const script = fileURLToPath(new URL('./refined-release.mjs', import.meta.url)), pin = await descriptorPin();
    const before = await readFile(resolve(root, 'assets/manifest.json'));
    await runFile('node', [script, pin.path, '--sha256', pin.sha256, '--check'], {cwd:root});
    assert.deepEqual(await readFile(resolve(root, 'assets/manifest.json')), before);
    await assert.rejects(() => runFile('node', [script, pin.path], {cwd:root}), /Usage/);
    assert.deepEqual(await readFile(resolve(root, 'assets/manifest.json')), before);
    await runFile('node', [script, pin.path, '--sha256', pin.sha256], {cwd:root});
    assert.deepEqual(await readJSON('assets/manifest.json'), manifest);
  });
  await check('missing or stale descriptor pin cannot publish', async () => {
    await assert.rejects(() => collectRefinedRelease(root), /descriptor pin/);
    await assert.rejects(() => collectRefinedRelease(root, {path:descriptorPath, sha256:'0'.repeat(64)}), /SHA-256 mismatch/);
    await assert.rejects(() => collectRefinedRelease(root, {path:descriptorPath, sha256:''}), /fixed SHA-256/);
  });
  for (const [key, value] of [['version', 2], ['release_status', 'approved'], ['authorization', 'candidate_approval_only'], ['authorized_on', '2026-10-17']]) {
    await rejectDescriptor(`reject invalid descriptor ${key}`, d => { d[key] = value; });
  }
  await rejectDescriptor('reject unknown publication gates', d => { d.skip_gpu = true; }, /unknown fields/);
  await rejectDescriptor('reject unapproved replacement ID', d => { d.approved_asset_ids[0] = 'cycad'; d.revisions[0].id = 'cycad'; }, /refinement IDs/);
  await rejectDescriptor('reject duplicate authorized IDs', d => { d.approved_asset_ids.push(d.approved_asset_ids[0]); }, /unique refinement IDs/);
  await rejectDescriptor('reject duplicate replacement entries', d => { d.revisions.push(d.revisions[0]); }, /without duplicates/);
  await rejectDescriptor('reject unauthorized extra replacement', d => { d.revisions.push({...d.revisions[0], id:'cycad'}); }, /exactly match approved IDs/);
  await rejectDescriptor('reject no explicit replacements', d => { d.approved_asset_ids = []; d.revisions = []; }, /explicitly approved/);
  await rejectDescriptor('reject incomplete provenance', d => { delete d.revisions[0].provenance.changes; }, /missing or unknown/);
  await rejectDescriptor('reject empty provenance', d => { d.revisions[0].provenance.changes = ''; }, /change statement/);
  await rejectDescriptor('reject unsafe provenance URL', d => { d.revisions[0].provenance.source_url = 'javascript:alert(1)'; }, /HTTP/);
  await rejectDescriptor('reject changed original approval pin', d => { d.initial_publication.sha256 = '0'.repeat(64); }, /immutable/);
  await check('original approval path changes fail even if new descriptor is rehashed', () => changedJSON(initialPath, p => { p.assets[0].glb += '.changed'; }, () => assert.rejects(collect, /SHA-256 mismatch/)));
  await check('changing old approval and repinning its hash fails', () => changedJSON(initialPath, p => { p.assets[0].glb += '.changed'; }, async () => {
    const digest = await hashFile(initialPath);
    await changedJSON(descriptorPath, d => { d.initial_publication.sha256 = digest; }, () => assert.rejects(collect, /immutable/));
  }));

  for (const role of ['metadata', 'candidate']) {
    await rejectDescriptor(`reject missing ${role} checksum`, d => { delete d.revisions[0][role].sha256; }, /missing or unknown/);
    await rejectDescriptor(`reject stale ${role} checksum`, d => { d.revisions[0][role].sha256 = '0'.repeat(64); }, /SHA-256 mismatch/);
  }
  await rejectDescriptor('reject missing candidate record', d => { d.revisions[0].candidate.path = 'absent.json'; }, /ENOENT/);
  await rejectPinned('reject pending candidate', 'candidate', c => { c.approval.status = 'pending'; }, /candidate evidence gate refused/);
  await rejectPinned('reject missing candidate gate', 'candidate', c => { delete c.stages.gpu; }, /candidate evidence gate refused/);
  for (const status of ['unknown', 'stale', 'fail', 'invented-pass']) {
    await rejectPinned(`reject ${status} candidate gate`, 'candidate', c => { c.stages.gpu.status = status; }, /candidate evidence gate refused/);
  }
  await rejectPinned('reject unknown required candidate stage', 'candidate', c => { c.stages.imagined_gate = {status:'pass'}; }, /candidate evidence gate refused/);
  await rejectPinned('reject stale acceptance snapshot', 'candidate', c => { c.stages.visual.note += ' Changed after final approval'; }, /stale review snapshot/);
  await check('reject stale candidate evidence despite an unchanged record', async () => {
    const path = `${revisions[0].candidate_root}/candidate/gpu-report.json`, before = await readFile(resolve(root, path));
    try { await writeFile(resolve(root, path), Buffer.concat([before, Buffer.from(' ')])); await assert.rejects(collect, /SHA-256 mismatch/); }
    finally { await writeFile(resolve(root, path), before); }
  });
  for (const [name, id, profile, pattern] of [['study approval', REFINABLE_ASSET_IDS[0], 'study', /approved production brief/], ['another asset approval', 'test-only', 'production', /belongs to another asset/]]) {
    const record = await fixture(id, profile, `-${profile}-other`);
    await rejectDescriptor(`reject ${name}`, d => { Object.assign(d.revisions[0], record); }, pattern);
  }
  await rejectPinned('reject wrong metadata asset ID', 'metadata', m => { m.id = 'fern-cluster'; }, /belongs to another asset/);
  await rejectPinned('reject wrong metadata revision', 'metadata', m => { m.revision = 'v002'; }, /revision differs/);
  await check('reject a publication revision different from the accepted candidate revision', async () => {
    const first = revisions[0], nextFolder = `assets/revisions/${first.id}/v002`;
    await cp(resolve(root, dirname(first.metadata.path)), resolve(root, nextFolder), {recursive:true});
    const path = `${nextFolder}/release-metadata.json`, metadata = await readJSON(path);
    metadata.revision = 'v002';
    for (const key of ['glb', 'blend', 'preview']) metadata[key] = metadata[key].replace('/v001/', '/v002/');
    await save(path, metadata);
    const digest = await hashFile(path);
    try {
      await changedJSON(descriptorPath, d => { d.revisions[0].revision = 'v002'; d.revisions[0].metadata = {path, sha256:digest}; }, () => assert.rejects(collect, /candidate revision differs/));
    } finally { await rm(resolve(root, nextFolder), {recursive:true, force:true}); }
  });
  await rejectPinned('reject wrong measured count', 'metadata', m => { m.triangles = 2; }, /measured candidate/);
  await rejectPinned('reject blanket metadata approval claim', 'metadata', m => { m.quality_status = 'approved'; }, /reserved metadata field/);
  await rejectPinned('reject alternate card preview delivery path', 'metadata', m => { m.card_preview = 'assets/unapproved.png'; }, /reserved metadata field/);
  await rejectDescriptor('reject released files placed in legacy original directories', d => { d.revisions[0].metadata.path = initial.assets[0].glb.replace(/[^/]+$/, 'metadata.json'); }, /immutable release-metadata/);

  const firstAsset = manifest.assets.find(a => a.id === revisions[0].id);
  for (const key of ['glb', 'blend', 'preview']) {
    await rejectDescriptor(`reject missing ${key} publication hash`, d => { delete d.revisions[0].sha256[key]; }, /missing or unknown/);
    await rejectDescriptor(`reject wrong ${key} publication hash`, d => { d.revisions[0].sha256[key] = '0'.repeat(64); }, /file hashes differ/);
    await check(`reject unapproved ${key} bytes with repinned publication metadata`, async () => {
      const original = await readFile(resolve(root, firstAsset[key]));
      try {
        await writeFile(resolve(root, firstAsset[key]), Buffer.concat([original, Buffer.from('UNREVIEWED')]));
        const digest = await hashFile(firstAsset[key]);
        await mutatePinned('metadata', m => { m.sha256[key] = digest; }, () => changedJSON(descriptorPath, d => { d.revisions[0].sha256[key] = digest; }, () =>
          assert.rejects(collect, key === 'glb' ? /different GLB bytes/ : key === 'blend' ? /different editable source/ : /absent from approved visual evidence/)));
      } finally { await writeFile(resolve(root, firstAsset[key]), original); }
    });
    await check(`reject same-byte ${key} symlink`, () => substituteSymlink(firstAsset[key], null, () => assert.rejects(collect, /symlink/)));
    const original = initial.assets.find(a => a.id === firstAsset.id);
    await check(`preserve replaced original ${key} bytes`, async () => {
      const bytes = await readFile(resolve(root, original[key]));
      try { await writeFile(resolve(root, original[key]), Buffer.concat([bytes, Buffer.from('changed')])); await assert.rejects(collect); }
      finally { await writeFile(resolve(root, original[key]), bytes); }
    });
  }
  await rejectPinned('reject revision path traversal', 'metadata', m => { m.preview = 'assets/revisions/../escape.png'; }, /Unsafe/);
  await rejectDescriptor('reject candidate root traversal', d => { d.revisions[0].candidate_root = '../outside'; }, /Safe repository-relative/);
  await rejectDescriptor('reject absolute candidate root', d => { d.revisions[0].candidate_root = '/tmp'; }, /Safe repository-relative/);
  await rejectDescriptor('reject candidate path traversal', d => { d.revisions[0].candidate.path = '../candidate.json'; }, /Safe repository-relative/);
  await check('reject candidate root symlink even inside repository', () => substituteSymlink(revisions[0].candidate_root, null, () => assert.rejects(collect, /candidate_root symlinks/)));
  await check('reject candidate record symlink', () => substituteSymlink(`${revisions[0].candidate_root}/${revisions[0].candidate.path}`, null, () => assert.rejects(collect, /symlink/)));
  await check('reject descriptor symlink', () => substituteSymlink(descriptorPath, null, () => assert.rejects(collect, /symlink/)));
  await check('reject metadata symlink', () => substituteSymlink(revisions[0].metadata.path, null, () => assert.rejects(collect, /symlink/)));
  const outside = await mkdtemp(join(tmpdir(), 'vault-refined-outside-'));
  try {
    await copyFile(resolve(root, firstAsset.preview), join(outside, 'preview.png'));
    await check('reject asset symlink escaping repository', () => substituteSymlink(firstAsset.preview, join(outside, 'preview.png'), () => assert.rejects(collect, /symlink/)));
  } finally { await rm(outside, {recursive:true, force:true}); }
  await check('reject accidentally discoverable duplicate metadata.json', async () => {
    const duplicate = resolve(root, dirname(revisions[0].metadata.path), 'metadata.json');
    await copyFile(resolve(root, revisions[0].metadata.path), duplicate);
    try { await assert.rejects(collect, /duplicate id/); } finally { await rm(duplicate); }
  });
  for (const [name, mutate] of [
    ['blanket quality promotion', m => { m.quality_status = 'approved'; }],
    ['original quality promotion', m => { m.assets.find(a => a.quality_status === 'work_in_progress').quality_status = 'accepted_for_brief'; }],
    ['unapproved catalog entry', m => { m.assets.push({...m.assets[0], id:'extra'}); }],
    ['duplicate catalog entry', m => { m.assets.push(m.assets[0]); }],
    ['missing catalog entry', m => { m.assets.pop(); }],
  ]) await check(`reject stored manifest ${name}`, () => changedJSON('assets/manifest.json', mutate, () => assert.rejects(() => checkPublishedManifest(root), /exactly match/)));
  await rejectPinned('reject alternate GLB filename that breaks viewer identity','metadata',asset=>{asset.glb=asset.glb.replace(/[^/]+$/, 'renamed.glb');},/basename must preserve catalog identity/);
  await check('capture preparation preserves exact mixed publication selection and revision bytes',async()=>{
    const out=join(root,'test-capture');
    const selected=await prepareRenderCapture({root,outDir:out});
    assert.deepEqual(selected,manifest);
    const captured=JSON.parse(await readFile(resolve(out,'assets/manifest.json')));
    assert.equal(captured.release_status,'mixed');
    for(const asset of captured.assets){
      assert.equal(sha(await readFile(resolve(out,asset.glb))),asset.sha256.glb);
      if(REFINABLE_ASSET_IDS.includes(asset.id))assert(asset.glb.startsWith(`assets/revisions/${asset.id}/`));
    }
    const originalPath=initial.assets.find(a=>a.id===revisions[0].id).glb;
    await assert.rejects(()=>readFile(resolve(out,originalPath)),{code:'ENOENT'});
  });
  await check('revision-aware deterministic downloads contain only allowlisted model/source/credits', async () => {
    const out = join(root, 'test-output');
    const delivered = await deliverManifestAssets(manifest, out, {root});
    assert.equal(assetFileAllowlist(delivered).length, 30);
    const revised = delivered.assets.find(a => a.id === revisions[0].id), original = delivered.assets.find(a => !REFINABLE_ASSET_IDS.includes(a.id));
    const credits = creditText(revised, delivered);
    assert(credits.includes('Revision creator: Synthetic revision creator'));
    assert(credits.includes('Changes: SYNTHETIC TEST ONLY'));
    assert(credits.includes('Original creator: Leon Made This / s010s'));
    assert(!credits.includes('no modifications are claimed'));
    assert(creditText(original, delivered).includes('further artistic and scientific refinement is ongoing'));
    await runFile('python3', ['-c', `import sys,zipfile,hashlib\nwith zipfile.ZipFile(sys.argv[1]) as z:\n assert sorted(z.namelist())==sorted([sys.argv[2],sys.argv[3],'CREDITS.txt'])\n assert hashlib.sha256(z.read(sys.argv[2])).hexdigest()==sys.argv[4]\n assert hashlib.sha256(z.read(sys.argv[3])).hexdigest()==sys.argv[5]\n assert b'Changes: SYNTHETIC TEST ONLY' in z.read('CREDITS.txt')\n`, resolve(out, revised.downloads.bundle), revised.glb.split('/').at(-1), revised.blend.split('/').at(-1), revised.sha256.glb, revised.sha256.blend]);
    assert(!(await readdir(resolve(out, dirname(revised.glb)))).includes('release-metadata.json'));
    assert.equal(delivered.assets.find(a => a.id === original.id).quality_status, 'work_in_progress');
  });
  await check('old website turntables reject legacy routes or revised GLB hash mismatches', async () => {
    await mkdir(resolve(root, 'assets/turntables'), {recursive:true});
    await copyFile(resolve(sourceRoot, 'assets/turntables/index.json'), resolve(root, 'assets/turntables/index.json'));
    const oldHash = initial.assets.find(a => a.id === 'natural-arch').sha256.glb;
    const newHash = manifest.assets.find(a => a.id === 'natural-arch').sha256.glb;
    await assert.rejects(() => collectTurntables(manifest, root), error => (error.actual === oldHash && error.expected === newHash) || /assets\/turntables\/.*\/v001\//.test(error.expected || ''));
  });
  await check('all originals and their approval/metadata/QA remain byte-identical', async () => {
    for (const [path, digest] of snapshots) assert.equal(await hashFile(path), digest, path);
    assert.deepEqual(await collect(), manifest);
    assert.deepEqual(await checkPublishedManifest(root), manifest);
  });
  console.log(`Refined-release tests passed: ${checks} checks; strict production evidence; explicit pinned publication; 3 accepted/7 WIP; unchanged originals; safe revision paths; revision credits; no real asset approval.`);
} finally { await rm(root, {recursive:true, force:true}); }
