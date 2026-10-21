/** One cancellable hover intent; recovery is event-driven, never a retry loop. */
export class HoverIntent {
  constructor({hit, enabled, ready, idle, create, delay=300,
    schedule=fn=>setTimeout(fn,delay), cancel=id=>clearTimeout(id)}) {
    Object.assign(this,{hit,enabled,ready,idle,create,schedule,cancel});
    this.point=null;this.request=null;this.timer=null;this.row=null;
  }
  pointer(event) {
    if(event.pointerType==='touch'){this.clear();return;}
    this.point={x:event.clientX,y:event.clientY};this.refresh();
  }
  target() { return this.point&&this.enabled()&&this.idle()?this.hit(this.point):null; }
  pause() {
    if(this.timer!==null)this.cancel(this.timer);
    this.timer=null;this.row=null;
    const request=this.request;this.request=null;request?.session?.stop();
  }
  clear() { this.point=null;this.pause(); }
  refresh() {
    const row=this.target();
    if(!row||!this.ready()){this.pause();return;}
    if(this.row===row)return;
    this.pause();this.row=row;
    this.timer=this.schedule(()=>{this.timer=null;void this.start(row);});
  }
  async start(row) {
    if(this.row!==row||this.target()!==row||!this.ready()){this.pause();return;}
    const request={session:null};this.request=request;
    const valid=()=>this.request===request&&this.row===row&&this.target()===row&&this.ready();
    let active=false;
    try {
      const session=request.session=this.create(row);
      if(!await session.prepare()||!valid())return;
      session.ready();
      if(await session.reveal()&&valid()){session.animate();active=true;}
    } catch { /* Keep the poster on load/reveal failure; retry only on new intent. */ }
    finally {
      // A cancelled promise cannot stop or reveal a newer request.
      if(this.request===request){
        if(!valid())this.pause();
        else if(!active){this.request=null;request.session?.stop();}
      }
    }
  }
}

/** Hit-test current geometry, not the row that happened to receive pointermove. */
export function hoverRowAt(document,wheel,slots,{x,y}) {
  const bounds=wheel.getBoundingClientRect();
  if(!wheel.clientHeight||x<bounds.left||x>=bounds.right||y<bounds.top||y>=bounds.bottom)return null;
  const row=document.elementFromPoint(x,y)?.closest('.slot');
  return row?.isConnected&&row.parentElement===slots?row:null;
}
