from __future__ import annotations

import json
import html as html_lib
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://www.salanproducciones.com"


STATIC_ROUTES = [
    ("index.html", "/", "/en/", "/de/"),
    ("proximos-conciertos/index.html", "/proximos-conciertos/", "/en/upcoming-concerts/", "/de/kommende-konzerte/"),
    ("conciertos-anteriores/index.html", "/conciertos-anteriores/", "/en/past-concerts/", "/de/vergangene-konzerte/"),
    ("pub-la-calle/index.html", "/pub-la-calle/", "/en/pub-la-calle/", "/de/pub-la-calle/"),
    ("proyectosculturales/index.html", "/proyectosculturales/", "/en/cultural-projects/", "/de/kulturprojekte/"),
    ("proyectosculturales/womex/index.html", "/proyectosculturales/womex/", "/en/cultural-projects/womex/", "/de/kulturprojekte/womex/"),
    ("proyectosculturales/cinezin/index.html", "/proyectosculturales/cinezin/", "/en/cultural-projects/cinezin/", "/de/kulturprojekte/cinezin/"),
    ("proyectosculturales/festivalsonora/index.html", "/proyectosculturales/festivalsonora/", "/en/cultural-projects/festivalsonora/", "/de/kulturprojekte/festivalsonora/"),
    ("contacto/index.html", "/contacto/", "/en/contact/", "/de/kontakt/"),
    ("privacidad/index.html", "/privacidad/", "/en/privacy/", "/de/datenschutz/"),
    ("aviso-legal/index.html", "/aviso-legal/", "/en/legal-notice/", "/de/impressum/"),
    ("cookies/index.html", "/cookies/", "/en/cookies/", "/de/cookies/"),
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(route: str, content: str) -> None:
    rel = route.strip("/")
    path = ROOT / (rel + "/index.html" if rel else "index.html")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def abs_url(route: str) -> str:
    return DOMAIN + route


def route_map(concerts: list[dict]) -> dict[str, dict[str, str]]:
    routes = {}
    for _src, es, en, de in STATIC_ROUTES:
        routes[es] = {"es": es, "en": en, "de": de}
    for c in concerts:
        slug = c["id"]
        es = f"/conciertos/2026/{slug}/"
        routes[es] = {"es": es, "en": f"/en/concerts/2026/{slug}/", "de": f"/de/konzerte/2026/{slug}/"}
    return routes


def alternate_block(es: str, en: str, de: str, lang: str) -> str:
    current = {"es": es, "en": en, "de": de}[lang]
    return "\n".join(
        [
            f'  <link rel="canonical" href="{abs_url(current)}">',
            f'  <link rel="alternate" hreflang="es" href="{abs_url(es)}">',
            f'  <link rel="alternate" hreflang="en" href="{abs_url(en)}">',
            f'  <link rel="alternate" hreflang="de" href="{abs_url(de)}">',
            f'  <link rel="alternate" hreflang="x-default" href="{abs_url(es)}">',
        ]
    )


def replace_head_seo(html: str, es: str, en: str, de: str, lang: str) -> str:
    current = {"en": en, "de": de}[lang]
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', html, count=1)
    html = re.sub(
        r'\s*<link rel="canonical"[^>]+>(?:\s*<link rel="alternate"[^>]+>)*',
        "\n" + alternate_block(es, en, de, lang),
        html,
        count=1,
    )
    locale = "en_US" if lang == "en" else "de_DE"
    if 'property="og:locale"' in html:
        html = re.sub(r'<meta property="og:locale" content="[^"]*">', f'<meta property="og:locale" content="{locale}">', html, count=1)
    else:
        html = html.replace("  <!-- Open Graph -->", f"  <!-- Open Graph -->\n  <meta property=\"og:locale\" content=\"{locale}\">", 1)
    html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{abs_url(current)}">', html, count=1)
    return html


def translate_common(html: str, lang: str) -> str:
    en = {
        "Inicio": "Home",
        "Próximos conciertos": "Upcoming concerts",
        "Conciertos anteriores": "Past concerts",
        "Anteriores": "Past",
        "Proyectos culturales": "Cultural projects",
        "Contacto": "Contact",
        "Navegación principal": "Main navigation",
        "Menú móvil": "Mobile menu",
        "Abrir menú": "Open menu",
        "Formulario de contacto": "Contact form",
        "Secciones": "Sections",
        "Privacidad": "Privacy",
        "Aviso legal": "Legal notice",
        "Política de privacidad": "Privacy policy",
        "Política de Cookies": "Cookie policy",
        "Todos los derechos reservados": "All rights reserved",
        "Más de 35 años produciendo y promoviendo música en directo en las Islas Canarias y España. Un proyecto de Juan Salán.": "More than 35 years producing and promoting live music in the Canary Islands and Spain. A project by Juan Salán.",
        "Más de 35 años produciendo y promoviendo música en directo en las Islas Canarias y España.": "More than 35 years producing and promoting live music in the Canary Islands and Spain.",
        "Islas Canarias, España": "Canary Islands, Spain",
        "Aceptar todo": "Accept all",
        "Solo necesarias": "Necessary only",
        "Más información": "More information",
        "Usamos cookies propias y de terceros (Google Analytics, Meta Pixel) para analítica y publicidad. Puedes aceptar todas o solo las necesarias para el funcionamiento del sitio.": "We use first-party and third-party cookies for analytics, advertising and basic site operation. You can accept all cookies or only the necessary ones.",
        "Comprar Entradas": "Buy tickets",
        "Comprar entradas": "Buy tickets",
        "Comprar": "Buy",
        "Próximamente": "Coming soon",
        "Entradas próximamente": "Tickets coming soon",
        "Agotado": "Sold out",
        "Ver vídeo": "Watch video",
        "Vídeo del show": "Show video",
        "Sobre ": "About ",
        "Ciudad": "City",
        "Fecha": "Date",
        "Hora": "Time",
        '<div class="info-label">Sala</div>': '<div class="info-label">Venue</div>',
        "Precio": "Price",
        "Aforo": "Capacity",
        "Desde": "From",
        "Gira España": "Spain Tour",
        "Gira Península": "Mainland Spain Tour",
        "Gran Canaria": "Gran Canaria",
        "Tenerife": "Tenerife",
        "España": "Spain",
        "Enero": "January",
        "Febrero": "February",
        "Marzo": "March",
        "Abril": "April",
        "Mayo": "May",
        "Junio": "June",
        "Julio": "July",
        "Agosto": "August",
        "Septiembre": "September",
        "Octubre": "October",
        "Noviembre": "November",
        "Diciembre": "December",
        "años de trayectoria": "years of history",
        "Conciertos producidos": "concerts produced",
        "En cartelera": "Now on sale",
        "Próximos": "Upcoming",
        "Conciertos": "Concerts",
        "en directo": "live",
        "desde": "since",
        "Desde": "From",
        "Salán Producciones presenta": "Salán Producciones presents",
        "Salan Producciones presenta": "Salán Producciones presents",
        "artista invitado": "guest artist",
        "+ artista invitado": "+ guest artist",
        "Mira un adelanto del directo antes del": "Watch a preview of the live show before",
        "No te quedes fuera": "Do not miss out",
        "Consigue tus entradas antes de que se agoten.": "Get your tickets before they sell out.",
        "10 ciudades": "10 cities",
        "ciudades": "cities",
        "Selecciona tu ciudad": "Select your city",
        "Tu fecha": "Your date",
        "Mejor Pianista de Blues": "Best Blues Pianist",
        "Premio Juno al Álbum de Blues": "Juno Award for Blues Album",
        "Premio Juno": "Juno Award",
        "Salas íntimas": "Intimate venues",
        "septiembre": "September",
        "gira española": "Spanish tour",
    }
    de = {
        "Inicio": "Start",
        "Próximos conciertos": "Kommende Konzerte",
        "Conciertos anteriores": "Vergangene Konzerte",
        "Anteriores": "Archiv",
        "Proyectos culturales": "Kulturprojekte",
        "Contacto": "Kontakt",
        "Navegación principal": "Hauptnavigation",
        "Menú móvil": "Mobiles Menü",
        "Abrir menú": "Menü öffnen",
        "Formulario de contacto": "Kontaktformular",
        "Secciones": "Bereiche",
        "Privacidad": "Datenschutz",
        "Aviso legal": "Impressum",
        "Política de privacidad": "Datenschutzerklärung",
        "Política de Cookies": "Cookie-Richtlinie",
        "Todos los derechos reservados": "Alle Rechte vorbehalten",
        "Más de 35 años produciendo y promoviendo música en directo en las Islas Canarias y España. Un proyecto de Juan Salán.": "Seit mehr als 35 Jahren Produktion und Promotion von Live-Musik auf den Kanaren und in Spanien. Ein Projekt von Juan Salán.",
        "Más de 35 años produciendo y promoviendo música en directo en las Islas Canarias y España.": "Seit mehr als 35 Jahren Produktion und Promotion von Live-Musik auf den Kanaren und in Spanien.",
        "Islas Canarias, España": "Kanarische Inseln, Spanien",
        "Aceptar todo": "Alle akzeptieren",
        "Solo necesarias": "Nur notwendige",
        "Más información": "Mehr Informationen",
        "Usamos cookies propias y de terceros (Google Analytics, Meta Pixel) para analítica y publicidad. Puedes aceptar todas o solo las necesarias para el funcionamiento del sitio.": "Wir verwenden eigene Cookies und Cookies von Drittanbietern für Analyse, Werbung und den grundlegenden Betrieb der Website. Du kannst alle oder nur die notwendigen Cookies akzeptieren.",
        "Comprar Entradas": "Tickets kaufen",
        "Comprar entradas": "Tickets kaufen",
        "Comprar": "Kaufen",
        "Próximamente": "Bald verfügbar",
        "Entradas próximamente": "Tickets bald verfügbar",
        "Agotado": "Ausverkauft",
        "Ver vídeo": "Video ansehen",
        "Vídeo del show": "Show-Video",
        "Sobre ": "Über ",
        "Ciudad": "Stadt",
        "Fecha": "Datum",
        "Hora": "Uhrzeit",
        '<div class="info-label">Sala</div>': '<div class="info-label">Ort</div>',
        "Precio": "Preis",
        "Aforo": "Kapazität",
        "Desde": "Ab",
        "Gira España": "Spanien-Tour",
        "Gira Península": "Tour Festland Spanien",
        "Gran Canaria": "Gran Canaria",
        "Tenerife": "Teneriffa",
        "España": "Spanien",
        "Enero": "Januar",
        "Febrero": "Februar",
        "Marzo": "März",
        "Abril": "April",
        "Mayo": "Mai",
        "Junio": "Juni",
        "Julio": "Juli",
        "Agosto": "August",
        "Septiembre": "September",
        "Octubre": "Oktober",
        "Noviembre": "November",
        "Diciembre": "Dezember",
        "años de trayectoria": "Jahre Erfahrung",
        "Conciertos producidos": "produzierte Konzerte",
        "En cartelera": "Im Programm",
        "Próximos": "Kommende",
        "Conciertos": "Konzerte",
        "en directo": "live",
        "desde": "seit",
        "Desde": "Ab",
        "Salán Producciones presenta": "Salán Producciones präsentiert",
        "Salan Producciones presenta": "Salán Producciones präsentiert",
        "artista invitado": "Gastkünstler",
        "+ artista invitado": "+ Gastkünstler",
        "Mira un adelanto del directo antes del": "Sieh dir vorab einen Eindruck der Live-Show an vor dem",
        "No te quedes fuera": "Nicht verpassen",
        "Consigue tus entradas antes de que se agoten.": "Sichere dir Tickets, bevor sie ausverkauft sind.",
        "10 ciudades": "10 Städte",
        "ciudades": "Städte",
        "Selecciona tu ciudad": "Wähle deine Stadt",
        "Tu fecha": "Dein Termin",
        "Mejor Pianista de Blues": "Bester Blues-Pianist",
        "Premio Juno al Álbum de Blues": "Juno Award für Blues-Album",
        "Premio Juno": "Juno Award",
        "Salas íntimas": "intime Clubs",
        "septiembre": "September",
        "gira española": "Spanien-Tour",
    }
    table = en if lang == "en" else de
    for src, dst in sorted(table.items(), key=lambda item: len(item[0]), reverse=True):
        html = html.replace(src, dst)
    return html


def translate_page_specific(html: str, lang: str, key: str) -> str:
    page = {
        "home": {
            "en": {
                "Salán Producciones — Canarias · Desde 1987": "Salán Producciones — Canary Islands · Since 1987",
                "Conciertos en directo<br>en <em>España</em><br>desde 1987": "Live concerts<br>in <em>Spain</em><br>since 1987",
                "Promotor musical de referencia en Gran Canaria y Tenerife. Rock, blues, soul y música alternativa en directo en las Islas Canarias.": "A trusted music promoter in Gran Canaria and Tenerife. Rock, blues, soul and alternative live music in the Canary Islands.",
                "Años de trayectoria": "Years of history",
                "El hombre detrás de los conciertos": "The man behind the concerts",
                "La capacidad de generar conocimiento para interpretar la realidad es la diferencia entre programar actividades y construir cultura. Ese ha sido el legado de Juan Salán durante casi cuarenta años": "The ability to generate knowledge in order to understand reality is the difference between programming activities and building culture. That has been Juan Salán's legacy for almost forty years",
                "ANTONIO CACEREÑO, LA PROVINCIA": "ANTONIO CACEREÑO, LA PROVINCIA",
                "Nacido en Burdeos y afincado en Canarias desde 1987, Juan Salán es uno de los promotores musicales más longevos e influyentes del archipiélago. Fundó <strong style=\"color:var(--text)\">Salán Producciones</strong> ese mismo año, arrancando con el legendario <strong style=\"color:var(--text)\">Pub La Calle</strong> (1988–2000) como primer gran proyecto: durante doce años, la única sala dedicada al rock en directo de las Islas Canarias.": "Born in Bordeaux and based in the Canary Islands since 1987, Juan Salán is one of the archipelago's longest-standing and most influential music promoters. He founded <strong style=\"color:var(--text)\">Salán Producciones</strong> that same year, beginning with the legendary <strong style=\"color:var(--text)\">Pub La Calle</strong> (1988-2000) as his first major project: for twelve years, the only venue dedicated to live rock in the Canary Islands.",
                "Entre sus hitos: los <strong style=\"color:var(--text)\">Ramones en Los Tarahales (1993)</strong>, Chuck Berry en Telde, Extremoduro, Los Rodríguez, Wilko Johnson… y hoy WOMEX Gran Canaria 2026. En 2023 fue nombrado <strong style=\"color:var(--text)\">Hijo Adoptivo de Las Palmas de Gran Canaria</strong> por unanimidad del pleno municipal. Lleva 38 años apostando por el directo con una sola filosofía: \"Lo difícil es permanecer después del caos.\"": "Highlights include <strong style=\"color:var(--text)\">Ramones at Los Tarahales (1993)</strong>, Chuck Berry in Telde, Extremoduro, Los Rodríguez, Wilko Johnson... and now WOMEX Gran Canaria 2026. In 2023 he was named <strong style=\"color:var(--text)\">Adopted Son of Las Palmas de Gran Canaria</strong> unanimously by the city council. For 38 years he has backed live music with one philosophy: \"The hard thing is to remain after the chaos.\"",
                "Años en activo": "Active years",
                "Ver historial de conciertos": "View concert history",
                "Legado": "Legacy",
                "Durante doce años, el Pub La Calle fue el corazón de la escena musical alternativa en Las Palmas de Gran Canaria. Una sala que se atrevió con lo que nadie más se atrevía: traer a los mejores del rock nacional e internacional al Puerto de la ciudad.": "For twelve years, Pub La Calle was the heart of the alternative music scene in Las Palmas de Gran Canaria. A venue that dared to do what nobody else did: bring the best national and international rock to the city's port.",
                "Extremoduro, Los Rodríguez, Dover, M-Clan, Siniestro Total, The Yardbirds… pasaron por su escenario. Un legado que sigue vivo en la memoria de toda una generación canaria.": "Extremoduro, Los Rodríguez, Dover, M-Clan, Siniestro Total and The Yardbirds all played its stage. A legacy that remains alive in the memory of a whole Canary Islands generation.",
                "Descubrir la historia": "Discover the story",
                "Entérate el primero 🎸": "Be the first to know",
                "Suscríbete y recibe los próximos conciertos antes de que se anuncien oficialmente.": "Subscribe and receive upcoming concerts before they are officially announced.",
                "Tu nombre (opcional)": "Your name (optional)",
                "Tu email": "Your email",
                "Suscribirme": "Subscribe",
                "Sin spam. Puedes darte de baja cuando quieras.": "No spam. You can unsubscribe whenever you want.",
            },
            "de": {
                "Salán Producciones — Canarias · Desde 1987": "Salán Producciones — Kanarische Inseln · Seit 1987",
                "Conciertos en directo<br>en <em>España</em><br>desde 1987": "Live-Konzerte<br>in <em>Spanien</em><br>seit 1987",
                "Promotor musical de referencia en Gran Canaria y Tenerife. Rock, blues, soul y música alternativa en directo en las Islas Canarias.": "Musikveranstalter auf Gran Canaria und Teneriffa. Rock, Blues, Soul und alternative Live-Musik auf den Kanarischen Inseln.",
                "Años de trayectoria": "Jahre Erfahrung",
                "El hombre detrás de los conciertos": "Der Mann hinter den Konzerten",
                "La capacidad de generar conocimiento para interpretar la realidad es la diferencia entre programar actividades y construir cultura. Ese ha sido el legado de Juan Salán durante casi cuarenta años": "Die Fähigkeit, Wissen zu schaffen, um die Realität zu verstehen, ist der Unterschied zwischen Programmen und Kulturaufbau. Das ist Juan Saláns Vermächtnis seit fast vierzig Jahren",
                "ANTONIO CACEREÑO, LA PROVINCIA": "ANTONIO CACEREÑO, LA PROVINCIA",
                "Nacido en Burdeos y afincado en Canarias desde 1987, Juan Salán es uno de los promotores musicales más longevos e influyentes del archipiélago. Fundó <strong style=\"color:var(--text)\">Salán Producciones</strong> ese mismo año, arrancando con el legendario <strong style=\"color:var(--text)\">Pub La Calle</strong> (1988–2000) como primer gran proyecto: durante doce años, la única sala dedicada al rock en directo de las Islas Canarias.": "Geboren in Bordeaux und seit 1987 auf den Kanaren zuhause, ist Juan Salán einer der langlebigsten und einflussreichsten Musikveranstalter des Archipels. Im selben Jahr gründete er <strong style=\"color:var(--text)\">Salán Producciones</strong> und begann mit dem legendären <strong style=\"color:var(--text)\">Pub La Calle</strong> (1988-2000): zwölf Jahre lang der einzige Club für Live-Rock auf den Kanarischen Inseln.",
                "Entre sus hitos: los <strong style=\"color:var(--text)\">Ramones en Los Tarahales (1993)</strong>, Chuck Berry en Telde, Extremoduro, Los Rodríguez, Wilko Johnson… y hoy WOMEX Gran Canaria 2026. En 2023 fue nombrado <strong style=\"color:var(--text)\">Hijo Adoptivo de Las Palmas de Gran Canaria</strong> por unanimidad del pleno municipal. Lleva 38 años apostando por el directo con una sola filosofía: \"Lo difícil es permanecer después del caos.\"": "Zu seinen Meilensteinen zählen <strong style=\"color:var(--text)\">Ramones in Los Tarahales (1993)</strong>, Chuck Berry in Telde, Extremoduro, Los Rodríguez, Wilko Johnson... und heute WOMEX Gran Canaria 2026. 2023 wurde er einstimmig vom Stadtrat zum <strong style=\"color:var(--text)\">Adoptivsohn von Las Palmas de Gran Canaria</strong> ernannt. Seit 38 Jahren setzt er auf Live-Musik mit einer Philosophie: \"Schwer ist es, nach dem Chaos zu bleiben.\"",
                "Años en activo": "Aktive Jahre",
                "Ver historial de conciertos": "Konzertarchiv ansehen",
                "Legado": "Vermächtnis",
                "Durante doce años, el Pub La Calle fue el corazón de la escena musical alternativa en Las Palmas de Gran Canaria. Una sala que se atrevió con lo que nadie más se atrevía: traer a los mejores del rock nacional e internacional al Puerto de la ciudad.": "Zwölf Jahre lang war Pub La Calle das Herz der alternativen Musikszene in Las Palmas de Gran Canaria. Ein Club, der wagte, was sonst niemand wagte: den besten nationalen und internationalen Rock in den Hafen der Stadt zu bringen.",
                "Extremoduro, Los Rodríguez, Dover, M-Clan, Siniestro Total, The Yardbirds… pasaron por su escenario. Un legado que sigue vivo en la memoria de toda una generación canaria.": "Extremoduro, Los Rodríguez, Dover, M-Clan, Siniestro Total und The Yardbirds standen auf dieser Bühne. Ein Vermächtnis, das in der Erinnerung einer ganzen kanarischen Generation weiterlebt.",
                "Descubrir la historia": "Geschichte entdecken",
                "Entérate el primero 🎸": "Als Erste erfahren",
                "Suscríbete y recibe los próximos conciertos antes de que se anuncien oficialmente.": "Abonniere den Newsletter und erfahre von kommenden Konzerten, bevor sie offiziell angekündigt werden.",
                "Tu nombre (opcional)": "Dein Name (optional)",
                "Tu email": "Deine E-Mail",
                "Suscribirme": "Abonnieren",
                "Sin spam. Puedes darte de baja cuando quieras.": "Kein Spam. Du kannst dich jederzeit abmelden.",
            },
        },
        "past": {
            "en": {
                "35+ años de historia": "35+ years of history",
                "Conciertos <span>Anteriores</span>": "Past <span>Concerts</span>",
                "Breve repaso a los conciertos producidos por Juan Salán a lo largo de los últimos años en las Islas Canarias y España.": "A brief look back at concerts produced by Juan Salán across the Canary Islands and Spain.",
                "Todos": "All",
                "2020 y anteriores": "2020 and earlier",
            },
            "de": {
                "35+ años de historia": "35+ Jahre Geschichte",
                "Conciertos <span>Anteriores</span>": "Vergangene <span>Konzerte</span>",
                "Breve repaso a los conciertos producidos por Juan Salán a lo largo de los últimos años en las Islas Canarias y España.": "Ein kurzer Rückblick auf Konzerte, die Juan Salán auf den Kanaren und in Spanien produziert hat.",
                "Todos": "Alle",
                "2020 y anteriores": "2020 und früher",
            },
        },
        "pub": {
            "en": {
                "Las Palmas de Gran Canaria · 1988 — 2000": "Las Palmas de Gran Canaria · 1988 — 2000",
                "Durante doce años, el Pub La Calle fue el corazón de la escena musical alternativa en Las Palmas de Gran Canaria. Una sala que equiparó la capital grancanaria con las ciudades más importantes del circuito de conciertos nacional.": "For twelve years, Pub La Calle was the heart of the alternative music scene in Las Palmas de Gran Canaria. A venue that placed the city alongside the most important live circuits in Spain.",
                "Años de historia": "Years of history",
                "Año de apertura": "Opening year",
                "Cierre": "Closed",
                "Artistas": "Artists",
                "Recuerdos": "Memories",
                "La historia": "The story",
                "Un lugar que <span>cambió</span> Canarias": "A place that <span>changed</span> the Canary Islands",
                "En 1988, Juan Salán abrió las puertas del <strong>Pub La Calle</strong> en el Puerto de Las Palmas de Gran Canaria con una idea clara: traer a la isla la mejor música live que el país y el mundo tenían para ofrecer. En una época en la que Canarias quedaba fuera de los circuitos habituales de las giras, La Calle se convirtió en la excepción.": "In 1988, Juan Salán opened <strong>Pub La Calle</strong> in the port of Las Palmas de Gran Canaria with a clear idea: to bring the best live music from Spain and the world to the island. At a time when the Canary Islands were outside the usual touring circuits, La Calle became the exception.",
                "La sala no tardó en ganar reputación. Pronto los programadores y agencias nacionales empezaron a incluir Las Palmas en sus itinerarios, sabiendo que allí encontrarían un escenario serio, un público entregado y un promotor de palabra. <strong>El Pub La Calle figuraba en las agendas de los mejores managers de rock de Spain</strong> como una parada obligatoria.": "The venue quickly built a reputation. Soon national promoters and agencies began adding Las Palmas to their routes, knowing they would find a serious stage, a committed audience and a promoter who kept his word. <strong>Pub La Calle appeared in the diaries of Spain's best rock managers</strong> as a must-play stop.",
                "\"Un punto de encuentro de cientos de consumidores de música live que logró <span>equiparar Las Palmas con algunas de las ciudades más importantes del país</span>.\"": "\"A meeting point for hundreds of live music fans that managed to <span>place Las Palmas alongside some of the country's most important cities</span>.\"",
                "Por su escenario pasaron <strong>Extremoduro</strong> en sus primeros años de carrera, <strong>Los Rodríguez</strong> antes de convertirse en fenómeno masivo, <strong>Siniestro Total</strong>, <strong>Los Suaves</strong>, <strong>Dover</strong>, <strong>M-Clan</strong>… Y también nombres de culto que pocas salas españolas podían permitirse: <strong>The Godfathers</strong>, <strong>Robyn Hitchcock</strong>, <strong>Long Ryders</strong>, <strong>The Yardbirds</strong>.": "<strong>Extremoduro</strong> played there in their early years, as did <strong>Los Rodríguez</strong> before becoming a mass phenomenon, <strong>Siniestro Total</strong>, <strong>Los Suaves</strong>, <strong>Dover</strong>, <strong>M-Clan</strong>... and cult names few Spanish venues could book: <strong>The Godfathers</strong>, <strong>Robyn Hitchcock</strong>, <strong>Long Ryders</strong>, <strong>The Yardbirds</strong>.",
                "Pero La Calle era también el hogar de la escena local más vibrante de la isla. <strong>Los Enemigos</strong>, <strong>Del Tonos</strong>, <strong>Marañones</strong>, <strong>El Inquilino Comunista</strong>… bandas de culto que encontraron en sus tablas un escenario donde crecer y un público que los seguía con devoción.": "La Calle was also home to the island's most vibrant local scene. <strong>Los Enemigos</strong>, <strong>Del Tonos</strong>, <strong>Marañones</strong>, <strong>El Inquilino Comunista</strong>... cult bands that found a stage to grow on and an audience that followed them with devotion.",
                "En el año 2000, la sala cerró sus puertas. Pero el legado de Pub La Calle sigue vivo en la memoria de toda una generación canaria que creció escuchando música de verdad, en un local de verdad, con un promotor que creía de verdad en lo que hacía.": "In 2000, the venue closed its doors. But Pub La Calle's legacy remains alive in the memory of a Canary Islands generation that grew up listening to real music, in a real venue, with a promoter who truly believed in what he was doing.",
                "Hoy, ese mismo espíritu es el que anima cada concierto que produce <strong>Salán Producciones</strong>: la convicción de que Canarias merece ver live a los mejores artistas del mundo.": "Today, that same spirit drives every concert produced by <strong>Salán Producciones</strong>: the conviction that the Canary Islands deserve to see the world's best artists live.",
            },
            "de": {
                "Las Palmas de Gran Canaria · 1988 — 2000": "Las Palmas de Gran Canaria · 1988 — 2000",
                "Durante doce años, el Pub La Calle fue el corazón de la escena musical alternativa en Las Palmas de Gran Canaria. Una sala que equiparó la capital grancanaria con las ciudades más importantes del circuito de conciertos nacional.": "Zwölf Jahre lang war Pub La Calle das Herz der alternativen Musikszene in Las Palmas de Gran Canaria. Ein Club, der die Stadt mit den wichtigsten Konzertorten Spaniens verband.",
                "Años de historia": "Jahre Geschichte",
                "Año de apertura": "Eröffnung",
                "Cierre": "Schließung",
                "Artistas": "Künstler",
                "Recuerdos": "Erinnerungen",
                "La historia": "Die Geschichte",
                "Un lugar que <span>cambió</span> Canarias": "Ein Ort, der die <span>Kanaren veränderte</span>",
                "En 1988, Juan Salán abrió las puertas del <strong>Pub La Calle</strong> en el Puerto de Las Palmas de Gran Canaria con una idea clara: traer a la isla la mejor música live que el país y el mundo tenían para ofrecer. En una época en la que Canarias quedaba fuera de los circuitos habituales de las giras, La Calle se convirtió en la excepción.": "1988 öffnete Juan Salán die Türen des <strong>Pub La Calle</strong> im Hafen von Las Palmas de Gran Canaria mit einer klaren Idee: die beste Live-Musik aus Spanien und der Welt auf die Insel zu bringen. Zu einer Zeit, in der die Kanaren abseits der üblichen Tourrouten lagen, wurde La Calle zur Ausnahme.",
                "La sala no tardó en ganar reputación. Pronto los programadores y agencias nacionales empezaron a incluir Las Palmas en sus itinerarios, sabiendo que allí encontrarían un escenario serio, un público entregado y un promotor de palabra. <strong>El Pub La Calle figuraba en las agendas de los mejores managers de rock de Spain</strong> como una parada obligatoria.": "Der Club gewann schnell einen Ruf. Bald nahmen nationale Veranstalter und Agenturen Las Palmas in ihre Routen auf, weil sie dort eine seriöse Bühne, ein engagiertes Publikum und einen verlässlichen Promoter fanden. <strong>Pub La Calle stand bei den besten Rock-Managern Spaniens als Pflichttermin im Kalender</strong>.",
                "\"Un punto de encuentro de cientos de consumidores de música live que logró <span>equiparar Las Palmas con algunas de las ciudades más importantes del país</span>.\"": "\"Ein Treffpunkt für Hunderte Live-Musikfans, der es schaffte, <span>Las Palmas mit einigen der wichtigsten Städte des Landes gleichzustellen</span>.\"",
                "Por su escenario pasaron <strong>Extremoduro</strong> en sus primeros años de carrera, <strong>Los Rodríguez</strong> antes de convertirse en fenómeno masivo, <strong>Siniestro Total</strong>, <strong>Los Suaves</strong>, <strong>Dover</strong>, <strong>M-Clan</strong>… Y también nombres de culto que pocas salas españolas podían permitirse: <strong>The Godfathers</strong>, <strong>Robyn Hitchcock</strong>, <strong>Long Ryders</strong>, <strong>The Yardbirds</strong>.": "Auf seiner Bühne standen <strong>Extremoduro</strong> in ihren frühen Jahren, <strong>Los Rodríguez</strong> vor ihrem großen Durchbruch, <strong>Siniestro Total</strong>, <strong>Los Suaves</strong>, <strong>Dover</strong>, <strong>M-Clan</strong>... und Kultnamen, die sich nur wenige spanische Clubs leisten konnten: <strong>The Godfathers</strong>, <strong>Robyn Hitchcock</strong>, <strong>Long Ryders</strong>, <strong>The Yardbirds</strong>.",
                "Pero La Calle era también el hogar de la escena local más vibrante de la isla. <strong>Los Enemigos</strong>, <strong>Del Tonos</strong>, <strong>Marañones</strong>, <strong>El Inquilino Comunista</strong>… bandas de culto que encontraron en sus tablas un escenario donde crecer y un público que los seguía con devoción.": "La Calle war auch Zuhause der lebendigsten lokalen Szene der Insel. <strong>Los Enemigos</strong>, <strong>Del Tonos</strong>, <strong>Marañones</strong>, <strong>El Inquilino Comunista</strong>... Kultbands, die dort eine Bühne zum Wachsen und ein treues Publikum fanden.",
                "En el año 2000, la sala cerró sus puertas. Pero el legado de Pub La Calle sigue vivo en la memoria de toda una generación canaria que creció escuchando música de verdad, en un local de verdad, con un promotor que creía de verdad en lo que hacía.": "Im Jahr 2000 schloss der Club seine Türen. Doch das Erbe des Pub La Calle lebt in der Erinnerung einer kanarischen Generation weiter, die mit echter Musik, in einem echten Club und mit einem Promoter aufwuchs, der wirklich an das glaubte, was er tat.",
                "Hoy, ese mismo espíritu es el que anima cada concierto que produce <strong>Salán Producciones</strong>: la convicción de que Canarias merece ver live a los mejores artistas del mundo.": "Heute treibt derselbe Geist jedes Konzert von <strong>Salán Producciones</strong> an: die Überzeugung, dass die Kanaren die besten Künstler der Welt live erleben sollten.",
            },
        },
    }
    for src, dst in page.get(key, {}).get(lang, {}).items():
        html = html.replace(src, dst)
    return html


EVENT_TEXT = {
    "La nueva reina del soul de Nueva Orleans trae su voz extraordinaria y una potencia arrolladora a España. Nominada al Grammy®, comparada con Aretha Franklin y Etta James. Una gira única en 4 ciudades españolas durante junio de 2026.": {
        "en": "The new queen of New Orleans soul brings her extraordinary voice and unstoppable power to Spain. Grammy-nominated and compared with Aretha Franklin and Etta James, she visits four Spanish cities in June 2026.",
        "de": "Die neue Queen des New-Orleans-Soul bringt ihre außergewöhnliche Stimme und enorme Kraft nach Spanien. Grammy-nominiert und mit Aretha Franklin und Etta James verglichen, kommt sie im Juni 2026 in vier spanische Städte.",
    },
    "La nueva reina del soul nominada al Grammy® vuelve a España en 2026. Con su aclamado álbum \"Beautiful Dreams\", Acantha Lang ofrece un directo elegante, vibrante y lleno de soul auténtico. Una experiencia que no te puedes perder.": {
        "en": "The Grammy-nominated new queen of soul returns to Spain in 2026. With her acclaimed album \"Beautiful Dreams\", Acantha Lang delivers an elegant, vibrant show full of authentic soul.",
        "de": "Die Grammy-nominierte neue Queen des Soul kehrt 2026 nach Spanien zurück. Mit ihrem gefeierten Album \"Beautiful Dreams\" liefert Acantha Lang eine elegante, lebendige Show voller echtem Soul.",
    },
    "Ex-guitarrista principal de Bunbury durante casi dos décadas. El músico sevillano Álvaro Suite presenta su cuarto álbum en solitario, un viaje que va desde el glam más eléctrico hasta el pop barroco, demostrando por qué es uno de los guitarristas más respetados del rock en español.": {
        "en": "Former lead guitarist for Bunbury for almost two decades. Seville musician Álvaro Suite presents his fourth solo album, a journey from electric glam to baroque pop that shows why he is one of the most respected guitarists in Spanish rock.",
        "de": "Fast zwei Jahrzehnte lang Leadgitarrist von Bunbury. Der Musiker aus Sevilla präsentiert sein viertes Soloalbum, eine Reise von elektrischem Glam bis Barock-Pop, die zeigt, warum er zu den angesehensten Gitarristen des spanischen Rock zählt.",
    },
    "La reina del punk nacional llega a Telde en una fecha única en Canarias. Ana Curra revivirá el legado de Parálisis Permanente interpretando íntegramente el álbum 'El Acto' junto a sus composiciones más recientes. Un concierto irrepetible para los amantes del punk rock más auténtico.": {
        "en": "The queen of Spanish punk comes to Telde for a unique Canary Islands date. Ana Curra revisits the legacy of Parálisis Permanente by performing 'El Acto' in full alongside her more recent songs.",
        "de": "Die Königin des spanischen Punk kommt für ein einmaliges Konzert auf den Kanaren nach Telde. Ana Curra lässt das Erbe von Parálisis Permanente aufleben und spielt 'El Acto' vollständig plus neuere Songs.",
    },
    "Una de las bandas más poderosas del soul y roots rock llega a Tenerife. Meghan Parnell y sus seis músicos traen un directo que ha conquistado escenarios en 10 países — 140 conciertos en 2024 — y esta noche aterrizan en el Teatro Leal de La Laguna.": {
        "en": "One of the most powerful soul and roots rock bands arrives in Tenerife. Meghan Parnell and her six musicians bring a live show that has conquered stages in 10 countries, with 140 concerts in 2024.",
        "de": "Eine der kraftvollsten Soul- und Roots-Rock-Bands kommt nach Teneriffa. Meghan Parnell und ihre sechs Musiker bringen eine Live-Show, die Bühnen in 10 Ländern erobert hat, mit 140 Konzerten im Jahr 2024.",
    },
    "Una de las bandas más poderosas del soul y roots rock llega a Las Palmas de Gran Canaria. Meghan Parnell y sus seis músicos traen un directo que ha conquistado escenarios en 10 países — 140 conciertos en 2024 — y esta noche aterrizan en el Teatro Guiniguada.": {
        "en": "One of the most powerful soul and roots rock bands arrives in Las Palmas de Gran Canaria. Meghan Parnell and her six musicians bring a live show that has conquered stages in 10 countries, with 140 concerts in 2024.",
        "de": "Eine der kraftvollsten Soul- und Roots-Rock-Bands kommt nach Las Palmas de Gran Canaria. Meghan Parnell und ihre sechs Musiker bringen eine Live-Show, die Bühnen in 10 Ländern erobert hat, mit 140 Konzerten im Jahr 2024.",
    },
    "Creedence Clearwater Revived llega a El Sauzal para revivir el auténtico sonido del Bayou Rock. Liderada por Peter Barton, exvocalista de The Animals, junto a veteranos músicos de Wings y The Hollies, la banda ofrece una recreación magistral del catálogo clásico de John Fogerty.": {
        "en": "Creedence Clearwater Revived comes to El Sauzal to revive the authentic Bayou Rock sound. Led by Peter Barton, former singer of The Animals, the band delivers a masterful recreation of John Fogerty's classic catalogue.",
        "de": "Creedence Clearwater Revived kommt nach El Sauzal, um den authentischen Bayou-Rock-Sound wieder aufleben zu lassen. Unter der Leitung von Peter Barton, Ex-Sänger von The Animals, interpretiert die Band John Fogertys Klassiker meisterhaft.",
    },
    "Creedence Clearwater Revived llega a Telde para revivir el auténtico sonido del Bayou Rock. Liderada por Peter Barton, exvocalista de The Animals, junto a veteranos músicos de Wings y The Hollies, la banda ofrece una recreación magistral del catálogo clásico de John Fogerty.": {
        "en": "Creedence Clearwater Revived comes to Telde to revive the authentic Bayou Rock sound. Led by Peter Barton, former singer of The Animals, the band delivers a masterful recreation of John Fogerty's classic catalogue.",
        "de": "Creedence Clearwater Revived kommt nach Telde, um den authentischen Bayou-Rock-Sound wieder aufleben zu lassen. Unter der Leitung von Peter Barton, Ex-Sänger von The Animals, interpretiert die Band John Fogertys Klassiker meisterhaft.",
    },
    "El pianista más electrizante del boogie-woogie desembarca en España con su banda completa. Boogie-Woogie Hall of Fame 2017 · Mejor Pianista de Blues 2024 · Premio Juno al Álbum de Blues.": {
        "en": "The most electrifying boogie-woogie pianist lands in Spain with his full band. Boogie-Woogie Hall of Fame 2017, Best Blues Pianist 2024 and Juno Award for Blues Album.",
        "de": "Der elektrisierendste Boogie-Woogie-Pianist kommt mit kompletter Band nach Spanien. Boogie-Woogie Hall of Fame 2017, bester Blues-Pianist 2024 und Juno Award für Blues Album.",
    },
    "La primera edición del Poseidón Rock Fest llega a Telde con un cartel brutal: H.E.A.T, Kadavar, The Zeronaut y Malamutte en el Auditorio Parque San Juan. Una noche que pasará a la historia del rock en las Islas Canarias.": {
        "en": "The first edition of Poseidón Rock Fest arrives in Telde with a powerful line-up: H.E.A.T, Kadavar, The Zeronaut and Malamutte at Auditorio Parque San Juan.",
        "de": "Die erste Ausgabe des Poseidón Rock Fest kommt nach Telde mit einem starken Line-up: H.E.A.T, Kadavar, The Zeronaut und Malamutte im Auditorio Parque San Juan.",
    },
    "Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor e Iñigo \"El Profe\" López forman Rebrote. La banda llega a Tenerife con su primer disco homónimo y una alineación que trae carretera, oficio y memoria de escenarios grandes. Una noche de rock con músculo, melodía y canciones propias en el Teatro El Sauzal.": {
        "en": "Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor and Iñigo \"El Profe\" López form Rebrote. The band comes to Tenerife with its self-titled debut album and a line-up shaped by the road, craft and big stages.",
        "de": "Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor und Iñigo \"El Profe\" López bilden Rebrote. Die Band kommt mit ihrem selbstbetitelten Debütalbum nach Teneriffa.",
    },
    "Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor e Iñigo \"El Profe\" López forman Rebrote. La banda abre en Telde su paso por Canarias con su primer disco homónimo: canciones propias, guitarras con firma y una forma de entender el rock que viene de tocarlo mucho, no de explicarlo demasiado.": {
        "en": "Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor and Iñigo \"El Profe\" López form Rebrote. The band opens its Canary Islands visit in Telde with its self-titled debut album.",
        "de": "Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor und Iñigo \"El Profe\" López bilden Rebrote. Die Band eröffnet ihren Kanaren-Besuch in Telde mit ihrem selbstbetitelten Debütalbum.",
    },
}

EVENT_DESC_BY_SLUG = {
    "acantha-lang-junio-gira-e-04-06-2026": EVENT_TEXT["La nueva reina del soul de Nueva Orleans trae su voz extraordinaria y una potencia arrolladora a España. Nominada al Grammy®, comparada con Aretha Franklin y Etta James. Una gira única en 4 ciudades españolas durante junio de 2026."],
    "acantha-lang-tour-espana-28-06-2026": EVENT_TEXT["La nueva reina del soul nominada al Grammy® vuelve a España en 2026. Con su aclamado álbum \"Beautiful Dreams\", Acantha Lang ofrece un directo elegante, vibrante y lleno de soul auténtico. Una experiencia que no te puedes perder."],
    "alvaro-suite-gran-canaria-01-05-2026": EVENT_TEXT["Ex-guitarrista principal de Bunbury durante casi dos décadas. El músico sevillano Álvaro Suite presenta su cuarto álbum en solitario, un viaje que va desde el glam más eléctrico hasta el pop barroco, demostrando por qué es uno de los guitarristas más respetados del rock en español."],
    "alvaro-suite-tenerife-30-04-2026": EVENT_TEXT["Ex-guitarrista principal de Bunbury durante casi dos décadas. El músico sevillano Álvaro Suite presenta su cuarto álbum en solitario, un viaje que va desde el glam más eléctrico hasta el pop barroco, demostrando por qué es uno de los guitarristas más respetados del rock en español."],
    "ana-curra-11-04-2026": EVENT_TEXT["La reina del punk nacional llega a Telde en una fecha única en Canarias. Ana Curra revivirá el legado de Parálisis Permanente interpretando íntegramente el álbum 'El Acto' junto a sus composiciones más recientes. Un concierto irrepetible para los amantes del punk rock más auténtico."],
    "bywater-call-16-06-2026": EVENT_TEXT["Una de las bandas más poderosas del soul y roots rock llega a Tenerife. Meghan Parnell y sus seis músicos traen un directo que ha conquistado escenarios en 10 países — 140 conciertos en 2024 — y esta noche aterrizan en el Teatro Leal de La Laguna."],
    "bywater-call-17-06-2026": EVENT_TEXT["Una de las bandas más poderosas del soul y roots rock llega a Las Palmas de Gran Canaria. Meghan Parnell y sus seis músicos traen un directo que ha conquistado escenarios en 10 países — 140 conciertos en 2024 — y esta noche aterrizan en el Teatro Guiniguada."],
    "clearwater-creedence-revival-el-sauzal-13-11-2026": EVENT_TEXT["Creedence Clearwater Revived llega a El Sauzal para revivir el auténtico sonido del Bayou Rock. Liderada por Peter Barton, exvocalista de The Animals, junto a veteranos músicos de Wings y The Hollies, la banda ofrece una recreación magistral del catálogo clásico de John Fogerty."],
    "clearwater-creedence-revival-telde-14-11-2026": EVENT_TEXT["Creedence Clearwater Revived llega a Telde para revivir el auténtico sonido del Bayou Rock. Liderada por Peter Barton, exvocalista de The Animals, junto a veteranos músicos de Wings y The Hollies, la banda ofrece una recreación magistral del catálogo clásico de John Fogerty."],
    "kenny-blues-boss-wayne-gira-espana-2026": EVENT_TEXT["El pianista más electrizante del boogie-woogie desembarca en España con su banda completa. Boogie-Woogie Hall of Fame 2017 · Mejor Pianista de Blues 2024 · Premio Juno al Álbum de Blues."],
    "poseidon-rock-fest-13-06-2026": EVENT_TEXT["La primera edición del Poseidón Rock Fest llega a Telde con un cartel brutal: H.E.A.T, Kadavar, The Zeronaut y Malamutte en el Auditorio Parque San Juan. Una noche que pasará a la historia del rock en las Islas Canarias."],
    "rebrote-el-sauzal-03-10-2026": EVENT_TEXT["Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor e Iñigo \"El Profe\" López forman Rebrote. La banda llega a Tenerife con su primer disco homónimo y una alineación que trae carretera, oficio y memoria de escenarios grandes. Una noche de rock con músculo, melodía y canciones propias en el Teatro El Sauzal."],
    "rebrote-telde-02-10-2026": EVENT_TEXT["Iñaki \"Uoho\" Antón, Jaime Moreno, José Ignacio Cantera, Miguel Colino, Jaime Tejedor e Iñigo \"El Profe\" López forman Rebrote. La banda abre en Telde su paso por Canarias con su primer disco homónimo: canciones propias, guitarras con firma y una forma de entender el rock que viene de tocarlo mucho, no de explicarlo demasiado."],
}


def translate_event_text(html: str, lang: str) -> str:
    for src, translations in EVENT_TEXT.items():
        html = html.replace(src, translations[lang])
    return html


def replace_event_desc(html: str, slug: str | None, lang: str) -> str:
    if not slug or slug not in EVENT_DESC_BY_SLUG:
        return html
    replacement = f'<p class="event-desc">\n                    {EVENT_DESC_BY_SLUG[slug][lang]}\n                </p>'
    return re.sub(r'<p class="event-desc">.*?</p>', replacement, html, count=1, flags=re.S)


def route_for_href(href: str, routes: dict[str, dict[str, str]], lang: str) -> str:
    if href.startswith("#"):
        return href
    if href == "/#proximos":
        return "/en/#proximos" if lang == "en" else "/de/#proximos"
    if href in routes:
        return routes[href][lang]
    # Strip query/hash for internal page links.
    match = re.match(r"([^?#]+)([?#].*)?$", href)
    if match and match.group(1) in routes:
        return routes[match.group(1)][lang] + (match.group(2) or "")
    if href.startswith("/conciertos/2026/"):
        return href.replace("/conciertos/2026/", "/en/concerts/2026/" if lang == "en" else "/de/konzerte/2026/")
    if href.startswith("/proyectosculturales/"):
        return href.replace("/proyectosculturales/", "/en/cultural-projects/" if lang == "en" else "/de/kulturprojekte/")
    common = {
        "/": "/en/" if lang == "en" else "/de/",
        "/proximos-conciertos/": "/en/upcoming-concerts/" if lang == "en" else "/de/kommende-konzerte/",
        "/conciertos-anteriores/": "/en/past-concerts/" if lang == "en" else "/de/vergangene-konzerte/",
        "/contacto/": "/en/contact/" if lang == "en" else "/de/kontakt/",
        "/privacidad/": "/en/privacy/" if lang == "en" else "/de/datenschutz/",
        "/aviso-legal/": "/en/legal-notice/" if lang == "en" else "/de/impressum/",
        "/cookies/": "/en/cookies/" if lang == "en" else "/de/cookies/",
        "/pub-la-calle/": "/en/pub-la-calle/" if lang == "en" else "/de/pub-la-calle/",
    }
    return common.get(href, href)


def rewrite_links(html: str, routes: dict[str, dict[str, str]], lang: str) -> str:
    def repl(match: re.Match) -> str:
        quote = match.group(1)
        href = match.group(2)
        if not href.startswith("/") or href.startswith("//"):
            return match.group(0)
        return f'href={quote}{route_for_href(href, routes, lang)}{quote}'

    return re.sub(r'href=(["\'])(/[^"\']*)\1', repl, html)


def rewrite_concert_asset_paths(html: str, slug: str) -> str:
    base = f"/conciertos/2026/{slug}/"
    html = html.replace('src="./poster.webp"', f'src="{base}poster.webp"')
    html = html.replace("src='./poster.webp'", f"src='{base}poster.webp'")
    html = html.replace("./poster-", base + "poster-")
    html = html.replace("./poster.webp", base + "poster.webp")
    html = re.sub(r'(?<=[="\',\s])poster-(\d+\.webp)', base + r'poster-\1', html)
    html = re.sub(r'(?<=[="\',\s])poster\.webp', base + "poster.webp", html)
    html = html.replace(f"/en/concerts/2026/{slug}/poster", base + "poster")
    html = html.replace(f"/de/konzerte/2026/{slug}/poster", base + "poster")
    return html


def apply_meta_titles(html: str, lang: str, key: str, title_hint: str | None = None) -> str:
    titles = {
        ("home", "en"): "Salán Producciones | Concerts and Live Music in Spain",
        ("home", "de"): "Salán Producciones | Konzerte und Live-Musik in Spanien",
        ("past", "en"): "Past Concerts | Salán Producciones",
        ("past", "de"): "Vergangene Konzerte | Salán Producciones",
        ("pub", "en"): "Pub La Calle Las Palmas — Rock Venue 1988-2000 | Salán Producciones",
        ("pub", "de"): "Pub La Calle Las Palmas — Rockclub 1988-2000 | Salán Producciones",
    }
    title = titles.get((key, lang)) or (title_hint and f"{title_hint} | Salán Producciones")
    if title:
        title_attr = html_lib.escape(title, quote=True)
        html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
        html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title_attr}">', html, count=1)
        html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title_attr}">', html, count=1)
    return html


