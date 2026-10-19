/** Resolve all gallery assets against the deployment prefix, never a nested route. */
export const siteRoot = new URL(import.meta.env?.BASE_URL || globalThis.document?.body?.dataset.siteBase || '/', globalThis.location?.origin || 'http://localhost/');
export function assetURL(value) {
  if (typeof value !== 'string' || !value || /[\\\u0000-\u001f]/.test(value)) return '';
  const url = new URL(value, siteRoot);
  return url.origin === siteRoot.origin && url.pathname.startsWith(siteRoot.pathname) ? url.href : '';
}
