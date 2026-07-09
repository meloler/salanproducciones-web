from __future__ import annotations

import html
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://www.salanproducciones.com"


STATIC_PAGES = [
    {
        "key": "home",
        "es": "/",
        "en": "/en/",
        "de": "/de/",
        "title": {"en": "Salan Producciones | Concerts and Live Music in Spain", "de": "Salan Producciones | Konzerte und Live-Musik in Spanien"},
        "h1": {"en": "Concerts and live music", "de": "Konzerte und Live-Musik"},
        "eyebrow": {"en": "Music production from the Canary Islands", "de": "Musikproduktion von den Kanarischen Inseln"},
        "desc": {
            "en": "Salán Producciones promotes rock, blues, soul and cultural events in the Canary Islands and across Spain. Discover upcoming concerts and official ticket links.",
            "de": "Salán Producciones veranstaltet Rock-, Blues-, Soul- und Kulturereignisse auf den Kanarischen Inseln und in ganz Spanien. Entdecke kommende Konzerte und offizielle Ticketlinks.",
        },
        "cta": {"en": "Upcoming concerts", "de": "Kommende Konzerte"},
        "cta_url": {"en": "/en/upcoming-concerts/", "de": "/de/kommende-konzerte/"},
    },
    {
        "key": "upcoming",
        "es": "/proximos-conciertos/",
        "en": "/en/upcoming-concerts/",
        "de": "/de/kommende-konzerte/",
        "title": {"en": "Upcoming Concerts in Spain | Salan Producciones", "de": "Kommende Konzerte in Spanien | Salan Producciones"},
        "h1": {"en": "Upcoming concerts in Spain", "de": "Kommende Konzerte in Spanien"},
        "eyebrow": {"en": "Agenda", "de": "Agenda"},
        "desc": {
            "en": "Official agenda for the concerts promoted by Salán Producciones. Rock, blues, soul and live music in the Canary Islands and Spain.",
            "de": "Offizielle Agenda der von Salán Producciones produzierten Konzerte. Rock, Blues, Soul und Live-Musik auf den Kanaren und in Spanien.",
        },
        "grid": "agenda-grid",
    },
    {
        "key": "past",
        "es": "/conciertos-anteriores/",
        "en": "/en/past-concerts/",
        "de": "/de/vergangene-konzerte/",
        "title": {"en": "Past Concerts | Salan Producciones", "de": "Vergangene Konzerte | Salan Producciones"},
        "h1": {"en": "Past concerts", "de": "Vergangene Konzerte"},
        "eyebrow": {"en": "Archive", "de": "Archiv"},
        "desc": {
            "en": "A living archive of concerts and cultural projects promoted by Salán Producciones over more than three decades.",
            "de": "Ein lebendiges Archiv der Konzerte und Kulturprojekte, die Salán Producciones seit mehr als drei Jahrzehnten begleitet.",
        },
        "grid": "concerts-timeline",
    },
    {
        "key": "pub",
        "es": "/pub-la-calle/",
        "en": "/en/pub-la-calle/",
        "de": "/de/pub-la-calle/",
        "title": {"en": "Pub La Calle | Rock venue in Las Palmas 1988-2000", "de": "Pub La Calle | Rockclub in Las Palmas 1988-2000"},
        "h1": {"en": "Pub La Calle", "de": "Pub La Calle"},
        "eyebrow": {"en": "Legacy", "de": "Geschichte"},
        "desc": {
            "en": "The story of Pub La Calle, the Las Palmas venue that became part of the musical memory of the Canary Islands between 1988 and 2000.",
            "de": "Die Geschichte des Pub La Calle, des Clubs in Las Palmas, der zwischen 1988 und 2000 Teil des musikalischen Gedächtnisses der Kanarischen Inseln wurde.",
        },
        "body": {
            "en": "This section preserves the memory of a venue, a scene and a way of understanding live music. The Spanish page remains the source text for names, dates and historical details.",
            "de": "Dieser Bereich bewahrt die Erinnerung an einen Club, eine Szene und eine besondere Art, Live-Musik zu verstehen. Die spanische Seite bleibt die Quelle für Namen, Daten und historische Details.",
        },
    },
    {
        "key": "cultural",
        "es": "/proyectosculturales/",
        "en": "/en/cultural-projects/",
        "de": "/de/kulturprojekte/",
        "title": {"en": "Cultural Projects | Salan Producciones", "de": "Kulturprojekte | Salan Producciones"},
        "h1": {"en": "Cultural projects", "de": "Kulturprojekte"},
        "eyebrow": {"en": "Beyond concerts", "de": "Mehr als Konzerte"},
        "desc": {
            "en": "Festivals, cultural collaborations and special projects connected with music, film and live creation.",
            "de": "Festivals, kulturelle Kooperationen und besondere Projekte rund um Musik, Film und Live-Kultur.",
        },
    },
    {
        "key": "contact",
        "es": "/contacto/",
        "en": "/en/contact/",
        "de": "/de/kontakt/",
        "title": {"en": "Contact | Salan Producciones", "de": "Kontakt | Salan Producciones"},
        "h1": {"en": "Contact", "de": "Kontakt"},
        "eyebrow": {"en": "Let us talk", "de": "Kontakt aufnehmen"},
        "desc": {
            "en": "Contact Salán Producciones for concert information, tickets, press, collaborations or memories of Pub La Calle.",
            "de": "Kontaktiere Salán Producciones für Informationen zu Konzerten, Tickets, Presse, Kooperationen oder Erinnerungen an Pub La Calle.",
        },
        "form": True,
    },
    {
        "key": "privacy",
        "es": "/privacidad/",
        "en": "/en/privacy/",
        "de": "/de/datenschutz/",
        "title": {"en": "Privacy Policy | Salan Producciones", "de": "Datenschutzerklarung | Salan Producciones"},
        "h1": {"en": "Privacy policy", "de": "Datenschutzerklarung"},
        "eyebrow": {"en": "Legal", "de": "Rechtliches"},
        "desc": {"en": "Information about privacy and personal data processing on this website.", "de": "Informationen zum Datenschutz und zur Verarbeitung personenbezogener Daten auf dieser Website."},
        "legal": True,
    },
    {
        "key": "legal",
        "es": "/aviso-legal/",
        "en": "/en/legal-notice/",
        "de": "/de/impressum/",
        "title": {"en": "Legal Notice | Salan Producciones", "de": "Impressum | Salan Producciones"},
        "h1": {"en": "Legal notice", "de": "Impressum"},
        "eyebrow": {"en": "Legal", "de": "Rechtliches"},
        "desc": {"en": "Legal information about the owner and use of this website.", "de": "Rechtliche Informationen zum Betreiber und zur Nutzung dieser Website."},
        "legal": True,
    },
    {
        "key": "cookies",
        "es": "/cookies/",
        "en": "/en/cookies/",
        "de": "/de/cookies/",
        "title": {"en": "Cookie Policy | Salan Producciones", "de": "Cookie-Richtlinie | Salan Producciones"},
        "h1": {"en": "Cookie policy", "de": "Cookie-Richtlinie"},
        "eyebrow": {"en": "Legal", "de": "Rechtliches"},
        "desc": {"en": "Information about the cookies used for analytics, advertising and basic site operation.", "de": "Informationen zu Cookies fuer Analyse, Werbung und den grundlegenden Betrieb der Website."},
        "legal": True,
    },
]