def repair_protected_names(html: str, lang: str) -> str:
    """Undo accidental partial translations inside proper names."""
    brand_present = "Salán Producciones presents" if lang == "en" else "Salán Producciones präsentiert"
    repairs = {
        "Venuen Producciones presents": brand_present,
        "Venuen Producciones präsentiert": brand_present,
        "Venuen Producciones": "Salán Producciones",
        "Venuen": "Salán",
    }
    for src, dst in repairs.items():
        html = html.replace(src, dst)
    return html


def translate_remaining_fragments(html: str, lang: str) -> str:
    en = {
        "Salán Producciones: más de 38 años organizando conciertos de rock, blues y música live en Gran Canaria, Tenerife y Spain. Juan Salán, promotor musical en Canarias since 1987.": "Salán Producciones: more than 38 years producing rock, blues and live music concerts in Gran Canaria, Tenerife and Spain. Juan Salán, music promoter in the Canary Islands since 1987.",
        "La mejor música live y conciertos en Canarias. Más de 38 años de experiencia, pasión por la música y momentos inolvidables. ¡Descubre nuestra agenda!": "The best live music and concerts in the Canary Islands. More than 38 years of experience, passion for music and unforgettable moments. Discover the agenda.",
        "Empresa de producción y promoción de conciertos y música live fundada por Juan Salán en 1987, con más de 38 years of history en Canarias y Spain. Rock, blues, soul y música alternativa live.": "Concert production and promotion company founded by Juan Salán in 1987, with more than 38 years of history in the Canary Islands and Spain. Rock, blues, soul and alternative live music.",
        "Conciertos en <span>vídeo</span>": "Concerts on <span>video</span>",
        "Concerts en <span>vídeo</span>": "Concerts on <span>video</span>",
        "Grabaciones históricas del escenario del Pub La Calle. Un archivo único del rock en Canarias.": "Historic recordings from the Pub La Calle stage. A unique archive of rock in the Canary Islands.",
        "Ver más vídeos en YouTube": "Watch more videos on YouTube",
        "\"Un punto de encuentro de cientos de consumidores de música live que logró <span>equiparar Las Palmas con algunas de las cities más importantes del país</span>.\"": "\"A meeting point for hundreds of live music fans that managed to <span>place Las Palmas alongside some of the country's most important cities</span>.\"",
        "Pub La Calle fue la única sala de rock live de Canarias entre 1988 y 2000. Extremoduro, Los Rodríguez, Ramones, Dover, Wilko Johnson y más de 100 artistas pasaron por su escenario en Las Palmas de Gran Canaria.": "Pub La Calle was the only live rock venue in the Canary Islands between 1988 and 2000. Extremoduro, Los Rodríguez, Ramones, Dover, Wilko Johnson and more than 100 artists played its stage in Las Palmas de Gran Canaria.",
        "Pub La Calle fue la sala de conciertos más importante de Las Palmas de Gran Canaria entre 1988 y 2000. Un legado musical que marcó a toda una generación canaria.": "Pub La Calle was the most important concert venue in Las Palmas de Gran Canaria between 1988 and 2000. A musical legacy that marked a whole Canary Islands generation.",
        "Kenny 'Blues Boss' Wayne Band en gira por Spain en September 2026. Boogie-Woogie Hall of Fame 2017 · Best Blues Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona y más.": "Kenny 'Blues Boss' Wayne Band tours Spain in September 2026. Boogie-Woogie Hall of Fame 2017, Best Blues Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona and more.",
        "Kenny Blues Boss Wayne Band en gira por Espana en September 2026. Boogie-Woogie Hall of Fame 2017, Best Blues Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona y mas cities.": "Kenny Blues Boss Wayne Band tours Spain in September 2026. Boogie-Woogie Hall of Fame 2017, Best Blues Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona and more cities.",
        "Kenny Wayne nació en New Westminster, Columbia Británica (Canadá), y since niño quedó atrapado\n                por el boogie-woogie y el blues que sonaba en casa. Con más de cuatro décadas encima de los escenarios,\n                se ha convertido en uno de los pianistas de blues más respetados del mundo. En 2017 fue nombrado\n                miembro del <strong style=\"color: var(--text)\">Boogie-Woogie Hall of Fame</strong>, y en 2024\n                recibió el galardón al <strong style=\"color: var(--text)\">Best Blues Pianist</strong>.\n                Su álbum más reciente fue premiado con el <strong style=\"color: var(--text)\">Blues Blast Music Award 2025</strong>\n                y el <strong style=\"color: var(--text)\">Juno Award for Blues Album</strong>, el Grammy canadiense.": "Kenny Wayne was born in New Westminster, British Columbia, Canada, and was captivated by the boogie-woogie and blues he heard at home from an early age. With more than four decades on stage, he has become one of the world's most respected blues pianists. In 2017 he was inducted into the <strong style=\"color: var(--text)\">Boogie-Woogie Hall of Fame</strong>, and in 2024 he received the <strong style=\"color: var(--text)\">Best Blues Pianist</strong> award. His latest album won the <strong style=\"color: var(--text)\">Blues Blast Music Award 2025</strong> and the <strong style=\"color: var(--text)\">Juno Award for Blues Album</strong>, Canada's Grammy equivalent.",
        "Con su banda completa, Kenny ofrece un show live que mezcla potencia, humor y alma a partes iguales.\n                Su piano rebota entre el boogie más desbocado y el blues más profundo, arrastrando al público since\n                el primer acorde. La Spain Tour 2026 es una oportunidad única de verle en salas íntimas antes de\n                que los grandes escenarios se lo lleven definitivamente.": "With his full band, Kenny delivers a live show that blends power, humor and soul in equal measure. His piano moves between wild boogie and deep blues, pulling the audience in from the first chord. The Spain Tour 2026 is a unique chance to see him in intimate venues before the big stages claim him for good.",
        "Cityes en Spain": "Cities in Spain",
        "Cityes en gira": "Cities on tour",
        "Cityes": "Cities",
        "Ver Cities y Buy": "View cities and buy",
        "Años en escena": "Years on stage",
        "Salan Producciones trae de nuevo a <strong style=\"color: var(--text)\">Acantha Lang</strong> a Spain": "Salán Producciones brings <strong style=\"color: var(--text)\">Acantha Lang</strong> back to Spain",
        "Salan Producciones trae a Kenny \"Blues Boss\" Wayne Band en su primera gran Spanish tour.": "Salán Producciones brings Kenny \"Blues Boss\" Wayne Band on his first major Spanish tour.",
        "De la mano de <strong style=\"color: var(--text)\">Juan Salán</strong>, promotor musical de referencia": "Led by <strong style=\"color: var(--text)\">Juan Salán</strong>, a leading music promoter",
        "con más de 38 years of history en Canarias y Spain, esta gira recorre 10 cities en September de 2026:": "with more than 38 years of history in the Canary Islands and Spain, this tour visits 10 cities in September 2026:",
        "Donosti, Bilbao, Ponferrada, Santiago de Compostela, A Coruña, Valladolid, Zaragoza, Castellón, Valencia y Barcelona.": "Donosti, Bilbao, Ponferrada, Santiago de Compostela, A Coruña, Valladolid, Zaragoza, Castellón, Valencia and Barcelona.",
        "Concerts de blues y boogie-woogie en Spain 2026": "Blues and boogie-woogie concerts in Spain 2026",
        "Si buscas <strong style=\"color: var(--text)\">conciertos de blues en Spain</strong>,": "If you are looking for <strong style=\"color: var(--text)\">blues concerts in Spain</strong>,",
        "<strong style=\"color: var(--text)\">boogie-woogie en Valladolid</strong>,": "<strong style=\"color: var(--text)\">boogie-woogie in Valladolid</strong>,",
        "<strong style=\"color: var(--text)\">música live en Bilbao</strong> o": "<strong style=\"color: var(--text)\">live music in Bilbao</strong> or",
        "<strong style=\"color: var(--text)\">piano blues en Barcelona</strong>,": "<strong style=\"color: var(--text)\">piano blues in Barcelona</strong>,",
        "esta es tu oportunidad. Kenny Wayne es uno de los últimos grandes maestros del piano blues clásico\n            en activo, con una energía live que deja sin palabras.": "this is your chance. Kenny Wayne is one of the last great active masters of classic blues piano, with a live energy that leaves audiences speechless.",
        "Síguenos en <a href=\"https://salanproducciones.com\" style=\"color: var(--gold); text-decoration: none;\">salanproducciones.com</a>": "Follow us at <a href=\"https://salanproducciones.com\" style=\"color: var(--gold); text-decoration: none;\">salanproducciones.com</a>",
        "para estar al tanto de todos los próximos conciertos en Spain y Canarias.": "to stay up to date with upcoming concerts in Spain and the Canary Islands.",
        "10 cities. Intimate venues. El boogie-woogie más poderoso del mundo live.": "10 cities. Intimate venues. The world's most powerful boogie-woogie live.",
    }
    de = {
        "Salán Producciones: más de 38 años organizando conciertos de rock, blues y música live en Gran Canaria, Teneriffa y Spanien. Juan Salán, promotor musical en Canarias seit 1987.": "Salán Producciones: mehr als 38 Jahre Rock-, Blues- und Live-Musik-Konzerte auf Gran Canaria, Teneriffa und in Spanien. Juan Salán, Musikveranstalter auf den Kanaren seit 1987.",
        "La mejor música live y conciertos en Canarias. Más de 38 años de experiencia, pasión por la música y momentos inolvidables. ¡Descubre nuestra agenda!": "Die beste Live-Musik und Konzerte auf den Kanaren. Mehr als 38 Jahre Erfahrung, Leidenschaft für Musik und unvergessliche Momente. Entdecke das Programm.",
        "Empresa de producción y promoción de conciertos y música live fundada por Juan Salán en 1987, con más de 38 Jahre Erfahrung en Canarias y Spanien. Rock, blues, soul y música alternativa live.": "Konzertproduktions- und Promotionfirma, 1987 von Juan Salán gegründet, mit mehr als 38 Jahren Geschichte auf den Kanaren und in Spanien. Rock, Blues, Soul und alternative Live-Musik.",
        "La sala no tardó en ganar reputación. Pronto los programadores y agencias nacionales empezaron a incluir Las Palmas en sus itinerarios, sabiendo que allí encontrarían un escenario serio, un público entregado y un promotor de palabra. <strong>El Pub La Calle figuraba en las agendas de los mejores managers de rock de Spanien</strong> como una parada obligatoria.": "Der Club gewann schnell einen Ruf. Bald nahmen nationale Veranstalter und Agenturen Las Palmas in ihre Routen auf, weil sie dort eine seriöse Bühne, ein engagiertes Publikum und einen verlässlichen Promoter fanden. <strong>Pub La Calle stand bei den besten Rock-Managern Spaniens als Pflichttermin im Kalender</strong>.",
        "Conciertos en <span>vídeo</span>": "Konzerte im <span>Video</span>",
        "Konzerte en <span>vídeo</span>": "Konzerte im <span>Video</span>",
        "Grabaciones históricas del escenario del Pub La Calle. Un archivo único del rock en Canarias.": "Historische Aufnahmen von der Bühne des Pub La Calle. Ein einzigartiges Rockarchiv der Kanarischen Inseln.",
        "Ver más vídeos en YouTube": "Weitere Videos auf YouTube ansehen",
        "\"Un punto de encuentro de cientos de consumidores de música live que logró <span>equiparar Las Palmas con algunas de las Städte más importantes del país</span>.\"": "\"Ein Treffpunkt für Hunderte Live-Musikfans, der es schaffte, <span>Las Palmas mit einigen der wichtigsten Städte des Landes gleichzustellen</span>.\"",
        "Pub La Calle fue la única sala de rock live de Canarias entre 1988 y 2000. Extremoduro, Los Rodríguez, Ramones, Dover, Wilko Johnson y más de 100 artistas pasaron por su escenario en Las Palmas de Gran Canaria.": "Pub La Calle war zwischen 1988 und 2000 der einzige Live-Rockclub der Kanarischen Inseln. Extremoduro, Los Rodríguez, Ramones, Dover, Wilko Johnson und mehr als 100 Künstler standen in Las Palmas de Gran Canaria auf seiner Bühne.",
        "Pub La Calle fue la sala de conciertos más importante de Las Palmas de Gran Canaria entre 1988 y 2000. Un legado musical que marcó a toda una generación canaria.": "Pub La Calle war zwischen 1988 und 2000 der wichtigste Konzertclub in Las Palmas de Gran Canaria. Ein musikalisches Erbe, das eine ganze kanarische Generation geprägt hat.",
        "Kenny 'Blues Boss' Wayne Band en gira por Spanien en September 2026. Boogie-Woogie Hall of Fame 2017 · Bester Blues-Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona y más.": "Kenny 'Blues Boss' Wayne Band auf Spanien-Tour im September 2026. Boogie-Woogie Hall of Fame 2017, Bester Blues-Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona und mehr.",
        "Kenny Blues Boss Wayne Band en gira por Espana en September 2026. Boogie-Woogie Hall of Fame 2017, Bester Blues-Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona y mas Städte.": "Kenny Blues Boss Wayne Band auf Spanien-Tour im September 2026. Boogie-Woogie Hall of Fame 2017, Bester Blues-Pianist 2024. Donosti, Bilbao, Valladolid, Valencia, Barcelona und weitere Städte.",
        "Kenny Wayne nació en New Westminster, Columbia Británica (Canadá), y seit niño quedó atrapado\n                por el boogie-woogie y el blues que sonaba en casa. Con más de cuatro décadas encima de los escenarios,\n                se ha convertido en uno de los pianistas de blues más respetados del mundo. En 2017 fue nombrado\n                miembro del <strong style=\"color: var(--text)\">Boogie-Woogie Hall of Fame</strong>, y en 2024\n                recibió el galardón al <strong style=\"color: var(--text)\">Bester Blues-Pianist</strong>.\n                Su álbum más reciente fue premiado con el <strong style=\"color: var(--text)\">Blues Blast Music Award 2025</strong>\n                y el <strong style=\"color: var(--text)\">Juno Award für Blues-Album</strong>, el Grammy canadiense.": "Kenny Wayne wurde in New Westminster, British Columbia, Kanada, geboren und war schon früh vom Boogie-Woogie und Blues fasziniert, der zuhause lief. Mit mehr als vier Jahrzehnten Bühnenerfahrung ist er heute einer der angesehensten Blues-Pianisten der Welt. 2017 wurde er in die <strong style=\"color: var(--text)\">Boogie-Woogie Hall of Fame</strong> aufgenommen, 2024 erhielt er die Auszeichnung <strong style=\"color: var(--text)\">Bester Blues-Pianist</strong>. Sein aktuelles Album gewann den <strong style=\"color: var(--text)\">Blues Blast Music Award 2025</strong> und den <strong style=\"color: var(--text)\">Juno Award für Blues-Album</strong>, das kanadische Grammy-Pendant.",
        "Con su banda completa, Kenny ofrece un show live que mezcla potencia, humor y alma a partes iguales.\n                Su piano rebota entre el boogie más desbocado y el blues más profundo, arrastrando al público seit\n                el primer acorde. La Spanien-Tour 2026 es una oportunidad única de verle en salas íntimas antes de\n                que los grandes escenarios se lo lleven definitivamente.": "Mit kompletter Band liefert Kenny eine Live-Show, die Kraft, Humor und Soul gleichermaßen verbindet. Sein Piano springt zwischen wildem Boogie und tiefem Blues und zieht das Publikum ab dem ersten Akkord mit. Die Spanien-Tour 2026 ist eine besondere Gelegenheit, ihn in intimen Clubs zu erleben, bevor ihn die großen Bühnen endgültig für sich beanspruchen.",
        "Años en escena": "Jahre auf der Bühne",
        "Städte en Spanien": "Städte in Spanien",
        "Salan Producciones trae de nuevo a <strong style=\"color: var(--text)\">Acantha Lang</strong> a Spanien": "Salán Producciones bringt <strong style=\"color: var(--text)\">Acantha Lang</strong> zurück nach Spanien",
        "Salan Producciones trae a Kenny \"Blues Boss\" Wayne Band en su primera gran Spanien-Tour.": "Salán Producciones bringt Kenny \"Blues Boss\" Wayne Band auf seine erste große Spanien-Tour.",
        "De la mano de <strong style=\"color: var(--text)\">Juan Salán</strong>, promotor musical de referencia": "Unter der Leitung von <strong style=\"color: var(--text)\">Juan Salán</strong>, einem führenden Musikveranstalter",
        "con más de 38 Jahre Erfahrung en Canarias y Spanien, esta gira recorre 10 Städte en September de 2026:": "mit mehr als 38 Jahren Erfahrung auf den Kanaren und in Spanien führt diese Tour im September 2026 durch 10 Städte:",
        "Donosti, Bilbao, Ponferrada, Santiago de Compostela, A Coruña, Valladolid, Zaragoza, Castellón, Valencia y Barcelona.": "Donosti, Bilbao, Ponferrada, Santiago de Compostela, A Coruña, Valladolid, Zaragoza, Castellón, Valencia und Barcelona.",
        "Konzerte de blues y boogie-woogie en Spanien 2026": "Blues- und Boogie-Woogie-Konzerte in Spanien 2026",
        "Si buscas <strong style=\"color: var(--text)\">conciertos de blues en Spanien</strong>,": "Wenn du <strong style=\"color: var(--text)\">Blues-Konzerte in Spanien</strong> suchst,",
        "<strong style=\"color: var(--text)\">boogie-woogie en Valladolid</strong>,": "<strong style=\"color: var(--text)\">Boogie-Woogie in Valladolid</strong>,",
        "<strong style=\"color: var(--text)\">música live en Bilbao</strong> o": "<strong style=\"color: var(--text)\">Live-Musik in Bilbao</strong> oder",
        "<strong style=\"color: var(--text)\">piano blues en Barcelona</strong>,": "<strong style=\"color: var(--text)\">Piano-Blues in Barcelona</strong>,",
        "esta es tu oportunidad. Kenny Wayne es uno de los últimos grandes maestros del piano blues clásico\n            en activo, con una energía live que deja sin palabras.": "ist das deine Gelegenheit. Kenny Wayne ist einer der letzten großen aktiven Meister des klassischen Blues-Pianos, mit einer Live-Energie, die sprachlos macht.",
        "Síguenos en <a href=\"https://salanproducciones.com\" style=\"color: var(--gold); text-decoration: none;\">salanproducciones.com</a>": "Folge uns auf <a href=\"https://salanproducciones.com\" style=\"color: var(--gold); text-decoration: none;\">salanproducciones.com</a>",
        "para estar al tanto de todos los próximos conciertos en Spanien y Canarias.": "um über kommende Konzerte in Spanien und auf den Kanaren informiert zu bleiben.",
        "10 Städte. intime Clubs. El boogie-woogie más poderoso del mundo live.": "10 Städte. Intime Clubs. Der kraftvollste Boogie-Woogie der Welt live.",
    }
    table = en if lang == "en" else de
    for src, dst in sorted(table.items(), key=lambda item: len(item[0]), reverse=True):
        html = html.replace(src, dst)
    return html


