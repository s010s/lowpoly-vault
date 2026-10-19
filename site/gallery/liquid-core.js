/** Approved v5 field. Bounded 384 x 216 CPU surface, one opacity cap.
 * Uses the real model floor polygon; no independent glow or secondary outline.
 */
export const LIQUID=Object.freeze({period:5000,arrival:2600,holdEnd:3200,releaseEnd:4300,
 color:[124,151,110],rimAlpha:.18,coreCap:.26,trailAlpha:.15,
 rimHalfWidth:2.4,waveStartHalfWidth:.75,waveEndHalfWidth:2.3,
 bridgeRadius:8,deformationPx:2.4,trailLag:420});
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const ease=x=>{x=clamp(x);return x*x*x*(x*(6*x-15)+10)};
// Monotone Hermite travel: no stop at the slow-contact interval. Values and
// velocity agree at every knot, giving adhesion time to read at card size.
const travel=[[0,.035,0],[1500,.86,.00016],[1800,.905,.00010],[2200,.947,.00010],[2600,1,0]];
export function radiusAt(t){
 if(t<=0)return .035;if(t>=LIQUID.arrival)return 1;
 const i=travel.findIndex((k,j)=>j<travel.length-1&&t>=k[0]&&t<travel[j+1][0]);
 const [ta,a,va]=travel[i],[tb,b,vb]=travel[i+1],dt=tb-ta,u=(t-ta)/dt;
 return (2*u**3-3*u**2+1)*a+(u**3-2*u**2+u)*dt*va+(-2*u**3+3*u**2)*b+(u**3-u**2)*dt*vb;
}
export function sampleLiquid(age){
 age=Math.max(0,age);
 const t=age%LIQUID.period,p=(radiusAt(t)-.035)/.965,arrived=t>=LIQUID.arrival;
 const response=arrived?1-ease((t-LIQUID.holdEnd)/(LIQUID.releaseEnd-LIQUID.holdEnd)):ease((p-.8)/.2);
 const settle=1-ease((t-LIQUID.arrival)/650);
 const tailDecay=arrived?(1-.45*ease((t-LIQUID.arrival)/700))*(1-ease((t-LIQUID.holdEnd)/(LIQUID.releaseEnd-LIQUID.holdEnd))):1;
 return {age:t,radius:radiusAt(t),previousRadius:radiusAt(t-LIQUID.trailLag),progress:p,
  waveAlpha:arrived?LIQUID.rimAlpha+(LIQUID.coreCap-LIQUID.rimAlpha)*response:(.10+.16*p)*ease(t/380),
  rimAlpha:LIQUID.rimAlpha+(LIQUID.coreCap-LIQUID.rimAlpha)*response,
  waveHalfWidth:LIQUID.waveStartHalfWidth+(LIQUID.waveEndHalfWidth-LIQUID.waveStartHalfWidth)*p,
  bridge:LIQUID.bridgeRadius*ease((p-.86)/.10)*settle,
  deform:LIQUID.deformationPx*ease((t-1600)/250)*(1-ease((t-2300)/300)),
  tailAlpha:LIQUID.trailAlpha*ease(t/500)*tailDecay,
  tailWidthScale:arrived?1-.55*ease((t-LIQUID.arrival)/700):1,
  stage:t<2000?'approach':t<2600?'adhesion':t<3200?'surface settling':t<4300?'return':'quiet'};
}
/** Precompute radial distance and local normal metric for the exact polygon. */
export function makeGeometry(spec,width=384,height=216){
 const cx=spec.floorCenter[0]*width,cy=spec.floorCenter[1]*height;
 const points=spec.floorPoints.map(p=>[p[0]*width-cx,p[1]*height-cy]);
 const count=2048,table=new Float64Array(count),tau=Math.PI*2;
 for(let i=0;i<count;i++){
  const angle=i/count*tau,dx=Math.cos(angle),dy=Math.sin(angle);let nearest=Infinity;
  for(let j=0;j<points.length;j++){
   const a=points[j],b=points[(j+1)%points.length],ex=b[0]-a[0],ey=b[1]-a[1],den=dx*ey-dy*ex;
   if(Math.abs(den)<1e-10)continue;
   const t=(a[0]*ey-a[1]*ex)/den,s=(a[0]*dy-a[1]*dx)/den;
   if(t>0&&s>=0&&s<=1)nearest=Math.min(nearest,t);
  }
  if(!Number.isFinite(nearest))throw new Error('Floor center must lie inside floor polygon');
  table[i]=nearest;
 }
 const rho=new Float32Array(width*height),metric=new Float32Array(rho.length),lobe=new Float32Array(rho.length);
 const indices=[];
 for(let y=0;y<height;y++)for(let x=0;x<width;x++){
  const dx=x+.5-cx,dy=y+.5-cy,angle=(Math.atan2(dy,dx)+tau)%tau,index=angle/tau*count;
  const i=Math.floor(index),f=index-i,ray=table[i]*(1-f)+table[(i+1)%count]*f;
  const derivative=(table[(i+1)%count]-table[(i-1+count)%count])/(2*tau/count);
  const n=y*width+x;rho[n]=Math.hypot(dx,dy)/ray;
  metric[n]=ray/Math.sqrt(1+(derivative/ray)**2)*(768/width);
  let delta=Math.atan2(Math.sin(angle-Math.PI/2),Math.cos(angle-Math.PI/2));
  lobe[n]=Math.exp(-.5*(delta/.60)**2);
  if((rho[n]-1)*metric[n]<6&&rho[n]>.005)indices.push(n);
 }
 const list=Uint32Array.from(indices),rimDistance=new Float32Array(rho.length),rimBand=new Float32Array(rho.length),outside=new Float32Array(rho.length);
 for(const n of list){rimDistance[n]=(rho[n]-1)*metric[n];rimBand[n]=Math.abs(rimDistance[n])-LIQUID.rimHalfWidth;outside[n]=1-ease((rimDistance[n]-LIQUID.rimHalfWidth+.5)/2);}
 return {width,height,rho,metric,lobe,indices:list,rimDistance,rimBand,outside};
}
export const renderLiquid=(geometry,age)=>renderLiquidSample(geometry,sampleLiquid(age));
export function renderLiquidSample(geometry,s,rgba=new Uint8ClampedArray(geometry.width*geometry.height*4)){
 const {rho,metric,lobe,indices,rimDistance,rimBand,outside}=geometry;
 const edgeFeather=1.1;
 for(const n of indices){
  const normal=metric[n];
  const dWave=(rho[n]-s.radius)*normal-s.deform*lobe[n];
  const a=rimBand[n],b=Math.abs(dWave)-s.waveHalfWidth;
  const h=s.bridge>.00001?clamp(.5+.5*(a-b)/s.bridge):(b<a?1:0);
  const distance=a*(1-h)+b*h-s.bridge*h*(1-h);
  const mask=1-ease((distance+edgeFeather)/(2*edgeFeather));
  // Keep the foundation's outer boundary fixed; liquid accumulates inward.
  const outerMask=outside[n];
  const core=mask*(s.rimAlpha*(1-h)+s.waveAlpha*h)*outerMask;
  const behind=Math.max(0,-dWave);
  const tailWidth=clamp((s.radius-s.previousRadius)*normal,18,42)*s.tailWidthScale;
  const trail=s.tailAlpha*(1-ease((dWave+1.3)/2.6))*Math.max(0,1-behind/tailWidth)**2;
  // Max-composition prevents additive brightness or layered ring buildup.
  const alpha=Math.min(LIQUID.coreCap,Math.max(core,trail*outerMask));
  const o=n*4;rgba[o]=LIQUID.color[0];rgba[o+1]=LIQUID.color[1];rgba[o+2]=LIQUID.color[2];rgba[o+3]=Math.round(alpha*255);
 }
 return rgba;
}
