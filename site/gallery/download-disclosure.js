// One model's unusually broad plinth intersects the standard desktop card.
const model='teichichnus-spreite-wall';

export function createDownloadDisclosure({stage,card,isMobile,text,redraw}){
 const originalParent=card.parentNode, originalNext=card.nextSibling, main=stage.closest('main');
 let mounted=null;
 function unmount(){
  if(!mounted)return;
  const {button,section,y}=mounted, active=document.activeElement;
  const restoreFocus=active===button||section.contains(active);
  originalParent.insertBefore(card,originalNext);
  if(!section.hidden)window.scrollTo(0,y);
  section.remove();button.remove();mounted=null;
  if(restoreFocus)stage.focus({preventScroll:true});
  redraw();
 }
 function sync(id){
  if(id!==model||isMobile()){unmount();return;}
  if(!mounted){
   const make=(tag,id)=>{const node=document.createElement(tag);node.id=id;return node;};
   const button=make('button','a308-download-entry'),section=make('section','a308-download-section');
   const heading=make('h2','a308-download-heading'),close=make('button','a308-download-close');
   button.type=close.type='button';heading.tabIndex=-1;
   button.setAttribute('aria-expanded','false');button.setAttribute('aria-controls',section.id);
   section.hidden=true;section.setAttribute('aria-labelledby',heading.id);
   section.append(heading,card,close);main.after(section);originalParent.append(button);
   mounted={button,section,heading,close,y:0};
   function collapse(){
    section.hidden=true;button.setAttribute('aria-expanded','false');
    window.scrollTo(0,mounted.y);button.focus({preventScroll:true});redraw();
   }
   button.onclick=()=>{
    if(!section.hidden){collapse();return;}
    mounted.y=window.scrollY;section.hidden=false;button.setAttribute('aria-expanded','true');
    section.scrollIntoView({block:'end',behavior:'instant'});heading.focus({preventScroll:true});redraw();
   };
   close.onclick=collapse;
   section.onkeydown=event=>{if(event.key==='Escape'){event.preventDefault();collapse();}};
  }
  mounted.button.textContent=text('Download model','下载模型');
  mounted.heading.textContent=mounted.button.textContent;
  mounted.close.textContent=text('Close downloads','收起下载');
 }
 return {sync,expanded:()=>!!mounted&&!mounted.section.hidden};
}
