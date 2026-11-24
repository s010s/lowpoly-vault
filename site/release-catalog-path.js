const release=token=>typeof token==='string'&&/^[a-f0-9]{12,40}$/.test(token)?'-'+token:'';
export const releaseCatalogBase=(name,token)=>'assets/'+name+release(token);
export function releaseCatalogPath(name,token=import.meta.env?.VITE_RELEASE_CATALOG_TOKEN){
 return releaseCatalogBase(name,token)+'.json';
}
