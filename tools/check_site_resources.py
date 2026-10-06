"""Check public local media references and static event fallbacks.

Run from any directory with: python tools/check_site_resources.py
The HTML event template is intentionally excluded because its poster is a placeholder.
"""
from __future__ import annotations

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
FEEDS = {
    "es": "conciertos.json",
    "en": "concerts.en.json",
    "de": "concerts.de.json",
}
PUBLIC_PAGES = {
    "home": {
        "es": "index.html",
        "en": "en/index.html",
        "de": "de/index.html",
    },
    "agenda": {
        "es": "proximos-conciertos/index.html",
        "en": "en/upcoming-concerts/index.html",
        "de": "de/kommende-konzerte/index.html",
    },
}
WOMEX_MEDIA = {
    "/proyectosculturales/womex/logo.webp",
    "/proyectosculturales/womex/foto-institucional.webp",
    "/proyectosculturales/womex/womex2018-1.webp",
    "/proyectosculturales/womex/womex2018-2.webp",
    "/proyectosculturales/womex/womex2018-3.webp",
    "/proyectosculturales/womex/womex2018-4.webp",
}
EVENT_ROUTE = re.compile(r"/(?:conciertos|concerts|konzerte)/2026/([^/]+)/")
EVENT_ROUTE_BY_LANGUAGE = {
    "es": "/conciertos/2026/",
    "en": "/en/concerts/2026/",
    "de": "/de/konzerte/2026/",
}


class PageReferences(HTMLParser):
    def __init__(self, source: str):
        super().__init__(convert_charrefs=True)
        self.media: list[str] = []
        self.articles: list[list[str]] = []
        self.article_links: list[str] | None = None
        self.carousel_depth = 0
        self.carousel_links: list[str] = []
        self.feed(source)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "article":
            self.article_links = []

        if tag == "div":
            if self.carousel_depth:
                self.carousel_depth += 1
            elif values.get("id") == "carousel-track":
                self.carousel_depth = 1

        for attr in ("src", "poster"):
            value = values.get(attr)
            if value:
                self.media.append(value)
        srcset = values.get("srcset")
        if srcset:
            self.media.extend(
                candidate.strip().split()[0]
                for candidate in srcset.split(",")
                if candidate.strip()
            )
        if tag == "meta" and (
            values.get("property", "").lower() == "og:image"
            or values.get("name", "").lower() == "twitter:image"
        ):
            value = values.get("content")
            if value:
                self.media.append(value)

        href = values.get("href")
        if tag == "a" and href:
            if self.article_links is not None:
                self.article_links.append(href)
            if self.carousel_depth:
                self.carousel_links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "article" and self.article_links is not None:
            self.articles.append(self.article_links)
            self.article_links = None
        if tag == "div" and self.carousel_depth:
            self.carousel_depth -= 1


def local_path(page: Path, url: str) -> Path | None:
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    path = unquote(parsed.path)
    if path.startswith("/"):
        return ROOT / path.lstrip("/")
    return page.parent / path


def media_errors() -> tuple[int, list[str]]:
    checked = 0
    errors: list[str] = []
    for page in ROOT.rglob("*.html"):
        relative = page.relative_to(ROOT)
        if relative.parts[0] in {".git", "output", "tools"}:
            continue
        if relative.as_posix() == "conciertos/PLANTILLA-evento.html":
            continue
        try:
            source = page.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            errors.append(f"{relative}: no se pudo leer como UTF-8 ({exc})")
            continue
        refs = PageReferences(source)
        for url in refs.media:
            target = local_path(page, url)
            if target is None:
                continue
            checked += 1
            if not target.is_file():
                errors.append(f"{relative}: recurso inexistente {url}")
    return checked, errors


def event_ids(links: list[str]) -> list[str]:
    return list(dict.fromkeys(
        match.group(1)
        for link in links
        if (match := EVENT_ROUTE.search(urlsplit(link).path))
    ))


