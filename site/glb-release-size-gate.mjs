/** Incremental release gate. Unchanged legacy violations remain explicit debt. */
import {execFileSync} from 'node:child_process';
import {readFile,stat,realpath} from 'node:fs/promises';
import {resolve,sep} from 'node:path';
import {MAX_GLB_BYTES,checkGlbSizes} from './glb-size-gate.mjs';
export async function checkReleaseGlbSizes({root=process.cwd(),baselineCommit,manifest}={}) {
 root=await realpath(root);
 if(!/^[a-f0-9]{40}$/.test(baselineCommit||'')) throw new Error('Explicit 40-character approved Git baseline commit required');
 const git=(...args)=>execFileSync('git',['-C',root,...args],{encoding:'utf8',maxBuffer:32*1024*1024});
 if(git('rev-parse',`${baselineCommit}^{commit}`).trim()!==baselineCommit) throw new Error('Invalid baseline commit');
 const baseline=JSON.parse(git('show',`${baselineCommit}:assets/manifest.json`));
 manifest??=JSON.parse(await readFile(resolve(root,'assets/manifest.json'),'utf8'));
 if(!Array.isArray(baseline.assets)||!baseline.assets.length||!Array.isArray(manifest.assets)||!manifest.assets.length) throw new Error('Nonempty baseline and current manifests required');
 const old=new Map(baseline.assets.map(a=>[a.id,a]));
 if(old.size!==baseline.assets.length) throw new Error('Duplicate baseline IDs');
 // Git compares actual working-tree contents against baseline, including staged changes.
 const changed=new Set([...git('diff','--name-only','-z',baselineCommit,'--').split('\0'),...git('ls-files','--others','--exclude-standard','-z').split('\0')]);
 const baselineTracked=new Set(git('ls-tree','-r','--name-only','-z',baselineCommit).split('\0'));
 const required=[],legacyOversize=[],seen=new Set();
 let unchanged=0;
 for(const a of manifest.assets){
  if(!a||typeof a.id!=='string'||!a.id||seen.has(a.id)) throw new Error('Missing or duplicate current asset ID');seen.add(a.id);
  const p=a.glb,b=old.get(a.id);
  if(typeof p!=='string'||!p.endsWith('.glb')||p.startsWith('/')||/[\\\u0000-\u001f?#%:]/.test(p)||p.split('/').some(x=>!x||x==='.'||x==='..')) throw new Error(`Unsafe GLB path: ${a.id}`);
  const full=resolve(root,p);
  if(await realpath(full)!==full||!full.startsWith(root+sep)) throw new Error(`Symlink GLB path: ${a.id}`);
  const f=await stat(full);if(!f.isFile()||!f.size) throw new Error(`Missing or empty GLB: ${a.id}`);
  const replacement=!b||b.glb!==p||b.sha256?.glb!==a.sha256?.glb||changed.has(p)||!baselineTracked.has(p);
  if(replacement)required.push(a);
  else {unchanged++;if(f.size>MAX_GLB_BYTES)legacyOversize.push({id:a.id,path:p,bytes:f.size,over_bytes:f.size-MAX_GLB_BYTES});}
 }
 const report={baseline_commit:baselineCommit,limit_bytes:MAX_GLB_BYTES,total:manifest.assets.length,changed_count:required.length,changed_ids:required.map(a=>a.id),unchanged_count:unchanged,legacy_oversize:legacyOversize,whole_site_within_budget:false};
 try {if(required.length)await checkGlbSizes({assets:required},{root});}
 catch(error){error.report={...report,status:'BLOCKED_CHANGED_ASSETS'};throw error;}
 return {...report,status:'CHANGED_ASSETS_PASS',whole_site_within_budget:legacyOversize.length===0};
}
