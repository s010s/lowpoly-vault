import assert from 'node:assert/strict';
import {assertOnlyTargetChanged,assertOnlyTargetResourcesChanged,assertCurrentTargetResources} from './model-commit-isolation.mjs';
const before={version:1,assets:[{id:'a',rev:1},{id:'b',rev:1}]},after={version:1,assets:[{id:'a',rev:2},{id:'b',rev:1}]};
assertOnlyTargetChanged(before,after,'a');
assert.throws(()=>assertOnlyTargetChanged(before,{...after,assets:[{id:'a',rev:2},{id:'b',rev:2}]},'a'),/unrelated/);
assert.throws(()=>assertOnlyTargetChanged(before,{...after,version:2},'a'),/metadata/);
assert.throws(()=>assertOnlyTargetChanged(before,before,'a'),/No target/);
const old={version:1,posters:{a:{p:1},b:{p:1}},files:[{path:'gallery/a.png',sha:1},{path:'gallery/b.png',sha:1}]};
const next=structuredClone(old);next.posters.a.p=2;next.files.push({path:'gallery/repairs/a/new.png',sha:2});assertOnlyTargetResourcesChanged(old,next,'a');
const wrong=structuredClone(next);wrong.posters.b.p=2;assert.throws(()=>assertOnlyTargetResourcesChanged(old,wrong,'a'),/Unrelated poster/);
const wrongFile=structuredClone(next);wrongFile.files[1].sha=2;assert.throws(()=>assertOnlyTargetResourcesChanged(old,wrongFile,'a'),/Unrelated resource file/);
console.log('PASS model-commit isolation: positive case and unrelated model/metadata/poster/file negative cases.');

const accumulated=structuredClone(next);accumulated.posters.b.p=9;accumulated.files[1].sha=9;assertCurrentTargetResources(next,accumulated,'a');
const specMutation=structuredClone(accumulated);specMutation.posters.a.wheelSpec={yaw:1};assert.throws(()=>assertCurrentTargetResources(next,specMutation,'a'),/Current target poster/);
const targetFileMutation=structuredClone(accumulated);targetFileMutation.files[0].sha=9;assert.throws(()=>assertCurrentTargetResources(next,targetFileMutation,'a'),/Current target resource files/);
console.log('PASS current target resources locked; unrelated later model allowed; wheelSpec and target-file mutations rejected.');
