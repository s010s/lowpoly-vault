// Keep the document's native scrolling. Only the catalog hides its scrollbar;
// the fixed, non-interactive hint never changes layout or intercepts input.
export function createCatalogScroll({ catalog, dialog, label, doc = document, view = window }) {
  const root = doc.documentElement;
  const cue = doc.createElement('div');
  cue.className = 'catalog-scroll-cue';
  cue.setAttribute('aria-hidden', 'true');
  cue.hidden = true;
  const text = doc.createElement('span');
  cue.append(text);
  doc.body.append(cue);
  let active = false, frame = 0;

  function update() {
    frame = 0;
    const nextLabel = `${label()} ↓`;
    if (text.textContent !== nextLabel) text.textContent = nextLabel;
    const height = view.innerHeight;
    cue.hidden = !active || dialog.open || root.scrollHeight <= height + 2 ||
      catalog.getBoundingClientRect().bottom <= height + 2;
  }
  function refresh() {
    if (!frame) frame = view.requestAnimationFrame(update);
  }
  const resize = new ResizeObserver(refresh);
  resize.observe(catalog);
  resize.observe(doc.body);
  const changes = new MutationObserver(refresh);
  changes.observe(dialog, { attributes: true, attributeFilter: ['open'] });
  changes.observe(root, { attributes: true, attributeFilter: ['lang'] });
  view.addEventListener('scroll', refresh, { passive: true });
  view.addEventListener('resize', refresh, { passive: true });

  return {
    setActive(value) {
      // History reconciliation often retains the same underlying catalog.
      // Do not force synchronous document measurement during modal reversal.
      if (active === value) { refresh(); return; }
      if (frame) view.cancelAnimationFrame(frame);
      active = value;
      // Keep this scope while the detail is above the catalog. Scroll lock then
      // cannot remove a gutter or change any measured card/flight coordinates.
      root.toggleAttribute('data-catalog-scroll', active);
      update();
    },
    dispose() {
      view.cancelAnimationFrame(frame);
      resize.disconnect();
      changes.disconnect();
      view.removeEventListener('scroll', refresh);
      view.removeEventListener('resize', refresh);
      root.removeAttribute('data-catalog-scroll');
      cue.remove();
    },
  };
}
