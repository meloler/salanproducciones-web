import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'c:\Users\Juan\Desktop\webpapa thedoors\salanproducciones'

SITE_HTML = [
    'index.html',
    'contacto/index.html',
    'pub-la-calle/index.html',
    'conciertos-anteriores/index.html',
    'conciertos/PLANTILLA-evento.html',
    'conciertos/2026/acantha-lang-junio-gira-e-04-06-2026/index.html',
    'conciertos/2026/acantha-lang-tour-espana-28-06-2026/index.html',
    'conciertos/2026/alvaro-suite-gran-canaria-01-05-2026/index.html',
    'conciertos/2026/alvaro-suite-tenerife-30-04-2026/index.html',
    'conciertos/2026/ana-curra-11-04-2026/index.html',
    'conciertos/2026/bywater-call-16-06-2026/index.html',
    'conciertos/2026/bywater-call-17-06-2026/index.html',
    'conciertos/2026/clearwater-creedence-revival-el-sauzal-13-11-2026/index.html',
    'conciertos/2026/clearwater-creedence-revival-telde-14-11-2026/index.html',
    'conciertos/2026/kenny-blues-boss-wayne-gira-espana-2026/index.html',
    'conciertos/2026/poseidon-rock-fest-13-06-2026/index.html',
]

COOKIE_BANNER = '''
<div id="cookie-banner" style="display:none;position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#111111;border-top:1px solid #2a2a2a;padding:18px 24px;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap">
  <p style="margin:0;font-size:.85rem;color:#888;max-width:680px;line-height:1.5">
    Usamos cookies propias y de terceros (Google Analytics, Meta Pixel) para anal\\u00edtica y publicidad. Puedes aceptar todas o solo las necesarias para el funcionamiento del sitio.
    <a href="/cookies/" style="color:#e8c44d;text-decoration:underline">M\\u00e1s informaci\\u00f3n</a>
  </p>
  <div style="display:flex;gap:12px;flex-shrink:0;flex-wrap:wrap">
    <button id="ck-accept-necessary" style="padding:10px 20px;background:transparent;color:#888;border:1px solid #2a2a2a;border-radius:4px;cursor:pointer;font-size:.85rem;font-family:inherit;white-space:nowrap">Solo necesarias</button>
    <button id="ck-accept-all" style="padding:10px 20px;background:#e8c44d;color:#000;border:none;border-radius:4px;cursor:pointer;font-size:.85rem;font-weight:700;font-family:inherit;white-space:nowrap">Aceptar todo</button>
  </div>
</div>'''

# GTM patterns to remove
GTM_HEAD = re.compile(
    r'\s*<!-- Google Tag Manager[^>]*-->\s*\n\s*<script>\(function[^<]+GTM-MMDNKZDQ[^<]+</script>',
    re.DOTALL
)
GTM_BODY = re.compile(
    r'\s*<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html\?id=GTM-MMDNKZDQ"[^>]*></iframe></noscript>'
)

# Footer legal link patterns
FOOTER_LEGAL_RE = re.compile(
    r'(<div class="footer-legal">)([\s\S]*?)(</div>)',
)

FOOTER_LEGAL_NEW = (
    '<div class="footer-legal">\n'
    '        <a href="/privacidad/">Privacidad</a>\n'
    '        <a href="/aviso-legal/">Aviso legal</a>\n'
    '        <a href="/cookies/" onclick="window.salanCookiesOpen &amp;&amp; window.salanCookiesOpen(); return false;">Cookies</a>\n'
    '      </div>'
)

for rel in SITE_HTML:
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f'  SKIP: {rel}')
        continue

    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    orig = html

    # 1. Remove GTM from <head>
    html = GTM_HEAD.sub('', html)

    # 2. Remove GTM noscript from <body>
    html = GTM_BODY.sub('', html)

    # 3. Update footer legal links
    html = FOOTER_LEGAL_RE.sub(FOOTER_LEGAL_NEW, html, count=1)

    # 4. Update contacto form privacy link
    html = html.replace(
        'href="#" style="color:var(--gold);text-decoration:underline">Política de privacidad',
        'href="/privacidad/" style="color:var(--gold);text-decoration:underline">Política de privacidad'
    )

    # 5. Add cookie banner + cookies.js before </body> if not already there
    if 'cookie-banner' not in html:
        html = html.replace(
            '<script src="/assets/js/main.js" defer></script>\n</body>',
            COOKIE_BANNER + '\n\n<script src="/assets/js/cookies.js"></script>\n<script src="/assets/js/main.js" defer></script>\n</body>'
        )
        # fallback if lite-yt-embed is also present
        if 'cookie-banner' not in html:
            html = html.replace(
                '</body>',
                COOKIE_BANNER + '\n\n<script src="/assets/js/cookies.js"></script>\n</body>',
                1
            )

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        tags = []
        if 'GTM' not in html or 'salan-gtm' not in html: tags.append('gtm-removed')
        if 'cookie-banner' in html:                       tags.append('banner')
        if '/privacidad/' in html:                        tags.append('footer-links')
        print(f'  OK  {rel}  [{", ".join(tags)}]')
    else:
        print(f'  --  {rel}  (sin cambios)')

print('\nDone.')
