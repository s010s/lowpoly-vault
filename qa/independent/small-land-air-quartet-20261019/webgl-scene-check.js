import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const ASSETS = [
  {id: 'sapeornis', path: '/production/concept-small-land-air-20261019/sapeornis/r001/output/sapeornis/sapeornis.glb', sha256: '7b0aef80ee8327ebc06a8372fc63fce63c393a62451820b4bd183ff868b2755b'},
  {id: 'longirostravis', path: '/production/concept-small-land-air-20261019/longirostravis/r001/output/longirostravis/longirostravis.glb', sha256: '10668416201cf7ec57e48285019fcd0738e6bb69665fd8fb519559aabaa6bd83'},
  {id: 'dunbaria', path: '/production/concept-small-land-air-20261019/dunbaria/r001/output/dunbaria/dunbaria.glb', sha256: '2f584412b3318fa3969e6b008271df107f73fe9f00c8f304c04bfa47e134311e'},
  {id: 'chimerarachne', path: '/production/concept-small-land-air-20261019/chimerarachne/r001/output/chimerarachne/chimerarachne.glb', sha256: '848328130f8874bc6c81b0636d8bfc78f76d04b46cfa0786fe7d978f28e3ad6c'}
];

const status = document.querySelector('#status');
const canvas = document.querySelector('#scene');
const loader = new GLTFLoader();
const renderer = new THREE.WebGLRenderer({canvas, antialias: false, alpha: false, powerPreference: 'low-power', failIfMajorPerformanceCaveat: false});
renderer.setPixelRatio(1);
renderer.setSize(1280, 720, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NoToneMapping;
renderer.toneMappingExposure = 1;
renderer.setClearColor(0xe8e4dc, 1);

function hex(bytes) {
  return Array.from(new Uint8Array(bytes), value => value.toString(16).padStart(2, '0')).join('');
}

async function digestResponse(path) {
  const response = await fetch(path, {cache: 'no-store'});
  if (!response.ok) throw new Error('GLB fetch failed for ' + path + ': HTTP ' + response.status);
  const bytes = await response.arrayBuffer();
  return {bytes, sha256: hex(await crypto.subtle.digest('SHA-256', bytes))};
}

function meshStats(root) {
  const meshes = [];
  const materialNames = new Set();
  let triangles = 0;
  root.traverse(object => {
    if (!object.isMesh) return;
    meshes.push(object);
    const geometry = object.geometry;
    const count = geometry.index ? geometry.index.count : geometry.attributes.position.count;
    const mode = geometry.userData?.mode;
    if (mode && mode !== 4) throw new Error('Unsupported GLTF primitive mode for ' + object.name + ': ' + mode);
    triangles += Math.floor(count / 3);
    for (const material of (Array.isArray(object.material) ? object.material : [object.material])) {
      if (material) materialNames.add(material.name || '(unnamed)');
    }
  });
  return {meshes, triangles, materialNames: Array.from(materialNames).sort()};
}

function addLighting(scene, span) {
  scene.add(new THREE.HemisphereLight(0xffffff, 0xb4aea3, 1.3));
  const key = new THREE.DirectionalLight(0xffffff, 2.0);
  key.position.set(span * -0.25, span * 0.8, span * 0.7);
  scene.add(key);
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(span * 1.8, span * 1.8),
    new THREE.MeshStandardMaterial({color: 0xd8d4cc, roughness: 1})
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.003;
  scene.add(ground);
}

function placeClone(scene, asset, xCenter, zCenter) {
  const clone = asset.scene.clone(true);
  clone.position.x = xCenter - asset.center[0];
  clone.position.y = -asset.bounds.min.y;
  clone.position.z = zCenter - asset.center[2];
  clone.updateMatrixWorld(true);
  scene.add(clone);
  return clone;
}

function assembleScenario(id, instanceCountPerAsset, gap) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0xe8e4dc);
  const allInstances = [];
  let outerWidth;
  let outerDepth;
  if (id === 'one-each') {
    outerWidth = ASSETS.reduce((sum, item) => sum + loaded[item.id].size.x, 0) + gap * (ASSETS.length - 1);
    let cursor = -outerWidth / 2;
    for (const item of ASSETS) {
      const asset = loaded[item.id];
      const size = asset.size.x;
      allInstances.push(placeClone(scene, asset, cursor + size / 2, 0));
      cursor += size + gap;
    }
    outerDepth = Math.max(...ASSETS.map(item => loaded[item.id].size.z));
  } else {
    outerWidth = (instanceCountPerAsset - 1) * gap + Math.max(...ASSETS.map(item => loaded[item.id].size.x));
    outerDepth = (ASSETS.length - 1) * gap + Math.max(...ASSETS.map(item => loaded[item.id].size.z));
    for (let row = 0; row < ASSETS.length; row++) {
      const item = ASSETS[row];
      const asset = loaded[item.id];
      const zCenter = row * gap - ((ASSETS.length - 1) * gap) / 2;
      for (let col = 0; col < instanceCountPerAsset; col++) {
        const xCenter = col * gap - ((instanceCountPerAsset - 1) * gap) / 2;
        allInstances.push(placeClone(scene, asset, xCenter, zCenter));
      }
    }
  }
  const span = Math.max(outerWidth, outerDepth, 1);
  addLighting(scene, span);
  scene.updateMatrixWorld(true);
  const contentBounds = new THREE.Box3();
  for (const child of allInstances) contentBounds.expandByObject(child);
  const center = contentBounds.getCenter(new THREE.Vector3());
  const width = Math.max(outerWidth, outerDepth * (1280 / 720)) * 1.12;
  const height = width * (720 / 1280);
  const camera = new THREE.OrthographicCamera(-width / 2, width / 2, height / 2, -height / 2, 0.001, Math.max(100, span * 20));
  camera.position.set(center.x, center.y + span * 0.28, center.z + span * 0.62);
  camera.up.set(0, 1, 0);
  camera.lookAt(center);
  camera.updateProjectionMatrix();
  return {scene, camera, allInstances, bounds: {width: outerWidth, depth: outerDepth}, cameraWidth: width};
}

