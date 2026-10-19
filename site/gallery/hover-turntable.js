import { LIQUID, ease, sampleLiquid, makeGeometry, renderLiquidSample } from './liquid-core.js';
const FIELD_FPS=30,CACHE_LIMIT=4;
const layers=new Map();
const fallbackSpec={floorCenter:[.5,350/432],floorPoints:Array.from({length:48},(_,i)=>[.5+Math.cos(i/48*Math.PI*2)*150/768,(350+Math.sin(i/48*Math.PI*2)*27)/432])};
function getLayer(spec){
 const key=spec?.floorPoints?.length?spec:fallbackSpec;
 if(layers.has(key)){const value=layers.get(key);layers.delete(key);layers.set(key,value);return value;}
 const geometry=makeGeometry(key),surface=document.createElement('canvas');surface.width=geometry.width;surface.height=geometry.height;
 const context=surface.getContext('2d'),pixels=context.createImageData(geometry.width,geometry.height);
 const layer={geometry,surface,context,pixels,key:null,renders:0};layers.set(key,layer);
 while(layers.size>CACHE_LIMIT)layers.delete(layers.keys().next().value);
 return layer;
}
export const liquidRuntime={FIELD_FPS,CACHE_LIMIT,cacheSize:()=>layers.size,clearCache:()=>layers.clear()};
export class HoverTurntableLiquid {
  constructor(e, t, { reduced: n = () => false } = {}) {
    this.rotatingAt=null;this.frozenAge=LIQUID.releaseEnd;this.liquidLayer=null;
    this.host = e, this.spec = t, this.reduced = n, this.phase = "loading", this.angle = 0, this.started = performance.now(), this.lastEmit = this.started, this.particles = [], this.seed = 811, this.raf = 0, this.canvas = document.createElement("canvas"), this.canvas.width = 768, this.canvas.height = 432, this.canvas.className = "hover-table", this.canvas.setAttribute("aria-hidden", "true"), e.prepend(this.canvas), e.dataset.hoverState = "loading", this.frame = this.frame.bind(this), this.schedule();
  }
  random() {
    return this.seed = Math.imul(this.seed, 1664525) + 1013904223 >>> 0, this.seed / 4294967296;
  }
  point(e, t = 1) {
    const n = this.spec?.floorPoints;
    if (!n?.length) return { x: 384 + Math.cos(e) * 150 * t, y: 350 + Math.sin(e) * 27 * t };
    const i = (e / (Math.PI * 2) % 1 + 1) % 1 * n.length, r = Math.floor(i), o = i - r, a = n[r], l = n[(r + 1) % n.length], c = this.spec.floorCenter[0] * 768, h = this.spec.floorCenter[1] * 432, d = (a[0] + (l[0] - a[0]) * o) * 768, u = (a[1] + (l[1] - a[1]) * o) * 432;
    return { x: c + (d - c) * t, y: h + (u - h) * t };
  }
  ready() {
    this.phase === "loading" && (this.phase = "ready", this.readyAt = performance.now(), this.host.dataset.hoverState = "ready", this.schedule());
  }
  rotate(e) {
    if(this.phase==='ending'||this.phase==='off')return;
    const now=performance.now();if(this.rotatingAt===null)this.rotatingAt=now;
    this.angle=e;this.phase='rotating';this.host.dataset.hoverState='rotating';this.draw(now);
  }
  stop() {
    if(this.phase==='off'||this.phase==='ending')return;
    this.endedAt=performance.now();
    this.frozenAge=this.rotatingAt===null?LIQUID.releaseEnd:(this.endedAt-this.rotatingAt)%LIQUID.period;
    this.phase='ending';this.host.dataset.hoverState='off';this.schedule();
  }
  drawLiquid(context,now,visibility){
    const quiet=this.rotatingAt===null||this.reduced();
    const age=quiet?LIQUID.releaseEnd:this.phase==='ending'?this.frozenAge:(now-this.rotatingAt)%LIQUID.period;
    const bucket=quiet?'quiet':Math.floor(age*FIELD_FPS/1000);
    const layer=this.liquidLayer||(this.liquidLayer=getLayer(this.spec));
    if(layer.key!==bucket){
      const sample=sampleLiquid(quiet?LIQUID.releaseEnd:bucket*1000/FIELD_FPS);
      renderLiquidSample(layer.geometry,sample,layer.pixels.data);layer.context.putImageData(layer.pixels,0,0);layer.key=bucket;layer.renders++;
    }
    context.save();context.globalAlpha=visibility;context.imageSmoothingEnabled=true;
    context.drawImage(layer.surface,0,0,768,432);context.restore();
  }
  schedule() {
    this.raf || (this.raf = requestAnimationFrame(this.frame));
  }
  frame(e) {
    if (this.raf = 0, this.particles = this.particles.filter((t) => e - t.born < t.life), this.reduced() && (this.particles = []), this.phase === "loading" && !this.reduced() && e - this.lastEmit >= 105) {
      this.lastEmit = e;
      const t = (e - this.started) * 32e-4 - 0.9, n = this.point(t - 1.05), i = this.point(t - 1.12), r = n.x - i.x, o = n.y - i.y, a = Math.hypot(r, o) || 1, l = [[195, 143, 79], [105, 159, 137], [128, 154, 178]];
      for (let c = 0; c < 2; c++) this.particles.push({ x: n.x, y: n.y, vx: -r / a * (11 + this.random() * 13), vy: -o / a * (11 + this.random() * 13) - 5, born: e, life: 270 + this.random() * 160, width: 0.65 + this.random() * 0.35, color: l[Math.floor(this.random() * l.length)] });
    }
    if (this.draw(e), this.phase === "ending" && this.particles.length === 0 && e - this.endedAt > 180) {
      this.phase = "off", this.canvas.remove();this.liquidLayer=null;
      return;
    }
    (this.phase === "loading" || this.phase === "ending" || this.particles.length || this.phase === "ready" && e - this.readyAt < 450) && this.schedule();
  }
  draw(e) {
    if (!this.canvas.isConnected) return;
    const t = this.canvas.getContext("2d");
    t.clearRect(0, 0, 768, 432);
    const n = this.phase === "ending", i = n ? 1-ease((e-this.endedAt)/180) : 1, r = this.phase !== "loading", o = r && !n;
    t.lineCap = "round", t.lineWidth = 1.35;
    if(r)this.drawLiquid(t,e,i);
    else {
    for (let a = 0; a < 72; a++) {
      const l = this.point(a / 72 * Math.PI * 2), c = this.point((a + 1) / 72 * Math.PI * 2);
      t.strokeStyle = `rgba(124,151,110,${(r ? 0.36 : 0.19) * i})`, t.beginPath(), t.moveTo(l.x, l.y), t.lineTo(c.x, c.y), t.stroke();
    }
    }
    if (this.phase === "loading" && !this.reduced()) {
      const a = (e - this.started) * 32e-4 - 0.9;
      t.strokeStyle = "rgba(117,150,104,.64)", t.lineWidth = 1.45, t.beginPath();
      for (let l = 0; l <= 26; l++) {
        const c = this.point(a - 1.05 + l / 26 * 1.05);
        l ? t.lineTo(c.x, c.y) : t.moveTo(c.x, c.y);
      }
      t.stroke();
    }
    if (o) {
      const a = Math.min(1, (e - (this.readyAt || e)) / 180);
      for (let l = 0; l < 12; l++) {
        const c = l / 12 * Math.PI * 2 + this.angle, h = this.point(c, 0.98), d = this.point(c, l === 0 ? 1.11 : 1.055);
        t.strokeStyle = `rgba(110,143,99,${(l === 0 ? 0.66 : 0.46) * a})`, t.lineWidth = 1.25, t.beginPath(), t.moveTo(h.x, h.y), t.lineTo(d.x, d.y), t.stroke();
      }
    }
    for (const a of this.particles) {
      const l = (e - a.born) / a.life, c = (e - a.born) / 1e3, h = (1 - Math.exp(-2 * c)) / 2, d = a.x + a.vx * h, u = a.y + a.vy * h, f = Math.hypot(a.vx, a.vy) || 1;
      t.strokeStyle = `rgba(${a.color.join(",")},${0.66 * (1 - l) ** 1.8})`, t.lineWidth = a.width, t.beginPath(), t.moveTo(d - a.vx / f * (2 + 3 * (1 - l)), u - a.vy / f * (2 + 3 * (1 - l))), t.lineTo(d, u), t.stroke();
    }
  }
}

export { HoverTurntableLiquid as HoverTurntable };
export function previewTurnAngle(seconds){const integral=u=>u*u*u-.5*u*u*u*u;let d;if(seconds<.4)d=24*.4*integral(seconds/.4);else if(seconds<.9)d=4.8+24*(seconds-.4);else if(seconds<1.4)d=16.8+24*(seconds-.9)-5*integral((seconds-.9)/.5);else d=26.3+14*(seconds-1.4);return d*Math.PI/180;}
