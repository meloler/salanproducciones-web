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
