import {build} from 'vite';
import {readFile,mkdir,copyFile,writeFile,stat} from 'node:fs/promises';
import {resolve,dirname} from 'node:path';
import {createHash} from 'node:crypto';
const root=import.meta.dirname,repo=resolve(root,'../..'),out=resolve(root,'build');
const models=JSON.parse(await readFile(resolve(root,'app/models.json')));
await build({configFile:resolve(root,'vite.config.js')});
const assets=[];
for(const model of models){for(const key of ['glb','blend','preview']){const relative=model[key];if(!relative.startsWith('assets/')||relative.includes('..'))throw Error('Unsafe asset path');const source=resolve(repo,relative),target=resolve(out,relative);await mkdir(dirname(target),{recursive:true});await copyFile(source,target);assets.push({id:model.id,format:key,path:relative,bytes:(await stat(target)).size,sha256:createHash('sha256').update(await readFile(target)).digest('hex')});}}
await writeFile(resolve(out,'preview-provenance.json'),JSON.stringify({productionBase:'de413ef720463a2999516faf92c606bcdf9ab1b7',models:models.length,isolatedPreview:true,assets},null,2)+'\n');
console.log(`Isolated preview: ${out}, ${models.length} existing models. No production build was changed.`);
