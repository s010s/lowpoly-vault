/** Chrome has its own timeline: never transform/fade the dialog that owns the
 * viewport-positioned model flight. All animated content keeps its layout space. */
export const DIALOG_TIMING = Object.freeze({
  flightOpen: 300, flightClose: 180,
  panelOpen: 240, panelClose: 120,
  backdropOpen: 220, backdropClose: 140,
  contentOpen: 180, contentDelay: 60, contentClose: 80,
});

export class DialogMotion {
  constructor(dialog, reduced) {
    this.dialog = dialog;
    this.reduced = reduced;
    this.active = new Set();
    this.version = 0;
    this.positionShadow = () => {
      const rect = dialog.getBoundingClientRect();
      Object.assign(this.shadow.style, { left: `${rect.left}px`, top: `${rect.top}px`, width: `${rect.width}px`, height: `${rect.height}px` });
    };
    this.resize = new ResizeObserver(this.positionShadow);
    this.resize.observe(dialog);
    this.resize.observe(dialog.ownerDocument.documentElement);
    this.onReduce = () => { if (reduced.matches) for (const animation of this.active) animation.finish(); };
    reduced.addEventListener('change', this.onReduce);
  }
  get panel() { return this.dialog.querySelector('.viewer-layout'); }
  get shadow() { return this.dialog.querySelector('.modal-chrome-shadow'); }
  get content() {
    return [...this.dialog.querySelectorAll('.asset-info > *, .viewer-topline, #viewer-status, .viewer-controls, #scale-status, .viewer-hint, :scope > button')];
  }
  capture() {
    if (!this.dialog.open) return null;
    return {
      opacity: new Map([this.panel, ...this.content].map(element => [element, Number(getComputedStyle(element).opacity)])),
      backdrop: Number(getComputedStyle(this.dialog, '::backdrop').opacity),
      shadow: Number(getComputedStyle(this.shadow).opacity),
    };
  }
  cancel() {
    this.version++;
    clearTimeout(this.deadline);
    for (const animation of this.active) animation.cancel();
    this.active.clear();
    this.dialog.removeAttribute('data-modal-motion');
    this.dialog.style.removeProperty('--modal-backdrop-start');
    this.dialog.style.removeProperty('--modal-backdrop-duration');
  }
  start({ reverse = false, from = null } = {}) {
    this.cancel();
    this.positionShadow();
    if (this.reduced.matches) return Promise.resolve();
    const version = this.version;
    // Flush removal of a previous same-direction CSS animation before restarting
    // it, including an opening interrupted by a new detail selection.
    getComputedStyle(this.dialog, '::backdrop').opacity;
    const direction = reverse ? 'closing' : 'opening';
    const end = reverse ? 0 : 1;
    const duration = reverse ? DIALOG_TIMING.panelClose : DIALOG_TIMING.panelOpen;
    const backdropDuration = reverse ? DIALOG_TIMING.backdropClose : DIALOG_TIMING.backdropOpen;
    const easing = reverse ? 'cubic-bezier(.2,0,.2,1)' : 'cubic-bezier(.2,.7,.3,1)';
    const animate = (element, frames, options = {}) => {
      const animation = element.animate(frames, { duration, easing, fill: 'both', ...options });
      this.active.add(animation);
      return animation.finished.catch(() => {});
    };
    const opacity = element => from?.opacity.get(element) ?? (reverse ? 1 : 0);
    const tasks = [animate(this.panel, [{ opacity: opacity(this.panel) }, { opacity: end }])];
    for (const element of this.content) {
      // A single small reveal overlaps the model flight. No serial 300 + 352ms tail.
      // Transform only leaf content, never the canvas host or its ancestors.
      const frames = [{ opacity: opacity(element) }, { opacity: end }];
      tasks.push(animate(element, frames, {
        duration: reverse ? DIALOG_TIMING.contentClose : DIALOG_TIMING.contentOpen,
        delay: reverse || from ? 0 : DIALOG_TIMING.contentDelay,
      }));
    }
    // Rasterize the static blur once, then composite opacity. Animating a large
    // box-shadow itself forces costly paint on every frame, especially on mobile.
    tasks.push(animate(this.shadow, [
      { opacity: from?.shadow ?? (reverse ? 1 : 0) },
      { opacity: end },
    ], { duration: backdropDuration }));
    this.dialog.style.setProperty('--modal-backdrop-start', String(from?.backdrop ?? (reverse ? 1 : 0)));
    this.dialog.style.setProperty('--modal-backdrop-duration', `${backdropDuration}ms`);
    this.dialog.dataset.modalMotion = direction;
    // Use the intended wall-clock endpoint if the compositor delays its WAAPI
    // start/finish notification. Dismissal must not acquire a scheduling tail.
    if (reverse) this.deadline = setTimeout(() => {
      if (version === this.version) for (const animation of this.active) animation.finish();
    }, backdropDuration);
    return Promise.all(tasks).then(() => {
      if (version !== this.version) return;
      clearTimeout(this.deadline);
      if (reverse) return;
      this.cancel();
      this.dialog.dataset.modalMotion = 'open';
    });
  }
  dispose() {
    this.cancel();
    this.resize.disconnect();
    this.reduced.removeEventListener('change', this.onReduce);
  }
}
