// Service Worker for AI Doctor PWA
const CACHE_NAME = 'ai-doctor-v1';
const urlsToCache = [
    '/',
    '/static/css/styles.css',
    '/static/js/main.js',
    '/static/images/logo.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            })
    );
});