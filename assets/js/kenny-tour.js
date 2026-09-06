/* Progressive enhancement: all ten ticket links also exist in the HTML. */
(function () {
  'use strict';
  const data = document.getElementById('kenny-dates');
  if (!data) return;
  const cities = JSON.parse(data.textContent);
  const select = document.getElementById('tour-city');
  const params = new URLSearchParams(location.search);
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'fbclid'];
  const tracking = new URLSearchParams();
  keys.forEach(key => { if (params.get(key)) tracking.set(key, params.get(key)); });
  if (!keys.slice(0, 5).some(key => tracking.has(key))) {
    tracking.set('utm_source', 'landing');
    tracking.set('utm_medium', 'web');
    tracking.set('utm_campaign', 'kenny-blues-boss-wayne-gira-espana-2026');
  }
  function ticketUrl(city) {
    const url = new URL(city.url);
    tracking.forEach((value, key) => url.searchParams.set(key, value));
    return url.href;
  }
  function activate(id, updateHash) {
    const city = cities[id];
    if (!city) return;
    if (select) select.value = id;
    Object.entries({ 'tac-city': city.name, 'tac-date': city.dateLabel,
      'tac-venue': city.venue, 'tac-price': city.priceLabel, 'tac-note': city.note,
      'sticky-city': city.name + ' · ' + city.priceLabel, 'sticky-date': city.dateLabel
    }).forEach(([key, value]) => { document.getElementById(key).textContent = value; });
    ['tac-btn', 'sticky-buy'].forEach(key => {
      const link = document.getElementById(key);
      link.href = ticketUrl(city);
      link.setAttribute('aria-label', link.textContent.trim() + ' — ' + city.name);
    });
    if (updateHash) history.replaceState(null, '', location.pathname + location.search + '#' + id);
    // Preserve the selected city and campaign when changing language.
    document.querySelectorAll('a[href]').forEach(link => {
      const url = new URL(link.href);
      if (url.origin === location.origin && url.pathname.includes('/kenny-blues-boss-wayne-gira-espana-2026/') && url.pathname !== location.pathname) {
        url.search = location.search;
        url.hash = id;
        link.href = url.href;
      }
    });
  }
  const selector = document.querySelector('.tour-selector');
  if (selector) selector.hidden = false;
  document.querySelectorAll('[data-ticket-city]').forEach(link => {
    link.href = ticketUrl(cities[link.dataset.ticketCity]);
  });
  const today = new Intl.DateTimeFormat('sv-SE', { timeZone: 'Europe/Madrid' }).format(new Date());
  const next = Object.keys(cities).find(id => cities[id].date >= today) || Object.keys(cities)[0];
  activate(Object.hasOwn(cities, location.hash.slice(1)) ? location.hash.slice(1) : next, false);
  if (select) select.addEventListener('change', () => activate(select.value, true));
  window.addEventListener('hashchange', () => activate(location.hash.slice(1), false));
  const sticky = document.querySelector('.tour-sticky');
  const cookie = document.getElementById('cookie-banner');
  function syncCookie() {
    // The purchase bar never covers the consent dialog or competes with it.
    sticky.hidden = !!cookie && getComputedStyle(cookie).display !== 'none';
  }
  if (cookie) new MutationObserver(syncCookie).observe(cookie, { attributes: true, attributeFilter: ['style'] });
  syncCookie();
})();
