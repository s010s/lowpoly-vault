// V5.4: eased ground light precedes the already-open hand, then a rise,
// complete landing, and one relaxed finger pose. All translations are authored
// meters; the main layout beat, reference scale and world orientation stay fixed.
export const ENTRY_TIMING=Object.freeze({
 layoutDuration:.70,glowDelay:.10,glowFadeInDuration:.80,
 revealStart:.95,revealDuration:.60,riseDuration:.95,
 settleStart:2.20,settleDuration:1.30,
 landedAt:3.50,handRelaxDuration:.60,
 humanRelaxStart:1.95,humanRelaxDuration:1.40,
 glowFadeOutStart:2.70,glowFadeOutDuration:1.10,total:4.10
});
export const DURATION=ENTRY_TIMING.total;
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const smooth=t=>{t=clamp(t);return t*t*(3-2*t)};
const lerp=(a,b,t)=>a+(b-a)*t;
export function entryAt(time,height,reducedMotion=false,kind='hand'){
 const timing=ENTRY_TIMING,t=reducedMotion?DURATION:clamp(time,0,DURATION),move=smooth(t/timing.layoutDuration);
 const rise=smooth((t-timing.revealStart)/timing.riseDuration),settle=1-smooth((t-timing.settleStart)/timing.settleDuration);
 const y=height*.03*rise*settle;
 const glow=smooth((t-timing.glowDelay)/timing.glowFadeInDuration)*(1-smooth((t-timing.glowFadeOutStart)/timing.glowFadeOutDuration));
 const opacity=smooth((t-timing.revealStart)/timing.revealDuration),hand=kind==='hand';
 // Set the open pose even while hidden, so no gathered/open transition can
 // appear in the first rendered frame. Finger relaxation starts after landing.
 // The human keeps its previous articulation relative to the delayed reveal.
 const gathered=0,open=hand?1-smooth((t-timing.landedAt)/timing.handRelaxDuration):1-smooth((t-timing.humanRelaxStart)/timing.humanRelaxDuration);
 return {move,y,glow,opacity,gathered,open,articulation:open,visible:opacity>0,progress:t/DURATION,
 phase:hand?(t<timing.revealStart?'掌根柔光':t<timing.settleStart?'张开 · 轻轻升起':t<timing.landedAt?'张开 · 平稳落下':t<DURATION?'落稳 · 手指微屈':'同一空间 · 真实比例'):
  (t<timing.revealStart?'掌根柔光':t<timing.settleStart?'轻升 · 手指舒展':t<timing.landedAt?'放松 · 平稳落下':'同一空间 · 真实比例')};
}
export function exitAt(time,height,start=null){
 const t=clamp(time/1.1),ease=smooth(t),from=start||{move:1,y:0,glow:0,opacity:1,gathered:0,open:0,articulation:0,visible:true};
 const opacity=from.opacity*(1-smooth(t/.85));
 const gathered=from.gathered||0,open=from.open??from.articulation??0;
 return {move:from.move*(1-smooth((t-.25)/.75)),y:lerp(Math.max(0,from.y),0,ease),glow:from.glow*(1-ease),opacity,gathered,open,articulation:open,visible:opacity>0,progress:1-t,phase:t<1?'柔光淡出':'就绪'};
}
