/** Small interaction feedback. Catalog results and keyboard actions stay immediate. */
export function initInteractionMotion(refine, doc = document) {
  const root = doc.documentElement;
  const summary = refine.querySelector('summary');
  const fields = refine.querySelector('.refine-fields');
  let pressed;
  root.dataset.motionInput = 'keyboard';
  const release = () => {
    pressed?.removeAttribute('data-pointer-pressed');
    pressed = null;
  };
  const keyboard = () => { root.dataset.motionInput = 'keyboard'; release(); };
  const pointer = event => {
    root.dataset.motionInput = 'pointer';
    release();
    if (event.button !== 0 || !event.isPrimary) return;
    pressed = event.target.closest('button:not(:disabled), #downloads a');
    pressed?.setAttribute('data-pointer-pressed', '');
  };
  const syncDisclosure = () => {
    // Native open/closed semantics change immediately, including during the visual exit.
    if (!refine.open && fields.contains(doc.activeElement)) summary.focus({preventScroll:true});
    fields.inert = !refine.open;
  };
  const observer = new MutationObserver(syncDisclosure);
  observer.observe(refine, {attributes:true, attributeFilter:['open']});
  syncDisclosure();
  doc.addEventListener('keydown', keyboard, true);
  doc.addEventListener('pointerdown', pointer, true);
  doc.addEventListener('pointerup', release, true);
  doc.addEventListener('pointercancel', release, true);
  doc.addEventListener('visibilitychange', release);
  doc.defaultView.addEventListener('blur', release);
  return () => {
    release(); observer.disconnect();
    doc.removeEventListener('keydown', keyboard, true);
    doc.removeEventListener('pointerdown', pointer, true);
    doc.removeEventListener('pointerup', release, true);
    doc.removeEventListener('pointercancel', release, true);
    doc.removeEventListener('visibilitychange', release);
    doc.defaultView.removeEventListener('blur', release);
  };
}

/** Only call after a successful clipboard write; repeat success stays settled. */
export function confirmCopy(button, message) {
  if (!button.isConnected) return;
  if (!button.querySelector('.copy-confirmation')) {
    button.style.minWidth = `${button.getBoundingClientRect().width}px`;
    const label = document.createElement('span');
    label.className = 'copy-label';
    label.textContent = message;
    const check = document.createElement('span');
    check.className = 'copy-confirmation';
    check.textContent = '✓'; check.setAttribute('aria-hidden', 'true');
    button.replaceChildren(label, check);
    // Establish the initial CSS state once; subsequent copies never restart it.
    getComputedStyle(check).opacity;
  }
  button.querySelector('.copy-label').textContent = message;
  button.dataset.copyState = 'copied';
}
