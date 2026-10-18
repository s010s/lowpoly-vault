import { CARD_RENDER_PRESET } from './render-preset.js';
/** Image-only card inspection. No Three.js, GLB fetches, autoplay or full-sequence preloading. */
export const PREVIEW_LIMITS = Object.freeze({ encodedEntries:12, encodedBytes:2*1024*1024, decodedEntries:3, manifestEntries:3, maxDimension:1024 });
const cancelled=()=>new DOMException('Preview superseded','AbortError');
export function validateTurntable(value, descriptor) {
  if(value?.version!==1||value.source_glb_sha256!==descriptor.source_glb_sha256||!Number.isInteger(value.frame_count)||value.frame_count<24||value.frame_count>36||value.frames?.length!==value.frame_count||value.frame_count!==descriptor.frame_count)throw new Error('Invalid turntable identity or frame count');
  for(const key of ['width','height'])if(!Number.isInteger(value[key])||value[key]<32||value[key]>PREVIEW_LIMITS.maxDimension)throw new Error('Preview dimensions exceed the card budget');
  if(value.width!==descriptor.width||value.height!==descriptor.height||value.poster_index!==descriptor.poster_index)throw new Error('Preview descriptor differs from sequence');
  if(!Number.isInteger(value.poster_index)||value.poster_index<0||value.poster_index>=value.frame_count)throw new Error('Invalid poster frame');
  const prefix=descriptor.manifest.slice(0,descriptor.manifest.lastIndexOf('/')+1),seen=new Set();
  for(const frame of value.frames) {
    if(typeof frame.path!=='string'||!frame.path.startsWith(prefix)||!/^assets\/turntables\/[a-z0-9-]+\/[a-zA-Z0-9._/-]+\.webp$/.test(frame.path)||frame.path.split('/').some(p=>p==='..'||p==='.')||seen.has(frame.path)||!Number.isSafeInteger(frame.bytes)||frame.bytes<1||frame.bytes>PREVIEW_LIMITS.encodedBytes||!/^[a-f0-9]{64}$/.test(frame.sha256||''))throw new Error('Invalid or unsafe turntable frame');
    seen.add(frame.path);
  }
  return value;
}
export class FrameLRU {
  constructor({maxEntries,maxBytes=Infinity,onDelete=()=>{}}){Object.assign(this,{maxEntries,maxBytes,onDelete});this.entries=new Map();this.bytes=0;}
  get(key){const item=this.entries.get(key);if(!item)return;this.entries.delete(key);this.entries.set(key,item);return item.value;}
  set(key,value,bytes=0){this.delete(key);if(bytes>this.maxBytes){this.onDelete(value);return false;}this.entries.set(key,{value,bytes});this.bytes+=bytes;while(this.entries.size>this.maxEntries||this.bytes>this.maxBytes)this.delete(this.entries.keys().next().value);return true;}
  delete(key){const item=this.entries.get(key);if(!item)return;this.entries.delete(key);this.bytes-=item.bytes;this.onDelete(item.value);}
  clear(){for(const key of [...this.entries.keys()])this.delete(key);}
}
export class ImageScrubPreview {
  constructor({resolvePath,language=()=> 'en',fetchImpl=globalThis.fetch.bind(globalThis),decode=blob=>createImageBitmap(blob)}) {
    Object.assign(this,{resolvePath,language,fetchImpl,decode});this.generation=0;this.current=null;this.want=null;this.prefetch=[];this.running=null;
    this.encoded=new FrameLRU({maxEntries:PREVIEW_LIMITS.encodedEntries,maxBytes:PREVIEW_LIMITS.encodedBytes});
    this.decoded=new FrameLRU({maxEntries:PREVIEW_LIMITS.decodedEntries,onDelete:bitmap=>bitmap.close()});
    this.manifests=new FrameLRU({maxEntries:PREVIEW_LIMITS.manifestEntries});
    this.stats={activeId:null,activeRequests:0,peakRequests:0,frameRequests:0,manifestRequests:0,downloadedBytes:0,decodedEntries:0,decodedBytes:0,peakDecodedBytes:0,encodedEntries:0,encodedBytes:0,canvasBytes:0,frame:null,errors:0,decodeMilliseconds:[],requestMilliseconds:[]};
    globalThis.__vaultPreview=this.stats;
    this.visibility=()=>{if(document.hidden)this.stop();};document.addEventListener('visibilitychange',this.visibility);
    this.intersection=new IntersectionObserver(entries=>{if(entries.some(e=>e.target===this.current?.card&&!e.isIntersecting))this.stop();});
  }
  text(en,zh){return this.language()==='zh'?zh:en;}
  sync(){Object.assign(this.stats,{activeId:this.current?.id||null,encodedEntries:this.encoded.entries.size,encodedBytes:this.encoded.bytes,decodedEntries:this.decoded.entries.size,decodedBytes:this.decoded.bytes,canvasBytes:this.canvas?this.canvas.width*this.canvas.height*4:0});this.stats.peakDecodedBytes=Math.max(this.stats.peakDecodedBytes,this.stats.decodedBytes);}
  activate(card,asset) {
    if(!asset?.turntable){this.stop();return false;}
    if(this.current?.card===card)return true;
    this.stop();this.current={card,id:asset.id,descriptor:asset.turntable,frame:asset.turntable.poster_index||0};this.intersection.observe(card);card.dataset.scrubState='loading';
    card.querySelector('.card-status').textContent=this.text('Loading image preview…','正在载入多角度预览…');this.request(this.current.frame);return true;
  }
  request(frame) {
    if(!this.current||this.current.failed)return;
    const count=this.current.descriptor.frame_count;this.current.frame=((Math.round(frame)%count)+count)%count;
    if(this.stats.frame===this.current.frame&&!this.current.snapshotView&&!this.running&&!this.want)return;
    this.prefetch=[];this.want={generation:this.generation,current:this.current,frame:this.current.frame};
    if(!this.running)this.running=this.pump().finally(()=>{this.running=null;if(this.want)this.request(this.want.frame);});
  }
  async fetch(url,{json=false,expectedBytes}={}) {
    const controller=this.controller=new AbortController(),start=performance.now();this.stats.activeRequests++;this.stats.peakRequests=Math.max(this.stats.peakRequests,this.stats.activeRequests);
    try {const response=await this.fetchImpl(this.resolvePath(url),{signal:controller.signal});if(!response.ok)throw new Error('Preview file unavailable');const blob=await response.blob();if(expectedBytes!==undefined&&blob.size!==expectedBytes)throw new Error('Preview byte size differs');this.stats.downloadedBytes+=blob.size;this.stats.requestMilliseconds.push(performance.now()-start);if(this.stats.requestMilliseconds.length>100)this.stats.requestMilliseconds.shift();return json?JSON.parse(await blob.text()):blob;}
    finally{this.stats.activeRequests--;if(this.controller===controller)this.controller=null;}
  }
  async pump() {
    while(this.want||this.prefetch.length) {
      const job=this.want||this.prefetch.shift();this.want=null;const live=()=>job.generation===this.generation&&job.current===this.current;
      try {
        let manifest=this.manifests.get(job.current.descriptor.manifest);
        if(!manifest){this.stats.manifestRequests++;manifest=validateTurntable(await this.fetch(job.current.descriptor.manifest,{json:true}),job.current.descriptor);if(!live())throw cancelled();this.manifests.set(job.current.descriptor.manifest,manifest);}
        if(!live())throw cancelled();
        if(job.preload&&this.want)continue;
        // New pointer input wins before another image request; intermediate positions are discarded.
        if(this.want?.generation===job.generation){job.frame=this.want.frame;this.want=null;}
        if(job.preload&&this.want)continue;
        const frame=manifest.frames[job.frame];let bitmap=this.decoded.get(frame.path);
        if(!bitmap){let blob=this.encoded.get(frame.path);if(!blob){this.stats.frameRequests++;blob=await this.fetch(frame.path,{expectedBytes:frame.bytes});if(!live())throw cancelled();this.encoded.set(frame.path,blob,blob.size);}
          if(this.decoded.entries.size>=PREVIEW_LIMITS.decodedEntries)this.decoded.delete(this.decoded.entries.keys().next().value);
          const start=performance.now();bitmap=await this.decode(blob);this.stats.decodeMilliseconds.push(performance.now()-start);if(this.stats.decodeMilliseconds.length>100)this.stats.decodeMilliseconds.shift();
          if(!live()){bitmap.close();throw cancelled();}if(bitmap.width!==manifest.width||bitmap.height!==manifest.height){bitmap.close();throw new Error('Unexpected decoded preview dimensions');}
          this.decoded.set(frame.path,bitmap,bitmap.width*bitmap.height*4);
        }
        if(!live())throw cancelled();
        if(this.want?.generation===job.generation&&this.want.frame!==job.frame){this.sync();continue;}
        if(job.preload){this.sync();continue;}
        if(!this.canvas){this.canvas=document.createElement('canvas');this.canvas.className='image-scrub-canvas';this.canvas.setAttribute('aria-hidden','true');this.canvas.width=manifest.width;this.canvas.height=manifest.height;job.current.card.querySelector('.asset-image').append(this.canvas);}
        // A returned detail snapshot may have a larger square backing. Restore
        // the sequence budget before painting the first new scrub frame.
        if(this.canvas.width!==manifest.width||this.canvas.height!==manifest.height){this.canvas.width=manifest.width;this.canvas.height=manifest.height;}
        const context=this.canvas.getContext('2d',{alpha:true});context.clearRect(0,0,this.canvas.width,this.canvas.height);context.drawImage(bitmap,0,0);
        job.current.snapshotView=null;job.current.card.dataset.scrubState='ready';job.current.card.dataset.scrubFrame=String(job.frame);job.current.card.querySelector('.card-status').textContent=this.text(`Image view ${job.frame+1}/${manifest.frame_count} · Click for 3D`,`图片视角 ${job.frame+1}/${manifest.frame_count} · 点击进入 3D`);this.stats.frame=job.frame;this.sync();
        this.prefetch=[-1,1].map(delta=>({...job,frame:(job.frame+delta+manifest.frame_count)%manifest.frame_count,preload:true})).filter(next=>!this.decoded.entries.has(manifest.frames[next.frame].path));
      } catch(error) {
        if(error.name==='AbortError'||!live())continue;
        if(job.preload){this.stats.errors++;this.sync();continue;}
        this.stats.errors++;job.current.failed=true;job.current.card.dataset.scrubState='fallback';job.current.card.querySelector('.card-status').textContent=this.text('Static preview · Click for 3D','静态预览 · 点击进入 3D');this.canvas?.remove();this.canvas=null;this.decoded.clear();this.want=null;this.sync();
      }
    }
  }
  retainSnapshot(card,asset,source,view,{transfer=false}={}) {
    if(!asset?.turntable||!source)return;
    this.stop();const count=asset.turntable.frame_count;
    const azimuth=view?.azimuth_deg??CARD_RENDER_PRESET.camera.azimuth_deg;
    const frame=((Math.round((azimuth-CARD_RENDER_PRESET.camera.azimuth_deg)*count/360)%count)+count)%count;
    this.current={card,id:asset.id,descriptor:asset.turntable,frame,snapshotView:view};this.intersection.observe(card);
    const width=source.naturalWidth||source.width,height=source.naturalHeight||source.height,size=Math.min(width,height);
    if(transfer&&width===height&&width<=PREVIEW_LIMITS.maxDimension){this.canvas=source;}else{
      this.canvas=document.createElement('canvas');this.canvas.width=asset.turntable.width;this.canvas.height=asset.turntable.height;
      this.canvas.getContext('2d').drawImage(source,(width-size)/2,(height-size)/2,size,size,0,0,this.canvas.width,this.canvas.height);
    }
    this.canvas.className='image-scrub-canvas';this.canvas.setAttribute('aria-hidden','true');
    card.querySelector('.asset-image').append(this.canvas);card.dataset.scrubState='ready';card.dataset.scrubFrame=String(frame);this.stats.frame=frame;this.sync();
  }
  capture({transfer=false}={}) {
    if(!this.canvas||!this.current||this.current.card.dataset.scrubState!=='ready')return null;
    const frame=this.manifests.get(this.current.descriptor.manifest)?.frames[this.stats.frame];
    // A detail flight can take the already rasterized card surface. Copying it
    // on every cached reopen forces a new canvas backing and GPU upload.
    const canvas=transfer?this.canvas:document.createElement('canvas');
    if(transfer){this.canvas=null;this.sync();}else{canvas.width=this.canvas.width;canvas.height=this.canvas.height;canvas.getContext('2d').drawImage(this.canvas,0,0);}
    canvas.className='model-handoff';canvas.setAttribute('aria-hidden','true');canvas.dataset.assetId=this.current.id;
    canvas.__presentation=this.current.snapshotView||(frame?{azimuth_deg:frame.azimuth_deg,elevation_deg:frame.elevation_deg}:undefined);
    return {canvas,id:this.current.id,view:this.current.snapshotView||(frame?{azimuth_deg:frame.azimuth_deg,elevation_deg:frame.elevation_deg}:undefined)};
  }
  fraction(value){if(this.current)this.request(Math.min(this.current.descriptor.frame_count-1,Math.max(0,Math.floor(value*this.current.descriptor.frame_count))));}
  step(delta){if(this.current)this.request(this.current.frame+delta);}
  stop(){this.generation++;this.want=null;this.prefetch=[];this.controller?.abort();this.intersection?.disconnect();if(this.current){delete this.current.card.dataset.scrubState;delete this.current.card.dataset.scrubFrame;this.current.card.querySelector('.card-status').textContent='';}this.canvas?.remove();this.canvas=null;this.decoded?.clear();this.current=null;if(this.stats){this.stats.frame=null;this.sync();}}
  dispose(){this.stop();this.encoded.clear();this.manifests.clear();this.sync();document.removeEventListener('visibilitychange',this.visibility);}
}
