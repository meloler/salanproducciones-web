"""Generate localized, single-event pages from verified tour data and tour templates.
Run after editing data/kenny-tour-2026.json or a tour template; no network required.
"""
from pathlib import Path
import json,re,html,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
HOST='https://www.salanproducciones.com'
SLUG='kenny-blues-boss-wayne-gira-espana-2026'
PATHS={'es':f'/conciertos/2026/{SLUG}/','en':f'/en/concerts/2026/{SLUG}/','de':f'/de/konzerte/2026/{SLUG}/'}
COPY={
'es':dict(month='septiembre',tour='Gira España 2026',home='Inicio',buy='Comprar entradas',fees='Gastos de gestión incluidos',info='Información del concierto',back='Ver todas las ciudades',location='Dónde es el concierto',directions='Cómo llegar',minor='Acceso a partir de 16 años.',note='Consulta las condiciones de acceso en la ticketera.',description='Blues y boogie-woogie en directo con Kenny y su banda.',lead='Kenny «Blues Boss» Wayne Band en {city}',summary='Consulta las 10 fechas de Kenny Blues Boss Wayne Band en España, del 9 al 20 de septiembre de 2026. Horarios, salas y entradas con gastos incluidos.'),
'en':dict(month='September',tour='Spain Tour 2026',home='Home',buy='Buy tickets',fees='Booking fees included',info='Concert details',back='See all cities',location='Concert venue',directions='Get directions',minor='Admission ages 16 and over.',note='Check admission conditions with the ticket seller.',description='Live blues and boogie-woogie with Kenny and his band.',lead='Kenny “Blues Boss” Wayne Band in {city}',summary='Explore all 10 Kenny Blues Boss Wayne Band dates in Spain, 9–20 September 2026. Venues, start times and tickets with booking fees included.'),
'de':dict(month='September',tour='Spanien-Tour 2026',home='Startseite',buy='Tickets kaufen',fees='Vorverkaufsgebühren inklusive',info='Konzertdetails',back='Alle Städte ansehen',location='Veranstaltungsort',directions='Anfahrt',minor='Einlass ab 16 Jahren.',note='Einlassbedingungen beim Ticketanbieter prüfen.',description='Blues und Boogie-Woogie live mit Kenny und seiner Band.',lead='Kenny „Blues Boss“ Wayne Band in {city}',summary='Alle 10 Termine der Spanien-Tour von Kenny Blues Boss Wayne Band vom 9.–20. September 2026. Spielorte, Uhrzeiten und Tickets inklusive Gebühren.')}
DATA=json.loads((ROOT/'data/kenny-tour-2026.json').read_text())['cities']
def esc(x):return html.escape(str(x),quote=True)
def ld(obj):return '<script type="application/ld+json">\n'+json.dumps(obj,ensure_ascii=False,indent=2)+'\n</script>'
def breadcrumbs(lang,items):
 return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':url} for i,(name,url) in enumerate(items)]}
def metadata(s,title,description,url,alternates):
 s=re.sub(r'<title>.*?</title>','<title>'+esc(title)+'</title>',s,flags=re.S)
 for attr,key,value in [('name','description',description),('property','og:title',title),('property','og:description',description),('property','og:url',url),('name','twitter:title',title),('name','twitter:description',description)]:
  s=re.sub(r'<meta '+attr+'="'+key+r'"[^>]*>',f'<meta {attr}="{key}" content="{esc(value)}">',s)
 s=re.sub(r'<link rel="canonical"[^>]*>',f'<link rel="canonical" href="{url}">',s)
 for lang,path in alternates.items():s=re.sub(r'<link rel="alternate" hreflang="'+lang+r'"[^>]*>',f'<link rel="alternate" hreflang="{lang}" href="{HOST+path}">',s)
 return s
