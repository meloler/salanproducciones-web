(function () {
    var KEY    = 'salan_consent';
    var GTM_ID = 'GTM-MMDNKZDQ';

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

    function acceptAll() {
        set('all');
        loadGTM();
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
        loadGTM();
    }

    // Wire buttons and show banner if no preference yet
    document.addEventListener('DOMContentLoaded', function () {
        var btnAll = document.getElementById('ck-accept-all');
        var btnNec = document.getElementById('ck-accept-necessary');
        if (btnAll) btnAll.addEventListener('click', acceptAll);
        if (btnNec) btnNec.addEventListener('click', acceptNecessary);
        if (!get()) show();
    });
})();
