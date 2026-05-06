# Salán Producciones — Style Guide

## Tipografías unificadas

### Familias
- **Oswald** (400, 500, 600, 700): Titulares, headings, números, call-to-action
- **Inter** (300, 400, 500, 600): Cuerpo de texto, descripciones, metadatos

Importadas desde Google Fonts en `main.css`

## Escala de tamaños (using `clamp()` para fluidez)

### Títulos principales
- `.hero-title` / `.event-title`: `clamp(2.5rem, 5vw, 4rem)` → responsive 2.5rem–4rem
- `.section-title`: `clamp(1.8rem, 4vw, 2.8rem)` → responsive 1.8rem–2.8rem

### Subtítulos y descripciones
- `.hero-subtitle` / `.event-desc`: `clamp(1rem, 2.5vw, 1.1rem)` → responsive 1rem–1.1rem
- `.section-sub`: `clamp(1rem, 2.5vw, 1.1rem)` → matches subtitle

### Labels y metadatos
- `.section-label` / `.info-label`: `.72rem` (0.8rem for some)
- Letter-spacing: `.2em` (labels), `.1em` (info-label)
- Font-weight: 600 (semibold)

### Tamaños estadísticos
- `.hero-stat-num` / `.bio-stat-num`: `clamp(2rem, 4vw, 2.5rem)` → responsive
- `.hero-stat-label` / `.bio-stat-label`: `.72rem` (muted, uppercase)

## Estructura de color

**CSS Variables** (defined in `:root`):
- `--gold`: #e8c44d (acents, highlights)
- `--red`: #c0392b (danger, critical info)
- `--bg`: #0a0a0a (base background)
- `--bg2`: #111111 (alternate sections)
- `--bg3`: #1a1a1a (card backgrounds)
- `--border`: #2a2a2a (borders, dividers)
- `--text`: #e8e8e8 (primary text)
- `--muted`: #888888 (secondary text, descriptions)

## Componentes unificados

### Hero Sections
- `.hero-grid`: 2-column on desktop, 1-column mobile (≤768px)
- Padding: `120px 24px 80px` desktop, `100px 24px 40px` mobile
- Gap: `40px` desktop, `32px` mobile

### Info Grid (event details)
- `.info-grid`: 2-column on desktop, 1-column mobile (≤600px)
- Padding: `20px`, Gap: `20px`
- Background: `var(--bg3)`, Border: `1px solid var(--border)`

### Bio Cards
- `.bio-card`: 2fr/1fr split on desktop, 1-column mobile (≤768px)
- Padding: `40px` desktop, `32px 24px` mobile
- Gap: `40px` desktop, `32px` mobile

### Buttons
- `.btn-primary`: Gold background, uppercase, letter-spacing `.08em`
- `.btn-secondary`: Outline style, transparent bg, gold border on hover
- `.btn`: Default padding `12px 24px`, radius `4px`

### Call-to-Action Groups
- `.cta-group`: flex row on desktop, column on mobile (≤600px)
- Gap: `16px`, flex-wrap: wrap
- Mobile: full-width buttons

## Responsive Breakpoints

- **Desktop**: 768px+ (desktop nav, 2-column grids)
- **Tablet**: 600px–767px (2-column in some grids)
- **Mobile**: <600px (single column, full width)
- **Small Mobile**: <400px (optimizations for concert cards)

## Type C Gira — City Selector Component

Used on gira landings (multiple cities, one page). Replaces the old `.cities-grid` pattern.

### Hero layout
- Replace `.hero-grid` with `.tour-grid` (inline `<style>` block in `<head>`)
- Two columns desktop (1fr 1fr), single column mobile
- Left: `.tour-poster` — poster image
- Right: `.tour-info` — eyebrow → H1 → event-guest → pills header → pills → CTA box → description

### H1 rule for Type C
Must include the tour name, not just the artist:
- `Acantha Lang – Gira España Junio 2026`
- `Kenny "Blues Boss" Wayne Band` (already descriptive enough with gira subtitle)

### City pill buttons
```html
<div class="tour-active-label" style="margin-bottom: 12px;">Comprar entradas</div>
<div class="tour-cities" role="tablist" aria-label="Selecciona tu ciudad">
  <button class="tour-city-btn" data-id="sevilla" role="tab">4 Jun · Sevilla</button>
  ...
</div>
```
- Class: `.tour-city-btn[data-id]`
- Active state: gold background, black text, font-weight 700
- Pill shape: `border-radius: 100px`
- With date prefix when dates are known (e.g. `9 Sep · Donosti`), city name only when not

### Active city CTA box
```html
<div class="tour-active-city" id="tour-active-city">
  <div class="tour-active-label">Tu fecha</div>
  <div class="tour-active-name" id="tac-city">—</div>
  <div class="tour-active-date" id="tac-date">—</div>
  <div class="tour-active-venue" id="tac-venue">—</div>
  <a href="#" id="tac-btn" class="tour-buy-btn" target="_blank" rel="noopener">🎟 Comprar entradas</a>
</div>
```
- `.changing` class triggers `opacity: 0` fade during city switch (150ms timeout)

