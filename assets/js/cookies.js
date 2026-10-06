(function () {
    var KEY    = 'salan_consent';
    var GTM_ID = 'GTM-MMDNKZDQ';
    var META_PIXEL_ID = '1011468751859822';

    function get()      { try { return localStorage.getItem(KEY); }        catch (e) { return null; } }
    function set(v)     { try { localStorage.setItem(KEY, v); }            catch (e) {} }
    function banner()   { return document.getElementById('cookie-banner'); }
    function hide()     { var b = banner(); if (b) b.style.display = 'none'; }
    function show()     { var b = banner(); if (b) b.style.display = 'flex'; }

    function loadGTM() {
        if (document.getElementById('salan-gtm')) return;
        var w = window, d = document;
        w.dataLayer = w.dataLayer || [];
        w.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
        var f = d.getElementsByTagName('script')[0];
        var j = d.createElement('script');
        j.id    = 'salan-gtm';
        j.async = true;
        j.src   = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
        f.parentNode.insertBefore(j, f);
        var ns = d.createElement('noscript');
        ns.innerHTML = '<iframe src="https://www.googletagmanager.com/ns.html?id=' + GTM_ID + '" height="0" width="0" style="display:none;visibility:hidden"></iframe>';
        if (d.body) d.body.insertBefore(ns, d.body.firstChild);
    }

    function loadMetaPixel() {
        if (window.fbq && window.fbq.loaded) {
            window.fbq('track', 'PageView');
            return;
        }

        var f = window;
        var b = document;
        var e = 'script';
        var v = 'https://connect.facebook.net/en_US/fbevents.js';
        var n, t, s;

        if (f.fbq) return;
        n = f.fbq = function () {
            n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
        };
        if (!f._fbq) f._fbq = n;
        n.push = n;
        n.loaded = true;
        n.version = '2.0';
        n.queue = [];

        t = b.createElement(e);
        t.async = true;
        t.src = v;
        s = b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t, s);

        f.fbq('init', META_PIXEL_ID);
        f.fbq('track', 'PageView');
    }

    function loadMarketingTags() {
        loadGTM();
        loadMetaPixel();
    }

    var TICKET_PROVIDER_HOSTS = Object.freeze({
        'auditorioalfredokraus.es': 'auditorio_alfredo_kraus',
        'tickety.es': 'tickety',
        'tureservaonline.es': 'tureservaonline',
        'entradium.com': 'entradium',
        'entradas.babylonmadrid.com': 'babylon_madrid',
        'entradas.elteatroguiniguada.com': 'teatro_guiniguada'
    });

    function ticketProvider(href) {
        try {
            var url = new URL(href, window.location.href);
            if (url.protocol !== 'https:' || url.username || url.password) return null;
            var host = url.hostname.toLowerCase().replace(/^www\./, '');
            if (host === 'entradas.plus' || host.slice(-14) === '.entradas.plus') return 'entradas_plus';
            return TICKET_PROVIDER_HOSTS[host] || null;
        } catch (error) {
            return null;
        }
    }

    function eventIdFor(link) {
        var tagged = link.closest('[data-analytics-event-id]');
        if (tagged && tagged.dataset.analyticsEventId) return tagged.dataset.analyticsEventId;

        var legacyTagged = link.closest('[data-event-id]');
        if (legacyTagged && legacyTagged.dataset.eventId) return legacyTagged.dataset.eventId;

        var canonical = document.querySelector('link[rel="canonical"][href]');
        if (!canonical) return '';
        try {
            var segments = new URL(canonical.href).pathname.split('/').filter(Boolean);
            if (segments[0] === 'en' || segments[0] === 'de') segments.shift();
            var yearIndex = segments.findIndex(function (segment) { return /^\d{4}$/.test(segment); });
            if (yearIndex >= 0) return segments.slice(yearIndex + 1).join('-');
            return segments.slice(-2).join('-');
        } catch (error) {
            return '';
        }
    }

    function cityFor(link) {
        var tagged = link.closest('[data-analytics-city]');
        if (tagged && tagged.dataset.analyticsCity) return tagged.dataset.analyticsCity;

        var scripts = document.querySelectorAll('script[type="application/ld+json"]');
        for (var i = 0; i < scripts.length; i++) {
            try {
                var data = JSON.parse(scripts[i].textContent);
                var entries = Array.isArray(data) ? data : (Array.isArray(data['@graph']) ? data['@graph'] : [data]);
                for (var j = 0; j < entries.length; j++) {
                    var entry = entries[j];
                    var types = Array.isArray(entry['@type']) ? entry['@type'] : [entry['@type']];
                    var location = entry.location;
                    var city = location && location.address && location.address.addressLocality;
                    if (types.some(function (type) { return typeof type === 'string' && /Event$/.test(type); }) && city) return city;
                }
            } catch (error) {}
        }
        return '';
    }

    function buttonLocationFor(link) {
        var tagged = link.closest('[data-analytics-location]');
        if (tagged && tagged.dataset.analyticsLocation) return tagged.dataset.analyticsLocation;
        if (link.closest('.concert-card, .carousel-item')) return 'concert_card';
        if (link.closest('.tour-sticky')) return 'tour_sticky';
        if (link.closest('.tour-selector')) return 'tour_selector';
        if (link.closest('.cta-group-proyecto')) return 'cultural_project';
        if (link.closest('.final-box')) return 'event_final';
        return 'event_page';
    }

    function trackTicketClick(event) {
        if (!event.isTrusted || event.defaultPrevented || get() !== 'all' || typeof window.fbq !== 'function') return;

        var target = event.target;
        var link = target && target.closest ? target.closest('a[href]') : null;
        if (!link) return;

        var provider = ticketProvider(link.href);
        if (!provider) return;
        var concertId = eventIdFor(link);
        if (!concertId) return;
        var language = (document.documentElement.lang || '').split('-')[0].toLowerCase();
        var properties = {
            content_name: 'Ticket click',
            content_category: 'Concert tickets',
            concert_id: concertId,
            language: language,
            button_location: buttonLocationFor(link),
            ticket_provider: provider
        };
        var city = cityFor(link);
        if (city) properties.city = city;

        try {
            window.fbq('trackCustom', 'TicketClick', properties);
        } catch (error) {}
    }

    function acceptAll() {
        set('all');
        loadMarketingTags();
        hide();
    }

    function acceptNecessary() {
        set('necessary');
        hide();
    }

    // Allow footer "Cookies" link to reopen banner
    window.salanCookiesOpen = function () {
        localStorage.removeItem(KEY);
        show();
    };

    // On load: apply saved preference
    var consent = get();
    if (consent === 'all') {
        loadMarketingTags();
    }

    // Wire buttons and show banner if no preference yet
    document.addEventListener('DOMContentLoaded', function () {
        var btnAll = document.getElementById('ck-accept-all');
        var btnNec = document.getElementById('ck-accept-necessary');
        if (btnAll) btnAll.addEventListener('click', acceptAll);
        if (btnNec) btnNec.addEventListener('click', acceptNecessary);
        document.addEventListener('click', trackTicketClick);
        if (!get()) show();
    });
})();
