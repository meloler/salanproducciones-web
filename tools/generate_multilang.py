from __future__ import annotations

import json
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
        "Sala": "Venue",
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
        "Salán Producciones presenta": "Salan Producciones presents",
        "Salan Producciones presenta": "Salan Producciones presents",
        "artista invitado": "guest artist",
        "+ artista invitado": "+ guest artist",
        "Mira un adelanto del directo antes del": "Watch a preview of the live show before",
        "No te quedes fuera": "Do not miss out",
        "Consigue tus entradas antes de que se agoten.": "Get your tickets before they sell out.",
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
        "Sala": "Ort",
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
        "Salán Producciones presenta": "Salan Producciones präsentiert",
        "Salan Producciones presenta": "Salan Producciones präsentiert",
        "artista invitado": "Gastkünstler",
        "+ artista invitado": "+ Gastkünstler",
        "Mira un adelanto del directo antes del": "Sieh dir vorab einen Eindruck der Live-Show an vor dem",
        "No te quedes fuera": "Nicht verpassen",
        "Consigue tus entradas antes de que se agoten.": "Sichere dir Tickets, bevor sie ausverkauft sind.",
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
            },
            "de": {
                "Salán Producciones — Canarias · Desde 1987": "Salán Producciones — Kanarische Inseln · Seit 1987",
                "Conciertos en directo<br>en <em>España</em><br>desde 1987": "Live-Konzerte<br>in <em>Spanien</em><br>seit 1987",
                "Promotor musical de referencia en Gran Canaria y Tenerife. Rock, blues, soul y música alternativa en directo en las Islas Canarias.": "Musikveranstalter auf Gran Canaria und Teneriffa. Rock, Blues, Soul und alternative Live-Musik auf den Kanarischen Inseln.",
                "Años de trayectoria": "Jahre Erfahrung",
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
            },
            "de": {
                "Las Palmas de Gran Canaria · 1988 — 2000": "Las Palmas de Gran Canaria · 1988 — 2000",
                "Durante doce años, el Pub La Calle fue el corazón de la escena musical alternativa en Las Palmas de Gran Canaria. Una sala que equiparó la capital grancanaria con las ciudades más importantes del circuito de conciertos nacional.": "Zwölf Jahre lang war Pub La Calle das Herz der alternativen Musikszene in Las Palmas de Gran Canaria. Ein Club, der die Stadt mit den wichtigsten Konzertorten Spaniens verband.",
                "Años de historia": "Jahre Geschichte",
                "Año de apertura": "Eröffnung",
                "Cierre": "Schließung",
                "Artistas": "Künstler",
                "Recuerdos": "Erinnerungen",
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
        html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
        html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', html, count=1)
        html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', html, count=1)
    return html


def transform(source_html: str, es: str, en: str, de: str, lang: str, routes: dict[str, dict[str, str]], key: str, slug: str | None = None, title_hint: str | None = None) -> str:
    html = replace_head_seo(source_html, es, en, de, lang)
    html = rewrite_links(html, routes, lang)
    html = translate_page_specific(html, lang, key)
    if key == "concert":
        html = translate_event_text(html, lang)
        html = replace_event_desc(html, slug, lang)
    html = translate_common(html, lang)
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
