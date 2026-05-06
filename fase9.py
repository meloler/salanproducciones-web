import os, re, sys, urllib.request
from PIL import Image

# Fix Windows console encoding
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

# --- 1. lite-youtube-embed
print('=== 1. Descargando lite-youtube-embed ===')
LYE_BASE = 'https://cdn.jsdelivr.net/npm/lite-youtube-embed@0.3.2/src'
for fname, folder in [('lite-yt-embed.css', 'assets/css'), ('lite-yt-embed.js', 'assets/js')]:
    dst = os.path.join(BASE, folder, fname)
    if not os.path.exists(dst):
        urllib.request.urlretrieve(f'{LYE_BASE}/{fname}', dst)
        print(f'  Descargado {fname} ({os.path.getsize(dst)//1024} KB)')
    else:
        print(f'  Ya existe: {fname}')

# --- 2. Imagenes grandes a WebP
print('\n=== 2. Imagenes a WebP ===')

def to_webp(rel_path, quality=82):
    src = os.path.join(BASE, rel_path)
    dst_rel = re.sub(r'\.(jpe?g|png)$', '.webp', rel_path, flags=re.IGNORECASE)
    dst = os.path.join(BASE, dst_rel)
    img = Image.open(src)
    mode = 'RGBA' if img.mode in ('RGBA', 'P') else 'RGB'
    img.convert(mode).save(dst, 'WEBP', quality=quality)
    src_kb = os.path.getsize(src) // 1024
    dst_kb = os.path.getsize(dst) // 1024
    print(f'  {src_kb:>5} KB -> {dst_kb:>4} KB  {dst_rel}')

to_webp('assets/images/pub-la-calle-interior.jpeg', quality=82)
to_webp('assets/images/juan-salan.jpeg', quality=82)
to_webp('assets/images/logo-desde-1987.png', quality=88)

# --- 3. Favicon
print('\n=== 3. Favicon ===')
fav_path = os.path.join(BASE, 'assets/favicon.ico')
orig_kb  = os.path.getsize(fav_path) // 1024
img = Image.open(fav_path).convert('RGBA').resize((48, 48), Image.LANCZOS)
img.save(fav_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48)])
new_kb = os.path.getsize(fav_path) // 1024
print(f'  {orig_kb} KB -> {new_kb} KB  favicon.ico')

# --- 4. main.css: quitar @import, png->webp
print('\n=== 4. main.css ===')
css_path = os.path.join(BASE, 'assets/css/main.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()
css_new = re.sub(
    r"/\* --- Google Fonts import --- \*/\n@import url\('[^']+'\);\n\n",
    '', css
)
css_new = css_new.replace('logo-desde-1987.png', 'logo-desde-1987.webp')
if css_new != css:
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_new)
    print('  main.css actualizado')
else:
    print('  main.css sin cambios')

# --- 5+6. HTML: Google Fonts + lite-youtube + img refs
FONTS_LINKS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap">'
)

IFRAME_RE = re.compile(
    r'<iframe[^>]*?youtube\.com/embed/([A-Za-z0-9_-]+)[^"]*"[^>]*?>[\s\S]*?</iframe>',
    re.DOTALL
)

def replace_iframes(html):
    def repl(m):
        iframe  = m.group(0)
        vid_id  = m.group(1)
        title_m = re.search(r'title="([^"]*)"', iframe)
        title   = title_m.group(1) if title_m else 'Video'
        return f'<lite-youtube videoid="{vid_id}" title="{title}"></lite-youtube>'
    return IFRAME_RE.sub(repl, html)

def fix_fonts(html):
    if 'fonts.gstatic.com' in html and 'family=Oswald' in html:
        return html
    # Quitar preconnect parcial si existe
    html = re.sub(r'[ \t]*<link rel="preconnect" href="https://fonts\.googleapis\.com"[^>]*>\n', '', html)
    # Insertar bloque completo antes de main.css
    html = re.sub(
        r'(<link[^>]*assets/css/main\.css[^>]*>)',
        FONTS_LINKS + '\n    ' + r'\1',
        html, count=1
    )
    return html

print('\n=== 5+6. HTML ===')
for rel in SITE_HTML:
    path = os.path.join(BASE, rel)
    if not os.path.exists(path):
        print(f'  SKIP: {rel}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    html_orig = html

    html = fix_fonts(html)
    html = replace_iframes(html)

    if '<lite-youtube' in html:
        if 'lite-yt-embed.css' not in html:
            html = re.sub(
                r'(<link[^>]*assets/css/main\.css[^>]*>)',
                r'\1\n    <link rel="stylesheet" href="/assets/css/lite-yt-embed.css">',
                html, count=1
            )
        if 'lite-yt-embed.js' not in html:
            html = html.replace(
                '<script src="/assets/js/main.js" defer></script>',
                '<script src="/assets/js/lite-yt-embed.js" defer></script>\n<script src="/assets/js/main.js" defer></script>'
            )

    html = html.replace('pub-la-calle-interior.jpeg', 'pub-la-calle-interior.webp')
    html = html.replace('juan-salan.jpeg',            'juan-salan.webp')
    html = html.replace('logo-desde-1987.png',        'logo-desde-1987.webp')

    if html != html_orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        tags = []
        if 'fonts.gstatic.com' in html:                       tags.append('fonts')
        if '<lite-youtube' in html:                            tags.append('lite-yt')
        if 'juan-salan.webp' in html or 'pub-la-calle-interior.webp' in html: tags.append('img.webp')
        print(f'  OK  {rel}  [{", ".join(tags)}]')
    else:
        print(f'  --  {rel}')

print('\nDone.')
