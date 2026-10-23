/** Change scope chooses tests, never authorizes a model or an output. Unknown provenance is full. */
import {execFileSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {immutableGitEnv} from './ci-git.mjs';
import {releaseAppendFromGit} from './ci-release-fast-scope.mjs';
const contentOnlyFiles=new Set(['site/content-production-acceptance.mjs','site/content-production-acceptance-test.mjs']);
const controls=/^(?:\.github\/|scripts\/|schemas\/)|(?:^|\/)package(?:-lock)?\.json$|^site\/(?:ci-|.*release|.*acceptance|.*publication|.*registry|.*delivery|.*manifest|.*poster|.*capture|.*archive|.*audit|validate|parse-models)/;
export function classifyTests(paths,{appendOnly=false,known=true}={}){
 if(!known||!Array.isArray(paths)||!paths.length)return {mode:'full',framework:true,publication:true,website:true,reason:'Unknown or empty change scope'};
 if(paths.every(p=>contentOnlyFiles.has(p)))return {mode:'content',framework:false,publication:false,website:false,reason:'Only content acceptance implementation/tests changed; focused regressions and normal source/output gates remain required'};
 const framework=paths.some(p=>!p.startsWith('site/public/gallery/posters/')&&controls.test(p));
 const website=paths.some(p=>p.startsWith('site/')&&!['site/catalog-data.json','site/gallery/wheel-framing.json','site/public/gallery/resources.json'].includes(p)&&!p.startsWith('site/public/gallery/posters/'));
 if(appendOnly&&!framework&&!website)return {mode:'models',framework:false,publication:false,website:false,reason:'Verified append-only model data; source and final output checks still run'};
 return {mode:'full',framework,publication:framework,website:true,reason:'Changed shared or non-additive inputs select relevant regressions'};
}
export function leanScope({root=process.cwd(),env=process.env}={}){
 const full=reason=>({...classifyTests([]),reason});
 try{
  const git=(...args)=>execFileSync('git',args,{cwd:root,env:immutableGitEnv(),encoding:'utf8',maxBuffer:128*1024*1024}).trim();
  if(!env.GITHUB_EVENT_PATH)return full('No CI event');
  const event=JSON.parse(readFileSync(env.GITHUB_EVENT_PATH));let base,head;
  if(env.GITHUB_EVENT_NAME==='pull_request'){
   const pr=event.pull_request;if(pr?.base?.ref!=='main'||pr.base.repo.full_name!==env.GITHUB_REPOSITORY||pr.head.repo.full_name!==env.GITHUB_REPOSITORY)return full('Unsupported PR context');base=pr.base.sha;head=pr.head.sha;
  }else if(env.GITHUB_EVENT_NAME==='push'&&event.ref==='refs/heads/main'&&env.GITHUB_REF===event.ref&&event.repository?.full_name===env.GITHUB_REPOSITORY){base=event.before;head=event.after;}
  else return full('Unsupported event');
  const checkout=git('rev-parse','HEAD');if(![base,head,checkout].every(s=>/^[a-f0-9]{40}$/.test(s)&&!/^0+$/.test(s))||checkout!==env.GITHUB_SHA)return full('Invalid exact source identity');
  if(checkout!==head&&!(env.GITHUB_EVENT_NAME==='pull_request'&&git('show','-s','--format=%P',checkout)===`${base} ${head}`))return full('Unexpected checkout');
  if(!git('ls-files','-v').split('\n').every(line=>line.startsWith('H ')))return full('Hidden index flags require full validation');
  if(git('status','--porcelain','--untracked-files=no'))return full('Tracked inputs changed');
  git('merge-base','--is-ancestor',base,checkout);
  const paths=git('diff','--name-only','--no-renames',base,checkout).split('\n').filter(Boolean);
  const append=releaseAppendFromGit(base,{root:resolve(root),currentSha:checkout});
  return {...classifyTests(paths,{appendOnly:append.eligible}),base,head:checkout,paths,added_ids:append.added_ids};
 }catch(error){return full(error.message);}
}

export function needsGeometryRegression(paths){return !Array.isArray(paths)||paths.length===0||paths.some(p=>p.startsWith('site/gallery/')&&!['site/gallery/wheel-framing.json','site/gallery/approved-poster-inputs.json'].includes(p)||['site/viewer.js','site/curation.js','site/routes.js','site/render-preset.js','package.json','package-lock.json'].includes(p));}
