/** Explicit IDs only: bind original bytes before the same-renderer wheel capture. */
import assert from 'node:assert/strict';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {wheelHash} from './wheel-presentation-contract.mjs';
const ids=(process.argv[2]||'').split(',').filter(Boolean),output=process.argv[3]||'qa/wheel-capture-inputs.json';
assert(ids.length&&new Set(ids).size===ids.length&&ids.every(id=>/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)),'Supply explicit unique asset IDs');
const manifest=JSON.parse(await readFile('assets/manifest.json')),resources=JSON.parse(await readFile('site/public/gallery/resources.json'));
const affected=manifest.assets.filter(a=>resources.posters[a.id]?.render_route==='blender-cycles-cpu-v1'&&!resources.posters[a.id]?.wheelSpec);
const assets=[];
for(const id of ids){const a=affected.find(a=>a.id===id);assert(a,'Unknown or already framed wheel: '+id);const p=resources.posters[id];const pins={id,source_glb_sha256:wheelHash(await readFile(a.glb)),previous_wheel_sha256:wheelHash(await readFile('site/public/'+p.wheel)),unchanged_detail_sha256:wheelHash(await readFile('site/public/'+p.detail))};assert.equal(pins.source_glb_sha256,a.sha256.glb);assets.push(pins);}
const scope={version:1,mode:'scoped',publication_authority:false,baseline_commit:process.env.GITHUB_SHA||null,expected_catalog_count:manifest.assets.length,expected_affected_count:affected.length,assets};
await mkdir(dirname(resolve(output)),{recursive:true});await writeFile(output,JSON.stringify(scope,null,2)+'\n');console.log('Prepared only:',ids.join(','));