PROJECT_PAGES = [
    ("womex", "WOMEX", "World music and professional cultural meeting.", "Weltmusik und professionelles Kulturtreffen."),
    ("cinezin", "Cinezin", "Film, music and independent culture project.", "Projekt fuer Film, Musik und unabhaengige Kultur."),
    ("festivalsonora", "Festival Sonora", "Music festival and emerging talent platform.", "Musikfestival und Plattform fuer neue Talente."),
]


def read_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path: str, content: str):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def abs_url(path: str) -> str:
    return DOMAIN + path


def alt_links(es: str, en: str, de: str, current: str) -> str:
    canon = {"es": es, "en": en, "de": de}[current]
    return "\n".join(
        [
            f'  <link rel="canonical" href="{abs_url(canon)}">',
            f'  <link rel="alternate" hreflang="es" href="{abs_url(es)}">',
            f'  <link rel="alternate" hreflang="en" href="{abs_url(en)}">',
            f'  <link rel="alternate" hreflang="de" href="{abs_url(de)}">',
            f'  <link rel="alternate" hreflang="x-default" href="{abs_url(es)}">',
        ]
    )


def nav(lang: str) -> str:
    labels = {
        "en": [("Home", "/en/"), ("Upcoming concerts", "/en/upcoming-concerts/"), ("Past", "/en/past-concerts/"), ("Pub La Calle", "/en/pub-la-calle/"), ("Cultural projects", "/en/cultural-projects/"), ("Contact", "/en/contact/")],
        "de": [("Start", "/de/"), ("Kommende Konzerte", "/de/kommende-konzerte/"), ("Archiv", "/de/vergangene-konzerte/"), ("Pub La Calle", "/de/pub-la-calle/"), ("Kulturprojekte", "/de/kulturprojekte/"), ("Kontakt", "/de/kontakt/")],
    }[lang]
    links = "\n      ".join(f'<a href="{url}">{text}</a>' for text, url in labels)
    return f"""<header class="site-header" role="banner">
  <div class="nav-inner">
    <a href="/{lang}/" class="nav-logo" aria-label="Salán Producciones">
      <img src="/assets/images/logo-salan.png" alt="Salán Producciones" height="36" style="height:36px;width:auto;display:block;filter:brightness(0) invert(1);">
    </a>
    <nav class="nav-links" aria-label="Main navigation">
      {links}
    </nav>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <nav class="nav-mobile" aria-label="Mobile menu">
    {links}
  </nav>
</header>"""


