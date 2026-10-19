import {Quaternion, Spherical, Vector3} from 'three';

// Matches the approved comparison's 0.70 s placement beat. This transition
// explains a spatial change; it is not applied to direct pointer/keyboard input.
export const RESET_DURATION = 700;
const clamp = value => Math.max(0, Math.min(1, value));
const smooth = value => {const t=clamp(value);return t*t*(3-2*t);};
const lerp = (a,b,t) => a+(b-a)*t;
const blendArray = (a,b,t) => a.map((value,i)=>lerp(value,b[i],t));
export const shortestAngle = (from,to) => Math.atan2(Math.sin(to-from),Math.cos(to-from));

/** Orbit in angle/radius space: never cut through the subject or spin 350°. */
export function interpolateView(from,to,progress,{camera=true}={}) {
  const t=smooth(progress), result={...from};
  if(camera){
    const a=new Spherical().setFromVector3(new Vector3().fromArray(from.position).sub(new Vector3().fromArray(from.target)));
    const b=new Spherical().setFromVector3(new Vector3().fromArray(to.position).sub(new Vector3().fromArray(to.target)));
    const target=new Vector3().fromArray(blendArray(from.target,to.target,t));
    const orbit=new Spherical(Math.exp(lerp(Math.log(Math.max(1e-8,a.radius)),Math.log(Math.max(1e-8,b.radius)),t)),lerp(a.phi,b.phi,t),a.theta+shortestAngle(a.theta,b.theta)*t);
    result.target=target.toArray();result.position=new Vector3().setFromSpherical(orbit).add(target).toArray();
    result.zoom=Math.exp(lerp(Math.log(from.zoom||1),Math.log(to.zoom||1),t));
    result.screenShift=lerp(from.screenShift||0,to.screenShift||0,t);
    result.screenShiftY=lerp(from.screenShiftY||0,to.screenShiftY||0,t);
  }
  if(from.modelYaw!==undefined||to.modelYaw!==undefined)result.modelYaw=(from.modelYaw||0)+shortestAngle(from.modelYaw||0,to.modelYaw||0)*t;
  if(from.contactPosition&&to.contactPosition)result.contactPosition=blendArray(from.contactPosition,to.contactPosition,t);
  if(from.modelPosition&&to.modelPosition)result.modelPosition=blendArray(from.modelPosition,to.modelPosition,t);
  if(from.modelQuaternion&&to.modelQuaternion)result.modelQuaternion=new Quaternion().fromArray(from.modelQuaternion).slerp(new Quaternion().fromArray(to.modelQuaternion),t).normalize().toArray();
  // Return the authored endpoint exactly, avoiding accumulated spherical error.
  if(progress>=1){for(const key of ['modelPosition','modelQuaternion','modelYaw','contactPosition',...(camera?['position','target','zoom','screenShift','screenShiftY']:[])])if(to[key]!==undefined)result[key]=Array.isArray(to[key])?[...to[key]]:to[key];}
  return result;
}

/** One interruptible owner for Compare, Reset and withdrawing comparison. */
export class ViewTransition {
  constructor({read,write,reduced=()=>false,clock=()=>performance.now(),request=callback=>requestAnimationFrame(callback),cancel=id=>cancelAnimationFrame(id),onActivity=()=>{}}){
    Object.assign(this,{read,write,reduced,clock,request,cancel,onActivity});this.frame=0;this.active=null;
  }
  start(destination,{duration=RESET_DURATION,camera=true,orientation=true,yaw=true,zoom=true}={}){
    const keys=['position','target','zoom','screenShift','screenShiftY','modelPosition','modelQuaternion','modelYaw','contactPosition'];
    if(camera&&orientation&&yaw&&zoom&&this.active?.camera&&this.active.orientation&&this.active.yaw&&this.active.zoom&&keys.every(key=>JSON.stringify(this.active.to[key])===JSON.stringify(destination[key])))return;
    // Capture the last presented frame, rather than advancing offscreen and
    // making a new input jump ahead of what the user was actually looking at.
    this.cancelAll();
    this.active={from:this.read(),to:structuredClone(destination),start:this.clock(),duration,camera,orientation,yaw,zoom};
    if(this.reduced()||duration<=0){this.finish();return;}
    this.onActivity(true);this.frame=this.request(time=>this.tick(time));
  }
  tick(time=this.clock()){
    this.frame=0;const active=this.active;if(!active)return false;
    const progress=clamp((time-active.start)/active.duration);
    let value=interpolateView(active.from,active.to,progress,{camera:active.camera});
    // An intervening drag/zoom owns the camera from that point onward. Model
    // placement can finish without overwriting one frame of the user's input.
    if(!active.camera){const live=this.read();value={...value,position:live.position,target:live.target,zoom:live.zoom,screenShift:live.screenShift,screenShiftY:live.screenShiftY};}
    if(!active.orientation)value.modelQuaternion=this.read().modelQuaternion;
    if(!active.yaw)value.modelYaw=this.read().modelYaw;
    if(!active.zoom)value.zoom=this.read().zoom;
    this.write(value,{cameraOwned:active.camera,orientationOwned:active.orientation});
    if(this.active!==active)return false;
    if(progress<1)this.frame=this.request(next=>this.tick(next));
    else{this.active=null;this.onActivity(false);}
    return progress<1;
  }
  interruptCamera(){if(this.active){this.active.camera=false;this.active.zoom=false;}}
  interruptComparisonInput(){if(this.active)this.active.yaw=false;}
  interruptZoom(){if(this.active)this.active.zoom=false;}
  interruptInspection(){if(this.active){this.active.camera=false;this.active.orientation=false;this.active.yaw=false;this.active.zoom=false;}}
  finish(){
    if(!this.active)return;const active=this.active,live=this.read();
    const end={...live,...active.to};if(!active.camera){end.position=live.position;end.target=live.target;end.zoom=live.zoom;end.screenShift=live.screenShift;end.screenShiftY=live.screenShiftY;}
    if(!active.orientation)end.modelQuaternion=live.modelQuaternion;
    if(!active.yaw)end.modelYaw=live.modelYaw;
    if(!active.zoom)end.zoom=live.zoom;
    this.cancelAll();this.write(end,{cameraOwned:active.camera,orientationOwned:active.orientation});
  }
  cancelAll(){if(this.frame)this.cancel(this.frame);this.frame=0;this.active=null;this.onActivity(false);}
}
