from PIL import Image, ImageDraw, ImageFont
import os, textwrap

BASE    = r'c:\Users\Juan\Desktop\webpapa thedoors\salanproducciones\conciertos\2026'
ASSETS  = r'c:\Users\Juan\Desktop\webpapa thedoors\salanproducciones\assets\images'

OG_W, OG_H = 1200, 630
BG_COLOR    = (10, 10, 10)
GOLD        = (232, 196, 77)
WHITE       = (232, 232, 232)
MUTED       = (136, 136, 136)

# Datos de cada concierto: (titulo, venue, fecha)
concerts = {
    'acantha-lang-junio-gira-e-04-06-2026':             ('Acantha Lang',               'Sevilla · Jerez · Estepona · Valencia', '4–7 Junio 2026'),
    'acantha-lang-tour-espana-28-06-2026':              ('Acantha Lang',               'Toledo · Madrid · Zaragoza · Valladolid', 'Junio–Julio 2026'),
    'alvaro-suite-gran-canaria-01-05-2026':             ('Álvaro Suite',               'Canarias en Vivo · Las Palmas GC', '1 Mayo 2026'),
    'alvaro-suite-tenerife-30-04-2026':                 ('Álvaro Suite',               'Lone Star · Santa Cruz de Tenerife', '30 Abril 2026'),
    'ana-curra-11-04-2026':                             ('Ana Curra',                  'Teatro Juan Ramón Jiménez · Telde', '11 Abril 2026'),
    'bywater-call-16-06-2026':                          ('Bywater Call',               'Teatro Leal · La Laguna, Tenerife', '16 Junio 2026'),
    'bywater-call-17-06-2026':                          ('Bywater Call',               'Teatro Guiniguada · Las Palmas GC', '17 Junio 2026'),
    'clearwater-creedence-revival-el-sauzal-13-11-2026':('Clearwater Creedence Revival','Teatro El Sauzal · El Sauzal, Tenerife', '13 Nov 2026'),
    'clearwater-creedence-revival-telde-14-11-2026':    ('Clearwater Creedence Revival','Teatro Juan Ramón Jiménez · Telde', '14 Nov 2026'),
    'kenny-blues-boss-wayne-gira-espana-2026':          ('Kenny "Blues Boss" Wayne',   'Gira España · 9 ciudades', '9–19 Sep 2026'),
    'poseidon-rock-fest-13-06-2026':                    ('Poseidón Rock Fest',         'Auditorio Parque San Juan · Telde', '13 Junio 2026'),
}

def load_font(size, bold=False):
    # Intentar cargar fuentes del sistema Windows
    font_paths = [
        r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf',
        r'C:\Windows\Fonts\calibrib.ttf' if bold else r'C:\Windows\Fonts\calibri.ttf',
        r'C:\Windows\Fonts\segoeui.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

def make_og(slug, title, venue, fecha):
    poster_path = os.path.join(BASE, slug, 'poster.webp')
    out_path    = os.path.join(BASE, slug, 'og.jpg')

    if not os.path.exists(poster_path):
        print(f'SKIP {slug} (sin poster)')
        return

    # Canvas
    canvas = Image.new('RGB', (OG_W, OG_H), BG_COLOR)

    # --- Poster (lado izquierdo) ---
    poster = Image.open(poster_path).convert('RGB')
    poster_area_w = int(OG_W * 0.42)  # 42% del ancho para el poster
    # Escalar para que ocupe toda la altura
    scale = OG_H / poster.height
    pw = int(poster.width * scale)
    ph = OG_H
    poster_resized = poster.resize((pw, ph), Image.LANCZOS)
    # Recortar al ancho del área si es más ancho
    if pw > poster_area_w:
        left = (pw - poster_area_w) // 2
        poster_resized = poster_resized.crop((left, 0, left + poster_area_w, ph))
        pw = poster_area_w
    canvas.paste(poster_resized, (0, 0))

    # Gradiente de difuminado en el borde derecho del poster
    grad_w = 120
    grad_start = pw - grad_w
    for x in range(grad_w):
        alpha = x / grad_w
        for y in range(OG_H):
            px = canvas.getpixel((grad_start + x, y))
            blended = tuple(int(px[i] * (1 - alpha) + BG_COLOR[i] * alpha) for i in range(3))
            canvas.putpixel((grad_start + x, y), blended)

    # --- Texto (lado derecho) ---
    draw = ImageDraw.Draw(canvas)
    text_x = pw + 40
    text_w  = OG_W - text_x - 40

    font_eyebrow = load_font(22)
    font_title   = load_font(120, bold=True)
    font_venue   = load_font(36)
    font_date    = load_font(48, bold=True)
    font_brand   = load_font(20)

    y = 60

    # Eyebrow
    eyebrow = 'SALÁN PRODUCCIONES PRESENTA'
    draw.text((text_x, y), eyebrow, font=font_eyebrow, fill=GOLD)
    y += 38

    # Separador dorado
    draw.rectangle([(text_x, y), (text_x + 60, y + 4)], fill=GOLD)
    y += 28

    # Título (con wrap si es muy largo)
    wrapped = textwrap.wrap(title, width=10)
    for line in wrapped:
        draw.text((text_x, y), line, font=font_title, fill=WHITE)
        bbox = font_title.getbbox(line)
        y += (bbox[3] - bbox[1]) + 6
    y += 18

    # Venue (con wrap)
    wrapped_venue = textwrap.wrap(venue, width=20)
    for line in wrapped_venue:
        draw.text((text_x, y), line, font=font_venue, fill=MUTED)
        bbox = font_venue.getbbox(line)
        y += (bbox[3] - bbox[1]) + 6
    y += 28

    # Fecha (en gold)
    draw.text((text_x, y), fecha, font=font_date, fill=GOLD)
    y += 70

    # Línea divisoria
    draw.rectangle([(text_x, y), (OG_W - 40, y + 1)], fill=(42, 42, 42))
    y += 22

    # Marca
    draw.text((text_x, y), 'salanproducciones.com', font=font_brand, fill=(80, 80, 80))

    # Guardar
    canvas.save(out_path, 'JPEG', quality=90, optimize=True)
    size_kb = os.path.getsize(out_path) // 1024
    print(f'OK  {slug}/og.jpg  ({size_kb} KB)')

for slug, (title, venue, fecha) in concerts.items():
    make_og(slug, title, venue, fecha)

print('\nDone.')
