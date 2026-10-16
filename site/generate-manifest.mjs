/** Explicit release step. Never invoked by build or dev. */
import { readdir, readFile, stat, writeFile, rename } from 'node:fs/promises';
import { dirname, join, resolve, relative } from 'node:path';
import { pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';

async function discover(dir){const result=[];for(const entry of await readdir(dir,{withFileTypes:true})){const p=join(dir,entry.name);if(entry.isDirectory())result.push(...await discover(p));else if(entry.isFile()&&entry.name==='metadata.json')result.push(p);}return result.sort();}
const requireThat=(condition,message)=>{if(!condition)throw new Error(message);};
export async function collectManifest(root=process.cwd(),{preview=false}={}){
  const base=resolve(root),files=await discover(join(base,'assets')),assets=[],ids=new Set(),errors=[];
  requireThat(files.length,'No asset metadata found. No manifest was written.');
  for(const file of files){try{
    const asset=JSON.parse(await readFile(file,'utf8')),folder=dirname(file),label=relative(base,folder);
    requireThat(asset.id&&!ids.has(asset.id),`${label}: missing or duplicate id`);ids.add(asset.id);
    requireThat(asset.name?.en&&asset.name?.zh&&asset.description?.en&&asset.description?.zh,`${label}: bilingual name and description required`);
    requireThat(asset.collection&&asset.category,`${label}: collection and category required`);
    requireThat(label.split('/').slice(0,3).join('/')===`assets/${asset.collection}/${asset.category}`,`${label}: expected assets/<collection>/<category>/<slug>`);
    requireThat(folder===join(base,'assets',asset.collection,asset.category,asset.id),`${label}: folder must match asset id`);
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
    assets.push({...asset,qa:`${label}/qa.json`});
  }catch(error){errors.push(`${relative(base,file)}: ${error.message}`);}}
  requireThat(!errors.length,`Manifest generation refused; no file was changed:\n${errors.join('\n')}`);
  return {version:1,...(preview?{review_only:true}:{}),license:'CC-BY-4.0',code_license:'MIT',author:'Leon Made This / s010s',attribution_url:'https://github.com/s010s/lowpoly-vault',assets};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
  try{const preview=process.argv.includes('--preview');const manifest=await collectManifest(process.cwd(),{preview});if(process.argv.includes('--check'))console.log(`Release gate passed: ${manifest.assets.length} assets. Manifest not changed.`);else{const destination=resolve(preview?'assets/manifest.review.json':'assets/manifest.json'),temp=`${destination}.tmp`;await writeFile(temp,JSON.stringify(manifest,null,2)+'\n');await rename(temp,destination);console.log(`Wrote ${relative(process.cwd(),destination)} with ${manifest.assets.length} ${preview?'structurally checked, review-pending':'QA-approved'} assets.`);}}
  catch(error){console.error(error.message);process.exitCode=1;}
}