def transform(source_html: str, es: str, en: str, de: str, lang: str, routes: dict[str, dict[str, str]], key: str, slug: str | None = None, title_hint: str | None = None) -> str:
    html = replace_head_seo(source_html, es, en, de, lang)
    html = rewrite_links(html, routes, lang)
    html = translate_page_specific(html, lang, key)
    if key == "concert":
        html = translate_event_text(html, lang)
        html = replace_event_desc(html, slug, lang)
    html = translate_common(html, lang)
    html = translate_page_specific(html, lang, key)
    html = repair_protected_names(html, lang)
    html = translate_remaining_fragments(html, lang)
    html = apply_meta_titles(html, lang, key, title_hint)
    if key == "concert":
        if lang == "en":
            html = re.sub(r'(<h1 class="event-title">[^<]+) en ([^<]+</h1>)', r'\1 in \2', html)
        else:
            html = re.sub(r'(<h1 class="event-title">[^<]+) en ([^<]+</h1>)', r'\1 in \2', html)
    if slug:
        html = rewrite_concert_asset_paths(html, slug)
    return html


def translate_concert_feed(concerts: list[dict], lang: str) -> list[dict]:
    feed = []
    for c in concerts:
        d = dict(c)
        d["linkInfo"] = f"/en/concerts/2026/{c['id']}/" if lang == "en" else f"/de/konzerte/2026/{c['id']}/"
        for key in ["dateDisplay", "subtitle", "venue", "badge", "price", "buyAria", "buttonLabel"]:
            if isinstance(d.get(key), str):
                d[key] = translate_common(d[key], lang)
        if d.get("linkBuy") and "utm_source=" not in d["linkBuy"]:
            sep = "&" if "?" in d["linkBuy"] else "?"
            d["linkBuy"] = f"{d['linkBuy']}{sep}utm_source=landing&utm_medium=web&utm_campaign={d['id']}-{lang}"
        feed.append(d)
    return feed


