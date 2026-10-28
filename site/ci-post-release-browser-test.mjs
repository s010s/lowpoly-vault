/** Real Chromium regression fixtures for entry-body lifecycle and the 160 ms UI handoff.
 * No production records, deployment proof, or model bytes are changed by these tests. */
import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {createHash} from 'node:crypto';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';
import {EventEmitter} from 'node:events';
import {createRuntimeEntryAudit,createCDPRuntimeEntryAudit,createRuntimeEntryAuditFromCDPSession} from './ci-post-release-browser.mjs';
import {runThumbnailRevealBrowserTests} from './gallery-thumbnail-reveal-browser-test.mjs';
const output=resolve(process.env.QA_OUTPUT_DIR||'qa/post-release-browser-regression');await mkdir(output,{recursive:true});
// Deterministic queue contract cases execute without Chromium. They are not
// reported as an actual-browser result when the browser environment is blocked.
async function queueContracts(){
 const rows=[],body=Buffer.from('actual browser response'),pin={path:'entry.js',bytes:body.length,sha256:createHash('sha256').update(body).digest('hex')};
 async function test(name,fn){await fn();rows.push({name,status:'PASS'});}
 function fixture({files=[pin],read=async()=>body,ok=true,status=ok?200:404,timeoutMs=1000}={}){const page=new EventEmitter(),report={entry_errors:[],loaded_entries:[]},request={url:()=> 'https://fixture.invalid/app/entry.js',failure:()=>({errorText:'ABORTED'})},response={request:()=>request,ok:()=>ok,status:()=>status,body:read},audit=createRuntimeEntryAudit(page,{base:'https://fixture.invalid/app/',files,report,timeoutMs});return {page,report,request,response,audit,emit(){page.emit('request',request);page.emit('response',response);}};}
 await test('pending-body-must-settle-before-drain',async()=>{let release;const x=fixture({read:()=>new Promise(r=>release=r)});x.emit();let complete=false;const wait=x.audit.drain().then(()=>complete=true);await new Promise(r=>setTimeout(r,20));assert.equal(complete,false);assert.deepEqual(x.report.loaded_entries,[]);release(body);await wait;assert.deepEqual(x.report.loaded_entries,['entry.js']);x.audit.detach();assert.equal(x.page.listenerCount('response'),0);});
 for(const [name,options,pattern] of [
  ['reject-wrong-hash',{files:[{...pin,sha256:'0'.repeat(64)}]},/hash differs/],
  ['reject-wrong-size',{files:[{...pin,bytes:pin.bytes+1}]},/size differs/],
  ['reject-unknown-entry',{files:[]},/Unexpected runtime entry/],
  ['reject-HTTP-failure',{ok:false},/HTTP 404/],
  ['reject-unreadable-CDP-body',{read:async()=>{throw Error('Network.getResponseBody missing');}},/Network.getResponseBody/]
 ])await test(name,async()=>{const x=fixture(options);x.emit();await assert.rejects(()=>x.audit.drain());assert.match(x.report.entry_errors.join(' '),pattern);assert.deepEqual(x.report.loaded_entries,[]);x.audit.detach();});
 await test('conditional-304-still-requires-the-actual-complete-marker-body',async()=>{const x=fixture({ok:false,status:304});x.emit();await x.audit.drain();assert.deepEqual(x.report.loaded_entries,['entry.js']);x.audit.detach();});
 for(const [name,options,pattern] of [
  ['304-empty-body',{read:async()=>Buffer.alloc(0)},/size differs/],
  ['304-wrong-hash',{files:[{...pin,sha256:'0'.repeat(64)}]},/hash differs/],
  ['304-wrong-size',{files:[{...pin,bytes:pin.bytes+1}]},/size differs/],
  ['304-unreadable-body',{read:async()=>{throw Error('Missing cached CDP body');}},/Missing cached CDP body/],
  ['304-unknown-entry',{files:[]},/Unexpected runtime entry/],
  ['other-redirect-remains-rejected',{status:302},/HTTP 302/]
 ])await test(name,async()=>{const x=fixture({ok:false,status:304,...options});x.emit();await assert.rejects(()=>x.audit.drain());assert.match(x.report.entry_errors.join(' '),pattern);assert.deepEqual(x.report.loaded_entries,[]);x.audit.detach();});
 await test('reject-unfinished-request-without-response',async()=>{const x=fixture({timeoutMs:20});x.page.emit('request',x.request);await assert.rejects(()=>x.audit.drain(),/Unfinished runtime entries/);assert.deepEqual(x.report.loaded_entries,[]);x.page.emit('requestfailed',x.request);await assert.rejects(()=>x.audit.drain(),/Actual loaded entry verification failed/);x.audit.detach();});
 await test('requests-arriving-while-draining-are-also-awaited',async()=>{let releaseA,releaseB;const x=fixture({read:()=>new Promise(r=>releaseA=r)});x.emit();const requestB={...x.request},responseB={...x.response,request:()=>requestB,body:()=>new Promise(r=>releaseB=r)};let done=false;const waiting=x.audit.drain().then(()=>done=true);x.page.emit('request',requestB);x.page.emit('response',responseB);releaseA(body);await new Promise(r=>setTimeout(r,10));assert.equal(done,false);releaseB(body);await waiting;assert.equal(x.report.loaded_entries.length,2);x.audit.detach();});
 return rows;
}
async function cdpQueueContracts(){
 const rows=[],body=Buffer.from('actual same CDP request entity'),pin={path:'entry.js',bytes:body.length,sha256:createHash('sha256').update(body).digest('hex')};
 async function test(name,fn){await fn();rows.push({name,status:'PASS'});}
 async function fixture({files=[pin],read=async()=>({body:body.toString(),base64Encoded:false}),timeoutMs=1000}={}){
  const session=new EventEmitter(),calls=[],report={entry_errors:[],loaded_entries:[]};let detached=false;
  session.send=async(method,params)=>{calls.push({method,params});if(method==='Network.enable')return{};assert.equal(method,'Network.getResponseBody');return read(params.requestId);};session.detach=async()=>{detached=true;};
  const audit=await createRuntimeEntryAuditFromCDPSession(session,{base:'https://fixture.invalid/app/',files,report,timeoutMs});
  const request=(id='current-1',url='https://fixture.invalid/app/entry.js',extra={})=>session.emit('Network.requestWillBeSent',{requestId:id,request:{url},...extra});
  const response=(id='current-1',status=200,url='https://fixture.invalid/app/entry.js')=>session.emit('Network.responseReceived',{requestId:id,response:{status,url}});
  const finish=(id='current-1')=>session.emit('Network.loadingFinished',{requestId:id});
  return{session,calls,report,audit,request,response,finish,detached:()=>detached};
 }
 for(const status of[200,304])await test('cdp-same-request-full-entity-'+status,async()=>{const x=await fixture({read:async id=>{assert.equal(id,'current-1');return{body:body.toString('base64'),base64Encoded:true};}});x.request();x.response('current-1',status);x.finish();await x.audit.drain();assert.deepEqual(x.report.loaded_entries,['entry.js']);assert.deepEqual(x.calls,[{method:'Network.enable',params:undefined},{method:'Network.getResponseBody',params:{requestId:'current-1'}}]);assert.equal(x.report.entry_body_evidence[0].request_id,'current-1');await x.audit.detach();assert(x.detached());assert.equal(x.session.eventNames().length,0);});
 await test('cdp-loading-finished-body-must-complete-before-drain',async()=>{let release;const x=await fixture({read:()=>new Promise(r=>release=r)});x.request();x.response();assert.equal(x.calls.length,1);x.finish();let done=false;const wait=x.audit.drain().then(()=>done=true);await new Promise(r=>setTimeout(r,10));assert(!done);assert.deepEqual(x.report.loaded_entries,[]);release({body:body.toString(),base64Encoded:false});await wait;assert(done);await x.audit.detach();});
 const negatives=[
  ['unknown-pin',{files:[]},x=>{x.request();x.response();x.finish();},/Unexpected runtime entry/],
  ['wrong-hash',{files:[{...pin,sha256:'0'.repeat(64)}]},x=>{x.request();x.response();x.finish();},/hash differs/],
  ['wrong-size',{files:[{...pin,bytes:pin.bytes+1}]},x=>{x.request();x.response();x.finish();},/size differs/],
  ['304-empty',{read:async()=>({body:'',base64Encoded:false})},x=>{x.request();x.response('current-1',304);x.finish();},/size differs/],
  ['304-unreadable',{read:async()=>{throw Error('No same-request cached entity');}},x=>{x.request();x.response('current-1',304);x.finish();},/No same-request/],
  ['invalid-body-shape',{read:async()=>({body:body.toString()})},x=>{x.request();x.response();x.finish();},/boolean/],
  ['redirect-302',{},x=>{x.request();x.response('current-1',302);x.finish();},/HTTP 302/],
  ['HTTP-404',{},x=>{x.request();x.response('current-1',404);x.finish();},/HTTP 404/],
  ['unbound-response',{},x=>{x.response();x.finish();},/Unbound runtime response/],
  ['wrong-response-url',{},x=>{x.request();x.response('current-1',200,'https://fixture.invalid/app/entry.js?other');x.finish();},/URL differs/],
  ['redirect-request',{},x=>x.request('current-1',undefined,{redirectResponse:{status:302}}),/redirect/],
  ['requestId-reuse',{},x=>{x.request();x.request();},/requestId reused/],
  ['duplicate-response',{},x=>{x.request();x.response();x.response();},/Duplicate runtime response/],
  ['finished-without-response',{},x=>{x.request();x.finish();},/finished without response/],
  ['request-failed',{},x=>{x.request();x.session.emit('Network.loadingFailed',{requestId:'current-1',errorText:'ABORTED'});},/ABORTED/],
  ['pending-request',{timeoutMs:20},x=>x.request(),/Unfinished runtime entries/]
 ];
 for(const[name,options,emit,pattern]of negatives)await test('cdp-reject-'+name,async()=>{const x=await fixture(options);emit(x);await assert.rejects(()=>x.audit.drain(),name==='pending-request'?pattern:undefined);if(name!=='pending-request')assert.match(x.report.entry_errors.join(' '),pattern);assert.deepEqual(x.report.loaded_entries,[]);await x.audit.detach();});
 await test('cdp-same-url-concurrent-requests-never-substitute-previous-body',async()=>{const x=await fixture({read:async id=>({body:id==='current-1'?body.toString():'wrong-current-2',base64Encoded:false})});for(const id of['current-1','current-2']){x.request(id);x.response(id,304);x.finish(id);}await assert.rejects(()=>x.audit.drain());assert.deepEqual(x.report.loaded_entries,['entry.js']);assert.deepEqual(x.calls.filter(c=>c.method==='Network.getResponseBody').map(c=>c.params.requestId),['current-1','current-2']);assert.equal(x.report.entry_body_evidence.length,1);await x.audit.detach();});
 return rows;
}

