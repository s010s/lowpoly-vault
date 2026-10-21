/** Gallery browsing state. The published manifest remains authoritative. */
import {normalizeText} from '../routes.js';
export function filterItems(items, query = '', facets = {}) {
  const terms = normalizeText(query).trim().split(/\s+/).filter(Boolean);
  return items.filter(item => {
    const searchable=normalizeText([item.id,...Object.values(item.name||{}),item.category,item.collection,...(item.worlds||[]),...(item.packs||[])].join(' '));
    if(!terms.every(term=>searchable.includes(term)))return false;
    return Object.entries(facets).every(([group, selected]) => {
      if (!selected.length) return true;
      if(group==='triangleMax')return Number.isFinite(item.triangles)&&item.triangles<=Number(selected[0]);
      const values = Array.isArray(item[group]) ? item[group] : [item[group]];
      return selected.some(value => values.includes(value));
    });
  });
}

/** Native scrolling remains authoritative until motion has become quiet. */
export class WheelSettler {
  constructor({ read, write, targets, center, settled = () => {}, reduced = () => false,
    now = () => performance.now(), frame = callback => requestAnimationFrame(callback),
    cancel = id => cancelAnimationFrame(id) }) {
    Object.assign(this, { read, write, targets, center, settled, reduced, now, frame, cancel });
    this.raf = 0;
    this.lastInput = this.lastMovement = -Infinity;
    this.previous = read();
    this.destroyed = false;
    this.state = 'idle';
    this.centeredId = null;
    this.pressed = false;
    this.moved = false;
  }

  input(scrollIntent = false) {
    this.lastInput = this.now();
    this.moved = scrollIntent;
    this.stop();
    this.state = 'tracking';
    this.previous = this.read();
    this.schedule();
  }

  scrolled() {
    const position = this.read();
    if (Math.abs(position - this.previous) > .2) this.moved = true;
    const nearest = this.nearest(position);
    if (nearest) this.setCenter(nearest.id);
    if (this.state === 'snapping' || this.state === 'centering') return;
    this.previous = position;
    this.lastMovement = this.now();
    this.state = 'tracking';
    this.schedule();
  }

  nearest(position) {
    return this.targets().reduce((best, target) => !best ||
      Math.abs(target.offset - position) < Math.abs(best.offset - position) ||
      (Math.abs(target.offset - position) === Math.abs(best.offset - position) && target.id === this.centeredId)
      ? target : best, null);
  }

  setCenter(id) { this.centeredId = id; this.center(id); }

  /** Explicit activation moves the list only; selecting a model belongs to the caller. */
  centerOn(id, {immediate = false} = {}) {
    if (this.destroyed) return false;
    const target = this.targets().find(item => item.id === id);
    if (!target) return false;
    if (this.state === 'centering' && this.destinationId === id && this.to === target.offset) return true;
    this.stop();
    this.from = this.read();
    this.to = target.offset;
    this.destinationId = id;
    if (immediate || this.reduced() || Math.abs(this.to - this.from) < 1) {
      this.write(this.to);
      this.previous = this.read();
      this.setCenter(id);
      this.settled();
      return true;
    }
    this.started = this.now();
    this.duration = Math.min(440, 280 + Math.abs(this.to - this.from) * .18);
    this.state = 'centering';
    this.schedule();
    return true;
  }
  pointerDown() { this.pressed = true; this.input(); }
  pointerUp() { this.pressed = false; this.lastInput = this.now(); this.stop(); this.state = 'tracking'; this.schedule(); }

  schedule() {
    if (!this.raf && !this.destroyed) this.raf = this.frame(() => { this.raf = 0; this.tick(); });
  }

  tick() {
    const time = this.now(), position = this.read();
    if (this.state === 'centering') {
      const target = this.targets().find(item => item.id === this.destinationId);
      if (!target || target.offset !== this.to) { this.finish(); return; }
      const progress = this.reduced() ? 1 : Math.min(1, (time - this.started) / this.duration);
      // Smooth start/finish; a new click retargets from the currently presented position.
      const eased = progress * progress * (3 - 2 * progress);
      this.write(this.from + (this.to - this.from) * eased);
      this.previous = this.read();
      const nearest = this.nearest(this.previous);
      if (nearest) this.setCenter(nearest.id);
      if (progress < 1) this.schedule();
      else this.finish();
      return;
    }
    if (this.state === 'tracking') {
      if (Math.abs(position - this.previous) > .2) { this.lastMovement = time; this.moved = true; }
      this.previous = position;
      if (this.pressed || time - Math.max(this.lastMovement, this.lastInput) < 150) { this.schedule(); return; }
      if (!this.moved) { this.finish(); return; }
      const target = this.nearest(position);
      if (!target) { this.finish(); return; }
      this.setCenter(target.id);
      if (this.reduced() || Math.abs(position - target.offset) < 1) { this.finish(); return; }
      this.from = position;
      this.to = target.offset;
      this.started = time;
      this.state = 'snapping';
    }
    if (this.state === 'snapping') {
      if (this.reduced()) { this.finish(); return; }
      const progress = Math.min(1, (time - this.started) / 220);
      this.write(this.from + (this.to - this.from) * (1 - (1 - progress) ** 3));
      if (progress < 1) this.schedule();
      else this.finish();
    }
  }

  finish() { this.stop();if(!this.destroyed)this.settled(); }

  stop() {
    if (this.raf) this.cancel(this.raf);
    this.raf = 0;
    this.state = 'idle';
  }

  dispose() { this.destroyed = true; this.stop(); }
}
