/* Offline support. The app shell and data are cached on install; images are cached as they are viewed.
   VERSION is rewritten by tools/build.py whenever the site files change. */
const VERSION = '6d5aaff3c5';
const SHELL = `shell-${VERSION}`, IMAGES = 'images-v1', MAX_IMAGES = 400;
const FILES = ['./', 'index.html', 'assets/app.css', 'assets/app.js', 'data/site.js', 'favicon.svg', 'manifest.webmanifest'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('shell-') && k !== SHELL).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});

async function trim(cache) {
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - MAX_IMAGES; i++) await cache.delete(keys[i]);
}

self.addEventListener('fetch', e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;
  if (/\.(webp|jpg|png)$/.test(url.pathname)) {
    e.respondWith(caches.open(IMAGES).then(async c => {
      const hit = await c.match(req); if (hit) return hit;
      const res = await fetch(req); if (res.ok) { c.put(req, res.clone()); trim(c); } return res;
    }));
    return;
  }
  e.respondWith(fetch(req).then(res => {
    if (res.ok) { const copy = res.clone(); caches.open(SHELL).then(c => c.put(req, copy)); }
    return res;
  }).catch(async () => (await caches.match(req)) || (await caches.match(req, { ignoreSearch: true })) || (await caches.match('index.html'))));
});
