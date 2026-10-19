/** A single 20 px stroke family for controls; visible text supplies the accessible name. */
const paths={
 wireframe:'<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9m-8-4.5 8-4.5 8 4.5M12 3v9"/>',
 compare:'<rect x="3" y="7" width="18" height="10" rx="1.5"/><path d="M7 7v4m4-4v6m4-6v4m4-4v6"/>',
 reset:'<path d="M3.5 10a8.5 8.5 0 1 1 1.7 7.3M3.5 4.5V10H9"/>',
 download:'<path d="M12 3v12m-4-4 4 4 4-4M4 15v4.5A1.5 1.5 0 0 0 5.5 21h13a1.5 1.5 0 0 0 1.5-1.5V15"/>',
 source:'<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9M8 5.25l8 4.5"/>',
 copy:'<rect x="8" y="8" width="12" height="13" rx="1.5"/><path d="M15.5 8V4.5A1.5 1.5 0 0 0 14 3H5.5A1.5 1.5 0 0 0 4 4.5V14a1.5 1.5 0 0 0 1.5 1.5H8"/>',
};
export function iconMarkup(name){
 if(!Object.hasOwn(paths,name))throw new Error('Unknown control icon: '+name);
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+paths[name]+'</svg>';
}
export function mountIcons(root){for(const slot of root.querySelectorAll('[data-icon]'))slot.innerHTML=iconMarkup(slot.dataset.icon);}
if(typeof document!=='undefined')mountIcons(document);
