# Metodologia para crear landings de conciertos

Este es el procedimiento unico vigente para crear o actualizar landings de conciertos en Salan Producciones.

Si otro documento del proyecto contradice este flujo, manda este documento. Los archivos `PROTOCOLO-NUEVOS-CONCIERTOS.md`, `CHEAT-SHEET-conciertos.txt` y `conciertos/README.md` quedan solo como referencia historica.

Objetivo: que Juan pueda pasar solo el cartel del concierto y la URL de venta, y que la IA cree una landing completa, coherente con Salan Producciones, sin inventar estructura ni estilo.

Antes de tocar archivos, leer siempre:

1. `AGENTS.md` o `CLAUDE.md`, segun el agente usado.
2. `STYLE_GUIDE.md`.
3. `conciertos/2026/bywater-call-17-06-2026/index.html`, como template canonico para concierto individual.
4. Una landing de gira si el cartel incluye varias ciudades:
   - `conciertos/2026/acantha-lang-tour-espana-28-06-2026/index.html`
   - `conciertos/2026/kenny-blues-boss-wayne-gira-espana-2026/index.html`

---

## Entradas minimas que debe pasar Juan

Para concierto individual:

- Cartel del concierto.
- URL de venta de entradas.

Para gira o varias ciudades:

- Cartel de la gira.
- URL de venta principal o URLs por ciudad, si existen.

Si falta algun dato critico que no se pueda leer del cartel ni de la URL de venta, la IA debe preguntar solo lo imprescindible: normalmente ciudad/sala, fecha, hora o precio.

---

## Lo que debe extraer la IA

Del cartel:

- Artista o nombre del festival.
- Fecha.
- Ciudad.
- Recinto.
- Hora, si aparece.
- Precio, si aparece.
- Artistas invitados o lineup.
- Promotores o colaboradores, solo si son relevantes para el texto.

De la URL de venta:

- Titulo oficial del evento.
- Precio real o rango de precios.
- Fecha/hora confirmada.
- Recinto y ciudad.
- Estado de entradas: a la venta, proximamente, agotado.

De investigacion musical necesaria:

- Bio breve y fiable del artista.
- Genero musical.
- 2 o 3 argumentos de venta reales.
- Video de YouTube adecuado para incrustar:
  - Preferencia 1: video oficial reciente.
  - Preferencia 2: directo de buena calidad.
  - Preferencia 3: tema mas reconocible si no hay directo bueno.

No inventar premios, colaboraciones, aforos, invitados ni precios.

---

## Decision: que tipo de landing crear

### Tipo A - Concierto individual

Usar cuando hay una fecha y una ciudad.

Estructura:

- 1 carpeta: `conciertos/2026/<artista-ciudad-dd-mm-yyyy>/`
- 1 `index.html`
- Poster responsive: `poster.webp`, `poster-320.webp`, `poster-480.webp`, `poster-768.webp`, `poster-1024.webp`
- 1 card en `index.html`
- 1 entrada en `conciertos.json`

H1 obligatorio:

`{Artista} en {Ciudad}`

### Tipo B - Mismo artista con fechas separadas

Usar cuando el mismo artista tiene varias fechas, pero cada ciudad necesita su propia landing.

Estructura:

- Una carpeta por ciudad.
- H1 unico por ciudad.
- Meta description unica por ciudad.
- Parrafo local unico por ciudad.
- Cross-link entre fechas relacionadas.

Ejemplo real:

- `bywater-call-16-06-2026`
- `bywater-call-17-06-2026`

### Tipo C - Gira en una sola landing

Usar cuando el cartel o la venta se entiende como gira conjunta.

Estructura:

- Una carpeta de gira.
- Selector de ciudades.
- Anchor por ciudad: `#madrid`, `#bilbao`, etc.
- Schema.org con un `MusicEvent` por ciudad.
- Una sola card en `index.html`.

Ejemplos reales:

- `acantha-lang-tour-espana-28-06-2026`
- `kenny-blues-boss-wayne-gira-espana-2026`

H1 obligatorio:

`{Artista} - {Nombre de gira o ano}`

---

## Estructura visual obligatoria

Para landings individuales, seguir el patron de Bywater Call:

- Header comun del sitio.
- Hero con poster a la izquierda y contenido a la derecha.
- Badge superior con fecha o tipo de evento.
- H1.
- Subtitulo breve.
- Grid de informacion:
  - Fecha
  - Hora
  - Recinto
  - Ciudad
  - Precio o estado de entradas
- CTA principal de compra.
- Video incrustado con `lite-youtube`.
- Seccion bio/contexto del artista.
- Seccion de por que verlo en directo.
- CTA final.
- Bloque de Salan Producciones.
- Footer comun.

