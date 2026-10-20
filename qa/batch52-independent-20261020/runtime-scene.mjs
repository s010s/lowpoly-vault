import assert from 'node:assert/strict';
import {createServer} from 'node:http';
import {createHash} from 'node:crypto';
import {mkdir, readFile, writeFile} from 'node:fs/promises';
import {resolve, sep} from 'node:path';
import {chromium} from 'playwright';

const root = resolve('.');
const output = resolve(root, process.env.QA_RUN_DIR || 'qa/batch52-independent-20261020', 'runtime');
const modules = resolve(root, 'node_modules/three');
await mkdir(output, {recursive: true});
const specs = [
  {id:'aturia', revision:'r002', sha256:'65f2c625334872f5e849d3bee11ff6085cc3245c93cb2cd86ba4baf13a74287b', triangles:12160, path:'assets/candidates/continuous-small-life-round18-20261020/batch-52/aturia/r002/aturia.glb'},
  {id:'phoenicopsis', revision:'r001', sha256:'7e7fa939eeca8d1d0571ae1724faa7fa2387f03441bf0794fe4b269d666182d0', triangles:1394, path:'assets/candidates/continuous-small-life-round18-20261020/batch-52/phoenicopsis/r001/phoenicopsis.glb'},
  {id:'cave-popcorn', revision:'r003', sha256:'36439f98c26784601b24ba4ac18c709f51c3ef9b071e0225438aaec42b7ba85b', triangles:7398, path:'assets/candidates/continuous-small-life-round18-20261020/batch-52/cave-popcorn/r003/cave-popcorn.glb'},
  {id:'curvolithus-trilobed-trail', revision:'r001', sha256:'c07529a8856b679af1a1d3e816c37046076488ee926f7e38e70241f0cbefed22', triangles:2790, path:'assets/candidates/continuous-small-life-round18-20261020/batch-52/curvolithus-trilobed-trail/r001/curvolithus-trilobed-trail.glb'},
];
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
const files = new Map();
for (const item of specs) {
  const bytes = await readFile(resolve(root, item.path));
  assert.equal(digest(bytes), item.sha256, item.id + ': frozen GLB SHA mismatch');
  item.bytes = bytes.length;
  files.set('/models/' + item.id + '.glb', bytes);
}

const html = '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;width:100%;height:100%;background:#e9e5dc}canvas{display:block}</style><script type="importmap">{"imports":{"three":"/modules/build/three.module.js"}}</script></head><body></body></html>';
const server = createServer(async (req, res) => {
  try {
    const pathname = new URL(req.url, 'http://127.0.0.1').pathname;
    if (pathname === '/') { res.setHeader('Content-Type', 'text/html'); res.end(html); return; }
    if (pathname === '/favicon.ico') { res.writeHead(204).end(); return; }
    if (files.has(pathname)) { res.setHeader('Content-Type', 'model/gltf-binary'); res.end(files.get(pathname)); return; }
    assert(pathname.startsWith('/modules/'));
    const path = resolve(modules, '.' + decodeURIComponent(pathname.slice('/modules'.length)));
    assert(path.startsWith(modules + sep) && path.endsWith('.js'));
    res.setHeader('Content-Type', 'text/javascript');
    res.end(await readFile(path));
  } catch {
    res.writeHead(404).end();
  }
});

