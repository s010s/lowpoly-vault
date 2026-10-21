/** Only bundle the unchanged native ModelStage entry, not the historic website. */
import {build} from 'vite';import {resolve} from 'node:path';
await build({configFile:false,root:process.cwd(),publicDir:false,base:'/lowpoly-vault/',build:{outDir:resolve(process.env.GALLERY_DIR||'qa/capture-inputs-site','assets'),emptyOutDir:true,lib:{entry:resolve('site/viewer.js'),formats:['es'],fileName:()=>'viewer-fifty-two-capture.js'},rollupOptions:{output:{inlineDynamicImports:true}}}});
