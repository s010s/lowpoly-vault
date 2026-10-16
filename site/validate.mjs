import { readFile, stat } from 'node:fs/promises';
import assert from 'node:assert/strict';
import { collectManifest } from './generate-manifest.mjs';
const review=process.argv.includes('--review');
const manifest=review?await collectManifest(process.cwd(),{preview:true}):JSON.parse(await readFile('assets/manifest.json','utf8'));
assert(Array.isArray(manifest.assets)&&manifest.assets.length>0,'Manifest needs assets');
const ids=new Set();
for(const a of manifest.assets){assert(a.id&&!ids.has(a.id),'Unique asset ID required');ids.add(a.id);assert(a.name?.en&&a.name?.zh,'Bilingual names required');assert(a.description?.en&&a.description?.zh,'Bilingual descriptions required');assert(typeof a.category==='string'&&/^[a-z0-9-]+$/.test(a.category),'Invalid category slug');assert(a.license==='CC-BY-4.0','Expected CC-BY-4.0');assert(Number.isInteger(a.triangles)&&a.triangles>0,'Triangle count required');assert(Array.isArray(a.dimensions)&&a.dimensions.length===3&&a.dimensions.every(x=>Number.isFinite(x)&&x>0),'Dimensions required');for(const key of ['glb','blend','preview']){const p=a[key];assert(typeof p==='string'&&p.startsWith('assets/')&&!p.split('/').includes('..'),'Asset path must be repository-relative');assert((await stat(p)).size>0,`${p} is empty`);}const data=await readFile(a.glb);assert(data.toString('ascii',0,4)==='glTF'&&data.readUInt32LE(4)===2,'Expected glTF 2 binary');assert(data.readUInt32LE(8)===data.length,'GLB size mismatch');}
console.log(`${review?'Review-only structural check (no publication approval): ':''}Validated ${ids.size} original asset entries and all GLB/Blend/preview paths.`);
