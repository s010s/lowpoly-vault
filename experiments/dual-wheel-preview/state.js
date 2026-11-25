/** Preview-only state. This module never writes the production catalog. */
export function filterItems(items, query = '', facets = {}) {
  const needle = query.trim().toLocaleLowerCase();
  return items.filter(item => {
    if (needle && ![item.id, ...Object.values(item.name || {})].join(' ').toLocaleLowerCase().includes(needle)) return false;
    return Object.entries(facets).every(([group, selected]) => {
      if (!selected.length) return true;
      const values = Array.isArray(item[group]) ? item[group] : [item[group]];
      return selected.some(value => values.includes(value));
    });
  });
}

/** Native scrolling remains authoritative until motion has become quiet. */
export class WheelSettler {
  constructor({ read, write, targets, center, reduced = () => false,
    now = () => performance.now(), frame = callback => requestAnimationFrame(callback),
    cancel = id => cancelAnimationFrame(id) }) {
    Object.assign(this, { read, write, targets, center, reduced, now, frame, cancel });
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
    if (this.state === 'snapping') return;
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
  pointerDown() { this.pressed = true; this.input(); }
  pointerUp() { this.pressed = false; this.lastInput = this.now(); this.stop(); this.state = 'tracking'; this.schedule(); }

  schedule() {
    if (!this.raf && !this.destroyed) this.raf = this.frame(() => { this.raf = 0; this.tick(); });
  }

  tick() {
    const time = this.now(), position = this.read();
    if (this.state === 'tracking') {
      if (Math.abs(position - this.previous) > .2) { this.lastMovement = time; this.moved = true; }
      this.previous = position;
      if (this.pressed || time - Math.max(this.lastMovement, this.lastInput) < 150) { this.schedule(); return; }
      if (!this.moved) { this.stop(); return; }
      const target = this.nearest(position);
      if (!target) { this.stop(); return; }
      this.setCenter(target.id);
      if (this.reduced() || Math.abs(position - target.offset) < 1) { this.stop(); return; }
      this.from = position;
      this.to = target.offset;
      this.started = time;
      this.state = 'snapping';
    }
    if (this.state === 'snapping') {
      if (this.reduced()) { this.stop(); return; }
      const progress = Math.min(1, (time - this.started) / 220);
      this.write(this.from + (this.to - this.from) * (1 - (1 - progress) ** 3));
      if (progress < 1) this.schedule();
      else this.stop();
    }
  }

  stop() {
    if (this.raf) this.cancel(this.raf);
    this.raf = 0;
    this.state = 'idle';
  }

  dispose() { this.destroyed = true; this.stop(); }
}
