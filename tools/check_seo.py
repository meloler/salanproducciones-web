"""Local structural checks; not a Google certification or a ranking prediction."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from collections import defaultdict
import xml.etree.ElementTree as ET
import json,re
ROOT=Path(__file__).resolve().parents[1]
HOST='https://www.salanproducciones.com'
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('.//s:loc',ns)]
assert len(urls)==len(set(urls))
pages={};titles=defaultdict(list)
for url in urls:
 assert url.startswith(HOST+'/') and not urlsplit(url).query and not urlsplit(url).fragment
 path=ROOT/urlsplit(url).path.lstrip('/')/'index.html';assert path.exists(),url
 s=path.read_text(encoding='utf-8-sig');page=Page(s);pages[url]=page
 canon=[a.get('href') for t,a in page.tags if t=='link' and a.get('rel')=='canonical'];assert canon==[url],(url,canon)
 desc=[a.get('content') for t,a in page.tags if t=='meta' and a.get('name')=='description'];assert len(desc)==1 and desc[0],url
 title=re.findall('<title>(.*?)</title>',s,re.S);assert len(title)==1 and title[0],url
 lang=next(a['lang'] for t,a in page.tags if t=='html');titles[(lang,title[0])].append(url)
 assert not any(t=='meta' and a.get('name')=='robots' and 'noindex' in a.get('content','') for t,a in page.tags),url
 for data in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):json.loads(data)
for url,page in pages.items():
 for t,a in page.tags:
  if t=='link' and a.get('rel')=='alternate':
   dest=a['href'];assert dest in pages,(url,dest)
   back=[x.get('href') for tag,x in pages[dest].tags if tag=='link' and x.get('rel')=='alternate'];assert url in back,(url,dest)
assert not [v for v in titles.values() if len(v)>1], [v for v in titles.values() if len(v)>1]
assert 'Sitemap: '+HOST+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
print(f'{len(urls)} sitemap URLs: existing pages, self canonicals, descriptions, unique titles per language, reciprocal hreflang and valid JSON-LD OK.')
