import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the grid section
match = re.search(r'<div class="concerts-grid">(.*?)</div>\s*</section>', html, re.DOTALL)
if match:
    grid_html = match.group(1)
    
    # Extract each card
    cards = re.findall(r'<article class="concert-card">(.*?)</article>', grid_html, re.DOTALL)
    
    concerts = []
    for card in cards:
        # Extract link
        link_match = re.search(r'<a href="(.*?)" class="concert-link">', card)
        link = link_match.group(1) if link_match else ""
        
        # Extract image
        img_match = re.search(r'<img src="(.*?)"', card)
        img = img_match.group(1) if img_match else ""
        
        # Extract date
        date_match = re.search(r'<div class="concert-date">(.*?)</div>', card, re.DOTALL)
        date_str = date_match.group(1).strip() if date_match else ""
        # clean date
        date_str = re.sub(r'<[^>]+>', ' ', date_str).replace('&nbsp;', ' ').strip()
        date_str = re.sub(r'\s+', ' ', date_str)
        
        # Extract title
        title_match = re.search(r'<h3 class="concert-title">(.*?)</h3>', card, re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""
        
        # Extract venue
        venue_match = re.search(r'<div class="concert-venue">(.*?)</div>', card, re.DOTALL)
        venue = venue_match.group(1).strip() if venue_match else ""
        venue = re.sub(r'<[^>]+>', ' ', venue).strip()
        
        # We need an ISO date for sorting/filtering. We will have to guess it from the link or date_str
        iso_date = "2026-01-01" # placeholder
        if "2026" in link:
            # extract dd-mm-yyyy from link like bywater-call-17-06-2026
            date_part = re.search(r'(\d{2}-\d{2}-2026)', link)
            if date_part:
                d, m, y = date_part.group(1).split('-')
                iso_date = f"{y}-{m}-{d}"
                
        concerts.append({
            "id": link.strip('/').split('/')[-1],
            "title": title,
            "dateDisplay": date_str,
            "dateISO": iso_date,
            "venue": venue,
            "image": img,
            "link": link
        })
        
    with open('conciertos.json', 'w', encoding='utf-8') as f:
        json.dump(concerts, f, indent=2, ensure_ascii=False)
    print(f'Extracted {len(concerts)} concerts to conciertos.json')
else:
    print('Grid not found')