def inject_hreflang_spanish(path: Path, es: str, en: str, de: str) -> None:
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    html = re.sub(
        r'\s*<link rel="canonical"[^>]+>(?:\s*<link rel="alternate"[^>]+>)*',
        "\n" + alternate_block(es, en, de, "es"),
        html,
        count=1,
    )
    if 'property="og:locale"' not in html:
        html = html.replace("  <!-- Open Graph -->", '  <!-- Open Graph -->\n  <meta property="og:locale" content="es_ES">', 1)
    path.write_text(html, encoding="utf-8", newline="\n")


def build_sitemap(concerts: list[dict]) -> None:
    entries = []
    for _src, es, en, de in STATIC_ROUTES:
        entries.append((es, en, de, "weekly" if es in {"/", "/proximos-conciertos/"} else "monthly", "1.0" if es == "/" else "0.7"))
    for c in concerts:
        slug = c["id"]
        entries.append((f"/conciertos/2026/{slug}/", f"/en/concerts/2026/{slug}/", f"/de/konzerte/2026/{slug}/", "weekly", "0.8"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for es, en, de, freq, prio in entries:
        for loc in [es, en, de]:
            lines.extend(
                [
                    "  <url>",
                    f"    <loc>{escape(abs_url(loc))}</loc>",
                    f'    <xhtml:link rel="alternate" hreflang="es" href="{escape(abs_url(es))}" />',
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{escape(abs_url(en))}" />',
                    f'    <xhtml:link rel="alternate" hreflang="de" href="{escape(abs_url(de))}" />',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{escape(abs_url(es))}" />',
                    f"    <changefreq>{freq}</changefreq>",
                    f"    <priority>{prio}</priority>",
                    "  </url>",
                ]
            )
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    concerts = json.loads((ROOT / "conciertos.json").read_text(encoding="utf-8"))
    routes = route_map(concerts)

    key_by_es = {
        "/": "home",
        "/conciertos-anteriores/": "past",
        "/pub-la-calle/": "pub",
    }

    for src, es, en, de in STATIC_ROUTES:
        source = read(src)
        key = key_by_es.get(es, "page")
        write(en, transform(source, es, en, de, "en", routes, key))
        write(de, transform(source, es, en, de, "de", routes, key))
        inject_hreflang_spanish(ROOT / src, es, en, de)

    for c in concerts:
        slug = c["id"]
        src = ROOT / f"conciertos/2026/{slug}/index.html"
        if not src.exists():
            continue
        es = f"/conciertos/2026/{slug}/"
        en = f"/en/concerts/2026/{slug}/"
        de = f"/de/konzerte/2026/{slug}/"
        source = src.read_text(encoding="utf-8")
        write(en, transform(source, es, en, de, "en", routes, "concert", slug=slug, title_hint=c["title"]))
        write(de, transform(source, es, en, de, "de", routes, "concert", slug=slug, title_hint=c["title"]))
        inject_hreflang_spanish(src, es, en, de)

    (ROOT / "concerts.en.json").write_text(json.dumps(translate_concert_feed(concerts, "en"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "concerts.de.json").write_text(json.dumps(translate_concert_feed(concerts, "de"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    build_sitemap(concerts)


if __name__ == "__main__":
    main()