def footer(lang: str) -> str:
    copy = {
        "en": ("More than 35 years producing and promoting live music in the Canary Islands and Spain.", "Sections", "Contact", "Privacy", "Legal notice", "Cookies"),
        "de": ("Seit mehr als 35 Jahren Produktion und Promotion von Live-Musik auf den Kanaren und in Spanien.", "Bereiche", "Kontakt", "Datenschutz", "Impressum", "Cookies"),
    }[lang]
    base = "/en" if lang == "en" else "/de"
    legal = ("/privacy/", "/legal-notice/", "/cookies/") if lang == "en" else ("/datenschutz/", "/impressum/", "/cookies/")
    sections = (
        [("Upcoming concerts", "/upcoming-concerts/"), ("Past concerts", "/past-concerts/"), ("Pub La Calle", "/pub-la-calle/"), ("Cultural projects", "/cultural-projects/"), (copy[2], "/contact/")]
        if lang == "en"
        else [("Kommende Konzerte", "/kommende-konzerte/"), ("Archiv", "/vergangene-konzerte/"), ("Pub La Calle", "/pub-la-calle/"), ("Kulturprojekte", "/kulturprojekte/"), (copy[2], "/kontakt/")]
    )
    section_links = "\n          ".join(f'<li><a href="{base}{url}">{label}</a></li>' for label, url in sections)
    return f"""<footer class="site-footer" role="contentinfo">
  <div class="container">
    <div class="footer-inner">
      <div>
        <div class="footer-brand-name">Salán <span>Producciones</span></div>
        <p class="footer-brand-desc">{copy[0]}</p>
        <div class="footer-social" aria-label="Social media">
          <a href="https://www.facebook.com/salanproducciones" target="_blank" rel="noopener noreferrer" aria-label="Facebook">f</a>
          <a href="https://www.instagram.com/salanjuan" target="_blank" rel="noopener noreferrer" aria-label="Instagram">ig</a>
          <a href="https://www.youtube.com/@juansalan" target="_blank" rel="noopener noreferrer" aria-label="YouTube">yt</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">{copy[1]}</div>
        <ul class="footer-links">
          {section_links}
        </ul>
      </div>
      <div>
        <div class="footer-col-title">{copy[2]}</div>
        <div class="footer-contact-item"><span>Tel</span><a href="tel:+34637138073">637 138 073</a></div>
        <div class="footer-contact-item"><span>Email</span><a href="{base}{'/contact/' if lang == 'en' else '/kontakt/'}">{copy[2]}</a></div>
        <div class="footer-contact-item"><span>Map</span><span>Canary Islands, Spain</span></div>
      </div>
    </div>
    <div class="footer-bottom">
      <p class="footer-copy">© 2026 Salán Producciones SL.</p>
      <div class="footer-legal">
        <a href="{base}{legal[0]}">{copy[3]}</a>
        <a href="{base}{legal[1]}">{copy[4]}</a>
        <a href="{base}{legal[2]}" onclick="window.salanCookiesOpen &amp;&amp; window.salanCookiesOpen(); return false;">{copy[5]}</a>
      </div>
    </div>
  </div>
</footer>"""


