/** Release byte budget. This is not visual or model-quality acceptance. */
import {realpath,stat,readFile} from 'node:fs/promises';
import {resolve,sep} from 'node:path';
import {pathToFileURL} from 'node:url';
export const MAX_GLB_BYTES = 5_000_000;
export async function checkGlbSizes(manifest,{root=process.cwd()}={}) {
 if(!Array.isArray(manifest?.assets)||!manifest.assets.length) throw new Error('GLB size gate: nonempty assets manifest required');
 root=await realpath(root);
 const failures=[],models=[],ids=new Set();
 for(const asset of manifest.assets){
  const id=asset?.id,path=asset?.glb;
  try {
   if(typeof id!=='string'||!id||ids.has(id)) throw new Error('missing or duplicate asset ID');
   ids.add(id);
   if(typeof path!=='string'||!path.endsWith('.glb')||path.startsWith('/')||/[\\\u0000-\u001f?#%:]/.test(path)||path.split('/').some(p=>!p||p==='.'||p==='..')) throw new Error('unsafe or non-GLB path');
   const full=resolve(root,path),actual=await realpath(full);
   if(!actual.startsWith(root+sep)||actual!==full) throw new Error('symlink or path outside release root');
   const file=await stat(full);
   if(!file.isFile()||file.size===0) throw new Error('not a nonempty regular file');
   if(file.size>MAX_GLB_BYTES) throw new Error(`${file.size} bytes exceeds ${MAX_GLB_BYTES} bytes by ${file.size-MAX_GLB_BYTES} bytes`);
   models.push({id,path,bytes:file.size});
  }catch(error){failures.push(`${id??'<missing ID>'} (${path??'<missing path>'}): ${error.message}`);}
 }
 if(failures.length) throw new Error(`GLB size gate failed (${failures.length}/${manifest.assets.length}); limit ${MAX_GLB_BYTES} bytes per file:\n${failures.join('\n')}`);
 return {count:models.length,limit_bytes:MAX_GLB_BYTES,models};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 try {const result=await checkGlbSizes(JSON.parse(await readFile('assets/manifest.json','utf8')));console.log(`GLB size gate passed: ${result.count} files, each <= ${result.limit_bytes} bytes.`);}
 catch(error){console.error(error.message);process.exitCode=1;}
}
