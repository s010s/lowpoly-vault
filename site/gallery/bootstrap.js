import shell from './shell.html?raw';
import {loadGalleryCatalog} from './catalog-source.js';
// Retain the useful, real SSG document if the catalog or enhancement fails.
const previous=[...document.body.childNodes];
const previousTheme=document.documentElement.dataset.theme;
const loadingStyle=document.createElement('style');loadingStyle.textContent='body.gallery-loading > :not(#static-route-content){display:none!important}';document.head.append(loadingStyle);document.body.classList.add('gallery-loading');
try {
  // The linked preview already uses the approved gallery composition. Keep it
  // usable while code, CSS or catalog is delayed; swap only when ready.
  // The module has no DOM side effects until mountGallery is called below.
  const [{mountGallery}]=await Promise.all([import('./main.js'),loadGalleryCatalog()]);
  const fragment=document.createElement('template');fragment.innerHTML=shell;
  document.dispatchEvent?.(new Event('gallery-mount'));
  document.body.replaceChildren(fragment.content.cloneNode(true));
  document.body.dataset.gallery='approved-v55';document.body.classList.remove('gallery-loading');loadingStyle.remove();
  document.documentElement.dataset.theme='light';
  await mountGallery();document.body.classList.remove('gallery-loading');loadingStyle.remove();
} catch(error) {
  console.error('Gallery enhancement unavailable',error);
  document.body.replaceChildren(...previous);
  document.dispatchEvent?.(new Event('gallery-restore'));
  delete document.body.dataset.gallery;document.head.append(loadingStyle);document.body.classList.add('gallery-loading');
  if(previousTheme)document.documentElement.dataset.theme=previousTheme;
  document.querySelector('#static-route-content')?.removeAttribute('hidden');
  const status=document.createElement('p');status.setAttribute('role','status');status.className='gallery-load-error';
  status.textContent=document.documentElement.lang==='zh-CN'?'交互视图暂不可用，仍可打开模型详情并下载文件。':'The interactive view is unavailable. You can still open model details and download their files.';
  document.querySelector('#static-route-content')?.append(status);
}
