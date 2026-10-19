/** Each route owns one application, including its styles and event listeners. */
import { parseRoute, normalizeSiteBase } from './routes.js';

export function routeApplication(pathname, siteRoot = '/') {
  return parseRoute(pathname, siteRoot).type === 'models' ? 'gallery' : 'site';
}

if (typeof document !== 'undefined') {
  const siteRoot = normalizeSiteBase(import.meta.env.BASE_URL);
  const application = routeApplication(location.pathname, siteRoot);
  document.documentElement.dataset.application = application;
  if (application === 'gallery') await import('./gallery/bootstrap.js');
  else await import('./main.js');
}
