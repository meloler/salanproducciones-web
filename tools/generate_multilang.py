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


def translate_cultural_project_fragments(html: str, lang: str) -> str:
    en = {
        "Proyectos Culturales – Salán Producciones": "Cultural Projects – Salán Producciones",
        "Festival Sonora, WOMEX 2026 y Cinezín: los proyectos culturales de Salán Producciones más allá de los conciertos.": "Festival Sonora, WOMEX 2026 and Cinezín: Salán Producciones' cultural projects beyond concerts.",
        "Proyectos Culturales": "Cultural Projects",
        "Proyectos culturales": "Cultural projects",
        "Más proyectos culturales": "More cultural projects",
        "Más allá de los conciertos, Salán Producciones impulsa la cultura musical en Canarias con proyectos propios que conectan artistas, público e industria.": "Beyond concerts, Salán Producciones promotes music culture in the Canary Islands through its own projects connecting artists, audiences and the industry.",
        "El concurso de bandas emergentes más veterano de Canarias": "The longest-running emerging band contest in the Canary Islands",
        "La mayor feria profesional de músicas del mundo, 22-26 oct · Las Palmas": "The world's leading professional music fair, 22-26 Oct · Las Palmas",
        "La mayor feria profesional de músicas del mundo vuelve a Las Palmas de Gran Canaria": "The world's leading professional music fair returns to Las Palmas de Gran Canaria",
        "Ciclo de documentales musicales": "Music documentary series",
        "Ver proyecto →": "View project →",
        "Ir a womex-festival.com →": "Go to womex-festival.com →",
        "Ir a festivalsonora.com →": "Go to festivalsonora.com →",
        "← Volver a proyectos": "← Back to projects",
        "Proyecto propio · Salán Producciones": "Own project · Salán Producciones",
        "Salán Producciones · impulsor en Gran Canaria": "Salán Producciones · promoter in Gran Canaria",
        "Fechas": "Dates",
        "Sede": "Venue",
        "Asistentes": "Attendees",
        "Países": "Countries",
        "Edición": "Edition",
        "Finales": "Finals",
        "Inscritos 2026": "2026 entries",
        "195 bandas y artistas": "195 bands and artists",
        "22-26 de octubre de 2026": "22-26 October 2026",
        "16-18 de octubre de 2026": "16-18 October 2026",
        "17-18 de abril de 2026": "17-18 April 2026",
        "2.300+ profesionales": "2,300+ professionals",
        "Qué es WOMEX": "What WOMEX Is",
        "El <strong style=\"color:var(--text)\">World Music Expo</strong> es la feria profesional más importante del mundo para músicas del mundo y folk. Cada año reúne a más de <strong style=\"color:var(--text)\">2.300 profesionales de 90 países</strong>: promotores, sellos, managers, festivales, agencias de booking, periodistas y artistas que toman decisiones que mueven la industria global.": "The <strong style=\"color:var(--text)\">World Music Expo</strong> is the world's most important professional fair for world music and folk. Every year it brings together more than <strong style=\"color:var(--text)\">2,300 professionals from 90 countries</strong>: promoters, labels, managers, festivals, booking agencies, journalists and artists who shape the global industry.",
        "El programa combina showcases en vivo de <strong style=\"color:var(--text)\">350 artistas</strong>, un mercado profesional, conferencias, paneles, networking y la entrega de los WOMEX Awards — el reconocimiento más prestigioso del sector de las músicas del mundo. Más de <strong style=\"color:var(--text)\">250 periodistas</strong> especializados cubren el evento desde todos los rincones del planeta.": "The programme combines live showcases by <strong style=\"color:var(--text)\">350 artists</strong>, a professional market, conferences, panels, networking and the WOMEX Awards, the most prestigious recognition in the world music sector. More than <strong style=\"color:var(--text)\">250 specialist journalists</strong> cover the event from every corner of the planet.",
        "El programa combina showcases en vivo de <strong style=\"color:var(--text)\">350 artistas</strong>, un mercado profesional, conferencias, paneles, networking y la entrega de los WOMEX Awards — el reconocimiento más prestigioso del sector de las músicas del mundo. Más de <strong style=\"color:var(--text)\">250 periodistas</strong> especializados cubren el evento since todos los rincones del planeta.": "The programme combines live showcases by <strong style=\"color:var(--text)\">350 artists</strong>, a professional market, conferences, panels, networking and the WOMEX Awards, the most prestigious recognition in the world music sector. More than <strong style=\"color:var(--text)\">250 specialist journalists</strong> cover the event from every corner of the planet.",
        "Profesionales asistentes": "Attending professionals",
        "Países representados": "Countries represented",
        "Artistas en showcases": "Showcase artists",
        "Periodistas especializados": "Specialist journalists",
        "Salán Producciones y WOMEX": "Salán Producciones and WOMEX",
        "Traer WOMEX a Las Palmas de Gran Canaria en 2026 no es casualidad — es el resultado de años de trabajo, relaciones y apuesta por la isla como referente de la industria musical. Juan Salán y Santiago Gutiérrez pusieron todo su empeño en conseguir que el evento más importante del sector de las músicas del mundo eligiera de nuevo Gran Canaria como sede.": "Bringing WOMEX to Las Palmas de Gran Canaria in 2026 is no coincidence. It is the result of years of work, relationships and commitment to the island as a reference point for the music industry. Juan Salán and Santiago Gutiérrez worked intensely to ensure that the sector's most important world music event chose Gran Canaria again as its host city.",
        "El impacto económico estimado supera los <strong style=\"color:var(--text)\">3 millones de euros</strong> en consumo de visitantes, con miles de noches de hotel, vuelos y actividad en la ciudad durante la semana del evento. Pero más allá del impacto económico, WOMEX sitúa a Las Palmas de Gran Canaria y a Canarias en el mapa de la industria cultural internacional, con 2.300 profesionales del mundo entero conociendo el destino de primera mano.": "The estimated economic impact exceeds <strong style=\"color:var(--text)\">3 million euros</strong> in visitor spending, with thousands of hotel nights, flights and activity across the city during event week. Beyond the economic impact, WOMEX places Las Palmas de Gran Canaria and the Canary Islands on the international cultural industry map, with 2,300 professionals from around the world experiencing the destination first-hand.",
        "Para Salán Producciones, impulsar proyectos como este es parte de una misión más amplia: no solo traer conciertos, sino construir un ecosistema cultural en las islas que conecte a los artistas locales con el mundo.": "For Salán Producciones, driving projects like this is part of a broader mission: not only bringing concerts, but building a cultural ecosystem in the islands that connects local artists with the world.",
        "WOMEX en Las Palmas: 2018 → 2026": "WOMEX in Las Palmas: 2018 → 2026",
        "Primera vez en Las Palmas": "First time in Las Palmas",
        "Las Palmas de Gran Canaria acoge WOMEX por primera vez. La ciudad demuestra que puede organizar uno de los eventos culturales más exigentes del mundo.": "Las Palmas de Gran Canaria hosts WOMEX for the first time. The city proves it can stage one of the world's most demanding cultural events.",
        "El regreso": "The Return",
        "Tras el éxito de 2018, Juan Salán y Santiago Gutiérrez trabajan para traerlo de nuevo. Las Palmas se convierte en sede por segunda vez, consolidando su posición como referente cultural internacional.": "After the success of 2018, Juan Salán and Santiago Gutiérrez work to bring it back. Las Palmas becomes host city for a second time, strengthening its position as an international cultural reference.",
        "WOMEX 2018 en Las Palmas": "WOMEX 2018 in Las Palmas",
        "Imágenes de la primera edición de WOMEX en Gran Canaria, que demostró la capacidad de la isla para albergar uno de los eventos culturales más exigentes del mundo.": "Images from the first WOMEX edition in Gran Canaria, which proved the island's ability to host one of the world's most demanding cultural events.",
        "En los medios": "In the Media",
        "Web oficial WOMEX": "Official WOMEX website",
        "womex-festival.com — Programa, showcases, acreditaciones y toda la información del evento": "womex-festival.com — Programme, showcases, accreditations and full event information",
        "¿Eres profesional de la industria musical? Contacta con nosotros para colaboraciones en WOMEX 2026": "Are you a music industry professional? Contact us for WOMEX 2026 collaborations",
        "Las Palmas se consolida como referente cultural internacional con WOMEX 2026": "Las Palmas strengthens its position as an international cultural reference with WOMEX 2026",
        "WOMEX 2026, la mayor feria de músicas del mundo, vuelve a Las Palmas de Gran Canaria del 22 al 26 de octubre. Juan Salán y Santiago Gutiérrez, impulsores del regreso de WOMEX a Canarias.": "WOMEX 2026, the world's leading music fair, returns to Las Palmas de Gran Canaria from 22 to 26 October. Juan Salán and Santiago Gutiérrez helped bring WOMEX back to the Canary Islands.",
        "WOMEX 2026 Las Palmas de Gran Canaria – Juan Salán y Santiago Gutiérrez lo traen de vuelta": "WOMEX 2026 Las Palmas de Gran Canaria – Juan Salán and Santiago Gutiérrez bring it back",
        "WOMEX 2026 en Las Palmas de Gran Canaria – Salán Producciones": "WOMEX 2026 in Las Palmas de Gran Canaria – Salán Producciones",
        "Juan Salán y Santiago Gutiérrez en la presentación de WOMEX 2026 en Las Palmas de Gran Canaria": "Juan Salán and Santiago Gutiérrez at the WOMEX 2026 presentation in Las Palmas de Gran Canaria",
        "WOMEX 2026: la mayor feria de músicas del mundo vuelve a Las Palmas del 22 al 26 de octubre.": "WOMEX 2026: the world's leading music fair returns to Las Palmas from 22 to 26 October.",
        "El World Music Expo 2026 en Las Palmas de Gran Canaria. La mayor feria profesional de músicas del mundo, con 2.300 profesionales de 90 países, 350 artistas y 250 periodistas.": "World Music Expo 2026 in Las Palmas de Gran Canaria. The world's leading professional music fair, with 2,300 professionals from 90 countries, 350 artists and 250 journalists.",
        "Cinezín – Ciclo de Cine y Música en Las Palmas | Salán Producciones": "Cinezín – Film and Music Series in Las Palmas | Salán Producciones",
        "Cinezín – Cine y Música en Las Palmas de Gran Canaria": "Cinezín – Film and Music in Las Palmas de Gran Canaria",
        "Cinezín – ciclo de cine y música en Las Palmas": "Cinezín – film and music series in Las Palmas",
        "Cine, música y debate en vivo. Documentales únicos y encuentros con especialistas en Las Palmas de Gran Canaria. Impulsado por Juan Salán.": "Film, music and live debate. Unique documentaries and encounters with specialists in Las Palmas de Gran Canaria. Driven by Juan Salán.",
        "Cinezín es el ciclo de cine y música impulsado por Juan Salán en Las Palmas de Gran Canaria. From 2022 proyecta documentales únicos sobre rock, soul, electrónica y cultura musical, con debates live.": "Cinezín is the film and music series driven by Juan Salán in Las Palmas de Gran Canaria. Since 2022 it has screened unique documentaries about rock, soul, electronic music and music culture, with live debates.",
        "Cuatro ediciones, documentales únicos y debates con expertos. El ciclo de cine musical de Salán Producciones since 2022 en Las Palmas de Gran Canaria.": "Four editions, unique documentaries and debates with experts. Salán Producciones' music film series in Las Palmas de Gran Canaria since 2022.",
        "Cuatro ediciones de cine musical en Las Palmas. Documentales únicos, debates live. Impulsado por Juan Salán.": "Four editions of music cinema in Las Palmas. Unique documentaries and live debates. Driven by Juan Salán.",
        "Cinezín – Ciclo de Cine y Música": "Cinezín – Film and Music Series",
        "Ciclo de proyecciones de documentales musicales impulsado por Juan Salán en Las Palmas de Gran Canaria. Cuatro ediciones since 2022: Castillo de Mata (2022, 2023, 2024) y Club La Provincia (2026). Proyecciones + debate live con músicos y directores.": "A series of music documentary screenings driven by Juan Salán in Las Palmas de Gran Canaria. Four editions since 2022: Castillo de Mata (2022, 2023, 2024) and Club La Provincia (2026). Screenings plus live debate with musicians and directors.",
        "Sobre Cinezín": "About Cinezín",
        "Cinezín nació en 2022 como un espacio diferente: proyecciones de documentales musicales que no encontrarás fácilmente en las plataformas, seguidas de <strong style=\"color:var(--text)\">debates en directo</strong> con músicos, periodistas y especialistas. Rock, soul, música electrónica, cantautores… y siempre con entrada libre o gratuita.": "Cinezín was born in 2022 as a different kind of space: screenings of music documentaries that are not easy to find on platforms, followed by <strong style=\"color:var(--text)\">live debates</strong> with musicians, journalists and specialists. Rock, soul, electronic music, singer-songwriters... and always with free admission.",
        "Cinezín nació en 2022 como un espacio diferente: proyecciones de documentales musicales que no encontrarás fácilmente en las plataformas, seguidas de <strong style=\"color:var(--text)\">debates live</strong> con músicos, periodistas y especialistas. Rock, soul, música electrónica, cantautores… y siempre con entrada libre o gratuita.": "Cinezín was born in 2022 as a different kind of space: screenings of music documentaries that are not easy to find on platforms, followed by <strong style=\"color:var(--text)\">live debates</strong> with musicians, journalists and specialists. Rock, soul, electronic music, singer-songwriters... and always with free admission.",
        "Ediciones": "Editions",
        "Películas": "Films",
        "Documentales": "Documentaries",
        "Primera edición": "First edition",
        "Entrada libre con reserva": "Free admission with booking",
        "Entrada libre": "Free admission",
        "Cuatro sesiones de cine y música con proyecciones gratuitas seguidas de mesas redondas con músicos, críticos y especialistas. La programación abarcó rock español, soul, música electrónica y mockumentary en un mes intenso en el Castillo de Mata.": "Four film and music sessions with free screenings followed by round tables with musicians, critics and specialists. The programme covered Spanish rock, soul, electronic music and mockumentary in an intense month at Castillo de Mata.",
        "Dos sesiones que cruzaron memoria, cine y música. La primera recuperó una grabación de 1990 perdida durante 30 años; la segunda trajo a Las Palmas el documental más taquillero de 2022, recién premiado con el Goya.": "Two sessions crossing memory, film and music. The first recovered a 1990 recording lost for 30 years; the second brought to Las Palmas the highest-grossing documentary of 2022, newly awarded the Goya.",
        "Cuatro sesiones en el Museo Castillo de Mata con documentales sobre grandes figuras del rock y el pop español. La edición arrancó con el estreno mundial de <em>Ánimo animal</em>, homenaje a Luis Eduardo Aute, con Gaizka Urresti y Miguel Aute en sala.": "Four sessions at Museo Castillo de Mata with documentaries about major figures in Spanish rock and pop. The edition opened with the world premiere of <em>Ánimo animal</em>, a tribute to Luis Eduardo Aute, with Gaizka Urresti and Miguel Aute in attendance.",
        "La cuarta edición de Cinezín regresa al Club La Provincia (León y Castillo, 39) con tres sesiones de proyecciones + debate en directo. Rock español de tres décadas distintas con sus protagonistas en sala. Moderado por Diego Hernández y Xavier Valiño.": "The fourth edition of Cinezín returns to Club La Provincia (León y Castillo, 39) with three screening and live debate sessions. Spanish rock from three different decades with its protagonists in attendance. Moderated by Diego Hernández and Xavier Valiño.",
        "La cuarta edición de Cinezín regresa al Club La Provincia (León y Castillo, 39) con tres sesiones de proyecciones + debate live. Rock español de tres décadas distintas con sus protagonistas en sala. Moderado por Diego Hernández y Xavier Valiño.": "The fourth edition of Cinezín returns to Club La Provincia (León y Castillo, 39) with three screening and live debate sessions. Spanish rock from three different decades with its protagonists in attendance. Moderated by Diego Hernández and Xavier Valiño.",
        "Invitado:": "Guest:",
        "Pioneras de la electrónica": "Pioneers of electronic music",
        "Lou Reed &amp; Cale homenajean a Warhol": "Lou Reed &amp; Cale pay tribute to Warhol",
        "Homenaje a Luis Eduardo Aute": "Tribute to Luis Eduardo Aute",
        "Con Miguel Aute": "With Miguel Aute",
        "Con Mª José Martín<br>y Mª Cristina Martín": "With Mª José Martín<br>and Mª Cristina Martín",
        "Con Kiko Veneno": "With Kiko Veneno",
        "Con Lauren Jordan<br>y Belén Zafra": "With Lauren Jordan<br>and Belén Zafra",
        "Ayto. LPGC — Presentación": "LPGC City Council — Presentation",
        "Festival Cinezín une cine y música del 10 al 30 de marzo en Castillo de Mata": "Festival Cinezín brings film and music together from 10 to 30 March at Castillo de Mata",
        "El Castillo de Mata acoge Cinezín, festival de cine conectado a la música": "Castillo de Mata hosts Cinezín, a film festival connected to music",
        "Cinezín rinde homenaje a las pioneras de la música electrónica con Sisters with Transistors": "Cinezín pays tribute to the women pioneers of electronic music with Sisters with Transistors",
        "Cinezín anticipa en Las Palmas el estreno de The Garlic Phantoms": "Cinezín previews The Garlic Phantoms in Las Palmas",
        "CINEZiN 2 abre con Songs for Drella: Lou Reed y John Cale homenajean a Andy Warhol": "CINEZiN 2 opens with Songs for Drella: Lou Reed and John Cale pay tribute to Andy Warhol",
        "CINEZiN presenta el Goya al Mejor Documental: Labordeta, un hombre sin más": "CINEZiN presents the Goya winner for Best Documentary: Labordeta, un hombre sin más",
        "Club Provincia acoge en mayo el ciclo Cinezín": "Club Provincia hosts the Cinezín series in May",
        "Festival Sonora 2026 – Ganadores, Finalistas y Próxima Edición | Salán Producciones": "Festival Sonora 2026 – Winners, Finalists and Next Edition | Salán Producciones",
        "Festival Sonora 2026 – Ganadores y Finalistas | Salán Producciones": "Festival Sonora 2026 – Winners and Finalists | Salán Producciones",
        "Festival Sonora 2026 – Concurso de Bandas Emergentes de Canarias": "Festival Sonora 2026 – Emerging Band Contest in the Canary Islands",
        "Festival Sonora 2026: Los Blody y Good Franco, ganadores absolutos. El concurso de bandas emergentes más veterano de Canarias, impulsado por Juan Salán y Santiago Gutiérrez. 195 inscritos, Auditorio Alfredo Kraus, Las Palmas.": "Festival Sonora 2026: Los Blody and Good Franco, overall winners. The longest-running emerging band contest in the Canary Islands, driven by Juan Salán and Santiago Gutiérrez. 195 entries, Auditorio Alfredo Kraus, Las Palmas.",
        "Festival Sonora 2026: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus. Organizado por Salán Producciones.": "Festival Sonora 2026: 195 entries, 10 finalists, Auditorio Alfredo Kraus. Organised by Salán Producciones.",
        "Festival Sonora, el concurso de bandas emergentes más veterano de Canarias. 2026 Edition: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.": "Festival Sonora, the longest-running emerging band contest in the Canary Islands. 2026 edition: 195 entries, 10 finalists, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.",
        "Festival Sonora, the longest-running emerging band contest in the Canary Islands. 2026 Edition: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.": "Festival Sonora, the longest-running emerging band contest in the Canary Islands. 2026 edition: 195 entries, 10 finalists, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.",
        "Festival Sonora, the longest-running emerging band contest in the Canary Islands. 2026 Edition: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.": "Festival Sonora, the longest-running emerging band contest in the Canary Islands. 2026 edition: 195 entries, 10 finalists, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.",
        "Festival Sonora, el concurso de bandas emergentes más veterano de Canarias.": "Festival Sonora, the longest-running emerging band contest in the Canary Islands.",
        "Festival Sonora – el concurso de bandas emergentes más veterano de Canarias": "Festival Sonora – the longest-running emerging band contest in the Canary Islands",
        "Sobre el Festival": "About the Festival",
        "About el Festival": "About the Festival",
        "Festival Sonora es el certamen de bandas y artistas emergentes más longevo de las Islas Canarias. Nacido de la visión de Juan Salán e impulsado por Juan Salán y su socio Santiago Gutiérrez a través de Salán Producciones, el festival abre sus puertas cada año a músicos de todos los géneros: rock, pop, urban, blues, folk, jazz y world music. No hay barreras de estilo; hay un único criterio: talento y directo.": "Festival Sonora is the longest-running contest for emerging bands and artists in the Canary Islands. Born from Juan Salán's vision and driven by Juan Salán and his partner Santiago Gutiérrez through Salán Producciones, the festival opens its doors every year to musicians of every genre: rock, pop, urban, blues, folk, jazz and world music. There are no style barriers; there is one criterion: talent and live performance.",
        "El premio es más que un trofeo. Los ganadores se llevan hasta <strong style=\"color:var(--text)\">6.000 euros en metálico</strong> y el codiciado <strong style=\"color:var(--text)\">Pasaporte Sonora</strong>, que abre las puertas de festivales nacionales e internacionales con los que Festival Sonora mantiene acuerdos de colaboración. Año tras año, el escenario de la Sala Jerónimo Saavedra del Auditorio Alfredo Kraus ha sido el trampolín de artistas que hoy forman parte de la escena musical española.": "The prize is more than a trophy. Winners receive up to <strong style=\"color:var(--text)\">6,000 euros in cash</strong> and the coveted <strong style=\"color:var(--text)\">Sonora Passport</strong>, opening doors to national and international festivals with which Festival Sonora has collaboration agreements. Year after year, the Sala Jerónimo Saavedra stage at Auditorio Alfredo Kraus has served as a springboard for artists who are now part of the Spanish music scene.",
        "Inscritos en 2026": "Entries in 2026",
        "Finalistas seleccionados": "Selected finalists",
        "Premio máximo": "Top prize",
        "Récord de participación": "Participation record",
        "Ganadores Sonora 2026": "Sonora 2026 Winners",
        "La final celebrada los días 17 y 18 de abril de 2026 en la <strong style=\"color:var(--text)\">Sala Jerónimo Saavedra del Auditorio Alfredo Kraus</strong> arrojó un resultado histórico: el jurado declaró dos ganadores absolutos, reconociendo el nivel excepcional de la edición.": "The final held on 17 and 18 April 2026 at <strong style=\"color:var(--text)\">Sala Jerónimo Saavedra, Auditorio Alfredo Kraus</strong> produced a historic result: the jury declared two overall winners, recognising the exceptional level of the edition.",
        "Premio:": "Prize:",
        "Prize: 6.000 € · Pasaporte Sonora: Canarias Tiene el Flow (Madrid), Sonidos Líquidos La Graciosa, Festivalito (La Palma)": "Prize: 6,000 € · Sonora Passport: Canarias Tiene el Flow (Madrid), Sonidos Líquidos La Graciosa, Festivalito (La Palma)",
        "Prize: 6.000 € · Pasaporte Sonora: Sonidos Líquidos (Lanzarote), Phe Festival (Puerto de la Cruz) + financiación EP con Taste The Floor": "Prize: 6,000 € · Sonora Passport: Sonidos Líquidos (Lanzarote), Phe Festival (Puerto de la Cruz) + EP funding with Taste The Floor",
        "Prize: 1.500 € · Pasaporte: WOMEX Gran Canaria": "Prize: 1,500 € · Passport: WOMEX Gran Canaria",
        "El Sonora 2026 amplía sus premios y los \"pasaportes\" para actuar en festivales": "Sonora 2026 expands its prizes and festival performance passports",
        "El concurso musical Sonora extiende sus \"pasaportes\" a La Palma y La Gomera": "The Sonora music contest extends its passports to La Palma and La Gomera",
        "Sonora Oro": "Sonora Gold",
        "Sonora Plata": "Sonora Silver",
        "Sonora Bronce": "Sonora Bronze",
        "Edición 2026": "2026 Edition",
        "La edición 2026 ha batido el récord de participación con <strong style=\"color:var(--text)\">195 inscritos</strong>. El proceso se divide en dos grandes fases: las rondas eliminatorias dan paso a las finales de primavera, y los mejores actúan en el gran festival de octubre ante el público del Auditorio Alfredo Kraus.": "The 2026 edition broke the participation record with <strong style=\"color:var(--text)\">195 entries</strong>. The process is divided into two major phases: elimination rounds lead into the spring finals, and the best acts perform at the major October festival before the Auditorio Alfredo Kraus audience.",
        "Fase 1": "Phase 1",
        "Fase 2": "Phase 2",
        "Finales de primavera": "Spring finals",
        "Festival de octubre": "October festival",
        "17 y 18 de abril de 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. Los 10 finalistas se miden en directo ante el jurado y el público.": "17 and 18 April 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. The 10 finalists perform live before the jury and the audience.",
        "17 y 18 de abril de 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. Los 10 finalistas se miden live ante el jurado y el público.": "17 and 18 April 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. The 10 finalists perform live before the jury and the audience.",
        "16, 17 y 18 de octubre de 2026 · Auditorio Alfredo Kraus. El gran festival, con los ganadores y artistas invitados, cierra la edición con tres noches de música en directo.": "16, 17 and 18 October 2026 · Auditorio Alfredo Kraus. The main festival, with winners and guest artists, closes the edition with three nights of live music.",
        "16, 17 y 18 de octubre de 2026 · Auditorio Alfredo Kraus. El gran festival, con los ganadores y artistas invitados, cierra la edición con tres noches de música live.": "16, 17 and 18 October 2026 · Auditorio Alfredo Kraus. The main festival, with winners and guest artists, closes the edition with three nights of live music.",
        "Galería Sonora 2026": "Sonora 2026 Gallery",
        "Los 10 finalistas de la edición 2026 y momentos del certamen.": "The 10 finalists from the 2026 edition and moments from the contest.",
        "Final en el Auditorio Alfredo Kraus": "Final at Auditorio Alfredo Kraus",
        "Jurado preselección 2026": "2026 preselection jury",
        "Los ganadores Sonora 2026": "Sonora 2026 winners",
        "Los Blody y Good Franco, ganadores absolutos del Sonora 2026": "Los Blody and Good Franco, overall winners of Sonora 2026",
        "El certamen Sonora 2026 da a conocer las 10 propuestas musicales de su gran final": "Sonora 2026 announces the 10 musical projects in its grand final",
        "El Sonora 2026 amplía sus premios y los \"pasaportes\" para actuar en festivales": "Sonora 2026 expands its prizes and festival performance passports",
        "El concurso musical Sonora extiende sus \"pasaportes\" a La Palma y La Gomera": "The Sonora music contest extends its passports to La Palma and La Gomera",
        "Web oficial": "Official website",
        "festivalsonora.com — Toda la información, bases del concurso e inscripciones": "festivalsonora.com — Full information, contest rules and registration",
    }
    de = {
        "Proyectos Culturales – Salán Producciones": "Kulturprojekte – Salán Producciones",
        "Festival Sonora, WOMEX 2026 y Cinezín: los proyectos culturales de Salán Producciones más allá de los conciertos.": "Festival Sonora, WOMEX 2026 und Cinezín: die Kulturprojekte von Salán Producciones über Konzerte hinaus.",
        "Proyectos Culturales": "Kulturprojekte",
        "Proyectos culturales": "Kulturprojekte",
        "Más proyectos culturales": "Weitere Kulturprojekte",
        "Más allá de los conciertos, Salán Producciones impulsa la cultura musical en Canarias con proyectos propios que conectan artistas, público e industria.": "Über Konzerte hinaus fördert Salán Producciones die Musikkultur auf den Kanaren mit eigenen Projekten, die Künstler, Publikum und Branche verbinden.",
        "El concurso de bandas emergentes más veterano de Canarias": "Der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren",
        "La mayor feria profesional de músicas del mundo, 22-26 oct · Las Palmas": "Die weltweit führende professionelle Musikmesse, 22.-26. Okt. · Las Palmas",
        "La mayor feria profesional de músicas del mundo vuelve a Las Palmas de Gran Canaria": "Die weltweit führende professionelle Musikmesse kehrt nach Las Palmas de Gran Canaria zurück",
        "Ciclo de documentales musicales": "Reihe musikalischer Dokumentarfilme",
        "Ver proyecto →": "Projekt ansehen →",
        "Ir a womex-festival.com →": "Zu womex-festival.com →",
        "Ir a festivalsonora.com →": "Zu festivalsonora.com →",
        "← Volver a proyectos": "← Zurück zu Projekten",
        "Proyecto propio · Salán Producciones": "Eigenes Projekt · Salán Producciones",
        "Salán Producciones · impulsor en Gran Canaria": "Salán Producciones · Impulsgeber auf Gran Canaria",
        "Fechas": "Termine",
        "Sede": "Ort",
        "Asistentes": "Teilnehmende",
        "Países": "Länder",
        "Edición": "Ausgabe",
        "Finales": "Finale",
        "Inscritos 2026": "Anmeldungen 2026",
        "195 bandas y artistas": "195 Bands und Künstler",
        "22-26 de octubre de 2026": "22.-26. Oktober 2026",
        "16-18 de octubre de 2026": "16.-18. Oktober 2026",
        "17-18 de abril de 2026": "17.-18. April 2026",
        "2.300+ profesionales": "2.300+ Fachbesucher",
        "Qué es WOMEX": "Was WOMEX ist",
        "El <strong style=\"color:var(--text)\">World Music Expo</strong> es la feria profesional más importante del mundo para músicas del mundo y folk. Cada año reúne a más de <strong style=\"color:var(--text)\">2.300 profesionales de 90 países</strong>: promotores, sellos, managers, festivales, agencias de booking, periodistas y artistas que toman decisiones que mueven la industria global.": "Die <strong style=\"color:var(--text)\">World Music Expo</strong> ist die wichtigste Fachmesse der Welt für World Music und Folk. Jedes Jahr bringt sie mehr als <strong style=\"color:var(--text)\">2.300 Fachleute aus 90 Ländern</strong> zusammen: Veranstalter, Labels, Manager, Festivals, Booking-Agenturen, Journalisten und Künstler, die die globale Branche bewegen.",
        "El programa combina showcases en vivo de <strong style=\"color:var(--text)\">350 artistas</strong>, un mercado profesional, conferencias, paneles, networking y la entrega de los WOMEX Awards — el reconocimiento más prestigioso del sector de las músicas del mundo. Más de <strong style=\"color:var(--text)\">250 periodistas</strong> especializados cubren el evento desde todos los rincones del planeta.": "Das Programm verbindet Live-Showcases von <strong style=\"color:var(--text)\">350 Künstlern</strong>, einen Fachmarkt, Konferenzen, Panels, Networking und die WOMEX Awards, die wichtigste Auszeichnung der World-Music-Branche. Mehr als <strong style=\"color:var(--text)\">250 Fachjournalisten</strong> berichten aus aller Welt über das Event.",
        "El programa combina showcases en vivo de <strong style=\"color:var(--text)\">350 artistas</strong>, un mercado profesional, conferencias, paneles, networking y la entrega de los WOMEX Awards — el reconocimiento más prestigioso del sector de las músicas del mundo. Más de <strong style=\"color:var(--text)\">250 periodistas</strong> especializados cubren el evento seit todos los rincones del planeta.": "Das Programm verbindet Live-Showcases von <strong style=\"color:var(--text)\">350 Künstlern</strong>, einen Fachmarkt, Konferenzen, Panels, Networking und die WOMEX Awards, die wichtigste Auszeichnung der World-Music-Branche. Mehr als <strong style=\"color:var(--text)\">250 Fachjournalisten</strong> berichten aus aller Welt über das Event.",
        "Profesionales asistentes": "Teilnehmende Fachleute",
        "Países representados": "Vertretene Länder",
        "Artistas en showcases": "Showcase-Künstler",
        "Periodistas especializados": "Fachjournalisten",
        "Salán Producciones y WOMEX": "Salán Producciones und WOMEX",
        "Traer WOMEX a Las Palmas de Gran Canaria en 2026 no es casualidad — es el resultado de años de trabajo, relaciones y apuesta por la isla como referente de la industria musical. Juan Salán y Santiago Gutiérrez pusieron todo su empeño en conseguir que el evento más importante del sector de las músicas del mundo eligiera de nuevo Gran Canaria como sede.": "WOMEX 2026 nach Las Palmas de Gran Canaria zu bringen, ist kein Zufall. Es ist das Ergebnis jahrelanger Arbeit, Beziehungen und des Engagements für die Insel als Bezugspunkt der Musikbranche. Juan Salán und Santiago Gutiérrez setzten alles daran, dass das wichtigste Event der World-Music-Branche Gran Canaria erneut als Gastgeber wählt.",
        "El impacto económico estimado supera los <strong style=\"color:var(--text)\">3 millones de euros</strong> en consumo de visitantes, con miles de noches de hotel, vuelos y actividad en la ciudad durante la semana del evento. Pero más allá del impacto económico, WOMEX sitúa a Las Palmas de Gran Canaria y a Canarias en el mapa de la industria cultural internacional, con 2.300 profesionales del mundo entero conociendo el destino de primera mano.": "Die geschätzte wirtschaftliche Wirkung übersteigt <strong style=\"color:var(--text)\">3 Millionen Euro</strong> an Besucherausgaben, mit Tausenden Hotelübernachtungen, Flügen und Aktivität in der Stadt während der Veranstaltungswoche. Über den wirtschaftlichen Effekt hinaus setzt WOMEX Las Palmas de Gran Canaria und die Kanaren auf die Karte der internationalen Kulturbranche.",
        "Para Salán Producciones, impulsar proyectos como este es parte de una misión más amplia: no solo traer conciertos, sino construir un ecosistema cultural en las islas que conecte a los artistas locales con el mundo.": "Für Salán Producciones ist die Förderung solcher Projekte Teil einer größeren Mission: nicht nur Konzerte zu bringen, sondern auf den Inseln ein kulturelles Ökosystem aufzubauen, das lokale Künstler mit der Welt verbindet.",
        "WOMEX en Las Palmas: 2018 → 2026": "WOMEX in Las Palmas: 2018 → 2026",
        "Primera vez en Las Palmas": "Erstes Mal in Las Palmas",
        "Las Palmas de Gran Canaria acoge WOMEX por primera vez. La ciudad demuestra que puede organizar uno de los eventos culturales más exigentes del mundo.": "Las Palmas de Gran Canaria richtet WOMEX zum ersten Mal aus. Die Stadt zeigt, dass sie eines der anspruchsvollsten Kulturereignisse der Welt organisieren kann.",
        "El regreso": "Die Rückkehr",
        "Tras el éxito de 2018, Juan Salán y Santiago Gutiérrez trabajan para traerlo de nuevo. Las Palmas se convierte en sede por segunda vez, consolidando su posición como referente cultural internacional.": "Nach dem Erfolg von 2018 arbeiten Juan Salán und Santiago Gutiérrez daran, WOMEX zurückzubringen. Las Palmas wird zum zweiten Mal Gastgeber und festigt seine Position als internationale Kulturreferenz.",
        "WOMEX 2018 en Las Palmas": "WOMEX 2018 in Las Palmas",
        "Imágenes de la primera edición de WOMEX en Gran Canaria, que demostró la capacidad de la isla para albergar uno de los eventos culturales más exigentes del mundo.": "Bilder der ersten WOMEX-Ausgabe auf Gran Canaria, die zeigte, dass die Insel eines der anspruchsvollsten Kulturereignisse der Welt ausrichten kann.",
        "En los medios": "In den Medien",
        "Web oficial WOMEX": "Offizielle WOMEX-Website",
        "womex-festival.com — Programa, showcases, acreditaciones y toda la información del evento": "womex-festival.com — Programm, Showcases, Akkreditierungen und alle Informationen zum Event",
        "¿Eres profesional de la industria musical? Contacta con nosotros para colaboraciones en WOMEX 2026": "Bist du in der Musikbranche tätig? Kontaktiere uns für Kooperationen rund um WOMEX 2026",
        "Las Palmas se consolida como referente cultural internacional con WOMEX 2026": "Las Palmas festigt mit WOMEX 2026 seine Position als internationale Kulturreferenz",
        "WOMEX 2026, la mayor feria de músicas del mundo, vuelve a Las Palmas de Gran Canaria del 22 al 26 de octubre. Juan Salán y Santiago Gutiérrez, impulsores del regreso de WOMEX a Canarias.": "WOMEX 2026, die weltweit führende Musikmesse, kehrt vom 22. bis 26. Oktober nach Las Palmas de Gran Canaria zurück. Juan Salán und Santiago Gutiérrez haben die Rückkehr von WOMEX auf die Kanaren mit vorangetrieben.",
        "WOMEX 2026 Las Palmas de Gran Canaria – Juan Salán y Santiago Gutiérrez lo traen de vuelta": "WOMEX 2026 Las Palmas de Gran Canaria – Juan Salán und Santiago Gutiérrez bringen es zurück",
        "WOMEX 2026 en Las Palmas de Gran Canaria – Salán Producciones": "WOMEX 2026 in Las Palmas de Gran Canaria – Salán Producciones",
        "Juan Salán y Santiago Gutiérrez en la presentación de WOMEX 2026 en Las Palmas de Gran Canaria": "Juan Salán und Santiago Gutiérrez bei der Vorstellung von WOMEX 2026 in Las Palmas de Gran Canaria",
        "WOMEX 2026: la mayor feria de músicas del mundo vuelve a Las Palmas del 22 al 26 de octubre.": "WOMEX 2026: Die weltweit führende Musikmesse kehrt vom 22. bis 26. Oktober nach Las Palmas zurück.",
        "El World Music Expo 2026 en Las Palmas de Gran Canaria. La mayor feria profesional de músicas del mundo, con 2.300 profesionales de 90 países, 350 artistas y 250 periodistas.": "World Music Expo 2026 in Las Palmas de Gran Canaria. Die weltweit führende professionelle Musikmesse mit 2.300 Fachleuten aus 90 Ländern, 350 Künstlern und 250 Journalisten.",
        "Cinezín – Ciclo de Cine y Música en Las Palmas | Salán Producciones": "Cinezín – Film- und Musikreihe in Las Palmas | Salán Producciones",
        "Cinezín – Cine y Música en Las Palmas de Gran Canaria": "Cinezín – Film und Musik in Las Palmas de Gran Canaria",
        "Cinezín – ciclo de cine y música en Las Palmas": "Cinezín – Film- und Musikreihe in Las Palmas",
        "Cine, música y debate en vivo. Documentales únicos y encuentros con especialistas en Las Palmas de Gran Canaria. Impulsado por Juan Salán.": "Film, Musik und Live-Debatte. Einzigartige Dokumentarfilme und Begegnungen mit Fachleuten in Las Palmas de Gran Canaria. Initiiert von Juan Salán.",
        "Cinezín es el ciclo de cine y música impulsado por Juan Salán en Las Palmas de Gran Canaria. Ab 2022 proyecta documentales únicos sobre rock, soul, electrónica y cultura musical, con debates live.": "Cinezín ist die von Juan Salán initiierte Film- und Musikreihe in Las Palmas de Gran Canaria. Seit 2022 zeigt sie einzigartige Dokumentarfilme über Rock, Soul, elektronische Musik und Musikkultur, mit Live-Debatten.",
        "Cuatro ediciones, documentales únicos y debates con expertos. El ciclo de cine musical de Salán Producciones seit 2022 en Las Palmas de Gran Canaria.": "Vier Ausgaben, einzigartige Dokumentarfilme und Debatten mit Fachleuten. Die Musikfilmreihe von Salán Producciones in Las Palmas de Gran Canaria seit 2022.",
        "Cuatro ediciones de cine musical en Las Palmas. Documentales únicos, debates live. Impulsado por Juan Salán.": "Vier Ausgaben Musikfilm in Las Palmas. Einzigartige Dokumentarfilme und Live-Debatten. Initiiert von Juan Salán.",
        "Cinezín – Ciclo de Cine y Música": "Cinezín – Film- und Musikreihe",
        "Ciclo de proyecciones de documentales musicales impulsado por Juan Salán en Las Palmas de Gran Canaria. Cuatro ediciones seit 2022: Castillo de Mata (2022, 2023, 2024) y Club La Provincia (2026). Proyecciones + debate live con músicos y directores.": "Eine von Juan Salán initiierte Reihe von Musikdokumentarfilm-Vorführungen in Las Palmas de Gran Canaria. Vier Ausgaben seit 2022: Castillo de Mata (2022, 2023, 2024) und Club La Provincia (2026). Vorführungen plus Live-Debatten mit Musikern und Regisseuren.",
        "Sobre Cinezín": "Über Cinezín",
        "Cinezín nació en 2022 como un espacio diferente: proyecciones de documentales musicales que no encontrarás fácilmente en las plataformas, seguidas de <strong style=\"color:var(--text)\">debates en directo</strong> con músicos, periodistas y especialistas. Rock, soul, música electrónica, cantautores… y siempre con entrada libre o gratuita.": "Cinezín entstand 2022 als anderer Raum: Vorführungen von Musikdokumentarfilmen, die man auf Plattformen kaum findet, gefolgt von <strong style=\"color:var(--text)\">Live-Debatten</strong> mit Musikern, Journalisten und Fachleuten. Rock, Soul, elektronische Musik, Singer-Songwriter... und immer mit freiem Eintritt.",
        "Cinezín nació en 2022 como un espacio diferente: proyecciones de documentales musicales que no encontrarás fácilmente en las plataformas, seguidas de <strong style=\"color:var(--text)\">debates live</strong> con músicos, periodistas y especialistas. Rock, soul, música electrónica, cantautores… y siempre con entrada libre o gratuita.": "Cinezín entstand 2022 als anderer Raum: Vorführungen von Musikdokumentarfilmen, die man auf Plattformen kaum findet, gefolgt von <strong style=\"color:var(--text)\">Live-Debatten</strong> mit Musikern, Journalisten und Fachleuten. Rock, Soul, elektronische Musik, Singer-Songwriter... und immer mit freiem Eintritt.",
        "Ediciones": "Ausgaben",
        "Películas": "Filme",
        "Documentales": "Dokumentarfilme",
        "Primera edición": "Erste Ausgabe",
        "Entrada libre con reserva": "Freier Eintritt mit Reservierung",
        "Entrada libre": "Freier Eintritt",
        "Cuatro sesiones de cine y música con proyecciones gratuitas seguidas de mesas redondas con músicos, críticos y especialistas. La programación abarcó rock español, soul, música electrónica y mockumentary en un mes intenso en el Castillo de Mata.": "Vier Film- und Musikabende mit kostenlosen Vorführungen, gefolgt von Runden Tischen mit Musikern, Kritikern und Fachleuten. Das Programm umfasste spanischen Rock, Soul, elektronische Musik und Mockumentary in einem intensiven Monat im Castillo de Mata.",
        "Dos sesiones que cruzaron memoria, cine y música. La primera recuperó una grabación de 1990 perdida durante 30 años; la segunda trajo a Las Palmas el documental más taquillero de 2022, recién premiado con el Goya.": "Zwei Abende, die Erinnerung, Film und Musik verbanden. Der erste brachte eine 30 Jahre verschollene Aufnahme von 1990 zurück; der zweite zeigte in Las Palmas den erfolgreichsten Dokumentarfilm von 2022, frisch mit dem Goya ausgezeichnet.",
        "Cuatro sesiones en el Museo Castillo de Mata con documentales sobre grandes figuras del rock y el pop español. La edición arrancó con el estreno mundial de <em>Ánimo animal</em>, homenaje a Luis Eduardo Aute, con Gaizka Urresti y Miguel Aute en sala.": "Vier Abende im Museo Castillo de Mata mit Dokumentarfilmen über große Figuren des spanischen Rock und Pop. Die Ausgabe begann mit der Weltpremiere von <em>Ánimo animal</em>, einer Hommage an Luis Eduardo Aute, mit Gaizka Urresti und Miguel Aute im Saal.",
        "La cuarta edición de Cinezín regresa al Club La Provincia (León y Castillo, 39) con tres sesiones de proyecciones + debate en directo. Rock español de tres décadas distintas con sus protagonistas en sala. Moderado por Diego Hernández y Xavier Valiño.": "Die vierte Ausgabe von Cinezín kehrt mit drei Film- und Live-Debattenabenden in den Club La Provincia (León y Castillo, 39) zurück. Spanischer Rock aus drei verschiedenen Jahrzehnten mit seinen Protagonisten im Saal. Moderiert von Diego Hernández und Xavier Valiño.",
        "La cuarta edición de Cinezín regresa al Club La Provincia (León y Castillo, 39) con tres sesiones de proyecciones + debate live. Rock español de tres décadas distintas con sus protagonistas en sala. Moderado por Diego Hernández y Xavier Valiño.": "Die vierte Ausgabe von Cinezín kehrt mit drei Film- und Live-Debattenabenden in den Club La Provincia (León y Castillo, 39) zurück. Spanischer Rock aus drei verschiedenen Jahrzehnten mit seinen Protagonisten im Saal. Moderiert von Diego Hernández und Xavier Valiño.",
        "Invitado:": "Gast:",
        "Pioneras de la electrónica": "Pionierinnen der elektronischen Musik",
        "Lou Reed &amp; Cale homenajean a Warhol": "Lou Reed &amp; Cale würdigen Warhol",
        "Homenaje a Luis Eduardo Aute": "Hommage an Luis Eduardo Aute",
        "Con Miguel Aute": "Mit Miguel Aute",
        "Con Mª José Martín<br>y Mª Cristina Martín": "Mit Mª José Martín<br>und Mª Cristina Martín",
        "Con Kiko Veneno": "Mit Kiko Veneno",
        "Con Lauren Jordan<br>y Belén Zafra": "Mit Lauren Jordan<br>und Belén Zafra",
        "Ayto. LPGC — Presentación": "Stadt Las Palmas — Präsentation",
        "Festival Cinezín une cine y música del 10 al 30 de marzo en Castillo de Mata": "Festival Cinezín verbindet Film und Musik vom 10. bis 30. März im Castillo de Mata",
        "El Castillo de Mata acoge Cinezín, festival de cine conectado a la música": "Das Castillo de Mata empfängt Cinezín, ein Filmfestival mit Musikbezug",
        "Cinezín rinde homenaje a las pioneras de la música electrónica con Sisters with Transistors": "Cinezín würdigt mit Sisters with Transistors die Pionierinnen der elektronischen Musik",
        "Cinezín anticipa en Las Palmas el estreno de The Garlic Phantoms": "Cinezín zeigt in Las Palmas eine Vorschau auf The Garlic Phantoms",
        "CINEZiN 2 abre con Songs for Drella: Lou Reed y John Cale homenajean a Andy Warhol": "CINEZiN 2 eröffnet mit Songs for Drella: Lou Reed und John Cale würdigen Andy Warhol",
        "CINEZiN presenta el Goya al Mejor Documental: Labordeta, un hombre sin más": "CINEZiN präsentiert den Goya-Gewinner für den besten Dokumentarfilm: Labordeta, un hombre sin más",
        "Club Provincia acoge en mayo el ciclo Cinezín": "Club Provincia empfängt im Mai die Reihe Cinezín",
        "Festival Sonora 2026 – Ganadores, Finalistas y Próxima Edición | Salán Producciones": "Festival Sonora 2026 – Gewinner, Finalisten und nächste Ausgabe | Salán Producciones",
        "Festival Sonora 2026 – Ganadores y Finalistas | Salán Producciones": "Festival Sonora 2026 – Gewinner und Finalisten | Salán Producciones",
        "Festival Sonora 2026 – Concurso de Bandas Emergentes de Canarias": "Festival Sonora 2026 – Wettbewerb für Nachwuchsbands auf den Kanaren",
        "Festival Sonora 2026: Los Blody y Good Franco, ganadores absolutos. El concurso de bandas emergentes más veterano de Canarias, impulsado por Juan Salán y Santiago Gutiérrez. 195 inscritos, Auditorio Alfredo Kraus, Las Palmas.": "Festival Sonora 2026: Los Blody und Good Franco, Gesamtsieger. Der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren, getragen von Juan Salán und Santiago Gutiérrez. 195 Anmeldungen, Auditorio Alfredo Kraus, Las Palmas.",
        "Festival Sonora 2026: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus. Organizado por Salán Producciones.": "Festival Sonora 2026: 195 Anmeldungen, 10 Finalisten, Auditorio Alfredo Kraus. Organisiert von Salán Producciones.",
        "Festival Sonora, el concurso de bandas emergentes más veterano de Canarias. Ausgabe 2026: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.": "Festival Sonora, der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren. Ausgabe 2026: 195 Anmeldungen, 10 Finalisten, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.",
        "Festival Sonora, der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren. Ausgabe 2026: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.": "Festival Sonora, der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren. Ausgabe 2026: 195 Anmeldungen, 10 Finalisten, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.",
        "Festival Sonora, der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren. Ausgabe 2026: 195 inscritos, 10 finalistas, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.": "Festival Sonora, der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren. Ausgabe 2026: 195 Anmeldungen, 10 Finalisten, Auditorio Alfredo Kraus, Las Palmas de Gran Canaria.",
        "Festival Sonora, el concurso de bandas emergentes más veterano de Canarias.": "Festival Sonora, der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren.",
        "Festival Sonora – el concurso de bandas emergentes más veterano de Canarias": "Festival Sonora – der traditionsreichste Wettbewerb für Nachwuchsbands auf den Kanaren",
        "Sobre el Festival": "Über das Festival",
        "Über el Festival": "Über das Festival",
        "Festival Sonora es el certamen de bandas y artistas emergentes más longevo de las Islas Canarias. Nacido de la visión de Juan Salán e impulsado por Juan Salán y su socio Santiago Gutiérrez a través de Salán Producciones, el festival abre sus puertas cada año a músicos de todos los géneros: rock, pop, urban, blues, folk, jazz y world music. No hay barreras de estilo; hay un único criterio: talento y directo.": "Festival Sonora ist der traditionsreichste Wettbewerb für Nachwuchsbands und Künstler auf den Kanaren. Aus der Vision von Juan Salán entstanden und von Juan Salán und seinem Partner Santiago Gutiérrez über Salán Producciones getragen, öffnet das Festival jedes Jahr Musikern aller Genres seine Türen: Rock, Pop, Urban, Blues, Folk, Jazz und World Music. Es gibt keine Stilgrenzen; es zählt nur ein Kriterium: Talent und Live-Performance.",
        "El premio es más que un trofeo. Los ganadores se llevan hasta <strong style=\"color:var(--text)\">6.000 euros en metálico</strong> y el codiciado <strong style=\"color:var(--text)\">Pasaporte Sonora</strong>, que abre las puertas de festivales nacionales e internacionales con los que Festival Sonora mantiene acuerdos de colaboración. Año tras año, el escenario de la Sala Jerónimo Saavedra del Auditorio Alfredo Kraus ha sido el trampolín de artistas que hoy forman parte de la escena musical española.": "Der Preis ist mehr als eine Trophäe. Die Gewinner erhalten bis zu <strong style=\"color:var(--text)\">6.000 Euro in bar</strong> und den begehrten <strong style=\"color:var(--text)\">Sonora-Pass</strong>, der Türen zu nationalen und internationalen Festivals öffnet, mit denen Festival Sonora kooperiert. Jahr für Jahr war die Bühne der Sala Jerónimo Saavedra im Auditorio Alfredo Kraus ein Sprungbrett für Künstler, die heute Teil der spanischen Musikszene sind.",
        "Inscritos en 2026": "Anmeldungen 2026",
        "Finalistas seleccionados": "Ausgewählte Finalisten",
        "Premio máximo": "Höchstpreis",
        "Récord de participación": "Teilnahmerekord",
        "Ganadores Sonora 2026": "Sonora-Gewinner 2026",
        "La final celebrada los días 17 y 18 de abril de 2026 en la <strong style=\"color:var(--text)\">Sala Jerónimo Saavedra del Auditorio Alfredo Kraus</strong> arrojó un resultado histórico: el jurado declaró dos ganadores absolutos, reconociendo el nivel excepcional de la edición.": "Das Finale am 17. und 18. April 2026 in der <strong style=\"color:var(--text)\">Sala Jerónimo Saavedra des Auditorio Alfredo Kraus</strong> brachte ein historisches Ergebnis: Die Jury erklärte zwei Gesamtsieger und würdigte damit das außergewöhnliche Niveau der Ausgabe.",
        "Premio:": "Preis:",
        "Preis: 6.000 € · Pasaporte Sonora: Canarias Tiene el Flow (Madrid), Sonidos Líquidos La Graciosa, Festivalito (La Palma)": "Preis: 6.000 € · Sonora-Pass: Canarias Tiene el Flow (Madrid), Sonidos Líquidos La Graciosa, Festivalito (La Palma)",
        "Preis: 6.000 € · Pasaporte Sonora: Sonidos Líquidos (Lanzarote), Phe Festival (Puerto de la Cruz) + financiación EP con Taste The Floor": "Preis: 6.000 € · Sonora-Pass: Sonidos Líquidos (Lanzarote), Phe Festival (Puerto de la Cruz) + EP-Finanzierung mit Taste The Floor",
        "Preis: 1.500 € · Pasaporte: WOMEX Gran Canaria": "Preis: 1.500 € · Pass: WOMEX Gran Canaria",
        "El Sonora 2026 amplía sus premios y los \"pasaportes\" para actuar en festivales": "Sonora 2026 erweitert seine Preise und Festival-Pässe",
        "El concurso musical Sonora extiende sus \"pasaportes\" a La Palma y La Gomera": "Der Musikwettbewerb Sonora erweitert seine Pässe auf La Palma und La Gomera",
        "Sonora Oro": "Sonora Gold",
        "Sonora Plata": "Sonora Silber",
        "Sonora Bronce": "Sonora Bronze",
        "Edición 2026": "Ausgabe 2026",
        "La edición 2026 ha batido el récord de participación con <strong style=\"color:var(--text)\">195 inscritos</strong>. El proceso se divide en dos grandes fases: las rondas eliminatorias dan paso a las finales de primavera, y los mejores actúan en el gran festival de octubre ante el público del Auditorio Alfredo Kraus.": "Die Ausgabe 2026 hat mit <strong style=\"color:var(--text)\">195 Anmeldungen</strong> den Teilnahmerekord gebrochen. Der Prozess gliedert sich in zwei große Phasen: Ausscheidungsrunden führen zu den Frühlingsfinals, und die besten Acts treten beim großen Oktoberfestival vor dem Publikum des Auditorio Alfredo Kraus auf.",
        "Fase 1": "Phase 1",
        "Fase 2": "Phase 2",
        "Finales de primavera": "Frühlingsfinale",
        "Festival de octubre": "Oktoberfestival",
        "17 y 18 de abril de 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. Los 10 finalistas se miden en directo ante el jurado y el público.": "17. und 18. April 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. Die 10 Finalisten treten live vor Jury und Publikum an.",
        "17 y 18 de abril de 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. Los 10 finalistas se miden live ante el jurado y el público.": "17. und 18. April 2026 · Sala Jerónimo Saavedra, Auditorio Alfredo Kraus. Die 10 Finalisten treten live vor Jury und Publikum an.",
        "16, 17 y 18 de octubre de 2026 · Auditorio Alfredo Kraus. El gran festival, con los ganadores y artistas invitados, cierra la edición con tres noches de música en directo.": "16., 17. und 18. Oktober 2026 · Auditorio Alfredo Kraus. Das große Festival mit Gewinnern und Gastkünstlern schließt die Ausgabe mit drei Nächten Live-Musik ab.",
        "16, 17 y 18 de octubre de 2026 · Auditorio Alfredo Kraus. El gran festival, con los ganadores y artistas invitados, cierra la edición con tres noches de música live.": "16., 17. und 18. Oktober 2026 · Auditorio Alfredo Kraus. Das große Festival mit Gewinnern und Gastkünstlern schließt die Ausgabe mit drei Nächten Live-Musik ab.",
        "Galería Sonora 2026": "Sonora-Galerie 2026",
        "Los 10 finalistas de la edición 2026 y momentos del certamen.": "Die 10 Finalisten der Ausgabe 2026 und Momente des Wettbewerbs.",
        "Final en el Auditorio Alfredo Kraus": "Finale im Auditorio Alfredo Kraus",
        "Jurado preselección 2026": "Vorauswahljury 2026",
        "Los ganadores Sonora 2026": "Die Sonora-Gewinner 2026",
        "Los Blody y Good Franco, ganadores absolutos del Sonora 2026": "Los Blody und Good Franco, Gesamtsieger von Sonora 2026",
        "El certamen Sonora 2026 da a conocer las 10 propuestas musicales de su gran final": "Sonora 2026 gibt die 10 Musikprojekte seines großen Finales bekannt",
        "El Sonora 2026 amplía sus premios y los \"pasaportes\" para actuar en festivales": "Sonora 2026 erweitert seine Preise und Festivalpässe",
        "El concurso musical Sonora extiende sus \"pasaportes\" a La Palma y La Gomera": "Der Musikwettbewerb Sonora erweitert seine Pässe auf La Palma und La Gomera",
        "Web oficial": "Offizielle Website",
        "festivalsonora.com — Toda la información, bases del concurso e inscripciones": "festivalsonora.com — Alle Informationen, Wettbewerbsregeln und Anmeldung",
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
    html = translate_cultural_project_fragments(html, lang)
    html = translate_cultural_project_fragments(html, lang)
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
