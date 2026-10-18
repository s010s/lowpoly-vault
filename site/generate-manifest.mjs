/** Explicit release step. Never invoked by build or dev. */
import { readdir, readFile, stat, writeFile, rename } from 'node:fs/promises';
import { dirname, join, resolve, relative } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createHash } from 'node:crypto';
import { catalogMembership } from './curation.js';
import { validAssetId } from './routes.js';

// Versioned candidates can share IDs and are never implicitly promoted by discovery.
async function discover(dir,candidateRoot){const result=[];for(const entry of await readdir(dir,{withFileTypes:true})){const p=join(dir,entry.name);if(p===candidateRoot)continue;if(entry.isDirectory())result.push(...await discover(p,candidateRoot));else if(entry.isFile()&&entry.name==='metadata.json')result.push(p);}return result.sort();}
const runFile=promisify(execFile);
const candidateGate=fileURLToPath(new URL('../scripts/validate_candidate.py',import.meta.url));
const requireThat=(condition,message)=>{if(!condition)throw new Error(message);};
export async function collectManifest(root=process.cwd(),{preview=false}={}){
  const base=resolve(root),files=await discover(join(base,'assets'),join(base,'assets/candidates')),assets=[],ids=new Set(),errors=[];
  requireThat(files.length,'No asset metadata found. No manifest was written.');
  for(const file of files){try{
    const asset=JSON.parse(await readFile(file,'utf8')),folder=dirname(file),label=relative(base,folder);
    requireThat(validAssetId(asset.id)&&!ids.has(asset.id),`${label}: missing or duplicate id`);ids.add(asset.id);
    requireThat(asset.name?.en&&asset.name?.zh&&asset.description?.en&&asset.description?.zh,`${label}: bilingual name and description required`);
    const membership=catalogMembership(asset);
    requireThat(membership.worlds.length&&membership.worlds.every(id=>/^[a-z0-9-]+$/.test(id)),`${label}: a valid world or legacy collection is required`);
    requireThat(typeof asset.category==='string'&&/^[a-z0-9-]+$/.test(asset.category),`${label}: valid cross-world category required`);
    requireThat(membership.packs.every(id=>/^[a-z0-9-]+$/.test(id)),`${label}: valid pack IDs required`);
    // Paths are stable storage locations, independent of mutable world/category membership.
    // Existing legacy folders remain valid; no physical migration or duplicate copies are needed.
    requireThat(asset.license==='CC-BY-4.0',`${label}: expected asset license CC-BY-4.0`);
    requireThat(Number.isInteger(asset.triangles)&&asset.triangles>0,`${label}: invalid triangle count`);
    requireThat(Array.isArray(asset.dimensions)&&asset.dimensions.length===3&&asset.dimensions.every(n=>Number.isFinite(n)&&n>0),`${label}: invalid meter dimensions`);
    for(const key of ['glb','blend','preview']){
      const p=asset[key];requireThat(typeof p==='string'&&p.startsWith('assets/')&&!p.split('/').includes('..'),`${label}: unsafe or missing ${key} path`);
      const full=resolve(base,p);requireThat(dirname(full)===folder,`${label}: ${key} must belong to this asset directory`);requireThat((await stat(full)).size>0,`${p}: empty file`);
      if(key==='glb'||key==='blend'){const bytes=await readFile(full);if(asset.sha256?.[key])requireThat(createHash('sha256').update(bytes).digest('hex')===asset.sha256[key],`${p}: SHA-256 no longer matches QA metadata`);if(key==='glb')requireThat(bytes.toString('ascii',0,4)==='glTF'&&bytes.readUInt32LE(4)===2&&bytes.readUInt32LE(8)===bytes.length,`${p}: invalid GLB 2 header`);}
    }
    const qa=JSON.parse(await readFile(join(folder,'qa.json'),'utf8'));
    for(const stage of (preview?['source','glb']:['source','glb','khronos_validator','threejs_runtime','visual_review'])){
      const report=qa[stage];requireThat(report&&['pass','pass_with_warnings'].includes(report.status),`${label}: ${stage} QA is ${report?.status||'missing'}`);
      requireThat(!report.errors?.length,`${label}: ${stage} has unresolved errors`);
      if(!preview&&(report.status==='pass_with_warnings'||report.warnings?.length)){requireThat(qa.warning_review?.status==='pass'||(Array.isArray(qa.reviewed_warnings)&&qa.reviewed_warnings.length)||(Array.isArray(asset.reviewed_warnings)&&asset.reviewed_warnings.length),`${label}: ${stage} warnings need explicit review`);}
    }
    if(!preview){
      // Formal publication needs the new evidence gate. The separately authorized,
      // hash-locked initial-ten release deliberately calls preview:true and stays WIP.
      const record=asset.candidate_record;
      requireThat(typeof record==='string'&&!record.startsWith('/')&&!record.split('/').includes('..')&&!record.includes('\\'),`${label}: formal release requires a safe candidate_record path`);
      let validation;
      try{
        const {stdout}=await runFile('python3',[candidateGate,record,'--root',base,'--require-approved','--json'],{maxBuffer:2*1024*1024});
        validation=JSON.parse(stdout);
      }catch(error){throw new Error(`${label}: candidate evidence gate refused formal release: ${error.stdout||error.stderr||error.message}`);}
      requireThat(validation.valid&&validation.approved_for_brief&&validation.profile==='production',`${label}: approved production brief required for formal release`);
      requireThat(validation.asset_id===asset.id,`${label}: candidate_record belongs to another asset`);
      const actualGlbHash=createHash('sha256').update(await readFile(resolve(base,asset.glb))).digest('hex');
      requireThat(validation.subject?.glb_sha256===actualGlbHash,`${label}: candidate_record approves different GLB bytes`);
      const sourceHash=createHash('sha256').update(await readFile(resolve(base,asset.blend))).digest('hex');
      const previewHash=createHash('sha256').update(await readFile(resolve(base,asset.preview))).digest('hex');
      requireThat(validation.artifact_sha256?.source===sourceHash,`${label}: candidate_record approves different editable source bytes`);
      requireThat(validation.approved_visual_image_sha256?.includes(previewHash),`${label}: published preview is absent from approved visual evidence`);
      requireThat(validation.measurements?.triangles===asset.triangles,`${label}: published triangle count differs from measured candidate`);
    }
    assets.push({...asset,...membership,collection:asset.collection||membership.worlds[0],qa:`${label}/qa.json`});
  }catch(error){errors.push(`${relative(base,file)}: ${error.message}`);}}
  requireThat(!errors.length,`Manifest generation refused; no file was changed:\n${errors.join('\n')}`);
  return {version:1,schema_version:2,...(preview?{review_only:true}:{}),license:'CC-BY-4.0',code_license:'MIT',author:'Leon Made This / s010s',attribution_url:'https://github.com/s010s/lowpoly-vault',assets};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
  try{const preview=process.argv.includes('--preview');const manifest=await collectManifest(process.cwd(),{preview});if(process.argv.includes('--check'))console.log(`Release gate passed: ${manifest.assets.length} assets. Manifest not changed.`);else{const destination=resolve(preview?'assets/manifest.review.json':'assets/manifest.json'),temp=`${destination}.tmp`;await writeFile(temp,JSON.stringify(manifest,null,2)+'\n');await rename(temp,destination);console.log(`Wrote ${relative(process.cwd(),destination)} with ${manifest.assets.length} ${preview?'structurally checked, review-pending':'QA-approved'} assets.`);}}
  catch(error){console.error(error.message);process.exitCode=1;}
}
