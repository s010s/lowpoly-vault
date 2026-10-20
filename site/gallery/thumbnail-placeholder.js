/** Original decorative wireframe. It is not a second model or a network asset. */
export function thumbnailPlaceholderMarkup(){
 return '<span class="thumbnail-placeholder" aria-hidden="true"><span class="thumbnail-placeholder-cube">'+['front','back','left','right','top','bottom'].map(face=>`<span class="thumbnail-placeholder-face thumbnail-placeholder-${face}"></span>`).join('')+'</span></span>';
}
