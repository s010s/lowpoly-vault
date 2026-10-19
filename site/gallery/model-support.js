// A reviewed support origin is asset-specific, not inferred from arbitrary
// low vertices (tails, fins, rocks and flat surfaces have ambiguous supports).
// This bird's paired-foot patch is measured in the authored GLB axes/meters.
// Both the catalog digest and the fetched bytes must match the reviewed source.
export const MEASURED_SUPPORTS=Object.freeze({
 confuciusornis:Object.freeze({
  sha256:'264383f0cca9b772479d93037f83c4084a6feabefd26d0285278e6a539f16bdb',
  point:Object.freeze([0,0,.013363168574869633]),
  min:Object.freeze([-.07154838740825653,0,-.3529999852180481]),
  max:Object.freeze([.07154838740825653,.21907636523246765,.125]),
  reason:'Midpoint of the paired feet support patch; excludes the long rear tail.'
 })
});
export function needsSupportDigest(asset){return !!MEASURED_SUPPORTS[asset.id];}
export function measuredSupport(asset,entry){
 const rule=MEASURED_SUPPORTS[asset.id];
 if(!rule||asset.sha256?.glb!==rule.sha256||entry.sha256!==rule.sha256)return null;
 const min=entry.box.min.toArray(),max=entry.box.max.toArray();
 if(min.some((v,i)=>Math.abs(v-rule.min[i])>1e-7)||max.some((v,i)=>Math.abs(v-rule.max[i])>1e-7))return null;
 return rule;
}