const report = {
  schema_version: 1,
  kind: 'batch52_software_webgl_runtime_parse_and_scene',
  status: 'running',
  engine: 'Three.js GLTFLoader',
  three_version_expected: '0.180.0',
  browser_engine: 'Chromium ANGLE SwiftShader software WebGL2',
  device: 'software renderer (SwiftShader)',
  limitation: 'Functional parsing and rendering evidence only. Physical GPU and target-device performance were not measured.',
  assets: specs.map(item => ({id:item.id, revision:item.revision, sha256:item.sha256, path:item.path, bytes:item.bytes, triangles:item.triangles})),
  errors: [],
  resource_errors: [],
};
let browser;
try {
  await new Promise(ok => server.listen(0, '127.0.0.1', ok));
  browser = await chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--enable-webgl', '--ignore-gpu-blocklist', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'],
  });
  report.browser_version = browser.version();
  const page = await browser.newPage({viewport: {width: 1280, height: 900}, deviceScaleFactor: 1});
  page.on('pageerror', error => report.errors.push(String(error)));
  page.on('console', message => { if (message.type() === 'error') report.errors.push(message.text()); });
  page.on('response', response => { if (response.status() >= 400) report.resource_errors.push(response.status() + ' ' + response.url()); });
  await page.goto('http://127.0.0.1:' + server.address().port + '/', {waitUntil: 'networkidle'});
  await page.evaluate(() => { window.__qaImages = {}; });
  const result = await page.evaluate(async items => {
    const T = await import('three');
    const {GLTFLoader} = await import('/modules/examples/jsm/loaders/GLTFLoader.js');
    const loader = new GLTFLoader();
    const renderer = new T.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
    renderer.setPixelRatio(1);
    renderer.setSize(512, 512);
    renderer.outputColorSpace = T.SRGBColorSpace;
    renderer.toneMapping = T.ACESFilmicToneMapping;
    document.body.append(renderer.domElement);
    const gl = renderer.getContext();
    const debug = gl.getExtension('WEBGL_debug_renderer_info');
    const loaded = [];
    const singleResults = [];
    function countAsset(gltf) {
      let triangles = 0, meshNodes = 0;
      const materials = new Set();
      gltf.scene.traverse(object => {
        if (!object.isMesh) return;
        meshNodes++;
        const geometry = object.geometry;
        const count = geometry.index ? geometry.index.count : geometry.attributes.position.count;
        triangles += count / 3;
        for (const material of (Array.isArray(object.material) ? object.material : [object.material])) if (material) materials.add(material.name);
      });
      return {triangles, mesh_nodes: meshNodes, material_names: [...materials].sort()};
    }
    function capture(scene, camera, filename) {
      renderer.info.reset();
      renderer.render(scene, camera);
      const value = {
        render_calls: renderer.info.render.calls,
        render_triangles: renderer.info.render.triangles,
        gl_error: gl.getError(),
        context_lost: gl.isContextLost(),
        data_url: renderer.domElement.toDataURL('image/png'),
      };
      window.__qaImages[filename] = value.data_url;
      delete value.data_url;
      return value;
    }
    function singleCamera(bounds) {
      const size = bounds.getSize(new T.Vector3());
      const center = bounds.getCenter(new T.Vector3());
      const span = Math.max(size.x, size.y, size.z) * 1.48;
      const camera = new T.OrthographicCamera(-span / 2, span / 2, span / 2, -span / 2, 0.0001, span * 30);
      const azimuth = 35 * Math.PI / 180, elevation = 20 * Math.PI / 180;
      const direction = new T.Vector3(Math.sin(azimuth) * Math.cos(elevation), Math.sin(elevation), Math.cos(azimuth) * Math.cos(elevation));
      camera.position.copy(center).addScaledVector(direction, Math.max(size.length() * 3, 0.2));
      camera.lookAt(center);
      camera.updateProjectionMatrix();
      return camera;
    }
    for (const item of items) {
      const gltf = await loader.loadAsync('/models/' + item.id + '.glb');
      gltf.scene.updateMatrixWorld(true);
      const box = new T.Box3().setFromObject(gltf.scene);
      const size = box.getSize(new T.Vector3());
      const counts = countAsset(gltf);
      if (counts.triangles !== item.triangles || counts.mesh_nodes < 1) throw new Error(item.id + ': runtime triangle/mesh mismatch');
      if (![size.x, size.y, size.z].every(value => Number.isFinite(value) && value > 0)) throw new Error(item.id + ': invalid runtime bounds');
      const scene = new T.Scene();
      scene.background = new T.Color('#e9e5dc');
      scene.add(new T.HemisphereLight(0xffffff, 0x766d5b, 2.1));
      const key = new T.DirectionalLight(0xffffff, 2.3);
      key.position.set(-1, 2, 2);
      scene.add(key);
      scene.add(gltf.scene);
      renderer.setSize(512, 512);
      const frame = capture(scene, singleCamera(box), item.id + '-single.png');
      singleResults.push({
        id: item.id,
        revision: item.revision,
        glb_sha256: item.sha256,
        runtime_bounds_m: {min: box.min.toArray(), max: box.max.toArray(), size: size.toArray()},
        triangles: counts.triangles,
        mesh_nodes: counts.mesh_nodes,
        material_names: counts.material_names,
        scale: gltf.scene.scale.toArray(),
        render: frame,
      });
      loaded.push({item, gltf});
    }
    const layout = loaded.map(({item, gltf}, index) => {
      const group = gltf.scene.clone(true);
      group.updateMatrixWorld(true);
      const bounds = new T.Box3().setFromObject(group);
      const size = bounds.getSize(new T.Vector3());
      return {item, group, bounds, size, col: index % 2, row: Math.floor(index / 2)};
    });
    const gap = 0.05;
    const colWidths = [0, 0], rowDepths = [0, 0];
    for (const item of layout) {
      colWidths[item.col] = Math.max(colWidths[item.col], item.size.x);
      rowDepths[item.row] = Math.max(rowDepths[item.row], item.size.z);
    }
    const totalWidth = colWidths[0] + colWidths[1] + gap;
    const totalDepth = rowDepths[0] + rowDepths[1] + gap;
    const colCenters = [-totalWidth / 2 + colWidths[0] / 2, totalWidth / 2 - colWidths[1] / 2];
    const rowCenters = [-totalDepth / 2 + rowDepths[0] / 2, totalDepth / 2 - rowDepths[1] / 2];
    const scene = new T.Scene();
    scene.background = new T.Color('#e9e5dc');
    scene.add(new T.HemisphereLight(0xffffff, 0x766d5b, 2.1));
    const key = new T.DirectionalLight(0xffffff, 2.3);
    key.position.set(-1, 2, 2);
    scene.add(key);
    for (const item of layout) {
      const center = item.bounds.getCenter(new T.Vector3());
      item.group.position.set(colCenters[item.col] - center.x, -item.bounds.min.y, rowCenters[item.row] - center.z);
      scene.add(item.group);
    }
    const ground = new T.Mesh(new T.PlaneGeometry(totalWidth + 0.12, totalDepth + 0.12), new T.MeshStandardMaterial({color: '#d6d0c4', roughness: 1}));
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.002;
    scene.add(ground);
    scene.updateMatrixWorld(true);
    const modelBounds = new T.Box3();
    for (const item of layout) modelBounds.expandByObject(item.group);
    const sceneSize = modelBounds.getSize(new T.Vector3());
    const center = modelBounds.getCenter(new T.Vector3());
    const distance = Math.max(sceneSize.length() * 2.5, 1.0);
    const camera = new T.OrthographicCamera(-0.65, 0.65, 0.457, -0.457, 0.0001, distance * 20);
    function sceneCapture(filename, azimuth, elevation, topView) {
      const az = azimuth * Math.PI / 180, el = elevation * Math.PI / 180;
      const direction = new T.Vector3(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el));
      camera.position.copy(center).addScaledVector(direction, distance);
      if (topView) camera.up.set(0, 0, -1); else camera.up.set(0, 1, 0);
      camera.lookAt(center);
      camera.updateProjectionMatrix();
      const frame = capture(scene, camera, filename);
      return {name: filename, ...frame};
    }
    renderer.setSize(1280, 900);
    const sceneFrames = [
      sceneCapture('scene-hero.png', 35, 22, false),
      sceneCapture('scene-top.png', 0, 89, true),
    ];
    return {
      three_revision: T.REVISION,
      webgl2: gl instanceof WebGL2RenderingContext,
      gl_renderer: gl.getParameter(gl.RENDERER),
      unmasked_renderer: debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : null,
      assets: singleResults,
      scene: {
        description: 'Four exact candidate GLBs arranged in a 2x2 QA composition at authored scales; translation only; neutral QA ground plane excluded from model metrics.',
        instances: layout.length,
        scales: layout.map(item => ({id: item.item.id, scale: item.group.scale.toArray()})),
        translation_only: layout.every(item => item.group.scale.toArray().every(value => value === 1)),
        asset_triangles: singleResults.reduce((sum, item) => sum + item.triangles, 0),
        asset_mesh_nodes: singleResults.reduce((sum, item) => sum + item.mesh_nodes, 0),
        model_bounds_m: {min: modelBounds.min.toArray(), max: modelBounds.max.toArray(), size: sceneSize.toArray()},
        views: sceneFrames,
      },
    };
  }, specs);
  assert.equal(result.three_revision, '180');
  assert.equal(result.webgl2, true);
  assert.equal(result.assets.length, 4);
  assert.equal(result.scene.instances, 4);
  assert.equal(result.scene.translation_only, true);
  assert.equal(result.scene.asset_triangles, 23742);
  assert(result.assets.every(item => item.render.gl_error === 0 && !item.render.context_lost));
  assert(result.scene.views.every(item => item.gl_error === 0 && !item.context_lost));
  report.runtime = {
    three_version: result.three_revision,
    webgl2: result.webgl2,
    gl_renderer: result.gl_renderer,
    unmasked_renderer: result.unmasked_renderer,
  };
  report.parse_results = result.assets;
  report.scene = result.scene;
  const dataUrls = await page.evaluate(() => window.__qaImages);
  const screenshots = [];
  for (const [name, dataUrl] of Object.entries(dataUrls)) {
    const bytes = Buffer.from(dataUrl.split(',')[1], 'base64');
    const path = resolve(output, name);
    await writeFile(path, bytes);
    screenshots.push({path: path.slice(root.length + 1), bytes: bytes.length, sha256: digest(bytes)});
  }
  report.screenshots = screenshots;
  report.status = report.errors.length === 0 && report.resource_errors.length === 0 ? 'pass_limited_software_webgl' : 'fail';
} catch (error) {
  report.status = 'fail';
  report.error = error.stack || String(error);
  process.exitCode = 1;
} finally {
  await writeFile(resolve(output, 'runtime-report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({status: report.status, browser_version: report.browser_version, runtime: report.runtime, asset_triangles: report.scene && report.scene.asset_triangles, errors: report.errors, resource_errors: report.resource_errors}));
  await browser?.close();
  if (server.listening) await new Promise(ok => server.close(ok));
}