### JavaScript pattern
```javascript
(function() {
    const cities = {
        sevilla: { name: 'Sevilla', date: '4 de junio · 20:00h', venue: 'Sala Moon · Sevilla', url: '...' },
        // ...
    };
    function activate(id) {
        const c = cities[id];
        if (!c) return;
        document.querySelectorAll('.tour-city-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.id === id);
        });
        const box = document.getElementById('tour-active-city');
        box.classList.add('changing');
        setTimeout(() => {
            document.getElementById('tac-city').textContent  = c.name;
            document.getElementById('tac-date').textContent  = c.date;
            document.getElementById('tac-venue').textContent = c.venue;
            const btn = document.getElementById('tac-btn');
            btn.href = c.url;
            btn.textContent = '🎟 Comprar entradas';
            box.classList.remove('changing');
        }, 150);
        history.replaceState(null, '', '#' + id);  // hash without scroll jump
    }
    const hash = window.location.hash.replace('#', '');
    activate(cities[hash] ? hash : 'first-city-id');  // default to first city
    document.querySelectorAll('.tour-city-btn').forEach(btn => {
        btn.addEventListener('click', () => activate(btn.dataset.id));
    });
})();
```

### Ad targeting with URL hash
- Facebook/Instagram ad for Sevilla → `https://salanproducciones.com/conciertos/2026/{slug}/#sevilla`
- The JS reads `window.location.hash` on load and activates the matching city automatically

### Schema for Type C
Use an array of MusicEvent objects — one per city:
```json
[
  { "@context": "https://schema.org", "@type": "MusicEvent", "name": "Artist en City", "startDate": "...", "location": {...}, "offers": {...} },
  ...
]
```

---

## Animations & Transitions

- `.reveal`: Scroll-reveal animation (opacity + translateY)
  - Initial: `opacity: 0; transform: translateY(24px)`
  - Active: `opacity: 1; transform: none`
  - Transition: `.6s ease`

## Spacing System

All padding/margin values in multiples of 4px or 8px for consistency:
- **Sections**: 80px (desktop), 48px (mobile)
- **Cards**: 20–40px
- **Gaps**: 16px–64px depending on context
- **Bottom margins**: 12–40px for text elements

## Using `clamp()` for Typography

Benefits:
- Auto-scales between min and max sizes
- Smooth responsive behavior (no jumps at breakpoints)
- Less media queries needed
- Better mobile experience

Example: `clamp(min, preferred, max)`
- `clamp(2.5rem, 5vw, 4rem)` = min 2.5rem, ideal 5% viewport, max 4rem

## Integration Notes

- All concert landing pages (`/conciertos/2026/*/index.html`) use these unified styles
- Home page (`index.html`) also respects this system
- No inline styles except for accessibility or unique overrides
- All color values use CSS variables for maintainability

---

## SEO Checklist — obligatorio en cada landing nueva

Toda landing generada con `/salan` DEBE incluir estos elementos. No omitir ninguno.

### `<head>` — meta tags obligatorios

```html
<!-- og:url SIEMPRE absoluto, apuntando al slug de la landing -->
<meta property="og:url" content="https://www.salanproducciones.com/conciertos/2026/<slug>/">

<!-- og:title, og:description, og:image SIEMPRE presentes -->
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<!-- og:image SIEMPRE URL absoluta — nunca relativa -->
<meta property="og:image" content="https://www.salanproducciones.com/conciertos/2026/<slug>/poster.webp">

<!-- Twitter Card SIEMPRE presente — los 4 tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">         <!-- igual que og:title -->
<meta name="twitter:description" content="...">   <!-- igual que og:description -->
<meta name="twitter:image" content="https://www.salanproducciones.com/conciertos/2026/<slug>/poster.webp">

<!-- Canonical SIEMPRE al dominio final, no a vercel.app -->
<link rel="canonical" href="https://www.salanproducciones.com/conciertos/2026/<slug>/">
```

### H1 — regla obligatoria

- Tipo A (concierto único): `{Artista} en {Ciudad}` — nunca solo el nombre del artista
- Tipo B (ciudad separada): `{Artista} en {Ciudad}`
- Tipo C (gira): `{Artista} – {Nombre de gira o año}`

### Schema.org JSON-LD — reglas obligatorias

```json
{
  "@type": "MusicEvent",
  "startDate": "2026-MM-DDT20:00:00+01:00",
  "endDate":   "2026-MM-DDT23:00:00+01:00",
  "image": "https://www.salanproducciones.com/conciertos/2026/<slug>/poster.webp",
  "organizer": {
    "@type": "Organization",
    "name": "Salan Producciones",
    "url": "https://salanproducciones.com"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://...",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock"
  }
}
```

Reglas:
- `startDate` y `endDate` SIEMPRE con zona horaria `+01:00` y segundos (`:00`)
- `image` SIEMPRE URL absoluta
- Si no hay entradas disponibles aún: `"availability": "https://schema.org/PreOrder"` y omitir `price`
- Si hay precio conocido: incluir `"price": "25"` (string, sin €)
- No usar `@type: Event` — siempre `MusicEvent`

### Imágenes — reglas obligatorias

- El poster se guarda como `poster.webp` dentro de la carpeta del slug
- En el `<img>` del poster: `loading="eager"` (es above the fold)
- Siempre incluir `width` y `height` en el `<img>`
- No usar URLs de WordPress (`/wp-content/uploads/`)

### BreadcrumbList — obligatorio en cada landing

Añadir un segundo bloque `<script type="application/ld+json">` justo antes del `</head>`:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.salanproducciones.com/" },
    { "@type": "ListItem", "position": 2, "name": "{nombre del evento}", "item": "https://www.salanproducciones.com/conciertos/2026/<slug>/" }
  ]
}
```

### Después de crear la landing — acciones obligatorias

1. Añadir la card estática en `index.html` dentro de `#upcoming-grid`
2. Añadir la entrada en `conciertos.json` con la URL local del poster (`/conciertos/2026/<slug>/poster.webp`)
3. Hacer commit y push a `main`