for lang,route in PATHS.items():
 t=COPY[lang];p=ROOT/route.strip('/')/'index.html';s=p.read_text(encoding='utf-8-sig')
 old=json.loads(re.search(r'<script id="kenny-dates" type="application/json">(.*?)</script>',s,re.S)[1]);localized={}
 for c in DATA:
  day=int(c['date'][-2:]);price=f"€{c['price']:.2f}" if lang=='en' else f"{c['price']:.2f}".replace('.',',')+' €'
  localized[c['id']]={**c,'dateLabel':f"{day}{'.' if lang=='de' else ''} {t['month']} 2026 · {c['time']}",'priceLabel':price,'note':t['minor'] if c['id']=='santiago' else t['note']}
 s=re.sub(r'(<script id="kenny-dates" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps(localized,ensure_ascii=False)+m[2],s,flags=re.S)
 # Collection pages expose a list of event URLs, never ten Event rich-results candidates.
 items=[{'@type':'ListItem','position':i+1,'name':t['lead'].format(city=c['name']),'url':HOST+route+c['id']+'/'} for i,c in enumerate(DATA)]
 s=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:ld({'@context':'https://schema.org','@type':'ItemList','itemListElement':items}),s,count=1,flags=re.S)
 scripts=list(re.finditer(r'<script type="application/ld\+json">.*?</script>',s,re.S))
 b=breadcrumbs(lang,[(t['home'],HOST+('/' if lang=='es' else '/'+lang+'/')),(t['tour'],HOST+route)])
 m=scripts[1];s=s[:m.start()]+ld(b)+s[m.end():]
 s=metadata(s,'Kenny Blues Boss Wayne · '+t['tour']+' | Salán',t['summary'],HOST+route,{**PATHS,'x-default':PATHS['es']})
 # Root list keeps direct tickets and adds useful, crawlable detail links.
 links=[]
 for c in localized.values():
  links.append(f'<li><a href="{c["url"]}" data-ticket-city="{c["id"]}" target="_blank" rel="noopener noreferrer"><strong>{c["name"]}</strong><span>{c["dateLabel"]} · {c["venue"]}</span><span>{c["priceLabel"]} · {t["fees"]} ↗</span></a><a class="event-details-link" href="{route+c["id"]}/">{t["info"]}: {c["name"]} →</a></li>')
 s=re.sub(r'(<details class="tour-dates">.*?<ul>).*?(</ul></details>)',lambda m:m[1]+''.join(links)+m[2],s,count=1,flags=re.S)
 p.write_text(s)
 for c in localized.values():
  cityroute=route+c['id']+'/';url=HOST+cityroute;title=t['lead'].format(city=c['name'])
  desc=f"{c['venue']} · {c['dateLabel']}. {t['description']} {c['priceLabel']} · {t['fees']}."
  page=metadata(s,title+' · 2026 | Salán',desc,url,{**{l:r+c['id']+'/' for l,r in PATHS.items()},'x-default':PATHS['es']+c['id']+'/'})
  event={'@context':'https://schema.org','@type':'MusicEvent','@id':url+'#event','url':url,'name':title,'description':desc,'startDate':c['date']+'T'+c['time']+':00+02:00','eventStatus':'https://schema.org/EventScheduled','eventAttendanceMode':'https://schema.org/OfflineEventAttendanceMode','location':{'@type':'Place','name':c['venue'],'address':{'@type':'PostalAddress',**c['address']}},'image':HOST+PATHS['es']+'poster-1024.webp','organizer':{'@type':'Organization','name':'Salán Producciones','url':HOST+'/'},'performer':{'@type':'MusicGroup','name':'Kenny “Blues Boss” Wayne Band'},'offers':{'@type':'Offer','url':c['url'],'price':f"{c['price']:.2f}",'priceCurrency':'EUR','availability':'https://schema.org/InStock'}}
  page=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:ld(event),page,count=1,flags=re.S)
  scripts=list(re.finditer(r'<script type="application/ld\+json">.*?</script>',page,re.S));m=scripts[1]
  b=breadcrumbs(lang,[(t['home'],HOST+('/' if lang=='es' else '/'+lang+'/')),(t['tour'],HOST+route),(c['name'],url)])
  page=page[:m.start()]+ld(b)+page[m.end():]
  page=re.sub(r'(<h1[^>]*>).*?(</h1>)',lambda m:m[1]+esc(title)+m[2],page,count=1,flags=re.S)
  page=re.sub(r'<div class="tour-selector".*?</div>','',page,count=1,flags=re.S)
  page=re.sub(r'<details class="tour-dates">.*?</details>',f'<a class="tour-video-link" href="{route}#{c["id"]}">← {t["back"]}</a>',page,count=1,flags=re.S)
  page=re.sub(r'(<script id="kenny-dates" type="application/json">).*?(</script>)',lambda m:m[1]+json.dumps({c['id']:c},ensure_ascii=False)+m[2],page,flags=re.S)
  for id,value in [('tac-city',c['name']),('tac-date',c['dateLabel']),('tac-venue',c['venue']),('tac-price',c['priceLabel']),('tac-note',c['note']),('sticky-city',c['name']),('sticky-date',c['dateLabel'])]:
   page=re.sub(r'(<[^>]+id="'+id+r'"[^>]*>).*?(</[^>]+>)',lambda m:m[1]+esc(value)+m[2],page,count=1,flags=re.S)
  page=re.sub(r'href="[^"]*" id="tac-btn"',f'href="{c["url"]}" id="tac-btn"',page)
  page=re.sub(r'id="sticky-buy" href="[^"]*"',f'id="sticky-buy" href="{c["url"]}"',page)
  # Avoid repeating the tour-wide SEO copy and final CTA on a single-event page.
  a=page.index('<!-- FINAL CTA -->');z=page.index('<!-- FOOTER -->',a) if '<!-- FOOTER -->' in page[a:] else page.index('<footer',a)
  address=c['address'];visible=f"{address['streetAddress']} · {address['postalCode']} {address['addressLocality']}"
  from urllib.parse import quote
  venue=f'<section class="section"><h2>{t["location"]}: {c["venue"]}</h2><p>{esc(visible)}</p><p>{esc(desc)}</p><a href="https://www.google.com/maps/search/?api=1&amp;query={quote(visible)}" target="_blank" rel="noopener noreferrer">{t["directions"]} ↗</a><p><a href="{route}#{c["id"]}">{t["back"]}</a></p></section>\n'
  page=page[:a]+venue+page[z:]
  # The hero must describe this performance, not a schedule of ten events.
  page=re.sub(r'<p class="event-guest">.*?</p>',f'<p class="event-guest">{c["venue"]}<br>{c["dateLabel"]}</p>',page,count=1,flags=re.S)
  page=page.replace('Diez ciudades para disfrutar de una noche de música en sala.','').replace('Ten cities for a night of music up close.','').replace('Zehn Städte für einen Konzertabend ganz nah an der Musik.','')
  dest=ROOT/cityroute.strip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(page)
# Sitemap preserves existing entries and reciprocal language alternates.
p=ROOT/'sitemap.xml';s=p.read_text()
city_urls={HOST+r+c['id']+'/' for r in PATHS.values() for c in DATA}
s=re.sub(r'<url>.*?</url>',lambda m:'' if re.search(r'<loc>(.*?)</loc>',m[0])[1] in city_urls else m[0],s,flags=re.S)
s=re.sub(r'\n[ \t]*\n', '\n', s)

new=[]
for c in DATA:
 alts={**{l:r+c['id']+'/' for l,r in PATHS.items()},'x-default':PATHS['es']+c['id']+'/'}
 for route in PATHS.values():
  links='\n'.join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{HOST+r}" />' for l,r in alts.items())
  new.append(f'  <url>\n    <loc>{HOST+route+c["id"]}/</loc>\n{links}\n  </url>')
s=s.replace('</urlset>','\n'.join(new)+'\n</urlset>')
s='\n'.join(line.rstrip() for line in s.splitlines() if line.strip())+'\n'
p.write_text(s)
print('Generated 30 single-event pages, three tour lists and sitemap entries.')