def event_fallback_errors(feeds: dict[str, list[dict]]) -> list[str]:
    errors: list[str] = []
    base = {item["id"]: item for item in feeds["es"]}
    for lang, items in feeds.items():
        translated = {item["id"]: item for item in items}
        if translated.keys() != base.keys():
            errors.append(f"Feed {lang}: los identificadores no coinciden con el feed ES.")
            continue
        for event_id, es_item in base.items():
            item = translated[event_id]
            for key in ("dateISO", "endDateISO", "status", "image"):
                if item.get(key) != es_item.get(key):
                    errors.append(f"Feed {lang}, {event_id}: el campo {key} no coincide con ES.")
                    break
            buy = [urlsplit(es_item.get("linkBuy", "")), urlsplit(item.get("linkBuy", ""))]
            if buy[0].hostname != buy[1].hostname:
                errors.append(f"Feed {lang}, {event_id}: cambia el proveedor de entradas.")

    for item in base.values():
        finish = item.get("endDateISO") or item["dateISO"]
        if item.get("status") == "scheduled" and finish < TODAY:
            errors.append(
                f"Feed ES, {item['id']}: figura como futuro, pero terminó el {finish}."
            )

    expected = {
        event_id
        for event_id, item in base.items()
        if (item.get("endDateISO") or item["dateISO"]) >= TODAY
    }
    for area, pages in PUBLIC_PAGES.items():
        for lang, relative in pages.items():
            page = ROOT / relative
            source = page.read_text(encoding="utf-8-sig")
            refs = PageReferences(source)
            cards = event_ids([
                href
                for article in refs.articles
                for href in article
            ])
            if set(cards) != expected or len(cards) != len(expected):
                errors.append(
                    f"{relative}: las tarjetas estáticas deben listar {sorted(expected)}; "
                    f"encontré {cards}."
                )
            if area == "home":
                carousel = event_ids(refs.carousel_links)
                if set(carousel) != expected or len(carousel) != len(expected):
                    errors.append(
                        f"{relative}: el carrusel estático debe listar {sorted(expected)}; "
                        f"encontré {carousel}."
                    )
            if area == "agenda":
                lists = []
                for payload in re.findall(
                    r'<script type="application/ld\+json">(.*?)</script>', source, re.S
                ):
                    data = json.loads(payload)
                    if data.get("@type") == "ItemList":
                        lists.append(data)
                if len(lists) != 1:
                    errors.append(f"{relative}: se esperaba un ItemList y encontré {len(lists)}.")
                else:
                    structured = lists[0]
                    elements = structured.get("itemListElement", [])
                    ids = event_ids([
                        element.get("item", {}).get("url", "")
                        for element in elements
                        if isinstance(element, dict)
                    ])
                    item_urls = {
                        event_match.group(1): element.get("item", {}).get("url", "")
                        for element in elements
                        if isinstance(element, dict)
                        and isinstance(element.get("item"), dict)
                        and (
                            event_match := EVENT_ROUTE.search(
                                urlsplit(element["item"].get("url", "")).path
                            )
                        )
                    }
                    expected_urls = {
                        event_id: (
                            "https://www.salanproducciones.com"
                            + EVENT_ROUTE_BY_LANGUAGE[lang]
                            + event_id
                            + "/"
                        )
                        for event_id in expected
                    }
                    positions = [element.get("position") for element in elements]
                    if (
                        set(ids) != expected
                        or len(ids) != len(expected)
                        or item_urls != expected_urls
                        or structured.get("numberOfItems") != len(expected)
                        or positions != list(range(1, len(expected) + 1))
                    ):
                        errors.append(
                            f"{relative}: el ItemList no coincide con los próximos eventos {sorted(expected)}."
                        )

    womex_sets = {}
    for lang, relative in {
        "es": "proyectosculturales/womex/index.html",
        "en": "en/cultural-projects/womex/index.html",
        "de": "de/kulturprojekte/womex/index.html",
    }.items():
        page = ROOT / relative
        refs = PageReferences(page.read_text(encoding="utf-8-sig"))
        womex_sets[lang] = {urlsplit(value).path for value in refs.media if "/proyectosculturales/womex/" in value}
        if womex_sets[lang] != WOMEX_MEDIA:
            errors.append(
                f"{relative}: los recursos WOMEX no coinciden con los seis archivos compartidos."
            )
    return errors


def main() -> int:
    media_count, errors = media_errors()
    feeds = {
        lang: json.loads((ROOT / path).read_text(encoding="utf-8"))
        for lang, path in FEEDS.items()
    }
    errors.extend(event_fallback_errors(feeds))
    if errors:
        print(f"Comprobación con {len(errors)} problema(s):")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"OK: {media_count} referencias locales, feeds ES/EN/DE, "
        f"tarjetas estáticas próximas y recursos WOMEX."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