def cookie_banner(lang: str) -> str:
    text = {
        "en": ("We use first-party and third-party cookies for analytics, advertising and basic site operation.", "More information", "Necessary only", "Accept all"),
        "de": ("Wir verwenden eigene Cookies und Cookies von Drittanbietern fuer Analyse, Werbung und den grundlegenden Betrieb der Website.", "Mehr Informationen", "Nur notwendige", "Alle akzeptieren"),
    }[lang]
    return f"""<div id="cookie-banner" style="display:none;position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#111111;border-top:1px solid #2a2a2a;padding:18px 24px;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap">
  <p style="margin:0;font-size:.85rem;color:#888;max-width:680px;line-height:1.5">{text[0]} <a href="/{lang}/cookies/" style="color:#e8c44d;text-decoration:underline">{text[1]}</a></p>
  <div style="display:flex;gap:12px;flex-shrink:0;flex-wrap:wrap">
    <button id="ck-accept-necessary" style="padding:10px 20px;background:transparent;color:#888;border:1px solid #2a2a2a;border-radius:4px;cursor:pointer;font-size:.85rem;font-family:inherit;white-space:nowrap">{text[2]}</button>
    <button id="ck-accept-all" style="padding:10px 20px;background:#e8c44d;color:#000;border:none;border-radius:4px;cursor:pointer;font-size:.85rem;font-weight:700;font-family:inherit;white-space:nowrap">{text[3]}</button>
  </div>
</div>"""


def head(title: str, desc: str, lang: str, es: str, en: str, de: str, image: str = "/assets/images/salan-og.jpg") -> str:
    locale = "en_US" if lang == "en" else "de_DE"
    current = {"en": en, "de": de}[lang]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.ico" type="image/x-icon">
  <link rel="apple-touch-icon" href="/assets/favicon.jpg">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0a0a0a">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
{alt_links(es, en, de, lang)}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="{locale}">
  <meta property="og:url" content="{abs_url(current)}">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:image" content="{abs_url(image)}">
  <meta property="og:site_name" content="Salán Producciones">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html.escape(title)}">
  <meta name="twitter:description" content="{html.escape(desc)}">
  <meta name="twitter:image" content="{abs_url(image)}">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap"></noscript>
  <link rel="stylesheet" href="/assets/css/main.css?v=3">
</head>"""


def page_html(page: dict, lang: str) -> str:
    es, en, de = page["es"], page["en"], page["de"]
    title = page["title"][lang]
    desc = page["desc"][lang]
    body = ""
    if page.get("grid") == "agenda-grid":
        body = f'<div class="concerts-grid" id="agenda-grid"></div>'
    elif page.get("grid") == "concerts-timeline":
        body = f'<div id="concerts-timeline" class="timeline"></div>'
    elif page.get("form"):
        submit = "Send message" if lang == "en" else "Nachricht senden"
        name = "Name" if lang == "en" else "Name"
        subject = "Subject" if lang == "en" else "Betreff"
        message = "Message" if lang == "en" else "Nachricht"
        body = f"""<form id="contact-form" class="contact-form" action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="384b54b5-88de-4130-b7ed-073508be7aaf">
  <input type="hidden" name="subject" value="New message from salanproducciones.com">
  <div class="form-group"><label class="form-label" for="name">{name}</label><input class="form-input" id="name" name="from_name" required></div>
  <div class="form-group"><label class="form-label" for="email">Email</label><input class="form-input" id="email" name="email" type="email" required></div>
  <div class="form-group"><label class="form-label" for="subject">{subject}</label><input class="form-input" id="subject" name="category" required></div>
  <div class="form-group"><label class="form-label" for="message">{message}</label><textarea class="form-textarea" id="message" name="message" required></textarea></div>
  <button type="submit" class="btn btn-primary btn-lg">{submit}</button>