const loaded = {};

async function loadAssets() {
  for (const item of ASSETS) {
    const bytes = await digestResponse(item.path);
    if (bytes.sha256 !== item.sha256) throw new Error('Frozen GLB hash mismatch: ' + item.id + ' actual=' + bytes.sha256 + ' expected=' + item.sha256);
    const gltf = await loader.loadAsync(item.path);
    gltf.scene.updateMatrixWorld(true);
    const box = new THREE.Box3().setFromObject(gltf.scene);
    const stats = meshStats(gltf.scene);
    loaded[item.id] = {
      scene: gltf.scene,
      bounds: box,
      center: box.getCenter(new THREE.Vector3()).toArray(),
      size: box.getSize(new THREE.Vector3()),
      stats,
      sha256: bytes.sha256,
      bytes: bytes.bytes.byteLength
    };
  }
}

async function measureScenario(id, count) {
  const arranged = assembleScenario(id, count, id === 'one-each' ? 0.18 : (id === 'normal-8-each' ? 1.05 : 0.9));
  renderer.info.reset();
  for (let warmup = 0; warmup < 3; warmup++) renderer.render(arranged.scene, arranged.camera);
  const sampleMs = [];
  for (let sample = 0; sample < 8; sample++) {
    const start = performance.now();
    renderer.render(arranged.scene, arranged.camera);
    sampleMs.push(performance.now() - start);
  }
  sampleMs.sort((a, b) => a - b);
  const gl = renderer.getContext();
  const dataUrl = canvas.toDataURL('image/png');
  return {
    id,
    instances_per_asset: id === 'one-each' ? 1 : count,
    instances_total: arranged.allInstances.length,
    instance_scale: [1, 1, 1],
    scene_content_bounds_m: arranged.bounds,
    camera_orthographic_width_m: arranged.cameraWidth,
    render_calls: renderer.info.render.calls,
    rendered_triangles: renderer.info.render.triangles,
    shader_program_count: renderer.info.programs?.length ?? null,
    frame_ms_samples: sampleMs,
    frame_ms_median: sampleMs[4],
    frame_ms_max: sampleMs[sampleMs.length - 1],
    canvas_png_data_url: dataUrl,
    gl_renderer: gl.getParameter(gl.RENDERER),
    gl_version: gl.getParameter(gl.VERSION),
    webgl_context_lost: gl.isContextLost()
  };
}

window.qaRun = async () => {
  try {
    status.textContent = 'Loading and parsing the four frozen GLBs.';
    await loadAssets();
    const gl = renderer.getContext();
    const assets = Object.fromEntries(ASSETS.map(item => {
      const value = loaded[item.id];
      return [item.id, {
        path: item.path,
        sha256: value.sha256,
        bytes: value.bytes,
        glb_bounds_xyz_m: value.size.toArray(),
        triangles_per_instance: value.stats.triangles,
        mesh_objects_per_instance: value.stats.meshes.length,
        material_names: value.stats.materialNames,
        scale: [1, 1, 1]
      }];
    }));
    const scenarios = [];
    status.textContent = 'Rendering native-scale one-each, 8-copy, and 32-copy scenes.';
    scenarios.push(await measureScenario('one-each', 1));
    scenarios.push(await measureScenario('normal-8-each', 8));
    scenarios.push(await measureScenario('stress-32-each', 32));
    const debugRenderer = gl.getExtension('WEBGL_debug_renderer_info');
    window.qaResult = {
      schema_version: 1,
      kind: 'software_webgl_scene_report',
      stage: 'gpu_and_scene_limited',
      runtime: {
        three_version: THREE.REVISION,
        engine: 'Three.js WebGLRenderer in headless Chromium with SwiftShader requested',
        browser_user_agent: navigator.userAgent,
        gl_vendor: gl.getParameter(gl.VENDOR),
        gl_renderer: gl.getParameter(gl.RENDERER),
        unmasked_gl_vendor: debugRenderer ? gl.getParameter(debugRenderer.UNMASKED_VENDOR_WEBGL) : null,
        unmasked_gl_renderer: debugRenderer ? gl.getParameter(debugRenderer.UNMASKED_RENDERER_WEBGL) : null,
        debug_renderer_info_available: Boolean(debugRenderer),
        gl_version: gl.getParameter(gl.VERSION),
        glsl_version: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
        context_type: 'WebGL2RenderingContext',
        output_color_space: renderer.outputColorSpace,
        tone_mapping: 'NoToneMapping',
        exposure: renderer.toneMappingExposure,
        context_created: true,
        rendered: true,
        rendered_frames: 3 * 11,
        context_lost: gl.isContextLost()
      },
      assets,
      scenarios
    };
    status.textContent = 'Rendered. Exact GLB hashes and per-scene metrics are available in window.qaResult.';
    return window.qaResult;
  } catch (error) {
    status.textContent = 'FAILED: ' + (error.stack || error.message || String(error));
    throw error;
  }
};
