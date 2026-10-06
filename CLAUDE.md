# Salán Producciones — Briefing para IA

Proyecto web estático de **Salán Producciones**, empresa de promoción musical fundada por Juan Salán en Las Palmas de Gran Canaria. El sitio anuncia conciertos, vende entradas y documenta el legado de la sala Pub La Calle (1988–2000).

- **Dominio**: https://www.salanproducciones.com
- **Hosting**: Vercel (rama `main` de GitHub → deploy automático)
- **Repo**: https://github.com/meloler/salanproducciones-web
- **Stack**: HTML estático + CSS (`/assets/css/main.css`) + JS mínimo (`/assets/js/main.js`)
- **Tipografías**: Oswald (títulos) + Inter (cuerpo) — Google Fonts
- **Sin frameworks, sin build step, sin npm**

---

## Si recibes un cartel de concierto → ejecuta `/salan`

Cuando el usuario te pase una **imagen de cartel** (con o sin URL de entradas), tu tarea es crear la landing page completa. Usa la skill:

```
/salan
```

La skill está en `.claude/skills/salan/SKILL.md` y contiene el flujo completo paso a paso.  
Antes de generar HTML, lee siempre:
1. `STYLE_GUIDE.md` — clases CSS, escala tipográfica, tokens de color
2. `conciertos/2026/bywater-call-17-06-2026/index.html` — template canónico

---

## Flujo vigente de cambios y publicación

- Trabajar en una rama `codex/...` y conservar cualquier cambio local existente.
- Preparar y revisar una preview de Vercel antes de presentar cambios visibles.
- Un push a `main` actualiza producción. Hacerlo únicamente cuando Juan haya autorizado publicar el lote concreto.
- Para conciertos, leer `STYLE_GUIDE.md` y `GUIA-MULTIDIOMA.md`; comprobar el feed y el HTML estático para conservar el acceso sin JavaScript.

## Estructura del proyecto

```
/
├── index.html                          ← Homepage (lista de próximos conciertos)
├── conciertos-anteriores/index.html    ← Archivo histórico
├── pub-la-calle/index.html             ← Historia del Pub La Calle
├── contacto/index.html                 ← Formulario de contacto
├── conciertos/2026/<slug>/             ← Landing por concierto
│   ├── index.html
│   └── poster.webp
├── assets/
│   ├── css/main.css                    ← Único archivo CSS — dark/rock aesthetic
│   ├── js/main.js
│   └── images/
├── STYLE_GUIDE.md                      ← ⬅ Leer antes de tocar CSS o HTML
└── CLAUDE.md                           ← Este archivo
```

---

## Tipos de landing (importante)

### Tipo A — Concierto único
- 1 landing, 1 slug: `artista-dd-mm-yyyy`
- Bio estándar (2 párrafos)
- 1 card en homepage

### Tipo B — Mismo artista, fechas separadas por ciudad
- **N landings separadas**, una por ciudad
- Slug por ciudad: `artista-ciudad-dd-mm-yyyy`
- Párrafo 2 de bio **único por ciudad** (evita penalización SEO por contenido duplicado)
- Cross-links entre fechas en el final CTA
- N cards en homepage

### Tipo C — Gira, varias ciudades en una sola página
- 1 landing con grid de fechas
- Anchor ID por ciudad: `#madrid`, `#bilbao`, etc.
- Útil para anuncios segmentados: `landing-url#madrid`
- Schema.org: array de MusicEvent (uno por ciudad)

---

## Reglas SEO obligatorias en toda landing

- `<link rel="canonical">` apuntando a sí misma
- Schema.org `@type: MusicEvent` (no `Event`) con `offers`, `performer`, `organizer`
- UTMs en todos los CTAs: `?utm_source=landing&utm_medium=web&utm_campaign=<slug>`
- Meta description única por página
- H1 único: "{Artista} en {Ciudad}" (no solo el nombre del artista)

---

## Organizer siempre igual

```json
"organizer": {
  "@type": "Organization",
  "name": "Salan Producciones",
  "url": "https://salanproducciones.com"
}
```

---

## GitHub

La carpeta y el comando de publicación que aparecían en versiones anteriores de este briefing están obsoletos. El flujo vigente está descrito al principio de este archivo: rama de trabajo, preview y autorización expresa antes de publicar en `main`.
