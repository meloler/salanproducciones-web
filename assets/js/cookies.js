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

    var lastTicketEventKey = null;
    var lastTicketEventAt = 0;

    function trackTicketClick(event) {
        if (get() !== 'all' || !window.fbq) return;

        var target = event.target;
        var link = target && target.closest ? target.closest('a[href]') : null;
        if (!link) return;

        var href = link.getAttribute('href') || '';
        if (href.indexOf('tickety.es') === -1 && href.indexOf('entradas.plus') === -1) return;

        var now = Date.now();
        var eventKey = href;
        if (lastTicketEventKey === eventKey && now - lastTicketEventAt < 1500) return;
        lastTicketEventKey = eventKey;
        lastTicketEventAt = now;

        window.fbq('trackCustom', 'TicketClick', {
            content_name: 'Ticket click',
            content_category: 'Concert tickets',
            destination_url: href
        });
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
        document.addEventListener('pointerdown', trackTicketClick);
        document.addEventListener('touchstart', trackTicketClick);
        document.addEventListener('click', trackTicketClick);
        if (!get()) show();
    });
})();