</form>"""
    elif page.get("legal"):
        body = f'<div class="bio-card"><div class="bio-text"><h2>{html.escape(page["h1"][lang])}</h2><p>{html.escape(desc)}</p><p>Salán Producciones SL. Canary Islands, Spain.</p></div></div>'
    elif page.get("key") == "cultural":
        items = "".join(project_card(slug, title, en_desc if lang == "en" else de_desc, lang) for slug, title, en_desc, de_desc in PROJECT_PAGES)
        body = f'<div class="concerts-grid">{items}</div>'
    elif page.get("key") == "home":
        heading = "Upcoming concerts" if lang == "en" else "Kommende Konzerte"
        intro = "Official ticket links and confirmed dates." if lang == "en" else "Offizielle Ticketlinks und bestätigte Termine."
        body_text = page.get("body", {}).get(lang, desc)
        cta = page.get("cta", {}).get(lang)
        cta_html = f'<a href="{page["cta_url"][lang]}" class="btn btn-primary">{cta}</a>' if cta else ""
        body = f"""
<div class="bio-card" style="margin-bottom:48px"><div class="bio-text"><h2>{html.escape(page["h1"][lang])}</h2><p>{html.escape(body_text)}</p>{cta_html}</div></div>
<div class="section-header reveal"><span class="section-label">{html.escape(page["eyebrow"][lang])}</span><h2 class="section-title">{heading}</h2><p class="section-desc">{intro}</p></div>
<div class="concerts-grid" id="upcoming-grid"></div>
"""
    else:
        body_text = page.get("body", {}).get(lang, desc)
        cta = page.get("cta", {}).get(lang)
        cta_html = f'<a href="{page["cta_url"][lang]}" class="btn btn-primary">{cta}</a>' if cta else ""
        body = f'<div class="bio-card"><div class="bio-text"><h2>{html.escape(page["h1"][lang])}</h2><p>{html.escape(body_text)}</p>{cta_html}</div></div>'
    return f"""{head(title, desc, lang, es, en, de)}
<body>
{nav(lang)}
<section class="page-hero">
  <div class="container">
    <p class="page-hero-eyebrow">{html.escape(page["eyebrow"][lang])}</p>
    <h1 class="page-hero-title"><span>{html.escape(page["h1"][lang])}</span></h1>
    <p class="page-hero-desc">{html.escape(desc)}</p>
  </div>
</section>
<section class="section">
  <div class="container">{body}</div>
</section>
{footer(lang)}
{cookie_banner(lang)}
<script src="/assets/js/cookies.js" defer></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def project_card(slug: str, title: str, desc: str, lang: str) -> str:
    base = "/en/cultural-projects" if lang == "en" else "/de/kulturprojekte"
    label = "View project" if lang == "en" else "Projekt ansehen"
    return f"""<article class="concert-card reveal">
  <div class="concert-card-body">
    <h2 class="concert-card-title">{html.escape(title)}</h2>
    <p class="concert-card-venue">{html.escape(desc)}</p>
    <a href="{base}/{slug}/" class="btn btn-outline">{label}</a>
  </div>
</article>"""


