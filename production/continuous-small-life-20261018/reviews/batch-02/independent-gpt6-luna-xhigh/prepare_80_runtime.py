"""Derive an 80px exact-GLB review runner without touching candidate outputs."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE = ROOT / "production/continuous-small-life-20261018/work/batch-02/runtime.mjs"
OUTPUT = HERE / "runtime80.mjs"
text = SOURCE.read_text()
old_out = "const dir=path.join(root,base,id),out=path.join(dir,'runtime');"
new_out = (
    "const dir=path.join(root,base,id),out=path.join(root,"
    "'production/continuous-small-life-20261018/reviews/batch-02/"
    "independent-gpt6-luna-xhigh/runtime80',id,'runtime');"
)
old_views = (
    "for(const [name,view,extent,copies]of [['normal','hero',240,1],['near','hero',360,1],"
    "...['reversehero','front','side','rear','top'].map(v=>[v,v,360,1]),['scene','hero',420,9]])"
)
new_views = "for(const [name,view,extent,copies]of [['small80','hero',80,1]])"
old_wait = "await page.goto('http://127.0.0.1:'+port);await page.waitForFunction(()=>window.ready);const bytes="
new_wait = (
    "await page.goto('http://127.0.0.1:'+port);"
    "try{await page.waitForFunction(()=>window.ready,null,{timeout:10000})}"
    "catch(e){console.log('PAGE_ERROR',errors,await page.locator('body').innerText());throw e};"
    "const bytes="
)
if text.count(old_out) != 1 or text.count(old_views) != 1 or text.count(old_wait) != 1:
    raise SystemExit("Pinned runtime source no longer matches expected review patch")
text = text.replace(old_out, new_out).replace(old_views, new_views).replace(old_wait, new_wait)
OUTPUT.write_text(text)
print(OUTPUT.relative_to(ROOT))
