/** Keeps a title through harmless motion; only a stable new centre takes ownership. */
export class WheelTitle {
  constructor({read, targets, change, delay = 200, tolerance = 12, maxVelocity = .45,
    quiet = 80, now = () => performance.now(),
    schedule = (callback, ms) => setTimeout(callback, ms), cancel = id => clearTimeout(id)}) {
    Object.assign(this, {read, targets, change, delay, tolerance, maxVelocity, quiet, now, schedule, cancel});
    this.owner = this.candidate = null;
    this.timer = null;
    this.destroyed = false;
    this.reset();
  }

  clear() {
    if (this.timer !== null) this.cancel(this.timer);
    this.timer = null;
    this.deadline = null;
  }

  reset() {
    this.clear();
    this.owner = this.candidate = null;
    this.position = this.read();
    this.sampledAt = this.now();
    this.fastAt = -Infinity;
  }

  update() {
    if (this.destroyed) return null;
    const time = this.now(), position = this.read(), targets = this.targets();
    if (position !== this.position) {
      // A minimum frame interval prevents duplicate renders from inventing velocity.
      if (Math.abs(position - this.position) / Math.max(16, time - this.sampledAt) > this.maxVelocity) this.fastAt = time;
      this.position = position;
      this.sampledAt = time;
    }
    if (!targets.length) { this.reset(); return null; }
    let nearest = targets.reduce((best, item) => !best || Math.abs(item.offset - position) < Math.abs(best.offset - position) ? item : best, null);
    if (!targets.some(item => item.id === this.owner)) {
      this.clear();
      this.owner = this.candidate = nearest.id;
      return this.owner;
    }
    const previous = targets.find(item => item.id === this.candidate);
    // Cross the halfway point by 12 px before changing direction, including reversal.
    if (previous && Math.abs(previous.offset - position) - Math.abs(nearest.offset - position) <= this.tolerance * 2) nearest = previous;
    if (nearest.id !== this.candidate) {
      this.candidate = nearest.id;
      this.candidateAt = time;
    }
    if (this.candidate === this.owner) { this.clear(); return this.owner; }
    const deadline = Math.max(this.candidateAt + this.delay, this.fastAt + this.quiet);
    if (time >= deadline) {
      this.clear();
      this.owner = this.candidate;
    } else if (this.deadline !== deadline || this.timer === null) {
      this.clear();
      this.deadline = deadline;
      this.timer = this.schedule(() => {
        this.timer = null;
        // Re-read the real position/results when the delayed render happens.
        if (!this.destroyed) this.change();
      }, deadline - time);
    }
    return this.owner;
  }

  dispose() { this.destroyed = true; this.clear(); }
}
