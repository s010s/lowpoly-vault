import assert from 'node:assert/strict';
import {mkdtempSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {execFileSync} from 'node:child_process';
import {extractFastArchive,restoreFastBase} from './ci-release-fast-base.mjs';
const root=mkdtempSync(join(tmpdir(),'fast-archive-fixture-'));
function make(kind){const p=join(root,kind+'.zip');execFileSync('python3',['-I','-c',`import io,tarfile,zipfile,sys\nb=io.BytesIO();kind=sys.argv[2]\nwith tarfile.open(fileobj=b,mode='w:gz') as t:\n names=['receipt.json','template.html','dist/index.html']\n if kind=='traversal':names.append('../escaped')\n if kind=='absolute':names.append('/tmp/escaped')\n if kind=='duplicate':names.append('dist/index.html')\n if kind=='double-slash':names.append('dist//index.html')\n if kind=='dot-alias':names.append('dist/./index.html')\n if kind=='unknown':names.append('run.py')\n if kind=='backslash':names.append('dist/x\\\\y')\n for name in names:\n  m=tarfile.TarInfo(name);v=b'fixture';m.size=len(v);t.addfile(m,io.BytesIO(v))\n if kind in ('symlink','hardlink'):\n  m=tarfile.TarInfo('dist/link');m.type=tarfile.SYMTYPE if kind=='symlink' else tarfile.LNKTYPE;m.linkname='../../escape';t.addfile(m)\nwith zipfile.ZipFile(sys.argv[1],'w') as z:\n z.writestr('base.tar.gz',b.getvalue())\n if kind=='extra-zip':z.writestr('unrequested','extra')\n`,p,kind]);return readFileSync(p);}
try{
 const good=extractFastArchive(make('valid'),mkdtempSync(join(root,'valid-')));assert.equal(readFileSync(join(good,'dist/index.html'),'utf8'),'fixture');let n=1;
 for(const kind of ['traversal','absolute','duplicate','double-slash','dot-alias','unknown','backslash','symlink','hardlink','extra-zip']){assert.throws(()=>extractFastArchive(make(kind),mkdtempSync(join(root,kind+'-'))));n++;}
 await assert.rejects(restoreFastBase({eligible:true,baseline:{}}),/process-local/);n++;
 console.log(`Fast artifact extraction: ${n} valid/hostile archive and forged-scope cases passed.`);
}finally{rmSync(root,{recursive:true,force:true});}
