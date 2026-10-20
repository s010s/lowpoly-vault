/** Original decorative wireframe. It is not a second model or a network asset. */
export function thumbnailPlaceholderMarkup(){
 return '<span class="thumbnail-placeholder" aria-hidden="true"><span class="thumbnail-placeholder-cube">'+['front','back','left','right','top','bottom'].map(face=>`<span class="thumbnail-placeholder-face thumbnail-placeholder-${face}"></span>`).join('')+'</span></span>';
}

/** CSS owns every frame; newly visible cubes join one document-timeline epoch. */
export function synchronizeThumbnailPlaceholders(cubes){
 for(const cube of cubes)for(const animation of cube.getAnimations?.()||[]){
  if(animation.animationName==='thumbnail-wireframe-turn'&&animation.playState==='running'&&animation.startTime!==0)animation.startTime=0;
 }
}
