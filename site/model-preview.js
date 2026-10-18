import { startHoverReveal } from './hover-reveal.js';
import { CARD_RENDER_PRESET } from './render-preset.js';

// A card is a poster until an intentional interaction acquires the application's
// single ModelStage. The controller owns no renderer, decoded model or GLB cache.
export class SharedModelPreview {
  constructor({ resolvePath, getStage, language = () => 'en' }) {
    Object.assign(this, { resolvePath, getStage, language });
    this.generation = 0;
    this.current = null;
    this.stats = { kind: 'shared-real-model', activeId: null, frame: null, errors: 0,
      frameRequests: 0, manifestRequests: 0, activations: 0, firstPreviewMilliseconds: 0 };
    globalThis.__vaultPreview = this.stats;
    this.visibility = () => { if (document.hidden) this.stop(); };
    document.addEventListener('visibilitychange', this.visibility);
    this.intersection = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.target === this.current?.card && !entry.isIntersecting)) this.stop();
    });
  }

  text(en, zh) { return this.language() === 'zh' ? zh : en; }
  sync() { this.stats.activeId = this.current?.id || null; this.stats.frame = this.current?.frame ?? null; }

  activate(card, asset) {
    if (!asset?.glb || !card?.isConnected || document.hidden) return false;
    if (this.current?.card === card && (this.current.loading || this.current.live)) return true;
    const previous = this.current?.card === card ? this.current : null;
    const view = previous?.snapshotView;
    // Keep the returned exact bitmap until the matching GLB has drawn.
    const retained = previous ? this.canvas : null;
    if (retained) this.canvas = null;
    this.stop();
    this.canvas = retained;
    const current = this.current = { card, id: asset.id, asset,
      descriptor: { frame_count: 24, poster_index: 0 },
      frame: previous?.frame || 0, snapshotView: view, loading: true, live: false };
    const generation = this.generation, started = performance.now();
    this.controller = new AbortController();
    const live = () => generation === this.generation && this.current === current && card.isConnected;
    this.intersection.observe(card);
    card.dataset.previewState = 'loading';
    card.querySelector('.card-status').textContent = this.text('Loading 3D preview…', '正在载入 3D 预览…');
    this.stats.activations++;
    this.sync();
    this.pending = this.getStage().then(async stage => {
      if (!live()) return false;
      this.stage = stage;
      return stage.show(card.querySelector('.asset-image'), this.resolvePath(asset.glb), {
        mode: 'hover', initialView: view, signal: this.controller.signal,
        onStatus: status => {
          if (!live()) return;
          card.dataset.previewState = status === 'error' ? 'fallback' : status;
          if (status === 'ready') {
            current.live = true; current.loading = false;
            this.reveal(current, stage);
            if (this.canvas) { this.canvas.remove(); this.canvas.width = this.canvas.height = 0; this.canvas = null; }
            card.querySelector('.card-status').textContent = this.text('3D preview · Move to orbit', '3D 预览 · 移动查看角度');
            this.stats.firstPreviewMilliseconds = performance.now() - started;
          }
        },
      }).then(ready => {
        if (ready && live() && current.want !== undefined) this.request(current.want);
        return ready;
      });
    }).catch(error => {
      if (!live() || error?.name === 'AbortError') return false;
      current.loading = current.live = false;
      this.stats.errors++;
      card.dataset.previewState = 'fallback';
      card.querySelector('.card-status').textContent = this.text('Static preview · Click for details', '静态预览 · 点击查看详情');
      return false;
    });
    return true;
  }

  reveal(current, stage) {
    const poster = this.canvas || current.card.querySelector('.asset-image img');
    if (globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches ||
        !poster || !(poster.width > 0) || (poster.tagName === 'IMG' && (!poster.complete || !poster.naturalWidth))) return;
    const model = stage.snapshot({ square: true });
    if (!model) return;
    // A retained canvas may be retired by activate immediately after this call.
    // Copy it once; the canonical poster image itself is stable while hovered.
    let lower = poster;
    if (poster === this.canvas) {
      lower = document.createElement('canvas'); lower.width = poster.width; lower.height = poster.height;
      lower.getContext('2d').drawImage(poster, 0, 0);
    }
    this.revealLower = lower === poster ? null : lower;
    this.revealMotion = startHoverReveal({ host: current.card.querySelector('.asset-image'), poster: lower, model,
      onFinish: () => {
        this.clearReveal();
        // Commit held input in this same paint opportunity. Exposing the
        // canonical canvas and queuing another RAF lets Enter capture a pose
        // that has never been displayed between reveal completion and orbit.
        if (this.current === current && current.want !== undefined) this.applyRequest(current);
      } });
  }

  clearReveal() {
    this.revealMotion?.cancel(); this.revealMotion = null;
    if (this.revealLower) this.revealLower.width = this.revealLower.height = 0;
    this.revealLower = null;
  }

  request(frame) {
    const current = this.current;
    if (!current || !Number.isFinite(frame)) return;
    current.frame = frame; current.want = frame;
    this.sync();
    if (!current.live || this.revealMotion || this.raf) return;
    const generation = this.generation;
    this.raf = requestAnimationFrame(() => {
      this.raf = 0;
      if (generation !== this.generation || this.current !== current || !current.live) return;
      this.applyRequest(current);
    });
  }
  applyRequest(current) {
    const base = current.snapshotView || CARD_RENDER_PRESET.camera;
    this.stage.setView(CARD_RENDER_PRESET.camera.azimuth_deg + current.want * 360 / 24,
      base.elevation_deg, base.distance);
    current.snapshotView = this.stage.presentationInfo;
    current.card.dataset.previewAzimuth = String(current.snapshotView.azimuth_deg);
  }
  step(delta) { if (this.current) this.request(this.current.frame + delta); }

  capture({ transfer = false } = {}) {
    const current = this.current;
    if (!current) return null;
    if (this.revealMotion) {
      // Clicking during reveal hands off the exact displayed blend, not the
      // unseen final GLB or a pending pointer pose.
      const source = this.revealMotion.canvas, canvas = document.createElement('canvas');
      canvas.width = source.width; canvas.height = source.height;
      canvas.getContext('2d').drawImage(source, 0, 0);
      canvas.className = 'model-handoff'; canvas.dataset.assetId = current.id;
      canvas.__presentation = source.__presentation;
      return { canvas, id: current.id, view: canvas.__presentation };
    }
    // Flush the latest pointer intent before taking the transfer frame.
    if (this.raf) { cancelAnimationFrame(this.raf); this.raf = 0;
      const base = current.snapshotView || CARD_RENDER_PRESET.camera;
      this.stage?.setView(CARD_RENDER_PRESET.camera.azimuth_deg + current.want * 15, base.elevation_deg, base.distance); }
    // The renderer frames inside a centered square. Capturing the rectangular
    // card margin would shrink its flight when the detail aspect ratio differs.
    let canvas = current.live ? this.stage.snapshot({ square: true }) : this.canvas;
    if (!canvas) return null;
    const view = canvas.__presentation || current.snapshotView;
    if (canvas === this.canvas && transfer) this.canvas = null;
    else if (canvas === this.canvas) {
      const copy = document.createElement('canvas'); copy.width = canvas.width; copy.height = canvas.height;
      copy.getContext('2d').drawImage(canvas, 0, 0); canvas = copy;
    }
    canvas.className = 'model-handoff'; canvas.dataset.assetId = current.id; canvas.__presentation = view;
    return { canvas, id: current.id, view };
  }

  retainSnapshot(card, asset, source, view, { transfer = false } = {}) {
    this.stop();
    if (!asset?.glb || !source || !card.isConnected) return;
    this.current = { card, id: asset.id, asset, descriptor: { frame_count: 24, poster_index: 0 },
      frame: ((view?.azimuth_deg ?? CARD_RENDER_PRESET.camera.azimuth_deg) - CARD_RENDER_PRESET.camera.azimuth_deg) / 15,
      snapshotView: view, loading: false, live: false };
    this.canvas = transfer ? source : document.createElement('canvas');
    if (!transfer) { this.canvas.width = source.width; this.canvas.height = source.height; this.canvas.getContext('2d').drawImage(source, 0, 0); }
    this.canvas.className = 'model-preview-snapshot'; this.canvas.setAttribute('aria-hidden', 'true');
    card.querySelector('.asset-image').append(this.canvas); card.dataset.previewState = 'ready';
    this.intersection.observe(card); this.sync();
  }

  stop() {
    this.generation++;
    this.clearReveal();
    this.controller?.abort(); this.controller = null;
    if (this.raf) cancelAnimationFrame(this.raf); this.raf = 0;
    this.intersection.disconnect();
    const current = this.current;
    if (current) {
      if (this.stage?._host === current.card.querySelector('.asset-image')) this.stage.hide();
      delete current.card.dataset.previewState; delete current.card.dataset.previewAzimuth;
      current.card.querySelector('.card-status').textContent = '';
    }
    if (this.canvas) { this.canvas.remove(); this.canvas.width = this.canvas.height = 0; this.canvas = null; }
    this.current = null; this.sync();
  }
  dispose() { this.stop(); document.removeEventListener('visibilitychange', this.visibility); }
}