Para giras, seguir el patron Acantha/Kenny:

- Hero con cartel.
- Selector de ciudad.
- Boton de compra que cambia segun la ciudad activa.
- Grid/listado de fechas.
- Video.
- Bio.
- CTA final.

---

## SEO obligatorio

Cada landing debe incluir:

- `<link rel="canonical">` apuntando a su URL final.
- Meta title unico.
- Meta description unica.
- Open Graph completo.
- Twitter Card completo.
- Schema.org `MusicEvent`, no `Event`.
- `organizer` fijo:

```json
{
  "@type": "Organization",
  "name": "Salan Producciones",
  "url": "https://salanproducciones.com"
}
```

- `BreadcrumbList`.
- CTAs con UTMs:

`?utm_source=landing&utm_medium=web&utm_campaign=<slug>`

Si la URL ya tiene parametros, usar `&utm_source=...`.

---

## Imagenes obligatorias

Guardar siempre dentro de la carpeta del concierto:

- `poster.webp`
- `poster-320.webp`
- `poster-480.webp`
- `poster-768.webp`
- `poster-1024.webp`

Reglas:

- El poster del hero usa `loading="eager"` y `fetchpriority="high"`.
- Incluir siempre `width` y `height`.
- Usar `srcset` cuando existan variantes.
- No depender de imagenes externas.
- No usar imagenes antiguas de WordPress.

---

## Video

Cada landing debe tener un video salvo que no exista material razonable.

Reglas:

- Usar `lite-youtube`.
- No usar iframe directo.
- Elegir video oficial o directo de calidad.
- El titulo del video debe describir claramente artista y tipo de video.

Ejemplo:

```html
<lite-youtube videoid="VZzDyTz46zQ" title="Bywater Call - video en directo"></lite-youtube>
```

---

## Textos

La IA debe escribir textos utiles para vender la entrada, no textos genericos.

Contenido minimo:

- Intro corta con artista, ciudad, sala y fecha.
- Bio de 2 parrafos.
- Parrafo local si hay ciudad concreta.
- Motivos para comprar: directo, trayectoria, estilo, rareza de la fecha, sala.
- CTA final claro.

Tono:

- Profesional, musical y cercano.
- Rock/blues/soul/live music.
- Sin exageraciones no verificadas.
- Sin frases vacias tipo "una experiencia unica e inolvidable" si no aportan nada.

---

## Archivos que se actualizan

Siempre:

- `conciertos/2026/<slug>/index.html`
- `en/concerts/2026/<slug>/index.html`
- `de/konzerte/2026/<slug>/index.html`
- `conciertos/2026/<slug>/poster*.webp`
- `index.html`
- `proximos-conciertos/index.html`
- `conciertos.json`
- `concerts.en.json`
- `concerts.de.json`
- `sitemap.xml`

Si el evento sustituye o corrige uno existente:

- Revisar enlaces cruzados.
- Revisar `conciertos-anteriores/index.html` solo si aplica.

---

## Validacion antes de entregar

Checklist obligatorio:

- La landing abre correctamente en local.
- Las versiones ES, EN y DE abren correctamente.
- El selector ES | EN | DE apunta a la pagina equivalente.
- El poster se ve.
- El video carga.
- Todos los CTAs de compra funcionan y tienen UTM.
- H1 cumple la regla del tipo de landing.
- Canonical correcto.
- Hreflang reciproco entre ES, EN, DE y x-default.
- Schema.org usa `MusicEvent`.
- `conciertos.json`, `concerts.en.json` y `concerts.de.json` contienen el evento.
- `index.html` y `proximos-conciertos/index.html` muestran la card.
- No quedan placeholders.
- No hay texto inventado.
- La fecha no esta caducada para "proximos conciertos".

## Regla multidioma

La version espanola sigue siendo la fuente principal, pero cada concierto nuevo debe publicarse tambien en ingles y aleman como paginas estaticas reales. No usar widgets de traduccion automatica ni publicar traducciones sin revisar.

Ver `GUIA-MULTIDIOMA.md` para la estructura, SEO internacional y checklist especifico.

---

## Flujo ideal para Juan

Juan envia:

1. Cartel.
2. URL de venta.

La IA responde con una confirmacion breve:

"Recibido. Voy a crear la landing, sacar los datos del cartel y la venta, buscar un video adecuado y dejarla enlazada en la web."

La IA trabaja y entrega:

- URL local de la landing.
- Resumen de lo creado.
- Datos que no haya podido confirmar, si los hubiera.
- Confirmacion de si hizo commit/push, cuando Juan lo pida o cuando el flujo lo requiera.
