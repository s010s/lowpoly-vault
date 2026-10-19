import shell from './shell.html?raw';
import {loadGalleryCatalog} from './catalog-source.js';
// Retain the useful, real SSG document if the catalog or enhancement fails.
const previous=[...document.body.childNodes];
const loadingStyle=document.createElement('style');loadingStyle.textContent='body.gallery-loading > :not(#static-route-content){display:none!important}';document.head.append(loadingStyle);document.body.classList.add('gallery-loading');
try {
  await loadGalleryCatalog();
  const fragment=document.createElement('template');fragment.innerHTML=shell;
  document.body.replaceChildren(fragment.content.cloneNode(true));
  document.body.dataset.gallery='approved-v55';document.body.classList.remove('gallery-loading');loadingStyle.remove();
  document.documentElement.dataset.theme='light';
  await import('./main.js');document.body.classList.remove('gallery-loading');loadingStyle.remove();
} catch(error) {
  console.error('Gallery enhancement unavailable',error);
  document.body.replaceChildren(...previous);
  delete document.body.dataset.gallery;document.head.append(loadingStyle);document.body.classList.add('gallery-loading');
  document.querySelector('#static-route-content')?.removeAttribute('hidden');
  const status=document.createElement('p');status.setAttribute('role','status');status.className='gallery-load-error';
  status.textContent=document.documentElement.lang==='zh-CN'?'交互视图暂不可用，仍可浏览下方模型并下载文件。':'The interactive view is unavailable. You can still browse the models and download their files below.';
  document.querySelector('#static-route-content')?.prepend(status);
}
