/** One user intent, owned by one mobile static detail selection. No independent timer. */
export function createMobileActivationIntent({eligible, activate, announce = () => {}}) {
 let current=null,noticeState='idle';
 function notice(status){if(noticeState===status)return;noticeState=status;announce(status);}
 function end(entry,status='idle'){
  if(!entry.requested)return;
  entry.requested=false;
  notice(status);
 }
 function cancel(){if(current)end(current);notice('idle');}
 function clear(){cancel();current=null;}
 function fire(entry,mode){
  if(current!==entry||!eligible(entry.context,mode))return false;
  end(entry);notice('idle');
  // Invalidate before choose: a second button event cannot reuse this opening.
  current=null;
  activate(entry.context);
  return true;
 }
 function bind(context,painted){
  clear();
  const e={context,requested:false,readiness:'pending'};
  current=e;
  const finish=ready=>{
   if(current!==e)return;
   e.readiness=ready===true?'ready':'unavailable';
   if(!e.requested)return;
   if(e.readiness==='ready'&&fire(e,'ready'))return;
   // If the poster failed while the user already requested 3D, honor that intent
   // immediately instead of making the user tap the exact same button twice.
   if(e.readiness==='unavailable'&&fire(e,'missing'))return;
   end(e,e.readiness==='unavailable'&&eligible(e.context,'missing')?'unavailable':'idle');
  };
  Promise.resolve(painted).then(finish,()=>finish(false));
 }
 function request(){
  const e=current;
  if(!e||!eligible(e.context,'pending'))return 'ignored';
  if(e.readiness==='ready')return fire(e,'ready')?'activated':'ignored';
  if(e.readiness==='unavailable')return fire(e,'missing')?'fallback':'ignored';
  if(!e.requested){
   e.requested=true;
   notice('pending');
  }
  return 'pending';
 }
 return {bind,request,cancel,clear};
}
