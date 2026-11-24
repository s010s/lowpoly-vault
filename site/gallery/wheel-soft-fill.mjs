export const EXACT_ID = 'ecphora';
export const EXACT_GLTF_SHA = 'b51a98cbc3c14469f8988e908faddf56f93e7622a9fd39e335930fe3c46e5392';

// Diagnostic only. entry must be the verified resource() result, not asset.sha256.
export function installWheelSoftFill(view, asset, entry, DirectionalLight, route) {
  if (route !== 'wheel-poster' && route !== 'wheel-hover') return false;
  if (asset?.id !== EXACT_ID || entry?.sha256 !== EXACT_GLTF_SHA) return false;
  if (view?.asset !== asset || view?.entry !== entry || !view?.scene || !view?.camera) return false;
  const name = 'scratch:ecphora-wheel-soft-fill';
  if (view.scene.getObjectByName(name)) return false;
  const light = new DirectionalLight(0xfff4e8, 0.62);
  light.name = name;
  light.position.set(3.5, 0.85, 4.6);
  light.castShadow = false;
  // Isolate to the view scene; don't mutate renderer exposure, camera, model or other scenes.
  view.scene.add(light);
  return true;
}
