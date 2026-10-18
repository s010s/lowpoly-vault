/** Real Node HTTP responses catch API shape errors before a Pages deployment. */
import {createServer} from 'node:http';
import assert from 'node:assert/strict';
import {waitForDeployedRelease} from './live-release-contract.mjs';
const expected={assets:[{id:'fixture',sha256:{glb:'a',blend:'b',preview:'c'}}]};
let requests=0;
const server=createServer((req,res)=>{
 requests++;
 if(req.url==='/delayed'&&requests===1){res.writeHead(503).end('not ready');return;}
 if(req.url==='/wrong'){res.setHeader('Content-Type','application/json');res.end(JSON.stringify({assets:[]}));return;}
 if(req.url==='/denied'){res.writeHead(403).end('denied');return;}
 res.setHeader('Content-Type','application/json');res.end(JSON.stringify(expected));
});
await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}`;
try {
 assert.deepEqual(await waitForDeployedRelease(base+'/ready',expected,{timeout:200}),expected);
 requests=0;assert.deepEqual(await waitForDeployedRelease(base+'/delayed',expected,{timeout:200,interval:5}),expected);assert.equal(requests,2);
 await assert.rejects(()=>waitForDeployedRelease(base+'/wrong',expected,{timeout:40,interval:5}),/deep-equal/);
 await assert.rejects(()=>waitForDeployedRelease(base+'/denied',expected,{timeout:40,interval:5}),/HTTP 403/);
 console.log('Actual Node HTTP Response: exact release, delayed publication, mismatched scope and 403 refusal passed.');
}finally{await new Promise(r=>server.close(r));}
