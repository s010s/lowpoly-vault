import assert from 'node:assert/strict';
import {checkLive} from './ci-live-smoke.mjs';
const sha='a'.repeat(40),model={id:'one',glb:'assets/one.glb',blend:'assets/one.blend',preview:'assets/one.png'};
function fixture({wrongSha=false,empty=false,broken=false,pathEscape=false}={}){return async(url,options)=>{
 const path=url.pathname;let value=path.endsWith('release-build.json')?{source_commit:wrongSha?'b'.repeat(40):sha,models:1,sample:[{id:'one',files:{glb:model.glb,blend:model.blend,left:'gallery/one/wheel.png',right:'gallery/one/detail.png'}}]}:{assets:empty?[]:[{...model,...(pathEscape?{glb:'https://evil.invalid/model.glb'}:{})}]};
 return {ok:!(broken&&options.method==='HEAD'),status:broken?404:200,json:async()=>value};
};}
const options={baseURL:'https://example.invalid/site/',expectedSha:sha};
assert.equal((await checkLive({...options,fetcher:fixture()})).status,'PASS');
for(const mode of ['wrongSha','empty','broken','pathEscape'])await assert.rejects(checkLive({...options,fetcher:fixture({[mode]:true})}));
await assert.rejects(checkLive({...options,expectedSha:'',fetcher:fixture()}));
console.log('PASS 6 live readback cases: current deployment, stale commit, empty catalog, missing file, path escape, missing expected SHA');
