import assert from 'node:assert/strict';
import {mkdtemp,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {writeStaticRoutes} from './static-routes.mjs';

const asset=(id,en,zh)=>({id,name:{en,zh},description:{en:'Test model',zh:'测试模型'},category:'animals',preview:`assets/${id}.png`,glb:`assets/${id}.glb`,blend:`assets/${id}.blend`,triangles:1});
const assets=[asset('corythosaurus','Corythosaurus','冠龙'),asset('guanlong','Guanlong','冠龙'),asset('unique','Unique','独有')];
const root=await mkdtemp(join(tmpdir(),'vault-title-collision-'));
const titles=new Set();
try {
  await writeFile(join(root,'index.html'),'<!doctype html><html><head><title>Template</title></head><body></body></html>');
  await writeStaticRoutes({assets},root,{base:'/lowpoly-vault/'});
  for(const lang of ['en','zh-CN'])for(const model of assets){
    const html=await readFile(join(root,lang==='en'?'':'zh-CN','models',model.id,'index.html'),'utf8');
    const matches=[...html.matchAll(/<title>([\s\S]*?)<\/title>/g)];
    assert.equal(matches.length,1);
    const title=matches[0][1],name=model.name[lang==='en'?'en':'zh'];
    const expectedName=lang==='zh-CN'&&model.id!=='unique'?`${name} (${model.id})`:name;
    assert.equal(title,`${expectedName} · ${lang==='en'?'Low-poly 3D model':'低多边形 3D 模型'} | Lowpoly Vault`);
    assert(!titles.has(title),'Keep all route titles unique');titles.add(title);
    assert(html.includes(`<meta property="og:title" content="${title}">`),'Open Graph matches route title');
    assert(html.includes(`<h1>${name}</h1>`),'Visible/scientific name remains unchanged');
  }
  console.log('PASS: six detail routes; Chinese collisions disambiguated; English and non-colliding Chinese titles unchanged; unique title assertion retained; names unchanged.');
} finally {await rm(root,{recursive:true,force:true});}
