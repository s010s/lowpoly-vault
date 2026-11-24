import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {mkdir,mkdtemp,rm,symlink,writeFile} from 'node:fs/promises';
import {dirname,join} from 'node:path';
import {tmpdir} from 'node:os';
import {BASE_URL,BASELINE_SHA,inspectCandidate,createDistFetcher} from './ci-release-delivery-candidate.mjs';
const sha=x=>createHash('sha256').update(x).digest('hex'), rev='a'.repeat(40), zip=sha('ZIP');
async function fx(t){
 const root=await mkdtemp(join(tmpdir(),'candidate-dist-')),dist=join(root,'dist');
 t.after(()=>rm(root,{recursive:true,force:true}));
 const w=async(path,data)=>{const f=join(dist,path);await mkdir(dirname(f),{recursive:true});await writeFile(f,typeof data==='string'?data:JSON.stringify(data));};
 const glb='assets/model.glb', bundle='assets/downloads/fixture-'+zip.slice(0,16)+'.zip';
 const poster={wheel:'gallery/fixture-wheel.png',detail:'gallery/fixture.png'};
 const manifest={assets:[{id:'fixture',glb,blend:'assets/model.blend',name:{en:'Fixture',zh:'模型'},zipVersioned:true,downloads:{bundle},galleryPosters:poster,sha256:{glb:sha('GLB'),bundle:zip,blend:sha('blend')},file_sizes:{glb:3,bundle:3}}]};
 const resources={posters:{fixture:poster},files:Object.values(poster).map(path=>({path,bytes:3,sha256:sha('PNG')}))};
 const gallery='assets/gallery-'+rev+'.json';
 await w('release-build.json',{source_commit:rev,models:1,gallery_path:gallery,catalog_path:'assets/catalog-'+rev+'.json'});
 await w('assets/manifest.json',manifest);await w(gallery,manifest);await w(glb,'GLB');await w(bundle,'ZIP');
 for(const path of Object.values(poster))await w(path,'PNG');
 const html=name=>'<h1>'+name+'</h1><a href="/lowpoly-vault/'+glb+'">GLB</a><a href="/lowpoly-vault/'+bundle+'">ZIP</a><a href="https://creativecommons.org/licenses/by/4.0/">CC</a>';
 await w('models/fixture/index.html',html('Fixture'));
 await w('zh-CN/models/fixture/index.html',html('模型'));
 const git=(...args)=>{const [op,path]=args;if(op==='rev-parse'){assert.equal(path,'HEAD');return rev;}assert.equal(op,'show');if(path===BASELINE_SHA+':assets/manifest.json')return JSON.stringify({assets:[]});if(path===rev+':assets/manifest.json')return JSON.stringify(manifest);assert.equal(path,rev+':site/public/gallery/resources.json');return JSON.stringify(resources);};
 return {options:{root,expectedSha:rev,git},dist,w,glb,bundle,poster,manifest};
}
test('candidate verifier checks actual file and bilingual pages, reports local only',async t=>{
 const f=await fx(t);const r=await inspectCandidate(f.options);assert.equal(r.status,'PASS');assert.equal(r.evidence,'LOCAL_BUILT_DIST');assert.equal(r.models[0].pages.length,2);assert.equal(r.models[0].bundle.sha256,zip);
});
test('wrong checkout or built marker is refused before reading GLB',async t=>{
 const f=await fx(t);await assert.rejects(inspectCandidate({...f.options,expectedSha:'b'.repeat(40)}),/not exact candidate/);
 await f.w('release-build.json',{source_commit:'b'.repeat(40),models:1});await assert.rejects(inspectCandidate(f.options),/Deployment not yet current/);
 await f.w('release-build.json',{source_commit:rev,models:1,gallery_path:'assets/wrong.json'});await assert.rejects(inspectCandidate(f.options),/Wrong gallery release path/);
});
for(const key of ['glb','bundle','poster'])test('same-length '+key+' corruption fails actual built contract',async t=>{
 const f=await fx(t);await f.w(key==='poster'?f.poster.wheel:f[key],'BAD');
 assert.equal((await inspectCandidate(f.options)).models[0].error_kind,'CONTENT_HASH_MISMATCH');
});
test('Chinese route must contain actual selected GLB link',async t=>{
 const f=await fx(t);await f.w('zh-CN/models/fixture/index.html','<h1>模型</h1>');assert.match((await inspectCandidate(f.options)).models[0].error,/GLB link missing/);
});
test('adapter rejects encoded separators, foreign URLs, wrong versions and symlinks',async t=>{
 const f=await fx(t), get=await createDistFetcher({dist:f.dist,expectedSha:rev}), q='?deployment='+rev;
 for(const path of ['assets%2fmodel.glb','assets/%252e%252e/x','assets/../../x','assets/model.glb?extra=1&bad='])await assert.rejects(get(new URL(path+q,BASE_URL)));
 await assert.rejects(get(new URL('https://example.test/lowpoly-vault/x'+q)));
 await symlink(join(f.dist,f.glb),join(f.dist,'alias.glb'));
 await assert.rejects(get(new URL('alias.glb'+q,BASE_URL)),/Non-regular/);
 assert.equal((await get(new URL('missing.glb'+q,BASE_URL))).status,404);
});

test('rejects raw dot normalization in adapter strings and source metadata before constructing URL', async t=>{
 const f=await fx(t), get=await createDistFetcher({dist:f.dist,expectedSha:rev}),q='?deployment='+rev;
 for(const suffix of ['assets/./model.glb','assets/%2e/model.glb','assets/local/../model.glb']) await assert.rejects(get(BASE_URL+suffix+q),/Unsafe raw/);
 f.manifest.assets[0].glb='assets/%2e/model.glb';
 await assert.rejects(inspectCandidate(f.options),/Unsafe raw/);
});