const queue_cases=[...await queueContracts(),...await cdpQueueContracts()];
const runtimeSource=await readFile(new URL('./ci-post-release-browser.mjs',import.meta.url),'utf8'),publicSource=await readFile(new URL('./detail-presentation-browser-test.mjs',import.meta.url),'utf8');
assert.match(runtimeSource,/const entries=await createCDPRuntimeEntryAudit/);
assert.match(runtimeSource,/finally\{try\{await entries.drain\(\);\}finally\{await entries.detach\(\);await context.close\(\);\}\}/);
assert(publicSource.includes("const {createCDPRuntimeEntryAudit:createRuntimeEntryAudit}=await import('./ci-post-release-browser.mjs');"));
assert(publicSource.includes('audits.set(page,await entryAudit(page,{base:url,files:deployedMarker.files,report}))'));
assert(publicSource.includes('await audits.get(page)?.drain();await audits.get(page)?.detach();await page.context().close();'));
queue_cases.push({name:'both-public-consumers-await-CDP-initialization-and-exact-body-drain',status:'PASS'});

if(process.env.QA_QUEUE_CONTRACT_ONLY==='1'){const result={status:'PASS',scope:'Deterministic event/response lifecycle contracts only; Chromium NOT_RUN.',cases:queue_cases};await writeFile(resolve(output,'report.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));process.exit(0);}

// Real JS response bytes. Body completion is controlled explicitly below.
// Fetch exposes the stream without waiting for classic-script compilation at EOF.
const bytes=Buffer.from('/*'+ 'streaming-fixture '.repeat(2048)+'*/\nwindow.fixtureLoaded = true;\n'),hash=b=>createHash('sha256').update(b).digest('hex');
const report={status:'RUNNING',scope:'Real local Chromium fixtures, not public deployment acceptance.',cases:queue_cases};
let browser;const contexts=[];let heldResponse,releaseHeldBody;let conditional304Count=0;
const server=createServer((req,res)=>{const u=new URL(req.url,'http://fixture');
 if(u.pathname==='/page'){res.setHeader('Content-Type','text/html');res.end(`<script src="/entry.js?mode=${u.searchParams.get('mode')||'normal'}"></script>`);return;}
 if(u.pathname==='/away'){res.end('<p>away</p>');return;}
 if(u.pathname==='/entry.js'){
  res.setHeader('Content-Type','text/javascript');res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Cache-Control','public,max-age=3600');
  const mode=u.searchParams.get('mode');
  if(mode==='conditional'){res.setHeader('ETag','"exact-browser-entry-v1"');res.setHeader('Cache-Control','no-cache');if(req.headers['if-none-match']==='"exact-browser-entry-v1"'){conditional304Count++;res.writeHead(304);res.end();return;}}
  if(mode==='404'){res.writeHead(404);res.end('missing');return;}
  if(mode==='reset'){req.socket.destroy();return;}
  if(mode==='slow'||mode==='hold'){
   res.setHeader('Content-Length',bytes.length);res.writeHead(200);res.flushHeaders();res.write(bytes.subarray(0,-1));
   if(mode==='slow'){heldResponse=res;releaseHeldBody=()=>{assert.equal(res.writableEnded,false);res.end(bytes.subarray(-1));};}
   return;
  }
  res.end(bytes);return;
 }
 res.writeHead(404).end();
});
await new Promise(done=>server.listen(0,'127.0.0.1',done));const base=`http://127.0.0.1:${server.address().port}/`;
const pins=[{path:'entry.js',bytes:bytes.length,sha256:hash(bytes)}];
try{
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox','--disable-dev-shm-usage']});report.browser=browser.version();
 async function fixture(name,fn){const context=await browser.newContext();contexts.push(context);const page=await context.newPage();const result={entry_errors:[],loaded_entries:[]};let audit;
  try{await fn({page,result,observe:async(files=pins,timeoutMs=3000)=>audit=await createCDPRuntimeEntryAudit(page,{base,files,report:result,timeoutMs})});report.cases.push({name,status:'PASS',...result});}
  finally{await audit?.detach();await context.close();}
 }
 // Observe a real browser fetch, not a classic-script loader that may withhold
 // its response event until compilation/EOF and deadlock the release handshake.
 // Actual script navigation/cache coverage remains in the following fixture.
 async function streamEntry(page,mode){
  await page.goto(base+'away');
  const first=await page.evaluate(async mode=>{
   const response=await fetch('/entry.js?mode='+mode),reader=response.body.getReader(),first=await reader.read();
   // Reading a genuine non-final browser chunk is the handshake. Do not make
   // release depend on the classic-script loader's separate response event.
   window.fixtureFetch=(async()=>{const chunks=[first.value];for(;;){const next=await reader.read();if(next.done)break;chunks.push(next.value);}return new TextDecoder().decode(await new Blob(chunks).arrayBuffer());})();
   // The unfinished negative closes its context; the unchanged audit owns
   // rejection of unfinished, unreadable, wrong-size and wrong-hash bodies.
   void window.fixtureFetch.catch(()=>{});
   return {status:response.status,done:first.done,bytes:first.value?.byteLength||0};
  },mode);
  assert.equal(first.status,200);assert.equal(first.done,false);assert(first.bytes>0&&first.bytes<bytes.length);return first;
 }
 await fixture('held-actual-response-cannot-finish-before-explicit-release',async({page,result,observe})=>{
  const audit=await observe();await streamEntry(page,'slow');
  assert(heldResponse&&releaseHeldBody,'The genuine streaming response must be held by the server');
  assert.equal(heldResponse.writableEnded,false);
  let settled=false;const draining=audit.drain();void draining.then(()=>{settled=true;},()=>{settled=true;});
  // A real controller/browser round trip lets premature resolutions surface.
  // The server cannot finish the body until this test explicitly releases it.
  await page.evaluate(()=>Promise.resolve('held-body-controller-barrier'));
  assert.equal(heldResponse.writableEnded,false);assert.equal(settled,false,'Drain must remain pending while the actual body is held');
  assert.deepEqual(result.loaded_entries,[]);releaseHeldBody();await draining;
  assert.equal(heldResponse.writableEnded,true);assert.deepEqual(result.loaded_entries,['entry.js']);
  assert.equal(await page.evaluate(()=>window.fixtureFetch),bytes.toString(),'The actual browser must receive the complete exact body');
  await page.goto(base+'away');
 });
 await fixture('cached-navigation-and-reload-retain-exact-bodies',async({page,result,observe})=>{const audit=await observe();for(let i=0;i<4;i++){await audit.drain();await page.goto(base+'page');await audit.drain();await page.reload();}await audit.drain();assert.equal(result.loaded_entries.length,8);assert.deepEqual(result.entry_errors,[]);});
 await fixture('conditional-cache-304-keeps-actual-exact-browser-bodies',async({page,result,observe})=>{const before=conditional304Count,audit=await observe();for(let i=0;i<3;i++){await audit.drain();await page.goto(base+'page?mode=conditional');await audit.drain();await page.reload();}await audit.drain();assert(conditional304Count>before,'Server must actually receive conditional requests and return 304');assert.equal(result.loaded_entries.length,6);assert.deepEqual(result.entry_errors,[]);assert.equal(await page.evaluate(()=>window.fixtureLoaded),true);});
 for(const [name,files,mode,pattern] of [
  ['wrong-hash-is-rejected',[{...pins[0],sha256:'0'.repeat(64)}],'normal',/hash differs/],
  ['wrong-size-is-rejected',[{...pins[0],bytes:bytes.length+1}],'normal',/size differs/],
  ['unknown-entry-is-rejected',[],'normal',/Unexpected runtime entry/],
  ['missing-entry-is-rejected',pins,'404',/HTTP 404/],
  ['failed-request-is-rejected',pins,'reset',/ERR_EMPTY_RESPONSE/]
 ])await fixture(name,async({page,result,observe})=>{const audit=await observe(files);await page.goto(base+'page?mode='+mode);await assert.rejects(()=>audit.drain());assert.match(result.entry_errors.join('\n'),pattern);assert.equal(result.loaded_entries.length,0);});
 await fixture('unfinished-response-cannot-pass',async({page,result,observe})=>{const audit=await observe(pins,60);await streamEntry(page,'hold');await assert.rejects(()=>audit.drain(),/Unfinished runtime entries: entry.js/);assert.equal(result.loaded_entries.length,0);});
 // Simulate protocol eviction on a genuine browser response. It must remain a
 // hard failure, never be replaced by a fresh API request or ignored catch.
 await fixture('unreadable-browser-body-cannot-pass',async({page,result,observe})=>{const context=page.context(),original=context.newCDPSession.bind(context);context.newCDPSession=async target=>{const session=await original(target),send=session.send.bind(session);session.send=(method,params)=>method==='Network.getResponseBody'?Promise.reject(Error('Network.getResponseBody: No resource with given identifier found')):send(method,params);return session;};const audit=await observe();await page.goto(base+'page');await assert.rejects(()=>audit.drain());assert.match(result.entry_errors.join('\n'),/Network.getResponseBody/);assert.equal(result.loaded_entries.length,0);});
 const run=process.env.QA_ORIGINAL_THUMBNAIL_SCRIPT?(await import(pathToFileURL(resolve(process.env.QA_ORIGINAL_THUMBNAIL_SCRIPT)))).runThumbnailRevealBrowserTests:runThumbnailRevealBrowserTests;
 // Introduce a 250 ms controller round trip around the fragile handoff. The
 // image's real 160 ms CSS transition still runs inside Chromium, unchanged.
 const delayedBrowser=new Proxy(browser,{get(target,key){if(key==='newContext')return async(...args)=>{const context=await target.newContext(...args);return new Proxy(context,{get(ctx,k){if(k==='newPage')return async()=>{const page=await ctx.newPage(),evaluate=page.evaluate.bind(page);page.evaluate=async(fn,arg)=>{const result=await evaluate(fn,arg);if(String(fn).includes('resolvers[7]'))await new Promise(done=>setTimeout(done,250));return result;};return page;};const value=ctx[k];return typeof value==='function'?value.bind(ctx):value;}});};const value=target[key];return typeof value==='function'?value.bind(target):value;}});
 const thumbnail=await run({browser:delayedBrowser,output:resolve(output,'thumbnail')});
 if(process.env.QA_ORIGINAL_THUMBNAIL_SCRIPT){assert.equal(thumbnail.status,'fail');assert.match(thumbnail.failure,/Exercise hover during a running arrival transition/);report.cases.push({name:'original-controller-race-reproduced',status:'PASS'});}
 else{assert.equal(thumbnail.status,'pass',thumbnail.failure);const handoff=thumbnail.cases.find(c=>c.name==='hover-during-arrival-cancels-only-ui-fade');assert(handoff);assert.equal(handoff.handoff.running,true);assert(handoff.handoff.arrivalOpacity>0&&handoff.handoff.arrivalOpacity<1);report.cases.push({name:'all-thumbnail-fixtures-with-controller-delay',status:'PASS',checks:thumbnail.cases.length,handoff:handoff.handoff});}
 // Navigation and closure consume the queue; no late-only Promise.all remains.
 const source=await readFile(new URL('./ci-post-release-browser.mjs',import.meta.url),'utf8');assert.match(source,/const navigate=async url=>\{await entries.drain\(\);return page.goto\(url\);\}/);assert.match(source,/const reload=async\(\)=>\{await entries.drain\(\);return page.reload\(\);\}/);assert.match(source,/finally\{try\{await entries.drain\(\);\}finally\{await entries.detach\(\);await context.close\(\);\}\}/);report.status='PASS';
}catch(error){report.status='FAIL';report.error=error.stack;process.exitCode=1;}
finally{await Promise.all(contexts.map(c=>c.close().catch(()=>{})));await browser?.close();server.closeAllConnections();await new Promise(done=>server.close(done));await writeFile(resolve(output,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));}