def translate_concert(c: dict, lang: str) -> dict:
    d = dict(c)
    replacements = {
        "en": {
            "Abril": "April", "Mayo": "May", "Junio": "June", "Septiembre": "September", "Noviembre": "November",
            "Gira España": "Spain Tour", "Gira Península": "Mainland Spain Tour", "Canarias": "Canary Islands",
            "Gran Canaria": "Gran Canaria", "Tenerife": "Tenerife", "Desde": "From", "Entradas próximamente": "Tickets coming soon",
            "Próximamente": "Coming soon", "Comprar": "Buy", "Agotado": "Sold out", "España": "Spain",
        },
        "de": {
            "Abril": "April", "Mayo": "Mai", "Junio": "Juni", "Septiembre": "September", "Noviembre": "November",
            "Gira España": "Spanien-Tour", "Gira Península": "Tour Festland Spanien", "Canarias": "Kanarische Inseln",
            "Gran Canaria": "Gran Canaria", "Tenerife": "Teneriffa", "Desde": "Ab", "Entradas próximamente": "Tickets bald verfügbar",
            "Próximamente": "Bald verfügbar", "Comprar": "Kaufen", "Agotado": "Ausverkauft", "España": "Spanien",
        },
    }[lang]
    for key in ["dateDisplay", "subtitle", "venue", "badge", "price", "buyAria", "buttonLabel"]:
        value = d.get(key)
        if isinstance(value, str):
            for src, dst in replacements.items():
                value = value.replace(src, dst)
            d[key] = value
    prefix = "/en/concerts/2026/" if lang == "en" else "/de/konzerte/2026/"
    d["linkInfo"] = prefix + d["id"] + "/"
    if d.get("linkBuy"):
        sep = "&" if "?" in d["linkBuy"] else "?"
        if "utm_source=" not in d["linkBuy"]:
            d["linkBuy"] = f'{d["linkBuy"]}{sep}utm_source=landing&utm_medium=web&utm_campaign={d["id"]}-{lang}'
    return d


