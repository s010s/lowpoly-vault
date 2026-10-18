/** Fail closed on missing diff provenance; only published model IDs can select GPU work. */
import { execFileSync } from 'node:child_process';
import { readFileSync, appendFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
export function classify(paths, manifest, full = false) {
  const runtime = full || paths.some(p => /^(package(?:-lock)?\.json|vite\.config\.js)$/.test(p) || /^site\/(?!ci-|.*(?:-test|\.test)\.m?js$|.*release\.mjs$)/.test(p));
  const changed = manifest.assets.filter(a => paths.some(p => [a.glb,a.blend,a.preview].includes(p) || p.startsWith(`assets/card-previews/${a.id}-`) || p.startsWith(`assets/turntables/${a.id}/`)));
  const models = runtime || paths.includes('assets/manifest.json') || changed.length > 0;
  // Manifest updates select all published IDs: metadata and release evidence are cheap, geometry remains immutable.
  const ids = runtime || paths.includes('assets/manifest.json') ? '' : changed.map(a=>a.id).join(',');
  const previews = full || paths.some(p => /^(site\/(viewer\.js|render-preset\.js|render-web-previews\.mjs|turntable-delivery\.mjs)|assets\/(card-previews\/|turntables\/))/.test(p)) || changed.length > 0;
  const tasks = runtime ? ['models','matrix','fallback','small-life','list','shared','handoff','conifer','modal','interaction'] : models ? ['models'] : [];
  if (previews) tasks.push('previews');
  return {runtime,models,previews,ids,tasks:tasks.length ? tasks : ['none']};
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  let paths=[], full=process.env.FULL_REVIEW==='true';
  if (!full) {
    try {
      if (!/^[a-f0-9]{40}$/.test(process.env.BASE_SHA||'') || /^0+$/.test(process.env.BASE_SHA)) throw Error('Missing base');
      paths=execFileSync('git',['diff','--name-only','-z',process.env.BASE_SHA,'HEAD'],{encoding:'utf8'}).split('\0').filter(Boolean);
    } catch { full=true; console.error('Diff provenance unavailable: requiring full review.'); }
  }
  const scope=classify(paths,JSON.parse(readFileSync('assets/manifest.json')),full);
  for (const [key,value] of Object.entries(scope)) {
    const line=`${key}=${Array.isArray(value)?JSON.stringify(value):value}\n`;
    if(process.env.GITHUB_OUTPUT) appendFileSync(process.env.GITHUB_OUTPUT,line);
  }
  console.log(JSON.stringify({paths,...scope},null,2));
}
