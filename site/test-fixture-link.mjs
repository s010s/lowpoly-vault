/** Test fixture copy only: preserve hardlinks when available, never hide other failures. */
import assert from 'node:assert/strict';
import {constants} from 'node:fs';
import {link,copyFile,readFile,lstat} from 'node:fs/promises';
export async function linkFixtureFile(source,target){
 try{await link(source,target);return;}
 catch(error){if(error.code!=='EXDEV')throw error;}
 await copyFile(source,target,constants.COPYFILE_EXCL);
 const [before,after]=await Promise.all([lstat(source),lstat(target)]);
 assert(before.isFile()&&after.isFile(),'Fixture copy requires regular files');
 assert.equal(after.mode&0o7777,before.mode&0o7777,'Fixture copy mode changed');
 assert.deepEqual(await readFile(target),await readFile(source),'Fixture copy bytes changed');
}
