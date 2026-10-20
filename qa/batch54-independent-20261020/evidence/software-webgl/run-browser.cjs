const {chromium}=require('/workspace/lowpoly-vault/node_modules/playwright');
const crypto=require('crypto'),fs=require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-webgl','--ignore-gpu-blocklist','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
 const page=await browser.newPage({viewport:{width:2112,height:1600},deviceScaleFactor:1});
 const consoleErrors=[];page.on('pageerror',e=>consoleErrors.push(String(e)));page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text())});
 const response=await page.goto('http://127.0.0.1:4179/',{waitUntil:'networkidle',timeout:120000});
 await page.waitForFunction(()=>window.__qaReady===true,{timeout:120000});
 await page.waitForTimeout(500);
 const summary=await page.evaluate(()=>({summary:window.__qaSummary,userAgent:navigator.userAgent,webglSupported:!!document.createElement('canvas').getContext('webgl2')}));
 summary.httpStatus=response.status();summary.consoleErrors=consoleErrors;
 const screenshot='/tmp/batch54-independent-20261020/browser/webgl-review.png';await page.screenshot({path:screenshot,fullPage:true});
 summary.screenshot={path:screenshot,sha256:crypto.createHash('sha256').update(fs.readFileSync(screenshot)).digest('hex'),bytes:fs.statSync(screenshot).size};
 fs.writeFileSync('/tmp/batch54-independent-20261020/browser/runtime-report.json',JSON.stringify(summary,null,2)+'\n');
 console.log(JSON.stringify(summary,null,2));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
