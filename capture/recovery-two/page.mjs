/** New two-candidate representative scene; does not change the old twelve-model test. */
import * as T from 'three';
import {GLTFLoader} from '/modules/examples/jsm/loaders/GLTFLoader.js';

export async function renderFrame({items, view, browserVersion, width, height, gap}) {
  const shaderErrors = [];
  const scene = new T.Scene();
  scene.background = new T.Color('#e8e4dc');
  const renderer = new T.WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
  renderer.setPixelRatio(1);
  renderer.setSize(width, height);
  renderer.outputColorSpace = T.SRGBColorSpace;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  renderer.debug.checkShaderErrors = true;
  renderer.debug.onShaderError = (gl, program, vertex, fragment) => shaderErrors.push({program: gl.getProgramInfoLog(program), vertex: gl.getShaderInfoLog(vertex), fragment: gl.getShaderInfoLog(fragment)});
  document.body.replaceChildren(renderer.domElement);
  scene.add(new T.HemisphereLight(0xffffff, 0x777060, 2));
  const key = new T.DirectionalLight(0xffffff, 2.5);
  key.position.set(-1, 2, 2);
  scene.add(key);
  const loaded = [];
  for (const item of items) {
    const gltf = await new GLTFLoader().loadAsync(`/models/${item.id}.glb`);
    const group = new T.Group();
    group.add(gltf.scene);
    group.updateMatrixWorld(true);
    const box = new T.Box3().setFromObject(group, true);
    const size = box.getSize(new T.Vector3());
    const materials = new Set();
    let triangles = 0, meshes = 0;
    gltf.scene.traverse(o => {
      if (o.isMesh) {
        meshes++;
        triangles += (o.geometry.index?.count ?? o.geometry.attributes.position.count) / 3;
        for (const m of Array.isArray(o.material) ? o.material : [o.material]) materials.add(m.uuid);
      }
    });
    if (![size.x, size.y, size.z].every(n => Number.isFinite(n) && n > 0)) throw Error('Nonfinite/empty geometry');
    loaded.push({item, group, size, box, triangles, meshes, materials: materials.size});
  }
  const totalWidth = loaded.reduce((n, x) => n + x.size.x, 0) + gap * (loaded.length - 1);
  let x = -totalWidth / 2;
  for (const entry of loaded) {
    entry.group.position.set(x - entry.box.min.x, -entry.box.min.y, -entry.box.getCenter(new T.Vector3()).z);
    scene.add(entry.group);
    x += entry.size.x + gap;
  }
  scene.updateMatrixWorld(true);
  const bounds = new T.Box3();
  for (const entry of loaded) bounds.union(new T.Box3().setFromObject(entry.group, true));
  const center = bounds.getCenter(new T.Vector3());
  const radius = bounds.getSize(new T.Vector3()).length() / 2;
  const directions = {hero: [1, 0.6, 1.8], reversehero: [-1, 0.6, -1.8], front: [0, 0, 1], rear: [0, 0, -1], left: [-1, 0, 0], right: [1, 0, 0], top: [0, 1, 0], bottom: [0, -1, 0]};
  if (!directions[view]) throw Error('Unknown camera view');
  const aspect = width / height, vertical = radius * 2 * 1.15, horizontal = vertical * aspect;
  const distance = radius * 6;
  const camera = new T.OrthographicCamera(-horizontal / 2, horizontal / 2, vertical / 2, -vertical / 2, radius * 0.001, radius * 20);
  if (view === 'top') camera.up.set(0, 0, -1);
  if (view === 'bottom') camera.up.set(0, 0, 1);
  camera.position.copy(center).add(new T.Vector3(...directions[view]).normalize().multiplyScalar(distance));
  camera.lookAt(center);
  camera.updateProjectionMatrix();
  camera.updateMatrixWorld(true);
  const frustum = new T.Frustum().setFromProjectionMatrix(new T.Matrix4().multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse));
  // No animation. Exactly three real render submissions; record final-frame work.
  for (let frame = 0; frame < 3; frame++) {
    renderer.info.reset();
    renderer.render(scene, camera);
    await new Promise(requestAnimationFrame);
  }
  const gl = renderer.getContext();
  const debug = gl.getExtension('WEBGL_debug_renderer_info');
  const unmaskedRenderer = debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : null;
  const unmaskedVendor = debug ? gl.getParameter(debug.UNMASKED_VENDOR_WEBGL) : null;
  const pixels = new Uint8Array(width * height * 4);
  gl.readPixels(0, 0, width, height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
  let foreground = 0;
  for (let i = 0; i < pixels.length; i += 4) if (Math.abs(pixels[i] - pixels[0]) + Math.abs(pixels[i + 1] - pixels[1]) + Math.abs(pixels[i + 2] - pixels[2]) > 18) foreground++;
  const pixelDigest = [...new Uint8Array(await crypto.subtle.digest('SHA-256', pixels))].map(x => x.toString(16).padStart(2, '0')).join('');
  const assets = loaded.map(entry => {
    let inside = true;
    entry.group.traverse(o => { if (o.isMesh && !frustum.intersectsObject(o)) inside = false; });
    const box = new T.Box3().setFromObject(entry.group, true);
    let cornersInside = true;
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) if (!frustum.containsPoint(new T.Vector3(x, y, z))) cornersInside = false;
    return {id: entry.item.id, glb_sha256: entry.item.subject.glb_sha256, instances: 1, triangles: entry.triangles, meshes: entry.meshes, materials: entry.materials, authored_bounds: {min: entry.box.min.toArray(), max: entry.box.max.toArray()}, presentation_translation: entry.group.position.toArray(), presentation_scale: entry.group.scale.toArray(), presentation_rotation: [entry.group.rotation.x, entry.group.rotation.y, entry.group.rotation.z], all_meshes_in_frustum: inside, all_bounds_inside_clipping: cornersInside};
  });
  // Leave the static canvas intact for the Node-side screenshot and SHA256.
  return {
    view, runtime: {engine: 'Three.js', version: T.REVISION, renderer: unmaskedRenderer ?? gl.getParameter(gl.RENDERER), device: unmaskedRenderer ?? 'unmasked device unavailable', browser: browserVersion, context: gl instanceof WebGL2RenderingContext ? 'WebGL2' : 'not-WebGL2', output_color_space: renderer.outputColorSpace, tone_mapping: renderer.toneMapping === T.ACESFilmicToneMapping ? 'ACESFilmicToneMapping' : String(renderer.toneMapping), exposure: renderer.toneMappingExposure, context_created: true, rendered: renderer.info.render.calls > 0, rendered_frames: 3, draw_calls: renderer.info.render.calls, triangles: renderer.info.render.triangles},
    assets, context_lost: gl.isContextLost(), gl_error: gl.getError(), shader_errors: shaderErrors,
    foreground_pixels: foreground, framebuffer_rgba_sha256: pixelDigest,
    framebuffer: {width, height, bytes: pixels.length, row_origin: 'bottom-left'},
    gl_vendor: gl.getParameter(gl.VENDOR), gl_version: gl.getParameter(gl.VERSION), shading_language_version: gl.getParameter(gl.SHADING_LANGUAGE_VERSION), unmasked_vendor: unmaskedVendor,
    camera: {type: camera.type, position: camera.position.toArray(), up: camera.up.toArray(), target: center.toArray(), near: camera.near, far: camera.far, left: camera.left, right: camera.right, top: camera.top, bottom: camera.bottom},
    lighting: {hemisphere: {sky: '#ffffff', ground: '#777060', intensity: 2}, directional: {color: '#ffffff', intensity: 2.5, position: [-1, 2, 2]}},
  };
}
