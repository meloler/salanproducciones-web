"""Read-only consistency checks for the three static Kenny tour pages.
Run: python tools/check_kenny_sales.py
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[1]
SLUG='kenny-blues-boss-wayne-gira-espana-2026'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.tags=[];self.feed(text)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
source=json.loads((ROOT/'data/kenny-tour-2026.json').read_text())['cities']
for lang,path,feed in [('es','conciertos','conciertos.json'),('en','en/concerts','concerts.en.json'),('de','de/konzerte','concerts.de.json')]:
    route=f'/{path}/2026/{SLUG}/';p=ROOT/route.strip('/')/'index.html';s=p.read_text();page=Page(s)
    data=json.loads(re.search(r'<script id="kenny-dates" type="application/json">(.*?)</script>',s,re.S)[1])
    schema=json.loads(re.search(r'<script type="application/ld\+json">\s*(\[.*?\])\s*</script>',s,re.S)[1])
    assert len(data)==len(schema)==10
    links={a['data-ticket-city']:a['href'] for tag,a in page.tags if tag=='a' and 'data-ticket-city' in a}
    assert len(links)==10, 'Ten direct ticket links must work without JS'
    assert len([a for tag,a in page.tags if tag=='h1'])==1
    for city,event in zip(source,schema):
        id=city['id'];actual=data[id]
        for key in ('name','date','time','venue','price','url'):assert actual[key]==city[key],(lang,id,key)
        assert links[id]==city['url']
        assert event['startDate']==city['date']+'T'+city['time']+':00+02:00'
        assert 'endDate' not in event, 'Do not invent concert end times'
        assert float(event['offers']['price'])==city['price']
        assert event['offers']['url'].split('?')[0]==city['url']
    for tag,a in page.tags:
        url=a.get('src') or a.get('href','');parts=urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:continue
        dest=ROOT/parts.path.lstrip('/') if parts.path.startswith('/') else p.parent/parts.path
        assert dest.exists(),(lang,url)
    concert=next(c for c in json.loads((ROOT/feed).read_text()) if c['id']==SLUG)
    assert concert['linkBuy']==route+'#tour-active-city'
    assert 'New Westminster' not in s
    assert 'tickety.es/entity/kenny' not in s
    print(f'{lang}: 10 dates, totals, direct links, metadata and local assets OK')
print('All sales consistency checks passed.')
