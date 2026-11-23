"""Refresh historical concert HTML from the venue's local date before publishing."""
from __future__ import annotations

import argparse
from datetime import date, datetime
from html import escape, unescape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parents[1]
EVENT_TYPES = {'Event', 'MusicEvent', 'Festival'}
LD = re.compile(r'(<script\b[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)', re.S)
LINKS = re.compile(r'<a\b([^>]*?)\s+href="([^"]*)"([^>]*)>(.*?)</a>', re.S)
TICKET_HOSTS = {
    'aclamclub.cat', 'auditorioalfredokraus.es', 'babylonmadrid.com', 'elteatroguiniguada.com',
    'enterticket.es', 'entradas.plus', 'entradium.com', 'tickety.es', 'ticketandroll.com',
    'tureservaonline.es',
}
LOCALES = {
    'es': ('conciertos', 'conciertos.json', '/proximos-conciertos/', 'Este concierto ya se celebró.', 'Ver próximos conciertos'),
    'en': ('en/concerts', 'concerts.en.json', '/en/upcoming-concerts/', 'This concert has already taken place.', 'See upcoming concerts'),
    'de': ('de/konzerte', 'concerts.de.json', '/de/kommende-konzerte/', 'Dieses Konzert hat bereits stattgefunden.', 'Kommende Konzerte ansehen'),
}


def events(value):
    if isinstance(value, list):
        for item in value:
            yield from events(item)
    elif isinstance(value, dict):
        if value.get('@type') in EVENT_TYPES:
            yield value
        for key in ('@graph', 'itemListElement', 'item', 'subEvent'):
            if key in value:
                yield from events(value[key])


def local_today(zone):
    try:
        return datetime.now(ZoneInfo(zone)).date()
    except ZoneInfoNotFoundError:
        raise SystemExit('Use --as-of YYYY-MM-DD when the host has no timezone database.') from None


def archive_html(text, agenda, notice, label):
    def remove_offers(match):
        data = json.loads(match[2])
        expired_sales = [event for event in events(data) if 'offers' in event]
        if not expired_sales:
            return match[0]
        for event in expired_sales:
            del event['offers']
        return match[1] + json.dumps(data, ensure_ascii=False, indent=2) + match[3]

    def replace_purchase(match):
        before, url, after, body = match.groups()
        attrs = before + after
        host = urlsplit(unescape(url)).hostname or ''
        is_seller = any(host == seller or host.endswith('.' + seller) for seller in TICKET_HOSTS)
        is_purchase = 'data-event-ticket' in attrs or re.search(r'compra|buy|ticket|kaufen|taquilla|entradas', unescape(body), re.I)
        if not (is_seller and is_purchase):
            return match[0]
        attrs = re.sub(r'\s(?:target|aria-label|rel|data-(?:event-ticket|analytics-[\w-]+))(?:="[^"]*")?', '', attrs)
        return f'<a{attrs} href="{agenda}">{escape(label)}</a>'

    text = LD.sub(remove_offers, text)
    text = LINKS.sub(replace_purchase, text)
    if 'id="event-archive-note"' not in text:
        text = re.sub(r'</h1>', '</h1>\n<p id="event-archive-note" class="event-guest">'
                      + escape(notice) + '</p>', text, count=1)
    return text


def refresh(as_of=None, check=False):
    changed = []
    for folder, feed, agenda, notice, label in LOCALES.values():
        concert_end = {
            item['linkInfo']: item.get('endDateISO') or item['dateISO']
            for item in json.loads((ROOT / feed).read_text(encoding='utf-8'))
        }
        for path in (ROOT / folder).glob('[0-9][0-9][0-9][0-9]/**/index.html'):
            text = path.read_bytes().decode('utf-8')
            route = '/' + path.parent.relative_to(ROOT).as_posix() + '/'
            dates = re.findall(r'data-event-last-date="(\d{4}-\d{2}-\d{2})"', text)
            if route in concert_end:
                dates.append(concert_end[route])
            for match in LD.finditer(text):
                for event in events(json.loads(match[2])):
                    event_end = event.get('endDate') or event.get('startDate')
                    if event_end:
                        dates.append(event_end[:10])
            if not dates:
                continue
            zone = re.search(r'data-event-timezone="([^"]+)"', text)
            today = as_of or local_today(zone[1] if zone else 'Atlantic/Canary')
            if date.fromisoformat(max(dates)) >= today:
                continue
            result = archive_html(text, agenda, notice, label)
            if result != text:
                changed.append(route)
                if not check:
                    path.write_bytes(result.encode('utf-8'))
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--as-of', type=date.fromisoformat, help='Override the current local date (YYYY-MM-DD).')
    parser.add_argument('--check', action='store_true', help='Report outdated pages without editing files.')
    options = parser.parse_args()
    changes = refresh(options.as_of, options.check)
    if changes:
        print('\n'.join(changes))
    print(f'{len(changes)} historical pages {"need changes" if options.check else "updated"}.')
    raise SystemExit(bool(changes) if options.check else 0)