def concert_page(c: dict, lang: str) -> str:
    slug = c["id"]
    es = f"/conciertos/2026/{slug}/"
    en = f"/en/concerts/2026/{slug}/"
    de = f"/de/konzerte/2026/{slug}/"
    city = c.get("venue", "").split("·")[-1].strip() if "·" in c.get("venue", "") else c.get("venue", "")
    h1 = f'{c["title"]} in {city}' if lang == "en" else f'{c["title"]} in {city}'
    title = f'{h1} | Salan Producciones'
    desc = (
        f'Official information and tickets for {c["title"]}. {c.get("dateDisplay", "")}. {c.get("venue", "")}.'
        if lang == "en"
        else f'Offizielle Informationen und Tickets für {c["title"]}. {c.get("dateDisplay", "")}. {c.get("venue", "")}.'
    )
    buy = "Buy tickets" if lang == "en" else "Tickets kaufen"
    video = "Watch video" if lang == "en" else "Video ansehen"
    about = f'About {c["title"]}' if lang == "en" else f'Über {c["title"]}'
    presents = "Salan Producciones presents" if lang == "en" else "Salan Producciones präsentiert"
    info_labels = ("Date", "Venue", "Price") if lang == "en" else ("Datum", "Ort", "Preis")
    preview = f'{c["title"]} live music preview.' if lang == "en" else f'Live-Vorschau von {c["title"]}.'
    intro = (
        f'{c["title"]} arrives with a live show promoted by Salán Producciones. Check the confirmed date, venue and official ticket link before booking.'
        if lang == "en"
        else f'{c["title"]} kommt mit einer Live-Show von Salán Producciones. Prüfe Datum, Ort und offiziellen Ticketlink vor der Buchung.'
    )
    poster = c["image"].replace("/poster.webp", "/poster-768.webp")
    buy_html = f'<a href="{html.escape(c.get("linkBuy") or es)}" class="btn btn-primary" target="_blank" rel="noopener noreferrer">{buy}</a>'
    schema_name = h1
    current_url = {"en": en, "de": de}[lang]
    start_date = f'{c.get("dateISO")}T20:00:00+01:00' if c.get("dateISO") else None
    end_date = f'{c.get("endDateISO", c.get("dateISO"))}T23:00:00+01:00' if c.get("dateISO") else None
    schema = {
        "@context": "https://schema.org",
        "@type": "MusicEvent",
        "name": schema_name,
        "startDate": start_date,
        "endDate": end_date,
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "url": abs_url(current_url),
        "image": abs_url(c["image"]),
        "organizer": {"@type": "Organization", "name": "Salan Producciones", "url": "https://salanproducciones.com"},
        "performer": {"@type": "MusicGroup", "name": c["title"]},
        "offers": {"@type": "Offer", "url": c.get("linkBuy") or abs_url(current_url), "priceCurrency": "EUR", "availability": "https://schema.org/InStock"},
    }
    breadcrumb_name = "Home" if lang == "en" else "Start"
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": breadcrumb_name, "item": abs_url("/en/" if lang == "en" else "/de/")},
            {"@type": "ListItem", "position": 2, "name": schema_name, "item": abs_url(current_url)},
        ],
    }
    head_html = head(title, desc, lang, es, en, de, c["image"]).replace(
        "</head>",
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>\n</head>',
    )
    return f"""{head_html}
<body>
{nav(lang)}
<section class="hero">
  <div class="hero-grid">
    <div class="poster-card"><img src="{poster}" alt="{html.escape(c["title"])}" loading="eager" fetchpriority="high" width="900" height="1260"></div>
    <div class="content-card">
      <span class="eyebrow">{presents}</span>
      <h1 class="event-title">{html.escape(h1)}</h1>
      <p class="event-desc">{html.escape(intro)}</p>
      <div class="info-grid">
        <div class="info-item"><div class="info-label">{info_labels[0]}</div><div class="info-value">{html.escape(c.get("dateDisplay", ""))}</div></div>
        <div class="info-item"><div class="info-label">{info_labels[1]}</div><div class="info-value">{html.escape(c.get("venue", ""))}</div></div>
        <div class="info-item"><div class="info-label">{info_labels[2]}</div><div class="info-value">{c.get("price", "")}</div></div>
      </div>
      <div class="cta-group">{buy_html}<a href="#video" class="btn btn-secondary">{video}</a></div>
    </div>
  </div>
</section>
<hr class="divider">
<div id="video" class="section"><h2 class="section-title">{video}</h2><p class="section-sub">{html.escape(preview)}</p></div>
<hr class="divider">
<div class="section"><div class="bio-card"><div class="bio-text"><h2>{html.escape(about)}</h2><p>{html.escape(intro)}</p><p>{html.escape(desc)}</p></div></div></div>
<div class="final-cta-wrap"><div class="final-cta"><div class="final-box"><h2>{buy}</h2><p>{html.escape(desc)}</p>{buy_html}</div></div></div>
{footer(lang)}
{cookie_banner(lang)}
<script src="/assets/js/cookies.js" defer></script>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""


def inject_hreflang_into_spanish(path: Path, es: str, en: str, de: str):
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if 'rel="alternate" hreflang="en"' in content:
        return
    block = "\n" + "\n".join(
        [
            f'  <link rel="alternate" hreflang="es" href="{abs_url(es)}">',
            f'  <link rel="alternate" hreflang="en" href="{abs_url(en)}">',
            f'  <link rel="alternate" hreflang="de" href="{abs_url(de)}">',
            f'  <link rel="alternate" hreflang="x-default" href="{abs_url(es)}">',
        ]
    )
    content = re.sub(r'(\s*<link rel="canonical"[^>]+>)', r'\1' + block, content, count=1)
    if 'property="og:locale"' not in content and '<meta property="og:type"' in content:
        content = content.replace('<meta property="og:type"', '<meta property="og:locale" content="es_ES">\n  <meta property="og:type"', 1)
    path.write_text(content, encoding="utf-8", newline="\n")


def update_spanish_pages(concerts: list[dict]):
    mapping = {p["key"]: p for p in STATIC_PAGES}
    spanish_paths = {
        "home": "index.html", "upcoming": "proximos-conciertos/index.html", "past": "conciertos-anteriores/index.html",
        "pub": "pub-la-calle/index.html", "cultural": "proyectosculturales/index.html", "contact": "contacto/index.html",
        "privacy": "privacidad/index.html", "legal": "aviso-legal/index.html", "cookies": "cookies/index.html",
    }
    for key, rel in spanish_paths.items():
        p = mapping[key]
        inject_hreflang_into_spanish(ROOT / rel, p["es"], p["en"], p["de"])
    for slug, _title, _en, _de in PROJECT_PAGES:
        inject_hreflang_into_spanish(ROOT / f"proyectosculturales/{slug}/index.html", f"/proyectosculturales/{slug}/", f"/en/cultural-projects/{slug}/", f"/de/kulturprojekte/{slug}/")
    for c in concerts:
        slug = c["id"]
        inject_hreflang_into_spanish(ROOT / f"conciertos/2026/{slug}/index.html", f"/conciertos/2026/{slug}/", f"/en/concerts/2026/{slug}/", f"/de/konzerte/2026/{slug}/")


def build_sitemap(concerts: list[dict]):
    entries = []
    for p in STATIC_PAGES:
        entries.append((p["es"], p["en"], p["de"], "weekly" if p["key"] in {"home", "upcoming"} else "monthly", "1.0" if p["key"] == "home" else "0.7"))
    for slug, _title, _en, _de in PROJECT_PAGES:
        entries.append((f"/proyectosculturales/{slug}/", f"/en/cultural-projects/{slug}/", f"/de/kulturprojekte/{slug}/", "monthly", "0.6"))
    for c in concerts:
        slug = c["id"]
        entries.append((f"/conciertos/2026/{slug}/", f"/en/concerts/2026/{slug}/", f"/de/konzerte/2026/{slug}/", "weekly", "0.8"))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for es, en, de, changefreq, priority in entries:
        for loc in [es, en, de]:
            lines.extend([
                "  <url>",
                f"    <loc>{escape(abs_url(loc))}</loc>",
                f'    <xhtml:link rel="alternate" hreflang="es" href="{escape(abs_url(es))}" />',
                f'    <xhtml:link rel="alternate" hreflang="en" href="{escape(abs_url(en))}" />',
                f'    <xhtml:link rel="alternate" hreflang="de" href="{escape(abs_url(de))}" />',
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{escape(abs_url(es))}" />',
                f"    <changefreq>{changefreq}</changefreq>",
                f"    <priority>{priority}</priority>",
                "  </url>",
            ])
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")


def main():
    concerts = read_json("conciertos.json")
    en_concerts = [translate_concert(c, "en") for c in concerts]
    de_concerts = [translate_concert(c, "de") for c in concerts]
    write("concerts.en.json", json.dumps(en_concerts, ensure_ascii=False, indent=2) + "\n")
    write("concerts.de.json", json.dumps(de_concerts, ensure_ascii=False, indent=2) + "\n")

    for page in STATIC_PAGES:
        write(page["en"].strip("/") + "/index.html" if page["en"] != "/en/" else "en/index.html", page_html(page, "en"))
        write(page["de"].strip("/") + "/index.html" if page["de"] != "/de/" else "de/index.html", page_html(page, "de"))

    for slug, title, en_desc, de_desc in PROJECT_PAGES:
        en_page = dict(STATIC_PAGES[4], key=slug, es=f"/proyectosculturales/{slug}/", en=f"/en/cultural-projects/{slug}/", de=f"/de/kulturprojekte/{slug}/", title={"en": f"{title} | Salan Producciones", "de": f"{title} | Salan Producciones"}, h1={"en": title, "de": title}, eyebrow={"en": "Cultural project", "de": "Kulturprojekt"}, desc={"en": en_desc, "de": de_desc})
        write(f"en/cultural-projects/{slug}/index.html", page_html(en_page, "en"))
        write(f"de/kulturprojekte/{slug}/index.html", page_html(en_page, "de"))

    for c in en_concerts:
        write(f"en/concerts/2026/{c['id']}/index.html", concert_page(c, "en"))
    for c in de_concerts:
        write(f"de/konzerte/2026/{c['id']}/index.html", concert_page(c, "de"))

    update_spanish_pages(concerts)
    build_sitemap(concerts)


if __name__ == "__main__":
    main()
