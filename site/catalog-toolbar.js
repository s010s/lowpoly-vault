/** Quiet, accessible catalog tools. Search remains the original catalog input. */
export function createCatalogToolbar({root,search,modes,language}){
 const svg=path=>`<svg viewBox="0 0 20 20" aria-hidden="true">${path}</svg>`;
 const icons={atlas:svg('<path d="m2.5 5 5-2 5 2 5-2v12l-5 2-5-2-5 2Zm5-2v12m5-10v12"/>'),grid:svg('<rect x="3" y="3" width="5" height="5" rx=".7"/><rect x="12" y="3" width="5" height="5" rx=".7"/><rect x="3" y="12" width="5" height="5" rx=".7"/><rect x="12" y="12" width="5" height="5" rx=".7"/>')};
 modes.querySelectorAll('button').forEach(b=>b.innerHTML=icons[b.dataset.mode]+'<span></span>');modes.setAttribute('role','group');
 const wrap=document.createElement('div');wrap.className='catalog-search';const label=search.closest('.search');label.before(wrap);wrap.append(label);
 const toggle=document.createElement('button');toggle.type='button';toggle.className='search-trigger';toggle.id='search-trigger';toggle.setAttribute('aria-controls','catalog-search-field');toggle.innerHTML=svg('<circle cx="8.5" cy="8.5" r="5.5"/><path d="m12.5 12.5 4 4"/>')+'<span></span><kbd aria-hidden="true">/</kbd>';wrap.prepend(toggle);label.id='catalog-search-field';
 const clear=document.createElement('button');clear.type='button';clear.className='search-dismiss';clear.innerHTML=svg('<path d="m6 6 8 8m0-8-8 8"/>');wrap.append(clear);label.querySelector('kbd')?.remove();
 let expanded=false;
 function setExpanded(value,{focus=false}={}){expanded=value;wrap.classList.toggle('is-expanded',value);label.hidden=!value;clear.hidden=!value;toggle.ariaExpanded=String(value);if(focus)(value?search:toggle).focus({preventScroll:true});}
 function open(){setExpanded(true,{focus:true});}
 toggle.onclick=()=>expanded&&!search.value?setExpanded(false,{focus:true}):open();
 function dismiss(){if(search.value){search.value='';search.dispatchEvent(new Event('input',{bubbles:true}));}setExpanded(false,{focus:true});}
 clear.onclick=dismiss;search.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();dismiss();}});
 wrap.addEventListener('focusout',()=>{queueMicrotask(()=>{if(!search.value&&!wrap.contains(document.activeElement))setExpanded(false);});});
 function paint(){const zh=language()==='zh';toggle.querySelector('span').textContent=zh?'搜索':'Search';toggle.ariaLabel=zh?'搜索模型':'Search models';clear.ariaLabel=zh?'清除并收起搜索':'Clear and close search';modes.ariaLabel=zh?'浏览方式':'Browse view';if(search.value)setExpanded(true);}
 root.classList.add('catalog-tools');document.querySelector('.results-bar').append(root);setExpanded(false);paint();return {open,paint};
}
